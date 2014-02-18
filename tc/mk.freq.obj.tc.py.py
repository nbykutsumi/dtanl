from numpy import *
from myfunc_fsub import *
from ctrack_fsub import *
import ctrack_fig
import ctrack_para, tc_para
import ctrack_func
#--------------------------
#filterflag = True
filterflag = False

#sum3x3flag = True
sum3x3flag = False

lmodel  = ["org"]
#iyear   = 1997
#eyear   = 2011
iyear   = 1980
eyear   = 1999
lyear   = range(iyear,eyear+1)
#lseason = ["ALL"]
lseason = range(1,12+1)
#lthsst  = array([15, 20, 25, 18, 22]) + 273.15
lthsst  = array([20,21,22,24,25,]) + 273.15

filtradkm = 1000.0 # km

countrad = 1000.0 # (km)
#countrad = 1.0 # (km)
ny,nx   = 180,360
miss    = -9999.0


a2areanum = ctrack_fsub.mk_a2radsum_saone(ones([ny,nx],float32).T, filtradkm, miss).T

#a2filter = array(\
#           [[1,2,1]\
#           ,[2,4,2]\
#           ,[1,2,1]], float32)

#a2filter = array(\
#           [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
#           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]], float32)

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

llkey = [[model,season,thsst] for model in lmodel for season in lseason for thsst in lthsst]
for model,season,thsst in llkey:
  thdura   = 48
  #thsst    = tc_para.ret_thsst()
  thwind   = tc_para.ret_thwind()
  thrvort  = tc_para.ret_thrvort(model)
  thwcore  = tc_para.ret_thwcore(model)
  #
  lmon     = ctrack_para.ret_lmon(season)
  #------------------
  a2num    = zeros([ny,nx],float32)
  for year in lyear:
    for mon in lmon:
      sidir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/tc/freq.%02dh.wc%4.2f.sst%02d.wind%02d.vor%.1e"%(model,thdura,thwcore,thsst-273.15,thwind,thrvort)
      #sidir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/tc/freq.%02dh"%(model,thdura)
      sidir      = sidir_root + "/%04d"%(year)
      siname     = sidir + "/num.tc.rad%04dkm.%04d.%02d.sa.one"%(countrad,year,mon)
      a2num_tmp  = fromfile(siname, float32).reshape(ny,nx)
      a2num      = a2num + a2num_tmp
    
  #-----------------------------------------
  totalnum   = ctrack_para.ret_totaldays(iyear,eyear,season) * 4.0
  a2freq     = a2num / totalnum
  sodir_root = sidir_root
  sodir      = sodir_root + "/%04d-%04d.%s"%(iyear,eyear,season)
  ctrack_func.mk_dir(sodir)
  soname     = sodir + "/freq.tc.rad%04dkm.%04d-%04d.%s.sa.one"%(countrad,iyear,eyear,season)
  a2freq.tofile(soname)
  print soname
  #*******************************
  # Figure
  #-----------
  if len(lmon) ==12:
    if sum3x3flag == True:
      #bnd        = [0.01,0.25,0.5,1.0,2.0,4.0]
      bnd        = [0.1,0.25,0.5,1.0,2.0,4.0]
    elif sum3x3flag == False:
      if countrad == 1000.0:
        bnd        = [1,3,6,9,12,15,18,21]
      else:
        bnd        = [0.01, 0.02, 0.05, 0.1, 0.2, 0.3, 0.4]
    
  elif len(lmon) ==3:
    #bnd        = [0.01,0.25,0.5,1.0,2.0,4.0]
    bnd        = [0.1,0.25,0.5,1.0,2.0,4.0]
  elif len(lmon) ==1:
    #bnd        = [0.01,0.25,0.5,1.0,2.0,4.0]
    bnd        = [0.1,0.25,0.5,1.0,2.0,4.0]
  #-----------
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
  stitle   = "freq. JRA25.TC season:%s %04d-%04d sst%02d wc%4.2f vor%.1e"%(season,iyear, eyear, thsst-273.15, thwcore, thrvort)
  mycm     = "Spectral"
  datname  = soname
  a2figdat = fromfile(datname, float32).reshape(ny,nx)
  #-------------------------------
  totaldays = ctrack_para.ret_totaldays(iyear,eyear,season)
  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
  #a2figdat = ma.masked_equal(a2freq, miss).filled(0.0) * totaldays / len(lyear)  # [days per season]

  #--- filtering ----
  if filterflag == True:
    #a2figdat = myfunc_fsub.mk_a2convolution(a2figdat.T, a2filter.T, miss).T
    a2figdat = ctrack_fsub.mk_a2radsum_saone(a2figdat.T, filtradkm, miss).T
    a2figdat = a2figdat / a2areanum

  if sum3x3flag == True:
    a2figdat = myfunc_fsub.mk_3x3sum_one(a2figdat.T, miss).T
  #------------------
  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
  print figname
  





