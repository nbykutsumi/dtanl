PROGRAM lcl
!###########################################################
! original code was obtained from
! http://www1.doshisha.ac.jp/~jmizushi/program/Fortran90/4.2.txt
! modified by: N.Utsumi
! f(x)=x**3+6*x**2+21*x+32
!###########################################################
double precision      Psfc, Tsfc, q
double precision      x, xk, fx
double precision      delta
integer               k
INTEGER,PARAMETER :: KMAX=99
!-------------
Psfc = 1000   !(hPa)
Tsfc = 293.15 !(K)
q    = 0.0087268029 !(kg/kg)
!-------------
x=1000.d0
delta=1.d-10
!-------------
fx=func(x, Psfc, Tsfc, q)
k=0
!WRITE(*,"('x(',i2,')=',1PE15.8,', f(',i2,')=',1PE15.8)") k,x,k,fx
!WRITE(*,*)

DO k=1,KMAX

xk=fnewton(x, Psfc, Tsfc, q)
fx=func(xk, Psfc, Tsfc, q)

!WRITE(*,"('x(',i2,')=',1PE15.8,', f(',i2,')=',1PE15.8)") k,xk,k,fx

    IF(abs(fx)<delta)GOTO 100

x=xk
    
END DO
WRITE(*,*) 'could not solve.'
STOP
100 CONTINUE
print *,"Tsfc=", Tsfc
print *,"Psfc=", Psfc
print *,"q=",q
WRITE(*,"('solution: x=',1PE15.8)") xk
STOP
!###########################################################
CONTAINS

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
print *,""
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
END PROGRAM lcl
