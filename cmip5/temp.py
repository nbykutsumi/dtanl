from dtanl_cmip_sbs import *
from numpy import *
dP_cal = 100.0
rPsfc = 980.0 *100.0
rTsfc = 273.15
rPlcl = 990.0 *100.0

r1lev_c = array([1000.0, 900.0, 800.0])*100.0
r1T_c   = [280.0,  270.0, 250.0]
r1lev_f = array([1000.0, 950.0, 900.0, 850.0, 800.0])*100.0
out = dtanl_cmip_sbs.dqdp_profile_epl(rPlcl, rPsfc, rTsfc, r1lev_c, r1lev_f, r1T_c)
print out

dqdp_sfc = dtanl_cmip_sbs.cal_rdqdp(rPsfc, rTsfc, dP_cal)
print dqdp_sfc

dqdp900 = dtanl_cmip_sbs.cal_rdqdp(900.0*100, 270.0, dP_cal)
print dqdp900

dqdp800 = dtanl_cmip_sbs.cal_rdqdp(800.0*100, 250.0, dP_cal)
print dqdp800

rTlcl = dtanl_cmip_sbs.t1tot2dry(rTsfc, rPsfc, rPlcl)
dqdp_lcl = dtanl_cmip_sbs.cal_rdqdp(rPlcl, rTlcl, dP_cal)
print "Plcl=", rPlcl
print "Pnext=",900.0*100.0
print "dqdp_lcl=", dqdp_lcl
print "dqdp900=", dqdp900
