from numpy import *
from ctrack_fsub import *
import calendar
import ctrack_para
import ctrack_func
#-----------------------------------------
singleday = True
iyear  = 2004
eyear  = 2004
lmon   = [8]
iday   = 17
lhour  = [0,6,12,18]
miss   = -9999.0

ny     = 180
nx     = 360

dpgradrange   = ctrack_para.ret_dpgradrange()
thpgrad        = dpgradrange[1][0] 
thdura   = 48
thwind   = 15 #m/s 
thrvort  = 3.5e-5
thwcore  = 1.5  # (K)

#thdura   = -9999.0
#thwind   = -9999.0 #m/s 
#thrvort  = -9999.0
#thwcore  = -9999.0  # (K)


plev_low = 850*100.0 # (Pa)
plev_mid = 500*100.0 # (Pa)
plev_up  = 250*100.0 # (Pa)

psldir_root     = "/media/disk2/data/JRA25/sa.one/6hr/PRMSL"
pgraddir_root   = "/media/disk2/out/JRA25/sa.one/6hr/pgrad"
lifedir_root    = "/media/disk2/out/JRA25/sa.one/6hr/life"
nextposdir_root = "/media/disk2/out/JRA25/sa.one/6hr/nextpos"
#
tdir_root       = "/media/disk2/data/JRA25/sa.one/6hr/TMP"
udir_root       = "/media/disk2/data/JRA25/sa.one/6hr/UGRD"
vdir_root       = "/media/disk2/data/JRA25/sa.one/6hr/VGRD"

#-----------------------------------------
for year in range(iyear,eyear+1):
  for mon in lmon:
    #----------
    if singleday == True:
      eday = iday
    else:
      eday = calendar.monthrange(year,mon)[1]
    #----------
    for day in range(iday, eday+1):
      print year, mon, day
      for hour in lhour:
        stime  = "%04d%02d%02d%02d"%(year, mon, day, hour)
        #
        pgraddir        = pgraddir_root   + "/%04d%02d"%(year, mon)
        lifedir         = lifedir_root    + "/%04d%02d"%(year, mon)
        tdir            = tdir_root       + "/%04d%02d"%(year, mon)
        udir            = udir_root       + "/%04d%02d"%(year, mon)
        vdir            = vdir_root       + "/%04d%02d"%(year, mon)
        #
        pgradname       = pgraddir   + "/pgrad.%s.sa.one"%(stime)
        lifename        = lifedir    + "/life.%s.sa.one"%(stime)
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
        a2tlow          = fromfile(tlowname,  float32).reshape(ny, nx)
        a2tmid          = fromfile(tmidname,  float32).reshape(ny, nx)
        a2tup           = fromfile(tupname,   float32).reshape(ny, nx)
        a2ulow          = fromfile(ulowname,  float32).reshape(ny, nx)
        a2uup           = fromfile(uupname,   float32).reshape(ny, nx)
        a2vlow          = fromfile(vlowname,  float32).reshape(ny, nx)
        a2vup           = fromfile(vupname,   float32).reshape(ny, nx)
        #--------------------------------


        a2tcloc         = ctrack_fsub.find_tc_saone(\
                          a2pgrad.T, a2life.T, a2tlow.T, a2tmid.T, a2tup.T, a2ulow.T, a2uup.T, a2vlow.T, a2vup.T\
                        , thpgrad, thdura, thwind, thrvort, thwcore, miss).T

      
