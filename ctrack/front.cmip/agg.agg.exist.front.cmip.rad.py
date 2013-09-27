from ctrack_fsub import *
from numpy import *
import matplotlib.pyplot as plt
import calendar
import ctrack_para, tc_para, cmip_para, front_para
import ctrack_func, tc_func, cmip_func
import ctrack_fig
import sys, os
#--------------------------------------
#sresol = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel  = ["MIROC5"]
lexpr   = ["historical","rcp85"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}

#lexpr   = ["historical"]
#dyrange = {"historical":[1980,1980], "rcp85":[2080,2080]}
lseason = ["ALL"]
#lseason = [1]
#calcflag   = False
calcflag   = True
ny      = 180
nx      = 360

countrad  = 300.0 # [km]
stepday   = 0.25
miss_int= -9999
miss    = -9999.0
# local region ------
#
# corner points should be
# at the center of original grid box
#lllat   = 25.
#urlat   = 50.
#lllon   = 130.
#urlon   = 155.

lllat   = -89.5
urlat   = 89.5
lllon   = 0.5
urlon   = 359.5

thorog  = ctrack_para.ret_thorog()
#----------------------------
dlat    = 1.0
dlon    = 1.0
a1lat   = arange(-89.5, 89.5 +dlat*0.5,  dlat)
a1lon   = arange(0.5,   359.5 +dlon*0.5, dlon)
#--------------
a2one   = ones([ny,nx],float32)
#--------------
llkey  = [[expr,model,season] for expr in lexpr for model in lmodel for season in lseason]
for expr, model, season in llkey:
  lmon  = ctrack_para.ret_lmon(season)
  #----
  ens   = cmip_para.ret_ens(model, expr, "psl")
  sunit, scalendar = cmip_para.ret_unit_calendar(model,expr)
  iyear,eyear      = dyrange[expr]
  lyear            = range(iyear,eyear+1)
  thfmask1t, thfmask2t, thfmask1q, thfmask2q   = front_para.ret_thfmasktq(model)
  #-- orog ------------------------
  orogname   = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog/orog.%s.sa.one"%(model,expr,model)

  #--- init ------------------
  a2count  = zeros([ny,nx],float32)

  #-----------------------------------------
  a1dtime,a1tnum  = cmip_func.ret_times(iyear,eyear,lmon,sunit,scalendar,stepday) 
  for year in lyear:
    for mon in lmon:
      #----------------------------
      print "agg.exist.front.cmip","rad",countrad,year,mon
      #-- load ----------------
      #idir_root  = "/media/disk2/out/CMIP5/sa.one.MIROC5.historical/6hr/front.t/freq"
      idir_root  = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/front.t/freq"%(model,expr)
      idir       = idir_root + "/%04d"%(iyear)
      iname      = idir + "/num.t.front.%s.%s.rad%04dkm.M1_%4.2f_M2_%3.1f.sa.one"%(model,ens, countrad, thfmask1t, thfmask2t)
      a2count_tmp= fromfile(iname, float32).reshape(ny,nx)
      a2count    = a2count + a2count_tmp

  #****************************
  # write
  #-----------------
  totaltime = cmip_para.ret_totaldays_cmip(iyear,eyear,season,sunit=sunit,scalendar=scalendar) *4.0
  a2freq   = a2count / totaltime
  odir_root= idir_root
  odir     = odir_root + "/%04d-%04d.%s"%(iyear,eyear,season)

  oname    = odir + "/freq.t.front.%s.%s.rad%04dkm.M1_%4.2f_M2_%3.1f.%04d-%04d.%s.sa.one"%(model,ens, countrad, thfmask1t, thfmask2t, iyear,eyear,season)
  #--- write -----
  ctrack_func.mk_dir(odir)
  a2freq.tofile(oname)
  print oname

  #***************
  # figure
  #---------------
  #--- shade       ------
  thorog     = ctrack_para.ret_thorog()
  orogname   = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog/orog.%s.sa.one"%(model,expr,model)
  a2orog     = fromfile(orogname, float32).reshape(ny,nx)
  a2one    = ones([ny,nx],float32)
  a2shade  = ma.masked_where( a2orog >=thorog, a2one).filled(miss)

  bnd         = [5,10,15,20,25,30,35,40,45]
  #----------
  figdir   = odir
  ctrack_func.mk_dir(figdir)
  figname  = figdir + "/freq.t.front.%s.%s.rad%04dkm.M1_%4.2f_M2_%3.1f.%04d-%04d.%s.png"%(model,ens,countrad,thfmask1t,thfmask2t,iyear,eyear,season)
  cbarname = figname[:-4] + ".cbar.png"
  #----------
  stitle   = "freq. front.t: %s %s season:%s %04d-%04d"%(model, ens, season,iyear, eyear)
  mycm     = "Spectral"
  datname  = oname
  a2figdat = fromfile(datname, float32).reshape(ny,nx)
  #-------------------------------
  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
  print figname  
 





