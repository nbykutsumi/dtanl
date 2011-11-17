module dtanl_p_swa

CONTAINS
!**************************************************************
!* SUBROUTINE
!**************************************************************
!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
SUBROUTINE calc_swa( dP, r1lev, rTsfc, rqsfc, rPsfc, r1wap, nz, rSWA) 

  implicit none
  integer                            nz
  real                               dP       ! [Pa]
  real,dimension(nz)             ::  r1lev    ! [hPa]. This should be converted to [Pa]
!f2py intent(in)                     dP
!f2py intent(in)                     r1lev

!
  real                               rTsfc, rqsfc, rPsfc
  real,dimension(nz)             ::  r1wap
!f2py intent(in)                     rTsfc, rqsfc, rPsfc
!f2py intent(in)                     r1wap

!-- for calculation ------
  integer                            iz, iz_btm, iz_scnd
  real                               rPlcl, rW_lcl, rT_lcl
  real,dimension(nz)             ::  r1wap_fz, r1T
  !
  real                               rSWA
!f2py intent(out)                    rSWA
  real,parameter                 ::  rmiss = -9999.0

!  print *,"nz=",nz
!  print *,"dP=",dP
!  print *,"r1lev=",r1lev
!  print *,"r1wap=",r1wap
!---------------------------
! convert r1lev from [hPa] -> [Pa]
!---------------------------
r1lev = r1lev *100.0

!---------------------------
rPlcl    = lcl(rPsfc, rTsfc, rqsfc)
iz_btm   = findiz_btm( nz, r1lev, rPsfc)
iz_scnd  = findiz_scnd( nz, r1lev, rPlcl)
!
!***************************
!* correct_r1wap is used only for MERRA
!***************************
r1wap    = correct_r1wap(r1wap, r1lev, rPsfc, rmiss, iz_btm, nz) 
!-------------
!
rW_lcl   = omega_lcl( nz, iz_btm, iz_scnd, r1wap, r1lev, rPsfc, rPlcl)
!
rT_lcl   = T1toT2dry( rTsfc, rPsfc, rPlcl)
!
r1wap_fz = mk_r1wap_fillzero(nz, r1wap, r1lev, rPsfc)
!
r1T      = mk_r1T_extend(nz, rTsfc, rqsfc, r1lev, rPsfc, dP)
!***************************
!* from LCL to r1lev(iz_scnd_lcl1)
!***************************
rSWA = integral_WA_seg(&
           rPlcl, r1lev(iz_scnd)        &   ! rPb, rPt
         , rW_lcl,  r1wap_fz(iz_scnd)   &   ! rWb, rWt
         , rT_lcl                       &   ! rTb
         , dP)                              ! dP
!***************************
!** from r1lev(iz_scnd) to top *------------
!***************************
do iz = iz_scnd, nz-1
  rSWA = rSWA &
       + integral_WA_seg(&
         r1lev(iz), r1lev(iz +1)        &   ! rPb, rPt
       , r1wap_fz(iz), r1wap_fz(iz+1)   &   ! rWb, rWt
       , r1T(iz)                        &   ! rTb
       , dP)                                ! dP
end do
!***************************
if ( rSWA .gt. 2.0)then
  print *,"/////////////////////////////////////////////////"
  print *,"Plcl=", rPlcl
  print *,"iz_scnd=",iz_scnd
  print *,""
  print *,"r1lev=",r1lev
end if
RETURN
END SUBROUTINE calc_swa
!**************************************************************


!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
!**************************************************************
!* FUNCTIONS
!**************************************************************
!$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
FUNCTION integral_WA_seg(rPb, rPt, rWb, rWt, rTb, dP)
  implicit none
!-----------------------------------
real                            rPb, rPt
real                            rWb, rWt
real                            rTb
real                            dP
!
real                            rP, rT, rW, rdqdP, rV
real                            rTnew, rWnew, rPnew
real                            rdWdP
integer                         ip, np
!
real                             integral_WA_seg
!-----------------------------------
np = int( (rPb-rPt)/dP )
!--- initialize -------
rWnew = rWb
rTnew = rTb
rPnew = rPb
rdWdP = (rWb - rWt)/(rPb - rPt)
!------------------------------------
do ip = 1, np
  rP = rPnew
  rT = rTnew
  rW = rWnew
  rdqdP = cal_rdqdP(rP, rT, dP)
  !
  rPnew = rP - dP
  rTnew = moistadiabat(rP, rT, rP-dP, dP)
  rWnew = rW - rdWdP * dP
  !
  if (rW .ge. 0.0) then
    rV = 0.0
  else
    rV = rW * rdqdP
  endif
  integral_WA_seg = integral_WA_seg + rV * dP
end do
!--- from rP = rPb - dP*np  to rP =rPt ----
rP = rPnew
rT = rTnew
rW = rWnew
rdqdP = cal_rdqdP(rP, rT, dP)
if (rW .ge. 0.0) then
  rV = 0.0
else
  rV = rW * rdqdP
endif
integral_WA_seg = integral_WA_seg + rV * ( (rPb - rPt) - dP*np )
!------------------------------------
integral_WA_seg = -integral_WA_seg
RETURN
END FUNCTION integral_WA_seg
!**************************************************************

!**************************************************************
FUNCTION findiz_btm( nz, r1lev, rPsfc)
  implicit none
  real                              rPsfc
  real,dimension(nz)             :: r1lev
  real                              findiz_btm
  integer                           iz,nz
!
do iz = 1, nz
  if(-r1lev(iz) .gt.  -rPsfc ) then
    findiz_btm = iz
    exit
  elseif (iz .eq. nz) then
    findiz_btm = nz
    exit
  end if
end do
return
END FUNCTION findiz_btm
!**************************************************************
FUNCTION findiz_scnd( nz, r1lev, rPlcl )
  implicit none
  integer                          nz
  real,dimension(nz)           ::  r1lev
  real                             rPlcl
  integer                          iz, findiz_scnd
!
do iz =1,nz
  if (r1lev(iz) .lt. rPlcl)then
    findiz_scnd = iz
    exit
  elseif (iz .eq. nz) then
    findiz_scnd = -9999
  end if
end do
RETURN
END FUNCTION findiz_scnd
!**************************************************************
FUNCTION omega_lcl( nz, iz_btm, iz_scnd, r1wap, r1lev, rPsfc, rPlcl)
  implicit none
  integer                           nz
  integer                           iz_btm, iz_scnd
  real,dimension(nz)             :: r1wap, r1lev
  real                              rPsfc, rPlcl
  real                              omega_lcl
!
if (-rPlcl .lt. -r1lev(iz_btm) )then
  omega_lcl = -r1wap(iz_btm) &
            / (rPsfc - r1lev(iz_btm)) &
            * (rPlcl - rPsfc)
else
  omega_lcl = r1wap(iz_scnd -1) &
            + (r1wap(iz_scnd) - r1wap(iz_scnd -1)) &
            / (r1lev(iz_scnd) -r1lev(iz_scnd -1)) &
            * (rPlcl - r1lev(iz_scnd -1))
end if
RETURN
END FUNCTION OMEGA_LCL
!**************************************************************
FUNCTION T1toT2dry(rT1, rP1, rP2)
  implicit none
  real              rT1, rP1, rP2
  real              T1toT2dry, rT2
  real           :: Rd    = 287.04  !(J kg^-1 K^-1)
  real           :: Cpd   = 1004.67 !(J kg^-1 K^-1)
!
rT2 = rT1 * (rP2/rP1)**(Rd/Cpd)
T1toT2dry = rT2
END FUNCTION T1toT2dry
!**************************************************************
FUNCTION mk_r1wap_fillzero(nz, r1wap, r1lev, rPsfc)
  implicit none
  integer                          nz
  real                             rPsfc
  real,dimension(nz)            :: r1wap,r1lev
!-----
  integer                          iz
  real,dimension(nz)            :: mk_r1wap_fillzero
!-----------------
do iz =1,nz
  if (-r1lev(iz) .le. -rPsfc) then
    mk_r1wap_fillzero(iz) = 0.0
  else
    mk_r1wap_fillzero(iz) = r1wap(iz)
  endif
end do
RETURN
END FUNCTION mk_r1wap_fillzero
!**************************************************************


!**************************************************************
FUNCTION lcl(rPsfc, rTsfc, rqsfc)
!###########################################################
! original code was obtained from
! http://www1.doshisha.ac.jp/~jmizushi/program/Fortran90/4.2.txt
! modified by: N.Utsumi
! f(x)=x**3+6*x**2+21*x+32
!###########################################################
implicit none
real                  rPsfc, rTsfc, rqsfc   ! rPsfc:[Pa]
real                  lcl
double precision      dPsfc_hPa, dTsfc, dq
double precision      x, xk, fx
double precision      delta
integer               k
INTEGER,PARAMETER :: KMAX=99
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
STOP
100 CONTINUE
!
lcl = real(x) *100.0  ! [hPa] -> [Pa]
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
FUNCTION cal_latentheat(rT)
  implicit none
  real                  rT
  real,parameter     :: Lv = 2.5e6  ! for vaporization
  real,parameter     :: Ld = 2.834e6 ! for sublimation
  real,parameter     :: rTliq = 273.15  !   0 deg.C
  real,parameter     :: rTice = 250.15   ! -23 deg.C
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

!**************************************************************
FUNCTION cal_rdqdP(rP, rT, dP)
  implicit none
  real                   rP, rT, dP
!--------
  real                   rP1, rP2, rT1, rT2, rqs1, rqs2
  real                   cal_rdqdP
!-------------------
rP1 = rP
rP2 = rP - dP
rT1 = rT
rT2 = moistadiabat(rP1, rT1, rP2, dP)
rqs1 = cal_qs(rT1, rP1)
rqs2 = cal_qs(rT2, rP2)
cal_rdqdP = (rqs2 -rqs1)/(rP2 - rP1)
!
RETURN
END FUNCTION cal_rdqdP
!**************************************************************
FUNCTION moistadiabat(rP1,rT1, rP2, dP)
  implicit none
  real                       rP1, rP2, rT1, dP
  real                       rP, rT
  real                       rsign
  real                       rTnext, rT2, dT_dP
  real                       moistadiabat
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
!**************************************************************
FUNCTION dT_dP_moist(rP, rT)
  implicit none
  real                        rP, rT
  real                        res, rqs        ! rP:[Pa], not [hPa]
  real                        dT_dP_moist     ! [K/Pa], not [K/hPa]
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

!**************************************************************
FUNCTION cal_qs(rT, rP)
  implicit none
  real                 rT, rP
  real                 res
  real                 cal_qs
  real,parameter    :: repsi = 0.62185
!
res = cal_es(rT)
cal_qs = repsi * res / (rP - res)
RETURN
END FUNCTION cal_qs
!**************************************************************
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
!**************************************************************
FUNCTION mk_r1T_extend(nz, rTsfc, rqsfc, r1lev, rPsfc, dP)
  implicit none
  integer                   nz
  real                      rTsfc, rqsfc, rzsfc, rPsea
  real,dimension(nz)     :: r1lev
  real                      dP
!-------------
  integer                   iz, iz_scnd
  real                      rPsfc
  real                      rPlcl, rTlcl
  real                      rT1, rT2, rP1, rP2
  real,dimension(nz)     :: mk_r1T_extend
!------------------------------------------
! Extend the moist adiabatic temperature profile
! to the layers below LCL.
!------------------------------------------
rPlcl   = lcl(rPsfc, rTsfc, rqsfc)
iz_scnd = findiz_scnd( nz, r1lev, rPlcl )
rTlcl   = T1toT2dry(rTsfc, rPsfc, rPlcl)
if (iz_scnd .gt. 1) then
  do iz = 1,iz_scnd-1
    mk_r1T_extend(iz) =  moistadiabat(rPlcl, rTlcl, r1lev(iz), dP)
  end do
  !
  mk_r1T_extend(iz_scnd) = moistadiabat(rPlcl, rTlcl, r1lev(iz_scnd), dP)
  !
  do iz = iz_scnd +1, nz
    rT1 = mk_r1T_extend(iz -1)
    rP1 = r1lev(iz -1)
    rP2 = r1lev(iz)
    mk_r1T_extend(iz) = moistadiabat(rP1, rT1, rP2, dP)
  end do
else if (iz_scnd .eq. 1) then
  !
  mk_r1T_extend(iz_scnd) = moistadiabat(rPlcl, rTlcl, r1lev(iz_scnd), dP)
  !
  do iz = iz_scnd+1, nz
    rT1 = mk_r1T_extend(iz -1)
    rP1 = r1lev(iz -1)
    rP2 = r1lev(iz)
    mk_r1T_extend(iz) = moistadiabat(rP1, rT1, rP2, dP)
  end do
end if
RETURN
END FUNCTION mk_r1T_extend
!**************************************************************
FUNCTION correct_r1wap(r1wap, r1lev, rPsfc, rmiss, iz_btm, nz)
!**************************************************************
! CAUTION!
! This function (correct_r1wap) is for MERRA data.
!**********************
implicit none
integer                         iz_btm, nz
real,dimension(nz)           :: r1wap, r1lev
real                            rPsfc, rmiss
!
integer                         iz, iz_first
integer                         flag
real                            rP_first, rwap_first, A
real,dimension(nz)           :: correct_r1wap
!--------------------------
correct_r1wap = r1wap
!
flag = 0
iz_first = 0
do iz = 1, nz
  if ( r1wap(iz) .ne. rmiss) then
    !-------------------------------------
    ! check whether the correction is necessary or not.
    !-------------------------------------
    if ( iz .eq. iz_btm) then
      flag = 1
      exit
    !------------------------------
    else
      iz_first = iz
      exit
    endif
  endif
enddo
if (flag .ne. 1)then
  !-----------------
  ! for the case: iz_first < iz_btm
  !-----------------
  if (iz_first .lt. iz_btm) then
    iz_first = iz_btm
  endif
  !----------------
  rP_first = r1lev(iz_first)
  rwap_first = r1wap(iz_first)
  A = -rwap_first /(rPsfc - rP_first)
  !---
  do iz =1, iz_first-1
    if ( iz .lt. iz_btm ) then
      correct_r1wap(iz) = rmiss
    else
      correct_r1wap(iz) = A *(r1lev(iz) -rPsfc)
    endif
  enddo
endif
RETURN
END FUNCTION correct_r1wap

!**************************************************************
END MODULE dtanl_p_swa
