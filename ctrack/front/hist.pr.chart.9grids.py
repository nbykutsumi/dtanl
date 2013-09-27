from numpy import *
import calendar,datetime
from ctrack_fsub import *
from dtanl_fsub import *
from chart_fsub import *
import gsmap_func, ctrack_func
import chart_para
#-----------------------------
iyear = 2001
eyear = 2001
lyear = range(iyear,eyear+1)
#lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
lmon  = [1]
iday  = 1
lhour = [0,6,12,18]
#lftype = [1,2,3,4]
lftype = [2]
#-----------------------------
miss  = -9999.0
ny,nx = 180,360

chartdir_root = "/media/disk2/out/chart/ASAS/front"

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
    a2regionmask = fromfile(name_domain_mask, float32).reshape(ny,nx)
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
    print year,mon
    #---- init ------------
    da1stck  = {}
    for ftype in lftype:
      da1stck[ftype] = array([],float32)
    #---- region ----------
    a2region = ret_regionmask(region,year,mon)

    #----------------------
    eday = calendar.monthrange(year,mon)[1]
    for day in range(iday,eday+1):
      for hour in lhour:
        #*************************
        #-- load fronts ----------
        chartdir  = chartdir_root + "/%04d%02d"%(year,mon)
        chartname = chartdir  + "/front.ASAS.%04d.%02d.%02d.%02d.sa.one"%(year,mon,day,hour)
        a2chart   = fromfile(chartname, float32).reshape(ny,nx)
        a2chart   = ma.masked_where(a2region==miss, a2chart).filled(miss)

        #*************************
        #-- load precip ----------
        a2pr      = gsmap_func.timeave_gsmap_backward_saone(year,mon,day,hour+1, 2)
        a2pr      = gsmap_func.gsmap2global_one(a2pr, miss)        
        ##*************************
        ##-- mk array -------------
        #for ftype in lftype:
        #  a2chart_seg  = ma.masked_not_equal(a2chart, ftype).filled(miss)
        #  a1temp       = chart_fsub.mk_a1pr_9gridmax(a2chart_seg.T, a2pr.T, miss)
        #  a1temp       = ma.masked_equal(a1temp, miss).compressed()
        #  da1stck[ftype]    = r_[ da1stck[ftype], a1temp ]

        #**************************
        # test ---------------
        for ftype in lftype:
          a2pr_seg     = ma.masked_where(a2chart != ftype, a2pr)
          a2pr_seg     = ma.masked_equal(a2pr_seg, miss)
          a1temp       = a2pr_seg.compressed()
          da1stck[ftype]    = r_[ da1stck[ftype], a1temp ]


 
    ##*************************
    ## write to files
    ##-------------------------
    #odir = "/media/disk2/out/chart/ASAS/pr.max.9grids/%04d"%(year)
    #ctrack_func.mk_dir(odir)
    #
    #for ftype in lftype:
    #  soname = odir + "/pr.max.9grids.%s.%02d.f%s.bn"%(region, mon, ftype)
    #  da1stck[ftype] = sort(da1stck[ftype])
    #  da1stck[ftype].tofile(soname)
    #  print soname


