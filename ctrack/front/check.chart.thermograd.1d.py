import calendar
import ctrack_func
from dtanl_fsub import *
from ctrack_fsub import *
from numpy import *

iyear = 2000
eyear = 2010
lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
iday  = 1
lhour = [0,6,12,18]
ny,nx = 180,360
sresol = "anl_p"
plev   = 850*100.0
distkm = 100.0
lftype = [1,2,3,4]
#-- region ----------------
lat_first = -89.5
lon_first = 0.5
dlat      = 1.0
dlon      = 1.0
#
lllat = 0.0
urlat = 80.0
lllon = 60.0
urlon = 220.0
#
a2regionmask = ctrack_func.mk_region_mask(lllat, urlat, lllon, urlon, nx, ny, lat_first, lon_first, dlat, dlon)
#---
miss   = -9999.0
#--------------------------
for year in range(iyear,eyear+1):
  for mon in lmon:
    #--- init -----------------
    a2one  = ma.ones([ny,nx],float32)
    da1gradtheta   = {}
    da1gradtheta_e = {}
    for ftype in lftype:
      da1gradtheta[ftype]   = []
      da1gradtheta_e[ftype] = []
    #--------------------------
    eday = calendar.monthrange(year,mon)[1]
    for day in range(iday,eday+1):
      print year,mon,day
      for hour in lhour:
        #******************************************************
        #-- load gridded chart -
        chartdir  = "/media/disk2/out/chart/ASAS/front/%04d%02d"%(year,mon)
        chartname = chartdir + "/front.ASAS.%04d.%02d.%02d.%02d.sa.one"%(year,mon,day,hour)
        a2chart   = fromfile(chartname, float32).reshape(ny,nx)

        #-- t: ---------------------------------------
        tname = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP/%04d%02d/%s.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,year, mon, sresol, plev*0.01, year, mon, day, hour)
        a2t   = fromfile(tname, float32).reshape(ny,nx)

        #-- q: mixing ratio --------------------------
        qname = "/media/disk2/data/JRA25/sa.one.%s/6hr/SPFH/%04d%02d/%s.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,year, mon, sresol, plev*0.01, year, mon, day, hour)
        a2q   = fromfile(qname, float32).reshape(ny,nx)
        #-- theta -----
        a2theta   = dtanl_fsub.mk_a2theta(plev, a2t.T).T
        a2theta_e = dtanl_fsub.mk_a2theta_e(plev, a2t.T, a2q.T).T
        #
        a2gradtheta   = dtanl_fsub.mk_a2grad_abs_saone(a2theta.T).T
        a2gradtheta_e = dtanl_fsub.mk_a2grad_abs_saone(a2theta_e.T).T

        #- coldside ---
        a2gradtheta_cs = ctrack_fsub.find_highsidevalue_saone(-a2theta.T, a2chart.T, a2gradtheta.T, distkm*1000.0, miss).T   
        a2gradtheta_e_cs = ctrack_fsub.find_highsidevalue_saone(-a2theta_e.T, a2chart.T, a2gradtheta_e.T, distkm*1000.0, miss).T   

        #--------------
        for ftype in lftype:
          a2gradtheta_tmp   = ma.masked_where(a2chart != ftype, a2gradtheta_cs)
          a2gradtheta_e_tmp = ma.masked_where(a2chart != ftype, a2gradtheta_e_cs)
          #
          a1gradtheta_tmp    = extract(a2gradtheta_tmp.mask==False, a2gradtheta_tmp)
          a1gradtheta_e_tmp  = extract(a2gradtheta_e_tmp.mask==False, a2gradtheta_e_tmp)
          #
          da1gradtheta[ftype]   = concatenate([da1gradtheta[ftype], a1gradtheta_tmp])
          da1gradtheta_e[ftype] = concatenate([da1gradtheta_e[ftype], a1gradtheta_e_tmp])

    #----------------
    #--- write ------
    sodir = "/media/disk2/out/JRA25/sa.one.%s/6hr/front/valid/%04d.%02d"%(sresol,year,mon)
    ctrack_func.mk_dir(sodir)
    for ftype in lftype:
      da1gradtheta[ftype]   = array(sort(da1gradtheta[ftype]), float32)
      da1gradtheta_e[ftype] = array(sort(da1gradtheta_e[ftype]), float32)
      #---
      a1out1  = array(sort(da1gradtheta[ftype]), float32)
      a1out2  = array(sort(da1gradtheta_e[ftype]), float32)
      print ftype, sum(a1out1)
      soname1 = sodir + "/a1gradtheta.%04dkm.%s.bn"%(distkm, ftype)
      soname2 = sodir + "/a1gradtheta_e.%04dkm.%s.bn"%(distkm,ftype)
      #
      a1out1.tofile(soname1)  
      a1out2.tofile(soname2)  
      print soname1




