from numpy import *
import calendar
import os


iyear = 2000
eyear = 2004
tstp  = "6hr"
ny    = 180
nx    = 360
imon  = 1
emon  = 12

var        = "PRMSL"
dtype  = {}
dtype["PRMSL"] = "fcst_phy2m"

idir_root  =  "/media/disk2/data/JRA25/sa.one/%s/%s"%(tstp, var)
odir_root  =  "/media/disk2/data/JRA25/sa.one/my.mean"


#********************************************
def mk_dir(sdir):
  if not os.access(sdir , os.F_OK):
    os.mkdir(sdir)
#********************************************
stype  = dtype[var]

odir       = odir_root + "/%s"%(var)
mk_dir(odir)
#-- initialize  -----------------------------
da2mean = {}
for mon in range(0, 12+1):
  da2mean[mon] = zeros([ny, nx], float32)
#--------------------------------------------
dtimes  = {}
for mon in range(0, 12+1):
  dtimes[mon] = 0
#--------------------------------------------
for year in range(iyear, eyear + 1):
  for mon in range(imon, emon + 1):
    idir    =  idir_root + "/%04d%02d"%(year, mon)
    ##-- no leap ------
    #if (mon ==2):
    #  eday = 28
    #else:
    #  eday  = calendar.monthrange(year, mon)[1]

    eday  = calendar.monthrange(year, mon)[1]
    #-----------------
    for day in range(1, eday+1):
      print year, mon, day
      for hour in [0, 6, 12, 18]:
        dtimes[0]     = dtimes[0] + 1
        dtimes[mon]   = dtimes[mon] + 1

        stime         = "%04d%02d%02d%02d"%(year, mon, day, hour)
        iname         =  idir + "/fcst_phy2m.PRMSL.2000013118.sa.one"
        iname         =  idir + "/%s.%s.%s.sa.one"%(stype, var, stime)
        a2in          = fromfile( iname , float32).reshape(ny, nx)
        da2mean[mon]  = da2mean[mon] + a2in
        da2mean[0]    = da2mean[0]   + a2in
#------------------------------
#for mon in range(0, 12+1):
for mon in [0,1,2]:
  da2mean[mon] = da2mean[mon] / dtimes[mon]
  soname       = odir + "/%s.%s.0000%02d0000.sa.one"%(stype, var, mon)
  da2mean[mon].tofile(soname)
  print soname

#------------------------------

