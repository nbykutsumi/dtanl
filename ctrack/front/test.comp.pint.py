from numpy import *
import gsmap_func
import calendar
from ctrack_fsub import *
#----------------------------------------------
rad = 300.
idir = "/media/disk2/out/chart/ASAS/front/agg/test/prof"
miss = -9999.
year = 2004
mon  = 4
iday = 1
lhour = [0,6,12,18]
#lhour = [0]
eday = calendar.monthrange(year,mon)[1]
#eday = iday
dist_mask = 500.  #(km)
#----------
lat_first = -89.5
dlat      = 1.0
dlon      = 1.0
#----------
sodir = "/media/disk2/out/chart/ASAS/front/agg/test/prof"
sout = "mon,day,hour,spr_w,nw,spr_c,nc,sprin_w,nin_w,sprin_c,nin_c\n"
for day in range(1,eday+1):
  for hour in lhour:
    frontname = "/media/disk2/out/chart/ASAS/front/%04d%02d/front.ASAS.%04d.%02d.%02d.%02d.saone"%(year,mon,year,mon,day,hour)

    a2front   = fromfile(frontname,float32).reshape(180,360)
    a2frontw  = ma.masked_not_equal(a2front, 1).filled(miss)
    a2frontc  = ma.masked_not_equal(a2front, 2).filled(miss)
    #
    a2terrw   = ctrack_fsub.mk_territory_saone((ma.masked_equal(a2front,1.0).filled(miss)).T, dist_mask*1000., miss, lat_first, dlat, dlon).T
    a2terrc   = ctrack_fsub.mk_territory_saone((ma.masked_equal(a2front,2.0).filled(miss)).T, dist_mask*1000., miss, lat_first, dlat, dlon).T
    a2frontinw = ma.masked_where(a2terrw ==miss, a2frontw).filled(miss)
    a2frontinc = ma.masked_where(a2terrc ==miss, a2frontc).filled(miss)

    #-----------------------
    a2gsmap   = gsmap_func.timeave_gsmap_backward_saone(year,mon,day,hour+1,2)
    a2gsmap   = gsmap_func.gsmap2global_one(a2gsmap, miss)
    
    #-----------------------
    a2prw     = ma.masked_where(a2front !=1.0 , a2gsmap)
    a2prc     = ma.masked_where(a2front !=2.0 , a2gsmap)
    #
    a2prinw   = ma.masked_where(a2frontinw ==miss, a2gsmap)    
    a2princ   = ma.masked_where(a2frontinc ==miss, a2gsmap)
    #-----------------------
    prw       = ma.masked_equal( a2prw, miss).filled(0.0).sum()*60*60.
    prc       = ma.masked_equal( a2prc, miss).filled(0.0).sum()*60*60.
    #
    prinw     = ma.masked_equal( a2prinw, miss).filled(0.0).sum()*60*60.
    princ     = ma.masked_equal( a2princ, miss).filled(0.0).sum()*60*60.
    #
    numw      = ma.count( ma.masked_equal(a2prw, miss))
    numc      = ma.count( ma.masked_equal(a2prc, miss))
    #
    numinw    = ma.count( ma.masked_equal(a2prinw, miss))
    numinc    = ma.count( ma.masked_equal(a2princ, miss))
    #
    sout = sout + "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"%(mon,day,hour,prw,numw,prc,numc,prinw,numinw,princ,numinc) 
#-----------------
csvname = sodir  + "/pint.%04d.%02d.csv"%(year,mon)
f=open(csvname, "w");  f.write(sout);  f.close();  print csvname
