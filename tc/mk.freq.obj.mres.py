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
eyear  = 1999
lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon   = [8]
iday   = 1
lhour  = [0,6,12,18]
miss   = -9999.0

ny     = 180
nx     = 360
#lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel = ["org"]
#countrad = 300.0 # (km)
countrad = 1.0 # (km)

#-- init -------
a2one = ones([ny,nx],float32)
#---------------
for model in lmodel:
  thdura   = 48
  thsst    = tc_para.ret_thsst()
  thwind   = tc_para.ret_thwind()
  thrvort  = tc_para.ret_thrvort(model)
  thwcore  = tc_para.ret_thwcore(model)
  #
  sodir_root      = "/media/disk2/out/JRA25/sa.one.%s/6hr/tc/freq.%02dh"%(model,thdura)
  
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
      sodir  = sodir_root + "/%04d"%(year)
      ctrack_func.mk_dir(sodir)
      a2num  = zeros([ny,nx],float32).reshape(ny,nx)
      #----------
      for day in range(iday, eday+1):
        print year, mon, day
        for hour in lhour:
          sidir  = "/media/disk2/out/JRA25/sa.one.%s/6hr/tc/%02dh/%04d/%02d"%(model,thdura,year,mon)
          stime  = "%04d%02d%02d%02d"%(year, mon, day, hour)
          iname  = sidir + "/tc.wc%4.2f.sst%02d.wind%02d.vor%.1e.%s.sa.one"%(thwcore, thsst-273.15, thwind, thrvort, stime)

          a2tc   = fromfile(iname,float32).reshape(ny,nx)
          a2terr = ctrack_fsub.mk_territory_saone(a2tc.T, countrad*1000.0, miss, -89.5, 1.0, 1.0).T
          a2num_tmp = ma.masked_where(a2terr==miss, a2one).filled(0.0)
          a2num     = a2num + a2num_tmp

      #--- write to file --    
      soname     = sodir + "/num.tc.%s.%02dh.w%3.1f.sst%d.wind%d.vor%.1e.rad%04dkm.%04d.%02d.sa.one"%(model,thdura, thwcore,thsst-273.15, thwind, thrvort,countrad,year,mon)
      a2num.tofile(soname)
      print soname
