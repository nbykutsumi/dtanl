from check_dtanl import *
from numpy import *
#***********************************************************
Psfc = 100000.0   # [Pa], not in [hPa]
Tsfc0   = 20 + 273.15
RHsfc0  = 20
RHsfc_t = 100
Psfc0   = 1000*100
Ptop    = 100*100
#-----
dT = 5.0
dRH = 20
dP = 1*100
dP_cal = 1.0
#------------------
sodir = "/home/utsumi/bin/dtanl/so/out"
soname_dqdp_rh = sodir + "/dqdp_rh.csv"
#------------------
Tsfc = Tsfc0
Psfc = Psfc0
ddqdp ={}
lRHsfc = range(RHsfc0, RHsfc_t +1,dRH)
lP = range(Psfc, Ptop-1, -dP)
#********************************************
for RHsfc in lRHsfc:
  qs   = check_dtanl.cal_qs(Tsfc, Psfc)
  qsfc = check_dtanl.cal_q(Tsfc, Psfc, RHsfc)
  Plcl = check_dtanl.lcl(Psfc, Tsfc, qsfc)
  #******************************************
  # from Surface to LCL
  #------------------------------------------
  for P in range(Psfc, int(Plcl)-1, -dP):
    ddqdp[RHsfc, P] = ""
    #print P, ddqdp[RHsfc, P]
  #******************************************
  # from Pscnd to Ptop
  #------------------------------------------
  Tlcl  = check_dtanl.t1tot2dry(Tsfc, Psfc, Plcl)
  Tprev = Tlcl
  Pprev = P
  Pscnd = P -dP
  for P in range(Pscnd, Ptop -1, -dP):
    T = check_dtanl.moistadiabat( Pprev, Tprev, P, dP_cal)
    ddqdp[RHsfc, P] = check_dtanl.cal_rdqdp(P, T, dP_cal) * 100 # output in [kg/kg/hPa], not in [kg/kg/Pa]
    dt_dp = check_dtanl.dt_dp_moist(P, T)
    #print P, T-273.15, ddqdp[RHsfc, P], dt_dp
    Tprev = T
    Pprev = P
  #******************************************
#********************************************
# make output data for dqdp & pressure height
#--------------------------------------------
sout = ""
sout = sout + "" + "," +",".join(map(str,lRHsfc)) + "\n"
for P in lP:
  sout_seg ="%s"%(P*0.01)
  for RHsfc in lRHsfc:
    sout_seg = sout_seg + ",%s"%(ddqdp[RHsfc, P])
  #-------------
  sout = sout + sout_seg + "\n"
#-----------------
sout = sout.strip()
#********************************************
# write to file
#--------------------------------------------
f = open(soname_dqdp_rh, "w")
f.write(sout)
f.close()
print soname_dqdp_rh
#********************************************
# make output data for dqdp & pressure (const T)
#--------------------------------------------
lT  = list(arange(273.15 -30, 273.15 +30 +1, 5))
lP = range(100*100, 1000*100 +1, 20*100)
#------
lT_deg = map(lambda x: x-273.15, lT)
sout = "" + "," + ",".join(map(str,lT_deg)) + "\n"
#****************************
for P in lP:
  sout_seg ="%s"%(P*0.01,)
  for T in lT:
    dqdp = check_dtanl.cal_rdqdp(P, T, dP_cal) *100   # output in [kg/kg/hPa], not in [kg/kg/Pa]
    sout_seg = sout_seg + ",%s"%(dqdp)
  #--------
  sout_seg = sout_seg + "\n"
  sout = sout + sout_seg
sout = sout.strip()
#****************************
# output file name
#----------------------------
sofile = sodir + "/dqdp_p.csv"
f = open( sofile, "w")
f.write(sout)
f.close()
print sofile
#############################
