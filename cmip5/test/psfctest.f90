program psfctest
!***********************************************
implicit none
!** parameters ****
integer,parameter                  :: nx = 144
integer,parameter                  :: ny = 96
integer,parameter                  :: nz = 8
!******************
character*1000                        ciqsfc, ciTsfc, ciRHsfc, cizsfc, ciPsea
real,dimension(nx,ny)              :: r2qsfc, r2Tsfc, r2RHsfc, r2zsfc, r2Psea
real,dimension(nx,ny)              :: r2Psfc_alt, r2Psfc_humid
real,dimension(nx,ny)              :: r2RHsfc_alt, r2RHsfc_humid
!** for output ****
character*1000                     :: codRHsfc, codPsfc_alt, codPsfc_humid
real,dimension(nx,ny)              :: r2dRHsfc, r2dPsfc_alt, codPsfc_humid
!** for calculation ****
integer                               ix,iy,iz
real                                  rqsfc, rTsfc, rRHsfc, rzsfc, rPsea
real                                  res
real                                  re_alt, re_humid
real                                  lat, lon
!***********************************************
!ciqsfc = "/media/disk2/data/CMIP5/bn/huss/day/NorESM1-M/historical/r1i1p1/1998/huss_day_NorESM1-M_historical_r1i1p1_1998010100.bn"
!ciTsfc = "/media/disk2/data/CMIP5/bn/tas/day/NorESM1-M/historical/r1i1p1/1998/tas_day_NorESM1-M_historical_r1i1p1_1998010100.bn"
!ciRHsfc= "/media/disk2/data/CMIP5/bn/rhs/day/NorESM1-M/historical/r1i1p1/1998/rhs_day_NorESM1-M_historical_r1i1p1_1998010100.bn"
!cizsfc ="/media/disk2/data/CMIP5/bn/orog/fx/NorESM1-M/historical/r0i0p0/orog_fx_NorESM1-M_historical_r0i0p0.bn"
!ciPsea ="/media/disk2/data/CMIP5/bn/psl/day/NorESM1-M/historical/r1i1p1/1998/psl_day_NorESM1-M_historical_r1i1p1_1998010100.bn"
!***********************************************
!* average
!***********************************************
ciqsfc = "/media/disk2/out/CMIP5/day/NorESM1-M/historical/r1i1p1/cnd.mean/huss/1990-1999/01-12/huss_day_NorESM1-M_historical_r1i1p1_099.00.bn"
ciTsfc = "/media/disk2/out/CMIP5/day/NorESM1-M/historical/r1i1p1/cnd.mean/tas/1990-1999/01-12/tas_day_NorESM1-M_historical_r1i1p1_099.00.bn"
ciRHsfc= "/media/disk2/out/CMIP5/day/NorESM1-M/historical/r1i1p1/cnd.mean/rhs/1990-1999/01-12/rhs_day_NorESM1-M_historical_r1i1p1_099.00.bn"
cizsfc ="/media/disk2/data/CMIP5/bn/orog/fx/NorESM1-M/historical/r0i0p0/orog_fx_NorESM1-M_historical_r0i0p0.bn"
ciPsea = "/media/disk2/out/CMIP5/day/NorESM1-M/historical/r1i1p1/cnd.mean/psl/1990-1999/01-12/psl_day_NorESM1-M_historical_r1i1p1_099.00.bn"
!***********************************************
!* output files
!-----------------------------------------------
codRHsfc = "/home/utsumi/bin/dtanl/cmip5/test/dRHsfc_alt.bn"
codPsfc_alt = "/home/utsumi/bin/dtanl/cmip5/test/dPsfc_alt.bn"
codRHsfc = "/home/utsumi/bin/dtanl/cmip5/test/dRHsfc_alt.bn"
!***********************************************
! read files : 2D data
!-----------------------------------------------
open(11, file = ciqsfc,  access = "DIRECT", status ="old", recl =nx)
open(12, file = ciTsfc,  access = "DIRECT", status ="old", recl =nx)
open(13, file = ciRHsfc, access = "DIRECT", status ="old", recl =nx)
open(14, file = cizsfc,  access = "DIRECT", status ="old", recl =nx)
open(15, file = ciPsea,  access = "DIRECT", status ="old", recl =nx)
do iy =1, ny
  !--------
  read(11, rec=iy) ( r2qsfc(ix,iy)  , ix=1,nx)
  read(12, rec=iy) ( r2Tsfc(ix,iy)  , ix=1,nx)
  read(13, rec=iy) ( r2RHsfc(ix,iy) , ix=1,nx)
  read(14, rec=iy) ( r2zsfc(ix,iy)  , ix=1,nx)
  read(15, rec=iy) ( r2Psea(ix,iy)  , ix=1,nx)
enddo
close(11)
close(12)
close(13)
close(14)
close(15)
!***********************************************

!***********************************************
!***********************************************
!***********************************************
do iy = -40,31
  rTsfc = 273.15 +iy-1
  res = cal_es(rTsfc)
  print *,"T, es =", rTsfc -273.15, res/100.0
end do

do iy = 1,ny
  do ix = 1,nx
    rqsfc = r2qsfc(ix,iy)
    rTsfc = r2Tsfc(ix,iy)
    rzsfc = r2zsfc(ix,iy)
    rPsea = r2Psea(ix,iy)
    rRHsfc= r2RHsfc(ix,iy)
    !**************************************
    !* common variables
    !--------------------------------------
    res = cal_es(rTsfc)  
    !**************************************
    !** with altitude correction
    !-------------------------------------- 
    r2Psfc_alt(ix,iy)  =  Psea2Psfc( rTsfc, rqsfc, rzsfc, rPsea)
    re_alt             = r2Psfc_alt(ix,iy) *rqsfc /(rqsfc + 0.62185)
    r2RHsfc_alt(ix,iy) = re_alt / res *100
    !**************************************
    !** with from q & RH & Tsfc
    !**************************************
    r2Psfc_humid(ix,iy)= P_from_T_RH_q(rTsfc, rRHsfc, rqsfc)
    re_humid           = r2Psfc_humid(ix,iy) * rqsfc / (rqsfc + 0.63285)
    r2RHsfc_humid(ix,iy)=re_humid / res *100
    !**************************************
    r2dRHsfc(ix,iy)= r2RHsfc_alt(ix,iy) - r2RHsfc(ix,iy)
    !**************************************
    lat = -90 + (iy -1)*1.875
    if ( lon .lt. 72 ) then
      lon = (ix -1)*2.5
    else if (lon .lt. 72) then
      lon = -( 360 - (ix -1)*2.5)
    end if
    !**************************************
    !if (rTsfc .gt. 275.0) then
    !if (rTsfc .lt. 275.0) then
    !if (abs(r2RHsfc_alt(ix,iy) - r2RHsfc(ix,iy)) .gt. 2.0) then
    !  print *,"************************************"
    !  print *,"iy, ix=", iy, ix
    !  print *,"lat, lon =", lat, lon
    !  print *,"---------------"
    !  print *,"Tsfc =", rTsfc
    !  print *,"zsfc =", rzsfc
    !  print *,"---------------"
    !  print *,"Psfc_alt"   ,r2Psfc_alt(ix,iy)
    !  print *,"Psfc_humid" ,r2Psfc_humid(ix,iy)
    !  print *,"---------------"
    !  print *,"RHsfc_alt"  ,r2RHsfc_alt(ix,iy)
    !  print *,"RHsfc_humid",r2RHsfc_humid(ix,iy)
    !  print *,"RHsfc_org"  ,r2RHsfc(ix,iy)
    !  print *,"RH_alt - RH_org=", r2RHsfc_alt(ix,iy)- r2RHsfc(ix,iy)
    !endif
  end do
end do
!***********************************************
!* write to file
!***********************************************
open(11, file = codRHsfc, access="direct", recl=nx)
do iy = 1,ny
  write(11, rec=iy) (r2dRHsfc(ix,iy)     , ix=1,nx)
end do
close(11)
print *,codRHsfc
!***********************************************
CONTAINS
!***********************************************

!***********************************************
FUNCTION Psea2Psfc(Tsfc, qsfc, zsfc, Psea)
  implicit none
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
!***********************************************
FUNCTION P_from_T_RH_q(rT, rRH, rq)
  implicit none
  real                      rT, rq, rRH
  real                      res
  real                      P_from_T_RH_q
  real,parameter         :: epsi = 0.62185
  !---------------------------------------
  !!!  P = e * ( q + epsi) / q
  !!!  e = RH/100 * es
  !!!  then, P = RH/100 * es * (q + epsi) /q
  !---------------------------------------
res = cal_es(rT)
P_from_T_RH_q = rRH / 100.0 * res * (rq + epsi)/rq
RETURN
END FUNCTION P_from_T_RH_q
!***********************************************
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
!***********************************************
FUNCTION cal_latentheat(rT)
  implicit none
  real                  rT
  real,parameter     :: Lv = 2.5e6  ! for vaporization
  real,parameter     :: Ld = 2.834e6 ! for sublimation
  real,parameter     :: rTliq = 273.15  !   0 deg.C
  !real,parameter     :: rTice = 250.15   ! -23 deg.C
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
!***********************************************
!***********************************************
end program psfctest
