from numpy import *
from ctrack_fsub import *
import calendar
import ctrack_para
import ctrack_func
#-----------------------------------------
#singleday = True
singleday = False
iyear  = 2000
eyear  = 2004
lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon   = [1]
iday   = 1
lhour  = [0,6,12,18]
miss   = -9999.0

ny     = 180
nx     = 360

dpgradrange   = ctrack_para.ret_dpgradrange()
thpgrad        = dpgradrange[1][0] 
thdura   = 36
thsst    = 273.15 + 25.0
thwind   = 0.0 #m/s 
thrvort  = 7.0e-5
thwcore  = 0.5  # (K)

plev_low = 850*100.0 # (Pa)
plev_mid = 500*100.0 # (Pa)
plev_up  = 250*100.0 # (Pa)

psldir_root     = "/media/disk2/data/JRA25/sa.one/6hr/PRMSL"
pgraddir_root   = "/media/disk2/out/JRA25/sa.one/6hr/pgrad"
lifedir_root    = "/media/disk2/out/JRA25/sa.one/6hr/life"
lastposdir_root = "/media/disk2/out/JRA25/sa.one/6hr/lastpos"
iposdir_root    = "/media/disk2/out/JRA25/sa.one/6hr/ipos"
nextposdir_root = "/media/disk2/out/JRA25/sa.one/6hr/nextpos"
#
tdir_root       = "/media/disk2/data/JRA25/sa.one/6hr/TMP"
udir_root       = "/media/disk2/data/JRA25/sa.one/6hr/UGRD"
vdir_root       = "/media/disk2/data/JRA25/sa.one/6hr/VGRD"
#
sstdir_root     = "/media/disk2/data/JRA25/sa.one/mon/WTMPsfc"
#
sodir_root      = "/media/disk2/out/JRA25/sa.one/6hr/tc/%02dh"%(thdura)
#sodir_root      = "/media/disk2/out/JRA25/sa.one/6hr/tc"

#** land sea mask -------------------
landseadir      = "/media/disk2/data/JRA25/sa.one/const/landsea"
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
        nextposname     = nextposdir + "/nextpos.%s.sa.one"%(stime
        tlowname        = tdir       + "/anal_p25.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_low*0.01, year, mon, day, hour)
        tmidname        = tdir       + "/anal_p25.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_mid*0.01, year, mon, day, hour)
        tupname         = tdir       + "/anal_p25.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_up *0.01, year, mon, day, hour)
        ulowname        = udir       + "/anal_p25.UGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_low*0.01, year, mon, day, hour)
        uupname         = udir       + "/anal_p25.UGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_up *0.01, year, mon, day, hour)
        vlowname        = vdir       + "/anal_p25.VGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_low*0.01, year, mon, day, hour)
        vupname         = vdir       + "/anal_p25.VGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_up *0.01, year, mon, day, hour)
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

        #
        a2tcloc         = tout[0].T
        a2lastflag      = tout[1].T
        #
        #---- save -----------------------
        soname   = sodir + "/tc.wc%3.1f.sst%02d.wind%02d.vor%.1e.%s.saone"%(thwcore, thsst-273.15, thwind, thrvort, stime)
        a2tcloc.tofile(soname)
        print soname
