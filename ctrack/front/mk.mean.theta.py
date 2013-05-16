from numpy import *
from dtanl_fsub import *
import calendar
import ctrack_func
import os
#---------------------------------------------------------
iyear  = 2000
eyear  = 2010
lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
iday   = 1
lhour  = [0,6,12,18]
lplev  = [925, 850, 700, 600, 500, 300, 250]
nx,ny  = 360,180
#----------------------------------------------------
tdir_root     = "/media/disk2/data/JRA25/sa.one/6hr/TMP"
qdir_root     = "/media/disk2/data/JRA25/sa.one/6hr/SPFH"
#----------------------------------------------------
for plev in lplev:
  itimes    = 0
  for year in range(iyear, eyear+1):
    for mon in lmon:
      #-- init --------------
      a2sum        = zeros([ny,nx],float32)
      #-----------------
      eday  = calendar.monthrange(year, mon)[1]
      #-----------------
      tdir      = tdir_root     + "/%04d%02d"%(year,mon)
      qdir      = qdir_root     + "/%04d%02d"%(year,mon)
      #-----------------
      for day in range(iday, eday+1):
        print plev,year,mon,day
        for hour in lhour:
          #-----------------
          itimes      = itimes + 1
          #-----------------
          tname     = tdir  + "/anl_p25.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev,year,mon,day,hour)
          qname     = qdir  + "/anl_p25.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev,year,mon,day,hour)
          a2t       = fromfile(tname,     float32).reshape(ny,nx)
          a2q       = fromfile(qname,     float32).reshape(ny,nx)
          a2sum     = a2sum + dtanl_fsub.mk_a2theta_e(plev*100., a2t.T, a2q.T).T
      #--- save ------------
      odir   = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d"%(year,mon)
      ctrack_func.mk_dir(odir)
      oname  = odir + "/sum.theta_e.%04dhPa.sa.one"%(plev)
      a2sum.tofile(oname)
      print oname

