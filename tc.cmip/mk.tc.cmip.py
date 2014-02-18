from numpy import *
from ctrack_fsub import *
import calendar
import ctrack_para
import ctrack_func
import tc_para, cmip_para, cmip_func
#-----------------------------------------
#bnflag    = True
bnflag    = False
#singleday = True
singleday = False
#lmodel=["CCSM","MRI-CGCM3","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel=["MRI-CGCM3"]
#lmodel=["inmcm4"]
##------------------
#lexpr  = ["historical","rcp85"]
#lexpr  = ["historical"]
lexpr  = ["rcp85"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
#------------------
lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon   = [9]
stepday = 0.25
miss   = -9999.0

ny     = 180
nx     = 360
dpgradrange   = ctrack_para.ret_dpgradrange()
thpgrad        = dpgradrange[1][0] 
thdura   = 48

#for expr,model in [[expr, model] for expr in lexpr for model in lmodel]:
for model,expr in [[model,expr] for model in lmodel for expr in lexpr]:
  #----
  ens   = cmip_para.ret_ens(model, expr, "psl")
  sunit, scalendar = cmip_para.ret_unit_calendar(model,expr)
  iyear, eyear = dyrange[expr] 
  #----
  #thsst    = 273.15 + 25.0
  #thwind   = 0.0 #m/s 
  #thrvort  = 7.0e-5
  #thwcore  = 0.5  # (K)
  thsst    = tc_para.ret_thsst()
  thwind   = tc_para.ret_thwind()
  thrvort  = tc_para.ret_thrvort(model)
  #thwcore  = tc_para.ret_thwcore(model)
  
  plev_low = 850*100.0 # (Pa)
  plev_mid = 500*100.0 # (Pa)
  plev_up  = 250*100.0 # (Pa)
 
  psldir_root     = "/media/disk2/data/CMIP5/sa.one.%s.%s/psl"%(model,expr)
  #
  #***** cyclone directories *******
  if bnflag == True:
    pgraddir_root   = "/media/disk2/out/CMIP5/bn.sa.one.%s.%s/6hr/pgrad"%(model,expr)
    lifedir_root    = "/media/disk2/out/CMIP5/bn.sa.one.%s.%s/6hr/life"%(model,expr)
    lastposdir_root = "/media/disk2/out/CMIP5/bn.sa.one.%s.%s/6hr/lastpos"%(model,expr)
    iposdir_root    = "/media/disk2/out/CMIP5/bn.sa.one.%s.%s/6hr/ipos"%(model,expr)
    nextposdir_root = "/media/disk2/out/CMIP5/bn.sa.one.%s.%s/6hr/nextpos"%(model,expr)
  elif bnflag == False:
    pgraddir_root   = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/pgrad"%(model,expr)
    lifedir_root    = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/life"%(model,expr)
    lastposdir_root = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/lastpos"%(model,expr)
    iposdir_root    = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/ipos"%(model,expr)
    nextposdir_root = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/nextpos"%(model,expr)
  #*********************************
  #
  tdir_root       = "/media/disk2/data/CMIP5/sa.one.%s.%s/ta"%(model,expr)
  udir_root       = "/media/disk2/data/CMIP5/sa.one.%s.%s/ua"%(model,expr)
  vdir_root       = "/media/disk2/data/CMIP5/sa.one.%s.%s/va"%(model,expr)
  #
  sstdir_root     = "/media/disk2/data/CMIP5/sa.one.%s.%s/ts"%(model,expr)
  #
  #***** OUTPUT directory **********
  if bnflag == True:
    #sodir_root      = "/media/disk2/out/CMIP5/bn.sa.one.%s.%s/6hr/tc/%02dh"%(model,expr,thdura)
    sodir_root      = "/media/disk2/out/CMIP5/bn.sa.one.%s.%s/6hr/tc/pot.tc.%02dh.sst%02d.wind%02d.vor%.1e"%(model,expr,thdura,thsst-273.15,thwind,thrvort)
  elif bnflag == False:
    #sodir_root      = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/tc/%02dh"%(model,expr,thdura)
    sodir_root      = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/tc/pot.tc.%02dh.sst%02d.wind%02d.vor%.1e"%(model,expr,thdura,thsst-273.15,thwind,thrvort)

  #** land sea mask -------------------
  landseadir      = "/media/disk2/data/CMIP5/sa.one.%s.%s/sftlf"%(model,expr)
  landseaname     = landseadir + "/sftlf.%s.sa.one"%(model)
  a2landsea       = fromfile(landseaname, float32).reshape(ny,nx)
  a2landsea       = ma.masked_greater(a2landsea, 0.0).filled(1.0) 
  #-----------------------------------------
  a2lastflag      = ones([ny,nx], float32)*miss
  initflag        = -1
  #-----------------------------------------
  #*****************************************
  # Time Loop
  #*****************************************
  a1dtime,a1tnum  = cmip_func.ret_times(iyear,eyear,lmon,sunit,scalendar,stepday, model=model)
  for dtime, tnum in map(None, a1dtime, a1tnum):
    year,mon,day,hour = dtime.year, dtime.month, dtime.day, dtime.hour

    #-- init --
    sodir  = sodir_root + "/%04d/%02d"%(year,mon)
    ctrack_func.mk_dir(sodir)
    a2num  = zeros([ny,nx],float32).reshape(ny,nx)
    ##############
    #  SST
    #-------------
    sstdir   = sstdir_root + "/%04d"%(year)
    sstname  = sstdir + "/ts.%s.%04d%02d000000.sa.one"%(ens, year, mon)
    a2sst    = fromfile( sstname, float32).reshape(ny,nx)
    #-------------
    initflag        = initflag + 1
    stime  = "%04d%02d%02d%02d00"%(year, mon, day, hour)
    #
    pgraddir        = pgraddir_root   + "/%04d%02d"%(year, mon)
    lifedir         = lifedir_root    + "/%04d%02d"%(year, mon)
    iposdir         = iposdir_root    + "/%04d%02d"%(year, mon)
    lastposdir      = lastposdir_root + "/%04d%02d"%(year, mon)
    nextposdir      = nextposdir_root + "/%04d%02d"%(year, mon)
    tdir            = tdir_root       + "/%04d%02d"%(year, mon)
    udir            = udir_root       + "/%04d%02d"%(year, mon)
    vdir            = vdir_root       + "/%04d%02d"%(year, mon)
    #
    pgradname       = pgraddir   + "/pgrad.%s.%s.sa.one"%(ens, stime)
    lifename        = lifedir    + "/life.%s.%s.sa.one"%(ens, stime)
    nextposdir      = nextposdir_root + "/%04d%02d"%(year, mon)
    iposname        = iposdir    + "/ipos.%s.%s.sa.one"%(ens, stime)
    lastposname     = lastposdir + "/lastpos.%s.%s.sa.one"%(ens, stime)
    nextposname     = nextposdir + "/nextpos.%s.%s.sa.one"%(ens, stime)
    tlowname        = tdir       + "/ta.%04dhPa.%s.%s.sa.one"%(plev_low*0.01, ens, stime)
    tmidname        = tdir       + "/ta.%04dhPa.%s.%s.sa.one"%(plev_mid*0.01, ens, stime)
    tupname         = tdir       + "/ta.%04dhPa.%s.%s.sa.one"%(plev_up *0.01, ens, stime)
    ulowname        = udir       + "/ua.%04dhPa.%s.%s.sa.one"%(plev_low*0.01, ens, stime)
    uupname         = udir       + "/ua.%04dhPa.%s.%s.sa.one"%(plev_up *0.01, ens, stime)
    vlowname        = vdir       + "/va.%04dhPa.%s.%s.sa.one"%(plev_low*0.01, ens, stime)
    vupname         = vdir       + "/va.%04dhPa.%s.%s.sa.one"%(plev_up *0.01, ens, stime)
    #
    a2pgrad         = fromfile(pgradname, float32).reshape(ny, nx)
    a2life          = fromfile(lifename,  int32).reshape(ny, nx)
    a2ipos          = fromfile(iposname,  int32).reshape(ny, nx)
    a2lastpos       = fromfile(lastposname,int32).reshape(ny, nx)
    a2nextpos       = fromfile(nextposname,  int32).reshape(ny, nx)
  
    a2tlow          = fromfile(tlowname,  float32).reshape(ny, nx)
    a2tmid          = fromfile(tmidname,  float32).reshape(ny, nx)
    a2tup           = fromfile(tupname,   float32).reshape(ny, nx)
    a2ulow          = fromfile(ulowname,  float32).reshape(ny, nx)
    a2uup           = fromfile(uupname,   float32).reshape(ny, nx)
    a2vlow          = fromfile(vlowname,  float32).reshape(ny, nx)
    a2vup           = fromfile(vupname,   float32).reshape(ny, nx)
    #--------------------------------
    tout            = ctrack_fsub.find_tc_saone(\
                      a2pgrad.T, a2life.T, a2lastpos.T, a2lastflag.T, a2tlow.T, a2tmid.T, a2tup.T, a2ulow.T, a2uup.T, a2vlow.T, a2vup.T, a2sst.T, a2landsea.T\
                    , thpgrad, thdura, thsst, thwind, thrvort, initflag, miss)
  
    #tout_old        = ctrack_fsub.find_tc_saone_old(\
    #                  a2pgrad.T, a2life.T, a2lastpos.T, a2lastflag.T, a2tlow.T, a2tmid.T, a2tup.T, a2ulow.T, a2uup.T, a2vlow.T, a2vup.T, a2sst.T, a2landsea.T\
    #                , thpgrad, thdura, thsst, thwind, thrvort, initflag, miss)
  
  
  
    #
    a2tcloc         = tout[0].T
    a2lastflag      = tout[1].T
    
    #---- save -----------------------
    #soname   = sodir + "/tc.wc%4.2f.sst%02d.wind%02d.vor%.1e.%s.sa.one"%(thwcore, thsst-273.15, thwind, thrvort, stime)
    soname   = sodir + "/pot.tc.%s.sa.one"%(stime)
    a2tcloc.tofile(soname)
    print soname
