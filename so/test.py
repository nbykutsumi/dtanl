from dtanl_fsub import *
import chart_para,ctrack_func
from numpy import *
import datetime
#-------------
year = 2000
mon  = 1
day  = 3
hour = 18
ny,nx = 180,360
miss  = -9999.0
ftype = 2
#--------------
lat_first = -89.5
lon_first = 0.5
dlat, dlon = 1.0, 1.0
#region= "JPN"
region = "ASAS"
if region == "ASAS":
  xydatadir   = "/media/disk2/out/chart/ASAS/const"
  paradate      = datetime.date(year,mon,1)
  if (paradate < datetime.date(2006,1,1)):
    name_domain_mask = xydatadir + "/domainmask_saone.%s.2000.01.bn"%(region)
  if ( datetime.date(2006,1,1)<=paradate<datetime.date(2006,3,1)):
    name_domain_mask = xydatadir + "/domainmask_saone.%s.2006.01.bn"%(region)
  if ( datetime.date(2006,3,1)<=paradate):
    name_domain_mask = xydatadir + "/domainmask_saone.%s.2006.03.bn"%(region)
  #
  a2regionmask  = fromfile(name_domain_mask, float32).reshape(ny,nx)
  a2regionmask = ma.masked_equal(a2regionmask, 0.0).filled(miss)
else:
  lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region)
  a2regionmask = ctrack_func.mk_region_mask(lllat,urlat,lllon,urlon, nx,ny, lat_first, lon_first, dlat, dlon)
  a2regionmask = ma.masked_equal(a2regionmask, 0.0).filled(miss)
#--------------
idir = "/media/disk2/out/chart/ASAS/front/%04d%02d"%(year,mon)
iname = idir + "/front.ASAS.%04d.%02d.%02d.%02d.sa.one"%(year,mon,day,hour)
a2in  = fromfile(iname,float32).reshape(ny,nx)
#
#---- mask ------
a2in    = ma.masked_not_equal(a2in, ftype).filled(miss)
#----------------
a1grids = dtanl_fsub.count_frontlen_grids(a2in.T, a2regionmask.T,miss)
a       = ma.compressed(ma.masked_equal(a1grids,0.0))
print a
