MODULE dtanl_fsub

CONTAINS
!*********************************************************
SUBROUTINE mk_a2wetbulbtheta(plev, a2T, a2q, nx, ny, a2wetbulbtheta)
implicit none
!--- in ---------
integer                  nx, ny
real,dimension(nx,ny) :: a2T, a2q
!f2py intent(in)         a2T, a2q
real                     plev       ! (Pa)
!f2py intent(in)         plev
!--- out --------
real,dimension(nx,ny) :: a2wetbulbtheta
!f2py intent(out)        a2wetbulbtheta
!--- calc -------
integer                  ix, iy
real                     t, q
!---------------------------------
do iy = 1, ny
  do ix = 1, nx
    t  = a2T(ix,iy)
    q  = a2q(ix,iy) 
    a2wetbulbtheta(ix,iy) = cal_wetbulbtheta(Plev, t, q)
  end do
end do

return
END SUBROUTINE mk_a2wetbulbtheta
!*********************************************************
SUBROUTINE mk_a2grad_abs_saone(a2in, a2gradabs)
!---------------------------------
! data order should be South -> North, West -> East
! returns two vector map (map of da/dx, map of da/dy)
!---------------------------------
implicit none
!--- in ----------
integer                 :: ny = 180
integer                 :: nx = 360
real,dimension(360,180) :: a2in
!f2py intent(in)           a2in
!--- out ---------
real,dimension(360,180) :: a2gradabs
!f2py intent(out)          a2gradabs
!--- para --------
real                    :: lat_first = -89.5
!--- calc --------
real                       dn, ds, dew
real                       vn, vs, vw, ve
real                       lat
real                       gradx, grady
integer                    ix,  iy
integer                    ixn, ixs, ixw, ixe
integer                    iyn, iys, iyw, iye
!-----------------
do iy = 1, ny
  lat = lat_first + (iy -1)*1.0
  dn  = hubeny_real(lat, 0.0, lat+1.0, 0.0)
  ds  = hubeny_real(lat, 0.0, lat-1.0, 0.0)
  dew = hubeny_real(lat, 0.0, lat, 1.0)
  do ix = 1, nx
    !---
    call ixy2iixy_saone(ix, iy+1, ixn, iyn)
    call ixy2iixy_saone(ix, iy-1, ixs, iys)
    call ixy2iixy_saone(ix-1, iy, ixw, iyw)
    call ixy2iixy_saone(ix+1, iy, ixe, iye)
    !---
    vn = a2in(ixn, iyn)
    vs = a2in(ixs, iys)
    vw = a2in(ixw, iyw)
    ve = a2in(ixe, iye)
    !---
    gradx = (ve - vw) / (2.0*dew)
    grady = (vn - vs) / (dn + ds)
    a2gradabs(ix, iy) = ( gradx**2.0 + grady**2.0)**0.5 
    !---
  end do
end do
!-----------------
return
END SUBROUTINE mk_a2grad_abs_saone


!*********************************************************
SUBROUTINE mk_a2grad_saone(a2in, a2gradx, a2grady)
!---------------------------------
! data order should be South -> North, West -> East
! returns two vector map (map of da/dx, map of da/dy)
!---------------------------------
implicit none
!--- in ----------
integer                 :: ny = 180
integer                 :: nx = 360
real,dimension(360,180) :: a2in
!f2py intent(in)           a2in
!--- out ---------
real,dimension(360,180) :: a2gradx, a2grady
!f2py intent(out)          a2gradx, a2grady
!--- para --------
real                    :: lat_first = -89.5
!--- calc --------
real                       dn, ds, dew
real                       vn, vs, vw, ve
real                       lat
integer                    ix,  iy
integer                    ixn, ixs, ixw, ixe
integer                    iyn, iys, iyw, iye
!-----------------
do iy = 1, ny
  lat = lat_first + (iy -1)*1.0
  dn  = hubeny_real(lat, 0.0, lat+1.0, 0.0)
  ds  = hubeny_real(lat, 0.0, lat-1.0, 0.0)
  dew = hubeny_real(lat, 0.0, lat, 1.0)
  do ix = 1, nx
    !---
    call ixy2iixy_saone(ix, iy+1, ixn, iyn)
    call ixy2iixy_saone(ix, iy-1, ixs, iys)
    call ixy2iixy_saone(ix-1, iy, ixw, iyw)
    call ixy2iixy_saone(ix+1, iy, ixe, iye)
    !---
    vn = a2in(ixn, iyn)
    vs = a2in(ixs, iys)
    vw = a2in(ixw, iyw)
    ve = a2in(ixe, iye)
    !---
    a2gradx(ix, iy) = (ve - vw) / (2.0*dew)
    a2grady(ix, iy) = (vn - vs) / (dn + ds)
    
  end do
end do
!-----------------
return
END SUBROUTINE mk_a2grad_saone
!*********************************************************
SUBROUTINE ixy2iixy_saone(ix, iy, iix, iiy)
!--------------------------
! data array order should be "South->North" & "West->East"
! data array : nx= 360, ny= 180
!--------------------------
implicit none
!--- input -----------
integer             ix, iy
!f2py intent(in)    ix, iy
!--- output ----------
integer             iix, iiy
!f2py intent(out)   iix, iiy
!--- calc  -----------
!---------------------
if (iy .le. 0)then
  iiy = 1 - iy
  iix = ix + 180
else if (iy .ge. 181) then
  iiy = 2*180 - iy +1
  iix = ix + 180
else
  iiy = iy
  iix = ix
end if
!
if (iix .ge. 361) then
  iix = mod(iix, 360)
else if (iix .le. 0) then
  iix = 360 - mod(abs(iix), 360)
end if
!
return
END SUBROUTINE ixy2iixy_saone
!*********************************************************
FUNCTION cal_wetbulbtheta(P, T, q)
implicit none
!----------------------------
! estimate wet-bulb potential temperature
!----------------------------
!--- in -------------
real                  P, T, q  ! (Pa), (K), (kg/kg: mixing ratio)
!f2py intent(in)      P, T, q
!--- out ------------
real                  cal_wetbulbtheta
!f2py intent(out)     cal_wetbulbtheta
!--- para -----------
real               :: P1000 = 1000.0*100.0
!--- calc -----------
real                  Plcl, Tlcl
!--------------------
Plcl  = cal_plcl(P, T, q)
Tlcl  = cal_tlcl(P, T, q)
!
cal_wetbulbtheta = t1_to_t2_moistadia(Plcl, P1000, Tlcl)
!
return
END FUNCTION cal_wetbulbtheta
!!!*********************************************************
FUNCTION t1_to_t2_moistadia(P1,P2, T1)
implicit none
!--- in -------------
real                  P1, P2, T1  ! pressure:(Pa), temperature:(K)
!f2py intent(in)      P1, P2, T1
!--- out ------------
real                  t1_to_t2_moistadia
!f2py intent(out)     t1_to_t2_moistadia
!--- para -----------
real               :: thres = 0.01
integer            :: imax  = 50
!--- calc -----------
real                  Tnow, Tnext, d
integer               i
!--------------------
Tnow = T1
Tnext = 0.0
do i = 1, imax
  call t1_to_t2_moistadia_sub(P1, P2, T1, Tnow, Tnext, d)
  if ( abs(d) .le. thres )then
    exit
  end if
  Tnow = Tnext
end do
t1_to_t2_moistadia  = Tnext
!
return
END FUNCTION t1_to_t2_moistadia
!!*********************************************************
SUBROUTINE t1_to_t2_moistadia_sub(P1,P2, T1, Tnow, Tnext, d)
implicit none
!--- in ----------
real                  P1, P2, T1, Tnow  ! pressure:(Pa), temerature:(K)
!f2py intent(in)      P1, P2, T1, Tnow
!--- out ---------
real                  Tnext, d
!f2py intent(out)     Tnext, d
!--- para --------
real               :: Cpd   = 1004.0 !(J kg^-1 K^-1)
real               :: Rd    = 287.04  !(J kg^-1 K^-1)
real               :: epsi  = 0.62185 ! = Rd/Rv = Mv/Md
real               :: Lv    = 2.5e6   ! for vaporization
real               :: P1000 = 1000.0*100.0
!--- calc --------
real                  f, df, dqs
real                  rA
real                  es, qs
!-----------------
es           = cal_es_water(Tnow)
qs           = cal_qs_water(Tnow, P2)
f            = cal_sateqtheta(P2, Tnow) - cal_sateqtheta(P1, T1)
rA           = (P1000/(P2-es))**(Rd/Cpd)
dqs          = epsi**2.0 * Lv*P2*es / (Rd *(P2-es)**2.0 *Tnow**2.0)
df           = rA*exp(Lv*qs/(Cpd*Tnow)) &
               + rA*Tnow* (Lv*(dqs*Tnow - qs)/(Cpd*Tnow**2.0)) &
                 *exp(Lv*qs/(Cpd*Tnow))
!
Tnext        = Tnow - f/df
d            = cal_sateqtheta(P2, Tnext) - cal_sateqtheta(P1, T1)
!-----------------
return
END SUBROUTINE t1_to_t2_moistadia_sub
!!*********************************************************
FUNCTION cal_sateqtheta(P, T)
implicit none
!--- in --------
real                  P, T  ! (Pa), (K)
!f2py intent(in)      P, T
!--- out -------
real                  cal_sateqtheta
!f2py intent(out)     cal_sateqtheta
!--- para ------
real               :: Cpd   = 1004.0 !(J kg^-1 K^-1)
real               :: Rd    = 287.04  !(J kg^-1 K^-1)             
real               :: Lv    = 2.5e6   ! for vaporization 
real               :: P1000 = 1000.0*100.0  !(Pa)
!--- calc ------
real                  drytheta
real                  es, qs
!---------------
es         = cal_es_water(T)
qs         = cal_qs_water(T, P)
drytheta   = T*( P1000/(P-es))**(Rd/Cpd)
cal_sateqtheta  = drytheta * exp((Lv*qs)/(Cpd*T))


END FUNCTION cal_sateqtheta
!!*********************************************************

FUNCTION cal_plcl(P0, T0, q0)
!!------------------------------------
!! Following the procedure from Yoshizaki and Kato (2007)
!! "Go-u Go-setsu no Kisho-gaku", A-3
!!------------------------------------
implicit none
!---- in ----------------
real                  P0, T0, q0  ! P:(Pa)  T:(K)  q:(kg/kg)
!f2py intent(in)      P0, T0, q0
!---- out ---------------
real                  cal_plcl    ! (Pa)
!---- calc --------------
real                  Plcl, Tlcl
!---- para --------------
real               :: Cpd   = 1004.0 !(J kg^-1 K^-1)
real               :: Rd    = 287.04  !(J kg^-1 K^-1)
!------------------------
Tlcl      = cal_tlcl(P0, T0, q0)
Plcl      = P0*(Tlcl/T0)**(Cpd/Rd)
cal_plcl  = Plcl
!------------------------
END FUNCTION cal_plcl

!**************************************************************
FUNCTION cal_tlcl(P0, T0, q0)
!!------------------------------------
!! Following the procedure from Yoshizaki and Kato (2007)
!! "Go-u Go-setsu no Kisho-gaku", A-3
!!------------------------------------
implicit none
!---- in  ---------------
real                  P0, T0, q0   ! P:(Pa)  T:(K)  q:(kg/kg)
!f2py intent(in)      P0, T0, q0
!---- out ---------------
real                  cal_tlcl     ! (K)
!f2py intent(out)     cal_tlcl
!---- calc --------------
real                  qs0
real                  Plcl, Tlcl
real                  Ttemp, Ptemp
!---- para --------------
real               :: Cpd   = 1004.0 !(J kg^-1 K^-1)
real               :: Rd    = 287.04  !(J kg^-1 K^-1)
!------------------------
!-- check saturation level ---
qs0   = cal_qs_water(T0, P0)
if (qs0 .le. q0)then
  cal_tlcl = T0
  return
endif
!-- FIRST guess ------
Tlcl  = cal_tlcl_sub(P0, T0, q0)
Plcl  = P0*(Tlcl/T0)**(Cpd/Rd)

!-- SECOND guess ------
Ttemp = Tlcl
Ptemp = Plcl

Tlcl  = cal_tlcl_sub(Ptemp, Ttemp, q0)

cal_tlcl = Tlcl
return
END FUNCTION cal_tlcl

!**************************************************************
FUNCTION cal_tlcl_sub(P0, T0, q0)
implicit none
!---- input  -------------
real                  P0, T0, q0   ! (Pa), (K), (kg/kg)
!---- output -------------
real                  cal_tlcl_sub
!---- calc   -------------
real                  qs0
real                  rA, rB, rC
real                  bunshi, bunbo
!---- para   -------------
real               :: Cpd   = 1004.0 !(J kg^-1 K^-1
real               :: Rd    = 287.04  !(J kg^-1 K^-1)
real               :: Lv    = 2.5e6   ! for vaporization
real               :: epsi  = 0.62185 ! = Rd/Rv = Mv/Md
!-------------------------
qs0        = cal_qs_water(T0, P0)

rA         = 2.0 * (qs0 - q0)/ (qs0 + q0)
rB         = Cpd * (epsi + (qs0 + q0)*0.5 )/(epsi*Rd)
rC         = Lv  * (epsi + (qs0 + q0)*0.5 )/ Rd

bunshi     = rB*T0 + rC - ( (rB*T0 - rC)**2.0 + 2.0*rA*rC*T0)**0.5
bunbo      = 2.0*rB - rA

cal_tlcl_sub= 2.0*bunshi/bunbo - T0

return
END FUNCTION cal_tlcl_sub  

!*********************************************************************
FUNCTION cal_qs_water(rT, rP)
  implicit none
  real                 rT, rP
!f2py intent(in)       rT, rP
  real                 res
  real                 cal_qs_water
!f2py intent(out)      cal_qs_water
  real,parameter    :: repsi = 0.62185
!
res = cal_es_water(rT)
cal_qs_water = repsi * res / (rP - res)
RETURN
END FUNCTION cal_qs_water
!*********************************************************************
FUNCTION cal_es_water(rT)
  real rT
  real cal_es_water
!
  real,parameter            ::  rT0 = 273.16
  real,parameter            ::  res0= 611.73 ![Pa]
  real,parameter            ::  Lv  = 2.5e6  ![J kg-1]
  real,parameter            ::  Rv  = 461.7 ![J K-1 kg -1]
!
cal_es_water = res0 * exp( Lv/Rv *(1.0/rT0 - 1.0/rT))
RETURN
END FUNCTION cal_es_water
!*********************************************************************

!**************************************************************
FUNCTION lcl_old(rPsfc, rTsfc, rqsfc)
!###########################################################
! original code was obtained from
! http://www1.doshisha.ac.jp/~jmizushi/program/Fortran90/4.2.txt
! modified by: N.Utsumi
! f(x)=x**3+6*x**2+21*x+32
!###########################################################
implicit none

real                  rPsfc, rTsfc, rqsfc   ! rPsfc:[Pa]
!f2py intent(in)      rPsfc, rTsfc, rqsfc
real                  lcl_old
!f2py intent(out)     lcl_old

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
  lcl_old = x    ! lcl = nan
else
  lcl_old = real(x) *100.0  ! [hPa] -> [Pa]
endif
!-----------------
! for the case: lcl is lower than the surface (RH > 100%)
!-----------------
if (-lcl_old .lt. -rPsfc) then
  lcl_old = rPsfc
endif
!-----------------
return
END FUNCTION lcl_old
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
  double precision :: Cpd   = 1004.0 !(J kg^-1 K^-1)
!
L = dble(cal_latentheat( real(Tsfc) ))
f1 = (1/T0 - Rv/L *log( q * P /( e0*(epsi + q) ) ) )**(-1)
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
  double precision :: Cpd   = 1004.0 !(J kg^-1 K^-1)
!
L = dble(cal_latentheat( real(Tsfc) ))
f1 = (1/T0 - Rv/L *log( q * P /( e0*(epsi + q) ) ) )**(-1)
f2 = Tsfc * ( P / Psfc )**(Rd/Cpd)
func = f1 - f2
!
df1_P = 1/P * Rv/L *(1/T0 - Rv/L*log( q*P /(e0*(epsi + q)) ) )**(-2)
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
FUNCTION hubeny_real(lat1, lon1, lat2, lon2)
  implicit none
  !-- for input -----------
  real                                  lat1, lon1, lat2, lon2
!f2py intent(in)                        lat1, lon1, lat2, lon2
  !-- for output-----------
  real                                  hubeny_real
!f2py intent(out)                       hubeny_real
  !-- for calc ------------
  real,parameter                     :: pi = atan(1.0)*4.0
  real,parameter                     :: a  = 6378137
  real,parameter                     :: b  = 6356752.314140
  real,parameter                     :: e2 = 0.00669438002301188
  real,parameter                     :: a_1_e2 = 6335439.32708317
  real                                  M, N, W
  real                                  latrad1, latrad2, lonrad1, lonrad2
  real                                  latave, dlat, dlon
  real                                  dlondeg
  !------------------------
  latrad1   = lat1 * pi / 180.0
  latrad2   = lat2 * pi / 180.0
  lonrad1   = lon1 * pi / 180.0
  lonrad2   = lon2 * pi / 180.0
  !
  latave    = (latrad1 + latrad2)/2.0
  dlat      = latrad2 - latrad1
  dlon      = lonrad2 - lonrad1
  !
  dlondeg   = lon2 - lon1
  if ( abs(dlondeg) .gt. 180.0) then
    dlondeg = 180.0 - mod(abs(dlondeg), 180.0)
    dlon    = dlondeg * pi / 180.0
  end if
  !-------
  W  = sqrt(1.0 - e2 * sin(latave)**2.0 )
  M  =  a_1_e2 / (W**3.0)
  N  =  a / W
  hubeny_real  = sqrt( (dlat * M)**2.0 + (dlon * N * cos(latave))**2.0 )
RETURN
END FUNCTION hubeny_real
!**************************************************************
!**************************************************************
!*********************************************************
END MODULE dtanl_fsub
