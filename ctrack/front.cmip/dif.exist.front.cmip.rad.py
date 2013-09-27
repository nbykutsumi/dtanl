from numpy import *
import ctrack_fig
import ctrack_func
import cmip_para, ctrack_para, front_para
#-----------------------------
lmodel = ["MIROC5"]
lfutexpr = ["rcp85"]
iyear_his = 1980
eyear_his = 1999
#eyear_his = 1980
dyrange  = {"rcp85":[2080,2099]}
#dyrange  = {"rcp85":[2080,2080]}
lseason  = ["ALL"]
#lseason  = [1]
thdura   = 48
countrad = 300.0 # [km]
#---------------
lllat  = -89.5
lllon  = 0.5
urlat  = 89.5
urlon  = 359.5
#---------------
ny,nx  = 180, 360
miss   = -9999.0

llkey = [[futexpr, model, season] for futexpr in lfutexpr for model in lmodel for season in lseason]
for futexpr, model, season in llkey:
  iyear_fut, eyear_fut = dyrange[futexpr]
  #-- parameter --
  ens   = cmip_para.ret_ens(model, futexpr, "psl")
  thfmask1t, thfmask2t, thfmask1q, thfmask2q   = front_para.ret_thfmasktq(model)  

  #--- shade       ------
  thorog     = ctrack_para.ret_thorog()
  orogname   = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog/orog.%s.sa.one"%(model,futexpr,model)
  a2orog     = fromfile(orogname, float32).reshape(ny,nx)
  a2one    = ones([ny,nx],float32)
  a2shade  = ma.masked_where( a2orog >=thorog, a2one).filled(miss)

  #---------------
  idir_fut = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/front.t/freq/%04d-%04d.%s"%(model,futexpr,iyear_fut,eyear_fut,season)
  idir_his = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/front.t/freq/%04d-%04d.%s"%(model,"historical",iyear_his,eyear_his,season)
  
  iname_fut= idir_fut + "/freq.t.front.%s.%s.rad%04dkm.M1_%4.2f_M2_%3.1f.%04d-%04d.%s.sa.one"%(model,ens,countrad,thfmask1t,thfmask2t,iyear_fut,eyear_fut,season)
  iname_his= idir_his + "/freq.t.front.%s.%s.rad%04dkm.M1_%4.2f_M2_%3.1f.%04d-%04d.%s.sa.one"%(model,ens,countrad,thfmask1t,thfmask2t,iyear_his,eyear_his,season)

  #---------------
  a2freq_fut = fromfile(iname_fut, float32).reshape(ny,nx)
  a2freq_his = fromfile(iname_his, float32).reshape(ny,nx)
  a2freq_dif = a2freq_fut - a2freq_his

  #-- write ------
  sodir      = idir_fut
  soname     = sodir + "/dif.freq.t.front.%s.%s.rad%04dkm.M1_%4.2f_M2_%3.1f.%04d-%04d.%s.sa.one"%(model,ens,countrad,thfmask1t,thfmask2t,iyear_fut,eyear_fut,season)
  a2freq_dif.tofile(soname)

  #*******************************
  # Figure
  #-----------
  bnd         = [-21,-15,-9,-3,3,9,15,21]
  #bnd         = [-1.0, -0.5, -0.1, 0.1, 0.5, 1.0]
  #bnd        = [0.01,0.25,0.5,1.0,2.0,4.0,8.0]
  #bnd        = [0.25,0.5,1.0,2.0,4.0,8.0]
  #bnd         = [5,10,15,20,25,30,35,40,45]
  #bnd        = [10,20,30,40,50,60,70,80]
  figdir     = sodir
  figname    = soname[:-7] + ".png"
  cbarname   = soname[:-7] + ".cbar.png"
  #----------
  stitle   = "freq. %s.ExC season:%s %04d-%04d %s"%(model,season,iyear_fut, eyear_fut,ens)
  #mycm     = "Spectral"
  mycm     = "RdBu_r"
  datname  = soname
  a2figdat = fromfile(datname, float32).reshape(ny,nx)

  #-------------------------------
  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
  ctrack_fig.mk_pict_saone_reg_symm(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
  print figname



