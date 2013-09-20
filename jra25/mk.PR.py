from numpy import *
import os
import calendar
import shutil

iyear = 2010
eyear = 2011
imon  = 1
emon  = 12
tstp  = "6hr"

idir_root = "/media/disk2/data/JRA25/sa.one/%s"%(tstp)

#********************************************
def mk_dir(sdir):
  if not os.access(sdir , os.F_OK):
    os.mkdir(sdir)
#********************************************

for year in range(iyear, eyear+1):
  for mon in range(imon, emon+1):
    idir_C  = "/media/disk2/data/JRA25/sa.one.fcst_phy2m/6hr/ACPCP/%04d%02d"%(year, mon)
    idir_L  = "/media/disk2/data/JRA25/sa.one.fcst_phy2m/6hr/NCPCP/%04d%02d"%(year, mon)
    odir    = "/media/disk2/data/JRA25/sa.one.fcst_phy2m/6hr/PR/%04d%02d"%(year, mon)
    mk_dir(odir)    
    #-- lat lon files ---
    shutil.copyfile(idir_C + "/dims.txt", odir + "/dims.txt")
    shutil.copyfile(idir_C + "/lat.txt", odir + "/lat.txt")
    shutil.copyfile(idir_C + "/lon.txt", odir + "/lon.txt")
    #
    sout  = "Convective precipitation + Largescale precipitaion\n"
    sout  = sout + "unit: (kg m-2 s-1)\n"
    f = open(odir + "/readme.txt", "w")
    f.write(sout)
    f.close()

    eday  = calendar.monthrange(year, mon)[1]
    #-----------------
    for day in range(1, eday+1):
      for hour in [0, 6, 12, 18]:
        
        #-- name ----
        siname_C = idir_C  + "/fcst_phy2m.ACPCP.%04d%02d%02d%02d.sa.one"%(year, mon, day, hour)
        siname_L = idir_L  + "/fcst_phy2m.NCPCP.%04d%02d%02d%02d.sa.one"%(year, mon, day, hour)
        soname_PR= odir    + "/fcst_phy2m.PR.%04d%02d%02d%02d.sa.one"%(year, mon, day, hour)

        #------------
        a2C   = fromfile(siname_C, float32)
        a2L   = fromfile(siname_L, float32)
        a2PR  = a2C + a2L
        a2PR.tofile(soname_PR)
        print soname_PR

