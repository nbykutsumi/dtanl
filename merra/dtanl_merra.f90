PROGRAM dtanl_merra
!--------------------------------------------------------------
implicit none
!
character*1000                       cTsfc1, cqsfc1, cPsfc1, cPlcl1, czg1, cwap1, cPrec1
character*1000                       cTsfc2, cqsfc2, cPsfc2, cPlcl2, czg2, cwap2, cPrec2
character*1000                       clev
character*1000                       cofile1, cofile2
character*1000                       codPrec, coDdynam, coDlapse, coDhumid, coDps, coDfull, colcl_full
character*100                        cnx, cny, cnz
!
integer                              nx, ny, nz
real,allocatable,dimension(:)     :: r1lev
real,allocatable,dimension(:,:)   :: r2Tsfc1, r2qsfc1, r2Psfc1
real,allocatable,dimension(:,:)   :: r2Tsfc2, r2qsfc2, r2Psfc2
real,allocatable,dimension(:,:,:) :: r3zg1, r3wap1
real,allocatable,dimension(:,:,:) :: r3zg2, r3wap2

!** parameter *
real,parameter                    :: dP =100.0 ! [Pa], not [hPa]
real,parameter                    :: rmiss = -9999.0
real,parameter                    :: dsig = 0.001  
!real,parameter                    :: rmiss = 0.0/0.0
!** input for SUBROUTINE calc_scales ****
real                                 rTsfc1, rqsfc1, rPsfc1
real                                 rTsfc2, rqsfc2, rPsfc2
real,allocatable,dimension(:)     :: r1wap1, r1zg1
real,allocatable,dimension(:)     :: r1wap2, r1zg2
real                                 rSWA, rSdWA, rSWdA, rSWAdlcl, rdPsfcSWA
!** for calculation **
integer                              ix, iy, iz, nnx
real                                 rlat, rlon
real,allocatable,dimension(:,:)   :: r2SWA, r2SdWA, r2SWdA, r2SWAdlcl, r2dPsfcSWA
real,allocatable,dimension(:,:)   :: r2full, r2lcl_full
real,allocatable,dimension(:,:)   :: r2Prec1, r2Prec2, r2dPrec
real,allocatable,dimension(:,:)   :: r2dTsfc, r2dqsfc, r2dqsatsfc, r2dRHsfc, r2dPlcl, r2absdRHsfc
real,allocatable,dimension(:)     :: r1Prec1, r1dPrec
real,allocatable,dimension(:)     :: r1dTsfc, r1dqsfc, r1dqsatsfc, r1dRHsfc, r1dPlcl, r1abs, dRHsfc, r1absdRHsfc
real,allocatable,dimension(:)     :: r1SWA, r1SdWA, r1SWdA, r1SWAdlcl, r1dPsfcSWA
real                                 re1, re2, res1, res2, rRH1, rRH2, rqsatsfc1, rqsatsfc2, rPlcl1, rPlcl2
!***********************************************************
!--------------------------------------------------
! Get filenames
!--------------------------------------------------
if (iargc().lt.25) then
  print *, "Usage: cmd  [ifile_Tsfc1] [ifile_qsfc1]&
          & [ifile_Psea1] [ifile_zg1] &
          & [ifile_wap1] &
          & [ifile_Prec1] &
          & [ifile_Tsfc2] [ifile_qsfc2] &
          & [ifile_Psea2] [ifile_zg2] &
          & [ifile_wap2] &
          & [ifile_Prec2] [ifile_lev] &
          & [olist_scale] [olist_others] &
          & [codPrec] [coDdynam] &
          & [coDlapse] [coDhumid] &
          & [coLCL_full] &
          & [nx] [ny] [nz]"
  stop
endif
!
call getarg(1, cTsfc1)
call getarg(2, cqsfc1)
call getarg(3, cPsfc1)
call getarg(4, czg1)
call getarg(5, cwap1)
call getarg(6, cPrec1)
!
call getarg(7, cTsfc2)
call getarg(8, cqsfc2)
call getarg(9, cPsfc2)
call getarg(10, czg2)
call getarg(11, cwap2)
call getarg(12, cPrec2)
!
call getarg(13, clev)
call getarg(14, cofile1)
call getarg(15, cofile2)
call getarg(16, codPrec)
call getarg(17, coDdynam)
call getarg(18, coDlapse)
call getarg(19, coDhumid)
call getarg(20, coDps)
call getarg(21, coDfull)
call getarg(22, colcl_full)
call getarg(23, cnx)
call getarg(24, cny)
call getarg(25, cnz)
read(cnx, *) nx
read(cny, *) ny
read(cnz, *) nz
!--------------------------------------------------
!*** for input ******
allocate(r1lev(nz))
allocate(r2Tsfc1(nx,ny), r2qsfc1(nx,ny), r2Psfc1(nx,ny), r2Prec1(nx,ny))
allocate(r2Tsfc2(nx,ny), r2qsfc2(nx,ny), r2Psfc2(nx,ny), r2Prec2(nx,ny))
allocate(r3zg1(nx,ny,nz), r3wap1(nx,ny,nz))
allocate(r3zg2(nx,ny,nz), r3wap2(nx,ny,nz))
!*** for SUBROUTINE calc_scales ****
allocate(r1wap1(nz), r1zg1(nz))
allocate(r1wap2(nz), r1zg2(nz))
!*** for calculation ****
allocate(r2dPrec(nx,ny),r2dTsfc(nx,ny), r2dqsfc(nx,ny), r2dqsatsfc(nx,ny), r2dRHsfc(nx,ny), r2dPlcl(nx,ny), r2absdRHsfc(nx,ny))
allocate(r2SWA(nx,ny), r2SdWA(nx,ny), r2SWdA(nx,ny), r2SWAdlcl(nx,ny))
allocate(r2full(nx,ny), r2lcl_full(nx,ny))
allocate(r1Prec1(ny), r1dPrec(ny), r1dTsfc(ny), r1dqsfc(ny), r1dqsatsfc(ny), r1dRHsfc(ny), r1dPlcl(ny), r1absdRHsfc(ny))
allocate(r1SWA(ny), r1SdWA(ny), r1SWdA(ny), r1SWAdlcl(ny))
!!--------------------------------------------------
!allocate( r1temp(nz) )
!allocate( r2temp(nx,ny) )
!allocate( r3temp(nx,ny,nz) )
!--------------------------------------------------
! read files : 2D files
!--------------------------------------------------
open(11, file = cTsfc1, access="DIRECT", status="old", recl =nx)
open(12, file = cqsfc1, access="DIRECT", status="old", recl =nx)
open(13, file = cPsfc1, access="DIRECT", status="old", recl =nx)
open(14, file = cPrec1, access="DIRECT", status="old", recl =nx)
!
open(15, file = cTsfc2, access="DIRECT", status="old", recl =nx)
open(16, file = cqsfc2, access="DIRECT", status="old", recl =nx)
open(17, file = cPsfc2, access="DIRECT", status="old", recl =nx)
open(18, file = cPrec2, access="DIRECT", status="old", recl =nx)

do iy =1, ny
  !-----
  read(11, rec=iy) ( r2Tsfc1(ix,iy) , ix=1, nx)
  read(12, rec=iy) ( r2qsfc1(ix,iy) , ix=1, nx)
  read(13, rec=iy) ( r2Psfc1(ix,iy) , ix=1, nx)
  read(14, rec=iy) ( r2Prec1(ix,iy) , ix=1, nx)
  !
  read(15, rec=iy) ( r2Tsfc2(ix,iy) , ix=1, nx)
  read(16, rec=iy) ( r2qsfc2(ix,iy) , ix=1, nx)
  read(17, rec=iy) ( r2Psfc2(ix,iy) , ix=1, nx)
  read(18, rec=iy) ( r2Prec2(ix,iy) , ix=1, nx)
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
!!-------
!! hPa -> Pa
!!-------
!do iy = 1,ny
!  do ix = 1,nx
!    if (r2Psfc1(ix,iy) .ne. rmiss) then
!      r2Psfc1(ix,iy) = r2Psfc1(ix,iy) *100
!    end if
!    if (r2Psfc2(ix,iy) .ne. rmiss) then
!      r2Psfc2(ix,iy) = r2Psfc2(ix,iy) *100
!    end if
!  end do
!end do
!-------------------------------------------------
! read files : 3D files
!-------------------------------------------------
open(21, file = czg1,   access="DIRECT", status="old", recl =nx)
open(22, file = cwap1,   access="DIRECT", status="old", recl =nx)
open(23, file = czg2,   access="DIRECT", status="old", recl =nx)
open(24, file = cwap2,   access="DIRECT", status="old", recl =nx)
do iz=1, nz
  do iy=1, ny
    read(21, rec=(iz-1)*ny + iy) (r3zg1(ix,iy,iz) , ix=1, nx)
    read(22, rec=(iz-1)*ny + iy) (r3wap1(ix,iy,iz) , ix=1, nx)
    read(23, rec=(iz-1)*ny + iy) (r3zg2(ix,iy,iz) , ix=1, nx)
    read(24, rec=(iz-1)*ny + iy) (r3wap2(ix,iy,iz) , ix=1, nx)
  enddo
enddo
close(21)
close(22)
close(23)
close(24)
!!------
!! hPa -> Pa
!!------
!do iz =1,nz
!  do iy = 1,ny
!    do ix = 1,nx
!      if (r3wap1(ix,iy,iz) .ne. rmiss) then
!        r3wap1(ix,iy,iz) = r3wap1(ix,iy,iz)*100
!      endif
!      if (r3wap2(ix,iy,iz) .ne. rmiss) then
!        r3wap2(ix,iy,iz) = r3wap2(ix,iy,iz)*100
!      endif
!    end do
!  end do
!end do
!-------------------------------------------------
! read files : 1D files
!-------------------------------------------------
open(11, file=clev, status="old")
do iz =1,nz
  read(11, *) r1lev(iz)
enddo
close(11)
!----
! hPa -> Pa  ! only pressure level is denoted by [hPa] 
!----
do iz = 1,nz
  if (r1lev(iz) .ne. rmiss) then
    r1lev(iz) = r1lev(iz) * 100
  end if
end do
!-----------------------------------------------------------
! calculation
!-----------------------------------------------------------
do iy =1,ny
  do ix =1,nx
    !---------------
    ! make input data for SUBROUTINE cal_scales
    !---------------
    rTsfc1 = r2Tsfc1(ix,iy)
    rqsfc1 = r2qsfc1(ix,iy)
    !rzsfc1 = r2zsfc1(ix,iy)
    rPsfc1 = r2Psfc1(ix,iy)
    r1wap1 = mk_r1wap_fillzero(nz, rTsfc1, rqsfc1, rPsfc1, r3wap1(ix,iy,:), r1lev)
    r1zg1  = r3zg1(ix,iy,:)
    !
    rTsfc2 = r2Tsfc2(ix,iy)
    rqsfc2 = r2qsfc2(ix,iy)
    !rzsfc2 = r2zsfc2(ix,iy)
    rPsfc2 = r2Psfc2(ix,iy)
    r1wap2 = mk_r1wap_fillzero(nz, rTsfc2, rqsfc2, rPsfc2, r3wap2(ix,iy,:), r1lev)
    r1zg2  = r3zg2(ix,iy,:)
    !------------------
    call calc_scales(nz, r1lev, dsig &
             ,rTsfc1, rqsfc1, rPsfc1, r1wap1, r1zg1 &
             ,rTsfc2, rqsfc2, rPsfc2, r1wap2, r1zg2 &
             ,rSWA, rSdWA, rSWdA, rSWAdlcl, rdPsfcSWA)
!    !---------------
!    ! make Prec, Tsfc, qsfc difference map between two era
!    !---------------
!
!    r2dPrec(ix,iy) = r2Prec2(ix,iy) - r2Prec1(ix,iy)
!    r2dPrec(ix,iy) = r2dPrec(ix,iy) / r2Prec1(ix,iy) *100
!    !
!    r2dTsfc(ix,iy) = r2Tsfc2(ix,iy) - r2Tsfc1(ix,iy)
!    r2dTsfc(ix,iy) = r2dTsfc(ix,iy) / r2Tsfc1(ix,iy) *100
!    !
!    r2dqsfc(ix,iy) = r2qsfc2(ix,iy) - r2qsfc1(ix,iy)
!    r2dqsfc(ix,iy) = r2dqsfc(ix,iy) / r2qsfc1(ix,iy) *100
!    !---------------
!    ! make RHsfc and qsatsfc difference map
!    !---------------
!    !rPsfc1 = Psea2Psfc( rTsfc1, rqsfc1, rzsfc1, rPsea1)
!    !rPsfc2 = Psea2Psfc( rTsfc2, rqsfc2, rzsfc2, rPsea2)
!    re1 = rPsfc1 *rqsfc1 /(rqsfc1 + 0.62185)
!    re2 = rPsfc2 *rqsfc2 /(rqsfc2 + 0.62185)
!    res1 = cal_es(rTsfc1)
!    res2 = cal_es(rTsfc2)
!    rRH1 = re1 / res1 *100
!    rRH2 = re2 / res2 *100
!    r2absdRHsfc(ix,iy) = rRH2 - rRH1
!    r2dRHsfc(ix,iy) = (rRH2 - rRH1)/rRH1
!    !
!    rqsatsfc1 = 0.62185*res1 / (rPsfc1 - res1)
!    rqsatsfc2 = 0.62185*res2 / (rPsfc2 - res2)
!    r2dqsatsfc(ix,iy) = (rqsatsfc2 - rqsatsfc1) / rqsatsfc1 *100
!    !---------------
!    ! make Plcl difference map
!    !---------------
!    rPlcl1 = lcl(rPsfc1, rTsfc1, rqsfc1)
!    rPlcl2 = lcl(rPsfc2, rTsfc2, rqsfc2)
!    r2dPlcl(ix,iy) = rPlcl1 - rPlcl2
!    r2dPlcl(ix,iy) = r2dPlcl(ix,iy) / rPlcl1 *100
!    !------------------
!    !* filter too small r2Prec1 and r2SWA
!    !------------------
!    print *,r2Prec1(ix,iy)*60*60*24, rdPsfcSWA, abs(rSWA)
!    if ( (r2Prec1(ix,iy)*60*60*24 .lt. 1.0) .or. ( abs(rSWA*60*60*24) .lt. 1.0 )) then
!      r2SWA(ix,iy)     = rmiss 
!      r2SdWA(ix,iy)    = rmiss   
!      r2SWdA(ix,iy)    = rmiss 
!      r2SWAdlcl(ix,iy) = rmiss 
!      r2dPsfcSWA(ix,iy)= rmiss
!      r2full(ix,iy)    = rmiss
!      !
!      r2dPrec(ix,iy)   = rmiss
!    else
!      r2SWA(ix,iy)     = rSWA         
!      r2SdWA(ix,iy)    = rSdWA /abs(rSWA)      *100   
!      r2SWdA(ix,iy)    = rSWdA /abs(rSWA)      *100 
!      r2SWAdlcl(ix,iy) = rSWAdlcl /abs(rSWA)   *100
!      r2dPsfcSWA(ix,iy)= rdPsfcSWA /abs(rSWA)  *100
!      r2full(ix,iy)    = r2SdWA(ix,iy) + r2SWdA(ix,iy) + r2SWAdlcl(ix,iy)
!    end if
!    !------------------
!    ! make r2SWAdlcl / r2full
!    !------------------
!    if (r2full(ix,iy) .eq. rmiss) then
!      r2lcl_full(ix,iy) = rmiss
!    else
!      r2lcl_full(ix,iy) = r2SWAdlcl(ix,iy) / abs(r2full(ix,iy))
!    end if
!    !------------------
!    if ((ix .eq. 104).and.(iy .eq. 39)) then
!    !if (iy .eq. 39) then
!      print *,"P1, P2",r2Prec1(ix,iy), r2Prec2(ix,iy)
!      print *,"nz=",nz
!      print *,"r1lev=",r1lev
!      print *,"dP=",dP
!      print *,"Tsfc1, Tsfc2= ", rTsfc1, rTsfc2
!      print *,"rqsfc1,rqsfc2=", rqsfc1, rqsfc2
!      print *,"r1wap1=",r1wap1
!      print *,"r1zg1=",r1zg1
!      print *,ix,r2SWA(ix,iy), r2SdWA(ix,iy), r2SWdA(ix,iy), r2SWAdlcl(ix,iy)
!      !print *,iy,ix,rSWA,rSdWA,rSWdA,rSWAdlcl
!    endif
  end do
end do
!!rtemp = integral_WdA_seg(100000.0, 99000.0, 5.0, -5.0, 293.15, 298.15, dP)
!!print *,rtemp
!
!!** make zonal average **-----------
!do iy = 1,ny
!  !r1Prec1(iy)   = 0.0
!  r1dPrec(iy)   = 0.0
!  r1dTsfc(iy)   = 0.0
!  r1dqsfc(iy)   = 0.0
!  r1dRHsfc(iy)  = 0.0
!  r1dPlcl(iy)   = 0.0
!  r1absdRHsfc(iy)=0.0
!  r1dqsatsfc(iy)= 0.0
!  !
!  r1SWA(iy)    = 0.0
!  r1SdWA(iy)   = 0.0
!  r1SWdA(iy)   = 0.0
!  r1SWAdlcl(iy)= 0.0
!  r1dPsfcSWA(iy)=0.0
!  nnx = 0
!  do ix = 1,nx
!    if ( r2SWA(ix,iy) .ne. rmiss) then
!      nnx = nnx + 1      
!      !r1Prec1(iy)   = r1Prec1(iy)  + r2Prec1(ix,iy)
!      r1dPrec(iy)   = r1dPrec(iy)  + r2dPrec(ix,iy)
!      r1dTsfc(iy)   = r1dTsfc(iy)  + r2dTsfc(ix,iy)
!      r1dqsfc(iy)   = r1dqsfc(iy)  + r2dqsfc(ix,iy)
!      r1dRHsfc(iy)  = r1dRHsfc(iy) + r2dRHsfc(ix,iy)
!      r1dPlcl(iy)   = r1dPlcl(iy)  + r2dPlcl(ix,iy)
!      r1absdRHsfc(iy)=r1absdRHsfc(iy) + r2absdRHsfc(ix,iy)
!      r1dqsatsfc(iy)= r1dqsatsfc(iy) + r2dqsatsfc(ix,iy)
!      !
!      r1SWA(iy)     = r1SWA(iy)    + r2SWA(ix,iy)
!      r1SdWA(iy)    = r1SdWA(iy)   + r2SdWA(ix,iy)
!      r1SWdA(iy)    = r1SWdA(iy)   + r2SWdA(ix,iy)
!      r1SWAdlcl(iy) = r1SWAdlcl(iy) + r2SWAdlcl(ix,iy) 
!    end if
!  end do
!  r1dPrec(iy)   = r1dPrec(iy) /nnx 
!  r1dTsfc(iy)   = r1dTsfc(iy) /nnx
!  r1dqsfc(iy)   = r1dqsfc(iy) /nnx
!  r1dRHsfc(iy)  = r1dRHsfc(iy) /nnx
!  r1dPlcl(iy)   = r1dPlcl(iy)  /nnx
!  r1absdRHsfc(iy)=r1absdRHsfc(iy)/nnx
!  r1dqsatsfc(iy)= r1dqsatsfc(iy) /nnx
!  print *,"dqsat",r1dqsatsfc(iy)      
!  !
!  r1SWA(iy)     = r1SWA(iy) / nnx 
!  r1SdWA(iy)    = r1SdWA(iy) / nnx 
!  r1SWdA(iy)    = r1SWdA(iy) / nnx 
!  r1SWAdlcl(iy) = r1SWAdlcl(iy) /nnx
!
!
!  print * ,"aa",iy,r1dPrec(iy), r1SdWA(iy)+ r1SWdA(iy)+r1SWAdlcl(iy), r1SdWA(iy), r1SWdA(iy), r1SWAdlcl(iy)
!end do
!!------------------------------------------------
!!** write to file
!!------------------------------------------------
!open(31, file=cofile1, status="replace")
!do iy = 1,ny
!  rlat = -90.0 + 180.0 / ny *iy - (180.0/ny)/2.0
!
!  write(31, '(i4, f7.2, 5f8.2)') ,iy, rlat, r1dPrec(iy), r1SdWA(iy) +r1SWdA(iy)+r1SWAdlcl(iy), r1SdWA(iy), r1SWdA(iy), r1SWAdlcl(iy)
!
!end do
!close(31) 
!print *,cofile1
!!------------------------------------------------
!!** write other list file
!!------------------------------------------------
!
!open(32, file=cofile2, status="replace")
!do iy = 1,ny
!  rlat = -90.0 + 180.0 / ny *iy - (180.0/ny)/2.0
!  print *,r1dPlcl(iy),r1dqsfc(iy),r1dqsatsfc(iy)
!  write(32,'(i4, f7.2, 5f8.2)' ), iy, rlat, r1dTsfc(iy),r1absdRHsfc(iy), r1dPlcl(iy), r1dqsfc(iy), r1dqsatsfc(iy)
!
!end do
!close(32)
!print *,cofile2
!!------------------------------------------------
!!** write r2dPrec (map) to file 
!!------------------------------------------------
!open(33, file=codPrec,  access="direct", recl=nx)
!open(34, file=coDdynam, access="direct", recl=nx)
!open(35, file=coDlapse, access="direct", recl=nx)
!open(36, file=coDhumid, access="direct", recl=nx)
!open(37, file=coDfull , access="direct", recl=nx)
!open(38, file=colcl_full, access="direct",recl=nx)
!do iy = 1,ny
!  write(33, rec=iy) (r2dPrec(ix,iy)     , ix=1,nx)
!  write(34, rec=iy) (r2SdWA(ix,iy)      , ix=1,nx)
!  write(35, rec=iy) (r2SWdA(ix,iy)      , ix=1,nx)
!  write(36, rec=iy) (r2SWAdlcl(ix,iy)   , ix=1,nx)
!  write(37, rec=iy) (r2full(ix,iy)      , ix=1,nx)
!  write(38, rec=iy) (r2lcl_full(ix,iy)  , ix=1,nx)
!end do
!close(33)
!close(34)
!close(35)
!close(36)
!close(37)
!close(38)
!print *,trim(codPrec)
!************************************
CONTAINS
!***********************************************************
!* estimate scales
!***********************************************************
SUBROUTINE calc_scales(nz, r1lev, dsig &
           ,rTsfc1, rqsfc1, rPsfc1, r1wap1, r1zg1 &
           ,rTsfc2, rqsfc2, rPsfc2, r1wap2, r1zg2 &
           ,rSWA, rSdWA, rSWdA, rSWAdlcl, rdPsfcSWA)
!-----------------------------------------------------
  implicit none
  integer                       nz
  real,dimension(nz)         :: r1lev
  real                          dsig
!
  real                          rTsfc, rqsfc, rPsfc
  real,dimension(nz)         :: r1wap
  real                          rTsfc1, rqsfc1, rPsfc1
  real,dimension(nz)         :: r1wap1, r1zg1
  real                          rTsfc2, rqsfc2, rPsfc2
  real,dimension(nz)         :: r1wap2, r1zg2
!
!--- for calculation ----------------
  real                       :: rSWA, rSdWA, rSWdA, rSWAdlcl, rdPsfcWA, rdPsfcSWA
!--
  real,dimension(nz)         :: r1sig
  real,dimension(nz)         :: r1wap_fz1, r1wap_fz2
  real,dimension(nz)         :: r1dqdP1,   r1dqdP2
  real,dimension(nz*2)       :: r1P_jo1, r1P_jo2
  real,dimension(nz*2)       :: r1T_jo1, r1T_jo2
  real,dimension(nz*2)       :: r1wap_fzjo1, r1wap_fzjo2
  real,dimension(nz*2)       :: r1state_jo, r1iz_jo, r1sig_jo
!--
  integer                       iz, iz_btm, iz_scnd
  integer                       iz_scnd1_lcl1
  integer                       iz_btm1, iz_btm2
  integer                       iz_scnd_lcl1, iz_scnd_lcl2
  integer                       iz_scnd_jo_lcl1
  real,dimension(nz)         :: r1zg
  real                          dP
  real                          rdqdp
  real                          rdqdsig
  real                          rPlcl1, rPlcl2
  real                          rsiglcl1, rsiglcl2
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
!************************
!** Plcl
!************************
print *,"rPsfc1, rTsfc1, rqsfc1"
print *,rPsfc1, rTsfc1, rqsfc1
print *,"qs"
print *,cal_qs(rTsfc1, rPsfc1)

rPlcl1 = lcl(rPsfc1, rTsfc1, rqsfc1)
rPlcl2 = lcl(rPsfc2, rTsfc2, rqsfc2)
!
!************************
!** sigma order
!************************
call sigma_order(nz, rPsfc1, rPsfc2, r1lev, r1state_jo, r1iz_jo, r1sig_jo)
!************************
!** iz_btm
!************************
iz_btm1         = findiz_btm(r1lev, rPsfc1, nz, rmiss)
iz_btm2         = findiz_btm(r1lev, rPsfc2, nz, rmiss)
!************************
!** iz_scnd_lcl & iz_scnd_jo_lcl
!************************
iz_scnd_lcl1      = findiz_scnd( nz, r1lev, rPlcl1)
iz_scnd_jo_lcl1   = findiz_scnd_jo( nz, r1sig_jo, rPlcl1, rPsfc1)
print *,"Plcl1"
print *,rPlcl1
print *,"rPsfc1"
print *,rPsfc1
print *,"Plcl1/Psfc1="
print *,rPlcl1/rPsfc1
!print *,"r1sig_jo="
!print *,r1sig_jo
!print *,"iz_scnd_jo_lcl1="
!print *,iz_scnd_jo_lcl1
print *,"ここまで"
stop
!!************************
!!** mk_wapjoint
!!************************
!call mk_wapjoint(nz, iz_btm1, iz_btm2, rPsfc1, rPsfc2, r1lev, r1wap1, r1wap2, r1sig_jo, r1wap_fzjo1, r1wap_fzjo2)
!
!!************************
!!** rsiglcl
!!************************
!rsiglcl1   = rPlcl1 / rPsfc1
!rsiglcl2   = rPlcl2 / rPsfc2
!
!!************************
!!** r1P_jo
!!************************
!r1P_jo1    = r1sig_jo * rPsfc1 
!r1P_jo2    = r1sig_jo * rPsfc2
!
!!************************
!!** rW_lcl
!!************************
!rW1_lcl1   = omega_lcl( nz, iz_btm1, iz_scnd_lcl1, r1wap_fz1, r1lev, rPsfc1, rPlcl1)
!rW2_lcl1   = omega_lcl( nz, iz_btm2, iz_scnd_lcl1, r1wap_fz2, r1lev, rPsfc2, rPlcl1)
!
!!************************
!!** r1T_jo
!!************************
!r1T_jo1    = mk_r1T_extend(nz*2, rTsfc1, rqsfc1, rPsfc1, r1P_jo1)
!r1T_jo2    = mk_r1T_extend(nz*2, rTsfc2, rqsfc2, rPsfc2, r1P_jo2)
!
!!************************
!!** rT_lcl
!!************************
!rT1_lcl1   = T1toT2dry(rTsfc1, rPsfc1, rPlcl1)
!rT2_lcl1   = T1toT2dry(rTsfc2, rPsfc2, rPlcl1)
!
!!************************
!!** from rSIGlcl1 to r1lev ***
!!************************
!rSWA  = integral_WA_seg(&
!            dsig                               &     ! dsig
!          , rsiglcl1, r1sig(iz_scnd_jo_lcl1)   &     ! rsigb, rsigt
!          , rW1_lcl1                           &     ! rWb
!          , r1wap_fzjo1(iz_scnd_jo_lcl1)       &     ! rWt
!          , rPsfc1                             &     ! rPsfc
!          , rT1_lcl1 )                               ! rTb 
!
!rSdWA = integral_dWA_seg(&
!            dsig                               &     ! dsig
!          , rsiglcl1, r1sig(iz_scnd_jo_lcl1)   &     ! rsigb, rsigt
!          , rW1_lcl1, rW2_lcl1                 &     ! rWb1, rWb2
!          , r1wap_fzjo1(iz_scnd_jo_lcl1)       &     ! rWt1
!          , r1wap_fzjo2(iz_scnd_jo_lcl1)       &     ! rWt2
!          , rPsfc1, rPsfc2                     &     ! rPsfc1, rPsfc2
!          , rT1_lcl1 )                               ! rTb1 
!
!rSWdA = integral_WdA_seg(&
!            dsig                               &     ! dsig
!          , rsiglcl1, r1sig(iz_scnd_jo_lcl1)   &     ! rsigb, rsigt
!          , rW1_lcl1                           &     ! rWb1
!          , r1wap_fzjo1(iz_scnd_jo_lcl1)       &     ! rWt1
!          , rPsfc1, rPsfc2                     &     ! rPsfc1, rPsfc2
!          , rT1_lcl1, rT2_lcl1 )                     ! rTb1, rTb2
!!************************
!!** from r1lev(iz_scnd) to top *------------ 
!!************************
!do iz = iz_scnd_jo_lcl1, nz*2-1
!  rSWA  = rSWA &
!         + integral_WA_seg(&
!            dsig                                &  ! dsig
!          , r1sig(iz), r1sig(iz+1)                &  ! rsigb, rsigt
!          , r1wap_fzjo1(iz), r1wap_fzjo1(iz+1)  &  ! rWb, rWt
!          , rPsfc                               &  ! rPsfc
!          , r1T_jo1(iz) )                          ! rTb
!
!  rSdWA = rSdWA &
!         + integral_dWA_seg(&
!            dsig                               &   ! dsig
!          , r1sig(iz)                          &   ! rsigb
!          , r1sig(iz + 1)                      &   ! rsigt
!          , r1wap_fzjo1(iz)                    &   ! rWb1
!          , r1wap_fzjo2(iz)                    &   ! rWb2
!          , r1wap_fzjo1(iz + 1)                &   ! rWt1
!          , r1wap_fzjo2(iz + 1)                &   ! rWt2
!          , rPsfc1, rPsfc2                     &   ! rPsfc1, rPsfc2
!          , r1T_jo1(iz) )                          ! rTb1 
!
!  rSWdA = rSWdA &
!         + integral_WdA_seg(&
!            dsig                               &   ! dsig
!          , r1sig(iz), r1sig(iz+1)             &   ! rsigb, rsigt
!          , r1wap_fzjo1(iz)                    &   ! rWb1
!          , r1wap_fzjo1(iz+1)                  &   ! rWt1
!          , rPsfc1, rPsfc2                     &   ! rPsfc1, rPsfc2 
!          , r1T_jo1(iz)                        &   ! rTb1
!          , r1T_jo2(iz) )                          ! rTb2
!end do
!!************************
!!** effect of LCL change ( from rPlcl1 to rPlcl2 )
!!************************
!if (rW1_lcl1 .lt. 0.0) then
!  dP = dsig * rPsfc
!  rdqdP = cal_rdqdP(rPlcl1, rT1_lcl1, dP)
!  rdqdsig = rdqdP * rPsfc1
!  rSWAdlcl = - rPsfc1 * rW1_lcl1 * rdqdsig * (rsiglcl2 - rsiglcl1)
!else
!  rSWAdlcl = 0.0
!end if
!!************************
!!** effect of Psfc change
!!************************
!rdPsfcSWA = (rPsfc2 - rPsfc1) * rSWA
RETURN
END SUBROUTINE

!!***********************************************************
!!* sigma_order
!!***********************************************************
SUBROUTINE sigma_order(nz, rPsfc1, rPsfc2, r1lev, r1state_jo, r1iz_jo, r1sig_jo)
  implicit none
  integer                     nz
  real                        rPsfc1, rPsfc2
  real,dimension(nz)         :: r1lev
  real,dimension(nz*2)       :: r1state_jo, r1iz_jo
  real,dimension(nz*2)       :: r1sig_jo
!
  integer                     iz, iz1, iz2
  real,dimension(nz)     :: r1sig1, r1sig2
!
r1sig1 = r1lev / rPsfc1
r1sig2 = r1lev / rPsfc2
!
iz1 = 1
iz2 = 1

do iz = 1, nz*2
  if ((iz1 .le. nz).and.( r1sig1(iz1) .ge. r1sig2(iz2) ))then
    r1state_jo(iz) = 1
    r1iz_jo(iz)    = iz1
    r1sig_jo(iz)   = r1sig1(iz1)
    if (iz1 .le. nz) then
      iz1 = iz1 + 1
    end if
  else
    r1state_jo(iz) = 2
    r1iz_jo(iz)    = iz2
    r1sig_jo(iz)   = r1sig2(iz2)
    if (iz2 .lt. nz) then
      iz2 = iz2 + 1
    end if
  end if
end do

RETURN
END SUBROUTINE
!!***********************************************************
!** mk_wapjoint
!!***********************************************************
SUBROUTINE mk_wapjoint(nz, iz_btm1, iz_btm2, rPsfc1, rPsfc2, r1lev, r1wap1, r1wap2, r1sig_jo, r1wap_fzjo1, r1wap_fzjo2)
  implicit none
  integer                                  nz
  integer                                  iz_btm1, iz_btm2
  real                                     rPsfc1, rPsfc2
  real,dimension(nz)                    :: r1lev
  real,dimension(nz)                    :: r1wap1, r1wap2
  real,dimension(nz*2)                  :: r1sig_jo
  real,dimension(nz*2)                  :: r1wap_fzjo1, r1wap_fzjo2
!
  integer                                  iz
  real                                     rP1, rP2
  real                                     rwap_jo1, rwap_jo2
do iz = 1,nz*2
  rP1 = r1sig_jo(iz) * rPsfc1
  rP2 = r1sig_jo(iz) * rPsfc2
  r1wap_fzjo1(iz) = omega_atP(nz, iz_btm1, r1wap1, r1lev, rPsfc1, rP1, 0.0)
  r1wap_fzjo2(iz) = omega_atP(nz, iz_btm2, r1wap2, r1lev, rPsfc2, rP2, 0.0)
end do
!
RETURN
END SUBROUTINE

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
!rPsfc = 67943.93   !(Pa)
!rTsfc = 233.7704 !(K)
!rqsfc    = 0.00017255328 !(kg/kg)
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
FUNCTION findiz_btm(r1lev, rPsfc, nz, rmiss)
  implicit none
  real,dimension(nz)             :: r1lev
  real                              rPsfc, findiz_btm, rmiss
  integer                           iz,nz
!
do iz = 1, nz
  if(-r1lev(iz) > -rPsfc ) then
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
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
FUNCTION findiz_scnd_jo( nz, r1sig_jo, rPlcl, rPsfc )
  implicit none
  integer                          nz
  real,dimension(nz)           ::  r1sig_jo
  real                             rPlcl, rPsfc
  integer                          iz, findiz_scnd_jo
!
  real                             rsiglcl
! 
rsiglcl = rPlcl / rPsfc
do iz =1,nz*2
  if (r1sig_jo(iz) .lt. rsiglcl)then
    findiz_scnd_jo = iz
    exit
  elseif (iz .eq. nz) then
    findiz_scnd_jo = -9999
  end if
end do
RETURN
END FUNCTION findiz_scnd_jo

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
FUNCTION mk_r1wap_fillzero(nz, rTsfc, rqsfc, rPsfc, r1wap, r1lev)
  implicit none
  integer                          nz
  real                             rTsfc, rqsfc, rPsfc
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
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
FUNCTION mk_r1T_extend(nz, rTsfc, rqsfc, rPsfc, r1lev)
  implicit none
  integer                   nz
  real                      rTsfc, rqsfc, rPsfc
  real,dimension(nz)     :: r1lev
!-------------
  integer                   iz, iz_scnd
  real                      rPlcl, rTlcl
  real                      rT1, rT2, rP1, rP2
  real                   :: dP = 100.0          ![Pa]
  real,dimension(nz)     :: mk_r1T_extend
!------------------------------------------
! Extend the moist adiabatic temperature profile
! to the layers below LCL.
!------------------------------------------
!rPsfc   = Psea2Psfc(rTsfc, rqsfc, rzsfc, rPsea)
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
FUNCTION integral_WA_seg(dsig, rsigb, rsigt, rWb, rWt, rPsfc, rTb)
  implicit none
!-----------------------------------
real                             dsig
real                             rsigb, rsigt
real                             rWb, rWt
real                             rPsfc
real                             rTb
!------
integer                          isig, nsig
real                             dP, rPb, rPt, rdWdP
real                             rPnew, rWnew, rTnew
real                             rP, rT, rW, rdqdP, rdqdsig, rV
!------
real                             integral_WA_seg
!-----------------------------------
!np = int( (rP1-rP2)/dP )
nsig = int( (rsigb - rsigt) / dsig )
dP   = dsig * rPsfc
rPb  = rsigb * rPsfc
rPt  = rsigt * rPsfc
rdWdP = (rWb - rWt) / (rPb - rPt)
!--- initialize -------
rPnew = rsigb * rPsfc
rWnew = rWb
rTnew = rTb
!------------------------------------
do isig = 1, nsig
  rP = rPnew
  rT = rTnew
  rW = rWnew
  rdqdP = cal_rdqdP(rP, rT, dP)
  rdqdsig = rdqdP * rPsfc
  !
  rPnew = rP - dP
  rTnew = moistadiabat(rP, rT, rP-dP, dP)
  rWnew = rW - rdWdP * dP
  !
  if (rW .ge. 0.0) then
    rV = 0.0
  else
    rV = rW/rPsfc * rdqdsig
  endif
  integral_WA_seg = integral_WA_seg + rV * dsig
end do
!--- from rP = rP1 - dP*np  to rP =rP2 ----
rP = rPnew
rT = rTnew
rW = rWnew
rdqdP = cal_rdqdP(rP, rT, dP)
if (rW .ge. 0.0) then
  rV = 0.0
else
  rV = rW/rPsfc * rdqdsig
endif
!print *,"P, W, dqdP", rP, rW, rdqdP
!print *," (rP1 - rP2) - dP*np )", (rP1 - rP2) - dP*np 
integral_WA_seg = integral_WA_seg + rV * ( (rsigb - rsigt) - dsig*nsig ) 
!------------------------------------
integral_WA_seg = -integral_WA_seg
RETURN
END FUNCTION integral_WA_seg

!***************************************************
FUNCTION integral_dWA_seg(dsig, rsigb, rsigt, rWb1, rWb2, rWt1, rWt2, rPsfc1, rPsfc2, rTb1)
  ! integral from sigb to sigt
  implicit none
  !-----
  real                           dsig
  real                           rsigb, rsigt
  real                           rWb1, rWb2, rWt1, rWt2
  real                           rPsfc1, rPsfc2
  real                           rTb1
  !--for calculation---
  integer                        isig, nsig
  real                           dP1, dP2
  real                           rPb1, rPb2, rPt1, rPt2
  real                           rWnew1, rWnew2, rPnew1, rTnew1
  real                           rW1, rW2
  real                           rP1, rP2
  real                           rT1
  real                           rdWdP1, rdWdP2
  real                           rdqdP1, rdqdsig1
  real                           rV
  !-
  real                           integral_dWA_seg
  !-----------------------------------------------------
nsig = int( (rsigb-rsigt)/dsig)
dP1 = dsig * rPsfc1
dP2 = dsig * rPsfc2
rPb1 = rsigb * rPsfc1
rPb2 = rsigb * rPsfc2
rPt1 = rsigt * rPsfc1
rPt1 = rsigt * rPsfc2
rdWdP1 = (rWb1 - rWt1)/(rPb1 - rPt1)
rdWdP2 = (rWb2 - rWt2)/(rPb2 - rPt2)
!-- initialize ------
rWnew1 = rWb1
rWnew2 = rWb2
rPnew1 = rsigb*rPsfc1
rTnew1 = rTb1
!------------------------------------
do isig = 1, nsig
  rW1 = rWnew1
  rW2 = rWnew2
  rP1  = rPnew1
  rT1  = rTnew1
  rdqdP1 = cal_rdqdP(rP1, rT1, dP1)
  rdqdsig1 = rdqdP1*rPsfc1
  !
  rWnew1 = rW1 - rdWdP1 * dP1
  rWnew2 = rW2 - rdWdP2 * dP2
  rPnew1 = rP1 - dP1
  rTnew1 = moistadiabat(rP1, rT1, rP1-dP1, dP1)
  !
  if (rW1 .gt. 0.0) then
    rW1 = 0.0d0
  end if
  if (rW2 .gt. 0.0) then
    rW2 = 0.0d0
  end if
  rV = (dble(rW2)/rPsfc2 - dble(rW1)/rPsfc1) * (rdqdsig1)
  integral_dWA_seg = integral_dWA_seg + rV * dsig
end do
!--- from rsig = rsigb - dsig*nsig  to rsig = rsigt ----
rW1 = rWnew1
rW2 = rWnew2
rP1 = rPnew1
rT1 = rTnew1
rdqdP1 = cal_rdqdP(rP1, rT1, dP1)
rdqdsig1 = rdqdP1 * rPsfc1
if (rW1 .gt. 0.0) then
  rW1 = 0.0d0
end if
if (rW2 .gt. 0.0) then
  rW2 = 0.0d0
end if
rV = (dble(rW2)/rPsfc2 - dble(rW1)/rPsfc1) * rdqdsig1
integral_dWA_seg = integral_dWA_seg + rV * ( (rsigb - rsigt) -  dsig*nsig )
!*** double --> real ******
integral_dWA_seg = real(integral_dWA_seg)
!------------------------------------
integral_dWA_seg = -integral_dWA_seg
integral_dWA_seg = rPsfc1 * integral_dWA_seg
RETURN
END FUNCTION integral_dWA_seg
!****************************************************

FUNCTION integral_WdA_seg(dsig, rsigb, rsigt, rWb1, rWt1, rPsfc1, rPsfc2, rTb1, rTb2)
  implicit none
!-----------------------------------
real                            dsig
real                            rsigb, rsigt
real                            rWb1, rWt1
real                            rPsfc1, rPsfc2
real                            rTb1, rTb2
!
integer                         isig, nsig
real                            dP1, dP2
real                            rsigb1, rsigb2
real                            rPb1, rPb2, rPt1, rPt2, rPnew1, rPnew2
real                            rP1, rP2
real                            rsig1, rsig2
real                            rT1, rT2, rTnew1, rTnew2
real                            rW1, rWnew1
real                            rdwdp1
real                            rdqdP1, rdqdP2, rdqdsig1, rdqdsig2
real                            rV
!
real                            integral_WdA_seg
!-----------------------------------
!np = int( (rP1-rP2)/dP )
nsig = int( (rsigb - rsigt) /dsig )
dP1  = dsig * rPsfc1
dP2  = dsig * rPsfc2
rPb1 = rsigb1 * rPsfc1
rPb2 = rsigb2 * rPsfc2
!--- initialize -------
rdWdP1 = (rWb1 - rWt1)/(rPb1 - rPt1)
rWnew1 = rWb1
rPnew1 = rPb1
rPnew2 = rPb2
rTnew1 = rTb1
rTnew2 = rTb2
!------------------------------------
do isig = 1, nsig
  rP1 = rPnew1
  rP2 = rPnew2
  rT1 = rTnew1
  rT2 = rTnew2
  rW1 = rWnew1
  rdqdP1 = cal_rdqdP(rP1, rT1, dP1)
  rdqdP2 = cal_rdqdP(rP2, rT2, dP2)
  rdqdsig1 = rdqdP1 * rPsfc1
  rdqdsig2 = rdqdP2 * rPsfc2
  !
  rPnew1 = rP1 - dP1
  rPnew2 = rP2 - dP2
  rTnew1 = moistadiabat(rP1, rT1, rP1 -dP1, dP1)
  rTnew2 = moistadiabat(rP2, rT2, rP2 -dP2, dP2)
  rWnew1  = rW1 - rdWdP1 * dP1
  !
  if (rW1 .ge. 0.0) then
    rV = 0.0
  else
    rV = rW1 /rPsfc1 * (rdqdsig2 - rdqdsig1)
  endif
  integral_WdA_seg = integral_WdA_seg + rV * dsig
end do
!--- from rP = rP1 - dP*np  to rP =rP2 ----
rP1 = rPnew1
rP2 = rPnew2
rT1 = rTnew1
rT2 = rTnew2
rW1 = rWnew1
rdqdP1 = cal_rdqdP(rP1, rT1, dP1)
rdqdP2 = cal_rdqdP(rP2, rT2, dP2)
rdqdsig1 = rdqdP1 * rPsfc1
rdqdsig2 = rdqdP2 * rPsfc2
!
if (rW1 .ge. 0.0) then
  rV = 0.0d0
else
  rV = rW1 /rPsfc1 * (rdqdsig2 - rdqdsig1)
endif
integral_WdA_seg = integral_WdA_seg + rV * ( (rsig1 - rsig2) - dsig*nsig ) 
!-----------------------------------a
integral_WdA_seg = -integral_WdA_seg
integral_WdA_seg = rPsfc1 * integral_WdA_seg
RETURN
END FUNCTION integral_WdA_seg
!****************************************************


END PROGRAM dtanl_merra

