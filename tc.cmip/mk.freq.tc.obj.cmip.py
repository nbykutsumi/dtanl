from numpy import *
from ctrack_fsub import *
import calendar
import ctrack_para, cmip_para
import ctrack_func, cmip_func
import tc_para
#-----------------------------------------
#singleday = True
singleday = False
#lmodel = ["CCSM4","MRI-CGCM3","MIROC5","MPI-ESM-MR","CSIRO-Mk3-6-0","GFDL-CM3","IPSL-CM5B-LR"]
lmodel = ["CCSM4"]
#lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
#lexpr   = ["historical", "rcp85"]
lexpr   = ["historical"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
lmon    = [1,2,3,4,5,6,7,8,9,10,11,12]
stepday = 0.25
miss   = -9999.0
#countrad = 300.0 # [km]
countrad = 1000.0 # [km]
#countrad = 1.0 # [km]
lthsst   = array([21,22,23,24,25]) + 273.15

ny     = 180
nx     = 360
thdura = 48
#--- init ------
a2one  = ones([ny,nx],float32)
#---------------
llkey  = [[expr,model,thsst] for expr in lexpr for model in lmodel for thsst in lthsst]
for expr, model, thsst in llkey:
  #----
  ens   = cmip_para.ret_ens(model, expr, "psl")
  sunit, scalendar = cmip_para.ret_unit_calendar(model,expr)
  iyear,eyear      = dyrange[expr]
  lyear            = range(iyear,eyear+1)
  #----

  dpgradrange   = ctrack_para.ret_dpgradrange()
  thpgrad        = dpgradrange[1][0] 
  #thsst    = tc_para.ret_thsst()
  thwind   = tc_para.ret_thwind()
  thrvort  = tc_para.ret_thrvort(model)
  thwcore  = tc_para.ret_thwcore(model)

 
  #** land sea mask -------------------
  landseadir      = "/media/disk2/data/JRA25/sa.one.anl_land/const/landsea"
  landseaname     = landseadir + "/landsea.sa.one"
  a2landsea       = fromfile(landseaname, float32).reshape(ny,nx)

  #-----------------------------------------
  a1dtime,a1tnum  = cmip_func.ret_times(iyear,eyear,lmon,sunit,scalendar,stepday,model=model)
  for year in lyear:
    for mon in lmon:
      #** init -------------------
      a2num    = zeros([ny,nx],float32)
      #-- load ----------
      sidir_root  = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/clist"%(model,expr)
      sidir       = sidir_root + "/%04d/%02d"%(year,mon)
      da1         = {}

      lstype  = ["rvort","dtlow","dtmid","dtup","wmeanlow","wmeanup","wmaxlow","dura","pgrad","sst","lat","lon","ipos","idate","nowpos","time","initsst"]
      for stype in lstype:
        siname        = sidir  + "/%s.%04d.%02d.bn"%(stype,year,mon)
        if stype in ["dura","ipos","idate","nowpos","time"]:
          da1[stype]  = fromfile(siname,   int32)
        else:
          da1[stype]  = fromfile(siname, float32)
      #-------------------
      stepflag = 0
      a2loc    = ones([ny,nx],float32)*miss
      nlist    = len(da1["rvort"])
      for i in range(nlist):
        rvort       = da1["rvort"][i]
        dtlow       = da1["dtlow"][i]
        dtmid       = da1["dtmid"][i]
        dtup        = da1["dtup" ][i]
        wmeanlow    = da1["wmeanlow" ][i]
        wmeanup     = da1["wmeanup"  ][i]
        wmaxlow     = da1["wmaxlow"  ][i]
        dura        = da1["dura"     ][i]
        pgrad       = da1["pgrad"    ][i]
        ipos        = da1["ipos"     ][i]
        nowpos      = da1["nowpos"   ][i]
        time        = da1["time"     ][i]
        initsst     = da1["initsst"  ][i]

        #---- check time ----
        ### This section should be prior to the condition filtering

        if (i == nlist-1):
          stepflag = 1
        else:
          timenext    = da1["time"][i+1]
          if (timenext != time):
            stepflag = 1

        #---- dura -------
        if dura < thdura:
          continue
        #print "dura"
        #---- rvort -------
        if abs(rvort) < thrvort:
          continue
        #print "rvort"
        #---- ipos: land or sea  -------
        iposx, iposy = ctrack_func.fortpos2pyxy( ipos, nx, -9999)
        if a2landsea[iposy, iposx] == 1.0:
          continue

        #print "landsea"
        #---- ipos: SST -----
        if initsst < thsst:
          continue

        #print "SST"
        #---- wmaxlow -----
        if wmaxlow < thwind:
          continue

        #print "max wind"
        #---- wmeanlow & wmeanup --
        if wmeanlow < wmeanup:
          continue
        #print "wind low < up"

        #---- warm core -----------
        if (dtlow + dtmid + dtup) < thwcore:
          continue
        print "warm core"

        #---- projection on the map --
        ix, iy       = ctrack_func.fortpos2pyxy( nowpos, nx, -9999)
        a2loc[iy,ix] = 1.0
        #print time,iy,ix

        #---- territory for each timestep --
        if stepflag == 1:
          a2terr    = ctrack_fsub.mk_territory_saone(a2loc.T, countrad*1000.0, miss, -89.5, 1.0, 1.0).T

          a2num_tmp = ma.masked_where(a2terr==miss, a2one).filled(0.0)
          a2num     = a2num + a2num_tmp
          #-- reset ---
          stepflag = 0
          a2loc    = ones([ny,nx],float32)*miss

      #-- output name ---
      sodir_root = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/tc/freq.%02dh.wc%4.2f.sst%02d.wind%02d.vor%.1e"%(model,expr,thdura,thwcore,thsst-273.15,thwind,thrvort)

      sodir      = sodir_root + "/%04d"%(year)
      ctrack_func.mk_dir(sodir)

      soname     = sodir + "/num.tc.rad%04dkm.%04d.%02d.sa.one"%(countrad,year,mon)
      a2num.tofile(soname)
      print "MAX",a2num.max()
      print soname




      #---------------------------
      #for dtime, tnum in map(None, a1dtime, a1tnum):
      #  yeart,mont,dayt,hourt = dtime.year, dtime.month, dtime.day, dtime.hour
      #  #--- check year and month ---
      #  if not (yeart==year)&(mont==mon):
      #    continue
      #  #----------------------------
      #  stime  = "%04d%02d%02d%02d00"%(yeart,mont,dayt,hourt)
      #  print "mk.freq.tc.obj.cmip","rad",model,countrad,yeart,mont,dayt,hourt

      #  #-- load -------
      #  tcdir  = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/tc/%02dh/%04d/%02d"%(model,expr,thdura,year,mon) 
      #
      #  tcname  = tcdir + "/tc.wc%4.2f.sst%02d.wind%02d.vor%.1e.%s.sa.one"%(thwcore, thsst-273.15, thwind, thrvort, stime)
      #
      #  a2tc      = fromfile(tcname, float32).reshape(180,360)
      #  #a2num_tmp = ma.masked_where(a2tc==miss, a2one).filled(0.0)
      #  a2num_tmp = ctrack_fsub.mk_territory_saone(a2tc.T, countrad*1000.0, miss, -89.5, 1.0, 1.0).T
      #  a2num_tmp = ma.masked_equal(a2num_tmp, miss).filled(0.0)
      #  a2num     = a2num + a2num_tmp
      #
      ##--- write -------
      #sodir_root  = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/tc/freq.%02dh"%(model,expr,thdura)
      #sodir       = sodir_root + "/%04d"%(year)
      #ctrack_func.mk_dir(sodir)
      #soname      = sodir + "/num.tc.wc%4.2f.sst%02d.wind%02d.vor%.1e.%s.rad%04dkm.%04d.%02d.sa.one"%(thwcore, thsst-273.15, thwind, thrvort,ens,countrad,year,mon)
      ##
      #a2num.tofile(soname)
      
      
      
      
