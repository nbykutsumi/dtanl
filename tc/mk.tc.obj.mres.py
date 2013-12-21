from numpy import *
from ctrack_fsub import *
import calendar
import ctrack_para
import ctrack_func
import tc_para
#-----------------------------------------
#bnflag    = True
bnflag    = False

#singleday = True
singleday = False

iyear  = 1980
eyear  = 2012
lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon   = [7]
iday   = 1
lhour  = [0,6,12,18]
miss   = -9999.0

ny     = 180
nx     = 360
dpgradrange   = ctrack_para.ret_dpgradrange()
thpgrad        = dpgradrange[1][0] 
#thdura   = 72
thdura   = 48

#lmodel = ["anl_p","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel = ["anl_p"]

for model in lmodel:
  #thsst    = 273.15 + 25.0
  #thwind   = 0.0 #m/s 
  #thrvort  = 7.0e-5
  #thwcore  = 0.5  # (K)
  thsst    = tc_para.ret_thsst()
  thwind   = tc_para.ret_thwind()
  thrvort  = tc_para.ret_thrvort(model)
  thwcore  = tc_para.ret_thwcore(model)
  
  plev_low = 850*100.0 # (Pa)
  plev_mid = 500*100.0 # (Pa)
  plev_up  = 250*100.0 # (Pa)
  
  if bnflag == True:
    pgraddir_root   = "/media/disk2/out/JRA25/bn.sa.one.%s/6hr/pgrad"%(model)
    lifedir_root    = "/media/disk2/out/JRA25/bn.sa.one.%s/6hr/life"%(model)
    lastposdir_root = "/media/disk2/out/JRA25/bn.sa.one.%s/6hr/lastpos"%(model)
    iposdir_root    = "/media/disk2/out/JRA25/bn.sa.one.%s/6hr/ipos"%(model)
    nextposdir_root = "/media/disk2/out/JRA25/bn.sa.one.%s/6hr/nextpos"%(model)
  elif bnflag == False:
    pgraddir_root   = "/media/disk2/out/JRA25/sa.one.%s/6hr/pgrad"%(model)
    lifedir_root    = "/media/disk2/out/JRA25/sa.one.%s/6hr/life"%(model)
    lastposdir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/lastpos"%(model)
    iposdir_root    = "/media/disk2/out/JRA25/sa.one.%s/6hr/ipos"%(model)
    nextposdir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/nextpos"%(model)


  #
  tdir_root       = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP"%(model)
  udir_root       = "/media/disk2/data/JRA25/sa.one.%s/6hr/UGRD"%(model)
  vdir_root       = "/media/disk2/data/JRA25/sa.one.%s/6hr/VGRD"%(model)
  #
  sstdir_root     = "/media/disk2/data/JRA25/sa.one.anl_p25/mon/WTMPsfc"
  #
  if bnflag == True:
    sodir_root      = "/media/disk2/out/JRA25/bn.sa.one.%s/6hr/tc/%02dh"%(model,thdura)
  elif bnflag == False: 
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
      #-- init --
      sodir  = sodir_root + "/%04d/%02d"%(year,mon)
      ctrack_func.mk_dir(sodir)
      a2num  = zeros([ny,nx],float32).reshape(ny,nx)
      ##############
      #  SST
      #-------------
      sstdir   = sstdir_root + "/%04d"%(year)
      sstname  = sstdir + "/fcst_phy2m.WTMPsfc.%04d%02d.sa.one"%(year,mon)
      a2sst    = fromfile( sstname, float32).reshape(ny,nx)
      #-------------
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
          nextposdir      = nextposdir_root + "/%04d%02d"%(year, mon)
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
          a2nextpos       = fromfile(nextposname,  int32).reshape(ny, nx)
  
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
          tout            = ctrack_fsub.find_tc_saone(\
                            a2pgrad.T, a2life.T, a2lastpos.T, a2lastflag.T, a2tlow.T, a2tmid.T, a2tup.T, a2ulow.T, a2uup.T, a2vlow.T, a2vup.T, a2sst.T, a2landsea.T\
                          , thpgrad, thdura, thsst, thwind, thrvort, initflag, miss)
  
          tout_old        = ctrack_fsub.find_tc_saone_old(\
                            a2pgrad.T, a2life.T, a2lastpos.T, a2lastflag.T, a2tlow.T, a2tmid.T, a2tup.T, a2ulow.T, a2uup.T, a2vlow.T, a2vup.T, a2sst.T, a2landsea.T\
                          , thpgrad, thdura, thsst, thwind, thrvort, initflag, miss)
  
  
  
          #
          a2tcloc         = tout[0].T
          a2lastflag      = tout[1].T
          
          #---- save -----------------------
          soname   = sodir + "/tc.wc%4.2f.sst%02d.wind%02d.vor%.1e.%s.sa.one"%(thwcore, thsst-273.15, thwind, thrvort, stime)
          a2tcloc.tofile(soname)
          print soname
