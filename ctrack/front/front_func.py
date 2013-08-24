from numpy import *
from ctrack_fsub import *
from dtanl_fsub import *
import ctrack_para, front_para
##########################################
# FUNCTIONS
##########################################
def wrap_front_q_saone(year,mon,day,hour, miss=-9999.0):
  #-- para ---
  ny,nx      = 180,360
  thorog     = ctrack_para.ret_thorog()
  thgradorog = ctrack_para.ret_thgradorog()
  thgrids    = front_para.ret_thgrids()
  thfmask1t, thfmask2t, thfmask1q, thfmask2q   = front_para.ret_thfmasktq()
  #-- names ---
  orogname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
  gradname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/maxgrad.0200km.sa.one"
  iname1q    = "/media/disk2/out/JRA25/sa.one.anl_p/6hr/front.q/%04d%02d/front.q.M1.%04d.%02d.%02d.%02d.sa.one"%(year,mon,year,mon,day,hour)
  iname2q    = "/media/disk2/out/JRA25/sa.one.anl_p/6hr/front.q/%04d%02d/front.q.M2.%04d.%02d.%02d.%02d.sa.one"%(year,mon,year,mon,day,hour)

  #-- load ----
  a2orog     = fromfile(orogname, float32).reshape(ny,nx)
  a2gradorog = fromfile(gradname, float32).reshape(ny,nx)
  a2potq1    = fromfile(iname1q,float32).reshape(ny,nx)
  a2potq2    = fromfile(iname2q,float32).reshape(ny,nx)
  a2loct     = wrap_front_t_saone(year,mon,day,hour, miss=-9999.0)
  #-- make locq --
  a2locq     = complete_front_q_saone(a2loct, a2potq1, a2potq2, thfmask1q, thfmask2q, a2orog, a2gradorog, thorog, thgradorog, thgrids, miss)
  #
  return a2locq

##########################################
def wrap_front_t_saone(year,mon,day,hour, miss=-9999.0):
  #--
  ny,nx      = 180,360
  thorog     = ctrack_para.ret_thorog()
  thgradorog = ctrack_para.ret_thgradorog()
  thgrids    = front_para.ret_thgrids()
  thfmask1t, thfmask2t, thfmask1q, thfmask2q   = front_para.ret_thfmasktq()
  #
  orogname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
  gradname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/maxgrad.0200km.sa.one"
  a2orog     = fromfile(orogname, float32).reshape(ny,nx)
  a2gradorog = fromfile(gradname, float32).reshape(ny,nx)
  
  iname1t = "/media/disk2/out/JRA25/sa.one.anl_p/6hr/front.t/%04d%02d/front.t.M1.%04d.%02d.%02d.%02d.sa.one"%(year,mon,year,mon,day,hour)
  iname2t = "/media/disk2/out/JRA25/sa.one.anl_p/6hr/front.t/%04d%02d/front.t.M2.%04d.%02d.%02d.%02d.sa.one"%(year,mon,year,mon,day,hour)
  a2pott1 = fromfile(iname1t,float32).reshape(ny,nx)
  a2pott2 = fromfile(iname2t,float32).reshape(ny,nx)
  a2loct  = complete_front_t_saone(a2pott1, a2pott2, thfmask1t, thfmask2t, a2orog, a2gradorog, thorog, thgradorog, thgrids, miss )
  return a2loct
##########################################
def complete_front_q_saone(a2loct, a2potlocq1, a2potlocq2, thfmask1q, thfmask2q, a2orog, a2gradorog, thorog=1500.0, thgradorog=3.0*1.e-3, thgrids=5, miss=-9999.0):
  delwgtflag = 1
  #--
  a2terrt  = ctrack_fsub.mk_territory_deg_saone(a2loct.T, 2, miss).T
  #--
  a2locq    = ma.masked_where(a2potlocq1 < thfmask1q, a2potlocq1)
  a2locq    = ma.masked_where(a2potlocq2 < thfmask2q, a2locq)
  a2locq    = ma.masked_where(a2orog > thorog, a2locq).filled(miss)
  a2locq    = ma.masked_where(a2gradorog > thgradorog, a2locq).filled(miss)

  a2locq  = ma.masked_where(a2terrt==1.0, a2locq).filled(miss)

  a2locq    = dtanl_fsub.fill_front_gap(a2locq.T, miss).T
  a2locq   = dtanl_fsub.del_front_lesseq_ngrids(a2locq.T, delwgtflag, miss, thgrids).T
  return a2locq

##########################################
def complete_front_t_saone(a2potloct1, a2potloct2, thfmask1t, thfmask2t, a2orog, a2gradorog, thorog=1500.0, thgradorog=3.0*1.e-3, thgrids=5, miss=-9999.0):
  #
  delwgtflag = 1
  a2loc    = ma.masked_where(a2potloct1 < thfmask1t, a2potloct1)
  a2loc    = ma.masked_where(a2potloct2 < thfmask2t, a2loc)
  a2loc    = ma.masked_where(a2orog > thorog, a2loc).filled(miss)
  a2loc    = ma.masked_where(a2gradorog > thgradorog, a2loc).filled(miss)
  a2loc    = dtanl_fsub.fill_front_gap(a2loc.T, miss).T
  a2loc    = dtanl_fsub.del_front_lesseq_ngrids(a2loc.T, delwgtflag, miss, thgrids).T
  return a2loc 

##########################################
def mk_a2chart_gradtv_highside_saone(sresol, year, mon,day, hour):
  stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)
  plev    = 850*100.
  nx,ny   = 360,180
  miss_out= -9999.
  highsidedist  = ctrack_para.ret_highsidedist()
  #-- chart front loc --------------------------
  frontname = "/media/disk2/out/chart/ASAS/front/%04d%02d/front.ASAS.%04d.%02d.%02d.%02d.saone"%(year,mon,year,mon,day,hour)
  a2loc     = fromfile(frontname, float32).reshape(ny,nx)
  #-- q: mixing ratio --------------------------
  qname = "/media/disk2/data/JRA25/sa.one.%s/6hr/SPFH/%04d%02d/anl_p.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol, year, mon, plev*0.01, year, mon, day, hour)
  a2q   = fromfile(qname, float32).reshape(ny,nx)

  #-- t: ---------------------------------------
  tname = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP/%04d%02d/anl_p.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol, year, mon, plev*0.01, year, mon, day, hour)
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

##########################################




