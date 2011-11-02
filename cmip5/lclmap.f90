PROGRAM lclmap
!--------------------------------------------------
implicit none
!
character*256                      cTsfc, cqsfc, czsfc
character*256                      cPsea
character*256                      cLCL
character*128                      cnx, cny
real                   rzsfc, rPsea
real                   rPsfc, rTsfc, rqsfc
real,allocatable,dimension(:,:) ::  r2zsfc, r2Psea
real,allocatable,dimension(:,:) ::  r2Psfc, r2Tsfc, r2qsfc, r2LCL
real                   x, kx, fx
real                   delta
integer                            k
integer                            io
integer                            nx, ny, xx, yy, ix, iy
integer,parameter       ::         KMAX=99
!--------------------------------------------------
! Get filenames
!--------------------------------------------------
if (iargc().lt.7) then
  print *, "Usage: cmd [ifile_Tsfc] [ifile_qsfc] [ifile_zsfc] [ifile_Psea] [ofile_LCL] [nx] [ny]"
  stop
endif
!
call getarg(1, cTsfc)
call getarg(2, cqsfc)
call getarg(3, czsfc)
call getarg(4, cPsea)
call getarg(5, cLCL)
call getarg(6, cnx)
call getarg(7, cny)
read(cnx, *) nx
read(cny, *) ny
!--------------------------------------------------
allocate( r2zsfc(nx,ny) )
allocate( r2Psea(nx,ny) )
allocate( r2Psfc(nx,ny) )
allocate( r2Tsfc(nx,ny) )
allocate( r2qsfc(nx,ny) )
allocate( r2LCL(nx,ny) )
!--------------------------------------------------
! read files
!--------------------------------------------------
open(11, file = cTsfc, access="DIRECT", status="old", recl =nx)
open(12, file = cqsfc, access="DIRECT", status="old", recl =nx)
open(13, file = czsfc, access="DIRECT", status="old", recl =nx)
open(14, file = cPsea, access="DIRECT", status="old", recl =nx)
do iy =1, ny
  !-----
  read(11, rec=iy) ( r2Tsfc(ix,iy) , ix=1, nx)
  read(12, rec=iy) ( r2qsfc(ix,iy) , ix=1, nx)
  read(13, rec=iy) ( r2zsfc(ix,iy) , ix=1, nx)
  read(14, rec=iy) ( r2Psea(ix,iy) , ix=1, nx)
  !-----
enddo
close(11)
close(12)
close(13)
close(14)
!---------------------------------------------------
! calculation 
!---------------------------------------------------
print *,czsfc
do iy = 1, ny
  do ix = 1, nx
    rTsfc = r2Tsfc(ix,iy)
    rqsfc = r2qsfc(ix,iy)
    rzsfc = r2zsfc(ix,iy)
    rPsea = r2Psea(ix,iy)
    !
    rPsfc = Psea2Psfc(rTsfc, rqsfc, rzsfc, rPsea)
    !
    r2LCL(ix,iy) = lcl(rPsfc, rTsfc, rqsfc)
  end do
end do
!---------------------------------------------------
! write to file
!---------------------------------------------------
open(55, file=cLCL, access="direct", recl=nx)
do iy = 1,ny
  write(55, rec=iy) ( r2LCL(ix,iy) , ix=1,nx)
end do
close(55)

CONTAINS
!***********************************************************
!* estimate Psfc
!***********************************************************
FUNCTION Psea2Psfc(Tsfc, qsfc, zsfc, Psea)
  real              Tsfc, qsfc, zsfc, Psea
  real              Psea2Psfc, Psfc
  real              Tvsfc  ! virtual temperature
  real              Tvm    ! mean virtual temperature
  real,parameter :: lapse_e = 0.0065   ! [K/m]
  real,parameter :: g       = 9.80665  ! [m/s^2]
  real,parameter :: Rd      = 287.04   !(J kg^-1 K^-1)
!
Tvsfc = Tsfc * (1.0 + 0.61*qsfc)
Tvm   =  Tvsfc + 1.0/2.0 *(1.0 + 0.61*qsfc)*lapse_e * zsfc
!
Psfc  = Psea * exp(-g*zsfc/(Rd*Tvm))
Psea2Psfc = Psfc
!
RETURN
END FUNCTION Psea2Psfc
!***********************************************************

FUNCTION lcl(rPsfc, rTsfc, rqsfc)
!###########################################################
! original code was obtained from
! http://www1.doshisha.ac.jp/~jmizushi/program/Fortran90/4.2.txt
! modified by: N.Utsumi
! f(x)=x**3+6*x**2+21*x+32
!###########################################################
real                  rPsfc, rTsfc, rqsfc
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
dPsfc_hPa = dble(rPsfc)*0.01d0 
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
!###########################################################

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!FUNCTION func(xx)
!   REAL(8),INTENT(IN) :: xx
!   REAL(8) :: func
!   func=xx**3+6.d0*xx**2+21.d0*xx+32.d0
!RETURN
!END FUNCTION func
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
FUNCTION func(P, Psfc, Tsfc, q)
  double precision      P, Psfc, Tsfc, q
  double precision      f1, f2, func
!
  double precision :: T0    = 273.16  !(K)
  double precision :: e0    = 6.1173  !(hPa)
  double precision :: Rv    = 461.7   !(J kg^-1 K^-1)
  double precision :: Lv    = 2.500d6 !(J kg^-1)
  double precision :: epsi  = 0.62185 !(-)
  double precision :: Rd    = 287.04  !(J kg^-1 K^-1)
  double precision :: Cpd   = 1004.67 !(J kg^-1 K^-1)
!
f1 = (1/T0 - Rv/Lv *log( q * P /( e0*(epsi + q) ) ) )**-1
f2 = Tsfc * ( P / Psfc )**(Rd/Cpd)
func = f1 - f2
RETURN
END FUNCTION func

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!FUNCTION fnewton(xx)
!   REAL(8),INTENT(IN) :: xx
!   REAL(8) :: fnewton
!fnewton=xx-(xx**3+6.d0*xx**2+21.d0*xx+32.d0)/(3.d0*xx**2+12.d0*xx+21.d0)
!RETURN
!END FUNCTION fnewton
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
FUNCTION fnewton(P, Psfc, Tsfc, q)
  double precision       P, Psfc, Tsfc, q
  double precision       f1, f2, func
  double precision       df1_P, df2_P, df_P
  double precision       fnewton
!
  double precision :: T0    = 273.16  !(K)
  double precision :: e0    = 6.1173  !(hPa)
  double precision :: Rv    = 461.7   !(J kg^-1 K^-1)
  double precision :: Lv    = 2.500d6 !(J kg^-1)
  double precision :: epsi  = 0.62185 !(-)
  double precision :: Rd    = 287.04  !(J kg^-1 K^-1)
  double precision :: Cpd   = 1004.67 !(J kg^-1 K^-1)
!
f1 = (1/T0 - Rv/Lv *log( q * P /( e0*(epsi + q) ) ) )**-1
f2 = Tsfc * ( P / Psfc )**(Rd/Cpd)
func = f1 - f2
!
df1_P = 1/P * Rv/Lv *(1/T0 - Rv/Lv*log( q*P /(e0*(epsi + q)) ) )**-2
df2_P = Tsfc* (1/Psfc)**(Rd/Cpd) * Rd/Cpd * (P **(Rd/Cpd -1))
df_P  = df1_P - df2_P
!
fnewton = P - func / df_P
RETURN
END FUNCTION fnewton
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


END PROGRAM lclmap




