      program SI_id
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!to   Spatial Interpolation with inverse distance method
!by   n.utsumi
!at   IIS, UT
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!     parameter
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      implicit none

      integer                nx,ny
      integer                nx_dec, ny_dec
      parameter              (nx_dec=250,ny_dec=220)
      integer                nx_5cnt, ny_5cnt
      parameter              (nx_5cnt=500,ny_5cnt=440)
      integer                nx_cnt, ny_cnt
      parameter              (nx_cnt=2500,ny_cnt=2200)
!
      real                   rdem_miss
      parameter              (rdem_miss=-999)
      real                   ridat_miss
      parameter              (ridat_miss=-999)
      real                   rout_miss
      parameter              (rout_miss=-999)
      real*8                 dlon_base,dlat_base
      parameter              (dlon_base=123.0d0)
      parameter              (dlat_base=46.0d0)
!
!
      real*8                 dpi
      parameter              (dpi=3.141592d0)
!
      integer                irad         !radius for station search
!      parameter              (irad=80)    ! [km] for cnt
      parameter              (irad=150.)    ![km] 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      integer                i,iy,ix
      integer                ilen,jstart,is
      integer                io
      real                   rtemp
      real*8                 dresol,dlat,dlon,drad_lon
      real*8                 wt,swt

      integer,allocatable::  iobs_x(:),iobs_y(:)
      real,allocatable::     ridat(:)
      real,allocatable::     robs_dat(:)
      real*8,allocatable::   dilon(:),dilat(:)
      real*8,allocatable::   dobs_lon(:),dobs_lat(:),dobs_L(:)

      real,allocatable::     rodat(:,:)  ! output data
      real,allocatable::     rDEM(:,:)
      character*128  cifname
      character*128  cofname
      character*128  cdem
      character*128  cresol
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! Get file name
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!
      if (iargc().lt.4) then
         write(*,*) "Usage: cmd [in list] [DEM] [out] [resol]"
         write(*,*) '[resol] 0.1deg: "dec", 0.05deg: "5cnt", 0.01deg: "cnt" '
         stop
      end if
!
      call getarg(1,cifname)
      call getarg(2,cdem)
      call getarg(3,cofname)
      call getarg(4,cresol)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! Check timestep
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      if(cresol.eq."dec")then
          nx=nx_dec
          ny=ny_dec
          dresol=0.1
      elseif(cresol.eq."5cnt")then
          nx=nx_5cnt
          ny=ny_5cnt
          dresol=0.05
      elseif(cresol.eq."cnt")then
          nx=nx_cnt
          ny=ny_cnt
          dresol=0.01
      else
          write(*,*) 'Caution!! [resol] 0.1deg: "dec", 0.05deg: "5cnt", 0.01deg: "cnt" '
          write(*,*) 'you set [resol]=',cresol
          stop
      endif

!     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!     Allocate variables with (nx,ny)
!     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      allocate(rodat(1:nx,1:ny))  ! output data
      allocate(rDEM(1:nx,1:ny))

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! Read List
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!     Count list length
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      io=0
      open(11,file=cifname,access="sequential",status='old',IOSTAT=io)
      if(io.gt.0)then
          write(*,*) "no file: ",cifname
          stop
      endif
      ilen=0
      io=0
      do while(io.ge.0)
        ilen=ilen+1
        read(11,*,IOSTAT=io)
      end do
      ilen=ilen -1

!     !!!!!!!!!!!!!!!!!!!!!!!!!!!!
!     Allocate variables
!     !!!!!!!!!!!!!!!!!!!!!!!!!!!!
      allocate(dilon(1:ilen))
      allocate(dilat(1:ilen))
      allocate(ridat(1:ilen))
!
      allocate(iobs_x(1:ilen))
      allocate(iobs_y(1:ilen))
      allocate(dobs_lon(1:ilen))
      allocate(dobs_lat(1:ilen))
      allocate(dobs_L(1:ilen))
      allocate(robs_dat(1:ilen))


!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      rewind 11
      do i=1,ilen
        read(11,*) dilon(i),dilat(i),ridat(i)
      enddo
      close(11)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! Read DEM map
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      open(13,file=cdem,status="old",access="DIRECT", recl=nx*4)
      do iy=1,ny
        read(13, rec=iy) (rDEM(ix,iy), ix=1,nx)
      enddo
      close(13)

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! Set estimation point on grid map
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      dlat=dlat_base +dresol-dresol/2.0d0    ! set initial latitude
      do iy=1,ny
        dlon=dlon_base -dresol  + dresol/2.0d0      ! set initial longitude
        dlat=dlat - dresol
!
!       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        CALL calc_drad_lon(dlat,dpi,irad,drad_lon)
!       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        jstart =1           ! for SUBROUTINE s_search()
!       !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        do ix=1,nx
          dlon=dlon + dresol
!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! If the point(nx,ny) is SEA...
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
          if(rdem(ix,iy).eq.rdem_miss)then
!
            rodat(ix,iy)=rout_miss
            CYCLE       ! skip to next ix
!
          endif
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! Station Search
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
          CALL s_search(dlon,dlat &
                       ,dpi       &
                       ,ridat_miss &
                       ,ilen      &
                       ,jstart    &
                       ,irad      &
                       ,drad_lon  &
                       ,dilon,dilat,ridat&
                       ,iobs_x,iobs_y,robs_dat&
                       ,dobs_lon, dobs_lat&
                       ,dlon_base,dlat_base &
                       ,dresol &
                       ,is     &
                       ,dobs_L)

          rtemp=0.
          do i=1,is
            rtemp=rtemp + robs_dat(i)
          enddo
          if(rtemp.eq.0.0)then
            rodat(ix,iy)=0.0
            CYCLE
          endif
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! Inverse-distance interpolation
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
          swt=0.0
          rtemp=0.0
          do i=1,is
            wt=1.0/(dobs_L(i)**2.0)
            swt=swt + wt
            rtemp=rtemp + robs_dat(i)*wt
          enddo
          rodat(ix,iy)=real(rtemp/swt)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        end do    !<---------- ix
      end do      !<---------- iy

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! write output grid data
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      open(13, file=cofname, access='direct', recl=nx*4)
      do iy=1,ny
        write(13,rec=iy) (rodat(ix,iy),ix=1,nx)
      end do
      close(13)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      deallocate(dilon)
      deallocate(dilat)
      deallocate(ridat)
!
      deallocate(iobs_x)
      deallocate(iobs_y)
      deallocate(dobs_lon)
      deallocate(dobs_lat)
      deallocate(robs_dat)
      deallocate(dobs_L)
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      END     ! <-------------------end of main program.

!***********************************************************************
!***********************************************************************

! SUBROUTINE calc_drad_lon

!***********************************************************************
!***********************************************************************
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      SUBROUTINE calc_drad_lon(dlat,dpi,irad1,drad_lon1)
!
      implicit none
!
      integer             irad1
      real*8              dpi
      real*8              dlat
      real*8              drad_lon1_radian
      real*8              drad_lon1                ![degree]
      real*8              dlat_radian
!     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      dlat_radian =dlat/180 *dpi

      drad_lon1_radian=irad1*1000 &
                *sqrt(1-0.006674d0*sin(dlat_radian)*sin(dlat_radian))&
                /6377397 / cos(dlat_radian)
      drad_lon1=drad_lon1_radian /dpi *180
!
      END SUBROUTINE calc_drad_lon
!***********************************************************************
!***********************************************************************
!***********************************************************************
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
! SUBROUTINE s_search
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!***********************************************************************
!***********************************************************************
      SUBROUTINE s_search(dlon,dlat &
                       ,dpi       &
                       ,ridat_miss &
                       ,ilen      &
                       ,jstart    &
                       ,irad      &
                       ,drad_lon  &
                       ,dilon,dilat,ridat&
                       ,iobs_x,iobs_y,robs_dat&
                       ,dobs_lon, dobs_lat&
                       ,dlon_base,dlat_base &
                       ,dresol &
                       ,is     &
                       ,dobs_L)
      implicit none
!
      integer             ilen
      integer             j,k
      integer             jstart,ju,jl,jm
      integer             irad
      integer             iobs_x(1:ilen)
      integer             iobs_y(1:ilen)
      integer             is
      real*8              dlon
      real*8              dlat
      real*8              dilon(1:ilen)
      real*8              dilat(1:ilen)
      real                ridat(1:ilen)
      real                robs_dat(1:ilen)
      real*8              dobs_L(1:ilen)
      real*8              dobs_lon(1:ilen), dobs_lat(1:ilen)
!
      real*8              dpi
      real                ridat_miss
      real*8              dlon_base, dlat_base
      real*8              dresol
      real*8              drad_lon               ! [degree]
      real*8              dlon_min1,dlon_max1
      real*8              dL,dap,dp,dr,dm,dn       ! for Hubeny's method
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
      dlon_min1= dlon -drad_lon
      dlon_max1= dlon +drad_lon
      jl=jstart
      ju=ilen
      do while(ju-jl.gt.1)
        jm=(ju+jl)/2
        if(dilon(jl).gt.dlon_min1)then
            exit
        else if( dilon(jm).ge.dlon_min1 )then
          ju=jm
        else
          jl=jm
        endif
      end do
!
      jstart=jl
!
      k=0
      do j=jstart,ilen
        if(dilon(j).gt.dlon_max1)then
          EXIT
        else if(ridat(j).eq.ridat_miss)then
          CYCLE
        endif
!     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!      Hubeny's method
!     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        dap=(dlat+dilat(j))/2/180*dpi
        dp=(dlat-dilat(j))/180.0*dpi
        dr=(dlon-dilon(j))/180.0*dpi

        dm=6334834/sqrt((1.00-0.006674d0*sin(dap)*sin(dap))**3.00)
        dn=6377397/sqrt(1.00-0.006674d0*sin(dap)*sin(dap))

        dL=sqrt((dm*dp)**2.00+(dn*cos(dap)*dr)**2.00)
        dL=dL/1000.000             ! [km]
!     !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if(dL.le.irad)then
          k=k+1
          iobs_x(k)= AINT( (dilon(j)-dlon_base) /dresol ) +1
          iobs_y(k)= AINT( (dlat_base-dilat(j)) /dresol ) +1
          robs_dat(k)=ridat(j)
          dobs_L(k)=dL
          dobs_lat(k)=dilat(j)
          dobs_lon(k)=dilon(j)
        endif
      end do
      is=k                    ! the number of stations in circle
!
      END SUBROUTINE s_search

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

