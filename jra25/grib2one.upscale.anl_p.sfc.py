from numpy import *
import calendar
import subprocess
import os, sys
import matplotlib.pyplot as plt
import cf
import jra_func
import ctrack_func
from myfunc_fsub import *
#---------------
if len(sys.argv) >1:
  iyear  = int(sys.argv[1])
  eyear  = iyear
  mon    = int(sys.argv[2])
  model  = sys.argv[3]
  var    = sys.argv[4]
  lvar   = [var]
  singleday   = False  # True or False
  #lmon     = [1,3,5,7,9,11]
  #lmon     = [2,4,6,8,10,12]
  lmon     = [mon]
  print "AAAAAAAAAAAAAA"
else:
  iyear    = 2004
  eyear    = 2004
  model       = "test.10deg"
  lvar  = ["PRMSL"]
  #lmon     = [1,3,5,7,9,11]
  lmon   = [1]
  singleday   = True  # True or False
#---------------

tstp     = "6hr"
miss_out    = -9999.0

stype = "anl_p"

#------------------------------------
# grib 1.25 -> 1.25 -> upscaled --> 1.0
#------------------------------------
#--- LAT & LON & NX, NY : upscaled  ------------------------------
cmiplist_dir = "/home/utsumi/mnt/iis.data1/utsumi/CMIP5"
cmiplistname = cmiplist_dir + "/list.6hrPlev.sfc.csv"
#cmiplistname = cmiplist_dir + "/list.test.csv"
f = open(cmiplistname, "r"); lines=f.readlines();  f.close()
flagtemp = 0
for line in lines[1:]:
  line =line.split(",")
  if line[0]==model:
    flagtemp = flagtemp + 1
    a1lat_upscale = map(float, line[5].split(" "))
    a1lon_upscale = map(float, line[6].split(" "))

if ((model !="org")&(flagtemp ==0)):
  print "no model in the list"
  print "model=",model
  print "list=",cmiplistname
  sys.exit()
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
      #ctlname    = idir_root + "/%s/%04d/%s.ctl"%(stype, iyear, stype)
      #idir      = idir_root  +  "/%s/%04d%02d"%(stype, year, mon)

      ctlname    = idir_root + "/%s/%04d/%s.ctl"%(stype, iyear, stype)
      idir      = idir_root  +  "/%s/%04d%02d"%(stype, year, mon)
      #-----
      if model == "org":
        odir_root =  "/media/disk2/data/JRA25/sa.one.anl_p/%s"%(tstp)
      else:
        odir_root =  "/media/disk2/data/JRA25/sa.one.%s/%s"%(model, tstp)
      #-----
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
          
          #-- Flipud --------
          a2org     = flipud(fromfile(tempname, float32).reshape(ny_org, nx_org))

          #********************************************
          #-- upscale -------------
          if model == "org":
            a2upscale  = a2org
            a1lat_upscale =  a1lat_org
            a1lon_upscale =  a1lon_org
          else:
            lupscale_prep  = myfunc_fsub.upscale_prep( a1lon_org, a1lat_org, a1lon_upscale, a1lat_upscale, miss_out)
            a1xw_corres_fort  = lupscale_prep[0]
            a1xe_corres_fort  = lupscale_prep[1]
            a1ys_corres_fort  = lupscale_prep[2]
            a1yn_corres_fort  = lupscale_prep[3]
            a2areasw          = lupscale_prep[4].T
            a2arease          = lupscale_prep[5].T
            a2areanw          = lupscale_prep[6].T
            a2areane          = lupscale_prep[7].T
            #
  
            pergrid           = 0
            missflag          = 0
            a2upscale         = myfunc_fsub.upscale_fast(a2org.T\
                              , a1xw_corres_fort, a1xe_corres_fort\
                              , a1ys_corres_fort, a1yn_corres_fort\
                              , a2areasw.T, a2arease.T, a2areanw.T, a2areane.T\
                              , len(a1lon_upscale), len(a1lat_upscale)\
                              , pergrid, missflag, miss_out\
                              ).T

          #-- Interpolation  --------
          #
          #
          a2fin     = cf.biIntp( a1lat_upscale, a1lon_upscale, a2upscale, a1lat_fin, a1lon_fin, miss = miss_out)[0]
    
          #
          a2fin.tofile( oname ) 
          print tempname
    
    
          ##-- delete temp file ----------------
          os.remove(tempname)
          #------------------------------------
  



