from dtanl_fsub import *
from chart_fsub import *
import chart_para,ctrack_func
from numpy import *
import datetime, calendar
#-------------
iyear = 2000
eyear = 2010
lyear = range(iyear,eyear+1)
lmon = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon  = [1]
iday  = 1
lhour = [0,6,12,18]
ny,nx = 180,360
miss  = -9999.0
lftype = [1,2,3,4]
#--------------
sodir_root  = "/media/disk2/out/chart/ASAS/length.grids"
#*******************
# Region mask
#-------------------
lat_first = -89.5
lon_first = 0.5
dlat, dlon = 1.0, 1.0
#region= "JPN"
region = "ASAS"
#*******************
# function
#-------------------
def ret_regionmask(region,year,mon):
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
  #--
  return a2regionmask
#*******************
for year in lyear:
  for mon in lmon:
    print mon
    #-- init -----
    da1grids  = {}  
    for ftype in lftype:
      da1grids[ftype] = array([],float32)
    #-------------
    idir = "/media/disk2/out/chart/ASAS/front/%04d%02d"%(year,mon)
    a2regionmask = ret_regionmask(region,year,mon)
    #------
    eday = calendar.monthrange(year,mon)[1]
    for day in range(iday,eday+1):
      for hour in lhour:
        iname = idir + "/front.ASAS.%04d.%02d.%02d.%02d.sa.one"%(year,mon,day,hour)
        a2in  = fromfile(iname,float32).reshape(ny,nx)
  
        for ftype in lftype:
          vfill     = ftype
          a2in_seg  = ma.masked_not_equal(a2in, ftype).filled(miss)
          a2in_seg  = chart_fsub.fill_front_gap_for_countfronts(a2in_seg.T, miss, vfill).T
          #----------------
          a1grids_tmp = dtanl_fsub.count_frontlen_grids(a2in_seg.T, a2regionmask.T,miss)
          a1grids_tmp = ma.compressed(ma.masked_equal(a1grids_tmp,0.0))
          #-
          da1grids[ftype] = r_[da1grids[ftype], a1grids_tmp]
    #******************
    # write
    #------------------
    for ftype in lftype:
      da1grids[ftype] = sort(da1grids[ftype])
      sodir  = sodir_root + "/%04d.%02d"%(year,mon)
      ctrack_func.mk_dir(sodir)
      soname = sodir + "/frontlen.grids.%04d.%02d.%s.f%s.bn"%(year,mon,region,ftype)
      da1grids[ftype].tofile(soname)
      print soname
           
