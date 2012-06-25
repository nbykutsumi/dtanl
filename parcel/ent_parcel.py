from ent_parcel import *
from numpy import *
import matplotlib.pyplot as plt
import sys
#----------------------------
# functions
#****************************
def q2rmix(q):
  return  q / (1.0 - q)
#----------------------------
def rmix2q(rmix):
  return rmix / (1.0 + rmix)
#----------------------------
def cal_Tv(T, rmix):
  return T * (1.0 + 0.61 * rmix) 
#----------------------------
def interpolate(yb, yu, xb, xu, x):
  return (yu - yb)/(xu - xb) * (x - xb) + yb
#----------------------------
def theta2T(P, theta):
  Rd_Cp   = 0.28571
  P0      = 1000.0*100
  return theta * (P / P0)**Rd_Cp
#----------------------------
def cal_rmix(P, T, RH):
  epsi    = 0.62185
  es      = ent_parcel.cal_es(T)
  e       = es * RH
  rmix    = epsi * e / (P - e )
  return rmix
#----------------------------

#****************************
c_d       = 1004.0
c_m       = 1952.0
#----------------------------
lenttype    = [0.000, 0.001, 0.005]
#lenttype    = [0.001]
dentrate    = {0.000:0.000, 0.001:0.001, 0.005:0.005}
lRHtype     = [60, 80]
miss      = -9999
dP        = 10.0*100
Pend      = 100.0*100
#-- parcel -------
#T0        = 273.16 + 21.0
RH0       = 1.0
m         = 1.0  # [kg]
mliq0     = 0.0  # [kg]
#md0       = 0.990879685  # [kg]
#mm0       = 0.0090  # [kg]

for enttype in lenttype:
  for RHtype in lRHtype:
    #****************************
    # filenames
    #----------------------------
    odir     = "/home/utsumi/bin/dtanl/parcel"
    profname = odir + "/env_profile_RH%02d.csv"%(RHtype)
    oname    = "/home/utsumi/bin/dtanl/parcel/parcel_out.e%s.RH%s.csv"%(enttype, RHtype)
    
    #****************************
    # read environmental profile
    #----------------------------
    f = open(profname, "r")
    lprof = f.readlines()
    f.close()
    lP     = []
    ltheta = []
    lRHe   = []
    for line in lprof[1:]:
      line = map(float, line.strip().split(","))
      lP.append(line[0]*100.0)
      ltheta.append(line[1])
      lRHe.append(line[2])
    #****************************
    # Level range
    #----------------------------
    P0        = lP[0]
    P1        = P0
    #****************************
    # calc initial value
    #----------------------------
    theta0    = ltheta[0] + 1.0
    T0        = theta2T(P0, theta0)
    rmix0     = cal_rmix(P0, T0, RH0)
    q0        = rmix2q(rmix0)
    mm0       = m * q0
    md0       = m - mm0

    #----------------------------
    # make tracer array
    #----------------------------
    nlev  = ( P0 - Pend )/ dP
    if (nlev > int(nlev)):
      nlev = int(nlev) + 1
    else:
      nlev = int(nlev)
    #----------------------------
    # initial parcel values
    #----------------------------
    P                = P0
    T_new            = T0
    mliq_new         = mliq0
    mm_new           = mm0
    md_new           = md0
    #
    amm_new     = zeros(nlev)
    amliq_new   = zeros(nlev)
    #
    amm_new[0]    = mm_new
    amliq_new[0]  = mliq_new
    #----------------------------
    # make tracer array
    #----------------------------
    ammij    = zeros(nlev*nlev).reshape(nlev, nlev)
    amliqij  = zeros(nlev*nlev).reshape(nlev, nlev)
    amcondij = zeros(nlev*nlev).reshape(nlev, nlev)
    #----------------------------
    i     = -1
    k     = 0
    lout  = []
    while (-P1 < -Pend):
      i = i + 1
      print P1*0.01
      #--------------------------
      # renew the variables
      #--------------------------
      T1          = T_new
      mliq        = mliq_new
      mm1         = mm_new
      md1         = md_new
      ammij[i]    = amm_new
      amliqij[i]  = amliq_new
      #
      #--------------------------
      # environmental value
      #--------------------------
      if (-lP[k+1] <= -P1):
        k = k+1
      #
      thetae_b   = ltheta[k]
      thetae_u   = ltheta[k+1]
      P_b        = lP[k]
      P_u        = lP[k+1]
      RHe_b      = lRHe[k]
      RHe_u      = lRHe[k+1]
      #
      thetae     = interpolate(thetae_b, thetae_u, P_b, P_u, P1)
      RHe        = interpolate(RHe_b, RHe_u, P_b, P_u, P1)
      #
      Te         = theta2T(P1, thetae)
      rmixe      = cal_rmix(P1, Te, RHe) 
      #--------------------------
      Lv        = ent_parcel.cal_latentheat(T1) 
      #----------------------------
      # mix with environment
      #----------------------------
      if isinstance(enttype, str):
        sys.exit()
      else:
        entrate = dentrate[enttype]
      #--
      m1               = mm1 + md1
      me               = m1 * entrate * dP * 0.01
      q1               = mm1 / (mm1 + md1)
      qe               = rmix2q(rmixe)
      mm_in            = me * qe
      md_in            = me - mm_in
      [T1, md1, mm1]   = ent_parcel.mixair(P1, T1, Te, q1, qe, m1, me) 
      ammij[i,i]        = mm_in
      #----------------------------
      # evaporative cooling
      #----------------------------
      levap_cool = ent_parcel.evap_cool(P1, T1, mliq, mm1, md1)
      T1         = levap_cool[0]
      mevap      = levap_cool[1]
      mliq       = mliq - mevap
      mm1        = mm1 + mevap
      qtemp      = mm1 / (mm1 + md1)
      qstemp     = ent_parcel.cal_qs(T1, P1)
      RH         = qtemp / qstemp
      #print "RH",RH
      if (mevap >=0.0):
        if (mliq + mevap) ==0.0:
          print "mliq + mevap = 0.0"
          ammij[i]   = ammij[i]
          amliqij[i] = amliqij[i]
        else:   
          ammij[i]   = ammij[i]   + mevap * amliqij[i] / (mliq + mevap)
          amliqij[i] = amliqij[i] - mevap * amliqij[i] / (mliq + mevap)
      else:
        mcond = abs(mevap)
        amliqij[i] = amliqij[i] + mcond * ammij[i] / (mm1 + abs(mevap))
        ammij[i]   = ammij[i]   - mcond * ammij[i] / (mm1 + abs(mevap))
      #----------------------------
      # check buoyancy
      #----------------------------
      rmix1      = mm1 / md1
      rmixe      = q2rmix(qe)
      Tv1        = cal_Tv(T1, rmix1)
      Tve        = cal_Tv(Te, rmixe)
      P2        = P1 - dP
      if ( Tv1 <= Tve ):
        print "Buoyancy = 0.0" 
        P1 = miss
        continue
      else:
        #----------------------------
        # raise the parcel
        #----------------------------
        rmix1     = mm1 / md1
        #
        qs1  = ent_parcel.cal_qs(T1, P1)
        q1   = rmix2q(rmix1)
        RH1  = q1 / qs1 * 100.0
        #-- check RH ------
        if ( RH1 >= 100.0):
          print "saturated"
          T2      = ent_parcel.moistadiabat(P1, T1, P2, (P1-P2)/10.0)
          rmix2   = ent_parcel.cal_rmixs(P2, T2)
          cond    = (rmix1 - rmix2) * md1
          mm2     = mm1 - cond
        else:
          Plcl    = ent_parcel.lcl(P1, T1, q1)
          #-- check LCL ----
          if (-Plcl > -P2):
            print "P1 -> P2: dry rise"
            #print "Plcl",Plcl
            #print "P2", P2
            T2      = ent_parcel.t1tot2dry(T1, P1, P2)
            rmix2   = rmix1
            cond    = 0.0
            mm2     = mm1
          else:
            print "Plcl -> P2: moist rise"
            #--------------------------------
            # P1    -> Plcl : dry adiabatic, cond = 0
            #--------------------------------
            Tlcl      = ent_parcel.t1tot2dry(T1, P1, Plcl)
            rmixs_lcl = ent_parcel.cal_rmixs(Plcl, Tlcl)
            #--------------------------------
            # Plcl  -> P2   : moist adiabatic
            #--------------------------------
            T2        = ent_parcel.moistadiabat(Plcl, Tlcl, P2, (Plcl - P2)/10.0)
            rmix2     = ent_parcel.cal_rmixs(P2, T2)
            cond      = (rmix1 - rmix2) * md1
            mm2       = mm1 - cond
            #--------------------------------
        T_new       = T2
        md_new      = md1
        mliq_new    = mliq + cond
        mm_new      = mm2
        md_new      = md1
        #
        rmix_new    = mm_new / md_new
        q_new       = mm_new / (mm_new + md_new)
        qs_new      = ent_parcel.cal_qs(T_new, P2)
        RH_new      = q_new / qs_new
        #
        Tv_new      = cal_Tv(T_new, rmix_new)
        #--------------
        # tracer array
        #--------------
        if (mm1 + cond) ==0.0:
          print "mm1 + cond == 0.0"
          ammij[i]       = ammij[i]
          amliqij[i]     = amliqij[i]
        else:
          ammij[i]       = ammij[i]    - cond * ammij[i] / (mm1 + cond)
          amliqij[i]     = amliqij[i]  + cond * ammij[i] / (mm1 + cond)
        #---
        amcondij[i]      = amliqij[i]  - amliq_new
        amm_new        = ammij[i]
        amliq_new      = amliqij[i]
        #--------------
        print "T_new, mliq_new, RH_new", T_new, mliq_new, RH_new
        print "cond, Tv1 - Tve", cond, Tv1 - Tve
        #----------------------
        lout.append([P2*0.01, T_new, Tv1 - Tve, md_new, mm_new, mliq_new, mm_in, md_in, RH_new, cond])
        #-----------
        istop = i 
      #--------------------------------------
      P1 = P1 - dP
    #----------------------------------------
    # write to file
    #-------------------
    # table file
    #-------------------
    # cond source
    #--
    lcondsource = amliqij[istop]
    #--------
    sout = ""
    for i in range(istop):
      ltemp   = lout[i]  + [lcondsource[i]]
      stemp   = ",".join(map(str, ltemp))
      sout  = sout + stemp  + "\n"
    sout = "P2, T_new, Tv1 - Tve, md_new, mm_new, mliq_new, mm_in, md_in, RH_new, cond, cond_source" + "\n"+ sout
    f = open(oname, "w")
    f.write(sout)
    f.close()
    #-------------------
    # gridfig
    #-------------------
    if (entrate == 0.0):
      continue
    #-------------------
    lextent = [P0*0.01, Pend*0.01, P0*0.01, Pend*0.01]
    #-- ammij ---
    sname   = odir + "/ammij.e%s.RH%s.png"%(enttype, RHtype)
    p       = plt.imshow(ma.masked_equal(ammij*1000.,0.0), origin="ll", extent = lextent)
    cbar    = plt.colorbar()
    plt.savefig(sname)
    plt.close()
    #-- amcondij ---
    sname   = odir + "/amcondij.e%s.RH%s.png"%(enttype, RHtype)
    p       = plt.imshow(ma.masked_equal(amcondij*1000., 0.0), origin="ll", extent = lextent)
    cbar    = plt.colorbar()
    plt.savefig(sname)
    plt.close()
    #-------------------
     
