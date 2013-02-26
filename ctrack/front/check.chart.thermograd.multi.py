from numpy import *
from dtanl_fsub import *
import calendar
import ctrack_fig
import ctrack_para
from ctrack_fsub import *

#----------------------------------------------------
#singleday =True
singleday = False
iyear = 2004
eyear = 2004
lseason = [1,2,3,4,5,6,7,8,9,10,11,12]
#lseason = [7]
iday  = 1
ny    = 180
nx    = 360
lhour = [0,6,12,18]
#lhour = [0]

#lllat = 0.0
#lllon = 90
#urlat = 80
#urlon = 210

lllat = 0.0
lllon = 90.0
urlat = 90.0
urlon = 140.0

#lllat = 0.0
#lllon = 140.0
#urlat = 80.0
#urlon = 210.0



plev  = 850*100.0
dist  = 300.0 * 1000.0  #[m]
#ndist = 2.0  #[deg]
#-----
miss  = -9999.0
chartdir_root = "/media/disk2/out/chart/ASAS/front"
tdir_root     = "/media/disk2/data/JRA25/sa.one/6hr/TMP"
qdir_root     = "/media/disk2/data/JRA25/sa.one/6hr/SPFH"
lftype = [1,2,3,4]
#------------------------
#************************
# for transform
xdom_saone_first = int((lllon - 0.5 + 0.5)/1.0)
xdom_saone_last  = int((urlon - 0.5 + 0.5)/1.0)
ydom_saone_first = int((lllat -(-89.5) + 0.5)/1.0)
ydom_saone_last  = int((urlat -(-89.5) + 0.5)/1.0)

#-- init ----------------
a2one   = ones([ny,nx],float32)
dgradtv = {}
dnine   = {}
dhighside={}
dcount  = {}
for season in lseason:
  for ftype in lftype:
    dgradtv[season, ftype] = 0
    dnine[season, ftype]  = 0
    dhighside[season, ftype] = 0
    dcount[season, ftype] = 0
#------------------------
for season in lseason:
  lmon     = ctrack_para.ret_lmon(season)
  for year in range(iyear, eyear+1):
    for mon in lmon:
      print season, year, mon
      #----------------
      if singleday ==True:
        eday = iday
      else:
        eday = calendar.monthrange(year,mon)[1]
      #----------------
      for day in range(iday, eday+1):
        for hour in lhour:
          chartdir  = chartdir_root + "/%04d%02d"%(year,mon)
          tdir      = tdir_root     + "/%04d%02d"%(year,mon)
          qdir      = qdir_root     + "/%04d%02d"%(year,mon)
          #
          chartname = chartdir      + "/front.ASAS.%04d.%02d.%02d.%02d.saone"%(year,mon,day,hour)
          tname     = tdir          + "/anal_p25.TMP.0850hPa.%04d%02d%02d%02d.sa.one"%(year,mon,day,hour)
          qname     = qdir          + "/anal_p25.SPFH.0850hPa.%04d%02d%02d%02d.sa.one"%(year,mon,day,hour)
          a2chart   = fromfile(chartname, float32).reshape(ny,nx)
          a2t       = fromfile(tname,     float32).reshape(ny,nx)
          a2q       = fromfile(qname,     float32).reshape(ny,nx)
          a2tv      = a2t * (1.0+0.61*a2q)
          a2theta   = dtanl_fsub.mk_a2theta_e(plev, a2t.T, a2q.T).T
          a2gradt   = dtanl_fsub.mk_a2grad_abs_saone(a2t.T).T
          a2gradtv  = dtanl_fsub.mk_a2grad_abs_saone(a2tv.T).T
          a2gradtheta=dtanl_fsub.mk_a2grad_abs_saone(a2theta.T).T 
  
          #-- 9grids mean -----------------
          a2gradtv_temp = ma.masked_where(a2chart==miss, a2gradtv).filled(miss)
          a2ninemean    = dtanl_fsub.mean_9grids_saone(a2gradtv_temp.T, miss).T
  
          #-- high side value -------------
          a2highside     = ctrack_fsub.find_highsidevalue_saone(a2gradtheta.T, a2chart.T, a2gradtv.T, dist, miss).T
          #-- transform -------------------
          a2one_trans      = a2one[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]

          a2chart_trans    = a2chart[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]

          a2gradtv_trans   = a2gradtv[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]

          a2ninemean_trans = a2ninemean[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]

          a2highside_trans = a2highside[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]

          #---------------------------------

          for ftype in lftype:
            if ma.count( ma.masked_not_equal(a2chart_trans ,ftype) ) ==0.0:
              continue
            else:
              dgradtv[season, ftype]   = dgradtv[season, ftype]   + ma.masked_where(a2chart_trans != ftype, a2gradtv_trans).sum()
              dnine[season, ftype]     = dnine[season, ftype]     + ma.masked_where(a2chart_trans != ftype, a2ninemean_trans).sum()
              dhighside[season, ftype] = dhighside[season, ftype] + ma.masked_where(a2chart_trans != ftype, a2highside_trans).sum()
              dcount[season, ftype]    = dcount[season, ftype]    + ma.masked_where(a2chart_trans != ftype, a2one_trans).sum()

          if singleday == True:
            bnd = [0.0, 0.000005, 0.000008, 0.000011, 0.000014, 0.000017, 0.000020, 0.000023, 0.000026, 0.000029, 0.000032]
            cbarname = "/home/utsumi/temp/grad.cbar.png"
            ##---- fig :chart --
            fignamechart = "/home/utsumi/temp/chart.%04d.%02d.%02d.%02d.png"%(year,mon,day,hour)
            #ctrack_fig.mk_pict_saone_reg(a2chart, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, soname=fignamechart,miss=-9999.0,cbarname="self")
    
            #-- gradt ----
            fignamegradt = "/home/utsumi/temp/gradt.%04d.%02d.%02d.%02d.png"%(year,mon,day,hour)
            ctrack_fig.mk_pict_saone_reg(a2gradt, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, soname=fignamegradt, miss=-9999.0, cbarname=cbarname, bnd=bnd)
            print fignamegradt
    
            #-- loc.gradt --
            figname = "/home/utsumi/temp/loc.gradt.%04d.%02d.%02d.%02d.png"%(year,mon,day,hour)
            ctrack_fig.mk_pict_saone_reg(a2gradt, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, soname=figname, a2shade=a2chart, miss=-9999.0, bnd=bnd)
    
            #-- ninegrids ---
            fignameninemean = "/home/utsumi/temp/ninegrids.%04d.%02d.%02d.%02d.png"%(year,mon,day,hour)
            ctrack_fig.mk_pict_saone_reg(a2ninemean, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, soname=fignameninemean, miss=miss, bnd=bnd)
    
            #-- highside --
            figname = "/home/utsumi/temp/highside.gradt.%04d.%02d.%02d.%02d.png"%(year,mon,day,hour)
            ctrack_fig.mk_pict_saone_reg(a2highside, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, soname=figname, miss=miss, bnd=bnd)
    
            #-- gradtheta --
            a2figdat= a2gradtheta
            figname = "/home/utsumi/temp/gradtheta.%04d.%02d.%02d.%02d.png"%(year,mon,day,hour)
            ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, soname=figname, miss=miss, bnd=bnd)
    
            #-- loc.gradtheta --
            a2figdat= a2gradtheta
            figname = "/home/utsumi/temp/loc.gradtheta.%04d.%02d.%02d.%02d.png"%(year,mon,day,hour)
            ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, soname=figname, a2shade=a2chart, miss=miss, bnd=bnd)
    
            #-- gradtv -----
            a2figdat= a2gradtv
            figname = "/home/utsumi/temp/gradtv.%04d.%02d.%02d.%02d.png"%(year,mon,day,hour)
            ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, soname=figname, miss=miss, bnd=bnd)
  
  #---------------------------
  for ftype in lftype:
    if dcount[season, ftype] !=0.0:
      dgradtv[season, ftype]   = dgradtv[season, ftype]   /dcount[season, ftype]
      dnine[season, ftype]     = dnine[season, ftype]     /dcount[season, ftype]
      dhighside[season, ftype] = dhighside[season, ftype] /dcount[season, ftype]

#--- write to file -----------
sodir   = "/home/utsumi/temp"
soname  = sodir + "/chart.lon.%03d-%03d.lat.%03d-%03d.grad.csv"%(lllon,urlon,lllat,urlat)
sout    = ""
#-- label ---
sout    = sout + "season,"
for ftype in lftype:
  sout  = sout + "grad.tv.%02d,"%(ftype)
for ftype in lftype:
  sout  = sout + "nine.%02d,"%(ftype)
for ftype in lftype:
  sout  = sout + "highside.%02d,"%(ftype)
sout    = sout[:-1] + "\n"
#------------
for season in lseason:
  sout  = sout  + "%s,"%(season)
  for ftype in lftype:
    sout = sout + "%s,"%(dgradtv[season, ftype])
  for ftype in lftype:
    sout = sout + "%s,"%(dnine[season, ftype])
  for ftype in lftype:
    sout = sout + "%s,"%(dhighside[season, ftype])
  #---
  sout   = sout[:-1] + "\n"
#--------------
if singleday != True:
  f = open(soname, "w")
  f.write(sout)
  f.close()
  print soname



