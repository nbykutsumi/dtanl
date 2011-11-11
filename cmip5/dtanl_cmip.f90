PROGRAM dtanl_cmip
!--------------------------------------------------------------
implicit none
!
character*1000                       cPRC1, cTsfc1, cqsfc1, cPsea1, cPlcl1, czg1, cwap1, czsfc1, cPrec1
character*1000                       cPRC2, cTsfc2, cqsfc2, cPsea2, cPlcl2, czg2, cwap2, czsfc2, cPrec2
character*1000                       clev
character*1000                       cofile1, cofile2
character*1000                       codPrec, coDdynam, coDlapse, coDhumid, coDfull, colcl_full, coNaN
character*100                        cnx, cny, cnz
!
integer                              nx, ny, nz
real,allocatable,dimension(:)     :: r1lev
real,allocatable,dimension(:,:)   :: r2PRC1, r2Tsfc1, r2qsfc1, r2zsfc1, r2Psea1
real,allocatable,dimension(:,:)   :: r2PRC2, r2Tsfc2, r2qsfc2, r2zsfc2, r2Psea2
real,allocatable,dimension(:,:,:) :: r3zg1, r3wap1
real,allocatable,dimension(:,:,:) :: r3zg2, r3wap2

!** parameter *
real,parameter                    :: dP =100.0 ! [Pa], not [hPa]
real,parameter                    :: rmiss = -9999.0
!real,parameter                    :: rmiss = 0.0/0.0
!** input for SUBROUTINE calc_scales ****
real                                 rTsfc1, rqsfc1, rzsfc1, rPsea1
real                                 rTsfc2, rqsfc2, rzsfc2, rPsea2
real,allocatable,dimension(:)     :: r1wap1, r1zg1
real,allocatable,dimension(:)     :: r1wap2, r1zg2
real                                 rSWA, rSdWA, rSWdA, rSWAdlcl
!** for calculation **
integer                              ix, iy, iz, nnx
real                                 rlat, rlon
real,allocatable,dimension(:,:)   :: r2SWA, r2SdWA, r2SWdA, r2SWAdlcl
real,allocatable,dimension(:,:)   :: r2dSWA
real,allocatable,dimension(:,:)   :: r2full, r2lcl_full
real,allocatable,dimension(:,:)   :: r2NaN
real,allocatable,dimension(:,:)   :: r2Prec1, r2Prec2, r2dPrec
real,allocatable,dimension(:,:)   :: r2dPRC, r2Pother1, r2Pother2, r2dPother
real,allocatable,dimension(:,:)   :: r2dTsfc, r2dqsfc, r2dqsatsfc, r2dRHsfc, r2dPlcl, r2absdRHsfc
real,allocatable,dimension(:)     :: r1Prec1, r1dPrec, r1dPRC, r1dPother
real,allocatable,dimension(:)     :: r1dTsfc, r1dqsfc, r1dqsatsfc, r1dRHsfc, r1dPlcl, r1abs, dRHsfc, r1absdRHsfc
real,allocatable,dimension(:)     :: r1SWA, r1SdWA, r1SWdA, r1SWAdlcl
real,allocatable,dimension(:)     :: r1dSWA
real                                 re1, re2, res1, res2, rRH1, rRH2, rqsatsfc1, rqsatsfc2, rPlcl1, rPlcl2,rPsfc1, rPsfc2
!***********************************************************
!--------------------------------------------------
! Get filenames
!--------------------------------------------------
if (iargc().lt.29) then
  print *, "Usage: cmd &
          & [ifile_prc1]  <-- convective precip &
          & [ifile_Tsfc1] [ifile_qsfc1]&
          & [ifile_Psea1] [ifile_zg1] [ifile_wap1] &
          & [ifile_zsfc1] [ifile_Prec1] &
          & [ifile_prc2]  <-- convective precip &
          & [ifile_Tsfc2] [ifile_qsfc2] &
          & [ifile_Psea2] [ifile_zg2] &
          & [ifile_wap2] [ifile_zsfc2] &
          & [ifile_Prec2] [ifile_lev] &
          & [olist_scale] [olist_others] &
          & [codPrec] [coDdynam] &
          & [coDlapse] [coDhumid] &
          & [coLCL_full] &
          & [coNaN] &
          & [nx] [ny] [nz]"
  stop
endif
!
call getarg(1, cPRC1)
call getarg(2, cTsfc1)
call getarg(3, cqsfc1)
call getarg(4, cPsea1)
call getarg(5, czg1)
call getarg(6, cwap1)
call getarg(7, czsfc1)
call getarg(8, cPrec1)
!
call getarg(9, cPRC2)
call getarg(10, cTsfc2)
call getarg(11, cqsfc2)
call getarg(12, cPsea2)
call getarg(13, czg2)
call getarg(14, cwap2)
call getarg(15, czsfc2)
call getarg(16, cPrec2)
!
call getarg(17, clev)
call getarg(18, cofile1)
call getarg(19, cofile2)
call getarg(20, codPrec)
call getarg(21, coDdynam)
call getarg(22, coDlapse)
call getarg(23, coDhumid)
call getarg(24, coDfull)
call getarg(25, colcl_full)
call getarg(26, coNaN)
call getarg(27, cnx)
call getarg(28, cny)
call getarg(29, cnz)
read(cnx, *) nx
read(cny, *) ny
read(cnz, *) nz
!--------------------------------------------------
!*** for input ******
allocate(r1lev(nz))
allocate(r2PRC1(nx,ny), r2Tsfc1(nx,ny), r2qsfc1(nx,ny), r2zsfc1(nx,ny), r2Psea1(nx,ny), r2Prec1(nx,ny))
allocate(r2PRC2(nx,ny), r2Tsfc2(nx,ny), r2qsfc2(nx,ny), r2zsfc2(nx,ny), r2Psea2(nx,ny), r2Prec2(nx,ny))
allocate(r3zg1(nx,ny,nz), r3wap1(nx,ny,nz))
allocate(r3zg2(nx,ny,nz), r3wap2(nx,ny,nz))
!*** for SUBROUTINE calc_scales ****
allocate(r1wap1(nz), r1zg1(nz))
allocate(r1wap2(nz), r1zg2(nz))
!*** for calculation ****
allocate(r2dPrec(nx,ny),r2dPRC(nx,ny), r2dTsfc(nx,ny), r2dqsfc(nx,ny), r2dqsatsfc(nx,ny), r2dRHsfc(nx,ny), r2dPlcl(nx,ny), r2absdRHsfc(nx,ny))
allocate(r2Pother1(nx,ny), r2Pother2(nx,ny), r2dPother(nx,ny))
allocate(r2SWA(nx,ny), r2SdWA(nx,ny), r2SWdA(nx,ny), r2SWAdlcl(nx,ny))
allocate(r2dSWA(nx,ny))
allocate(r2full(nx,ny), r2lcl_full(nx,ny))
allocate(r2NaN(nx,ny))
allocate(r1Prec1(ny), r1dPrec(ny), r1dPRC(ny), r1dTsfc(ny), r1dqsfc(ny), r1dqsatsfc(ny), r1dRHsfc(ny), r1dPlcl(ny), r1absdRHsfc(ny))
allocate(r1dPother(ny))
allocate(r1SWA(ny), r1SdWA(ny), r1SWdA(ny), r1SWAdlcl(ny))
allocate(r1dSWA(ny))
!!--------------------------------------------------
!allocate( r1temp(nz) )
!allocate( r2temp(nx,ny) )
!allocate( r3temp(nx,ny,nz) )
!--------------------------------------------------
! read files : 2D files
!--------------------------------------------------
open(11, file = cPRC1 , access="DIRECT", status="old", recl =nx)
open(12, file = cTsfc1, access="DIRECT", status="old", recl =nx)
open(13, file = cqsfc1, access="DIRECT", status="old", recl =nx)
open(14, file = czsfc1, access="DIRECT", status="old", recl =nx)
open(15, file = cPsea1, access="DIRECT", status="old", recl =nx)
open(16, file = cPrec1, access="DIRECT", status="old", recl =nx)
!
open(17, file = cPRC2,  access="DIRECT", status="old", recl =nx)
open(18, file = cTsfc2, access="DIRECT", status="old", recl =nx)
open(19, file = cqsfc2, access="DIRECT", status="old", recl =nx)
open(20, file = czsfc2, access="DIRECT", status="old", recl =nx)
open(21, file = cPsea2, access="DIRECT", status="old", recl =nx)
open(22, file = cPrec2, access="DIRECT", status="old", recl =nx)

do iy =1, ny
  !-----
  read(11, rec=iy) ( r2PRC1(ix,iy)  , ix=1, nx)
  read(12, rec=iy) ( r2Tsfc1(ix,iy) , ix=1, nx)
  read(13, rec=iy) ( r2qsfc1(ix,iy) , ix=1, nx)
  read(14, rec=iy) ( r2zsfc1(ix,iy) , ix=1, nx)
  read(15, rec=iy) ( r2Psea1(ix,iy) , ix=1, nx)
  read(16, rec=iy) ( r2Prec1(ix,iy) , ix=1, nx)
  !
  read(17, rec=iy) ( r2PRC2(ix,iy)  , ix=1, nx)
  read(18, rec=iy) ( r2Tsfc2(ix,iy) , ix=1, nx)
  read(19, rec=iy) ( r2qsfc2(ix,iy) , ix=1, nx)
  read(20, rec=iy) ( r2zsfc2(ix,iy) , ix=1, nx)
  read(21, rec=iy) ( r2Psea2(ix,iy) , ix=1, nx)
  read(22, rec=iy) ( r2Prec2(ix,iy) , ix=1, nx)
  !-----
enddo
close(11)
close(12)
close(13)
close(14)
close(15)
close(16)
close(17)
close(18)
close(19)
close(20)
close(21)
close(22)
!-------------------------------------------------
! read files : 3D files
!-------------------------------------------------
open(31, file = czg1,   access="DIRECT", status="old", recl =nx)
open(32, file = cwap1,   access="DIRECT", status="old", recl =nx)
open(33, file = czg2,   access="DIRECT", status="old", recl =nx)
open(34, file = cwap2,   access="DIRECT", status="old", recl =nx)
do iz=1, nz
  do iy=1, ny
    read(31, rec=(iz-1)*ny + iy) (r3zg1(ix,iy,iz) , ix=1, nx)
    read(32, rec=(iz-1)*ny + iy) (r3wap1(ix,iy,iz) , ix=1, nx)
    read(33, rec=(iz-1)*ny + iy) (r3zg2(ix,iy,iz) , ix=1, nx)
    read(34, rec=(iz-1)*ny + iy) (r3wap2(ix,iy,iz) , ix=1, nx)
  enddo
enddo
close(31)
close(32)
close(33)
close(34)
!-------------------------------------------------
! read files : 1D files
!-------------------------------------------------
open(11, file=clev, status="old")
do iz =1,nz
  read(11, *) r1lev(iz)
enddo
close(11)
!-------------------------------------------------
! calculate 2Pother
!-------------------------------------------------
r2Pother1 = r2Prec1 - r2PRC1
r2Pother2 = r2Prec2 - r2PRC2
!-----------------------------------------------------------
! calculation
!-----------------------------------------------------------
do iy =1,ny
  print *,iy
  do ix =1,nx
    !---------------
    ! make input data for SUBROUTINE cal_scales
    !---------------
    rTsfc1 = r2Tsfc1(ix,iy)
    rqsfc1 = r2qsfc1(ix,iy)
    rzsfc1 = r2zsfc1(ix,iy)
    rPsea1 = r2Psea1(ix,iy)
    r1wap1 = mk_r1wap_fillzero(nz, rTsfc1, rqsfc1, rzsfc1, rPsea1, r3wap1(ix,iy,:), r1lev)
    r1zg1  = r3zg1(ix,iy,:)
    !
    rTsfc2 = r2Tsfc2(ix,iy)
    rqsfc2 = r2qsfc2(ix,iy)
    rzsfc2 = r2zsfc2(ix,iy)
    rPsea2 = r2Psea2(ix,iy)
    r1wap2 = mk_r1wap_fillzero(nz, rTsfc2, rqsfc2, rzsfc2, rPsea2, r3wap2(ix,iy,:), r1lev)
    r1zg2  = r3zg2(ix,iy,:)
    !------------------
    call calc_scales(nz, r1lev, dP &
             ,rTsfc1, rqsfc1, rzsfc1, rPsea1, r1wap1, r1zg1 &
             ,rTsfc2, rqsfc2, rzsfc2, rPsea2, r1wap2, r1zg2 &
             ,rSWA, rSdWA, rSWdA, rSWAdlcl)
    !---------------
    ! make Prec, Tsfc, qsfc difference map between two era
    !---------------
    r2dPrec(ix,iy) = r2Prec2(ix,iy) - r2Prec1(ix,iy)
    r2dPrec(ix,iy) = r2dPrec(ix,iy) / r2Prec1(ix,iy) *100
    !
    r2dPRC(ix,iy)  = r2PRC2(ix,iy) - r2PRC1(ix,iy)
    r2dPRC(ix,iy)  = r2dPRC(ix,iy) / r2PRC1(ix,iy) * 100
    !
    r2dTsfc(ix,iy) = r2Tsfc2(ix,iy) - r2Tsfc1(ix,iy)
    r2dTsfc(ix,iy) = r2dTsfc(ix,iy) / r2Tsfc1(ix,iy) *100
    !
    r2dqsfc(ix,iy) = r2qsfc2(ix,iy) - r2qsfc1(ix,iy)
    r2dqsfc(ix,iy) = r2dqsfc(ix,iy) / r2qsfc1(ix,iy) *100
    !
    r2dPother(ix,iy) = r2Pother2(ix,iy) - r2Pother1(ix,iy)
    r2dPother(ix,iy) = r2dPother(ix,iy) / r2Pother1(ix,iy) *100
    !---------------
    ! make RHsfc and qsatsfc difference map
    !---------------
    rPsfc1 = Psea2Psfc( rTsfc1, rqsfc1, rzsfc1, rPsea1)
    rPsfc2 = Psea2Psfc( rTsfc2, rqsfc2, rzsfc2, rPsea2)
    re1 = rPsfc1 *rqsfc1 /(rqsfc1 + 0.62185)
    re2 = rPsfc2 *rqsfc2 /(rqsfc2 + 0.62185)
    res1 = cal_es(rTsfc1)
    res2 = cal_es(rTsfc2)
    rRH1 = re1 / res1 *100
    rRH2 = re2 / res2 *100
    r2absdRHsfc(ix,iy) = rRH2 - rRH1
    r2dRHsfc(ix,iy) = (rRH2 - rRH1)/rRH1
    !
    rqsatsfc1 = 0.62185*res1 / (rPsfc1 - res1)
    rqsatsfc2 = 0.62185*res2 / (rPsfc2 - res2)
    r2dqsatsfc(ix,iy) = (rqsatsfc2 - rqsatsfc1) / rqsatsfc1 *100
    !---------------
    ! make Plcl difference map
    !---------------
    rPlcl1 = lcl(rPsfc1, rTsfc1, rqsfc1)
    rPlcl2 = lcl(rPsfc2, rTsfc2, rqsfc2)
    r2dPlcl(ix,iy) = rPlcl1 - rPlcl2
    r2dPlcl(ix,iy) = r2dPlcl(ix,iy) / rPlcl1 *100
    !------------------
    !* filter too small r2Prec1 and r2SWA
    !------------------
    if ( (r2Prec1(ix,iy)*60*60*24 .lt. 1.0) .or. ( abs(rSWA*60*60*24) .lt. 1.0 )) then
      r2SWA(ix,iy)     = rmiss 
      r2SdWA(ix,iy)    = rmiss   
      r2SWdA(ix,iy)    = rmiss 
      r2SWAdlcl(ix,iy) = rmiss 
      r2full(ix,iy)    = rmiss
      !
      r2dPrec(ix,iy)   = rmiss
      r2dPRC(ix,iy)    = rmiss
      r2dPother(ix,iy) = rmiss
      r2NaN(ix,iy)     = 1.0
    else
      r2SWA(ix,iy)     = rSWA         
      r2SdWA(ix,iy)    = rSdWA /abs(rSWA)      *100   
      r2SWdA(ix,iy)    = rSWdA /abs(rSWA)      *100 
      r2SWAdlcl(ix,iy) = rSWAdlcl /abs(rSWA)   *100
      !
      r2full(ix,iy)    = r2SdWA(ix,iy) + r2SWdA(ix,iy) + r2SWAdlcl(ix,iy)
      r2NaN(ix,iy)     = 0.0
    end if
    !------------------
    ! make r2SWAdlcl / r2full
    !------------------
    if (r2full(ix,iy) .eq. rmiss) then
      r2lcl_full(ix,iy) = rmiss
    else
      r2lcl_full(ix,iy) = r2SWAdlcl(ix,iy) / abs(r2full(ix,iy))
    end if
    !------------------
  end do
end do
!rtemp = integral_WdA_seg(100000.0, 99000.0, 5.0, -5.0, 293.15, 298.15, dP)
!print *,rtemp

!** make zonal average **-----------
do iy = 1,ny
  !r1Prec1(iy)   = 0.0
  r1dPrec(iy)   = 0.0
  r1dPRC(iy)    = 0.0
  r1dPother(iy) = 0.0
  r1dTsfc(iy)   = 0.0
  r1dqsfc(iy)   = 0.0
  r1dRHsfc(iy)  = 0.0
  r1dPlcl(iy)   = 0.0
  r1absdRHsfc(iy)=0.0
  r1dqsatsfc(iy)= 0.0
  !
  r1SWA(iy)    = 0.0
  r1SdWA(iy)   = 0.0
  r1SWdA(iy)   = 0.0
  r1SWAdlcl(iy)= 0.0
  nnx = 0
  do ix = 1,nx
    if (iy .eq. 1) then
      print *,"iy,ix, r1dPrec=",iy,ix,r2dPrec(ix,iy)
    end if
    if ( r2SWA(ix,iy) .ne. rmiss) then
      nnx = nnx + 1      
      !r1Prec1(iy)   = r1Prec1(iy)  + r2Prec1(ix,iy)
      r1dPrec(iy)   = r1dPrec(iy)  + r2dPrec(ix,iy)
      r1dPRC(iy)    = r1dPRC(iy)   + r2dPRC(ix,iy)
      r1dPother(iy) = r1dPother(iy)+ r2dPother(ix,iy)
      r1dTsfc(iy)   = r1dTsfc(iy)  + r2dTsfc(ix,iy)
      r1dqsfc(iy)   = r1dqsfc(iy)  + r2dqsfc(ix,iy)
      r1dRHsfc(iy)  = r1dRHsfc(iy) + r2dRHsfc(ix,iy)
      r1dPlcl(iy)   = r1dPlcl(iy)  + r2dPlcl(ix,iy)
      r1absdRHsfc(iy)=r1absdRHsfc(iy) + r2absdRHsfc(ix,iy)
      r1dqsatsfc(iy)= r1dqsatsfc(iy) + r2dqsatsfc(ix,iy)
      !
      r1SWA(iy)     = r1SWA(iy)    + r2SWA(ix,iy)
      r1SdWA(iy)    = r1SdWA(iy)   + r2SdWA(ix,iy)
      r1SWdA(iy)    = r1SWdA(iy)   + r2SWdA(ix,iy)
      r1SWAdlcl(iy) = r1SWAdlcl(iy) + r2SWAdlcl(ix,iy) 
    end if
  end do
  r1dPrec(iy)   = r1dPrec(iy) /nnx 
  r1dPRC(iy)    = r1dPRC(iy) /nnx
  r1dPother(iy) = r1dPother(iy) /nnx
  r1dTsfc(iy)   = r1dTsfc(iy) /nnx
  r1dqsfc(iy)   = r1dqsfc(iy) /nnx
  r1dRHsfc(iy)  = r1dRHsfc(iy) /nnx
  r1dPlcl(iy)   = r1dPlcl(iy)  /nnx
  r1absdRHsfc(iy)=r1absdRHsfc(iy)/nnx
  r1dqsatsfc(iy)= r1dqsatsfc(iy) /nnx
  print *,"dqsat",r1dqsatsfc(iy)      
  !
  r1SWA(iy)     = r1SWA(iy) / nnx 
  r1SdWA(iy)    = r1SdWA(iy) / nnx 
  r1SWdA(iy)    = r1SWdA(iy) / nnx 
  r1SWAdlcl(iy) = r1SWAdlcl(iy) /nnx

  print * ,"aa",iy,r1dPrec(iy), r1dPRC(iy), r1SdWA(iy)+ r1SWdA(iy)+r1SWAdlcl(iy), r1SdWA(iy), r1SWdA(iy), r1SWAdlcl(iy)
end do

!------------------------------------------------
!** write to file
!------------------------------------------------
open(31, file=cofile1, status="replace")
do iy = 1,ny
  rlat = -90.0 + 180.0 / ny *iy - (180.0/ny)/2.0

  write(31, '(i4, f7.2, 7f8.2)') ,iy, rlat, r1dPrec(iy), r1SdWA(iy) +r1SWdA(iy)+r1SWAdlcl(iy), r1SdWA(iy), r1SWdA(iy), r1SWAdlcl(iy), r1dPRC(iy), r1dPother(iy)

end do
close(31) 
print *,cofile1
!------------------------------------------------
!** write other list file
!------------------------------------------------

open(32, file=cofile2, status="replace")
do iy = 1,ny
  rlat = -90.0 + 180.0 / ny *iy - (180.0/ny)/2.0
  print *,r1dPlcl(iy),r1dqsfc(iy),r1dqsatsfc(iy)
  write(32,'(i4, f7.2, 5f8.2)' ), iy, rlat, r1dTsfc(iy),r1absdRHsfc(iy), r1dPlcl(iy), r1dqsfc(iy), r1dqsatsfc(iy)

end do
close(32)
print *,cofile2
!------------------------------------------------
!** write r2dPrec (map) to file 
!------------------------------------------------
open(33, file=codPrec,  access="direct", recl=nx)
open(34, file=coDdynam, access="direct", recl=nx)
open(35, file=coDlapse, access="direct", recl=nx)
open(36, file=coDhumid, access="direct", recl=nx)
open(37, file=coDfull , access="direct", recl=nx)
open(38, file=colcl_full, access="direct",recl=nx)
open(39, file=coNaN,    access="direct", recl=nx)
do iy = 1,ny
  write(33, rec=iy) (r2dPrec(ix,iy)     , ix=1,nx)
  write(34, rec=iy) (r2SdWA(ix,iy)      , ix=1,nx)
  write(35, rec=iy) (r2SWdA(ix,iy)      , ix=1,nx)
  write(36, rec=iy) (r2SWAdlcl(ix,iy)   , ix=1,nx)
  write(37, rec=iy) (r2full(ix,iy)      , ix=1,nx)
  write(38, rec=iy) (r2lcl_full(ix,iy)  , ix=1,nx)
  write(39, rec=iy) (r2NaN(ix,iy)       , ix=1,nx)
end do
close(33)
close(34)
close(35)
close(36)
close(37)
close(38)
close(39)
print *,trim(codPrec)
!************************************
CONTAINS
!***********************************************************
!* estimate scales
!***********************************************************
SUBROUTINE calc_scales(nz, r1lev, dP &
           ,rTsfc1, rqsfc1, rzsfc1, rPsea1, r1wap1, r1zg1 &
           ,rTsfc2, rqsfc2, rzsfc2, rPsea2, r1wap2, r1zg2 &
           ,rSWA, rSdWA, rSWdA, rSWAdlcl)
!-----------------------------------------------------
  implicit none
  integer                       nz
  real,dimension(nz)         :: r1lev
  real                          dP
!
  real                          rTsfc, rqsfc, rzsfc, rPsea
  real,dimension(nz)         :: r1wap
  real                          rTsfc1, rqsfc1, rzsfc1, rPsea1
  real,dimension(nz)         :: r1wap1, r1zg1
  real                          rTsfc2, rqsfc2, rzsfc2, rPsea2
  real,dimension(nz)         :: r1wap2, r1zg2
!
!--- for calculation ----------------
  real                       :: rSWA, rSdWA, rSWdA, rSWAdlcl
!--
  real,dimension(nz)         :: r1wap_fz1, r1wap_fz2
  real,dimension(nz)         :: r1T1,      r1T2
  real,dimension(nz)         :: r1dqdP1,   r1dqdP2
!--
  integer                       iz, iz_btm, iz_scnd
  integer                       iz_btm1, iz_btm2
  integer                       iz_scnd_lcl1, iz_scnd_lcl2
  real,dimension(nz)         :: r1zg
  real                          rPlcl1, rPlcl2
  real                          rPsfc, rPsfc1, rPsfc2
  real                          rW1_lcl1, rW1_lcl2
  real                          rW2_lcl1, rW2_lcl2
  real                          rT1_lcl1,   rT1_lcl2
  real                          rT2_lcl1,   rT2_lcl2
  real                          rdqdP1_lcl1, rdqdP1_lcl2
  real                          rdqdP2_lcl1, rdqdP2_lcl2
!-------------
  real,parameter             :: rmiss = -9999.0
  ! this missing value doesn't affect the calculation
!-------------
!
!print *,"nz",nz
!print *,"Tsfc",rTsfc2
!print *,"qsfc",rqsfc2
!print *,"zsfc",rzsfc2
!print *,"Psea",rPsea2
!print *,"wap", r1wap2
!print *,"lev", r1lev
!
!--------
rPsfc1 = Psea2Psfc(rTsfc1, rqsfc1, rzsfc1, rPsea1)
rPsfc2 = Psea2Psfc(rTsfc2, rqsfc2, rzsfc2, rPsea2)
rPlcl1 = lcl(rPsfc1, rTsfc1, rqsfc1)
rPlcl2 = lcl(rPsfc2, rTsfc2, rqsfc2)
!**** state 1 *********
rTsfc = rTsfc1
rqsfc = rqsfc1
rzsfc = rzsfc1
rPsea = rPsea1
r1wap = r1wap1
r1zg  = r1zg1
rPsfc = rPsfc1
!------
iz_btm1      = findiz_btm( rzsfc, r1zg, nz)
iz_scnd_lcl1 = findiz_scnd( nz, r1lev, rPlcl1 )
!------
r1wap_fz1  = mk_r1wap_fillzero(nz, rTsfc, rqsfc, rzsfc, rPsea, r1wap, r1lev)
r1T1       = mk_r1T_extend(nz, rTsfc, rqsfc, rzsfc, rPsea, r1lev, dP)
r1dqdP1    = mk_r1dqdP(r1lev, r1T1, nz, dP, rmiss)
!------
rW1_lcl1 = omega_lcl( nz, iz_btm1, iz_scnd_lcl1, r1wap, r1lev, rPsfc, rPlcl1)
rW1_lcl2 = omega_lcl( nz, iz_btm1, iz_scnd_lcl1, r1wap, r1lev, rPsfc, rPlcl2)
!------
rT1_lcl1   = T1toT2dry(rTsfc, rPsfc1, rPlcl1)
rT1_lcl2   = moistadiabat(r1lev(1),r1T1(1), rPlcl2, dP)
!**** state 2 *********
rTsfc = rTsfc2
rqsfc = rqsfc2
rzsfc = rzsfc2
rPsea = rPsea2
r1wap = r1wap2
r1zg  = r1zg2
rPsfc = rPsfc2
!------
iz_btm2      = findiz_btm( rzsfc, r1zg, nz)
iz_scnd_lcl2 = findiz_scnd( nz, r1lev, rPlcl2 )
!------
r1wap_fz2  = mk_r1wap_fillzero(nz, rTsfc, rqsfc, rzsfc, rPsea, r1wap, r1lev)
r1T2       = mk_r1T_extend(nz, rTsfc, rqsfc, rzsfc, rPsea, r1lev, dP)
r1dqdP2    = mk_r1dqdP(r1lev, r1T2, nz, dP, rmiss)
!
rW2_lcl1 = omega_lcl( nz, iz_btm2, iz_scnd_lcl2, r1wap, r1lev, rPsfc, rPlcl1)
rW2_lcl2 = omega_lcl( nz, iz_btm2, iz_scnd_lcl2, r1wap, r1lev, rPsfc, rPlcl2)
!
rT2_lcl2   = T1toT2dry(rTsfc, rPsfc2, rPlcl2)
rT2_lcl1   = moistadiabat(r1lev(1),r1T2(1), rPlcl1, dP)
!**********************
!print *,r1wap_fz1
!print *,rT2_lcl2
!print *,rT2_lcl1
!** scales ************
!  integral_WA_seg(rP1, rP2, rW1, rW2, rT1, dP)
!  integral_dWA_seg(rP1, rP2, rW1_i, rW2_i, rW1_e, rW2_e, rT1, dP)
!  integral_WdA_seg(rP1, rP2, rW1, rW2, rT1_i, rT1_e, dP)
!************************
!** from rPlcl1 to r1lev(iz_scnd_lcl1) ***
!************************
rSWA  =  integral_WA_seg(&
            rPlcl1, r1lev(iz_scnd_lcl1) &               ! rP1, rP2
           , rW1_lcl1, r1wap_fz1(iz_scnd_lcl1)&          ! rW1, rW2
           , rT1_lcl1, dP)                               ! rT1, dP
rSdWA = integral_dWA_seg(&
            rPlcl1, r1lev(iz_scnd_lcl1) &               ! rP1, rP2
           , rW1_lcl1, r1wap_fz1(iz_scnd_lcl1) &         ! rW1_i, rW2_i
           , rW2_lcl1, r1wap_fz2(iz_scnd_lcl1)  &        ! rW1_e, rW2_e
           , rT1_lcl1, dP )                    ! rT1, dP
rSWdA = integral_WdA_seg(&
            rPlcl1, r1lev(iz_scnd_lcl1)  &              ! rP1, rP2
           , rW1_lcl1, r1wap_fz1(iz_scnd_lcl1)  &        ! rW1, rW2
           , rT1_lcl1, rT2_lcl1   &                      ! rT1_i, rT1_e
           , dP)                                         ! dP

!************************
!** from r1lev(iz_scnd) to top *------------ 
!************************
do iz = iz_scnd_lcl1, nz-1
  rSWA  = rSWA &
         + integral_WA_seg(&
              r1lev(iz), r1lev(iz +1) &                  ! rP1, rP2
             , r1wap_fz1(iz), r1wap_fz1(iz+1)&            ! rW1, rW2
             , r1T1(iz) , dP)                             ! rT1, dP
  rSdWA = rSdWA &
         + integral_dWA_seg(&
              r1lev(iz), r1lev(iz+1) &                   ! rP1, rP2
             , r1wap_fz1(iz), r1wap_fz1(iz+1) &           ! rW1_i, rW2_i
             , r1wap_fz2(iz), r1wap_fz2(iz+1) &           ! rW1_e, rW2_e
             , r1T1(iz), dP )                             ! rT1, dP
  rSWdA = rSWdA &
         + integral_WdA_seg(&
              r1lev(iz), r1lev(iz+1) &                   ! rP1, rP2
             , r1wap_fz1(iz), r1wap_fz1(iz+1) &            ! rW1, rW2
             , r1T1(iz), r1T2(iz)  &                      ! rT1_i, rT1_e
             , dP)                                        ! dP
  
  !rSWAdlcl = rSWAdlcl &
  !       + rW1_lcl1 * cal_rdqdP(rPlcl1, rT1_lcl1, dP) * (rPlcl2 - rPlcl1)


!  integral_WA_seg(rP1, rP2, rW1, rW2, rT1, dP)
!  integral_dWA_seg(rP1, rP2, rW1_i, rW2_i, rW1_e, rW2_e, rT1, dP)
!  integral_WdA_seg(rP1, rP2, rW1, rW2, rT1_i, rT1_e, dP)
end do
!************************
!** effect of LCL change ( from rPlcl1 to rPlcl2 )
!************************
if (rW1_lcl1 .lt. 0.0) then
  rSWAdlcl = -rW1_lcl1 * cal_rdqdP(rPlcl1, rT1_lcl1, dP) * (rPlcl2 - rPlcl1)
else
  rSWAdlcl = 0.0
end if
!print *, "bbbb",rSWAdlcl, rW1_lcl1, cal_rdqdP(rPlcl1, rT1_lcl1, dP), rPlcl1, rPlcl2

!************************

RETURN
END SUBROUTINE
!***********************************************************
!* estimate Psfc
!***********************************************************
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
!***********************************************************

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

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!FUNCTION fnewton(xx)
!   REAL(8),INTENT(IN) :: xx
!   REAL(8) :: fnewton
!fnewton=xx-(xx**3+6.d0*xx**2+21.d0*xx+32.d0)/(3.d0*xx**2+12.d0*xx+21.d0)
!RETURN
!END FUNCTION fnewton
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
FUNCTION findiz_btm( rzsfc, r1zg, nz)
  implicit none
  real                              rzsfc
  real,dimension(nz)             :: r1zg
  real                              findiz_btm
  integer                           iz,nz
!
do iz = 1, nz
  if(r1zg(iz) > rzsfc ) then
    findiz_btm = iz
    exit
  elseif (iz .eq. nz) then
    findiz_btm = nz
    exit
  end if
end do
return
END FUNCTION findiz_btm
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
FUNCTION omega_atP(nz, iz_btm, r1wap, r1lev, rPsfc, rP, rmiss)
  implicit none
  integer                           nz, iz_btm
  real,dimension(nz)             :: r1wap, r1lev
  real                              rPsfc, rP, rmiss
  integer                           iz_scnd
  real                              omega_atP
!
if ( -rP .lt. -rPsfc ) then
  omega_atP = rmiss
else if ( -rP .lt. -r1lev(iz_btm) ) then
  omega_atP = r1wap(iz_btm) + ( rP - r1lev(iz_btm) )&
                  *(0.0 - r1wap(iz_btm))/(rPsfc - r1lev(iz_btm))
else
  iz_scnd = findiz_scnd( nz, r1lev, rP )
  omega_atP =r1wap(iz_scnd)&
             + ( r1wap(iz_scnd -1) - r1wap(iz_scnd) )&
             /( r1lev(iz_scnd -1) - r1lev(iz_scnd) )&
             *( rP - r1lev(iz_scnd) )

end if
RETURN
END FUNCTION omega_atP
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
FUNCTION mk_r1dqdP(r1lev, r1T, nz, dP, rmiss)
  implicit none
  integer                       nz
  real,dimension(nz)         :: r1lev, r1T
  real                          dP, rmiss
!----------
  integer                       iz
  real,dimension(nz)         :: mk_r1dqdP
  real                          rP, rT
  real                          rtemp
!--------------
do iz = 1, nz -1
  if ( r1T(iz) .eq. rmiss) then
    mk_r1dqdP(iz) = rmiss
  else
    rP = r1lev(iz)
    rT = r1T(iz)
    mk_r1dqdP(iz) = cal_rdqdP(rP, rT, dP)
  end if
end do
mk_r1dqdP(nz) = 0.0
!
RETURN
END FUNCTION mk_r1dqdP
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
FUNCTION mk_r1wap_fillzero(nz, rTsfc, rqsfc, rzsfc, rPsea, r1wap, r1lev)
  implicit none
  integer                          nz
  real                             rTsfc, rqsfc, rzsfc, rPsea
  real,dimension(nz)            :: r1wap,r1lev
!-----
  integer                          iz
  real                             rPsfc
  real,dimension(nz)            :: mk_r1wap_fillzero
!-----------------
rPsfc = Psea2Psfc(rTsfc, rqsfc, rzsfc, rPsea)
do iz =1,nz
  if (-r1lev(iz) .le. -rPsfc) then
    mk_r1wap_fillzero(iz) = 0.0
  else
    mk_r1wap_fillzero(iz) = r1wap(iz)
  endif
end do
RETURN
END FUNCTION mk_r1wap_fillzero
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
FUNCTION mk_r1T_extend(nz, rTsfc, rqsfc, rzsfc, rPsea, r1lev, dP)
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
rPsfc   = Psea2Psfc(rTsfc, rqsfc, rzsfc, rPsea)
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
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
FUNCTION mk_r1T(nz, rTsfc, rqsfc, rzsfc, rPsea, r1lev, dP, rmiss)
  implicit none
  integer                   nz
  real                      rTsfc, rqsfc, rzsfc, rPsea
  real,dimension(nz)     :: r1lev
  real                      dP, rmiss
!-------------
  integer                   iz, iz_scnd
  real                      rPsfc
  real                      rPlcl, rTlcl
  real                      rT1, rT2, rP1, rP2
  real,dimension(nz)     :: mk_r1T
!
!-------------------------
rPsfc   = Psea2Psfc(rTsfc, rqsfc, rzsfc, rPsea)
rPlcl   = lcl(rPsfc, rTsfc, rqsfc)
iz_scnd = findiz_scnd( nz, r1lev, rPlcl )
rTlcl   = T1toT2dry(rTsfc, rPsfc, rPlcl)
if (iz_scnd .gt. 1) then
  do iz = 1,iz_scnd-1
    mk_r1T(iz) = rmiss 
  end do
  !
  mk_r1T(iz_scnd) = moistadiabat(rPlcl, rTlcl, r1lev(iz_scnd), dP)
  !
  do iz = iz_scnd +1, nz
    rT1 = mk_r1T(iz -1)
    rP1 = r1lev(iz -1)
    rP2 = r1lev(iz)
    mk_r1T(iz) = moistadiabat(rP1, rT1, rP2, dP)
  end do
else if (iz_scnd .eq. 1) then
  !
  mk_r1T(iz_scnd) = moistadiabat(rPlcl, rTlcl, r1lev(iz_scnd), dP)
  !
  do iz = iz_scnd+1, nz
    rT1 = mk_r1T(iz -1)
    rP1 = r1lev(iz -1)
    rP2 = r1lev(iz)
    mk_r1T(iz) = moistadiabat(rP1, rT1, rP2, dP)
  end do
end if
RETURN
END FUNCTION mk_r1T
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
FUNCTION integral_fromP(nz, rVlcl, rPlcl, r1V, r1lev)
  implicit none
  integer                     nz
  real                        rVlcl   ! Value at lcl
  real                        rPlcl       
  real,dimension(nz)       :: r1V     ! array of Values at each level
  real,dimension(nz)       :: r1lev
!
  integer                     iz_scnd, iz
  real                        rP1, rP2, rV1, rV2
  real                        integral_fromP
!------------------------
iz_scnd = findiz_scnd( nz, r1lev, rPlcl )
!
!-------
! from Plcl to P_scnd
!-------
rP1 = rPlcl
rP2 = r1lev(iz_scnd)
rV1 = rVlcl
rV2 = r1V(iz_scnd)
integral_fromP = 1.0/2.0*(rV1 + rV2) * (rP1 - rP2)
!-------
! from P_scnd to P_top
!-------
do iz = iz_scnd, nz -3  !  integral to top-2 layer 
  rP1 = r1lev(iz)
  rP2 = r1lev(iz+1)
  rV1 = r1V(iz)
  rV2 = r1V(iz+1)
  integral_fromP = integral_fromP + 1.0/2.0*(rV1 + rV2) * (rP1 - rP2)
end do
RETURN
END FUNCTION integral_fromP
!***************************************************
FUNCTION integral_WA_seg(rP1, rP2, rW1, rW2, rT1, dP)
  implicit none
!-----------------------------------
real                            rP1, rP2
real                            rW1, rW2
real                            rT1
real                            dP
!
real                            rP, rT, rW, rdqdP, rV
real                            rTnew, rWnew, rPnew
real                            rdWdP
integer                         ip, np
!
real                             integral_WA_seg
!-----------------------------------
np = int( (rP1-rP2)/dP )
!--- initialize -------
rWnew = rW1
rTnew = rT1
rPnew = rP1
rdWdP = (rW1 - rW2)/(rP1 - rP2)
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
!--- from rP = rP1 - dP*np  to rP =rP2 ----
rP = rPnew
rT = rTnew
rW = rWnew
rdqdP = cal_rdqdP(rP, rT, dP)
if (rW .ge. 0.0) then
  rV = 0.0
else
  rV = rW * rdqdP
endif
!print *,"P, W, dqdP", rP, rW, rdqdP
!print *," (rP1 - rP2) - dP*np )", (rP1 - rP2) - dP*np 
integral_WA_seg = integral_WA_seg + rV * ( (rP1 - rP2) - dP*np ) 
!------------------------------------
integral_WA_seg = -integral_WA_seg
RETURN
END FUNCTION integral_WA_seg
!***************************************************
FUNCTION integral_dWA_seg(rP1, rP2, rW1_i, rW2_i, rW1_e, rW2_e, rT1, dP)
  implicit none
!-----------------------------------
real                            rP1, rP2
real                            rW1_i, rW2_i, rW1_e, rW2_e
real                            rT1
real                            dP
!-----------
real                            rP, rT, rW_i, rW_e, rdqdP, rV
real                            rTnew, rWnew_i, rWnew_e, rPnew
real                            rdWdP_i, rdWdP_e
integer                        ip, np
!
real                             integral_dWA_seg
!-----------------------------------
np = int( (rP1-rP2)/dP )
!--- initialize -------
rWnew_i = rW1_i
rWnew_e = rW1_e
rTnew = rT1
rPnew = rP1
rdWdP_i = (rW1_i - rW2_i)/(rP1 - rP2)
rdWdP_e = (rW1_e - rW2_e)/(rP1 - rP2)
!------------------------------------
do ip = 1, np
  rP = rPnew
  rT = rTnew
  rW_i = rWnew_i
  rW_e = rWnew_e
  rdqdP = cal_rdqdP(rP, rT, dP)
  !
  rPnew = rP - dP
  rTnew = moistadiabat(rP, rT, rP-dP, dP)
  rWnew_i = rW_i - rdWdP_i * dP
  rWnew_e = rW_e - rdWdP_e * dP
  !
  if (rW_i .gt. 0.0) then
    rW_i = 0.0
  end if
  if (rW_e .gt. 0.0) then
    rW_e = 0.0
  end if
  rV = (dble(rW_e) - dble(rW_i)) * rdqdP
  integral_dWA_seg = integral_dWA_seg + rV * dP
end do

!--- from rP = rP1 - dP*np  to rP =rP2 ----
rP = rPnew
rT = rTnew
rW_i = rWnew_i
rW_e = rWnew_e
rdqdP = cal_rdqdP(rP, rT, dP)
!
if (rW_i .gt. 0.0) then
  rW_i = 0.0d0
end if
if (rW_e .gt. 0.0) then
  rW_e = 0.0d0
end if
rV = (dble(rW_e) - dble(rW_i)) * rdqdP
integral_dWA_seg = integral_dWA_seg + rV * ( (rP1 - rP2) -  dP*np )
!*** double --> real ******
integral_dWA_seg = real(integral_dWA_seg)
!------------------------------------
integral_dWA_seg = -integral_dWA_seg
RETURN
END FUNCTION integral_dWA_seg
!****************************************************
FUNCTION integral_WdA_seg(rP1, rP2, rW1, rW2, rT1_i, rT1_e, dP)
  implicit none
!-----------------------------------
real                            rP1, rP2
real                            rW1, rW2
real                            rT1_i, rT1_e
real                            dP
!
real                            rT_i, rT_e, rW, rP, rdqdP_i, rdqdP_e, rV
real                            rTnew_i, rTnew_e, rWnew, rPnew
real                            rdWdP
integer                         ip, np
!
real                            integral_WdA_seg
!-----------------------------------
np = int( (rP1-rP2)/dP )
!--- initialize -------
rWnew = rW1
rTnew_i = rT1_i
rTnew_e = rT1_e
rPnew = rP1
rdWdP = (rW1 - rW2)/(rP1 - rP2)
!------------------------------------
do ip = 1, np
  rP = rPnew
  rT_i = rTnew_i
  rT_e = rTnew_e
  rW = rWnew
  rdqdP_i = cal_rdqdP(rP, rT_i, dP)
  rdqdP_e = cal_rdqdP(rP, rT_e, dP)
  !
  rPnew = rP - dP
  rTnew_i = moistadiabat(rP, rT_i, rP-dP, dP)
  rTnew_e = moistadiabat(rP, rT_e, rP-dP, dP)
  rWnew = rW - rdWdP * dP
  !
  if (rW .ge. 0.0) then
    rV = 0.0
  else
    rV = rW * (rdqdP_e - rdqdP_i)
  endif
  integral_WdA_seg = integral_WdA_seg + rV * dP
end do
!--- from rP = rP1 - dP*np  to rP =rP2 ----
  rP = rPnew
  rT_i = rTnew_i
  rT_e = rTnew_e
  rW = rWnew
  rdqdP_i = cal_rdqdP(rP, rT_i, dP)
  rdqdP_e = cal_rdqdP(rP, rT_e, dP)
  !
  rPnew = rP - dP
  rTnew_i = moistadiabat(rP, rT_i, rP-dP, dP)
  rTnew_e = moistadiabat(rP, rT_e, rP-dP, dP)
  rWnew = rW - rdWdP * dP
  !
  if (rW .ge. 0.0) then
    rV = 0.0
  else
    rV = rW * (rdqdP_e - rdqdP_i)
  endif
  integral_WdA_seg = integral_WdA_seg + rV * ( (rP1 - rP2) - dP*np ) 
!-----------------------------------a
integral_WdA_seg = -integral_WdA_seg
RETURN
END FUNCTION integral_WdA_seg
!****************************************************

END PROGRAM dtanl_cmip

