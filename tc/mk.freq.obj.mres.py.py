from numpy import *
from myfunc_fsub import *
import ctrack_fig
import ctrack_para, tc_para
import ctrack_func
#--------------------------
lmodel  = ["org"]
#iyear   = 1997
#eyear   = 2011
iyear   = 1980
eyear   = 1999
lyear   = range(iyear,eyear+1)
lseason = ["ALL"]
#lseason = range(1,12+1)
#countrad = 300.0 # (km)
countrad = 1.0 # (km)
ny,nx   = 180,360
miss    = -9999.0

#-------------------------
lllat  = -89.5
lllon  = 0.5
urlat  = 89.5
urlon  = 359.5

#--- shade       ------
thorog     = ctrack_para.ret_thorog()
orogname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
a2orog     = fromfile(orogname, float32).reshape(ny,nx)
a2one    = ones([ny,nx],float32)
a2shade  = ma.masked_where( a2orog >=thorog, a2one).filled(miss)
#-------------------------

llkey = [[model,season] for model in lmodel for season in lseason]
for model,season in llkey:
  thdura   = 48
  thsst    = tc_para.ret_thsst()
  thwind   = tc_para.ret_thwind()
  thrvort  = tc_para.ret_thrvort(model)
  thwcore  = tc_para.ret_thwcore(model)
  #
  lmon     = ctrack_para.ret_lmon(season)
  #------------------
  a2num    = zeros([ny,nx],float32)
  for year in lyear:
    for mon in lmon:
      sidir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/tc/freq.%02dh"%(model,thdura)
      sidir      = sidir_root + "/%04d"%(year)
      siname     = sidir + "/num.tc.%s.%02dh.w%3.1f.sst%d.wind%d.vor%.1e.rad%04dkm.%04d.%02d.sa.one"%(model,thdura, thwcore,thsst-273.15, thwind, thrvort,countrad,year,mon)
      a2num_tmp  = fromfile(siname, float32).reshape(ny,nx)
      a2num      = a2num + a2num_tmp

    
  #-----------------------------------------
  totalnum   = ctrack_para.ret_totaldays(iyear,eyear,season) * 4.0
  a2freq     = a2num / totalnum
  sodir_root = sidir_root
  sodir      = sodir_root + "/%04d-%04d.%s"%(iyear,eyear,season)
  ctrack_func.mk_dir(sodir)
  soname     = sodir + "/freq.tc.%s.%02dh.w%3.1f.sst%d.wind%d.vor%.1e.rad%04dkm.%04d-%04d.%s.sa.one"%(model,thdura, thwcore,thsst-273.15, thwind, thrvort,countrad,iyear,eyear,season)
  a2freq.tofile(soname)
  print soname
  #*******************************
  # Figure
  #-----------
  if len(lmon) ==12:
    #bnd        = [0.01,0.25,0.5,1.0,2.0,4.0]
    bnd        = [0.1,0.25,0.5,1.0,2.0,4.0]
    #bnd        = [0.25,0.5,1.0,2.0,4.0]
  elif len(lmon) ==3:
    #bnd        = [0.01,0.25,0.5,1.0,2.0,4.0]
    bnd        = [0.1,0.25,0.5,1.0,2.0,4.0]
  elif len(lmon) ==1:
    #bnd        = [0.01,0.25,0.5,1.0,2.0,4.0]
    bnd        = [0.1,0.25,0.5,1.0,2.0,4.0]
  #-----------
  figdir     = sodir
  figname    = soname[:-7] + ".png"
  cbarname   = soname[:-7] + ".cbar.png"
  #----------
  stitle   = "freq.(days/season) JRA25.%s.TC season:%s %04d-%04d"%(model,season,iyear, eyear)
  mycm     = "Spectral"
  datname  = soname
  a2figdat = fromfile(datname, float32).reshape(ny,nx)
  #-------------------------------
  totaldays = ctrack_para.ret_totaldays(iyear,eyear,season)
  #a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
  a2figdat = ma.masked_equal(a2freq, miss).filled(0.0) * totaldays / len(lyear)  # [days per season]
  a2figdat = myfunc_fsub.mk_3x3sum_one(a2figdat.T, miss).T

  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
  print figname
  





