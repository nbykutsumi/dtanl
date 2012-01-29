program cal_nth
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!to calculate Nth percentile of time series for grid data
!by N.Utsumi
!at IIS, UT
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! parameter
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
implicit none
!
character*256   cidir_root1, cidir_root2, cidir_root
character*256   codir_root
character*256   cidir, codir
character*256   ciname_head, coname_head
character*256   ciname_tail, coname_tail
character*256   ciname
character*256   coname, coname_up, coname_low
character*256   cpercent, cpercent_up, cpercent_low
character*4     cyear, ciyear, ceyear
character*2     cmon, cday, cimon, cemon
character*10    cidate
character*5     cnx, cny
!
integer, allocatable,dimension(:) ::  i1mons    ! array of months
integer                               ilenmon   ! length of ilmons
real, allocatable,dimension(:,:)  ::  r2ipr
real, allocatable,dimension(:)    ::  r1ipr
real, allocatable,dimension(:,:)  ::  r2stck    ! data stock
real, allocatable,dimension(:,:)  ::  r2out     ! Xth percentiles
real, allocatable,dimension(:,:)  ::  r2out_up  ! Xth percentiles upper boundary
real, allocatable,dimension(:,:)  ::  r2out_low ! Xth percentiles lower boundary
!
real                                  rpercent, rpercent_up, rpercent_low

integer                               nx,ny
integer                               ix,iy, ixx,iyy
integer                               im     ! for mon loop
integer                               year, mon, day
integer                               iyear, imon, iday
integer                               eyear, emon, eday
!
integer                               io
!
integer                               itimes, ntimes  ! length of timeseries 
integer                               itmp
real                                  rtmp
!real                                  r1tmp(10)
!real                                  r1tmp900(900)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
print *,ciname
ny = 96
nx = 144
iyear = 1990
eyear = 1992
imon  = 1
emon  = 12
rpercent = 34.0  ! shold be more than 34.0
!****************************************************
!* Get variables from standard input
!****************************************************
if (iargc().lt.10) then
  print *, "Usage: iyear, eyear, imon, emon, cidir_root, ciname_head, codir, coname_head, nx, ny, rpercent"
  stop
endif
!
call getarg(1, ciyear)
call getarg(2, ceyear)
call getarg(3, cimon)
call getarg(4, cemon)
call getarg(5, cidir_root)
call getarg(6, ciname_head)
call getarg(7, codir)
call getarg(8, coname_head)
call getarg(9, cnx)
call getarg(10, cny)
call getarg(11,cpercent)
!
!** character -> number
read(ciyear,*) iyear
read(ceyear,*) eyear
read(cimon ,*) imon
read(cemon ,*) emon
read(cnx   ,*) nx
read(cny   ,*) ny
read(cpercent,*) rpercent
!****************************************************
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!cidir_root1     = "/media/disk2/data/CMIP5/bn"
!cidir_root2     = "/pr/day/NorESM1-M/historical/r1i1p1"
!cidir_root      = trim(cidir_root1) // trim(cidir_root2) 
!ciname_head    = "pr_day_NorESM1-M_historical_r1i1p1_"
!ciname_tail    = "1990010100.bn"
!ciname         = trim(cidir) // "/" // trim(ciname_head) // trim(ciname_tail)
!****************************************************
! set output file name
!****************************************************
!codir_root  = "/media/disk2/out/CMIP5/day/NorESM1-M/historical/r1i1p1/prxth"
write(ciyear, "(i4)"  ) iyear
write(ceyear, "(i4)"  ) eyear
write(cimon , "(i2.2)") imon
write(cemon , "(i2.2)") emon
write(cpercent, "(f0.2)") rpercent
!!!!!!!!!!!!!!!!!!!!!!!!!!!
if (len_trim(cpercent) .eq. 4) then
  cpercent = "00"//trim(cpercent)
else if (len_trim(cpercent) .eq. 5) then
  cpercent = "0"//trim(cpercent)
endif
print *,trim(cpercent)
!!!!!!!!!!!!!!!!!!!!!!!!!!!
!codir = trim(codir_root)//"/"//ciyear//"-"//ceyear//"/"//cimon//"-"//cemon
!coname_head   = "prxth_day_NorESM1-M_historical_r1i1p1"
coname_head = trim(codir)//"/"//trim(coname_head)//"_"//cpercent
coname      = trim(coname_head) // ".bn"
coname_low  = trim(coname_head) // "_lw.bn"
coname_up   = trim(coname_head) // "_up.bn"
print *,coname_low
!****************************************************
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! allocate array size
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
allocate( r2ipr(nx,ny))
allocate( r1ipr(ny))
allocate( r2out(nx,ny), r2out_low(nx,ny), r2out_up(nx,ny))
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! make i1mons
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
ilenmon = lenmon(imon, emon) 
allocate( i1mons(ilenmon))
i1mons = MKI1MONS(imon, emon, ilenmon)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! allocate r2stck
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
ntimes = MKNTIMES(iyear, eyear, ilenmon, i1mons)
allocate( r2stck(ntimes, nx) )
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! set rpercent_up, rpercent_low
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
if ( rpercent .ge. 99.0) then
  rpercent_low = (100. - 3./2.*(100. - rpercent))
  rpercent_up  = (100. - 1./2.*(100. - rpercent))
else
  rpercent_low  =  rpercent - 1.0
  rpercent_up  =  rpercent + 1.0
endif
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
do iy = 1, ny    ! latitude loop
  !********************************************************
  !* make data for calculation
  !********************************************************
  itimes = 0
  do year = iyear, eyear
    write( cyear, "(i4)") year
    do  im= 1, ilenmon
      mon = i1mons(im)
      write( cmon, "(i2.2)") mon
      do day = 1, NUMDAYS_NOLEAP(mon) 
        write( cday, "(i2.2)") day
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ! name of the input file
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        cidir       = trim(cidir_root) // "/" // trim(cyear)
        cidate      = cyear // cmon // cday // "00"
        ciname_tail = cidate // ".bn"
        ciname      = trim(cidir) // "/" // trim(ciname_head)//"_"//trim(ciname_tail)
        !print *,ciname
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        ! open and read input file
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        open(11, file = ciname, access="DIRECT", status="old", recl = nx, IOSTAT=io)
        !! check the existence of input file 
        if(io.gt.0)then
          print *, "no file", ciname
        end if
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        itimes = itimes + 1
        read(11, rec=iy) ( r2stck( itimes, ix ), ix =1,nx )
        close(11)
        !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      enddo
    enddo
  enddo
  !********************************************************
  !* estimate percentile
  !********************************************************
  do ix = 1,nx    
    r2out(ix, iy) =percentile( r2stck(:, ix), ntimes, rpercent)
    r2out_low(ix, iy) =percentile( r2stck(:, ix), ntimes, rpercent_low)
    r2out_up(ix, iy) =percentile( r2stck(:, ix), ntimes, rpercent_up)
  enddo
enddo
print *,rpercent_low, rpercent, rpercent_up
print *,r2out_low(10,5), r2out(10,5),r2out_up(10,5)
!*******************************************************! write to output file
!*******************************************************
open(12, file=coname,     access="direct", recl=nx)
open(13, file=coname_low, access="direct", recl=nx)
open(14, file=coname_up,  access="direct", recl=nx)
do iy = 1,ny
  write(12, rec=iy) (r2out(ix,iy)    , ix=1,nx)
  write(13, rec=iy) (r2out_low(ix,iy), ix=1,nx)
  write(14, rec=iy) (r2out_up(ix,iy) , ix=1,nx)
  
enddo   
close(12)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
!
contains
  !*****************************************************
  !*  Sorts an array RA of length N in ascending order *
  !*                by the Heapsort method             *
  !* taken from:
  !* http://jean-pierre.moreau.pagesperso-orange.fr/fortran.html
  !* modified by: N.Utsumi
  !* ------------------------------------------------- *
  !* INPUTS:                                           *
  !*	    N	  size of table RA                   *
  !*        RA	  table to be sorted                 *
  !* OUTPUT:                                           *
  !*	    RA    table sorted in ascending order    *
  !*                                                   *
  !* NOTE: The Heapsort method is a N Log2 N routine,  *
  !*       and can be used for very large arrays.      *
  !*****************************************************         
  SUBROUTINE HPSORT(N,RA)
    implicit none
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    integer    N
    real       RA(N)
    real       RRA
    integer    L, I, J, IR
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    L=N/2+1
    IR=N
    !The index L will be decremented from its initial value during the
    !"hiring" (heap creation) phase. Once it reaches 1, the index IR 
    !will be decremented from its initial value down to 1 during the
    !"retirement-and-promotion" (heap selection) phase.
  10 continue
    if(L > 1)then
      L=L-1
      RRA=RA(L)
    else
      RRA=RA(IR)
      RA(IR)=RA(1)
      IR=IR-1
      if(IR.eq.1)then
        RA(1)=RRA
        return
      end if
    end if
    I=L
    J=L+L
  20 if(J.le.IR)then
    if(J < IR)then
      if(RA(J) < RA(J+1))  J=J+1
    end if
    if(RRA < RA(J))then
      RA(I)=RA(J)
      I=J; J=J+J
    else
      J=IR+1
    end if
    goto 20
    end if
    RA(I)=RRA
    goto 10
    !!!!!
  END SUBROUTINE HPSORT
  !*****************************************************
  !* calculate percentile
  !*
  !* L   Length of data in array
  !* RA  input array
  !* percent  : XX %
  !* precentile  : XXth percentile value
  !*
  !*****************************************************
  REAL FUNCTION PERCENTILE(R1, L, percent)
    implicit none
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    integer    L
    integer    ii, n, n_up, n_low
    real       percent
    real       precentile
    real       R1(L)
    real       CRF, CRF_up, CRF_low
    real       x, x_up, x_low
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    call HPSORT(L, R1)
    percentile = R1(1)
    n = int(floor(L*percent*0.01) +1)
    if (n*1.0 .eq. L*percent*0.01 +1.0) then
      percentile = R1(n-1)
    else
      if (L < n) then
        n_up = n-1
      else
        n_up = n
      endif
      n_low= n-1

      !n = int(floor(L*percent*0.01) +1)
      !if (L < n) then
      !  n_up =L
      !else if ( R1(n-1)*1.0 < R1(n)*1.0 ) then
      !  n_up = n
      !else if ( R1(n-1)*1.0 .eq. R1(n)*1.0 ) then
      !  do ii = n, L
      !    if (ii .eq. L) then
      !      n_up = L
      !    else if ( R1(ii)*1.0 < R1(ii+1)*1.0 ) then
      !      n_up = ii
      !      exit
      !    endif
      !  enddo
      !endif 
      !do ii = n-1, 1,-1
      !  if ( R1(ii)*1.0 < R1(n)*1.0) then
      !    n_low = ii
      !    exit
      !  elseif (ii .eq.1) then
      !    n_low = 0
      !  endif
      !enddo
      CRF = percent*0.01   ! Cummulative Relative Frequency
      CRF_up = (n_up*1.0) / ( L*1.0)
      x_up = R1(n_up)
      if (n_low .ne. 0) then
        CRF_low = (n_low*1.0) / (L*1.0)
        x_low = R1(n_low)
      else
        CRF_low = 0.0
        x_low = 0.0
      endif
      percentile = x_low + (x_up - x_low) * (CRF -CRF_low) / (CRF_up - CRF_low)
  endif
  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
  END FUNCTION PERCENTILE
  !*****************************************************
  !*
  !* calculate the number of days in a month
  !*
  !*****************************************************
  INTEGER FUNCTION NUMDAYS_NOLEAP(MON)
    implicit none
    integer          mon
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if ((mon .eq. 1).or.(mon .eq. 3).or.(mon .eq. 5).or.(mon .eq. 7)&
      &.or.(mon .eq. 8).or.(mon .eq. 10).or.(mon .eq. 12)) then
      numdays_noleap = 31
    else if ((mon .eq. 4) .or. (mon .eq. 6)&
      & .or. (mon .eq. 9) .or. (mon .eq. 11)) then
      numdays_noleap = 30
    else if (mon .eq. 2) then
      numdays_noleap = 28
    end if
  END FUNCTION NUMDAYS_NOLEAP
  !*****************************************************
  !*
  !* calculate the number of months in a year
  !*
  !*****************************************************
  INTEGER FUNCTION LENMON(imon,emon)
    implicit none
    integer            imon, emon
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if (imon .le. emon) then
      lenmon = emon - imon +1
    else if (emon .lt. imon) then
      lenmon = (12+emon) -imon + 1
    endif
  END FUNCTION LENMON
  !*****************************************************
  !*
  !* calculate the number of months in a year
  !*
  !*****************************************************
  FUNCTION MKI1MONS(imon, emon, ilenmon)
    implicit none
    integer    i, ii
    integer    imon, emon, ilenmon
    integer    mki1mons(ilenmon)
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if (imon .le. emon) then
      do ii = 1, ilenmon
        mki1mons(ii) = imon + ii -1
      enddo
    else if (emon .lt. imon) then
      do ii = 1, ilenmon
        if (ii .le. emon) then  ! ii = 1,2,..emon
          mki1mons(ii) = ii
        else if (emon .lt. ii) then ! ii = emon+1, emon+2,..12
          mki1mons(ii) = imon + (ii - emon) -1
        endif
      enddo
    endif
  END FUNCTION MKI1MONS
  !*****************************************************
  !*
  !* calculate the number of all timesteps
  !*
  !*****************************************************
  INTEGER FUNCTION MKNTIMES(iyear, eyear, ilenmon, i1mons)
    implicit none
    integer          iyear, eyear, ilenmon
    integer          i1mons(ilenmon)
    integer          ii
    integer          mon
    integer          numdays_noleap
    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    mkntimes = 0
    do ii = 1, ilenmon
      mon = i1mons(ii)
      !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      if ((mon .eq. 1).or.(mon .eq. 3).or.(mon .eq. 5).or.(mon .eq. 7)&
        &.or.(mon .eq. 8).or.(mon .eq. 10).or.(mon .eq. 12)) then
        numdays_noleap = 31
      else if ((mon .eq. 4) .or. (mon .eq. 6)&
        & .or. (mon .eq. 9) .or. (mon .eq. 11)) then
        numdays_noleap = 30
      else if (mon .eq. 2) then
        numdays_noleap = 28
      end if
      !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      mkntimes = mkntimes + numdays_noleap
  enddo
  mkntimes = mkntimes * (eyear - iyear +1) 
  END FUNCTION MKNTIMES 
  !*****************************************************
end program cal_nth

