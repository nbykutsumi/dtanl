from numpy import *
from ctrack_fsub import *
import calendar
import ctrack_para
import ctrack_func
import tc_para
#-----------------------------------------
#singleday = True
singleday = False
iyear  = 2004
eyear  = 2004
lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon   = [8]
iday   = 1
lhour  = [0,6,12,18]
miss   = -9999.0

ny     = 180
nx     = 360
lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]

for model in lmodel:
  dpgradrange   = ctrack_para.ret_dpgradrange()
  thpgrad        = dpgradrange[1][0] 
  thdura   = 36
  thsst    = tc_para.ret_thsst()
  thwind   = tc_para.ret_thwind()
  thrvort  = tc_para.ret_thrvort(model)
  thwcore  = tc_para.ret_thwcore(model)
  
  plev_low = 850*100.0 # (Pa)
  plev_mid = 500*100.0 # (Pa)
  plev_up  = 250*100.0 # (Pa)
  
  psldir_root     = "/media/disk2/data/JRA25/sa.one.%s/6hr/PRMSL"%(model)
  pgraddir_root   = "/media/disk2/out/JRA25/sa.one.%s/6hr/pgrad"%(model)
  lifedir_root    = "/media/disk2/out/JRA25/sa.one.%s/6hr/life"%(model)
  nextposdir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/nextpos"%(model)
  lastposdir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/lastpos"%(model)
  iposdir_root    = "/media/disk2/out/JRA25/sa.one.%s/6hr/ipos"%(model)
  #
  tdir_root       = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP"%(model)
  udir_root       = "/media/disk2/data/JRA25/sa.one.%s/6hr/UGRD"%(model)
  vdir_root       = "/media/disk2/data/JRA25/sa.one.%s/6hr/VGRD"%(model)
  #
  sstdir_root     = "/media/disk2/data/JRA25/sa.one.anl_p25/mon/WTMPsfc"
  #
  sodir_root      = "/media/disk2/out/JRA25/sa.one.%s/6hr/tc/%02dh"%(model,thdura)
  
  #** land sea mask -------------------
  landseadir      = "/media/disk2/data/JRA25/sa.one.anl_land/const/landsea"
  landseaname     = landseadir + "/landsea.sa.one"
  a2landsea       = fromfile(landseaname, float32).reshape(ny,nx)
  
  #-----------------------------------------
  a2lastflag      = ones([ny,nx], float32)*miss
  initflag        = -1
  #-----------------------------------------
  for year in range(iyear,eyear+1):
    for mon in lmon:
      #----------
      if singleday == True:
        eday = iday
      else:
        eday = calendar.monthrange(year,mon)[1]
      #**********
      # SST
      #----------
      sstdir   = sstdir_root + "/%04d"%(year)
      sstname  = sstdir + "/fcst_phy2m.WTMPsfc.%04d%02d.sa.one"%(year,mon)
      a2sst    = fromfile( sstname, float32).reshape(ny,nx)
  
      #-- init --
      sodir  = sodir_root + "/%04d/%02d"%(year,mon)
      ctrack_func.mk_dir(sodir)
      a2num  = zeros([ny,nx],float32).reshape(ny,nx)
      #----------
      for day in range(iday, eday+1):
        print year, mon, day
        for hour in lhour:
          initflag        = initflag + 1
          stime  = "%04d%02d%02d%02d"%(year, mon, day, hour)
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
          pgradname       = pgraddir   + "/pgrad.%s.sa.one"%(stime)
          lifename        = lifedir    + "/life.%s.sa.one"%(stime)
          iposname        = iposdir    + "/ipos.%s.sa.one"%(stime)
          lastposname     = lastposdir + "/lastpos.%s.sa.one"%(stime)
          nextposname     = nextposdir + "/nextpos.%s.sa.one"%(stime)
          tlowname        = tdir       + "/anl_p.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_low*0.01, year, mon, day, hour)
          tmidname        = tdir       + "/anl_p.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_mid*0.01, year, mon, day, hour)
          tupname         = tdir       + "/anl_p.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_up *0.01, year, mon, day, hour)
          ulowname        = udir       + "/anl_p.UGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_low*0.01, year, mon, day, hour)
          uupname         = udir       + "/anl_p.UGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_up *0.01, year, mon, day, hour)
          vlowname        = vdir       + "/anl_p.VGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_low*0.01, year, mon, day, hour)
          vupname         = vdir       + "/anl_p.VGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_up *0.01, year, mon, day, hour)
          #
          a2pgrad         = fromfile(pgradname, float32).reshape(ny, nx)
          a2life          = fromfile(lifename,  int32).reshape(ny, nx)
          a2ipos          = fromfile(iposname,  int32).reshape(ny, nx)
          a2lastpos       = fromfile(lastposname,int32).reshape(ny, nx)
          a2tlow          = fromfile(tlowname,  float32).reshape(ny, nx)
          a2tmid          = fromfile(tmidname,  float32).reshape(ny, nx)
          a2tup           = fromfile(tupname,   float32).reshape(ny, nx)
          a2ulow          = fromfile(ulowname,  float32).reshape(ny, nx)
          a2uup           = fromfile(uupname,   float32).reshape(ny, nx)
          a2vlow          = fromfile(vlowname,  float32).reshape(ny, nx)
          a2vup           = fromfile(vupname,   float32).reshape(ny, nx)
          #--------------------------------
          #tout            = ctrack_fsub.find_tc_saone(\
          #                  a2pgrad.T, a2life.T, a2lastpos.T, a2lastflag.T, a2tlow.T, a2tmid.T, a2tup.T, a2ulow.T, a2uup.T, a2vlow.T, a2vup.T, a2landsea.T\
          #                , thpgrad, thdura, thlat, thwind, thrvort, initflag, miss)
          ##
          tout            = ctrack_fsub.find_tc_saone(\
                            a2pgrad.T, a2life.T, a2lastpos.T, a2lastflag.T, a2tlow.T, a2tmid.T, a2tup.T, a2ulow.T, a2uup.T, a2vlow.T, a2vup.T, a2sst.T, a2landsea.T\
                          , thpgrad, thdura, thsst, thwind, thrvort, initflag, miss)
          #
          a2tcloc         = tout[0].T
          a2lastflag      = tout[1].T
          #
          a2tcloc  = ma.masked_less(a2tcloc, thwcore).filled(miss)
          a2tcloc  = ma.masked_not_equal(a2tcloc, miss).filled(1.0)
          a2tcloc  = ma.masked_equal(a2tcloc, miss).filled(0.0)
          #
          #---------------------------------
          a2num   = a2num + a2tcloc
      #--- num -> freq ----
      totalnum   = ctrack_para.ret_totaldays(year, year, mon) * len(lhour)
      a2freq     = a2num / totalnum
      #--- write to file --    
      soname     = sodir + "/freq.tc.%02dh.w%3.1f.sst%d.wind%d.vor%.1e.sa.one"%(thdura, thwcore,thsst-273.15, thwind, thrvort)
      a2freq.tofile(soname)
      print soname
