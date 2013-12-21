from numpy import *
from ctrack_fsub import *
import calendar
import ctrack_func
#-----------------------------------
iyear  = 2007
eyear  = 2010
imon   = 1
emon   = 12
iday   = 1
lhour  = [0,6,12,18]
region = "ASAS"
ny     = 180
nx     = 360
miss   = -9999.0
#rad    = 200  # (km)
rad    = 1 # (km)
#
lat_first = -89.5
dlat      = 1.0
dlon      = 1.0
#--- dir --------------
idir_root = "/media/disk2/out/chart/ASAS/front"
odir_root = idir_root + "/agg"
#--- domain mask ------
domdir   = "/media/disk2/out/chart/ASAS/const"
domname  = domdir + "/domainmask_saone.ASAS.2000-2006.bn"
a2dom    = fromfile(domname, float32).reshape(180,360)
#---- dummy -----------
a2one    = ones([ny,nx],float32)
#----------------------
for year in range(iyear, eyear+1):
  for mon in range(imon, emon+1):
    #--out name ----
    odir        = odir_root + "/%04d/%02d"%(year, mon)
    ctrack_func.mk_dir(odir)

    oname_warm  = odir   + "/count.rad%04dkm.warm.sa.one"%(rad)
    oname_cold  = odir   + "/count.rad%04dkm.cold.sa.one"%(rad)
    oname_occ   = odir   + "/count.rad%04dkm.occ.sa.one"%(rad)
    oname_stat  = odir   + "/count.rad%04dkm.stat.sa.one"%(rad)
    #-- init -------
    a2count_warm = zeros([ny,nx],float32)
    a2count_cold = zeros([ny,nx],float32)
    a2count_occ  = zeros([ny,nx],float32)
    a2count_stat = zeros([ny,nx],float32)

    #---------------
    eday = calendar.monthrange(year, mon)[1]
    for day in range(iday, eday+1):
      for hour in lhour:
        idir  = idir_root + "/%04d%02d"%(year, mon)
        iname = idir + "/front.ASAS.%04d.%02d.%02d.%02d.sa.one"%(year,mon,day,hour)
        a2in  = fromfile(iname, float32).reshape(ny,nx)
        #----
        a2count_warm_tmp = ma.masked_where(a2in !=1.0, a2one).filled(0.0)
        a2count_cold_tmp = ma.masked_where(a2in !=2.0, a2one).filled(0.0)
        a2count_occ_tmp  = ma.masked_where(a2in !=3.0, a2one).filled(0.0)
        a2count_stat_tmp = ma.masked_where(a2in !=4.0, a2one).filled(0.0)
        #----
        a2count_warm_tmp = ctrack_fsub.mk_territory_saone(a2count_warm_tmp.T, rad*1000., 0.0, lat_first, dlat, dlon).T
        a2count_cold_tmp = ctrack_fsub.mk_territory_saone(a2count_cold_tmp.T, rad*1000., 0.0, lat_first, dlat, dlon).T
        a2count_occ_tmp  = ctrack_fsub.mk_territory_saone(a2count_occ_tmp.T,  rad*1000., 0.0, lat_first, dlat, dlon).T
        a2count_stat_tmp = ctrack_fsub.mk_territory_saone(a2count_stat_tmp.T, rad*1000., 0.0, lat_first, dlat, dlon).T

        #------
        a2count_warm = a2count_warm + a2count_warm_tmp
        a2count_cold = a2count_cold + a2count_cold_tmp
        a2count_occ  = a2count_occ  + a2count_occ_tmp
        a2count_stat = a2count_stat + a2count_stat_tmp
        #------
    #---------------
    a2count_warm   = ma.masked_where(a2dom == 0.0, a2count_warm).filled(miss)
    a2count_cold   = ma.masked_where(a2dom == 0.0, a2count_cold).filled(miss)
    a2count_occ    = ma.masked_where(a2dom == 0.0, a2count_occ ).filled(miss)
    a2count_stat   = ma.masked_where(a2dom == 0.0, a2count_stat).filled(miss)
    #---------------
    a2count_warm.tofile(oname_warm)
    a2count_cold.tofile(oname_cold)
    a2count_occ.tofile(oname_occ)
    a2count_stat.tofile(oname_stat)
    print oname_warm
     
         




