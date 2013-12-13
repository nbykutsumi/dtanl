from ctrack_fsub import *
from numpy import *
import matplotlib.pyplot as plt
import calendar
import ctrack_para, tc_para, cmip_para, front_para
import ctrack_func, tc_func, cmip_func, front_func
import ctrack_fig
import sys, os
#--------------------------------------
#lmodel = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
#lmodel = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","GFDL-CM3"]
lmodel = ["IPSL-CM5A-MR","CNRM-CM5"]
#lmodel = ["MIROC5","inmcm4","MPI-ESM-MR"]
#lmodel = ["CSIRO-Mk3-6-0","NorESM1-M","GFDL-CM3"]
#lexpr   = ["historical","rcp85"]
lexpr   = ["historical"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
lmon    = range(1,12+1)
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

thdura_c  = 48
thdura_tc = thdura_c
thorog  = ctrack_para.ret_thorog()
#----------------------------
dlat    = 1.0
dlon    = 1.0
a1lat   = arange(-89.5, 89.5 +dlat*0.5,  dlat)
a1lon   = arange(0.5,   359.5 +dlon*0.5, dlon)
#--------------
a2one   = ones([ny,nx],float32)
#--------------
llkey  = [[expr,model] for expr in lexpr for model in lmodel]
for expr, model in llkey:
  #----
  ens   = cmip_para.ret_ens(model, expr, "psl")
  sunit, scalendar = cmip_para.ret_unit_calendar(model,expr)
  iyear,eyear      = dyrange[expr]
  lyear            = range(iyear,eyear+1)
  #----------------------------
  #-- orog ------------------------
  orogname   = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog/orog.%s.sa.one"%(model,expr,model)
  gradname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/maxgrad.0200km.sa.one"
  a2orog     = fromfile(orogname, float32).reshape(ny,nx)
  a2gradorog = fromfile(gradname, float32).reshape(ny,nx)
  #--- ExC -------
  dpgradrange  = ctrack_para.ret_dpgradrange(model)
  thpgrad      = dpgradrange[0][0]
  pgradmin     = dpgradrange[2][0]  # Pa/1000km
  
  #--- TC --------
  thsst    = tc_para.ret_thsst()
  thwind   = tc_para.ret_thwind()
  thrvort  = tc_para.ret_thrvort(model)
  thwcore  = tc_para.ret_thwcore(model)

  #--- Front -----
  thfmask1t, thfmask2t, thfmask1q, thfmask2q   = front_para.ret_thfmasktq(model)
  print 1
  plev     = 850*100.0 # (Pa)
  print 2
  thorog     = ctrack_para.ret_thorog()
  thgradorog = ctrack_para.ret_thgradorog()
  thgrids    = front_para.ret_thgrids()

  #-----------------------------------------
  a1dtime,a1tnum  = cmip_func.ret_times(iyear,eyear,lmon,sunit,scalendar,stepday,model=model) 
  for year in lyear:
    for mon in lmon:
      #--- init ------------------
      a2count  = zeros([ny,nx],float32)

      #---------------------------
      for dtime, tnum in map(None, a1dtime, a1tnum):
        yeart,mont,dayt,hourt = dtime.year, dtime.month, dtime.day, dtime.hour
        #--- check year and month ---
        if not (yeart==year)&(mont==mon):
          continue
        #----------------------------
        stime  = "%04d%02d%02d%02d00"%(yeart,mont,dayt,hourt)
        print "freq.cf",model,"rad",countrad,yeart,mont,dayt,hourt

        psldir_root  = "/media/disk2/data/CMIP5/sa.one.%s.%s/psl"%(model,expr)
        pgraddir_root= "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/pgrad"%(model,expr)
        lifedir_root = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/life"%(model,expr)
     
        psldir       = psldir_root     + "/%04d%02d"%(year, mon)
        pgraddir     = pgraddir_root   + "/%04d%02d"%(year, mon)
        lifedir      = lifedir_root    + "/%04d%02d"%(year, mon)
        
        pslname      = psldir     + "/psl.%s.%s.sa.one"%(ens,stime)
        pgradname    = pgraddir   + "/pgrad.%s.%s.sa.one"%(ens,stime)
        lifename     = lifedir    + "/life.%s.%s.sa.one"%(ens,stime)
        
        a2pgrad      = fromfile(pgradname, float32).reshape(ny, nx)
        a2life       = fromfile(lifename,  int32).reshape(ny, nx)

        #************************
        # load TCs
        #------------------------
        tcdir  = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/tc/%02dh/%04d/%02d"%(model,expr,thdura_tc,year,mon)

        tcname  = tcdir + "/tc.wc%4.2f.sst%02d.wind%02d.vor%.1e.%s.sa.one"%(thwcore, thsst-273.15, thwind, thrvort, stime)

        a2tc      = fromfile(tcname, float32).reshape(180,360) 
        #************************
        # screen ExC
        #------------------------
        a2dura      = ctrack_fsub.solvelife(a2life.T, miss_int)[0].T
        a2c         = ma.masked_where(a2dura<thdura_c, a2pgrad)
        a2c         = ma.masked_less(a2c, pgradmin).filled(miss)
        #a2c         = ctrack_fsub.mk_8gridsmask_saone(a2c.T, miss).T
        a2c_terr    = ctrack_fsub.mk_territory_saone(a2c.T, countrad*1000.0, miss, -89.5, 1.0, 1.0).T  
        a2c_terr    = ma.masked_where(a2c_terr==miss, a2one).filled(0.0)
        #------------------------
        #************************
        # for objective front locator
        #-----------------------------
        # Name
        frontdir_t_root = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/front.t"%(model,expr)
        frontdir_t  = frontdir_t_root + "/%04d%02d"%(year, mon)
        #
        fronttname1 = frontdir_t + "/front.t.M1.%04d.%02d.%02d.%02d.sa.one"%(yeart, mont, dayt, hourt)
        fronttname2 = frontdir_t + "/front.t.M2.%04d.%02d.%02d.%02d.sa.one"%(yeart, mont, dayt, hourt)

        #-- front.t ---
        a2fbc1      = fromfile(fronttname1, float32).reshape(ny,nx)
        a2fbc2      = fromfile(fronttname2, float32).reshape(ny,nx)
        a2fbc       = front_func.complete_front_t_saone(a2fbc1, a2fbc2, thfmask1t, thfmask2t, a2orog, a2gradorog, thorog, thgradorog, thgrids, miss )

        #-- count baloclinic front loc --
        a2loc = a2fbc
        a2fbc_terr  = ctrack_fsub.mk_territory_saone( a2loc.T, countrad*1000.0, miss, -89.5, 1.0, 1.0).T
        a2fbc_terr  = ma.masked_where(a2fbc_terr ==miss, a2one).filled(0.0)

        #*************************
        # count ExC + Front
        #-------------------------
        a2count_tmp = ma.masked_greater(a2c_terr + a2fbc_terr, 0.0).filled(1.0)
        a2count     = a2count + a2count_tmp

      #****************************
      # write
      #-----------------
      odir_root= "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/cf/freq.%02dh.M1_%s.M2_%s"%(model,expr,thdura_c,thfmask1t,thfmask2t)
      odir     = odir_root + "/%04d"%(year)

      oname    = odir + "/num.cf.%s.%s.rad%04dkm.%04d.%02d.sa.one"%(model, ens, countrad, year,mon)
      #--- write -----
      ctrack_func.mk_dir(odir)
      a2count.tofile(oname)
      print oname

#    #***************
#    # figure
#    #---------------
#    #  figure all
#    #---------------------------
#    bnd        = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0]
#    #bnd        = [5,10,15,20,25,30,35,40,45]
#    #bnd        = [10,20,30,40,50,60,70,80]
#    #----------
#    figdir   = odir + "/pict"
#    ctrack_func.mk_dir(figdir)
#    figname  = figdir + "/freq.exc.%stc.%04d-%04d.%s.png"%(bstflag_tc,iyear,eyear,season)
#    cbarname = figdir + "/freq.exc.%stc.cbar.%s.png"%(bstflag_tc,season)
#    #----------
#    stitle   = "freq. exc: w/%s tc season:%s %04d-%04d"%(bstflag_tc, season,iyear, eyear)
#    mycm     = "Spectral"
#    datname  = oname
#    a2figdat = fromfile(datname, float32).reshape(ny,nx)
#    #-------------------------------
#    a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
#    ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
#    print figname  
#   





