from numpy import *
import calendar
import subprocess
import os
import matplotlib.pyplot as plt
import cf
import jra_func
import ctrack_func
import sys


iyear    = 2000
eyear    = 2004
imon     = 1
emon     = 12
tstp     = "mon"
#idir_root   =  "/home/utsumi/mnt/export/nas12/JRA25"
idir_root   =  "/media/disk2/data/JRA25/gr/mon"
odir_root   =  "/media/disk2/data/JRA25/sa.one/%s"%(tstp)
singleday   = False  # True or False
#singleday   = True  # True or False
miss_out    = -9999.0

lvar = ["WTMPsfc"]
for var in lvar:
  dtype  = {}
  dtype["WTMPsfc"] = "fcst_phy2m"
  
  lvar_2d    = ["WTMPsfc"]
  lvar_700mb = ["UGRD", "VGRD"]
  lvar_nonegative = ["PRMSL", "ACPCP", "NCPCP"]
  lvar_prec  = ["ACPCP", "NCPCP"]
  
  ctlname    = idir_root + "/%s.monthly.ctl"%(dtype[var])
  #--- LAT & LON & NX, NY : Original  ------------------------------
  if dtype[var] in ["anal_p25"]:
    dlat_org      = 2.5
    dlon_org      = 2.5
  
    lat_first_org = -90.0
    lat_last_org  = 90.0
    lon_first_org = 0.0
    lon_last_org  = 360.0 - 2.5
    a1lat_org     = arange(lat_first_org, lat_last_org + dlat_org*0.1, dlat_org)  
  
  elif var in lvar_2d:
    dlon_org      = 1.125
  
    lon_first_org = 0.0
    lon_last_org  = lon_first_org + dlon_org*(320-1) + dlon_org*0.1
    #a1lat_org     = array( jra_func.read_llat(ctlname, dtype[var]))
    a1lat_org     = array( jra_func.read_llat(ctlname))
  
  elif var in lvar_700mb:  
    dlat_org      = 2.5
    dlon_org      = 2.5
  
    lat_first_org = -90.0
    lat_last_org  = 90.0
    lon_first_org = 0.0
    lon_last_org  = 360.0 - 2.5
    a1lat_org     = arange(lat_first_org, lat_last_org + dlat_org*0.1, dlat_org)  
  #-----------
  a1lon_org     = arange(lon_first_org, lon_last_org + dlon_org*0.1, dlon_org)
  
  #---------------------------------------------------------------
  ny_org     = len(a1lat_org)
  nx_org     = len(a1lon_org)
  
  print ny_org, nx_org
  
  #-- modify a1lat_rog for interpolation at polar region --
  a1lat_org[0]  = -90.0
  a1lon_org[-1] = 90.0
  
  
  #--- LAT & LON & NX, NY : After Interpolation  ------------------
  dlat_fin   = 1.0
  dlon_fin   = 1.0
  a1lat_fin  = arange(-90.0+dlat_fin*0.5, 90.0 - dlat_fin*0.5 + dlat_fin*0.1, dlat_fin)
  a1lon_fin  = arange(0.0+dlon_fin*0.5, 360.0 - dlon_fin*0.5 + dlon_fin*0.1, dlon_fin)
  
  ny_fin     = len(a1lat_fin)
  nx_fin     = len(a1lon_fin)
  nz_fin     = 1
  #********************************************
  def mk_dir(sdir):
    if not os.access(sdir , os.F_OK):
      os.mkdir(sdir)
  #********************************************
  stype      = dtype[var]

  #******************************************************
  #--- search varname from ctl file -----------------
  f = open(ctlname, "r")
  lines = f.readlines()
  f.close()
  for i in range(len(lines)):
    line = lines[i]
    line = line.split(" ")
    #--------
    if line[0] == "vars":
      break
  #---
  nhead = i
  ivar  = -1
  for line in lines[nhead+1:]:
    ivar  = ivar + 1
    line  = line.split(" ")  
    if line[0].strip() == var:
      break
    if line[0].strip() == "ENDVARS":
      print "no varname:",var
      sys.exit()
  #-----------------------------------
  #-----------------------------------
  for year in range(iyear, eyear + 1):
    for mon in range(imon, emon + 1):
      idir      = idir_root
      odir_temp = odir_root  +  "/%s"%(var)
      odir      = odir_temp  +  "/%04d"%(year)
      #-- make directory ---
      mk_dir(odir_temp)
      mk_dir(odir)
  
  
      #-- discription file ----------------
      #< dims >
      sout   = "lev %d\nlat %d\nlon %d"%(nz_fin, ny_fin, nx_fin)
      f      = open( odir + "/dims.txt", "w")
      f.write(sout)
      f.close()
  
      #< lat >
      sout   = "\n".join(map( str, a1lat_fin))
      f      = open( odir + "/lat.txt", "w")
      f.write(sout)
      f.close()
  
      #< lon >
      sout   = "\n".join(map( str, a1lon_fin))
      f      = open( odir + "/lon.txt", "w")
      f.write(sout)
      f.close()
  
      #< dump >
      subprocess.call("cp %s %s/"%(ctlname, odir), shell=True)
      #
      stime     = "%04d%02d"%(year, mon)
      #----- Names ------------
      grname    = idir + "/%s.%s.gr"%(stype, stime)
      oname     = odir + "/%s.%s.%s.sa.one"%(stype, var, stime)
      #-------------------------
      if not os.access(grname, os.F_OK):
        print "no file", grname
        sys.exit
      #-------------------------
      print grname  
      #-- Interpolation and Flipud --------
      a2org     = fromfile(grname, float32).byteswap().reshape(-1,ny_org, nx_org)[ivar]
      #
      if var in lvar_nonegative:
        a2org   = ma.masked_less(a2org, 0.0).filled(miss_out)
      #
      a2fin     = cf.biIntp( a1lat_org, a1lon_org, a2org, a1lat_fin, a1lon_fin, miss = miss_out)[0]
  
      #-- change unit [kg m-2] -> [kg m-2 s-1] ---
      if var in lvar_prec:
        coef    = 1.0/(60.0*60.0*24.0)
        a2fin   = ma.masked_equal(a2fin , miss_out) * coef
        a2fin   = a2fin.filled(0.0)
      #
      a2fin.tofile( oname ) 
      print oname
  
      #------------------------------------




