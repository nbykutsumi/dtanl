from numpy import *
from ctrack_fsub import *
from dtanl_fsub import *
import ctrack_para
##########################################
# FUNCTIONS
##########################################
def mk_a2chart_gradtv_highside_saone(year, mon,day, hour):
  stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)
  plev    = 850*100.
  nx,ny   = 360,180
  miss_out= -9999.
  highsidedist  = ctrack_para.ret_highsidedist()
  #-- chart front loc --------------------------
  frontname = "/media/disk2/out/chart/ASAS/front/%04d%02d/front.ASAS.%04d.%02d.%02d.%02d.saone"%(year,mon,year,mon,day,hour)
  a2loc     = fromfile(frontname, float32).reshape(ny,nx)
  #-- q: mixing ratio --------------------------
  qname = "/media/disk2/data/JRA25/sa.one/6hr/SPFH/%04d%02d/anal_p25.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
  a2q   = fromfile(qname, float32).reshape(ny,nx)

  #-- t: ---------------------------------------
  tname = "/media/disk2/data/JRA25/sa.one/6hr/TMP/%04d%02d/anal_p25.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
  a2t   = fromfile(tname, float32).reshape(ny,nx)

  #-- tv: --------------------------------------
  a2tv  = a2t * (1.0+0.61*a2q)

  #-- a2gradtv ---------------------------------
  a2gradtv  = dtanl_fsub.mk_a2grad_abs_saone(a2tv.T).T

  #-- theta_e -----------------------------------
  a2theta_e = dtanl_fsub.mk_a2theta_e(plev, a2t.T, a2q.T).T
  #-- grad.theta_e ------------------------------------
  a2thermo         = a2theta_e
  a2gradtheta_e    = dtanl_fsub.mk_a2grad_abs_saone(a2thermo.T).T
  a2out            = ctrack_fsub.find_highsidevalue_saone(a2gradtheta_e.T, a2loc.T, a2gradtv.T, highsidedist, miss_out).T
  return  a2out

