module check_dtanl

CONTAINS
!*****************
FUNCTION f(x)
  implicit none
  real               x
!f2py intent(in)     x
  real               f
!f2py intent(out)    f
!-----------------
f = x*2
!-----------------
RETURN
END FUNCTION

!*****************
!*********************************************************************
!* FUNCTION
!*********************************************************************
FUNCTION cal_rdqdP(rP, rT, dP)
  implicit none
  real                   rP, rT, dP
!f2py intent(in)         rP, rT, dP         ! rP : [Pa], not in [hPa]
!--------
  real                   rP1, rP2, rT1, rT2, rqs1, rqs2
  real                   cal_rdqdP          ! [(g/g)/Pa], not in [(g/g)/hPa]   
!f2py intent(out)        cal_rdqdP 
!-------------------
cal_rdqdP = rP*2
rP1 = rP
rP2 = rP - dP
rT1 = rT
rT2 = moistadiabat(rP1, rT1, rP2, dP)
rqs1 = cal_qs(rT1, rP1)
rqs2 = cal_qs(rT2, rP2)
cal_rdqdP = (rqs2 -rqs1)/(rP2 - rP1)
!!
RETURN
END FUNCTION cal_rdqdP
!*********************************************************************
FUNCTION cal_q(rT, rP, rRH)
  implicit none
  !--------------
  real                  rT, rP, rRH     ! rP:[Pa], rRH:[%]
!f2py intent(in)        rT, rP, rRH
  !----
  real,parameter     :: repsi = 0.62185
  real                  res, re
  real                  cal_q
!f2py intent(out)       cal_q
  !---------------
res = cal_es(rT)
re  = rRH *0.01* res
cal_q = repsi * re / (rP - re)
!
RETURN
END FUNCTION cal_q
!*********************************************************************
FUNCTION lcl(rPsfc, rTsfc, rqsfc)
!###########################################################
! original code was obtained from
! http://www1.doshisha.ac.jp/~jmizushi/program/Fortran90/4.2.txt
! modified by: N.Utsumi
! f(x)=x**3+6*x**2+21*x+32
!###########################################################
implicit none
real                  rPsfc, rTsfc, rqsfc   ! rPsfc:[Pa]
!f2py intent(in)      rPsfc, rTsfc, rqsfc
real                  lcl
!f2py intent(out)     lcl
double precision      dPsfc_hPa, dTsfc, dq
double precision      x, xk, fx
double precision      delta
integer               k
INTEGER,PARAMETER :: KMAX=200
!-------------
!Psfc = 1000   !(hPa)
!Tsfc = 293.15 !(K)
!q    = 0.0087268029 !(kg/kg)
!-------------
dPsfc_hPa = dble(rPsfc)*0.01d0  ! Pa -> hPa
dTsfc = dble(rTsfc)
dq    = dble(rqsfc)
!-------------
x=1000.d0
delta=1.d-10
!-------------
fx=func(x, dPsfc_hPa, dTsfc, dq)
k=0
!WRITE(*,"('x(',i2,')=',1PE15.8,', f(',i2,')=',1PE15.8)") k,x,k,fx
!WRITE(*,*)

DO k=1,KMAX

xk=fnewton(x, dPsfc_hPa, dTsfc, dq)
fx=func(xk, dPsfc_hPa, dTsfc, dq)
!WRITE(*,"('x(',i2,')=',1PE15.8,', f(',i2,')=',1PE15.8)") k,xk,k,fx

    IF(abs(fx)<delta)GOTO 100

x=xk    ! LCL [hPa]

END DO

WRITE(*,*) 'could not solve.'
print *, "Psfc=",dPsfc_hPa
print *, "Tsfc=",dTsfc
print *, "q=",dq
print *, "fx=",fx
if (.not.isnan(x)) then
  STOP
endif

100 CONTINUE
!
if (isnan(x) ) then
  lcl = x    ! lcl = nan
else
  lcl = real(x) *100.0  ! [hPa] -> [Pa]
endif
!-----------------
! for the case: lcl is lower than the surface (RH > 100%)
!-----------------
if (-lcl .lt. -rPsfc) then
  lcl = rPsfc
endif
!-----------------
return
END FUNCTION lcl
!**************************************************************
FUNCTION func(P, Psfc, Tsfc, q)
  implicit none
  double precision      P, Psfc, Tsfc, q
  double precision      f1, f2, func
  double precision      L
!
  double precision :: T0    = 273.16  !(K)
  double precision :: e0    = 6.1173  !(hPa)
  double precision :: Rv    = 461.7   !(J kg^-1 K^-1)
  !double precision :: Lv    = 2.500d6 !(J kg^-1)
  double precision :: epsi  = 0.62185 !(-)
  double precision :: Rd    = 287.04  !(J kg^-1 K^-1)
  double precision :: Cpd   = 1004.67 !(J kg^-1 K^-1)
!
L = dble(cal_latentheat( real(Tsfc) ))
f1 = (1/T0 - Rv/L *log( q * P /( e0*(epsi + q) ) ) )**-1
f2 = Tsfc * ( P / Psfc )**(Rd/Cpd)
func = f1 - f2
RETURN
END FUNCTION func
!**************************************************************
FUNCTION fnewton(P, Psfc, Tsfc, q)
  implicit none
  double precision       P, Psfc, Tsfc, q
  double precision       f1, f2, func
  double precision       df1_P, df2_P, df_P
  double precision       fnewton

!
  double precision    L
  double precision :: T0    = 273.16  !(K)
  double precision :: e0    = 6.1173  !(hPa)
  double precision :: Rv    = 461.7   !(J kg^-1 K^-1)
  !double precision :: Lv    = 2.500d6 !(J kg^-1)
  double precision :: epsi  = 0.62185 !(-)
  double precision :: Rd    = 287.04  !(J kg^-1 K^-1)
  double precision :: Cpd   = 1004.67 !(J kg^-1 K^-1)
!
L = dble(cal_latentheat( real(Tsfc) ))
f1 = (1/T0 - Rv/L *log( q * P /( e0*(epsi + q) ) ) )**-1
f2 = Tsfc * ( P / Psfc )**(Rd/Cpd)
func = f1 - f2
!
df1_P = 1/P * Rv/L *(1/T0 - Rv/L*log( q*P /(e0*(epsi + q)) ) )**-2
df2_P = Tsfc* (1/Psfc)**(Rd/Cpd) * Rd/Cpd * (P **(Rd/Cpd -1))
df_P  = df1_P - df2_P
!
fnewton = P - func / df_P
RETURN
END FUNCTION fnewton
!**************************************************************
!**************************************************************
!*********************************************************************
FUNCTION moistadiabat(rP1,rT1, rP2, dP)
  implicit none
  real                       rP1, rP2, rT1, dP
!f2py intent(in)             rP1, rP2, rT1, dP
  real                       rP, rT
  real                       rsign
  real                       rTnext, rT2, dT_dP
  real                       moistadiabat
!f2py intent(out)            moistadiabat
  integer                    ip, np
!
  real                       rtemp
!
if (rP1 .ge. rP2) then
  rsign = 1.0
else
  rsign = -1.0
end if
np = int( (rP1 - rP2)/dP )
rP = rP1
rT = rT1
do ip = 1,abs(np)
  dT_dP = dT_dP_moist(rP, rT)
  rT = rT - rsign *dT_dP * dP
  rP = rP - rsign *dP
end do
rT2 = rT - rsign * dT_dP_moist( rP, rT ) * abs((rP1 - np*dP) - rP2)
moistadiabat = rT2
RETURN
END FUNCTION moistadiabat
!*********************************************************************
FUNCTION dT_dP_moist(rP, rT)
  implicit none
  real                        rP, rT
!f2py                         rP, rT
  real                        res, rqs        ! rP:[Pa], not [hPa]
  real                        dT_dP_moist     ! [K/Pa], not [K/hPa]
!f2py                         dT_dP_moist
!** parameters ******
  real                          L, a, b, c
  real,parameter            ::  epsi = 0.62185
  real,parameter            ::  cp   = 1004.67
  real,parameter            ::  Rd   = 287.04
  !real,parameter            ::  a0 = 0.28571
  !real,parameter            ::  b0 = 1.347e7
  !real,parameter            ::  c0 = 2488.4
  real                          rtemp
!********************
L = cal_latentheat(rT)
a = Rd / cp
b = epsi *(L**2)/(cp*Rd)
c = L/cp
rqs = cal_qs(rT, rP)
dT_dP_moist = (a * rT + c *rqs)/( rP *(1 + b*rqs/(rT**2) ) )
!
RETURN
END FUNCTION dT_dP_moist
!*********************************************************************
FUNCTION cal_qs(rT, rP)
  implicit none
  real                 rT, rP
!f2py intent(in)       rT, rP
  real                 res
  real                 cal_qs
!f2py intent(out)      cal_qs
  real,parameter    :: repsi = 0.62185
!
res = cal_es(rT)
cal_qs = repsi * res / (rP - res)
RETURN
END FUNCTION cal_qs
!*********************************************************************
FUNCTION T1toT2dry(rT1, rP1, rP2)
  implicit none
  real                 rT1, rP1, rP2
!f2py intent(in)       rT1, rP1, rP2   
  real                 T1toT2dry, rT2
!f2py intent(out)      T1toT2dry
  real              :: Rd    = 287.04  !(J kg^-1 K^-1)
  real              :: Cpd   = 1004.67 !(J kg^-1 K^-1)
!
rT2 = rT1 * (rP2/rP1)**(Rd/Cpd)
T1toT2dry = rT2
END FUNCTION T1toT2dry
!*********************************************************************
FUNCTION cal_es(rT)
  real rT
  real cal_es
!
  real                          L
  real,parameter            ::  rT0 = 273.16
  real,parameter            ::  res0= 611.73 ![Pa]
  !real,parameter            ::  Lv  = 2.5e6  ![J kg-1]
  real,parameter            ::  Rv  = 461.7 ![J K-1 kg -1]
!
L = cal_latentheat(rT)
cal_es = res0 * exp( L/Rv *(1.0/rT0 - 1.0/rT))
RETURN
END FUNCTION cal_es
!*********************************************************************
FUNCTION cal_latentheat(rT)
  implicit none
  real                  rT
  real,parameter     :: Lv = 2.5e6  ! for vaporization
  real,parameter     :: Ld = 2.834e6 ! for sublimation
  real,parameter     :: rTliq = 273.15  !   0 deg.C
  real,parameter     :: rTice = 250.15   ! -23 deg.C
  !real,parameter     :: rTice = 273.15   ! -23 deg.C
  !real,parameter     :: rTliq = 0.0  !  -273.15 deg.C
  !real,parameter     :: rTice = 0.0   ! -273.15
  real               cal_latentheat
!
if ( rT .ge. rTliq) then
  cal_latentheat = Lv
else if ( rT .le. rTice ) then
  cal_latentheat = Ld
else
  cal_latentheat = ((rT - rTice)*Lv + (rTliq - rT)*Ld)/(rTliq - rTice)
end if
RETURN
END FUNCTION cal_latentheat
!*********************************************************************
!*********************************************************************
!*********************************************************************
!*********************************************************************



end module check_dtanl
