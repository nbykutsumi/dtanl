from numpy import *
from ctrack_fsub import *
import calendar
import ctrack_para, cmip_para
import ctrack_func, cmip_func
import tc_para
#-----------------------------------------
#singleday = True
singleday = False
lmodel = ["MRI-CGCM3","CNRM-CM5","MIROC5","HadGEM2-ES","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","IPSL-CM5A-MR","NorESM1-M","GFDL-CM3","IPSL-CM5B-LR"]
#lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
#lexpr   = ["historical", "rcp85"]
lexpr   = ["historical"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
lmon    = [1,2,3,4,5,6,7,8,9,10,11,12]
stepday = 0.25
miss   = -9999.0
#countrad = 300.0 # [km]
countrad = 1.0 # [km]

ny     = 180
nx     = 360
thdura = 48
#--- init ------
a2one  = ones([ny,nx],float32)
#---------------
llkey  = [[expr,model] for expr in lexpr for model in lmodel]
for expr, model in llkey:
  #----
  ens   = cmip_para.ret_ens(model, expr, "psl")
  sunit, scalendar = cmip_para.ret_unit_calendar(model,expr)
  iyear,eyear      = dyrange[expr]
  lyear            = range(iyear,eyear+1)
  #----

  dpgradrange   = ctrack_para.ret_dpgradrange()
  thpgrad        = dpgradrange[1][0] 
  thsst    = tc_para.ret_thsst()
  thwind   = tc_para.ret_thwind()
  thrvort  = tc_para.ret_thrvort(model)
  thwcore  = tc_para.ret_thwcore(model)

 
  #** land sea mask --------------
  orogname   = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog/orog.%s.sa.one"%(model,expr,model)  
  #-----------------------------------------
  a1dtime,a1tnum  = cmip_func.ret_times(iyear,eyear,lmon,sunit,scalendar,stepday,model=model)
  for year in lyear:
    for mon in lmon:
      #** init -------------------
      a2num    = zeros([ny,nx],float32)
      #---------------------------
      for dtime, tnum in map(None, a1dtime, a1tnum):
        yeart,mont,dayt,hourt = dtime.year, dtime.month, dtime.day, dtime.hour
        #--- check year and month ---
        if not (yeart==year)&(mont==mon):
          continue
        #----------------------------
        stime  = "%04d%02d%02d%02d00"%(yeart,mont,dayt,hourt)
        print "mk.freq.tc.obj.cmip","rad",countrad,yeart,mont,dayt,hourt

        #-- load -------
        tcdir  = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/tc/%02dh/%04d/%02d"%(model,expr,thdura,year,mon) 
      
        tcname  = tcdir + "/tc.wc%4.2f.sst%02d.wind%02d.vor%.1e.%s.sa.one"%(thwcore, thsst-273.15, thwind, thrvort, stime)
      
        a2tc      = fromfile(tcname, float32).reshape(180,360)
        #a2num_tmp = ma.masked_where(a2tc==miss, a2one).filled(0.0)
        a2num_tmp = ctrack_fsub.mk_territory_saone(a2tc.T, countrad*1000.0, miss, -89.5, 1.0, 1.0).T
        a2num_tmp = ma.masked_equal(a2num_tmp, miss).filled(0.0)
        a2num     = a2num + a2num_tmp
      
      #--- write -------
      sodir_root  = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/tc/freq.%02dh"%(model,expr,thdura)
      sodir       = sodir_root + "/%04d"%(year)
      ctrack_func.mk_dir(sodir)
      soname      = sodir + "/num.tc.wc%4.2f.sst%02d.wind%02d.vor%.1e.%s.rad%04dkm.%04d.%02d.sa.one"%(thwcore, thsst-273.15, thwind, thrvort,ens,countrad,year,mon)
      #
      a2num.tofile(soname)
      
      
      
      
