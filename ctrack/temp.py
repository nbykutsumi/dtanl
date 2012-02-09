from ctrack import *
from numpy import *
import datetime, calendar
#--------------------------------
def time_slide(year, mon, day, hour, hourdelta):
  now         = datetime.datetime(year, mon, day, hour)
  target      = now + datetime.timedelta(hours = hourdelta)
  targetyear  = target.year
  #***********
  if ( calendar.isleap(targetyear) ):
    targetmonth = target.month
    targetday   = target.day
    if ( (targetmonth == 2) and (targetday == 29)):
      if (hourdelta < 0):
        target = target + datetime.timedelta(hours = -24)
      elif (hourdelta >0):
        target = target + datetime.timedelta(hours = 24)
  #-----------
  return target

#*****************************************************
# test for 
#-----------------------------------------------------
year = 1991
mon = 8
nx = 144
ny = 96
miss_int = -9999
miss_dbl = -9999.0
lat_first = -90.0
dlat = 1.89473684
dlon = 2.5
#---------------------
thdist    = 1500.0 * 1000.0   # [m]
thdura    = 24   #[days]
#*****************************************************
# precip
#*****************************************************
prname  = "/media/disk2/data/CMIP5/bn/pr/6hr/NorESM1-M/historical/r1i1p1/%04d/pr_6hr_NorESM1-M_historical_r1i1p1_%04d%02d0100.bn"%(year, year,mon)

a2pr = fromfile(prname, float32).reshape(ny,nx)

#*****************************************************


#*****************************************************
# test for aggr_pr
#---------------------
lifename  = "/media/disk2/out/CMIP5/6hr/NorESM1-M/historical/r1i1p1/life/%04d/life_6hr_NorESM1-M_historical_r1i1p1_%04d%02d0100.bn"%(year, year, mon)
pgradname = "/media/disk2/out/CMIP5/6hr/NorESM1-M/historical/r1i1p1/pgrad/%04d/pgrad_6hr_NorESM1-M_historical_r1i1p1_%04d%02d0100.bn"%(year, year, mon)

a2life  = fromfile(lifename,  int32).reshape(ny, nx)
a2pgrad = fromfile(pgradname, float32).reshape(ny, nx)
#
a2life  = array(a2life.T,  int64)
a2pgrad = array(a2pgrad.T, float64)
#
tout = ctrack.aggr_pr(a2life, a2pgrad, thdist, thdura\
                      , miss_int,miss_dbl, lat_first, dlat\
                      , dlon)

a2territory = tout[0].T
a2dist      = tout[1].T
print tout
print a2territory.max()
#
########################################################
## test for circle_xy
##------------------------------------------------------
#latname = "/media/disk2/data/CMIP5/bn/pr/day/NorESM1-M/historical/r1i1p1/lat.txt"
#f = open(latname, "r")
#a1lat = array(map(float, f.readlines()))
#f.close()
##
#xtarget = 102
#ytarget = 52
#
#nx = 144
#ny = 96
#thdist    = 1000.0*1000  #[m]
#miss_int  = -9999
#lat_first = a1lat[0]
#dlat = a1lat[1] - a1lat[0]
#dlon = 2.5
#
#icount = -1
#for lat in a1lat:
#  icount = icount + 1
#  if icount == ytarget:
#    tout   = ctrack.circle_xy(lat, lat_first, dlon, dlat, thdist, miss_int, nx, ny)
#    print tout[0]
##------------------
#x = xtarget
#y = ytarget
#a1x = tout[0]
#a1y = tout[1]
#a2temp = zeros(nx*ny).reshape(ny, nx)
#i = 0
#while a1x[i] != miss_int:
#  ix_loop = x + a1x[i]
#  iy_loop = y + a1y[i]
#  (ix, iy) = ctrack.ixy2iixy(ix_loop, iy_loop, nx, ny)
#  print "ix_loop, iy_loop, ix, iy",ix_loop, iy_loop, ix, iy
#  i = i +1
#  ix = ix -1
#  iy = iy -1
#  a2temp[iy, ix] = 1.0
#  
#
#
##*****************************************************
##year = 1990
##mon = 8
##nx = 144
##ny = 96
##miss_dbl = -9999.0
##lat_first = 0.0
##dlat = 1.89473684
##dlon = 2.5
###---------
##uname   = "/media/disk2/data/CMIP5/bn/ua/day/NorESM1-M/historical/r1i1p1/1990/ua_day_NorESM1-M_historical_r1i1p1_%04d%02d0100.bn"%(year,mon)
##vname   = "/media/disk2/data/CMIP5/bn/va/day/NorESM1-M/historical/r1i1p1/1990/va_day_NorESM1-M_historical_r1i1p1_%04d%02d0100.bn"%(year,mon)
##prname  = "/media/disk2/data/CMIP5/bn/pr/day/NorESM1-M/historical/r1i1p1/1990/pr_day_NorESM1-M_historical_r1i1p1_%04d%02d0100.bn"%(year,mon)
##pslname = "/media/disk2/data/CMIP5/bn/psl/day/NorESM1-M/historical/r1i1p1/1990/psl_day_NorESM1-M_historical_r1i1p1_%04d%02d0100.bn"%(year,mon)
###---------
##a2u = fromfile(uname, float32).reshape(8,96,144)[1].T
##a2v = fromfile(vname, float32).reshape(8,96,144)[1].T
###---------
##a2u = array(a2u, float64)
##a2v = array(a2v, float64)
###---------
##a2vor = ctrack.vorticity(a2u, a2v, lat_first, dlon, dlat, miss_dbl)
##a2vor = a2vor.T
###---------
##pr   = fromfile(prname, float32).reshape(96,144)
##psl  = fromfile(pslname,float32).reshape(96,144)
#
#
