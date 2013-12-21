from numpy import *
from myfunc_fsub import *
import ctrack_func, cmip_func, tc_func
import ctrack_para, cmip_para, tc_para
import ctrack_fig
#-------------------------
filterflag = True
#filterflag = False

#sum3x3flag = True
sum3x3flag = False

figflag = True
#onlyMME = True
onlyMME = False
lmodel = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3","MRI-CGCM3"]
#lmodel = ["MRI-CGCM3","IPSL-CM5B-LR"]

#lexpr  = ["historical","rcp85"]
lexpr  = ["historical"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
lseason = ["ALL"]
#lseason = [1,2,3,4,5,6,7,8,9,10,11,12]

#lexpr  = ["historical"]
#dyrange = {"historical":[1980,1985], "rcp85":[2080,2099]}
#lseason = [1]

miss    = -9999.0
ny,nx   = 180,360
thdura  = 48
#countrad = 300.0 #[km]
countrad = 1.0 #[km]

#a2filter = array(\
#           [[1,2,1]\
#           ,[2,4,2]\
#           ,[1,2,1]], float32)

a2filter = array(\
           [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]], float32)



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
  if (figflag == False)or(onlyMME == True):
    continue
  #-----------
  #---------------------------
  if len(lmon) ==12:
    if sum3x3flag == True:
      bnd        = [0.1,0.25,0.5,1.0,2.0,4.0]
    if sum3x3flag == False:
      bnd        = [0.01, 0.025, 0.5, 0.1, 0.2, 0.4]
  elif len(lmon) ==3:
    #bnd        = [0.01,0.25,0.5,1.0,2.0,4.0]
    bnd        = [0.1,0.25,0.5,1.0,2.0,4.0]
  elif len(lmon) ==1:
    #bnd        = [0.01,0.25,0.5,1.0,2.0,4.0]
    bnd        = [0.1,0.25,0.5,1.0,2.0,4.0]
  #---------------------------
  figdir     = sodir
  #-----------
  if (filterflag == True)&(sum3x3flag==True):
    figname    = soname[:-7] + ".filt.3x3.png"
  if (filterflag == True)&(sum3x3flag==False):
    figname    = soname[:-7] + ".filt.png"
  if (filterflag == False)&(sum3x3flag==True):
    figname    = soname[:-7] + ".3x3.png"
  if (filterflag == False)&(sum3x3flag==False):
    figname    = soname[:-7] + ".png"
  #-----------
  if sum3x3flag == True:
    cbarname   = soname[:-7] + ".3x3.cbar.png"
  elif sum3x3flag == False:
    cbarname   = soname[:-7] + ".cbar.png"
  #----------
  stitle   = "freq (days/season) %s.TC season:%s %04d-%04d %s"%(model,season,iyear, eyear,ens)
  mycm     = "Spectral"
  datname  = soname
  a2figdat = fromfile(datname, float32).reshape(ny,nx)

  #-------------------------------
  totaldays = cmip_para.ret_totaldays_cmip(iyear,eyear,season,sunit,scalendar)
  #a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
  a2figdat = ma.masked_equal(a2freq, miss).filled(0.0) * totaldays / len(lyear)  # [days per season]
  #--- filtering ----
  if filterflag == True:
    a2figdat = myfunc_fsub.mk_a2convolution(a2figdat.T, a2filter.T, miss).T
    #a2figdat = myfunc_fsub.mk_a2convolution(a2figdat.T, a2filter.T, miss).T
  
  if sum3x3flag == True:
    a2figdat = myfunc_fsub.mk_3x3sum_one(a2figdat.T, miss).T
  #------------------
  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
  print figname

#*** MME **********
llkey = [[season,expr] for season in lseason for expr in lexpr]
for season, expr in llkey:
  #---
  a2freq  = zeros([ny,nx],float32)
  a2shade = ones([ny,nx],float32)
  #---
  for model in lmodel:
    ens   = cmip_para.ret_ens(model, expr, "psl")
    sunit, scalendar = cmip_para.ret_unit_calendar(model,expr)
    iyear,eyear = dyrange[expr]
    lyear       = range(iyear,eyear+1)
    lmon        = ctrack_para.ret_lmon(season)
  
    thsst    = tc_para.ret_thsst()
    thwind   = tc_para.ret_thwind()
    thrvort  = tc_para.ret_thrvort(model)
    thwcore  = tc_para.ret_thwcore(model)

    #--- shade       ------
    thorog     = ctrack_para.ret_thorog()
    orogname   = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog/orog.%s.sa.one"%(model,expr,model)
    a2orog     = fromfile(orogname, float32).reshape(ny,nx)
    a2one    = ones([ny,nx],float32)
    a2shade_tmp  = ma.masked_where( a2orog >=thorog, a2one).filled(miss)
    a2shade  = ma.masked_where(a2shade_tmp==miss, a2shade).filled(miss)

    #---------
    sidir_root  = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/tc/freq.%02dh"%(model,expr,thdura)
    sidir = sidir_root + "/%04d-%04d.%s"%(iyear,eyear,season)
    siname = sidir + "/freq.tc.%s.wc%4.2f.sst%02d.wind%02d.vor%.1e.%s.rad%04dkm.%04d-%04d.%s.sa.one"%(model, thwcore, thsst-273.15, thwind, thrvort, ens, countrad,iyear,eyear,season)
    a2in   = fromfile(siname, float32).reshape(ny,nx)
    a2freq = a2freq + a2in 
  #---
  a2freq  = a2freq / len(lmodel)

  sodir   = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/tc/freq.%02dh/%04d-%04d.%s"%("MME",expr,thdura,iyear,eyear,season)
  ctrack_func.mk_dir(sodir)

  soname  = sodir + "/freq.tc.MME.rad%04d.%04d-%04d.%s.sa.one"%(countrad,iyear,eyear,season)

  a2freq.tofile(soname)
  
  #*** Figure *********
  #-----------
  if len(lmon) ==12:
    if sum3x3flag == True:
      #bnd        = [0.01,0.25,0.5,1.0,2.0,4.0]
      bnd        = [0.1,0.25,0.5,1.0,2.0,4.0]
    if sum3x3flag == False:
      bnd        = [0.01, 0.025, 0.5, 0.1, 0.2, 0.4]
  elif len(lmon) ==3:
    #bnd        = [0.01,0.25,0.5,1.0,2.0,4.0]
    bnd        = [0.1,0.25,0.5,1.0,2.0,4.0]
  elif len(lmon) ==1:
    #bnd        = [0.01,0.25,0.5,1.0,2.0,4.0]
    bnd        = [0.1,0.25,0.5,1.0,2.0,4.0]
  #-----------

  model   = "MME"
  figdir     = sodir

  #-----------
  if (filterflag == True)&(sum3x3flag==True):
    figname    = soname[:-7] + ".filt.3x3.png"
  if (filterflag == True)&(sum3x3flag==False):
    figname    = soname[:-7] + ".filt.png"
  if (filterflag == False)&(sum3x3flag==True):
    figname    = soname[:-7] + ".3x3.png"
  if (filterflag == False)&(sum3x3flag==False):
    figname    = soname[:-7] + ".png"
  #-----------
  if sum3x3flag == True:
    cbarname   = soname[:-7] + ".3x3.cbar.png"
  elif sum3x3flag == False:
    cbarname   = soname[:-7] + ".cbar.png"
  #----------
  stitle   = "freq(percent) %s.TC season:%s %04d-%04d %s"%(model,season,iyear, eyear,ens)
  mycm     = "Spectral"
  #----- unit -------
  totaldays = ctrack_para.ret_totaldays(iyear,eyear,season)
  #a2figdat = ma.masked_equal(a2freq, miss).filled(0.0) * 100.0
  a2figdat = ma.masked_equal(a2freq, miss).filled(0.0) * totaldays / len(lyear)  # [days per season]
  #--- filtering ----
  if filterflag == True:
    a2figdat = myfunc_fsub.mk_a2convolution(a2figdat.T, a2filter.T, miss).T
    #a2figdat = myfunc_fsub.mk_a2convolution(a2figdat.T, a2filter.T, miss).T
  
  if sum3x3flag == True:
    a2figdat = myfunc_fsub.mk_3x3sum_one(a2figdat.T, miss).T
  #------------------
  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
  print figname


   
