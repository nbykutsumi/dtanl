import calendar
import ctrack_func
from dtanl_fsub import *
from numpy import *

iyear = 2001
eyear = 2004
lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
iday  = 1
lhour = [0,6,12,18]
ny,nx = 180,360
sresol = "anl_p"
plev   = 850*100.0
ftype  = "nbc"
#-- region ----------------
lat_first = -89.5
lon_first = 0.5
dlat      = 1.0
dlon      = 1.0
#
if ftype == "fbc":
  lllat = 0.0
  urlat = 80.0
  lllon = 60.0
  urlon = 220.0
elif ftype == "nbc":
  lllat = 0.0
  urlat = 80.0
  lllon = 60.0
  urlon = 135
#
a2regionmask = ctrack_func.mk_region_mask(lllat, urlat, lllon, urlon, nx, ny, lat_first, lon_first, dlat, dlon)
#---
miss   = -9999.0
#--- init -----------------
a2one  = ma.ones([ny,nx],float32)
a1fmask1 = []
a1fmask2 = []

#--------------------------
for year in range(iyear,eyear+1):
  for mon in lmon:
    eday = calendar.monthrange(year,mon)[1]
    for day in range(iday,eday+1):
      print year,mon,day
      for hour in lhour:
        #******************************************************
        #-- load gridded chart -
        chartdir  = "/media/disk2/out/chart/ASAS/front/%04d%02d"%(year,mon)
        chartname = chartdir + "/front.ASAS.%04d.%02d.%02d.%02d.sa.one"%(year,mon,day,hour)
        a2chart   = fromfile(chartname, float32).reshape(ny,nx)

        #-- screen out baiu front ---
        if (ftype == "fbc")&(mon in [5,6,7,8]):
          a2chart   = ma.masked_equal(a2chart,4.0).filled(miss)

        #-- screen out stationary front ---
        a2chart  = ma.masked_equal(a2chart,4.0).filled(miss)


        #-- screen out occluded front ---
        a2chart  = ma.masked_equal(a2chart,3.0).filled(miss)

        #-- t: ---------------------------------------
        tname = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP/%04d%02d/%s.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,year, mon, sresol, plev*0.01, year, mon, day, hour)
        #-- q: mixing ratio --------------------------
        qname = "/media/disk2/data/JRA25/sa.one.%s/6hr/SPFH/%04d%02d/%s.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,year, mon, sresol, plev*0.01, year, mon, day, hour)

        #
        if ftype == "fbc":
          a2thermo   = fromfile(tname, float32).reshape(ny,nx)
        elif ftype == "nbc":
          a2thermo   = fromfile(qname, float32).reshape(ny,nx)
        #
        a2fmask_tmp1 = dtanl_fsub.mk_a2frontmask1(a2thermo.T).T
        a2fmask_tmp2 = dtanl_fsub.mk_a2frontmask2(a2thermo.T).T
        a2fmask_tmp1 = a2fmask_tmp1 * (1000.0*100.0)**2.0  #[(100km)-2]
        a2fmask_tmp2 = a2fmask_tmp2 * (1000.0*100.0)       #[(100km)-1]
        #
        a2fmask_tmp1 = ma.masked_where(a2chart==miss, a2fmask_tmp1)  
        a2fmask_tmp2 = ma.masked_where(a2chart==miss, a2fmask_tmp2)
        #
        a1fmask_tmp1 = extract( a2fmask_tmp1.mask==False, a2fmask_tmp1.flatten())
        a1fmask_tmp2 = extract( a2fmask_tmp2.mask==False, a2fmask_tmp2.flatten())
        #
        a1fmask1     = concatenate([a1fmask1, a1fmask_tmp1])
        a1fmask2     = concatenate([a1fmask2, a1fmask_tmp2])
#----
a1fmask1 = array(sort(a1fmask1), float32)
a1fmask2 = array(sort(a1fmask2), float32)

#-- write -------
sodir = "/media/disk2/out/JRA25/sa.one.%s/6hr/front/valid/%04d-%04d"%(sresol,iyear,eyear)
ctrack_func.mk_dir(sodir)
soname1 = sodir + "/a1fmask1.%s.bn"%(ftype)
soname2 = sodir + "/a1fmask2.%s.bn"%(ftype)

a1fmask1.tofile(soname1)
a1fmask2.tofile(soname2)
print soname1




