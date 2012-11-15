! ====================================================================
!  read_v1101.f90
!   Sample program to read APHRODITE V1101 prodct,
!   displaying the time series at the center of MA/ME/RU domain
! ====================================================================
program main

  implicit none

  ! =======================================================
  !  User-specified variables
  ! =======================================================
  character(*),parameter :: dir='./'          ! Directory where data stored
  character(*),parameter :: prod='MA_025deg'  ! In XX_YYYdeg, XX is MA, ME, or RU, YY is 025 or 050.
  character(*),parameter :: ver='V1101'     ! Version of APHRODITE
  integer,parameter      :: year=2001         ! Year to be read


  ! -------------------------------------------------------
  !  Local variables
  ! -------------------------------------------------------
  character(256) :: fname
  integer :: nx, ny
  real(4),allocatable :: prcp(:,:), rstn(:,:)
  integer :: nday, iday
  logical :: exist


  ! -------------------------------------------------------
  !  Allocate arrays
  ! -------------------------------------------------------
  select case( prod )
  case('MA_025deg')
    nx = 360
    ny = 280
  case('MA_050deg')
    nx = 180
    ny = 140
  case('ME_025deg')
    nx = 180
    ny = 120
  case('ME_050deg')
    nx =  90
    ny =  60
  case('RU_025deg')
    nx = 720
    ny = 200
  case('RU_050deg')
    nx = 360
    ny = 100
  case default
    stop 'ERROR: Invalid product specified.'
  end select
  allocate( prcp(nx,ny), rstn(nx,ny) )


  ! -------------------------------------------------------
  !  Check leap year
  ! -------------------------------------------------------
  if( (mod(year,4) == 0 .and. mod(year,100) /= 0 ) &
       & .or. mod(year,400) == 0 ) then
    nday = 366
  else
    nday = 365
  end if


  ! -------------------------------------------------------
  !  Open input file
  ! -------------------------------------------------------
  write(fname,'(2a,i4)') dir, '/APHRO_'//prod//'_'//ver//'.', year
  inquire(file=trim(fname),exist=exist)
  if( .not. exist ) then
    write(6,*) 'ERROR: File not found - '//trim(fname)
    stop
  end if
  write(6,'(a)') 'Reading: '//trim(fname)
  open(31, file=trim(fname), access='direct', form='unformatted', recl=4*2*nx*ny)


  ! =======================================================
  !  ADD YOUR ANALYSIS HERE
  ! =======================================================
  write(6,'(a4,2a8)') 'iday', 'precip', 'rstn'
  do iday=1, nday
    read(31, rec=iday) prcp, rstn
    write(6,'(i4,2f8.2)') iday, prcp(nx/2,ny/2), rstn(nx/2,ny/2)
  end do
  ! =======================================================
  !  ADD YOUR ANALYSIS HERE
  ! =======================================================


  close(31)
  deallocate( prcp, rstn )

end program main
