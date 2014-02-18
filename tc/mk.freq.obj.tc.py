from numpy import *
from ctrack_fsub import *
import calendar
import ctrack_para
import ctrack_func
import tc_para
#-----------------------------------------
#singleday = True
singleday = False
#iyear  = 1997
#eyear  = 2011
iyear  = 1980
eyear  = 2012
lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
iday   = 1
lhour  = [0,6,12,18]
miss   = -9999.0

ny     = 180
nx     = 360
#lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel = ["org"]
#countrad = 300.0 # (km)
#countrad = 1.0 # (km)
countrad = 1000.0 # (km)
#lthsst   = array([15.0,20.0,25.0,18.0,22.0]) + 273.15
lthsst   = array([20,21,23,24,25]) + 273.15
print lthsst
#-- init -------
a2one = ones([ny,nx],float32)
#---------------
for model in lmodel:
  for thsst in lthsst:
    print thsst
    thdura   = 48
    #thsst    = tc_para.ret_thsst()
    thwind   = tc_para.ret_thwind()
    thrvort  = tc_para.ret_thrvort(model)
    thwcore  = tc_para.ret_thwcore(model)
    #
    
    #** land sea mask -------------------
    landseadir      = "/media/disk2/data/JRA25/sa.one.anl_land/const/landsea"
    landseaname     = landseadir + "/landsea.sa.one"
    a2landsea       = fromfile(landseaname, float32).reshape(ny,nx)
    
    #-----------------------------------------
    for year in range(iyear,eyear+1):
      for mon in lmon:
        #----------
        if singleday == True:
          eday = iday
        else:
          eday = calendar.monthrange(year,mon)[1]
   
        #-- init --
        a2num  = zeros([ny,nx],float32)
        #-- load ----------
        sidir_root  = "/media/disk2/out/JRA25/sa.one.%s/6hr/clist"%(model)
        sidir       = sidir_root + "/%04d/%02d"%(year,mon)      
        da1         = {}
        
        lstype  = ["rvort","dtlow","dtmid","dtup","wmeanlow","wmeanup","wmaxlow","dura","pgrad","sst","lat","lon","ipos","idate","nowpos","time","initsst"]
        for stype in lstype:
          siname        = sidir  + "/%s.%04d.%02d.bn"%(stype,year,mon)
          if stype in ["dura","ipos","idate","nowpos","time"]:
            da1[stype]  = fromfile(siname,   int32)
          else:
            da1[stype]  = fromfile(siname, float32) 
        #----------
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
           
          #---- rvort -------
          if abs(rvort) < thrvort:
            continue 
  
          #---- ipos: land or sea  -------
          iposx, iposy = ctrack_func.fortpos2pyxy( ipos, nx, -9999)
          if a2landsea[iposy, iposx] == 1.0:
            continue
  
          #---- ipos: SST -----
          if initsst < thsst:
            continue
  
          #---- wmaxlow -----
          if wmaxlow < thwind:
            continue
  
          #---- wmeanlow & wmeanup --
          if wmeanlow < wmeanup:
            continue
  
          #---- worm core -----------
          if (dtlow + dtmid + dtup) < thwcore:
            continue
  
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
        print "AAA",thsst - 273.15
        sodir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/tc/freq.%02dh.wc%4.2f.sst%02d.wind%02d.vor%.1e"%(model,thdura,thwcore,thsst-273.15,thwind,thrvort)
        sodir      = sodir_root + "/%04d"%(year)
        ctrack_func.mk_dir(sodir)
  
        soname     = sodir + "/num.tc.rad%04dkm.%04d.%02d.sa.one"%(countrad,year,mon)
        a2num.tofile(soname)
        print soname
