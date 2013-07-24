from numpy import *
from myfunc_fsub import *
import cf
import subprocess
import calendar
import os

#singleday = True
singleday = False
iyear = 2000
eyear = 2010
tstp  = "6hr"
ny    = 180
nx    = 360
lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon  = [1,2]
miss  = -9999.0
var   = "PRMSL"
dtype = {}
dtype["PRMSL"] = "anl_p"
#lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel     = ["org"]
idir_root   =  "/home/utsumi/mnt/iis.data2/JRA25"
iday       = 1
#********************************************
#--- LAT & LON & NX, NY : Original  ------------------------------
dlat_org      = 1.25
dlon_org      = 1.25

lat_first_org = -90.0
lat_last_org  = 90.0
lon_first_org = 0.0
lon_last_org  = 360.0 - 1.25
a1lat_org     = arange(lat_first_org, lat_last_org + dlat_org*0.1, dlat_org)
a1lon_org     = arange(lon_first_org, lon_last_org + dlon_org*0.1, dlon_org)
nx_org        = len(a1lon_org)
ny_org        = len(a1lat_org)

#--- LAT & LON & NX, NY : After Interpolation  ------------------
dlat_one   = 1.0
dlon_one   = 1.0
a1lat_one  = arange(-90.0+dlat_one*0.5, 90.0 - dlat_one*0.5 + dlat_one*0.1, dlat_one)
a1lon_one  = arange(0.0+dlon_one*0.5, 360.0 - dlon_one*0.5 + dlon_one*0.1, dlon_one)

ny_one     = len(a1lat_one)
nx_one     = len(a1lon_one)
nz_one     = 1


#********************************************
def mk_dir(sdir):
  if not os.access(sdir , os.F_OK):
    os.makedirs(sdir)
#********************************************
stype  = dtype[var]

for model in lmodel:
  odir_root  = "/media/disk2/data/JRA25/sa.one.%s/my.mean"%(model)
  odir       = odir_root + "/%s"%(var)
  mk_dir(odir)

  tempdir_root  = "/media/disk2/data/JRA25/temp.bn"
  #******************************************
  #--- LAT & LON & NX, NY : upscaled  -------
  cmiplist_dir = "/home/utsumi/mnt/iis.data1/utsumi/CMIP5"
  cmiplistname = cmiplist_dir + "/list.6hrPlev.sfc.csv"
  f = open(cmiplistname, "r"); lines=f.readlines();  f.close()
  for line in lines[1:]:
    line =line.split(",")
    if line[0]==model:
      a1lat_upscale = map(float, line[5].split(" "))
      a1lon_upscale = map(float, line[6].split(" "))
      nx_upscale    = len(a1lon_upscale)
      ny_upscale    = len(a1lat_upscale)
  #*******************************************
  #-- initialize  -----------------------------
  da2mean = {}
  for mon in [0]+lmon:
    da2mean[mon] = zeros([ny, nx], float32)
  #--------------------------------------------
  dtimes  = {}
  for mon in [0]+lmon:
    dtimes[mon] = 0
  #--------------------------------------------
  for year in range(iyear, eyear + 1):
    for mon in lmon:
      idir      = idir_root     +  "/%s.tmp/%04d%02d"%(dtype[var], year, mon)
      tempdir   = tempdir_root  +  "/%s/%04d%02d"%(var,year,mon)
      mk_dir(tempdir)
      #-----------------
      if singleday == True:
        eday  = iday
      else:
        eday  = calendar.monthrange(year, mon)[1]
      #-----------------
      for day in range(iday, eday+1):
        print model,var, year, mon, day
        for hour in [0, 6, 12, 18]:
          dtimes[0]     = dtimes[0] + 1
          dtimes[mon]   = dtimes[mon] + 1
          #-- in name -------------
          #----- Names ------------

          stime     = "%04d%02d%02d%02d"%(year, mon, day, hour)
          gribname  = idir    + "/%s.%s"%(stype, stime)
          tempname  = tempdir + "/%s.%s.%s.temp.bn"%(stype, var, stime)

          ##-- grib --> binary -----
          #if model == lmodel[0]:
          #  args      = "wgrib %s | grep %s | wgrib %s -i -nh -o %s"%(gribname, var, gribname, tempname)
          #  #
          #  ptemp     = subprocess.call(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   
          #  print "create",tempname

          #-- load org bn data --
          a2in          = fromfile( tempname , float32).reshape(ny_org, nx_org)

          ##-- remove tempfile --
          #if model == lmodel[-1]:
          #  os.remove(tempname)
          #  print "removed", model

          #********************************************
          # flip ud
          a2in          = flipud(a2in)

          #********************************************
          #--- upscale ---------
          if (model != "org"):
            pergrid       = 0
            missflag      = 0
            a2up          = myfunc_fsub.upscale(a2in.T\
                                         , a1lon_org, a1lat_org\
                                         , a1lon_upscale, a1lat_upscale\
                                         , pergrid, missflag, miss\
                                         , nx_org, ny_org\
                                         , nx_upscale, ny_upscale).T
            #----
          else:
            model         = "org"
            a2up          = a2in
            a1lat_upscale = a1lat_org
            a1lon_upscale = a1lon_org 
          #--- downscale -------
          a2one     = cf.biIntp( a1lat_upscale, a1lon_upscale, a2up, a1lat_one, a1lon_one, miss = miss)[0]
          #-------------------------------
          da2mean[mon]  = da2mean[mon] + a2one
          da2mean[0]    = da2mean[0]   + a2one
  #------------------------------
  #for mon in range(0, 12+1):
  for mon in [0]+lmon:
    da2mean[mon] = da2mean[mon] / dtimes[mon]
    soname       = odir + "/%s.%s.0000%02d0000.sa.one"%(stype, var, mon)
    da2mean[mon].tofile(soname)
    print soname
  
  #------------------------------
  
