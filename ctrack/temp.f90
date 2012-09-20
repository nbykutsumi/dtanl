PROGRAM temp

CONTAINS
FUNCTION hubeny_real(lat1, lon1, lat2, lon2)
  implicit none
  !-- for input -----------
  real                                  lat1, lon1, lat2, lon2
!f2py intent(in)                        lat1, lon1, lat2, lon2
  !-- for output-----------
  real                                  hubeny_real
!f2py intent(out)                       hubeny_real
  !-- for calc ------------
  real,parameter                     :: pi = atan(1.0)*4.0
  real,parameter                     :: a  = 6378137
  real,parameter                     :: b  = 6356752.314140
  real,parameter                     :: e2 = 0.00669438002301188
  real,parameter                     :: a_1_e2 = 6335439.32708317
  real                                  M, N, W
  real                                  latrad1, latrad2, lonrad1, lonrad2
  real                                  latave, dlat, dlon
  real                                  dlondeg
  real                                  meridian, primevertical
  !------------------------
  latrad1   = lat1 * pi / 180.0
  latrad2   = lat2 * pi / 180.0
  lonrad1   = lon1 * pi / 180.0
  lonrad2   = lon2 * pi / 180.0
  !
  latave    = (latrad1 + latrad2)/2.0
  dlat      = latrad2 - latrad1
  dlon      = lonrad2 - lonrad1
  !
  dlondeg   = lon2 - lon1
  if ( abs(dlondeg) .gt. 180.0) then
    dlondeg = 180.0 - mod(abs(dlondeg), 180.0)
    dlon    = dlondeg * pi / 180.0
  end if
  !-------
  W  = sqrt(1.0 - e2 * sin(latave)**2.0 )
  M  =  a_1_e2 / (W**3.0)
  N  =  a / W
  hubeny_real  = sqrt( (dlat * M)**2.0 + (dlon * N * cos(latave))**2.0 )
  !print *, hubeny * 0.001
  !print *, "a_1_e2=", a_1_e2
  !print *, "calc",a*(1.0 - e2)

  !M  = 6334834.0 / sqrt( (1.0 - 0.006674 * sin(latave) **2.0)**2.0 )
  !N  = 6377397.0 / sqrt( 1.0 - 0.006674 * sin(latave) **2.0)
  !hubeny = sqrt( (M * dlat )**2.0 + ( N * cos(latave) * dlon)**2.0 )
RETURN
END FUNCTION hubeny_real
!--------------------------------------------------------------
!!*****************************************************************
FUNCTION longrids_real(lat, dlon, thdist)
  implicit none
  !-- for input -----------
  real                                  thdist   ! [m]
!f2py intent(in)                        thdist
  real                                  lat, dlon
!f2py intent(in)                        lat, dlon
  !-- for output ----------
  integer                               longrids_real
!f2py intent(out)                       longrids_real
  !-- for calc  -----------
  integer                               i
  real                                  dist, lon2
  real                                  dist_pre
  real                                  hubeny_real
  !------------------------
dist = 0.0
do i = 1, 100000
  lon2     = dlon * i
  dist_pre = dist
  dist     = hubeny_real(lat, 0.0, lat, lon2)
  if (dist .gt. abs(thdist)) then
    if ( (dist + dist_pre)*0.5 .lt. abs(thdist) )then
      if (thdist .ge. 0.0) then
        longrids_real = i
      else
        longrids_real = -i
      end if
    else
      if (thdist .ge. 0.0) then
        longrids_real = i -1
      else
        longrids_real = -(i -1)
      end if
    endif
    exit
  end if
end do
RETURN
END FUNCTION longrids_real
!*****************************************************************
!*****************************************************************
FUNCTION latgrids_real(lat, dlat, thdist)
  implicit none
  !-- for input -----------
  real                                  thdist   ! [m]
!f2py intent(in)                        thdist
  real                                  lat, dlat
!f2py intent(in)                        lat, dlat
  !-- for output ----------
  integer                               latgrids_real
!f2py intent(out)                       latgrids_real
  !-- for calc  -----------
  integer                               i
  real                                  dist, lat2
  real                                  dist_pre
  real                                  hubeny_real
  !------------------------
dist = 0.0
do i = 1, 100000
  lat2     = lat + dlat * i
  dist_pre = dist
  dist     = hubeny_real(lat, 0.0, lat2, 0.0)
  if (dist .gt. abs(thdist)) then
    if ( (dist + dist_pre)*0.5 .lt. abs(thdist) )then
      if (thdist .ge. 0.0) then
        latgrids_real = i
      else
        latgrids_real = -i
      end if
    else
      if (thdist .ge. 0.0) then
        latgrids_real = i-1
      else
        latgrids_real = -(i-1)
      end if
    end if
    exit
  end if
end do
RETURN
END FUNCTION latgrids_real
!!*****************************************************************


SUBROUTINE eqgrid_aggr(a2in, a1lat, a1lon, dkm, nradout, iy, ix, ny_in, nx_in, a2sum, a2num)
  implicit none
  !-- input -------------------------------------
  integer                                        ny_in, nx_in

  integer                                        nradout, iy, ix
!f2py intent(in)                                 nradout, iy, ix
  real,dimension(nx_in, ny_in)                :: a2in
!f2py intent(in)                                 a2in
  real,dimension(ny_in)                       :: a1lat
!f2py intent(in)                                 a1lat
  real,dimension(nx_in)                       :: a1lon
!f2py intent(in)                                 a1lon
  real                                           dkm
!f2py intent(in)                                 dkm

  !-- output ------------------------------------
  real,dimension(2*nradout+1, 2*nradout+1)    :: a2sum, a2num
!f2py intent(out)                                a2sum, a2num

  !-- calc   ------------------------------------
  integer                                        iiy, iix
  integer                                        nyrad_sub, nxrad_sub
  integer                                        iiy_sub, iix_sub
  integer                                        iiradgrids_sub
  real                                           lat_first, lon_first
  real                                           latc, lonc
  real                                           latt, lont
  real                                           nyrad_in
  real                                           dlat, dlon
  real                                           yradkm
  real                                           onegridkm
  real                                           radtemp
  !-- functions --------
  real                                           hubeny_real
  integer                                        latgrids_real, longrids_real
  !----------------------------------------------
  dlat           = a1lat(2) - a1lat(1)
  dlon           = a1lon(2) - a1lon(1)
  lat_first      = a1lat(1)
  lon_first      = a1lon(1)

  latc           = a1lat(iy)
  lonc           = a1lon(ix)
  nyrad_sub      = latgrids_real(latc, dlat, nradout*dkm*1000.0)
  nxrad_sub      = longrids_real(latc, dlon, nradout*dkm*1000.0)

  !----------------------------------------------
  !----------------------------------------------
  !--- initialize -------------------------------
  a2sum  = 0.0
  a2num  = 0.0

  !--- aggregate --------------------------------
  print *,"AAAAAAA"

  do iiy = iy -nyrad_sub, iy + nyrad_sub
    if (iiy <=0) then
      continue
    endif

    print *,"BBB, iiy=",iiy

    latt     = lat_first + (iiy-1)*dlat

    yradkm    = hubeny_real(latc, 0.0, latt, 0.0)* 0.001

    iiy_sub   = int( (yradkm + dkm*0.5)/dkm ) * int(sign(1.0, latt - latc)) + nradout + 1

    onegridkm = hubeny_real(latt, lonc, latt, lonc + dlon)*0.001

    !--
    do iix = ix - nxrad_sub, ix + nxrad_sub
      if (iix <=0) then
        continue
      endif
      !---
      lont       = lon_first + (iix-1)*dlon

      iiradgrids_sub  = int( (onegridkm* abs(iix-ix) + dkm*0.5)/dkm )
      if ( (lont - lonc) .ge. 0.0)then
        iix_sub    =  iiradgrids_sub + nradout + 1
      else
        iix_sub    =  -iiradgrids_sub + nradout + 1
      endif
      print *,"iiradgrids_sub, nradout", iiradgrids_sub, nradout

      !a2sum(iix_sub, iiy_sub)  =  a2sum(iix_sub, iiy_sub) + a2in(iix, iiy)
      print *, iix_sub, iiy_sub, a2sum(iix_sub, iiy_sub)

      !iix_sub = 10
      a2sum(iix_sub, iiy_sub) = 1.0
  !    print *,"a2sum", a2sum(iix_sub, iiy_sub)
  !    !a2num(iix_sub, iiy_sub)  =  a2num(iix_sub, iiy_sub) + 1.0
  !    !a2num(iix_sub, iiy_sub)  =  (iix-ix)**2.0 + (iiy-iy)**2.0

    enddo
  enddo
  !----------------------------------------------
  print *, a2sum
  print *, "XXX, iix_sub, iiy_sub", iix_sub, iiy_sub



RETURN
END SUBROUTINE eqgrid_aggr

END PROGRAM temp
