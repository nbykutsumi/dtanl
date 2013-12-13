from numpy import *
import calendar
import subprocess
import os, sys
import matplotlib.pyplot as plt
import cf
import jra_func
import ctrack_func

iyear    = 1987
eyear    = 1995
#lmon     = [1]
lmon     = arange(1,12+1)
tstp     = "6hr"
singleday   = False  # True or False
miss_out    = -9999.0

stype = "anl_p"
lvar  = ["PRMSL"]
lvar_nonegative = ["PRMSL"]

#--- LAT & LON & NX, NY : Original  ------------------------------
if stype == "anl_p":
  dlat_org      = 1.25
  dlon_org      = 1.25

lat_first_org = -90.0
lat_last_org  = 90.0
lon_first_org = 0.0
lon_last_org  = 360.0 - dlon_org
a1lat_org     = arange(lat_first_org, lat_last_org + dlat_org*0.1, dlat_org)  
#-----------
a1lon_org     = arange(lon_first_org, lon_last_org + dlon_org*0.1, dlon_org)

#-----------
idir_root   =  "/home/utsumi/mnt/iis.data2/JRA25"


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
#********************************************
for year in range(iyear, eyear + 1):
  for mon in lmon:
    for var in lvar:
      ctlname    = idir_root + "/%s/%04d01/%s.ctl"%(stype, iyear, stype)
      idir      = idir_root  +  "/%s/%04d%02d"%(stype, year, mon)

      odir_root =  "/media/disk2/data/JRA25/sa.one.%s/%s"%(stype, tstp)
      odir_temp = odir_root  +  "/%s"%(var)
      odir      = odir_temp  +  "/%04d%02d"%(year, mon)
      #-- make directory ---
      ctrack_func.mk_dir(odir_root)
      ctrack_func.mk_dir(odir_temp)
      ctrack_func.mk_dir(odir)
    
    
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
          tempname  = odir + "/%s.%s.%s.temp.sa.one"%(stype, var, stime)
          oname     = odir + "/%s.%s.%s.sa.one"%(stype, var, stime)
    
          print gribname
          if not os.access(gribname, os.F_OK): 
            print "no file"
            print gribname
            sys.exit()
          #-- grib --> binary -----
    
          args      = "wgrib %s | grep %s | wgrib %s -i -nh -o %s"%(gribname, var, gribname, tempname)
           
          #print args
          ptemp     = subprocess.call(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
          
          #-- Interpolation and Flipud --------
          a2org     = flipud(fromfile(tempname, float32).reshape(ny_org, nx_org))
          #
          if var in lvar_nonegative:
            a2org   = ma.masked_less(a2org, 0.0).filled(miss_out)
          #
          a2fin     = cf.biIntp( a1lat_org, a1lon_org, a2org, a1lat_fin, a1lon_fin, miss = miss_out)[0]
    
          #
          a2fin.tofile( oname ) 
          print tempname
    
          
    
          ##-- delete temp file ----------------
          os.remove(tempname)
          #------------------------------------
  



