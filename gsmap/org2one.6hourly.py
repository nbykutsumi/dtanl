#-----------------------------------
# IMPORTANT !!
# This script makes "Backward 6-hour mean" precipitation
#-----------------------------------
from numpy import *
import calendar
import ctrack_func
import os
import subprocess
import cf
import cf.util

iyear      = 2001
eyear      = 2008
imon       = 1
emon       = 12

miss_out   = -9999.0
sunit      = "kg m-2 s-1"
#--- latlon fin -------
ny_fin     = 1200
nx_fin     = 3600

#--- latlon one -------
ny_one     = 120  # lat = -60 .. 60
nx_one     = 360
newShape   = array([ny_one, nx_one], int)
#--- for dimension files ----------
lat_one_first  = -59.5
lat_one_last   = 59.5
lon_one_first  = 0.5
lon_one_last   = 359.5
dlat_one       = 1.0
dlon_one       = 1.0

a1lat_one  = arange(lat_one_first, lat_one_last + dlat_one*0.5, dlat_one)
a1lon_one  = arange(lon_one_first, lon_one_last + dlon_one*0.5, dlon_one)

def mk_latlontxt(odir):
  sout     = "\n".join(map( str, a1lat_one))
  f        = open( odir + "/lat.txt", "w")
  f.write(sout)
  f.close()
  #
  sout     = "\n".join(map( str, a1lon_one))
  f        = open( odir + "/lon.txt", "w")
  f.write(sout)
  f.close()
#----
def mk_dimtxt(odir):
  sout   = "lev %d\nlat %d\nlon %d"%(1, ny_one, nx_one)
  f      = open( odir + "/dims.txt", "w")
  f.write(sout)
  f.close()  
#--- for unit file -----------
def mk_unittxt(odir):
  sout   = "unit: %s"%(sunit)
  f      = open( odir + "/unit.txt","w")
  f.write(sout)
  f.close()
#-- readme -------------------
def mk_readme(odir):
  sout   = "e.g.\n"
  sout   = sout + "gsmap_mvk.6rh.YYYYMMDD.hh00.v5.222.1.sa.one\n"
  sout   = sout + "mean precipitation rate (%s)\n"%(sunit)
  sout   = sout + "six hours from hh:00"
  f      = open( odir + "/readme.txt","w")
  f.write(sout)
  f.close()
#-----------------------------

idir_root  = "/home/utsumi/mnt/export/nas_d/data/GSMaP/standard/v5/hourly"
odir_root  = "/media/disk2/data/GSMaP/sa.one/6hr/ptot"

for year in range(iyear , eyear+1):
  for mon in range(imon, emon+1):
    odir  = odir_root + "/%04d%02d"%(year, mon)
    ctrack_func.mk_dir(odir)
    #-- make dimesion & lat, lon file ----
    mk_latlontxt(odir)
    mk_dimtxt(odir)
    mk_unittxt(odir)
    mk_readme(odir)
    #-- no leap ------
    if (mon ==2):
      eday = 28
    else:
      eday  = calendar.monthrange(year, mon)[1]

    #eday  = 1
    #-----------------
    for day in range(1, eday+1):
      idir   = idir_root + "/%04d/%02d/%02d"%(year, mon, day)
      #-----
      for hour0 in [0, 6, 12, 18]:
      #for hour0 in [0]:

        a2dat_fin    =  ones([ny_fin, nx_fin], float32)
        a2dat_one    =  ones([ny_one, nx_one], float32)

        da2dat_org   = {}
        for hour_inc in [0, 1, 2, 3, 4, 5]: 
          hour = hour0 + hour_inc
          #------------
          orgname    = idir + "/gsmap_mvk.%04d%02d%02d.%02d00.v5.222.1.dat.gz"%(year, mon, day, hour)
          dat_org    = subprocess.Popen(["gzip", "-dc", orgname, " >", "/dev/stdout"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
          a2dat_org  = fromstring( dat_org, float32).reshape(ny_fin, nx_fin)

          da2dat_org[hour] = ma.masked_less(a2dat_org, 0.0)
          #--- Accumulate --------
          a2dat_fin  = a2dat_fin + ma.masked_less(a2dat_org, 0.0)
        #--- Interpolation -----
        a2dat_fin    = a2dat_fin.filled(miss_out)
        a2dat_one    = cf.util.upscale(a2dat_fin, newShape, mode="m", missing=miss_out)

        #-----------------------
        a2dat_one    = array(a2dat_one, float32)
        a2dat_one    = (ma.masked_equal( a2dat_one, miss_out)/(6.0*60.0*60.0)).filled(miss_out)
        a2dat_one    = flipud(a2dat_one)

        #-- write to file -----
        soname       = odir + "/gsmap_mvk.6rh.%04d%02d%02d.%02d00.v5.222.1.sa.one"%(year, mon, day, hour0)
        a2dat_one.tofile(soname)
        print soname

