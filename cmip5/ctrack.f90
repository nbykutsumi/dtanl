module ctrack

CONTAINS
!*****************************************************************
!* SUBROUTINE & FUNCTION
!*****************************************************************
!*****************************************************************
SUBROUTINE connectc(&
        &  a2pmean0, a2pmean1, a2psl0, a2psl1, a2ua0, a2va0&
        &, a2pmin0, a2ipos0, a2idate0, a2time0&
        &, a1lon, a1lat, thdp, thdist, hinc, miss_dbl, miss_int&
        &, year1, mon1, day1, hour1&
        &, a2lastpos1, a2pmin1, a2ipos1, a2idate1, a2time1&
        &, nx, ny)
  implicit none  
  !**************************************
  !** for input 
  !**************************************
  integer                                          nx, ny
  double precision,dimension(nx, ny)            :: a2pmean0, a2pmean1, a2psl0, a2psl1, a2ua0, a2va0
!f2py intent(in)                                   a2pmean0, a2pmean1, a2psl0, a2psl1, a2ua0, a2va0
  double precision,dimension(nx, ny)            :: a2pmin0
!f2py intent(in)                                   a2pmin0
  integer,dimension(nx,ny)                      :: a2ipos0, a2idate0, a2time0
!f2py intent(in)                                   a2ipos0, a2idate0, a2time0
  double precision,dimension(ny)                :: a1lat
!f2py intent(in)                                   a1lat
  double precision,dimension(nx)                :: a1lon
!f2py intent(in)                                   a1lon
  double precision                                 thdp, thdist
!f2py intent(in)                                   thdp, thdist
  integer                                          hinc
!f2py intent(in)                                   hinc
  double precision                                 miss_dbl
!f2py intent(in)                                   miss_dbl
  integer                                          miss_int
!f2py intent(in)                                   miss_int
  integer                                          year1, mon1, day1, hour1
!f2py intent(in)                                   year1, mon1, day1, hour1
  !**************************************
  !** for output 
  !**************************************
  double precision,dimension(nx,ny)             :: a2pmin1
!f2py intent(out)                                  a2pmin1
  integer,dimension(nx, ny)                     :: a2lastpos1, a2ipos1, a2idate1, a2time1
!f2py intent(out)                                  a2lastpos1, a2ipos1, a2idate1, a2time1
  !**************************************
  !** for calc 
  !**************************************
  integer                                          ix, iy, ix0, iy0, ix1, iy1, iix1, iiy1, iix, iiy, iix_loop, iiy_loop
  integer                                          ngrids, sgrids, xgrids, ygrids
  double precision                                 lat0, lon0, lat1, lon1
  double precision                                 ua0, va0, pmean0, psl0, dp0
  double precision                                 dp1
  double precision                                 londist, latdist
  double precision                                 dlat, dlon
  double precision                                 iilon, iilat, iipmean, iipsl
  double precision                                 iidist, iidp
  double precision                                 iidist_temp, iidp_temp
  double precision                                 dp
  integer                                          ik
  integer                                          xx, yy
  !integer,dimension(nx*ny)                      :: a1x, a1y
  integer                                          cflag
!------------------------------------------------------------
dlat  = a1lat(2) - a1lat(1)
dlon  = a1lon(2) - a1lon(1)
!************************************************
! initialize 
!------------------------------------------------
a2lastpos1 = miss_int
a2pmin1    = miss_dbl
a2ipos1    = miss_int
a2idate1   = miss_int
a2time1    = miss_int
!************************************************
! search cyclone same as previous timestep
!------------------------------------------------
do iy0 = 1, ny
  do ix0 = 1, nx
    if (a2pmean0(ix,iy) .ne. miss_dbl) then
      dp0 = a2pmean0(ix0,iy0) -a2psl0(ix0,iy0)
      if ( dp0 .gt. thdp ) then
        !-----------------
        lat0    = a1lat(iy0)
        lon0    = a1lon(ix0) 
        ua0     = a2ua0(ix0, iy0)
        va0     = a2va0(ix0, iy0)
        pmean0  = a2pmean0(ix0, iy0)
        psl0    = a2psl0(ix0, iy0)
        !-----------------
        londist = ua0 * 60d0 * 60d0 * hinc ! [m]
        latdist = va0 * 60d0 * 60d0 * hinc ! [m]
        ix1     = ix0 + longrids(lat0, dlon, londist)
        iy1     = iy0 + latgrids(lat0, dlat, latdist)
        call ixy2iixy(ix1, iy1, nx, ny, iix1, iiy1)
        ix1     = iix1
        iy1     = iiy1
        !****************************************
        ! search
        !----------------------------------------
        ! set range
        !***********
        lat1    = a1lat(iy1)
        lon1    = a1lon(ix1)
        call gridrange(lat1, dlat, dlon, thdist, ngrids, sgrids, xgrids)
        if (sgrids .ge. ngrids )then
          ygrids = sgrids
        else
          ygrids = ngrids
        end if
        !--
        !-----------
        ! search loop
        !***********
        iidist = 1.0e+20
        iidp   = -1.0e+20
        xx     = 0
        yy     = 0
        cflag  = 0
        do iix_loop = ix1 - xgrids, ix1 + xgrids
          do iiy_loop = iy1 - ygrids, iy1 + ygrids
            call ixy2iixy(iix_loop, iiy_loop, nx, ny, iix, iiy)
            iipmean = a2pmean1(iix, iiy)
            if (iipmean .ne. miss_dbl) then
              iipsl        = a2psl1(iix, iiy)
              iidp_temp    = iipmean - iipsl
              iilat        = a1lat(iiy)
              iilon        = a1lon(iix)
              if (iidp_temp .gt. thdp) then
                iidist_temp  = hubeny(lat1, lon1, iilat, iilon)
                if (iidist_temp .lt. iidist) then
                  cflag        = 1
                  iidist       = iidist_temp
                  iidp         = iidp_temp
                  iilon        = a1lon(iix)
                  iilat        = a1lat(iiy)
                  xx           = iix
                  yy           = iiy
                else if (iidist_temp .eq. iidist) then
                  if (iidp_temp .gt. iidp) then
                    cflag        = 1
                    iidist       = iidist_temp
                    iidp         = iidp_temp
                    iilon        = a1lon(iix)
                    iilat        = a1lat(iiy)
                    xx           = iix
                    yy           = iiy
                  end if
                end if
              end if 
            end if
          end do
        end do
        !-----
        if (cflag .eq. 1) then
          a2lastpos1(xx, yy) = nx * (iy0-1) + ix0
          if ( a2psl1(xx, yy) .lt. a2pmin0(xx, yy)) then
            a2pmin1(xx,yy)     = a2psl1(xx, yy)
          else
            a2pmin1(xx,yy)     = a2pmin0(xx, yy)
          end if
          a2ipos1(xx,yy)     = a2ipos0(ix0,iy0)
          a2idate1(xx,yy)    = a2idate0(ix0,iy0)
          a2time1(xx,yy)     = a2time0(ix0,iy0) + hinc
        end if
        !-----------------
      end if
    end if
  end do
end do
!************************************************
! search new cyclone
!------------------------------------------------
do yy = 1, ny
  do xx = 1, nx
    if (a2pmean1(xx,yy) .ne. miss_dbl) then
      if (a2lastpos1(xx,yy) .eq. miss_int) then
        dp1 = a2pmean1(xx,yy) - a2psl1(xx, yy) 
        if ( dp1 .gt. thdp )then
          a2pmin1(xx,yy)  = a2psl1(xx, yy)
          a2ipos1(xx,yy)  = (yy -1)*nx + xx
          a2idate1(xx,yy) = year1*10**6 + mon1*10**4 + day1*10**2 + hour1
          a2time1(xx,yy)  = 0
        end if
      end if
    end if
  end do
end do    
!a2lastpos1 = miss_int
!a2pmin1 = miss_dbl
!a2ipos1 = miss_int
!a2idate1= miss_int
!a2time1 = miss_int
!-----
RETURN
END SUBROUTINE connectc
!*****************************************************************
SUBROUTINE mk_a1xa1y(ix1, iy1, xgrids, ygrids, nx, ny, imiss, a1x, a1y)
  implicit none
  !-- for input -------------------
  integer                                       nx, ny
  integer                                       ix1, iy1
!f2py intent(in)                                ix1, iy1
  integer                                       xgrids, ygrids
!f2py intent(in)                                xgrids, ygrids
  integer                                       imiss
!f2py intent(in)                                imiss
  !-- for output ------------------
  integer,dimension(nx*ny)                   :: a1x, a1y
!f2py intent(out)                               a1x, a1y
  !-- for calc --------------------             
  integer                                       irad, nrad
  integer                                       iiy, iix
  integer                                       ik, ndat
!----------------------------------  
ndat = nx*ny
!**************
! initialize
!**************
do ik = 1, ndat
  a1x(ik) = imiss
  a1y(ik) = imiss
end do
ik = 0
!**************
! center grids
!--------------
iiy = iy1
iix = ix1
ik = ik +1
a1x(ik) = iix
a1y(ik) = iiy
!**************
if (ygrids .lt. xgrids) then
  nrad = ygrids
else
  nrad = xgrids
end if
do irad = 1, nrad
  !------
  iiy = iy1 + irad 
  do iix = ix1 - irad, ix1 + irad
    ik = ik +1
    a1x(ik) = iix
    a1y(ik) = iiy
  end do
  !------
  iiy = iy1 - irad
  do iix = ix1 - irad, ix1 + irad
    ik = ik +1
    a1x(ik) = iix
    a1y(ik) = iiy
  end do
  !------
  iix = ix1 - irad
  do iiy = iy1 - irad +1, iy1 + irad -1
    ik = ik +1
    a1x(ik) = iix
    a1y(ik) = iiy
  end do
  iix = ix1 + irad
  do iiy = iy1 - irad +1, iy1 + irad -1
    ik = ik +1
    a1x(ik) = iix
    a1y(ik) = iiy
  end do
  !------
end do
!**************
! extra grids
!--------------
if (ygrids .lt. xgrids) then
  do irad = ygrids+1, xgrids
    !-------
    iix = ix1 - irad
    do iiy = iy1 - ygrids, iy1 + ygrids
      ik = ik +1
      a1x(ik) = iix
      a1y(ik) = iiy
    end do
    !--------
    iix = ix1 + irad
    do iiy = iy1 - ygrids, iy1 + ygrids
      ik = ik +1
      a1x(ik) = iix
      a1y(ik) = iiy
    end do
    !--------
  end do
else if (xgrids .lt. ygrids) then
  do irad = xgrids+1, ygrids
    !--------
    iiy = iy1 - irad
    do iix = ix1 - xgrids, ix1 + xgrids
      ik = ik +1
      a1x(ik) = iix
      a1y(ik) = iiy
    end do
    !--------
    iiy = iy1 + irad
    do iix = ix1 - xgrids, ix1 + xgrids
      ik = ik +1
      a1x(ik) = iix
      a1y(ik) = iiy
    end do
    !--------
  end do
end if
RETURN
END SUBROUTINE mk_a1xa1y
!*****************************************************************
SUBROUTINE findcyclone(a2psl, miss_in, miss_out, nx, ny, a2pmean)
  implicit none
  !** for input ---------------------------------------------
  integer                                           nx, ny
  double precision,dimension(nx ,ny)             :: a2psl
!f2py intent(in)                                    a2psl
  double precision                                  miss_in, miss_out
!f2py intent(in)                                    miss_in, miss_out
  !** for output --------------------------------------------
  double precision,dimension(nx, ny)             :: a2pmean
!f2py intent(out)                                   a2pmean
  !** for calc  ---------------------------------------------
  integer                                           ix, iy, ik
  integer                                           iix, iiy, iiix, iiiy
  integer                                           icount, flag
  double precision                                  pmean, psl
  double precision,dimension(8)                  :: a1ambi
  !----------------------------------------------------------
do iy = 1, ny
  do ix = 1, nx
    psl = a2psl(ix, iy)
    !---------------
    ! ambient data
    !---------------
    ik = 0
    do iiy = iy-1, iy+1, 2
      do iix = ix -1, ix+1
        ik = ik +1
        call ixy2iixy(iix, iiy, nx, ny, iiix, iiiy)
        a1ambi(ik) = a2psl(iiix, iiiy)
      end do
    end do
    iiy = iy
    do iix = ix-1, ix+1, 2
      ik = ik +1
      call ixy2iixy(iix, iiy, nx, ny, iiix, iiiy)
      a1ambi(ik) = a2psl(iiix, iiiy)
    end do
    !----------------
    ! compare to the ambient grids
    !----------------
    flag = 0
    do ik = 1, 8
      if ( psl .ge. a1ambi(ik) )  then
        flag = 1
        exit
      end if
    end do
    !----------------
    if (flag .eq. 1) then
      a2pmean(ix, iy) = miss_out
    else if (flag .eq. 0) then
      pmean  = 0.0d0
      icount = 0
      do ik = 1, 8
        icount = icount + 1
        pmean = pmean + a1ambi(ik)
      end do
      pmean = pmean /icount
      !---------------
      if (a2psl(ix, iy) .lt. pmean) then
        a2pmean(ix, iy) = pmean
      else
        a2pmean(ix, iy) = miss_out
      end if
    end if
    !---------------
  end do
end do


RETURN
END SUBROUTINE
!!*****************************************************************
SUBROUTINE ixy2iixy(ix,iy, nx, ny, iix, iiy)
  implicit none
  !- for input -----------------
  integer                   ix, iy, nx, ny
!f2py intent(in)            ix, iy, nx, ny
  !- for output ----------------
  integer                   iix, iiy
!f2py intent(out)           iix, iiy
  !-----------------------------
if (iy .lt. 1) then
  iiy = 2 - iy
  iix = ix + int(nx/2.0)
  iix = roundx(iix, nx)
else if (iy .gt. ny) then
  iiy = 2*ny -iy
  iix = ix + int(nx/2.0)
  iix = roundx(iix, nx)
else
  iiy = iy
  iix = roundx(ix, nx)
end if
RETURN
END SUBROUTINE
!*****************************************************************
FUNCTION latgrids(lat, dlat, thdist)
  implicit none
  !-- for input -----------
  double precision                      thdist   ! [m]
!f2py intent(in)                        thdist
  double precision                      lat, dlat
!f2py intent(in)                        lat, dlat
  !-- for output ----------
  double precision                      latgrids 
!f2py intent(out)                       latgrids
  !-- for calc  -----------
  integer                               i
  double precision                      dist, lat2
  double precision                      dist_pre
  !------------------------
dist = 0.0d0
do i = 1, 100000
  lat2     = lat + dlat * i
  dist_pre = dist
  dist     = hubeny(lat, 0.0d0, lat2, 0.0d0)
  if (dist .gt. abs(thdist)) then
    if ( (dist + dist_pre)*0.5d0 .lt. abs(thdist) )then
      if (thdist .ge. 0.0d0) then
        latgrids = i
      else
        latgrids = -i
      end if
    else
      if (thdist .ge. 0.0d0) then
        latgrids = i-1
      else
        latgrids = -(i-1)
      end if
    end if
    exit
  end if
end do
RETURN
END FUNCTION latgrids
!*****************************************************************
FUNCTION longrids(lat, dlon, thdist)
  implicit none
  !-- for input -----------
  double precision                      thdist   ! [m]
!f2py intent(in)                        thdist
  double precision                      lat, dlon
!f2py intent(in)                        lat, dlon
  !-- for output ----------
  double precision                      longrids 
!f2py intent(out)                       longrids
  !-- for calc  -----------
  integer                               i
  double precision                      dist, lon2
  double precision                      dist_pre
  !------------------------
dist = 0.0d0
do i = 1, 100000
  lon2     = dlon * i
  dist_pre = dist
  dist     = hubeny(lat, 0.0d0, lat, lon2)
  if (dist .gt. abs(thdist)) then
    if ( (dist + dist_pre)*0.5d0 .lt. abs(thdist) )then
      if (thdist .ge. 0.0d0) then
        longrids = i
      else
        longrids = -i
      end if
    else
      if (thdist .ge. 0.0d0) then
        longrids = i -1 
      else
        longrids = -(i -1)
      end if
    endif
    exit
  end if
end do
RETURN
END FUNCTION longrids
!*****************************************************************
SUBROUTINE gridrange(lat, dlat, dlon, thdist, ngrids, sgrids, xgrids)
  implicit none
  !-- for input -----------
  double precision                      thdist   ! [km]
!f2py intent(in)                        thdist
  double precision                      lat, dlat, dlon
!f2py intent(in)                        lat, dlat, dlon
  !-- for output ----------
  integer                               ngrids, sgrids, xgrids
!f2py intent(out)                       ngrids, sgrids, xgrids
  !-- for calc  -----------
  integer                               i
  double precision                      dist, lat2, lon2
  !------------------------
do i = 1, 100000
  lat2 = lat + dlat * i
  dist = hubeny(lat, 0.0d0, lat2, 0.0d0)
  if (dist .gt. thdist) then
    ngrids = i
    exit
  end if
end do
do i = 1, 100000
  lat2 = lat - dlat * i
  dist = hubeny(lat, 0.0d0, lat2, 0.0d0)
  if (dist .gt. thdist) then
    sgrids = i
    exit
  end if
end do
do i = 1, 100000
  lon2 = dlon * i
  dist = hubeny(lat, 0.0d0, lat, lon2)
  if (dist .gt. thdist) then
    xgrids = i
    exit
  end if 
end do
RETURN
END SUBROUTINE gridrange
!*****************************************************************
FUNCTION hubeny(lat1, lon1, lat2, lon2)
  implicit none
  !-- for input -----------
  double precision                      lat1, lon1, lat2, lon2
!f2py intent(in)                        lat1, lon1, lat2, lon2
  !-- for output-----------
  double precision                      hubeny
!f2py intent(out)                       hubeny
  !-- for calc ------------
  double precision,parameter         :: pi = atan(1.0d0)*4.0d0
  double precision,parameter         :: a  = 6378137d0
  double precision,parameter         :: b  = 6356752.314140d0
  double precision,parameter         :: e2 = 0.00669438002301188d0
  double precision,parameter         :: a_1_e2 = 6335439.32708317d0
  double precision                      M, N, W
  double precision                      latrad1, latrad2, lonrad1, lonrad2
  double precision                      latave, dlat, dlon
  double precision                      dlondeg
  double precision                      meridian, primevertical
  !------------------------
  latrad1   = lat1 * pi / 180.0d0
  latrad2   = lat2 * pi / 180.0d0
  lonrad1   = lon1 * pi / 180.0d0
  lonrad2   = lon2 * pi / 180.0d0
  !
  latave    = (latrad1 + latrad2)/2.0d0
  dlat      = latrad2 - latrad1
  dlon      = lonrad2 - lonrad1
  !
  dlondeg   = lon2 - lon1
  if ( abs(dlondeg) .gt. 180.0d0) then
    dlondeg = 180.0d0 - mod(abs(dlondeg), 180.0d0)
    dlon    = dlondeg * pi / 180.0d0
  end if
  !-------
  W  = sqrt(1.0d0 - e2 * sin(latave)**2.0d0 )
  M  =  a_1_e2 / (W**3.0d0)
  N  =  a / W
  hubeny  = sqrt( (dlat * M)**2.0d0 + (dlon * N * cos(latave))**2.0d0 )
  !print *, hubeny * 0.001d0
  !print *, "a_1_e2=", a_1_e2
  !print *, "calc",a*(1.0d0 - e2)

  !M  = 6334834.0d0 / sqrt( (1.0d0 - 0.006674d0 * sin(latave) **2.0d0)**2.0d0 )
  !N  = 6377397.0d0 / sqrt( 1.0d0 - 0.006674d0 * sin(latave) **2.0d0)
  !hubeny = sqrt( (M * dlat )**2.0d0 + ( N * cos(latave) * dlon)**2.0d0 )
RETURN
END FUNCTION hubeny
!*****************************************************************
!*****************************************************************
!*****************************************************************
FUNCTION roundx(ix, nx)
  implicit none
  !-- for input -----------
  integer                     ix, nx
!f2py intent(in)              ix, nx
  !-- for output ----------
  integer                     roundx
!f2py intent(out)             roundx
  !------------------------
  if (ix .lt. 1) then
    roundx = nx + ix
  else if (ix .gt. nx) then
    roundx = ix - nx
  else
    roundx = ix
  end if
RETURN
END FUNCTION roundx
!*****************************************************************
!*****************************************************************
!*****************************************************************
!*****************************************************************
!*****************************************************************
!*****************************************************************
!*****************************************************************
!*****************************************************************
!*****************************************************************
end module ctrack
