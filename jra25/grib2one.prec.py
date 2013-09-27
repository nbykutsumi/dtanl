from numpy import *
import calendar
import subprocess
import os
import matplotlib.pyplot as plt
import cf
import jra_func
import ctrack_func

iyear    = 2005
eyear    = 2011
imon     = 1
emon     = 12
tstp     = "6hr"
sresol   = "fcst_phy2m"
#idir_root   =  "/home/utsumi/mnt/export/nas12/JRA25"
idir_root   =  "/home/utsumi/mnt/iis.data2/JRA25"
odir_root   =  "/media/disk2/data/JRA25/sa.one.%s/%s"%(sresol,tstp)
singleday   = False  # True or False
#singleday   = True  # True or False
miss_out    = -9999.0

#lvar = ["ACPCP", "NCPCP"]
lvar = ["NCPCP"]
#lvar = ["WTMP"]
for var in lvar:
  dtype  = {}
  dtype["ACPCP"] = "fcst_phy2m"
  dtype["NCPCP"] = "fcst_phy2m"
  
  lvar_2d    = ["ACPCP", "NCPCP"]
  ctlname    = idir_root + "/%s/%04d01/%s.ctl"%(dtype[var], iyear, dtype[var])
  #--- LAT & LON & NX, NY : Original  ------------------------------
  dlon_org      = 1.125
  lon_first_org = 0.0
  lon_last_org  = lon_first_org + dlon_org*(320-1) + dlon_org*0.1
  #a1lat_org     = array( jra_func.read_llat(ctlname, dtype[var]))
  a1lat_org     = array( jra_func.read_llat(ctlname))
  
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
  for year in range(iyear, eyear + 1):
    for mon in range(imon, emon + 1):
      idir      = idir_root  +  "/%s/%04d%02d"%(sresol,year, mon)
      odir_temp = odir_root  +  "/%s"%(var)
      odir      = odir_temp  +  "/%04d%02d"%(year, mon)
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
      tempname = idir + "/%s.%04d%02d0100"%(stype, year, mon)
      dumpname = odir + "/dump.txt"
  
      ptemp  = subprocess.call("wgrib -V %s | grep -A 6 %s > %s"%(tempname, var, dumpname), shell=True)
      #---------
      eday  = calendar.monthrange(year, mon)[1]
      if singleday == True:
        eday   = 1
      #-----------------
      for day in range(1, eday+1):
      #for day in range(28, eday+1):
        #---
        if singleday == True:
          print "*****************"
          print "   single day !!"
          print "*****************"
        #---
        print year, mon, day 
        for hour in [0, 6, 12, 18]:
          stime     = "%04d%02d%02d%02d"%(year, mon, day, hour)
          #----- Names ------------
          gribname  = idir + "/%s.%s"%(stype, stime)
          tempname  = odir + "/%s.%s.%s.temp.sa.one"%(stype, var,  stime)
          oname     = odir + "/%s.%s.%s.sa.one"%(stype, var, stime)
  
          print gribname
  
  
          #-- grib --> binary -----
  
          args      = "wgrib %s | grep %s | wgrib %s -i -nh -o %s"%(gribname, var, gribname, tempname)
          ptemp     = subprocess.call(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
          
          #-- Interpolation and Flipud --------
          a2org     = flipud(fromfile(tempname, float32).reshape(ny_org, nx_org))
          #
          a2org   = ma.masked_less(a2org, 0.0).filled(miss_out)
          #
          a2fin     = cf.biIntp( a1lat_org, a1lon_org, a2org, a1lat_fin, a1lon_fin, miss = miss_out)[0]
  
          #-- change unit [kg m-2] -> [kg m-2 s-1] ---
          coef    = 1.0/(60.0*60.0*24.0)
          a2fin   = ma.masked_equal(a2fin , miss_out) * coef
          a2fin   = a2fin.filled(0.0)
          #
          a2fin.tofile( oname ) 
          print oname
          
  
          ##-- delete temp file ----------------
          os.remove(tempname)
          #------------------------------------




