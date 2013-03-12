from numpy import *
from dtanl_fsub import *
import calendar
import ctrack_fig
import ctrack_para
import ctrack_func
from ctrack_fsub import *

#----------------------------------------------------
#singleday =True
singleday = False
#figflag   = True
figflag   = False
iyear = 2000
eyear = 2004
lseason = [1,2,3,4,5,6,7,8,9,10,11,12]
#lseason = [7]
iday  = 1
ny    = 180
nx    = 360
#lhour = [0,6,12,18]
lhour = [0]
thorog = 1500 # (m)
#lllat = 0.0
#lllon = 90
#urlat = 80
#urlon = 210

lllat = 0.0
lllon = 70.0
urlat = 80.0
urlon = 210.0

#lllat = 0.0
#lllon = 140.0
#urlat = 80.0
#urlon = 210.0

region = "ASAS"


plev  = 850*100.0
#dist  = 300.0 * 1000.0  #[m]
dist  = 300.0 * 1000.0  #[m]
#ndist = 2.0  #[deg]
#-----
miss  = -9999.0
chartdir_root = "/media/disk2/out/chart/ASAS/front"
tdir_root     = "/media/disk2/data/JRA25/sa.one/6hr/TMP"
qdir_root     = "/media/disk2/data/JRA25/sa.one/6hr/SPFH"
lftype = [1,2,3,4]
#------------------------
a2one    = ones([ny,nx],float32)
#-- orog --------------------
orogname = "/media/disk2/data/JRA25/sa.one/const/topo/topo.sa.one"
a2orog   = fromfile(orogname, float32).reshape(ny,nx)
#-- domain ------------------
domname  = "/media/disk2/out/chart/%s/const/domainmask_saone.%s.2000-2006.bn"%(region,region)
a2domain = fromfile(domname , float32).reshape(ny,nx)
#-- shade  ------------------
a2shade  = ma.masked_where( a2domain==0.0, a2one).filled(miss)
a2shade  = ma.masked_where( a2orog > thorog, a2shade).filled(miss)

#************************
# for transform
xdom_saone_first = int((lllon - 0.5 + 0.5)/1.0)
xdom_saone_last  = int((urlon - 0.5 + 0.5)/1.0)
ydom_saone_first = int((lllat -(-89.5) + 0.5)/1.0)
ydom_saone_last  = int((urlat -(-89.5) + 0.5)/1.0)

#-- init ----------------
a2one      = ones([ny,nx],float32)
dgradtv    = {}
dcount     = {}

dshighside = {}
dshighside2= {}
dmhighside = {}
dstdhighside = {}

dsmaxgrad  = {}
dsmaxgrad2 = {}
dmmaxgrad  = {}
dstdmaxgrad = {}

dsmeangrad  = {}
dsmeangrad2 = {}
dmmeangrad  = {}
dstdmeangrad = {}


for season in lseason:
  for ftype in lftype:
    dgradtv[season, ftype]    = 0

    dshighside[season, ftype]  = 0
    dshighside2[season, ftype] = 0

    dsmaxgrad[season, ftype]  = 0
    dsmaxgrad2[season, ftype] = 0

    dsmeangrad[season, ftype]  = 0
    dsmeangrad2[season, ftype] = 0

    dcount[season, ftype]     = 0
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
  
          #-- high side value -------------
          a2highside     = ctrack_fsub.find_highsidevalue_saone(a2gradtheta.T, a2chart.T, a2gradtv.T, dist, miss).T

          #-- maxgrad  --------------------
          a2maxgrad      = ctrack_fsub.find_circle_max(a2gradtv.T, a2chart.T, dist, miss).T 

          #-- meangrad --------------------
          a2meangrad     = ctrack_fsub.find_circle_mean(a2gradtv.T, a2chart.T, dist, miss).T
          #-- transform -------------------
          a2one_trans      = a2one[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]

          a2chart_trans    = a2chart[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]

          a2highside_trans = a2highside[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]

          a2maxgrad_trans  = a2maxgrad[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]

          a2meangrad_trans  = a2meangrad[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]

          #---------------------------------

          for ftype in lftype:
            if ma.count( ma.masked_not_equal(a2chart_trans ,ftype) ) ==0.0:
              continue
            else:
              dshighside[season, ftype] = dshighside[season, ftype]  + ma.masked_where(a2chart_trans != ftype, a2highside_trans).sum()
              dshighside2[season, ftype]= dshighside2[season, ftype] + (ma.masked_where(a2chart_trans != ftype, a2highside_trans)**2.0).sum()
              dsmaxgrad[season, ftype] = dsmaxgrad[season, ftype]  + ma.masked_where(a2chart_trans != ftype, a2maxgrad_trans).sum()
              dsmaxgrad2[season, ftype]= dsmaxgrad2[season, ftype] + (ma.masked_where(a2chart_trans != ftype, a2maxgrad_trans)**2.0).sum()

              dsmeangrad[season, ftype] = dsmeangrad[season, ftype]  + ma.masked_where(a2chart_trans != ftype, a2meangrad_trans).sum()
              dsmeangrad2[season, ftype]= dsmeangrad2[season, ftype] + (ma.masked_where(a2chart_trans != ftype, a2meangrad_trans)**2.0).sum()

              dcount[season, ftype]     = dcount[season, ftype]      + ma.masked_where(a2chart_trans != ftype, a2one_trans).sum()

          if figflag == True:
            figdir   = "/home/utsumi/temp/%04d.%02d"%(year,mon)
            ctrack_func.mk_dir(figdir)
            #--
            bnd = [0.0, 0.000005,  0.000007, 0.000009, 0.000011]
            cbarname = figdir + "/grad.cbar.png"
            ##---- fig :chart --
            fignamechart = figdir + "/chart.%04d.%02d.%02d.%02d.png"%(year,mon,day,hour)
            #ctrack_fig.mk_pict_saone_reg(a2chart, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, soname=fignamechart,miss=-9999.0,cbarname="self")
    
            ##-- gradtv ----
            #figname      = figdir + "/gradtv.%04d.%02d.%02d.%02d.png"%(year,mon,day,hour)
            #stitle       = "gradtv.%04d.%02d.%02d.%02d"%(year,mon,day,hour)
            #ctrack_fig.mk_pict_saone_reg(a2gradtv, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, soname=figname, miss=-9999.0, cbarname=cbarname, bnd=bnd, stitle=stitle)
            #print figname
    
            ##-- loc.gradtv --
            #figname = figdir + "/loc.gradtv.%04d.%02d.%02d.%02d.png"%(year,mon,day,hour)
            #stitle       = "loc.gradtv.%04d.%02d.%02d.%02d"%(year,mon,day,hour)
            #ctrack_fig.mk_pict_saone_reg(a2gradtv, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, soname=figname, a2shade=a2chart, miss=-9999.0, bnd=bnd, stitle=stitle)
            #-- highside --
            figname = figdir + "/highside.highside.%03d.gradtv.%04d.%02d.%02d.%02d.png"%(dist*0.001, year,mon,day,hour)
            stitle       = "loc.highside.%03d.%04d.%02d.%02d.%02d"%(dist*0.001,year,mon,day,hour)
            ctrack_fig.mk_pict_saone_reg(a2highside, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, soname=figname, miss=miss, bnd=bnd, stitle=stitle, a2shade=a2shade)

            ##-- maxgrad --
            #figname = figdir + "/maxgrad.maxgrad.%03d.gradtv.%04d.%02d.%02d.%02d.png"%(dist*0.001, year,mon,day,hour)
            #stitle       = "loc.maxgrad.%03d.%04d.%02d.%02d.%02d"%(dist*0.001,year,mon,day,hour)
            #ctrack_fig.mk_pict_saone_reg(a2maxgrad, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, soname=figname, miss=miss, bnd=bnd, stitle=stitle)
            #print figname

            ##-- meangrad --
            #figname = figdir + "/meangrad.meangrad.%03d.gradtv.%04d.%02d.%02d.%02d.png"%(dist*0.001, year,mon,day,hour)
            #stitle       = "loc.meangrad.%03d.%04d.%02d.%02d.%02d"%(dist*0.001,year,mon,day,hour)
            #ctrack_fig.mk_pict_saone_reg(a2meangrad, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, soname=figname, miss=miss, bnd=bnd, stitle=stitle, cbarname=cbarname)
            print figname
 
            ##-- gradtheta --
            #a2figdat= a2gradtheta
            #figname = figdir + "/gradtheta.%04d.%02d.%02d.%02d.png"%(year,mon,day,hour)
            #ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, soname=figname, miss=miss, bnd=bnd)
    
            ##-- loc.gradtheta --
            #a2figdat= a2gradtheta
            #figname = figdir + "/loc.gradtheta.%04d.%02d.%02d.%02d.png"%(year,mon,day,hour)
            #ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, soname=figname, a2shade=a2chart, miss=miss, bnd=bnd)


#***********************************
#  warmside 
#---------------------------
for season in lseason:
  for ftype in lftype:
    if dcount[season, ftype] !=0.0:
      dmhighside[season, ftype] = dshighside[season, ftype] /dcount[season, ftype]
      n    = dcount[season, ftype]
      sv2  = dshighside2[season, ftype]
      sv   = dshighside[season, ftype]
      mv   = sv  / n
      std  = ((sv2 - 2.0*mv*sv + n*mv*mv)/n)**0.5
      dstdhighside[season, ftype] = std
#--- write to file -----------
sodir   = "/home/utsumi/temp"
soname  = sodir + "/chart.lon.highside.%03d-%03d.lat.%03d-%03d.wside%03d.grad.csv"%(lllon,urlon,lllat,urlat,dist*0.001)
sout    = ""
#-- label ---
sout    = sout + "season,"
for ftype in lftype:
  sout  = sout + "highside.%02d,"%(ftype)
for ftype in lftype:
  sout  = sout + "std.%02d,"%(ftype)

sout    = sout[:-1] + "\n"
#------------
for season in lseason:
  sout  = sout  + "%s,"%(season)
  for ftype in lftype:
    sout = sout + "%s,"%(dmhighside[season, ftype])
  for ftype in lftype:
    sout = sout + "%s,"%(dstdhighside[season, ftype])
  #---
  sout   = sout[:-1] + "\n"
#--------------
if singleday != True:
  f = open(soname, "w")
  f.write(sout)
  f.close()
  print soname
#
#
##***********************************
##  maxgrad 
##---------------------------
#for season in lseason:
#  for ftype in lftype:
#    if dcount[season, ftype] !=0.0:
#      dmmaxgrad[season, ftype] = dsmaxgrad[season, ftype] /dcount[season, ftype]
#      n    = dcount[season, ftype]
#      sv2  = dsmaxgrad2[season, ftype]
#      sv   = dsmaxgrad[season, ftype]
#      mv   = sv  / n
#      std  = ((sv2 - 2.0*mv*sv + n*mv*mv)/n)**0.5
#      dstdmaxgrad[season, ftype] = std
##--- write to file -----------
#sodir   = "/home/utsumi/temp"
#soname  = sodir + "/chart.maxgrad.lon.%03d-%03d.lat.%03d-%03d.wside%03d.grad.csv"%(lllon,urlon,lllat,urlat,dist*0.001)
#sout    = ""
##-- label ---
#sout    = sout + "season,"
#for ftype in lftype:
#  sout  = sout + "maxgrad.%02d,"%(ftype)
#for ftype in lftype:
#  sout  = sout + "std.%02d,"%(ftype)
#
#sout    = sout[:-1] + "\n"
##------------
#for season in lseason:
#  sout  = sout  + "%s,"%(season)
#  for ftype in lftype:
#    sout = sout + "%s,"%(dmmaxgrad[season, ftype])
#  for ftype in lftype:
#    sout = sout + "%s,"%(dstdmaxgrad[season, ftype])
#  #---
#  sout   = sout[:-1] + "\n"
##--------------
#if singleday != True:
#  f = open(soname, "w")
#  f.write(sout)
#  f.close()
#  print soname
#
#
##***********************************
##  meangrad 
##---------------------------
#for season in lseason:
#  for ftype in lftype:
#    if dcount[season, ftype] !=0.0:
#      dmmeangrad[season, ftype] = dsmeangrad[season, ftype] /dcount[season, ftype]
#      n    = dcount[season, ftype]
#      sv2  = dsmeangrad2[season, ftype]
#      sv   = dsmeangrad[season, ftype]
#      mv   = sv  / n
#      std  = ((sv2 - 2.0*mv*sv + n*mv*mv)/n)**0.5
#      dstdmeangrad[season, ftype] = std
##--- write to file -----------
#sodir   = "/home/utsumi/temp"
#soname  = sodir + "/chart.meangrad.lon.%03d-%03d.lat.%03d-%03d.wside%03d.grad.csv"%(lllon,urlon,lllat,urlat,dist*0.001)
#sout    = ""
##-- label ---
#sout    = sout + "season,"
#for ftype in lftype:
#  sout  = sout + "meangrad.%02d,"%(ftype)
#for ftype in lftype:
#  sout  = sout + "std.%02d,"%(ftype)
#
#sout    = sout[:-1] + "\n"
##------------
#for season in lseason:
#  sout  = sout  + "%s,"%(season)
#  for ftype in lftype:
#    sout = sout + "%s,"%(dmmeangrad[season, ftype])
#  for ftype in lftype:
#    sout = sout + "%s,"%(dstdmeangrad[season, ftype])
#  #---
#  sout   = sout[:-1] + "\n"
##--------------
#if singleday != True:
#  f = open(soname, "w")
#  f.write(sout)
#  f.close()
#  print soname
#




