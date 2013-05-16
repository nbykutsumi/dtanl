from numpy import *
from dtanl_fsub import *
import ctrack_func
import calendar
#*************************************************************
iyear      = 2004
eyear      = 2004
#lmon       = [1,2,3,4,5,6,7,8,9,10,11,12]
lmon       = [6,7]
iday       = 1
lhour      = [0,6,12,18]
#lplev      = array([925,850,700,500,300])*100.
lplev      = array([250])*100.

sresol     = "anl_p"
ny,nx      = 180,360

#-------------------------------------------------------------
odir_root  = "/media/disk2/out/JRA25/sa.one.anl_p/day"
for year in range(iyear, eyear+1):
  for mon in lmon:
    eday   = calendar.monthrange(year,mon)[1]
    for day in range(iday,eday+1):
      for plev in lplev:
        print year,mon,day, plev
        a2theta_e  = zeros([ny,nx],float32)
        for hour in lhour:
          #-- q: mixing ratio --------------------------
          qname = "/media/disk2/data/JRA25/sa.one.%s/6hr/SPFH/%04d%02d/%s.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,year, mon, sresol, plev*0.01, year, mon, day, hour)
          a2q   = fromfile(qname, float32).reshape(ny,nx)
          
          #-- t: ---------------------------------------
          tname = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP/%04d%02d/%s.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol, year, mon, sresol, plev*0.01, year, mon, day, hour)
          a2t   = fromfile(tname, float32).reshape(ny,nx)
          #--- thetae ----------------------------------
          #a2theta_e_tmp  = dtanl_fsub.mk_a2theta_e(plev, a2t.T, a2q.T).T
          a2theta_e_tmp  = dtanl_fsub.mk_a2theta_e(plev, a2t.T, a2q.T).T

          a2theta_e      = a2theta_e + a2theta_e_tmp
        #-----------------------------------------------
        a2theta_e   = a2theta_e / len(lhour)

        #--- save --------------------
        odir        = odir_root + "/theta_e/%04d%02d"%(year,mon)
        ctrack_func.mk_dir(odir)
        thetaename  = odir + "/%s.thetae.%04dhPa.%04d%02d%02d.sa.one"%(sresol, plev*0.01, year,mon,day)
        a2theta_e.tofile(thetaename)
        print thetaename         



