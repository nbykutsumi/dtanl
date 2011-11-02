PROGRAM conditional_means
!----------------------------------------------------------------
implicit none
!
character*1000                        clistfile_var, clistfile_pr, cpr_lw, cpr_up, coname
character*128                        cnx, cny, cnz
character*1000                       ciname_var, ciname_pr
real,allocatable,dimension(:,:)   :: r2pr, r2pr_lw, r2pr_up
real,allocatable,dimension(:,:,:) :: r3in
real,allocatable,dimension(:,:,:) :: r3stck, r3count,r3mean
integer                              nx, ny, nz, ix, iy, iz
integer                              ik
!
real                                 rtemp
!** parameter ***
real,parameter                    :: dP = 1000 ![Pa], not [hPa]
real,parameter                    :: rmiss = -9999.0
!***********************************************************
!--------------------------------------------------
! Get filenames
!--------------------------------------------------
if (iargc().lt.8) then
  print *, "Usage: cmd [listfile_var] [listfile_pr] [ifile_prxth_lw] [ifile_prxt_up] [oname] [nx] [ny] [nz]"
  stop
endif
!
call getarg(1, clistfile_var)
call getarg(2, clistfile_pr)
call getarg(3, cpr_lw)
call getarg(4, cpr_up)
call getarg(5, coname)
call getarg(6, cnx)
call getarg(7, cny)
call getarg(8, cnz)
read(cnx, *) nx
read(cny, *) ny
read(cnz, *) nz
!--------------------------------------------------
allocate( r2pr(nx,ny) )
allocate( r2pr_lw(nx,ny) )
allocate( r2pr_up(nx,ny) )
allocate( r3in(nx,ny,nz) )
!
allocate( r3stck(nx,ny,nz) )
allocate( r3count(nx,ny,nz) )
allocate( r3mean(nx,ny,nz) )
!--------------------------------------------------
! set initial value
!--------------------------------------------------
r3stck  = 0.0
r3count = 0.0
!--------------------------------------------------
! read files : precipitation files (upper & lower) :2D files
!--------------------------------------------------
open(11, file = cpr_lw, access="DIRECT", status="old", recl =nx)
open(12, file = cpr_up, access="DIRECT", status="old", recl =nx)
do iy =1, ny
  !-----
  read(11, rec=iy) ( r2pr_lw(ix,iy) , ix=1, nx)
  read(12, rec=iy) ( r2pr_up(ix,iy) , ix=1, nx)
  !-----
enddo
close(11)
close(12)
!-------------------------------------------------
! read files : 1D files
!-------------------------------------------------
open(21, file=clistfile_var, status="old")
open(22, file=clistfile_pr,  status="old")
do
  read(21, '(A)',end =100) ciname_var
  read(22, '(A)',end =101) ciname_pr
  !-------------------------------------------------
  ! read files : precipitation of each time
  !-------------------------------------------------
  open(31, file = ciname_pr,   access="DIRECT", status="old", recl =nx)
  do iy=1, ny
    read(31, rec=iy) (r2pr(ix,iy) , ix=1, nx)
  enddo
  close(31)
  !-------------------------------------------------
  ! read files : 3D files
  !-------------------------------------------------
  open(32, file = ciname_var,   access="DIRECT", status="old", recl =nx)
  do iz=1, nz
    do iy=1, ny
      read(32, rec=(iz-1)*ny + iy) (r3in(ix,iy,iz) , ix=1, nx)
    enddo
  enddo
  close(32)

  !-------------------------------------------------
  ! filter
  !-------------------------------------------------
  do iy=1,ny
    do ix=1,nx
      if ((r2pr(ix,iy) .gt. r2pr_lw(ix,iy)) .and. (r2pr(ix,iy) .le. r2pr_up(ix,iy)) ) then
        r3stck(ix,iy,:) = r3stck(ix,iy,:) +r3in(ix,iy,:)
        r3count(ix,iy,:) = r3count(ix,iy,:) +1.0
      end if
    end do
  end do
  !-------------------------------------------------
enddo
100 close(21)
101 close(22)
r3mean = r3stck / r3count
!-------------------------------------------------
! write conditional mean data to the file
!-------------------------------------------------
open(41, file=coname, access="direct", recl=nx)
  do iz=1,nz
    do iy =1,ny
      write(41, rec=(iz-1)*ny +iy) (r3mean(ix,iy,iz) , ix=1,nx)
    end do
  end do
close(41)
!***********************************************************
END PROGRAM conditional_means

