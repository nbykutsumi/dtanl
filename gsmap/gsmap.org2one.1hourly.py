#-----------------------------------
# IMPORTANT !!
# This script makes "Backward mean" precipitation
#-----------------------------------
from numpy import *
import calendar
import datetime
import ctrack_func
import os
import subprocess
import cf
import cf.util

iyear      = 2001
eyear      = 2010
imon       = 1
emon       = 12

#relaxflag  = False
relaxflag  = True
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
  sout   = "mean precipitation rate (%s)\n"%(sunit)
  sout   = sout + "backward mean"
  f      = open( odir + "/readme.txt","w")
  f.write(sout)
  f.close()
#-----------------------------

idir_root  = "/home/utsumi/mnt/iis.data2/GSMaP/standard/v5/hourly"
if   relaxflag == False:
  odir_root  = "/media/disk2/data/GSMaP/sa.one/1hr/ptot"
elif relaxflag == True:
  odir_root  = "/media/disk2/data/GSMaP/sa.one.R/1hr/ptot"

for year in range(iyear , eyear+1):
  for mon in range(imon, emon+1):
    odir  = odir_root + "/%04d%02d"%(year, mon)
    ctrack_func.mk_dir(odir)
    #-- make dimesion & lat, lon file ----
    mk_latlontxt(odir)
    mk_dimtxt(odir)
    mk_unittxt(odir)
    mk_readme(odir)
    #-----------------
    eday  = calendar.monthrange(year, mon)[1]
    #eday  = 1
    #-----------------
    for day in range(1, eday+1):
      #-----
      for hour0 in [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]:
      #for hour0 in [0]:
        now          =  datetime.datetime(year, mon, day, hour0)
        a2dat_fin    =  zeros([ny_fin, nx_fin], float32)
        #a2dat_one    =  zeros([ny_one, nx_one], float32)

        validtimes   = 0
        #-- check first step -----
        if ((year==iyear)&(mon==imon)&(day==1)&(hour0==0)):
          dhour       = datetime.timedelta(hours=1)
          before      = now - dhour
          year_before = before.year
          mon_before  = before.month
          day_before  = before.day
          hour_before = before.hour
          #------------
          idir   = idir_root + "/%04d/%02d/%02d"%(year_before, mon_before, day_before)
          orgname     = idir + "/gsmap_mvk.%04d%02d%02d.%02d00.v5.222.1.dat.gz"%(year_before, mon_before, day_before, hour_before)
          #-- check file --
          if os.access(orgname, os.F_OK):
            print  "XXX", orgname
            #continue
            lhour_inc = [1]
          else:
            lhour_inc = [1]
            print  "YYY", orgname
          #----------------
        else:
          lhour_inc = [1]
        #----------------
        for hour_inc in lhour_inc:
          dhour       = datetime.timedelta(hours=hour_inc)
          before      = now - dhour
          year_before = before.year
          mon_before  = before.month
          day_before  = before.day
          hour_before = before.hour
          print year, mon, day, hour0, before
          #------------
          idir   = idir_root + "/%04d/%02d/%02d"%(year_before, mon_before, day_before)

          #*******************************************
          # for compressed files
          #----------------------
          #orgname     = idir + "/gsmap_mvk.%04d%02d%02d.%02d00.v5.222.1.dat.gz"%(year_before, mon_before, day_before, hour_before)

          ##-- check file --
          #if not os.access(orgname, os.F_OK):
          #  print "no file", orgname
          #  continue
          ##----------------
          #validtimes  = validtimes + 1

          #dat_org     = subprocess.Popen(["gzip", "-dc", orgname, " >", "/dev/stdout"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
          #a2dat_org   = fromstring( dat_org, float32).reshape(ny_fin, nx_fin)

          #da2dat_org[hour_before] = ma.masked_less(a2dat_org, 0.0)

          #*******************************************
          # for uncompressed files
          #----------------------
          orgname     = idir + "/gsmap_mvk.%04d%02d%02d.%02d00.v5.222.1.dat"%(year_before, mon_before, day_before, hour_before)
          #-- check file --
          if not os.access(orgname, os.F_OK):
            print "no file", orgname
            sys.exit()
            continue
          #----------------
          validtimes  = validtimes + 1
          a2dat_org   = fromfile(orgname, float32).reshape(ny_fin, nx_fin)
          #--- Accumulate --------
          if relaxflag   == False:
            a2dat_fin  = a2dat_fin + ma.masked_less(a2dat_org, 0.0)
          elif relaxflag == True:
            a2dat_fin  = a2dat_fin + ma.masked_less(a2dat_org, 0.0).filled(0.0)
        #--- Interpolation -----
        if type(a2dat_fin) ==  ma.core.MaskedArray:
          a2dat_fin    = a2dat_fin.filled(miss_out)
          a2dat_one    = cf.util.upscale(a2dat_fin, newShape, mode="m", missing=miss_out)
          print "AAA", type(a2dat_fin)
        else: 
          a2dat_one    = cf.util.upscale(a2dat_fin, newShape, mode="m")
          print "BBB", type(a2dat_fin)

        #-----------------------
        a2dat_one    = array(a2dat_one, float32)
        a2dat_one    = (ma.masked_equal( a2dat_one, miss_out)/(validtimes*60.0*60.0)).filled(miss_out)
        a2dat_one    = flipud(a2dat_one)
        print "validtimes", validtimes
        #-- write to file -----
        soname       = odir + "/gsmap_mvk.1rh.%04d%02d%02d.%02d00.v5.222.1.sa.one"%(year, mon, day, hour0)
        a2dat_one.tofile(soname)
        print a2dat_one.max()
        print soname

