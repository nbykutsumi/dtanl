from numpy import *
import ctrack_func, cmip_func, tc_func
import ctrack_para, cmip_para, tc_para
import ctrack_fig
#-------------------------
lmodel = ["MIROC5"]

lexpr  = ["historical","rcp85"]
#lexpr  = ["rcp85"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
lseason = ["ALL"]

#lexpr  = ["historical"]
#dyrange = {"historical":[1980,1985], "rcp85":[2080,2099]}
#lseason = [1]

miss    = -9999.0
ny,nx   = 180,360
thdura  = 48
countrad = 300.0 #[km]

#-------------------------
lllat  = -89.5
lllon  = 0.5
urlat  = 89.5
urlon  = 359.5
#---------------
llkey  = [[season,expr,model] for season in lseason for expr in lexpr for model in lmodel]
for season, expr, model in llkey:
  #----
  ens   = cmip_para.ret_ens(model, expr, "psl")
  sunit, scalendar = cmip_para.ret_unit_calendar(model,expr)
  iyear,eyear = dyrange[expr]
  lyear       = range(iyear,eyear+1)
  lmon        = ctrack_para.ret_lmon(season)

  thsst    = tc_para.ret_thsst()
  thwind   = tc_para.ret_thwind()
  thrvort  = tc_para.ret_thrvort(model)
  thwcore  = tc_para.ret_thwcore(model)

  #** land sea mask --------------

  #--- shade       ------
  thorog     = ctrack_para.ret_thorog()
  orogname   = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog/orog.%s.sa.one"%(model,expr,model)
  a2orog     = fromfile(orogname, float32).reshape(ny,nx)
  a2one    = ones([ny,nx],float32)
  a2shade  = ma.masked_where( a2orog >=thorog, a2one).filled(miss)

  #** init  ----------------------
  a2num      = zeros([ny,nx],float32)
  #-------------------------------
  for year in lyear:
    for mon in lmon:
      print year, mon
      #---- load ----
      sidir_root  = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/tc/freq.%02dh"%(model,expr,thdura)
      sidir       = sidir_root + "/%04d"%(year)
      siname      = sidir + "/num.tc.wc%4.2f.sst%02d.wind%02d.vor%.1e.%s.rad%04dkm.%04d.%02d.sa.one"%(thwcore, thsst-273.15, thwind, thrvort, ens, countrad, year, mon)
      a2num_tmp   = fromfile(siname, float32).reshape(180,360)
      a2num       = a2num + a2num_tmp
  #-- calc freq ---
  totaltime = cmip_para.ret_totaldays_cmip(iyear,eyear,season,sunit=sunit,scalendar=scalendar) *4.0
  a2freq    = a2num / totaltime
  #-- write ------
  sodir = sidir_root + "/%04d-%04d.%s"%(iyear,eyear,season)
  ctrack_func.mk_dir(sodir)
  soname = sodir + "/freq.tc.%s.wc%4.2f.sst%02d.wind%02d.vor%.1e.%s.rad%04dkm.%04d-%04d.%s.sa.one"%(model, thwcore, thsst-273.15, thwind, thrvort, ens, countrad,iyear,eyear,season)
  a2freq.tofile(soname)
  print soname
  #*******************************
  # Figure
  #-----------
  bnd        = [0.01,0.25,0.5,1.0,2.0,4.0,8.0]
  #bnd        = [0.25,0.5,1.0,2.0,4.0,8.0]
  #bnd         = [5,10,15,20,25,30,35,40,45]
  #bnd        = [10,20,30,40,50,60,70,80]
  figdir     = sodir
  figname    = soname[:-7] + ".png"
  cbarname   = soname[:-7] + ".cbar.png"
  #----------
  stitle   = "freq. %s.TC season:%s %04d-%04d %s"%(model,season,iyear, eyear,ens)
  mycm     = "Spectral"
  datname  = soname
  a2figdat = fromfile(datname, float32).reshape(ny,nx)

  #-------------------------------
  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
  print figname



