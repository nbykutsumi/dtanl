from numpy import *
import sys
import calendar
from ctrack_fsub import *
from dtanl_fsub import *
import front_para, ctrack_para, cmip_para
import front_func, ctrack_func, cmip_func
#---------------------------------
#sresol = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
#lmodel = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","GFDL-CM3"]
lmodel = ["MRI-CGCM3","IPSL-CM5B-LR"]
#lexpr   = ["historical","rcp85"]
lexpr   = ["historical"]
#lexpr   = ["rcp85"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
#dyrange = {"historical":[1980,1995], "rcp85":[2080,2099]}
lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
ny    = 180
nx    = 360
miss  = -9999.0
thdist   = front_para.ret_thdistkm()  # (km)
stepday  = 0.25
#
#countrad = 300  # (km) for frequency count
countrad = 1.0  # (km) for frequency count
#
#-- para for objective locator -------------
plev     = 850*100.0 # (Pa)
thorog     = ctrack_para.ret_thorog()
thgradorog = ctrack_para.ret_thgradorog()
thgrids    = front_para.ret_thgrids()

llkey  = [[expr,model] for expr in lexpr for model in lmodel]
for expr, model in llkey:
  #----
  ens   = cmip_para.ret_ens(model, expr, "psl")
  sunit, scalendar = cmip_para.ret_unit_calendar(model,expr)
  iyear,eyear = dyrange[expr]
  lyear       = range(iyear,eyear+1)
  thfmask1t, thfmask2t, thfmask1q, thfmask2q   = front_para.ret_thfmasktq(model)
  orogname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
  gradname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/maxgrad.0200km.sa.one"
  a2orog     = fromfile(orogname, float32).reshape(ny,nx)
  a2gradorog = fromfile(gradname, float32).reshape(ny,nx)
  
  #-------------------------------------------
  a2one    = ones([ny,nx],float32)
  #******************************
  for year in lyear:
    for mon in lmon:
      #************************
      #-- init for front ------
      a2count  = zeros([ny,nx],float32)
      #************************
      a1dtime,a1tnum  = cmip_func.ret_times(iyear,eyear,lmon,sunit,scalendar,stepday,model=model)

      for dtime, tnum in map(None, a1dtime, a1tnum):
        yeart,mont,dayt,hourt = dtime.year, dtime.month, dtime.day, dtime.hour
        #--- check year and month ---
        if not (yeart==year)&(mont==mon):
          continue
        #----------------------------
        print "agg.exist.front.cmip","rad",countrad,yeart,mont,dayt,hourt
        #-------------------
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
        #-------------------
        a2countterr = ctrack_fsub.mk_territory_saone( a2loc.T, countrad*1000.0, miss, -89.5, 1.0, 1.0).T
        a2count_tmp = ma.masked_where(a2countterr ==miss, a2one).filled(0.0)
  
        a2count     = a2count + a2count_tmp
      #********************************
      #-- for monthly data front ------
      odir       = frontdir_t_root + "/freq/%04d"%(year)
      ctrack_func.mk_dir(odir)
      oname      = odir + "/num.t.front.%s.%s.rad%04dkm.M1_%s_M2_%s.%04d.%02d.sa.one"%(model, ens, countrad, thfmask1t, thfmask2t, year, mon)
      a2count.tofile(oname)
      print oname
