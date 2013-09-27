from numpy import *
import ctrack_para, ctrack_func
#-------------------------------------

lseason = ["ALL"]
lregion = ["ASAS"]
lftype  = [1,2,3,4]
iyear   = 2000
eyear   = 2010
lyear   = range(iyear,eyear+1)
lmon    = range(1,12+1)

idir_root = "/media/disk2/out/chart/ASAS/length.grids"
odir_root = idir_root

for region in lregion:
  for ftype in lftype:
    #--- init --------
    da1grids = {}
    for year in lyear:
      for mon in lmon:
        da1grids[year,mon] = []
    #-----------------
    for year in lyear:
      for mon in lmon:
        idir  = idir_root + "/%04d.%02d"%(year,mon)
        iname = idir + "/frontlen.grids.%04d.%02d.%s.f%s.bn"%(year,mon,region,ftype)
        da1grids[year,mon] = mean(fromfile(iname,float32))
    #---------------
    sout = ","+ ",".join(map(str,range(1,12+1))) + "\n"
    for year in lyear:
      lout_seg = [da1grids[year,mon] for mon in lmon]
      sout = sout + "%04d,"%(year) + ",".join(map(str, lout_seg)) + "\n"
    #---------------
    odir     = odir_root + "/csv"
    ctrack_func.mk_dir(odir)
    oname    = odir + "/frontlen.grids.%04d-%04d.%s.f%s.csv"%(iyear,eyear,region,ftype)
    #
    f = open(oname,"w"); f.write(sout); f.close()
    print oname
     
