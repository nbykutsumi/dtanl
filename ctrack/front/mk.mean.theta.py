from numpy import *
from dtanl_fsub import *
import calendar
import ctrack_func
import os
#---------------------------------------------------------
iyear  = 2001
eyear  = 2010
lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
iday   = 1
lhour  = [0,6,12,18]
lplev  = [850]
#lplev  = [925]
nx,ny  = 360,180
sresol = "anl_p"
#----------------------------------------------------
tdir_root     = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP"%(sresol)
qdir_root     = "/media/disk2/data/JRA25/sa.one.%s/6hr/SPFH"%(sresol)
#----------------------------------------------------
for plev in lplev:
  for year in range(iyear, eyear+1):
    for mon in lmon:
      #-- init --------------
      a2theta   = zeros([ny,nx],float32)
      a2theta_e = zeros([ny,nx],float32)
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
          tname     = tdir  + "/%s.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,plev,year,mon,day,hour)
          qname     = qdir  + "/%s.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,plev,year,mon,day,hour)
          a2t       = fromfile(tname,     float32).reshape(ny,nx)
          a2q       = fromfile(qname,     float32).reshape(ny,nx)
          a2theta_tmp   = dtanl_fsub.mk_a2theta(plev*100.0, a2t.T).T
          a2theta_e_tmp = dtanl_fsub.mk_a2theta_e(plev*100., a2t.T, a2q.T).T
          a2theta   = a2theta   + a2theta_tmp 
          a2theta_e = a2theta_e + a2theta_e_tmp
      #--- save ------------
      odir   = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d"%(year,mon)
      ctrack_func.mk_dir(odir)
      theta_name    = odir + "/sum.theta.%04dhPa.sa.one"%(plev)
      theta_e_name  = odir + "/sum.theta_e.%04dhPa.sa.one"%(plev)
      a2theta.tofile(theta_name)
      a2theta_e.tofile(theta_e_name)
      print a2theta.max()
      print theta_name

