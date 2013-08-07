module ctrack_fsub

!-----------------------------------
CONTAINS
!*****************************************************************
!* SUBROUTINE & FUNCTION
!*****************************************************************
SUBROUTINE mk_a2max_rad_saone(a2in, radkm, nx, ny, a2out)
implicit none
!----------------------------------------------
integer                        nx, ny
!--- in ------------
real,dimension(nx,ny)       :: a2in
!f2py intent(in)               a2in
real                           radkm
!f2py intent(in)               radkm
!--- out -----------
real,dimension(nx,ny)       :: a2out
!f2py intent(out)              a2out
!--- calc ----------
integer,dimension(nx*ny)    :: a1x, a1y
integer                        ix, iy, ixt, iyt, dx, dy, icount
real                           lat
real                           vmax
!--- para ----------
integer,parameter           :: miss_int = -9999
real,parameter              :: dlat = 1.0
real,parameter              :: dlon = 1.0
real,parameter              :: lat_first = -89.5
real,parameter              :: lon_first = 0.5
!-------------------
do iy = 1,ny
  do ix = 1,nx
    lat  = lat_first + dlat*(iy -1)
    vmax = a2in(ix,iy)
    CALL circle_xy_real(lat, lat_first, dlon, dlat, radkm*1000.0, miss_int, nx, ny, a1x, a1y)
    !
    icount = 1
    do while (a1x(icount) .ne. miss_int)
      dx = a1x(icount)
      dy = a1y(icount)
      CALL ixy2iixy(ix+dx, iy+dy, nx, ny, ixt, iyt)
      vmax = max(vmax, a2in(ixt,iyt))
      icount  = icount + 1
    end do
    a2out(ix,iy) = vmax
    !-
  end do
end do
!!----------------------------------------------
return
END SUBROUTINE mk_a2max_rad_saone

!*****************************************************************
SUBROUTINE point_pgrad_rad_saone(ixfort, iyfort, a2psl, radkm, miss, nx, ny, pgrad)
implicit none
!----------------------------------------------
integer                        nx, ny
!--- in ------------
integer                        ixfort, iyfort
!f2py intent(in)               ixfort, iyfort
real,dimension(nx,ny)       :: a2psl
!f2py intent(in)               a2psl
real                           radkm
!f2py intent(in)               radkm
real                           miss
!f2py intent(in)               miss
!--- out -----------
real                           pgrad
!f2py intent(out)              pgrad
!--- calc ----------
integer                        icount, missflag
integer,dimension(nx*ny)    :: a1x, a1y
integer                        ixt, iyt, dx, dy
real                           lat
real                           pgrad_tmp
!--- para ----------
integer,parameter           :: miss_int = -9999
real,parameter              :: dlat = 1.0
real,parameter              :: dlon = 1.0
real,parameter              :: lat_first = -89.5
real,parameter              :: lon_first = 0.5
!-------------------
lat  = lat_first + dlat*(iyfort -1)
CALL circle_xy_real(lat, lat_first, dlon, dlat, radkm*1000.0, miss_int, nx, ny, a1x, a1y)
!
pgrad    = 0.0
missflag = 0
icount   = 0
do while (a1x(icount) .ne. miss_int)
  dx = a1x(icount)
  dy = a1y(icount)
  CALL ixy2iixy(ixfort+dx, iyfort+dy, nx, ny, ixt, iyt)
  if (a2psl(ixt, iyt).eq. miss)then
    missflag = 1
    cycle
  end if
  pgrad_tmp  =  (a2psl(ixt, iyt) - a2psl(ixfort,iyfort))/radkm
  pgrad      = pgrad + pgrad_tmp
  icount = icount + 1
end do
!-
if (missflag .eq.0)then
  !print *,"before,t,mt,icount",a2t(ixfort,iyfort), mt,icount
  pgrad  = pgrad / real(icount)
else
  pgrad  = miss
end if
!!----------------------------------------------
return
END SUBROUTINE point_pgrad_rad_saone

!*****************************************************************
SUBROUTINE point_dt_rad_saone(ixfort, iyfort, a2t, radkm, miss, nx, ny, dt)
implicit none
!----------------------------------------------
integer                        nx, ny
!--- in ------------
integer                        ixfort, iyfort
!f2py intent(in)               ixfort, iyfort
real,dimension(nx,ny)       :: a2t
!f2py intent(in)               a2t
real                           radkm
!f2py intent(in)               radkm
real                           miss
!f2py intent(in)               miss
!--- out -----------
real                           dt
!f2py intent(out)              dt
!--- calc ----------
integer                        icount, missflag
integer,dimension(nx*ny)    :: a1x, a1y
integer                        ixt, iyt, dx, dy
real                           lat
real                           mt
!--- para ----------
integer,parameter           :: miss_int = -9999
real,parameter              :: dlat = 1.0
real,parameter              :: dlon = 1.0
real,parameter              :: lat_first = -89.5
real,parameter              :: lon_first = 0.5
!-------------------
lat  = lat_first + dlat*(iyfort -1)
CALL circle_xy_real(lat, lat_first, dlon, dlat, radkm*1000.0, miss_int, nx, ny, a1x, a1y)
!
mt       = 0
missflag = 0
icount   = 1
do while (a1x(icount) .ne. miss_int)
  dx = a1x(icount)
  dy = a1y(icount)
  CALL ixy2iixy(ixfort+dx, iyfort+dy, nx, ny, ixt, iyt)
  !print *,"ix,iy,ixt,iyt,a2tt",ixfort,iyfort,ixt,iyt,a2t(ixt,iyt)
  mt       = mt + a2t(ixt, iyt)
  icount = icount + 1
  if (a2t(ixt, iyt).eq. miss)then
    missflag = 1
    exit
  end if
end do
icount = icount -1
!-
if (missflag .eq.0)then
  !print *,"before,t,mt,icount",a2t(ixfort,iyfort), mt,icount
  mt  = mt / real(icount)
  dt  = a2t(ixfort,iyfort) - mt
  !print *,"after ,t,mt,icount",a2t(ixfort,iyfort), mt,icount
else
  dt  = miss
end if
!!----------------------------------------------
return
END SUBROUTINE point_dt_rad_saone

!*****************************************************************
SUBROUTINE point_rvort_saone(ixfort, iyfort, a2u, a2v,miss, nx, ny, rvort)
implicit none
!----------------------------------------------
integer                        nx, ny
!--- in ------------
integer                        ixfort, iyfort
!f2py intent(in)               ixfort, iyfort
real,dimension(nx,ny)       :: a2u, a2v
!f2py intent(in)               a2u, a2v
real                           miss
!f2py intent(in)               miss
!--- out -----------
real                           rvort
!f2py intent(out)              rvort
!--- calc ----------
integer                        ixw,ixe,ixs,ixn
integer                        iyw,iye,iys,iyn
real                           lat
real                           un, us, ve, vw
real                           dn, ds, dns, dew
!--- para ----------
real,parameter              :: dlat = 1.0
real,parameter              :: dlon = 1.0
real,parameter              :: lat_first = -89.5
real,parameter              :: lon_first = 0.5

!!-------------------
lat  = lat_first + dlat*(iyfort -1)

!-- relative vorticity ---
dn  = hubeny_real(lat, 0.0, lat+1.0, 0.0)
ds  = hubeny_real(lat, 0.0, lat-1.0, 0.0)
dns = (dn + ds)/2.0
dew = hubeny_real(lat, 0.0, lat, 1.0)


call ixy2iixy_saone(ixfort, iyfort+1, ixn, iyn)
call ixy2iixy_saone(ixfort, iyfort-1, ixs, iys)
call ixy2iixy_saone(ixfort-1, iyfort, ixw, iyw)
call ixy2iixy_saone(ixfort+1, iyfort, ixe, iye)
!---
us  = a2u(ixs, iys)
un  = a2u(ixn, iyn)
vw  = a2v(ixw, iyw)
ve  = a2v(ixe, iye)
!-
if ( (us.eq.miss).or.(un.eq.miss) )then
  rvort = miss
else
  rvort  =  (ve - vw)/(dew*2.0) - (un - us)/(dns*2.0) 
end if
!-
!
!----------------------------------------------
return
END SUBROUTINE point_rvort_saone


!*****************************************************************
SUBROUTINE point_rvort_rad_saone(ixfort, iyfort, a2u, a2v, radkm, miss, nx, ny, rvort)
implicit none
!----------------------------------------------
integer                        nx, ny
!--- in ------------
integer                        ixfort, iyfort
!f2py intent(in)               ixfort, iyfort
real,dimension(nx,ny)       :: a2u, a2v
!f2py intent(in)               a2u, a2v
real                           radkm   ! (km)
!f2py intent(in)               radkm
real                           miss
!f2py intent(in)               miss
!--- out -----------
real                           rvort
!f2py intent(out)              rvort
!--- calc ----------
integer                        ngrids, sgrids, xgrids
integer                        ixw,ixe,ixs,ixn
integer                        iyw,iye,iys,iyn
real                           lat
real                           un, us, ve, vw
real                           dn, ds, dns, dew
!--- para ----------
real,parameter              :: dlat = 1.0
real,parameter              :: dlon = 1.0
real,parameter              :: lat_first = -89.5
real,parameter              :: lon_first = 0.5

!!-------------------
lat  = lat_first + dlat*(iyfort -1)
CALL gridrange_real(lat, dlat, dlon, radkm*1000.0, ngrids, sgrids, xgrids)

!-- relative vorticity ---
dn  = hubeny_real(lat, 0.0, lat+1.0*ngrids, 0.0)
ds  = hubeny_real(lat, 0.0, lat-1.0*sgrids, 0.0)
dns = (dn + ds)/2.0
dew = hubeny_real(lat, 0.0, lat, 1.0*xgrids)


call ixy2iixy_saone(ixfort, iyfort+ngrids, ixn, iyn)
call ixy2iixy_saone(ixfort, iyfort-sgrids, ixs, iys)
call ixy2iixy_saone(ixfort-xgrids, iyfort, ixw, iyw)
call ixy2iixy_saone(ixfort+xgrids, iyfort, ixe, iye)
!---
us  = a2u(ixs, iys)
un  = a2u(ixn, iyn)
vw  = a2v(ixw, iyw)
ve  = a2v(ixe, iye)
!-
if ( (us.eq.miss).or.(un.eq.miss) )then
  rvort = miss
else
  rvort  =  (ve - vw)/(dew*2.0) - (un - us)/(dns*2.0) 
end if
!-
!
!----------------------------------------------
return
END SUBROUTINE point_rvort_rad_saone
!*****************************************************************
SUBROUTINE check_pgrad_saone(a2psl, a2psl_org, a2pos, radkm, lenout, miss, nx, ny, a1v)
implicit none
!---------------------
! estimate pressure mean gradient (hPa/100km)
! in the 300km radius circle
!--- dimensions ------
integer                              nx, ny
!--- in --------------
real,dimension(nx,ny)             :: a2psl, a2psl_org, a2pos
!f2py intent(in)                     a2psl, a2psl_org, a2pos
real                                 radkm   ! (km)
!f2py intent(in)                     radkm
integer                              lenout
!f2py intent(in)                     lenout
real                                 miss
!f2py intent(in)                     miss
!--- out --------------
real,dimension(lenout)            :: a1v
!f2py intent(out)                    a1v
!--- calc -------------
integer,dimension(8)              :: a1surrx, a1surry
integer                              localflag, i, ixt, iyt
integer                              ix, iy, iiy, iix
integer                              dx, dy
integer                              ndx, ndyn, ndys, ndy
integer                              iout, icount
real                                 dist  ! (km)
real                                 latc, lonc, latt, lont
real                                 v, sv
!--- parameter --------
real,parameter                    :: lat_first = -89.5
real,parameter                    :: lon_first = 89.5
real,parameter                    :: dlon      = 1.0
real,parameter                    :: dlat      = 1.0
!--- init -------------
a1v    = miss
!----------------------
iout  = 0
do iy = 1,ny
  do ix = 1,nx
    if (a2pos(ix,iy) .ne. miss)then
      latc = lat_first + dlat*(iy-1)
      lonc = lon_first + dlon*(ix-1)
      ndyn  = int(radkm/ (hubeny_real(0.0, 0.0, +1.0, 0.0)) * 1000.0) +1
      ndys  = int(radkm/ (hubeny_real(0.0, 0.0, -1.0, 0.0)) * 1000.0) +1
      ndy   = max(ndyn, ndys)
      ndx   = int(radkm/ (hubeny_real(latc, 0.0, latc+1.0, 0.0)) * 1000.0) +1
      !--- check local minima -----------
      localflag = 0
      CALL mk_8gridsxy(ix,iy,nx,ny,a1surrx,a1surry)
      do i = 1, 8
        ixt = a1surrx(i)
        iyt = a1surry(i)
        if (a2psl_org(ix,iy) .gt. a2psl_org(ixt,iyt))then
          localflag = localflag + 1
        end if
      end do
      if (localflag .gt. 0)then
        cycle
      end if
      !----------------------------------
      icount = 0
      sv     = 0.0
      do dy = -ndy, ndy
        iiy  = iy + dy
        if (iiy .gt. ny) iiy = ny
        if (iiy .lt. 1)  iiy = 1
        latt = lat_first + dlat*(iiy-1)
        do dx = -ndx, ndx
          if ((dx.eq.0).and.(dy.eq.0)) cycle
          iix  = roundx(ix+dx, nx)
          lont = lon_first + dlon*(iix-1) 
          dist = hubeny_real(latc, lonc, latt, lont) * 0.001   ! (km)
          !------------
          if (dist.gt.radkm)then
            cycle
          end if
          v    = (a2psl(iix,iiy) - a2psl(ix, iy))*0.01 / dist *100.0  ! (hPa/100km)
          !print *,"v=",v, a2psl(iix,iiy), a2psl(ix, iy), dist
          sv   = sv + v
          icount = icount + 1
        end do       
      end do
      !------------
      iout        = iout + 1
      a1v(iout)   = sv / icount
      !------------
    end if 
  end do
end do

!----------------------
return
END SUBROUTINE check_pgrad_saone
!*****************************************************************
SUBROUTINE vs_dist_dv_saone(a2v, a2pos, dkm, lenout, miss, nx, ny, a1sv, a1sv2, a1num)
implicit none
!--- dimensions ------
integer                              nx, ny
!--- in --------------
real,dimension(nx,ny)             :: a2v, a2pos
!f2py intent(in)                     a2v, a2pos
real                                 dkm   ! (km)
!f2py intent(in)                     dkm
integer                              lenout
!f2py intent(in)                     lenout
real                                 miss
!f2py intent(in)                     miss
!--- out --------------
real,dimension(lenout)            :: a1sv, a1sv2, a1num
!f2py intent(out)                    a1sv, a1sv2, a1num
!--- calc -------------
integer                              ix, iy, iiy, iix
integer                              dx, dy
integer                              ndx, ndyn, ndys, ndy
integer                              iout
real                                 dist  ! (km)
real                                 latc, lonc, latt, lont
real                                 temp
!--- parameter --------
real,parameter                    :: lat_first = -89.5
real,parameter                    :: lon_first = 89.5
real,parameter                    :: dlon      = 1.0
real,parameter                    :: dlat      = 1.0
!--- init -------------
a1sv    = 0.0
a1sv2   = 0.0
a1num   = 0.0
!----------------------
temp = 0.0
!----------------------
do iy = 1,ny
  do ix = 1,nx
    if (a2pos(ix,iy) .ne. miss)then
      latc = lat_first + dlat*(iy-1)
      lonc = lon_first + dlon*(ix-1)
      ndyn  = int(lenout*dkm/ (hubeny_real(0.0, 0.0, +1.0, 0.0)) * 1000.0) +1
      ndys  = int(lenout*dkm/ (hubeny_real(0.0, 0.0, -1.0, 0.0)) * 1000.0) +1
      ndy   = max(ndyn, ndys)
      ndx   = int(lenout*dkm/ (hubeny_real(latc, 0.0, latc+1.0, 0.0)) * 1000.0) +1
      do dy = -ndy, ndy
        iiy  = iy + dy
        if (iiy .gt. ny) iiy = ny
        if (iiy .lt. 1)  iiy = 1
        latt = lat_first + dlat*(iiy-1)
        do dx = -ndx, ndx
          iix  = roundx(ix+dx, nx)
          lont = lon_first + dlon*(iix-1) 
          dist = hubeny_real(latc, lonc, latt, lont) * 0.001   ! (km)
          iout = int((dist+0.5*dkm) / dkm) + 1
          !------------
          if (iout.gt.lenout)then
            cycle
          end if
          !------------
          a1sv(iout)   = a1sv(iout)  + (a2v(iix,iiy) - a2v(ix,iy))
          a1sv2(iout)  = a1sv2(iout) + (a2v(iix,iiy) - a2v(ix,iy))**2.0
          a1num(iout)  = a1num(iout) + 1.0

        end do       
      end do
    end if 
  end do
end do

!----------------------
return
END SUBROUTINE vs_dist_dv_saone

!*****************************************************************
SUBROUTINE vs_dist_c_saone(a2v, a2pos, dkm, lenout, miss, nx, ny, a1sv, a1sv2, a1num)
implicit none
!--- dimensions ------
integer                              nx, ny
!--- in --------------
real,dimension(nx,ny)             :: a2v, a2pos
!f2py intent(in)                     a2v, a2pos
real                                 dkm   ! (km)
!f2py intent(in)                     dkm
integer                              lenout
!f2py intent(in)                     lenout
real                                 miss
!f2py intent(in)                     miss
!--- out --------------
real,dimension(lenout)            :: a1sv, a1sv2, a1num
!f2py intent(out)                    a1sv, a1sv2, a1num
!--- calc -------------
integer                              ix, iy, iiy, iix
integer                              dx, dy
integer                              ndx, ndyn, ndys, ndy
integer                              iout
real                                 dist  ! (km)
real                                 latc, lonc, latt, lont
real                                 temp
!--- parameter --------
real,parameter                    :: lat_first = -89.5
real,parameter                    :: lon_first = 89.5
real,parameter                    :: dlon      = 1.0
real,parameter                    :: dlat      = 1.0
!--- init -------------
a1sv    = 0.0
a1sv2   = 0.0
a1num   = 0.0
!----------------------
temp = 0.0
!----------------------
do iy = 1,ny
  do ix = 1,nx
    if (a2pos(ix,iy) .ne. miss)then
      !-----------------------------------
      latc = lat_first + dlat*(iy-1)
      lonc = lon_first + dlon*(ix-1)
      ndyn  = int(lenout*dkm/ (hubeny_real(0.0, 0.0, +1.0, 0.0)) * 1000.0) +1
      ndys  = int(lenout*dkm/ (hubeny_real(0.0, 0.0, -1.0, 0.0)) * 1000.0) +1
      ndy   = max(ndyn, ndys)
      ndx   = int(lenout*dkm/ (hubeny_real(latc, 0.0, latc+1.0, 0.0)) * 1000.0) +1
      do dy = -ndy, ndy
        iiy  = iy + dy
        if (iiy .gt. ny) iiy = ny
        if (iiy .lt. 1)  iiy = 1
        latt = lat_first + dlat*(iiy-1)
        do dx = -ndx, ndx
          iix  = roundx(ix+dx, nx)
          lont = lon_first + dlon*(iix-1) 
          dist = hubeny_real(latc, lonc, latt, lont) * 0.001   ! (km)
          iout = int((dist+0.5*dkm) / dkm) + 1
          !------------
          if (iout.gt.lenout)then
            cycle
          end if
          !------------
          a1sv(iout)   = a1sv(iout)  + a2v(iix,iiy)
          a1sv2(iout)  = a1sv2(iout) + a2v(iix,iiy)**2.0
          a1num(iout)  = a1num(iout) + 1.0

        end do       
      end do
    end if 
  end do
end do

!----------------------
return
END SUBROUTINE vs_dist_c_saone
!*****************************************************************
SUBROUTINE find_tc_saone(a2pgrad, a2life, a2lastpos, a2lastflag, a2tlow, a2tmid, a2tup&
                        &, a2ulow, a2uup, a2vlow, a2vup, a2sst, a2landsea&
                        &, thpgrad, thdura, thsst, thwind, thrvort, initflag, miss&
                        &, nx, ny, a2tcloc, a2nowflag)

implicit none
!---- in ------
integer                              nx, ny
real,dimension(nx,ny)             :: a2pgrad, a2lastflag, a2tlow, a2tmid, a2tup, a2ulow, a2uup, a2vlow, a2vup, a2sst, a2landsea
!f2py intent(in)                     a2pgrad, a2lastflag, a2tlow, a2tmid, a2tup, a2ulow, a2uup, a2vlow, a2vup, a2sst, a2landsea
integer,dimension(nx,ny)          :: a2life, a2lastpos
!f2py intent(in)                     a2life, a2lastpos
real                                 thpgrad, thdura, thsst, thwind, thrvort
!f2py intent(in)                     thpgrad, thdura, thsst, thwind, thrvort
integer                              initflag
!f2py intent(in)                     initflag
real                                 miss
!f2py intent(in)                     miss
!---- out -----
real,dimension(nx,ny)             :: a2tcloc, a2nowflag
!f2py intent(out)                    a2tcloc, a2nowflag
!---- para ----
integer,parameter                 :: miss_int  = -9999
real,parameter                    :: lat_first = -89.5
real,parameter                    :: dlat      = 1.0
real,parameter                    :: dlon      = 1.0
real,parameter                    :: radkm     = 300.0  ! km
!---- calc ----
integer                              itemp
integer                              ix, iy
integer                              xgrids, sgrids, ngrids
integer                              ix_last, iy_last
integer                              ixw,ixe,ixs,ixn
integer                              iyw,iye,iys,iyn
integer                              life, lastpos, dura, pgmax
integer,dimension(7,7)            :: a1xt, a1yt
integer,dimension(nx*ny)          :: a1x, a1y
integer                              xt_temp, yt_temp
integer                              dix, diy, ixt, iyt
integer                              icount
real                                 pgrad
real                                 rvort
real                                 lat, lat_last
real                                 dn, ds, dns, dew
real                                 us, un, vw, ve
real                                 wmaxlow, wmeanlow, wmeanup
real                                 ulow, vlow, uup, vup
real                                 wlow, wup
real                                 tmeanlow, tmeanmid, tmeanup
real                                 dtlow, dtmid, dtup

!--- init ------
a2tcloc   = miss
a2nowflag = miss
!---------------
do iy = 1,ny
  lat = lat_first + (iy -1)*1.0
  dn  = hubeny_real(lat, 0.0, lat+1.0, 0.0)
  ds  = hubeny_real(lat, 0.0, lat-1.0, 0.0)
  dns = (dn + ds)/2.0
  dew = hubeny_real(lat, 0.0, lat, 1.0)
  !-----------------------------
  do ix = 1,nx
    !-- pgrad ----------
    pgrad  = a2pgrad(ix,iy)
    if (pgrad .lt. thpgrad)then
      cycle
    end if
    !-- dura -----------
    life   = a2life(ix,iy)
    call solvelife_point(life, miss_int, dura, pgmax)
    if (real(dura) .lt. thdura)then
      cycle
    end if
    !-- check missing value at center --
    if (a2tlow(ix,iy) .eq. miss)then
      cycle
    end if
    !!-------------------
    lat  = lat_first + dlat*(iy -1)
    CALL gridrange_real(lat, dlat, dlon, radkm*1000.0, ngrids, sgrids, xgrids)
    
    !-- relative vorticity @ low level ---
    dn  = hubeny_real(lat, 0.0, lat+1.0*ngrids, 0.0)
    ds  = hubeny_real(lat, 0.0, lat-1.0*sgrids, 0.0)
    dns = (dn + ds)/2.0
    dew = hubeny_real(lat, 0.0, lat, 1.0*xgrids)
    
    
    call ixy2iixy_saone(ix, iy+ngrids, ixn, iyn)
    call ixy2iixy_saone(ix, iy-sgrids, ixs, iys)
    call ixy2iixy_saone(ix-xgrids, iy, ixw, iyw)
    call ixy2iixy_saone(ix+xgrids, iy, ixe, iye)
    !---
    us  = a2ulow(ixs, iys)
    un  = a2ulow(ixn, iyn)
    vw  = a2vlow(ixw, iyw)
    ve  = a2vlow(ixe, iye)
    !-
    if ( (us.eq.miss).or.(un.eq.miss) )then
      rvort = miss
    else
      rvort  =  (ve - vw)/(dew*2.0) - (un - us)/(dns*2.0) 
    end if
    !-
    if (abs(rvort) .lt. thrvort)then
      cycle
    endif

    !-- check last step -----------
    if (initflag .eq. 0)then
      if (a2sst(ix,iy).lt.thsst)then
        cycle
      else if (a2landsea(ix,iy).gt.0.0)then
        cycle
      endif
    else
      lastpos = a2lastpos(ix,iy)
      if (lastpos .eq. miss_int)then
        if (a2sst(ix,iy).lt.thsst)then
          cycle
        else if (a2landsea(ix,iy).gt.0.0)then
          cycle
        end if
      else
        iy_last = int(lastpos/nx) +1
        ix_last = lastpos - nx*(iy_last-1)
        lat_last= lat_first + (iy_last-1)*1.0
        if (a2lastflag(ix_last,iy_last).gt.0.0)then
          a2nowflag(ix,iy)   = 1.0
        else if (a2sst(ix,iy).lt.thsst)then
          cycle
        else if (a2landsea(ix,iy).gt.0.0)then
          cycle
        endif
      end if
    end if

    !print *,"AAA",ix_last, iy_last, ix,iy

    !-- 7x7 grid box ---------
    do diy = 1,7
      do dix = 1,7
        call ixy2iixy_saone(ix+dix-4, iy+diy-4, xt_temp, yt_temp)
        a1xt(dix, diy) = xt_temp
        a1yt(dix, diy) = yt_temp
      end do
    end do
    !-- vmax & vmean ----------
    wmaxlow  = 0.0
    wmeanlow = 0.0
    wmeanup  = 0.0
    !--
    icount = 7*7
    do diy = 1,7
      do dix = 1,7
        ixt = a1xt(dix, diy)
        iyt = a1yt(dix, diy)
        !--
        ulow = a2ulow(ixt,iyt)
        vlow = a2vlow(ixt,iyt)
        uup  = a2uup(ixt,iyt)
        vup  = a2vup(ixt,iyt)
        !--
        if (ulow.eq.miss)then
          icount = icount -1
          cycle
        end if
        !--
        wlow = ((ulow)**2.0 + (vlow)**2.0)**0.5
        wup  = ((uup)**2.0  + (vup)**2.0)**0.5
        !--
        wmaxlow   = max(wmaxlow, wlow)
        wmeanlow  = wmeanlow + wlow
        wmeanup   = wmeanup  + wup
        !--
      end do
    end do
    if (icount.eq.0)then
      cycle
    endif
    wmeanlow = wmeanlow / icount
    wmeanup  = wmeanup  / icount
    !-- check wmaxlow ---
    if (wmaxlow .lt. thwind)then
      cycle
    end if
    !-- check wmean low and up --
    if (wmeanlow.le.wmeanup)then
      cycle
    endif

    !-- temperature anomaly -----
    lat  = lat_first + dlat*(iy -1)
    CALL circle_xy_real(lat, lat_first, dlon, dlat, radkm*1000.0, miss_int, nx, ny, a1x, a1y)
    !
    tmeanlow  = 0.0
    tmeanmid  = 0.0
    tmeanup   = 0.0
    icount   = 0
    itemp    = 1
    do while (a1x(itemp) .ne. miss_int)
      dix = a1x(itemp)
      diy = a1y(itemp)
      CALL ixy2iixy(ix+dix, iy+diy, nx, ny, ixt, iyt)
      if (a2tlow(ixt, iyt).eq. miss)then
        cycle
      else
        tmeanlow   = tmeanlow + a2tlow(ixt, iyt)
        tmeanmid   = tmeanmid + a2tmid(ixt, iyt)
        tmeanup    = tmeanup  + a2tup(ixt, iyt)
        icount = icount + 1
      end if
      itemp  = itemp +1
    end do
    !-
    if (icount .eq.0)then
      cycle
    else
      tmeanlow  = tmeanlow / real(icount)
      tmeanmid  = tmeanmid / real(icount)
      tmeanup   = tmeanup  / real(icount)
      !
      dtlow     = a2tlow(ix,iy) - tmeanlow  
      dtmid     = a2tmid(ix,iy) - tmeanmid
      dtup      = a2tup(ix,iy)  - tmeanup  
    end if
    a2tcloc(ix,iy)   = dtlow + dtmid + dtup
    a2nowflag(ix,iy) = 1.0
  end do
end do

!--------------
END SUBROUTINE find_tc_saone

!*****************************************************************
SUBROUTINE find_tc_saone_old(a2pgrad, a2life, a2lastpos, a2lastflag, a2tlow, a2tmid, a2tup&
                        &, a2ulow, a2uup, a2vlow, a2vup, a2sst, a2landsea&
                        &, thpgrad, thdura, thsst, thwind, thrvort, initflag, miss&
                        &, nx, ny, a2tcloc, a2nowflag)

implicit none
!---- in ------
integer                              nx, ny
real,dimension(nx,ny)             :: a2pgrad, a2lastflag, a2tlow, a2tmid, a2tup, a2ulow, a2uup, a2vlow, a2vup, a2sst, a2landsea
!f2py intent(in)                     a2pgrad, a2lastflag, a2tlow, a2tmid, a2tup, a2ulow, a2uup, a2vlow, a2vup, a2sst, a2landsea
integer,dimension(nx,ny)          :: a2life, a2lastpos
!f2py intent(in)                     a2life, a2lastpos
real                                 thpgrad, thdura, thsst, thwind, thrvort
!f2py intent(in)                     thpgrad, thdura, thsst, thwind, thrvort
integer                              initflag
!f2py intent(in)                     initflag
real                                 miss
!f2py intent(in)                     miss
!---- out -----
real,dimension(nx,ny)             :: a2tcloc, a2nowflag
!f2py intent(out)                    a2tcloc, a2nowflag
!---- para ----
integer,parameter                 :: miss_int  = -9999
real,parameter                    :: lat_first = -89.5
!---- calc ----
integer                              ix, iy
integer                              ix_last, iy_last
integer                              ixw,ixe,ixs,ixn
integer                              iyw,iye,iys,iyn
integer                              life, lastpos, dura, pgmax
integer,dimension(7,7)            :: a1xt, a1yt
integer                              xt_temp, yt_temp
integer                              dix, diy, ixt, iyt
integer                              icount
real                                 pgrad
real                                 rvort
real                                 lat, lat_last
real                                 dn, ds, dns, dew
real                                 us, un, uw, ue, vs, vn, vw, ve
real                                 wmaxlow, wmeanlow, wmeanup
real                                 ulow, vlow, uup, vup
real                                 wlow, wup
real                                 tlow, tmid, tup
real                                 tmeanlow, tmeanmid, tmeanup
real                                 dtlow, dtmid, dtup

!--- init ------
a2tcloc   = miss
a2nowflag = miss
!---------------
do iy = 1,ny
  lat = lat_first + (iy -1)*1.0
  dn  = hubeny_real(lat, 0.0, lat+1.0, 0.0)
  ds  = hubeny_real(lat, 0.0, lat-1.0, 0.0)
  dns = (dn + ds)/2.0
  dew = hubeny_real(lat, 0.0, lat, 1.0)
  !-----------------------------
  do ix = 1,nx
    !-- pgrad ----------
    pgrad  = a2pgrad(ix,iy)
    if (pgrad .lt. thpgrad)then
      cycle
    end if
    !-- dura -----------
    life   = a2life(ix,iy)
    call solvelife_point(life, miss_int, dura, pgmax)
    if (real(dura) .lt. thdura)then
      cycle
    end if

    !-- relative vorticity ---
    call ixy2iixy_saone(ix, iy+1, ixn, iyn)
    call ixy2iixy_saone(ix, iy-1, ixs, iys)
    call ixy2iixy_saone(ix-1, iy, ixw, iyw)
    call ixy2iixy_saone(ix+1, iy, ixe, iye)
    !---
    us  = a2ulow(ixs, iys)
    un  = a2ulow(ixn, iyn)
    uw  = a2ulow(ixw, iyw)
    ue  = a2ulow(ixe, iye)
    vs  = a2vlow(ixs, iys)
    vn  = a2vlow(ixn, iyn)
    vw  = a2vlow(ixw, iyw)
    ve  = a2vlow(ixe, iye)
    !-
    if ( (us.eq.miss).or.(un.eq.miss).or.(uw.eq.miss).or.(ue.eq.miss) )then
      cycle
    end if
    !
    rvort  = (ve - vw)/(dew*2.0) - (un - us)/(dns*2.0)
    !
    if (abs(rvort) .lt. thrvort)then
      cycle
    endif
    !-- check last step -----------
    if (initflag .eq. 0)then
      if (a2sst(ix,iy).lt.thsst)then
        cycle
      else if (a2landsea(ix,iy).gt.0.0)then
        cycle
      endif
    else
      lastpos = a2lastpos(ix,iy)
      if (lastpos .eq. miss_int)then
        if (a2sst(ix,iy).lt.thsst)then
          cycle
        else if (a2landsea(ix,iy).gt.0.0)then
          cycle
        end if
      else
        iy_last = int(lastpos/nx) +1
        ix_last = lastpos - nx*(iy_last-1)
        lat_last= lat_first + (iy_last-1)*1.0
        if (a2lastflag(ix_last,iy_last).gt.0.0)then
          a2nowflag(ix,iy)   = 1.0
        else if (a2sst(ix,iy).lt.thsst)then
          cycle
        else if (a2landsea(ix,iy).gt.0.0)then
          cycle
        endif
      end if
    end if

    !print *,"AAA",ix_last, iy_last, ix,iy

    !-- 7x7 grid box ---------
    do diy = 1,7
      do dix = 1,7
        call ixy2iixy_saone(ix+dix-4, iy+diy-4, xt_temp, yt_temp)
        a1xt(dix, diy) = xt_temp
        a1yt(dix, diy) = yt_temp
      end do
    end do
    !-- vmax & vmean ----------
    wmaxlow  = 0.0
    wmeanlow = 0.0
    wmeanup  = 0.0
    !--
    icount = 7*7
    do diy = 1,7
      do dix = 1,7
        ixt = a1xt(dix, diy)
        iyt = a1yt(dix, diy)
        !--
        ulow = a2ulow(ixt,iyt)
        vlow = a2vlow(ixt,iyt)
        uup  = a2uup(ixt,iyt)
        vup  = a2vup(ixt,iyt)
        !--
        if (ulow.eq.miss)then
          icount = icount -1
          cycle
        end if
        !--
        wlow = ((ulow)**2.0 + (vlow)**2.0)**0.5
        wup  = ((uup)**2.0  + (vup)**2.0)**0.5
        !--
        wmaxlow   = max(wmaxlow, wlow)
        wmeanlow  = wmeanlow + wlow
        wmeanup   = wmeanup  + wup
        !--
      end do
    end do
    if (icount.eq.0)then
      cycle
    endif
    wmeanlow = wmeanlow / icount
    wmeanup  = wmeanup  / icount
    !-- check wmaxlow ---
    if (wmaxlow .lt. thwind)then
      cycle
    end if
    !-- check wmean low and up --
    if (wmeanlow.le.wmeanup)then
      cycle
    endif
    !-- temperature anomaly -----
    icount = 7*7
    tmeanlow = 0.0
    tmeanmid = 0.0
    tmeanup  = 0.0
    do diy = 1,7
      do dix = 1,7
        ixt = a1xt(dix, diy)
        iyt = a1yt(dix, diy)
        !--
        tlow = a2tlow(ixt,iyt)
        tmid = a2tmid(ixt,iyt)
        tup  = a2tup(ixt,iyt)
        !--
        if (tlow.eq.miss)then
          icount = icount -1
          cycle
        end if
        !--
        tmeanlow  = tmeanlow + tlow
        tmeanmid  = tmeanmid + tmid
        tmeanup   = tmeanup  + tup
        !--
      end do
    end do
    if (icount.eq.0)then
      cycle
    endif
    tmeanlow  = tmeanlow / icount
    tmeanmid  = tmeanmid / icount
    tmeanup   = tmeanup  / icount
    !-------
    dtlow     = a2tlow(ix,iy) - tmeanlow  
    dtmid     = a2tmid(ix,iy) - tmeanmid
    dtup      = a2tup(ix,iy)  - tmeanup  
    !!-------
    !if ((dtlow.lt.0.0).or.(dtmid.lt.0.0).or.(dtup.lt.0.0))then
    !  cycle
    !end if
    !!-------
    !if (dtlow.gt. dtup)then
    !  cycle
    !end if
    !-------
    !-------
    a2tcloc(ix,iy)   = dtlow + dtmid + dtup
    a2nowflag(ix,iy) = 1.0
  end do
end do

!--------------
END SUBROUTINE find_tc_saone_old

!*****************************************************************
!*****************************************************************
SUBROUTINE find_circle_mean(a2in, a2loc, dist, miss, nx, ny, a2out)
implicit none
!---- in ------
integer                              nx, ny
real,dimension(nx,ny)             :: a2in, a2loc
!f2py intent(in)                     a2in, a2loc
real                                 dist, miss  ! dist: (m)
!f2py intent(in)                     dist, miss
!---- out -----
real,dimension(nx,ny)             :: a2out
!f2py intent(out)                    a2out
!---- para ----
real,parameter                    :: lat_first = -89.5
real,parameter                    :: dlat = 1.0
real,parameter                    :: dlon = 1.0
integer,parameter                 :: miss_int = -9999
!---- calc ----
integer                              ix, iy, iix, iiy
integer,dimension(nx*ny)          :: a1x, a1y
integer                              ix_loop, iy_loop
integer                              icount, inum
real                                 mean_temp
real                                 ilat
!--------------
a2out = miss
!--------------
do iy = 1,ny
  ilat = lat_first + (iy -1)*dlat
  
  call circle_xy_real(ilat, lat_first, dlon, dlat, dist, miss_int, nx, ny, a1x, a1y) 

  do ix = 1, nx
    if ( a2loc(ix,iy) .ne. miss)then
      icount = 1
      inum   = 0
      mean_temp   = 0.0
     do while (a1x(icount) .ne. miss_int)
        ix_loop  = ix + a1x(icount)
        iy_loop  = iy + a1y(icount)
        call ixy2iixy(ix_loop, iy_loop, nx, ny, iix, iiy)
        if ( a2in(iix,iiy) .ne. miss)then
          mean_temp = mean_temp + a2in(iix, iiy)
          inum      = inum + 1 
        end if
        icount     = icount + 1
      end do
      if (inum .eq. 0)then
        mean_temp   = miss
      else
        mean_temp   = mean_temp / inum
      end if
      a2out(ix,iy) = mean_temp
    end if  
  end do
end do

RETURN
END SUBROUTINE find_circle_mean
!*****************************************************************
SUBROUTINE find_circle_max(a2in, a2loc, dist, miss, nx, ny, a2out)
implicit none
!---- in ------
integer                              nx, ny
real,dimension(nx,ny)             :: a2in, a2loc
!f2py intent(in)                     a2in, a2loc
real                                 dist, miss  ! dist: (m)
!f2py intent(in)                     dist, miss
!---- out -----
real,dimension(nx,ny)             :: a2out
!f2py intent(out)                    a2out
!---- para ----
real,parameter                    :: lat_first = -89.5
real,parameter                    :: dlat = 1.0
real,parameter                    :: dlon = 1.0
integer,parameter                 :: miss_int = -9999
!---- calc ----
integer                              ix, iy, iix, iiy
integer,dimension(nx*ny)          :: a1x, a1y
integer                              ix_loop, iy_loop
integer                              icount
real                                 max_temp
real                                 ilat
!--------------
a2out = miss
!--------------
do iy = 1,ny
  ilat = lat_first + (iy -1)*dlat
  
  call circle_xy_real(ilat, lat_first, dlon, dlat, dist, miss_int, nx, ny, a1x, a1y) 

  do ix = 1, nx
    if ( a2loc(ix,iy) .ne. miss)then
      icount = 1
      max_temp   = -1.0e+10
     do while (a1x(icount) .ne. miss_int)
        ix_loop  = ix + a1x(icount)
        iy_loop  = iy + a1y(icount)
        call ixy2iixy(ix_loop, iy_loop, nx, ny, iix, iiy)
        if ( a2in(iix,iiy) .ne. miss)then
          max_temp = max(a2in(iix,iiy), max_temp) 
        end if
        icount     = icount + 1
      end do
      if (max_temp .eq. -1.0e+10)then
        max_temp   = miss
      end if
      a2out(ix,iy) = max_temp
    end if  
  end do
end do

RETURN
END SUBROUTINE find_circle_max
!*********************************************************
SUBROUTINE mk_a2highsidevector_saone(a2iso, a2loc, dist, miss, nx, ny, a2vecx, a2vecy)
implicit none
!---- in ------
integer                              nx, ny
real,dimension(nx,ny)             :: a2iso, a2loc
!f2py intent(in)                     a2iso, a2loc
real                                 dist, miss

!---- out -----
real,dimension(nx,ny)             :: a2vecx, a2vecy
!f2py intent(out)                    a2vecx, a2vecy
!---- para ----
real,parameter                    :: lat_first = -89.5
!---- calc ----
integer                              ix, iy
integer                              dx, dy
integer                              iix, iiy
integer                              ixw,ixe,ixs,ixn
integer                              iyw,iye,iys,iyn
real                                 dn, ds, dns, dew
real                                 lat
real                                 gradisox, gradisoy, gradisoabs
real                                 vecx, vecy
!--------------
a2vecx = 0.0
a2vecy = 0.0
!--------------
do iy = 1,ny
  lat = lat_first + (iy -1)*1.0
  dn  = hubeny_real(lat, 0.0, lat+1.0, 0.0)
  ds  = hubeny_real(lat, 0.0, lat-1.0, 0.0)
  dns = (dn + ds)/2.0
  dew = hubeny_real(lat, 0.0, lat, 1.0)
  do ix = 1,nx
    if (a2loc(ix,iy).ne. miss) then
      call ixy2iixy_saone(ix, iy+1, ixn, iyn)
      call ixy2iixy_saone(ix, iy-1, ixs, iys)
      call ixy2iixy_saone(ix-1, iy, ixw, iyw)
      call ixy2iixy_saone(ix+1, iy, ixe, iye)
      gradisox  = (a2iso(ixe,iye)-a2iso(ixw,iyw)) / (2.0*dew)
      gradisoy  = (a2iso(ixn,iyn)-a2iso(ixs,iys)) / (2.0*dns)
      gradisoabs= (gradisox**2.0+gradisoy**2.0)**0.5
      vecx      = gradisox / gradisoabs * dist
      vecy      = gradisoy / gradisoabs * dist
      dx        = int(sign(1.0, vecx))* int((abs(vecx) + 0.5*dew)/ dew)
      dy        = int(sign(1.0, vecy))* int((abs(vecy) + 0.5*dns)/ dns)
      call ixy2iixy_saone(ix+dx, iy+dy, iix, iiy)
      a2vecx(ix,iy) = dx
      a2vecy(ix,iy) = dy
      !a2vecx(ix,iy) = vecx
      !a2vecy(ix,iy) = vecy
    end if
  end do
end do

return
END SUBROUTINE mk_a2highsidevector_saone

!*********************************************************
SUBROUTINE mk_a2highsidemask_saone(a2iso, a2loc, dist, miss, nx, ny, a2out)
implicit none
!---- in ------
integer                              nx, ny
real,dimension(nx,ny)             :: a2iso, a2loc
!f2py intent(in)                     a2iso, a2loc
real                                 dist, miss

!---- out -----
real,dimension(nx,ny)             :: a2out
!f2py intent(out)                    a2out
!---- para ----
real,parameter                    :: lat_first = -89.5
!---- calc ----
integer                              ix, iy
integer                              dx, dy
integer                              iix, iiy
integer                              ixw,ixe,ixs,ixn
integer                              iyw,iye,iys,iyn
real                                 dn, ds, dns, dew
real                                 lat
real                                 gradisox, gradisoy, gradisoabs
real                                 vecx, vecy
!--------------
a2out = miss
!--------------
do iy = 1,ny
  lat = lat_first + (iy -1)*1.0
  dn  = hubeny_real(lat, 0.0, lat+1.0, 0.0)
  ds  = hubeny_real(lat, 0.0, lat-1.0, 0.0)
  dns = (dn + ds)/2.0
  dew = hubeny_real(lat, 0.0, lat, 1.0)
  do ix = 1,nx
    if (a2loc(ix,iy).ne. miss) then
      call ixy2iixy_saone(ix, iy+1, ixn, iyn)
      call ixy2iixy_saone(ix, iy-1, ixs, iys)
      call ixy2iixy_saone(ix-1, iy, ixw, iyw)
      call ixy2iixy_saone(ix+1, iy, ixe, iye)
      gradisox  = (a2iso(ixe,iye)-a2iso(ixw,iyw)) / (2.0*dew)
      gradisoy  = (a2iso(ixn,iyn)-a2iso(ixs,iys)) / (2.0*dns)
      gradisoabs= (gradisox**2.0+gradisoy**2.0)**0.5
      vecx      = gradisox / gradisoabs * dist
      vecy      = gradisoy / gradisoabs * dist
      dx        = int(sign(1.0, vecx))* int((abs(vecx) + 0.5*dew)/ dew)
      dy        = int(sign(1.0, vecy))* int((abs(vecy) + 0.5*dns)/ dns)
      call ixy2iixy_saone(ix+dx, iy+dy, iix, iiy)
      a2out(iix,iiy) = 1.0
    end if
  end do
end do

return
END SUBROUTINE mk_a2highsidemask_saone

!*****************************************************************
SUBROUTINE find_highsidevalue_saone(a2iso, a2loc, a2in, dist, miss, nx, ny, a2out)
implicit none
!---- in ------
integer                              nx, ny
real,dimension(nx,ny)             :: a2iso, a2loc, a2in
!f2py intent(in)                     a2iso, a2loc, a2in
real                                 dist, miss

!---- out -----
real,dimension(nx,ny)             :: a2out
!f2py intent(out)                    a2out
!---- para ----
real,parameter                    :: lat_first = -89.5
!---- calc ----
integer                              ix, iy
integer                              dx, dy
integer                              iix, iiy
integer                              ixw,ixe,ixs,ixn
integer                              iyw,iye,iys,iyn
real                                 dn, ds, dns, dew
real                                 lat
real                                 gradisox, gradisoy, gradisoabs
real                                 vecx, vecy
!--------------
a2out = miss
!--------------
do iy = 1,ny
  lat = lat_first + (iy -1)*1.0
  dn  = hubeny_real(lat, 0.0, lat+1.0, 0.0)
  ds  = hubeny_real(lat, 0.0, lat-1.0, 0.0)
  dns = (dn + ds)/2.0
  dew = hubeny_real(lat, 0.0, lat, 1.0)
  do ix = 1,nx
    if (a2loc(ix,iy).ne. miss) then
      call ixy2iixy_saone(ix, iy+1, ixn, iyn)
      call ixy2iixy_saone(ix, iy-1, ixs, iys)
      call ixy2iixy_saone(ix-1, iy, ixw, iyw)
      call ixy2iixy_saone(ix+1, iy, ixe, iye)
      gradisox  = (a2iso(ixe,iye)-a2iso(ixw,iyw)) / (2.0*dew)
      gradisoy  = (a2iso(ixn,iyn)-a2iso(ixs,iys)) / (2.0*dns)
      gradisoabs= (gradisox**2.0+gradisoy**2.0)**0.5
      vecx      = gradisox / gradisoabs * dist
      vecy      = gradisoy / gradisoabs * dist
      dx        = int(sign(1.0, vecx))* int((abs(vecx) + 0.5*dew)/ dew)
      dy        = int(sign(1.0, vecy))* int((abs(vecy) + 0.5*dns)/ dns)
      call ixy2iixy_saone(ix+dx, iy+dy, iix, iiy)
      a2out(ix,iy) = a2in(iix,iiy)
    end if
  end do
end do

return
END SUBROUTINE find_highsidevalue_saone
!*****************************************************************
SUBROUTINE mk_territory_deg_saone(a2in, ngrids&
                , miss &
                , nx, ny, a2territory )
  implicit none
  !-- input -------------------------------------
  integer                                         nx, ny
  real,dimension(nx,ny)                       ::  a2in
!f2py intent(in)                                  a2in
  integer                                         ngrids  ! [grids]
!f2py intent(in)                                  ngrids
  real                                            miss
!f2py intent(in)                                  miss

  !-- output ------------------------------------
  real,dimension(nx,ny)                       ::  a2territory
!f2py intent(out)                                 a2territory
  !-- calc --------------------------------------
  integer                                         ix, iy, iix, iiy, dx, dy
  !----------------------------------------------
a2territory = miss

do iy = 1, ny
  do ix = 1, nx
    !------------------------
    ! check
    !------------------------
    if (a2in(ix,iy) .eq.miss) cycle

    !- territory ------------
    do dy = -ngrids, ngrids
      do dx = -ngrids, ngrids
        call ixy2iixy( ix+dx, iy+dy, nx, ny, iix, iiy)
        a2territory(iix,iiy) = 1.0
      end do
    end do
    !------------------------
  end do
end do
RETURN
END SUBROUTINE mk_territory_deg_saone

!*****************************************************************
SUBROUTINE mk_territory_saone(a2in, thdist&
                , miss, lat_first, dlat, dlon&
                , nx, ny, a2territory )
  implicit none
  !-- input -------------------------------------
  integer                                         nx, ny
  real,dimension(nx,ny)                       ::  a2in
!f2py intent(in)                                  a2in
  real                                            thdist  ! [m]
!f2py intent(in)                                  thdist
  real                                            miss
!f2py intent(in)                                  miss
  real                                            lat_first, dlat, dlon
!f2py intent(in)                                  lat_first, dlat, dlon


  !-- output ------------------------------------
  real,dimension(nx,ny)                       ::  a2territory
!f2py intent(out)                                 a2territory
  !-- calc --------------------------------------
  integer                                         ix, iy, iix, iiy, ix_loop, iy_loop
  real                                            ilat
  integer,dimension(nx*ny)                     :: a1x, a1y
  integer                                         icount
  integer                                         itemp   ! for test
  !--- para -------------------------------------
  integer,parameter                            :: miss_int = -9999

  !----------------------------------------------
a2territory = miss

itemp = 0
do iy = 1, ny
  do ix = 1, nx
    !------------------------
    ! check
    !------------------------
    if (a2in(ix,iy) .eq.miss) cycle
    !------------------------
    itemp = itemp + 1
    ilat  = lat_first + (iy -1)*dlat
    call circle_xy_real(ilat, lat_first, dlon, dlat, thdist, miss_int, nx, ny, a1x, a1y) 
    !-------------------------
    ! search
    !-------------------------
    icount = 1
    do while ( a1x(icount) .ne. miss_int )
      ix_loop = ix + a1x(icount)
      iy_loop = iy + a1y(icount) 
      call ixy2iixy(ix_loop, iy_loop, nx, ny, iix, iiy)
      !************************************
      a2territory(iix,iiy) = 1.0
      icount = icount + 1
    end do
  end do
end do
RETURN
END SUBROUTINE mk_territory_saone

!*****************************************************************
SUBROUTINE eqgrid_aggr(a2in, a1lat, a1lon, dkm, nrad_kmgrid, iy, ix, miss, ny_in, nx_in, a2sum, a2num)
  implicit none
  !-- input -------------------------------------
  integer                                        ny_in, nx_in

  integer                                        nrad_kmgrid, iy, ix
!f2py intent(in)                                 nrad_kmgrid, iy, ix
  real                                           miss
!f2py intent(in)                              :: miss
  real,dimension(nx_in, ny_in)                :: a2in
!f2py intent(in)                                 a2in
  real,dimension(ny_in)                       :: a1lat
!f2py intent(in)                                 a1lat
  real,dimension(nx_in)                       :: a1lon
!f2py intent(in)                                 a1lon
  real                                           dkm
!f2py intent(in)                                 dkm

  !-- output ------------------------------------
  real,dimension(2*nrad_kmgrid+1, 2*nrad_kmgrid+1)    :: a2sum
!f2py intent(out)                                a2sum
  real,dimension(2*nrad_kmgrid+1, 2*nrad_kmgrid+1)    :: a2num
!f2py intent(out)                                a2num

  !-- calc   ------------------------------------
  integer                                     :: extragrid = 4
  integer                                        ny_kmgrid, nx_kmgrid
  integer                                        iiy_latlongrid, iix_latlongrid
  integer                                        iix_latlongrid_loop
  integer                                        nyrad_latlongrid, nxrad_latlongrid
  integer                                        iiy_kmgrid, iix_kmgrid
  real                                           lat_first, lon_first
  real                                           latc, lonc
  real                                           latt, lont
  real                                           dlat, dlon
  real                                           yradkm, xradkm
  real                                           reskm_latlongrid
  !----------------------------------------------
  ny_kmgrid      = 2*nrad_kmgrid+1
  nx_kmgrid      = 2*nrad_kmgrid+1 

  !----------------------------------------------
  dlat           = a1lat(2) - a1lat(1)
  dlon           = a1lon(2) - a1lon(1)
  lat_first      = a1lat(1)
  lon_first      = a1lon(1)

  latc           = a1lat(iy)
  lonc           = a1lon(ix)
  nyrad_latlongrid   = latgrids_real(latc, dlat, nrad_kmgrid*dkm*1000.0)

  !----------------------------------------------
  !--- initialize -------------------------------
  a2sum  = 0.0
  a2num  = 0.0
  !--- aggregate --------------------------------
  do iiy_latlongrid = iy - nyrad_latlongrid -extragrid, iy + nyrad_latlongrid +extragrid
    !-------------
    if ((iiy_latlongrid <=0).or.(iiy_latlongrid > ny_in)) cycle

    !-------------
    latt       =  lat_first + (iiy_latlongrid -1) * dlat
    yradkm     =  hubeny_real(latc, 0.0, latt, 0.0)*0.001    ! [km]
    iiy_kmgrid =  int((yradkm + 0.5*dkm)/dkm) * int( sign( 1.0, latt - latc)) + (nrad_kmgrid + 1)
    
    !-- check iiy_kmgrid
    if ((iiy_kmgrid .le. 0).or.(iiy_kmgrid .gt. ny_kmgrid))cycle

    !-------------
    nxrad_latlongrid   = longrids_real(latt, dlon, nrad_kmgrid*dkm*1000.0)

    reskm_latlongrid  = hubeny_real( latt,  0.0, latt, dlon) * 0.001 ![km]
    do iix_latlongrid_loop = ix - nxrad_latlongrid -extragrid, ix + nxrad_latlongrid +extragrid
      !----------------
      !if (( iix_latlongrid_loop <= 0).or.( iix_latlongrid_loop > nx_in))cycle
      if ( iix_latlongrid_loop <= 0) then
        iix_latlongrid   = nx_in + iix_latlongrid_loop

      else if (iix_latlongrid_loop > nx_in) then
        iix_latlongrid   = iix_latlongrid_loop - nx_in

      else
        iix_latlongrid   = iix_latlongrid_loop
      endif

      !----------------
      lont       =  lon_first + (iix_latlongrid -1) * dlon
      xradkm     =  reskm_latlongrid * abs(iix_latlongrid_loop - ix)  !<- use iix_latlongrid_loop, not iix_latlongrid
      iix_kmgrid =  int((xradkm + 0.5*dkm)/dkm) * sign( 1, iix_latlongrid_loop - ix ) + ( nrad_kmgrid + 1)

      !-- check iix_kmgrid
      if ((iix_kmgrid .le. 0).or.(iix_kmgrid .gt. nx_kmgrid))cycle

      !-- check miss value -------
      if (a2in(iix_latlongrid, iiy_latlongrid) .eq. miss)cycle

      !-- sum up -------
      a2sum(iix_kmgrid, iiy_kmgrid) = a2sum(iix_kmgrid, iiy_kmgrid) + a2in(iix_latlongrid, iiy_latlongrid)
      !a2sum(iix_kmgrid, iiy_kmgrid) = a2sum(iix_kmgrid, iiy_kmgrid) + lont
      !a2sum(iix_kmgrid, iiy_kmgrid) = lont

      a2num(iix_kmgrid, iiy_kmgrid) = a2num(iix_kmgrid, iiy_kmgrid) + 1

      !a2num(iix_kmgrid, iiy_kmgrid) = a2num(iix_kmgrid, iiy_kmgrid) + abs(yradkm)
      !------------------------------------------------
    enddo
  enddo
RETURN
END SUBROUTINE eqgrid_aggr

!*****************************************************************
SUBROUTINE aggr_pr(a2life, a2pgrad, thdist, thdura&
                , miss_int,miss_dbl, lat_first, dlat&
                , dlon, nx, ny, a2territory, a2dist )
  implicit none
  !-- input -------------------------------------
  integer                                         nx, ny
  integer,dimension(nx,ny)                     :: a2life, a2pgrad
!f2py intent(in)                                  a2life, a2pgrad
  double precision                                thdist
!f2py intent(in)                                  thdist
  integer                                         thdura
!f2py intent(in)                                  thdura
  integer                                         miss_int
!f2py intent(in)                                  miss_int
  double precision                                miss_dbl
!f2py intent(in)                                  miss_dbl
  double precision                                lat_first, dlat, dlon
!f2py intent(in)                                  lat_first, dlat, dlon


  !-- output ------------------------------------
  double precision,dimension(nx,ny)           ::  a2territory, a2dist
!f2py intent(out)                                 a2territory, a2dist
  !-- calc --------------------------------------
  integer                                         ix, iy, iix, iiy, ix_loop, iy_loop
  double precision                                ilat, iilat
  integer                                         life, dura, pgmax
  integer,dimension(nx*ny)                     :: a1x, a1y
  integer                                         icount
  double precision                                dist
  integer                                         itemp   ! for test
  !----------------------------------------------
a2dist      = miss_dbl
a2territory = miss_dbl

itemp = 0
do iy = 1, ny
  do ix = 1, nx
    life = a2life(ix,iy)
    if (life .ne. miss_int) then
      itemp = itemp + 1
      ilat  = lat_first + (iy -1)*dlat
      call solvelife_point(life, miss_int, dura, pgmax)
      if (dura .gt. thdura)then
        call circle_xy(ilat, lat_first, dlon, dlat, thdist, miss_int, nx, ny, a1x, a1y) 
        !-------------------------
        ! search
        !------------------    -------
        icount = 1
        do while ( a1x(icount) .ne. miss_int )
          ix_loop = ix + a1x(icount)
          iy_loop = iy + a1y(icount) 
          call ixy2iixy(ix_loop, iy_loop, nx, ny, iix, iiy)
          !************************************
          iilat = lat_first + (iiy -1)*dlat
          dist  = hubeny(ilat, 0.0d0, iilat, dlon*(a1x(icount)))
          !dist  = hubeny(ilat, 0.0d0, iilat, 0.0d0)

          !!******************
          !! for test
          !!******************
          !if (itemp .eq. 70) then
          !  print *, iix, iiy, a1x(icount), a1y(icount), dist
          !  a2dist(iix,iiy) = dist
          !  a2territory(iix,iiy) = 1
          !end if
          !!******************
          !----------
          ! when the iix, iiy grid has been found before
          !----------
          if (a2territory(iix, iiy) .ne. miss_dbl)then
            if (dist .lt. a2dist(iix, iiy))then
              a2dist(iix, iiy)      = dist
              a2territory(iix, iiy) = a2pgrad(ix, iy)
            else if (dist .eq. a2dist(iix, iiy))then
              if ( a2pgrad(ix, iy) .gt. a2territory(iix,iiy) )then
                a2dist(iix, iiy)      = dist
                a2territory(iix, iiy) = a2pgrad(ix, iy)
              end if 
            end if
          !----------
          ! when the iix. iiy grid is found for the first time
          !----------
          else
            a2dist(iix, iiy)      = dist
            a2territory(iix, iiy) = a2pgrad(ix, iy)
          end if
          !---
          icount = icount + 1
        end do
      end if
    end if
  end do
end do
RETURN
END SUBROUTINE aggr_pr
!*****************************************************************
SUBROUTINE solvelife_point(life, miss_int, dura, pgmax)
  implicit none
  !**************************************
  !** for input 
  !**************************************
  integer                                         life
!f2py intent(in)                                  life
  integer                                         miss_int
!f2py intent(in)                                  miss_int
  !**************************************
  !** for output
  !**************************************
  integer                                         pgmax, dura
!f2py intent(out)                                 pgmax, dura
  !**************************************
  !*s for calc
  !**************************************
  !**************************************
if (life .eq. miss_int) then
  dura  = miss_int
  pgmax = miss_int
else
  dura  = int(life /1000000)
  pgmax = life - dura*1000000
end if

RETURN
END SUBROUTINE solvelife_point
!*****************************************************************
SUBROUTINE solvelife(a2life, miss_int, nx, ny, a2dura, a2pgmax)
  implicit none
  !**************************************
  !** for input 
  !**************************************
  integer                                         nx, ny
  integer,dimension(nx, ny)                    :: a2life
!f2py intent(in)                                  a2life
  integer                                         miss_int
!f2py intent(in)                                  miss_int
  !**************************************
  !** for output
  !**************************************
  integer,dimension(nx, ny)                    :: a2pgmax, a2dura
!f2py intent(out)                                 a2pgmax, a2dura
  !**************************************
  !** for calc
  !**************************************
  integer                                         ix, iy
  integer                                         life
  integer                                         dura, pgmax
  !**************************************
do iy = 1, ny
  do ix = 1, nx
    life = a2life(ix, iy)
    !if (life .eq. miss_int) then
    !  a2dura(ix,iy)  = miss_int
    !  a2pgmax(ix,iy) = miss_int
    !else
    !  a2dura(ix,iy)  = int(life /1000000)
    !  a2pgmax(ix,iy) = life - a2dura(ix,iy)*1000000
    !end if
    call solvelife_point(life, miss_int, dura, pgmax)
    a2dura(ix,iy)  = dura
    a2pgmax(ix,iy) = pgmax
  end do
end do 

RETURN
END SUBROUTINE solvelife
!*****************************************************************
SUBROUTINE connectc(&
        &  a2pgrad0, a2pgrad1, a2ua0, a2va0&
        &, a2pgmax0, a2ipos0, a2idate0, a2time0&
        &, a1lon, a1lat, thdp, thdist, hinc, miss_dbl, miss_int&
        &, year1, mon1, day1, hour1&
        &, a2lastpos1, a2pgmax1, a2ipos1, a2idate1, a2time1&
        &, nx, ny)
  implicit none  
  !**************************************
  ! a2lastpos returns nx*(iy -1) + ix
  ! where ix = 1,2, .. nx,   iy = 1, 2, .. ny
  ! NOT ix = 0, 1, .. nx-1,  iy = 0, 1, .. ny

  !**************************************
  !** for input 
  !**************************************
  integer                                          nx, ny
  double precision,dimension(nx, ny)            :: a2pgrad0, a2pgrad1, a2ua0, a2va0
!f2py intent(in)                                   a2pgrad0, a2pgrad1, a2ua0, a2va0
  double precision,dimension(nx, ny)            :: a2pgmax0
!f2py intent(in)                                   a2pgmax0
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
  double precision,dimension(nx,ny)             :: a2pgmax1
!f2py intent(out)                                  a2pgmax1
  integer,dimension(nx, ny)                     :: a2lastpos1, a2ipos1, a2idate1, a2time1
!f2py intent(out)                                  a2lastpos1, a2ipos1, a2idate1, a2time1
  !**************************************
  !** for calc 
  !**************************************
  integer                                          ix0, iy0, ix1, iy1, iix1, iiy1, iix, iiy, iix_loop, iiy_loop
  integer                                          ngrids, sgrids, xgrids, ygrids
  double precision                                 lat0, lon0, lat1, lon1
  double precision                                 ua0, va0, dp0
  double precision                                 dp1
  double precision                                 londist, latdist
  double precision                                 dlat, dlon
  double precision                                 iilon, iilat
  double precision                                 iidist, iidp
  double precision                                 iidist_temp, iidp_temp
  integer                                          xx, yy
  !integer,dimension(nx*ny)                      :: a1x, a1y
  !integer,dimension(8)                           :: a1surrx, a1suury
  integer                                          cflag
!------------------------------------------------------------
dlat  = a1lat(2) - a1lat(1)
dlon  = a1lon(2) - a1lon(1)
!************************************************
! initialize 
!------------------------------------------------
a2lastpos1 = miss_int
a2pgmax1   = miss_dbl
a2ipos1    = miss_int
a2idate1   = miss_int
a2time1    = miss_int
!************************************************
! search cyclone same as previous timestep
!------------------------------------------------
do iy0 = 1, ny
  do ix0 = 1, nx
    if (a2pgrad0(ix0,iy0) .ne. miss_dbl) then
      dp0 = a2pgrad0(ix0,iy0)
      if ( dp0 .gt. thdp ) then
        !-----------------
        lat0    = a1lat(iy0)
        lon0    = a1lon(ix0) 
        ua0     = a2ua0(ix0, iy0)
        va0     = a2va0(ix0, iy0)
        !pmean0  = a2pmean0(ix0, iy0)
        !psl0    = a2psl0(ix0, iy0)
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
            if (a2pgrad1(iix,iiy) .ne. miss_dbl) then
              !iipsl        = a2psl1(iix, iiy)
              iidp_temp    = a2pgrad1(iix,iiy)
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
          !--------------
          ! make pgmax
          !--------------
          a2lastpos1(xx, yy) = nx * (iy0-1) + ix0
          if ( a2pgmax0(ix0, iy0) .eq. miss_dbl )then
            a2pgmax1(xx,yy)     = a2pgrad1(xx, yy)
          else if ( a2pgrad1(xx, yy) .gt. a2pgmax0(ix0, iy0)) then
            a2pgmax1(xx,yy)     = a2pgrad1(xx, yy)
          else
            a2pgmax1(xx,yy)     = a2pgmax0(ix0, iy0)
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
    if (a2pgrad1(xx,yy) .ne. miss_dbl) then
      if (a2lastpos1(xx,yy) .eq. miss_int) then
        dp1 = a2pgrad1(xx,yy)
        if ( dp1 .gt. thdp )then
          a2pgmax1(xx,yy)  = a2pgrad1(xx, yy)
          a2ipos1(xx,yy)  = (yy -1)*nx + xx
          a2idate1(xx,yy) = year1*10**6 + mon1*10**4 + day1*10**2 + hour1
          a2time1(xx,yy)  = 0
        end if
      end if
    end if
  end do
end do    
!-----
RETURN
END SUBROUTINE connectc

!*****************************************************************



!*****************************************************************
SUBROUTINE connectc_old(&
        &  a2pmean0, a2pmean1, a2psl0, a2psl1, a2ua0, a2va0&
        &, a2pgmax0, a2ipos0, a2idate0, a2time0&
        &, a2pgrad1&
        &, a1lon, a1lat, thdp, thdist, hinc, miss_dbl, miss_int&
        &, year1, mon1, day1, hour1&
        &, a2lastpos1, a2pgmax1, a2ipos1, a2idate1, a2time1&
        &, nx, ny)
  implicit none  
  !**************************************
  ! a2lastpos returns nx*(iy -1) + ix
  ! where ix = 1,2, .. nx,   iy = 1, 2, .. ny
  ! NOT ix = 0, 1, .. nx-1,  iy = 0, 1, .. ny

  !**************************************
  !** for input 
  !**************************************
  integer                                          nx, ny
  double precision,dimension(nx, ny)            :: a2pmean0, a2pmean1, a2psl0, a2psl1, a2ua0, a2va0
!f2py intent(in)                                   a2pmean0, a2pmean1, a2psl0, a2psl1, a2ua0, a2va0
  double precision,dimension(nx, ny)            :: a2pgmax0
!f2py intent(in)                                   a2pgmax0
  integer,dimension(nx,ny)                      :: a2ipos0, a2idate0, a2time0
!f2py intent(in)                                   a2ipos0, a2idate0, a2time0
  double precision,dimension(nx, ny)            :: a2pgrad1
!f2py intent(in)                                   a2pgrad1
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
  double precision,dimension(nx,ny)             :: a2pgmax1
!f2py intent(out)                                  a2pgmax1
  integer,dimension(nx, ny)                     :: a2lastpos1, a2ipos1, a2idate1, a2time1
!f2py intent(out)                                  a2lastpos1, a2ipos1, a2idate1, a2time1
  !**************************************
  !** for calc 
  !**************************************
  integer                                          ix0, iy0, ix1, iy1, iix1, iiy1, iix, iiy, iix_loop, iiy_loop
  integer                                          ngrids, sgrids, xgrids, ygrids
  double precision                                 lat0, lon0, lat1, lon1
  double precision                                 ua0, va0, pmean0, psl0, dp0
  double precision                                 dp1
  double precision                                 londist, latdist
  double precision                                 dlat, dlon
  double precision                                 iilon, iilat, iipmean, iipsl
  double precision                                 iidist, iidp
  double precision                                 iidist_temp, iidp_temp
  integer                                          xx, yy
  !integer,dimension(nx*ny)                      :: a1x, a1y
  !integer,dimension(8)                           :: a1surrx, a1suury
  integer                                          cflag
!------------------------------------------------------------
dlat  = a1lat(2) - a1lat(1)
dlon  = a1lon(2) - a1lon(1)
!************************************************
! initialize 
!------------------------------------------------
a2lastpos1 = miss_int
a2pgmax1   = miss_dbl
a2ipos1    = miss_int
a2idate1   = miss_int
a2time1    = miss_int
!************************************************
! search cyclone same as previous timestep
!------------------------------------------------
do iy0 = 1, ny
  do ix0 = 1, nx
    if (a2pmean0(ix0,iy0) .ne. miss_dbl) then
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
          !--------------
          ! make pgmax
          !--------------
          a2lastpos1(xx, yy) = nx * (iy0-1) + ix0
          if ( a2pgmax0(ix0, iy0) .eq. miss_dbl )then
            a2pgmax1(xx,yy)     = a2pgrad1(xx, yy)
          else if ( a2pgrad1(xx, yy) .gt. a2pgmax0(ix0, iy0)) then
            a2pgmax1(xx,yy)     = a2pgrad1(xx, yy)
          else
            a2pgmax1(xx,yy)     = a2pgmax0(ix0, iy0)
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
          a2pgmax1(xx,yy)  = a2pgrad1(xx, yy)
          a2ipos1(xx,yy)  = (yy -1)*nx + xx
          a2idate1(xx,yy) = year1*10**6 + mon1*10**4 + day1*10**2 + hour1
          a2time1(xx,yy)  = 0
        end if
      end if
    end if
  end do
end do    
!-----
RETURN
END SUBROUTINE connectc_old

!*****************************************************************
!*****************************************************************
SUBROUTINE mk_8gridsxy(x, y, nx, ny, a1surrx, a1surry)
  implicit none
  !-- for input -------------------
  integer                                       x, y, nx, ny
!f2py intent(in)                                x, y, nx, ny
  !-- for output ------------------
  integer,dimension(8)                      :: a1surrx, a1surry
!f2py intent(out)                               a1surrx, a1surry
  !-- for calc --------------------
  integer                                       i, ix_loop, iy_loop, ix, iy
!----------------------------------
i = 0
do iy_loop = y -1, y+1, 2
  do ix_loop = x-1, x+1
    call ixy2iixy(ix_loop, iy_loop, nx, ny, ix, iy)
    i = i + 1
    a1surrx(i) = ix
    a1surry(i) = iy
  end do
end do
!-----------
i = i +1
ix_loop = x-1
iy_loop = y
call ixy2iixy(ix_loop, iy_loop, nx, ny, ix, iy)
a1surrx(i) = ix
a1surry(i) = iy
!-----------
i = i +1
ix_loop = x+1
iy_loop = y
call ixy2iixy(ix_loop, iy_loop, nx, ny, ix, iy)
a1surrx(i) = ix
a1surry(i) = iy
!-----------
RETURN
END SUBROUTINE mk_8gridsxy
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
!*****************************************************************
SUBROUTINE findcyclone_real(a2psl, a1lat, a1lon, miss_in, miss_out, nx, ny, a2pmean, a2pgrad)
  implicit none
  !** for input ---------------------------------------------
  integer                                           nx, ny
  real,dimension(nx ,ny)                         :: a2psl
!f2py intent(in)                                    a2psl
  real,dimension(ny)                             :: a1lat
!f2py intent(in)                                    a1lat
  real,dimension(nx)                             :: a1lon
!f2py intent(in)                                    a1lon
  real                                              miss_in, miss_out
!f2py intent(in)                                    miss_in, miss_out
  !** for output --------------------------------------------
  real,dimension(nx, ny)                         :: a2pmean, a2pgrad
!f2py intent(out)                                   a2pmean, a2pgrad
  !** for calc  ---------------------------------------------
  integer                                           ix, iy, ik
  integer                                           iix, iiy, iiix, iiiy, ix_surr, iy_surr
  integer                                           iy_surr_rad, ix_surr_rad
  integer                                           validnum, flag
  integer                                        :: miss_int = -9999
  real                                              pmean, psl, pgrad, pgrad_temp
  real                                              dist_surr
  real                                              lat, lon, lat_surr, lon_surr
  real                                              lat_first, dlat, dlon
  real                                           :: thdist = 300.0*1000.0  ! (300km)
  real,dimension(8)                              :: a1ambi
  integer,dimension(nx*ny)                       :: a1surrx, a1surry

  !----------------------------------------------------------
lat_first = a1lat(1)
dlat      = a1lat(2) - a1lat(1)
dlon      = a1lon(2) - a1lon(1)

!------------------
a2pmean = miss_out
a2pgrad = miss_out
do iy = 1, ny
  do ix = 1, nx
    psl = a2psl(ix, iy)
    if (psl .ne. miss_in) then
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
      if (flag .eq. 0) then

        lat = a1lat(iy)
        lon = a1lon(ix) 
        !call mk_8gridsxy(ix, iy, nx, ny, a1surrx, a1surry)
        call circle_xy_real(lat, lat_first, dlon, dlat, thdist, miss_int, nx, ny, a1surrx, a1surry)
        pmean  = 0.0
        pgrad  = 0.0
        validnum= 0
        do ik = 1, nx*ny

          ix_surr_rad = a1surrx(ik)
          iy_surr_rad = a1surry(ik)
          if ((ix_surr_rad .eq. miss_int) .or. (iy_surr_rad .eq. miss_int)) cycle

          ix_surr  = roundx(ix + ix_surr_rad, nx)
          iy_surr  = iy + iy_surr_rad
          if ((iy_surr .le. 0) .or. (iy_surr .gt. ny)) cycle
          if (a2psl(ix_surr, iy_surr) .eq. miss_in) cycle
          if ( (ix_surr .eq. ix) .and. (iy_surr .eq. iy) ) cycle

          lon_surr = a1lon(ix_surr)
          lat_surr = a1lat(iy_surr)

          validnum = validnum + 1
          !------------
          ! make pgrad
          !------------
          dist_surr  = hubeny_real(lat, lon, lat_surr, lon_surr)
          pgrad_temp = ( a2psl(ix_surr, iy_surr) - a2psl(ix, iy) )/dist_surr * 1000.0 * 1000.0    ![Pa/1000km]

          pgrad      = pgrad + pgrad_temp
          pmean      = pmean + a2psl(ix_surr, iy_surr)

        end do

        if (validnum .eq. 0)then
          pmean = miss_out
          pgrad = miss_out
        else
          pmean = pmean /real(validnum)
          pgrad = pgrad /real(validnum)
        end if
        a2pmean(ix, iy) = pmean
        a2pgrad(ix, iy) = pgrad

      end if
    end if

    !---------------
  end do
end do

RETURN
END SUBROUTINE findcyclone_real




!*****************************************************************
SUBROUTINE findcyclone_dbl(a2psl, a1lat, a1lon, miss_in, miss_out, nx, ny, a2pmean, a2pgrad)
  implicit none
  !** for input ---------------------------------------------
  integer                                           nx, ny
  double precision,dimension(nx ,ny)             :: a2psl
!f2py intent(in)                                    a2psl
  double precision,dimension(ny)                 :: a1lat
!f2py intent(in)                                    a1lat
  double precision,dimension(nx)                 :: a1lon
!f2py intent(in)                                    a1lon
  double precision                                  miss_in, miss_out
!f2py intent(in)                                    miss_in, miss_out
  !** for output --------------------------------------------
  double precision,dimension(nx, ny)             :: a2pmean, a2pgrad
!f2py intent(out)                                   a2pmean, a2pgrad
  !** for calc  ---------------------------------------------
  integer                                           ix, iy, ik
  integer                                           iix, iiy, iiix, iiiy, ix_surr, iy_surr
  integer                                           iy_surr_rad, ix_surr_rad
  integer                                           validnum, flag
  integer                                        :: miss_int = -9999
  double precision                                  pmean, psl, pgrad, pgrad_temp
  double precision                                  dist_surr
  double precision                                  lat, lon, lat_surr, lon_surr
  double precision                                  lat_first, dlat, dlon
  double precision                               :: thdist = 300.0d0*1000.0d0  ! (300km)
  double precision,dimension(8)                  :: a1ambi
  integer,dimension(nx*ny)                       :: a1surrx, a1surry

  !----------------------------------------------------------
lat_first = a1lat(1)
dlat      = a1lat(2) - a1lat(1)
dlon      = a1lon(2) - a1lon(1)

!------------------
a2pmean = miss_out
a2pgrad = miss_out
do iy = 1, ny
  do ix = 1, nx
    psl = a2psl(ix, iy)
    if (psl .ne. miss_in) then
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
      if (flag .eq. 0) then

        lat = a1lat(iy)
        lon = a1lon(ix) 
        !call mk_8gridsxy(ix, iy, nx, ny, a1surrx, a1surry)
        call circle_xy(lat, lat_first, dlon, dlat, thdist, miss_int, nx, ny, a1surrx, a1surry)
        pmean  = 0.0d0
        pgrad  = 0.0d0
        validnum= 0
        do ik = 1, nx*ny

          ix_surr_rad = a1surrx(ik)
          iy_surr_rad = a1surry(ik)
          if ((ix_surr_rad .eq. miss_int) .or. (iy_surr_rad .eq. miss_int)) cycle

          ix_surr  = roundx(ix + ix_surr_rad, nx)
          iy_surr  = iy + iy_surr_rad
          if ((iy_surr .le. 0) .or. (iy_surr .gt. ny)) cycle
          if (a2psl(ix_surr, iy_surr) .eq. miss_in) cycle
          if ( (ix_surr .eq. ix) .and. (iy_surr .eq. iy) ) cycle

          lon_surr = a1lon(ix_surr)
          lat_surr = a1lat(iy_surr)

          validnum = validnum + 1
          !------------
          ! make pgrad
          !------------
          dist_surr  = hubeny(lat, lon, lat_surr, lon_surr)
          pgrad_temp = ( a2psl(ix_surr, iy_surr) - a2psl(ix, iy) )/dist_surr * 1000.0d0 * 1000.0d0    ![Pa/1000km]

          pgrad      = pgrad + pgrad_temp
          pmean      = pmean + a2psl(ix_surr, iy_surr)

          if (pgrad_temp .gt. 1000000.0d0)then
            print *, pgrad_temp, a2psl(ix_surr, iy_surr), dist_surr
            print *, ix_surr, iy_surr
            stop
          endif
        end do

        if (validnum .eq. 0)then
          pmean = miss_out
          pgrad = miss_out
        else
          pmean = pmean /dble(validnum)
          pgrad = pgrad /dble(validnum)
        end if
        a2pmean(ix, iy) = pmean
        a2pgrad(ix, iy) = pgrad

      end if
    end if

    !---------------
  end do
end do

RETURN
END SUBROUTINE findcyclone_dbl

!*****************************************************************
SUBROUTINE findcyclone_old(a2psl, a1lat, a1lon, miss_in, miss_out, nx, ny, a2pmean, a2pgrad)
  implicit none
  !** for input ---------------------------------------------
  integer                                           nx, ny
  double precision,dimension(nx ,ny)             :: a2psl
!f2py intent(in)                                    a2psl
  double precision,dimension(ny)                 :: a1lat
!f2py intent(in)                                    a1lat
  double precision,dimension(nx)                 :: a1lon
!f2py intent(in)                                    a1lon
  double precision                                  miss_in, miss_out
!f2py intent(in)                                    miss_in, miss_out
  !** for output --------------------------------------------
  double precision,dimension(nx, ny)             :: a2pmean, a2pgrad
!f2py intent(out)                                   a2pmean, a2pgrad
  !** for calc  ---------------------------------------------
  integer                                           ix, iy, ik
  integer                                           iix, iiy, iiix, iiiy, ix_surr, iy_surr
  integer                                           icount, validnum, flag
  double precision                                  pmean, psl, pgrad, pgrad_temp
  double precision                                  dist_surr
  double precision                                  lat, lon, lat_surr, lon_surr
  double precision,dimension(8)                  :: a1ambi
  integer,dimension(8)                           :: a1surrx, a1surry

  !----------------------------------------------------------
do iy = 1, ny
  do ix = 1, nx
    psl = a2psl(ix, iy)
    if (psl .eq. miss_in)then
      a2pmean(ix,iy) = miss_out
      a2pgrad(ix,iy) = miss_out
    else
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
        a2pgrad(ix, iy) = miss_out
      else if (flag .eq. 0) then
        lat = a1lat(iy)
        lon = a1lon(ix) 
        call mk_8gridsxy(ix, iy, nx, ny, a1surrx, a1surry)
        pmean  = 0.0d0
        pgrad  = 0.0d0
        icount = 0
        validnum= 0
        do ik = 1, 8
          icount   = icount + 1
          ix_surr  = a1surrx(ik)
          iy_surr  = a1surry(ik)
          lon_surr = a1lon(ix_surr)
          lat_surr = a1lat(iy_surr)
          if ( a1ambi(ik) .ne. miss_in)then
            validnum = validnum + 1
            !------------
            ! make pgrad
            !------------
            dist_surr  = hubeny(lat, lon, lat_surr, lon_surr)
            pgrad_temp = ( a2psl(ix_surr, iy_surr) - a2psl(ix, iy) )/dist_surr * 1000.0 * 1000.0    ![Pa/1000km]
            pgrad      = pgrad + pgrad_temp
            !------------
            pmean = pmean + a1ambi(ik)
          end if
        end do
        if (validnum .eq. 0)then
          pmean = miss_out
          pgrad = miss_out
        else
          pmean = pmean /validnum
          pgrad = pgrad /validnum
        end if
        a2pmean(ix, iy) = pmean
        a2pgrad(ix, iy) = pgrad
      end if
    end if
    !---------------
  end do
end do

RETURN
END SUBROUTINE findcyclone_old
!*****************************************************************
!*****************************************************************
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
END SUBROUTINE ixy2iixy
!*****************************************************************
SUBROUTINE circle_xy_light(lat, lat_first, dlon, dlat, thdist, miss_int, nx, ny, nlen_out, a1x, a1y)
  implicit none
  !-- input -----------------------------
  integer                               nx, ny, nlen_out
  double precision                      lat, lat_first, dlon, dlat
!f2py intent(in)                        lat, lat_first, dlon, dlat
  double precision                      thdist  ![m]
!f2py intent(in)                        thdist  ![m]
  integer                               miss_int
!f2py intent(in)                        miss_int
  !-- output ----------------------------
  integer,dimension(nlen_out)        :: a1x, a1y
!f2py intent(out)                       a1x, a1y
  !-- calc ------------------------------
  integer                               icount
  integer                               x, y, ix, iy, ix_loop, iy_loop
  integer                               ngrids, sgrids, xgrids, ygrids
  double precision                      idist, ilat, ilon
  double precision                      lon
!****************************************
! search
!----------------------------------------
lon       = 0.0d0
x  = 1
y  = int((lat - lat_first)/dlat) + 1
!-----------
! set range
!***********
call gridrange(lat, dlat, dlon, thdist, ngrids, sgrids, xgrids)
if (sgrids .ge. ngrids )then
  ygrids = sgrids
else
  ygrids = ngrids
end if
!--
!-----------
! search loop
!***********
icount = 0
a1x    = miss_int
a1y    = miss_int

do iy_loop = -ygrids, ygrids
  do ix_loop = -xgrids, xgrids

    call ixy2iixy(ix_loop, iy_loop, nx, ny, ix, iy)
    ilat        = lat + iy_loop *dlat
    ilon        = lon + ix_loop *dlon
    idist       = hubeny(lat, lon, ilat, ilon)

    if (idist .lt. thdist) then
      icount = icount + 1
      a1x(icount) = ix_loop   ! not ix
      a1y(icount) = iy_loop   ! not iy
    end if
    if (icount .eq. nlen_out)then
      exit
    endif
  end do
end do

 
RETURN
END SUBROUTINE circle_xy_light

!*****************************************************************
SUBROUTINE circle_xy_real(lat, lat_first, dlon, dlat, thdist, miss_int, nx, ny, a1x, a1y)
  implicit none
  !-- input -----------------------------
  integer                               nx, ny
  real                                  lat, lat_first, dlon, dlat
!f2py intent(in)                        lat, lat_first, dlon, dlat
  real                                  thdist  ![m]
!f2py intent(in)                        thdist  ![m]
  integer                               miss_int
!f2py intent(in)                        miss_int
  !-- output ----------------------------
  integer,dimension(nx*ny)           :: a1x, a1y
!f2py intent(out)                       a1x, a1y
  !-- calc ------------------------------
  integer                               icount
  integer                               x, y, ix, iy, ix_loop, iy_loop
  integer                               ngrids, sgrids, xgrids, ygrids
  real                                  idist, ilat, ilon
  real                                  lon
!****************************************
! search
!----------------------------------------
lon       = 0.0
x  = 1
y  = int((lat - lat_first)/dlat) + 1
!-----------
! set range
!***********
call gridrange_real(lat, dlat, dlon, thdist, ngrids, sgrids, xgrids)
if (sgrids .ge. ngrids )then
  ygrids = sgrids
else
  ygrids = ngrids
end if
!--
!-----------
! search loop
!***********
icount = 0
a1x    = miss_int
a1y    = miss_int
if (xgrids .ne. 0)then
  do iy_loop = -ygrids, ygrids
    do ix_loop = -xgrids, xgrids
  
      call ixy2iixy(ix_loop, iy_loop, nx, ny, ix, iy)
      ilat        = lat + iy_loop *dlat
      ilon        = lon + ix_loop *dlon
      idist       = hubeny_real(lat, lon, ilat, ilon)
  
      if (idist .lt. thdist) then
        icount = icount + 1
        a1x(icount) = ix_loop   ! not ix
        a1y(icount) = iy_loop   ! not iy
      end if
    end do
  end do
else
  do iy_loop = -ygrids, ygrids
    ix_loop = 0
    call ixy2iixy(ix_loop, iy_loop, nx, ny, ix, iy)
    ilat        = lat + iy_loop *dlat
    ilon        = lon + ix_loop *dlon
    idist       = hubeny_real(lat, lon, ilat, ilon)
  
    if (idist .lt. thdist) then
      icount = icount + 1
      a1x(icount) = ix_loop   ! not ix
      a1y(icount) = iy_loop   ! not iy
    end if
  end do
end if

 
RETURN
END SUBROUTINE circle_xy_real

!*****************************************************************
SUBROUTINE circle_xy(lat, lat_first, dlon, dlat, thdist, miss_int, nx, ny, a1x, a1y)
  implicit none
  !-- input -----------------------------
  integer                               nx, ny
  double precision                      lat, lat_first, dlon, dlat
!f2py intent(in)                        lat, lat_first, dlon, dlat
  double precision                      thdist  ![m]
!f2py intent(in)                        thdist  ![m]
  integer                               miss_int
!f2py intent(in)                        miss_int
  !-- output ----------------------------
  integer,dimension(nx*ny)           :: a1x, a1y
!f2py intent(out)                       a1x, a1y
  !-- calc ------------------------------
  integer                               icount
  integer                               x, y, ix, iy, ix_loop, iy_loop
  integer                               ngrids, sgrids, xgrids, ygrids
  double precision                      idist, ilat, ilon
  double precision                      lon
!****************************************
! search
!----------------------------------------
lon       = 0.0d0
x  = 1
y  = int((lat - lat_first)/dlat) + 1
!-----------
! set range
!***********
call gridrange(lat, dlat, dlon, thdist, ngrids, sgrids, xgrids)
if (sgrids .ge. ngrids )then
  ygrids = sgrids
else
  ygrids = ngrids
end if
!--
!-----------
! search loop
!***********
icount = 0
a1x    = miss_int
a1y    = miss_int
do iy_loop = -ygrids, ygrids
  do ix_loop = -xgrids, xgrids

    call ixy2iixy(ix_loop, iy_loop, nx, ny, ix, iy)
    ilat        = lat + iy_loop *dlat
    ilon        = lon + ix_loop *dlon
    idist       = hubeny(lat, lon, ilat, ilon)

    if (idist .lt. thdist) then
      icount = icount + 1
      a1x(icount) = ix_loop   ! not ix
      a1y(icount) = iy_loop   ! not iy
    end if
  end do
end do

 
RETURN
END SUBROUTINE circle_xy
!*****************************************************************
SUBROUTINE vorticity_real(a2u, a2v, lat_first, dlon, dlat, miss, nx, ny, a2vort)
  implicit none
  !-- input -------------------------
  integer                      nx, ny
  real,dimension(nx,ny)     :: a2u, a2v
!f2py intent(in)               a2u, a2v
  real                         lat_first
!f2py intent(in)               lat_first
  real                         dlon, dlat
!f2py intent(in)               dlon, dlat
  real                         miss
!f2py intent(in)               miss
  !-- output ------------------------
  real,dimension(nx,ny)     :: a2vort
!f2py intent(out)              a2vort
  !-- calc  -------------------------
  integer                      ix, iy
  integer                      ix_nxt, ix_pre, iy_nxt, iy_pre
  integer                      iix_nxt, iix_pre, iiy_nxt, iiy_pre
  real                         dx, dy
  real                         lat, lat1, lat2, lon1, lon2
  !----------------------------------
lat1 = 90.0
lat2 = lat1 + dlat
dy = hubeny_real(lat1, 0.0, lat2, 0.0)
!---------------------
do iy = 1, ny
  !-------------------
  ! make dx
  !--------
  lat = lat_first + (iy -1) *dlat
  lon1 = 0.0
  lon2 = dlon
  dx = hubeny_real(lat, lon1, lat, lon2)
  !-------------------
  iy_nxt = iy + 1
  iy_pre = iy - 1
  !-------------------
  do ix = 1, nx
    ix_nxt = ix + 1
    ix_pre = ix - 1
    call ixy2iixy(ix_nxt, iy_nxt, nx, ny, iix_nxt, iiy_nxt) 
    call ixy2iixy(ix_pre, iy_pre, nx, ny, iix_pre, iiy_pre)
    !----------------
    ! make vorticity
    !----------------
    if (   ( a2u(ix, iy) .eq. miss ) &
      .or. ( a2u(ix_nxt, iy) .eq. miss)&
      .or. ( a2u(ix, iy_nxt) .eq. miss)&
      .or. ( a2u(ix_pre, iy) .eq. miss)&
      .or. ( a2u(ix, iy_pre) .eq. miss)&
      .or. ( a2u(ix_nxt, iy_nxt) .eq. miss)&
      .or. ( a2u(ix_pre, iy_pre) .eq. miss) ) then
      a2vort(ix, iy) = miss
    else
      a2vort(ix, iy) = &
        ( a2v(iix_nxt, iiy_nxt) - a2v(iix_pre, iiy_pre))*0.5 / dx&
      - ( a2u(iix_nxt, iiy_nxt) - a2u(iix_pre, iiy_pre))*0.5 / dy
    end if
    !----------------
  end do
end do

RETURN
END SUBROUTINE vorticity_real
!*****************************************************************
SUBROUTINE vorticity(a2u, a2v, lat_first, dlon, dlat, miss_dbl, nx, ny, a2vort)
  implicit none
  !-- input -------------------------
  integer                                  nx, ny
  double precision,dimension(nx,ny)     :: a2u, a2v
!f2py intent(in)                           a2u, a2v
  double precision                         lat_first
!f2py intent(in)                           lat_first
  double precision                         dlon, dlat
!f2py intent(in)                           dlon, dlat
  double precision                         miss_dbl
!f2py intent(in)                           miss_dbl
  !-- output ------------------------
  double precision,dimension(nx,ny)     :: a2vort
!f2py intent(out)                          a2vort
  !-- calc  -------------------------
  integer                                  ix, iy
  integer                                  ix_nxt, ix_pre, iy_nxt, iy_pre
  integer                                  iix_nxt, iix_pre, iiy_nxt, iiy_pre
  double precision                         dx, dy
  double precision                         lat, lat1, lat2, lon1, lon2
  !----------------------------------
lat1 = 90.0d0
lat2 = lat1 + dlat
dy = hubeny(lat1, 0.0d0, lat2, 0.0d0)
!---------------------
do iy = 1, ny
  !-------------------
  ! make dx
  !--------
  lat = lat_first + (iy -1) *dlat
  lon1 = 0.0d0
  lon2 = dlon
  dx = hubeny(lat, lon1, lat, lon2)
  !-------------------
  iy_nxt = iy + 1
  iy_pre = iy - 1
  !-------------------
  do ix = 1, nx
    ix_nxt = ix + 1
    ix_pre = ix - 1
    call ixy2iixy(ix_nxt, iy_nxt, nx, ny, iix_nxt, iiy_nxt) 
    call ixy2iixy(ix_pre, iy_pre, nx, ny, iix_pre, iiy_pre)
    !----------------
    ! make vorticity
    !----------------
    if (   ( a2u(ix, iy) .eq. miss_dbl ) &
      .or. ( a2u(ix_nxt, iy) .eq. miss_dbl)&
      .or. ( a2u(ix, iy_nxt) .eq. miss_dbl)&
      .or. ( a2u(ix_pre, iy) .eq. miss_dbl)&
      .or. ( a2u(ix, iy_pre) .eq. miss_dbl)&
      .or. ( a2u(ix_nxt, iy_nxt) .eq. miss_dbl)&
      .or. ( a2u(ix_pre, iy_pre) .eq. miss_dbl) ) then
      a2vort(ix, iy) = miss_dbl
    else
      a2vort(ix, iy) = &
        ( a2v(iix_nxt, iiy_nxt) - a2v(iix_pre, iiy_pre))*0.5d0 / dx&
      - ( a2u(iix_nxt, iiy_nxt) - a2u(iix_pre, iiy_pre))*0.5d0 / dy
    end if
    !----------------
  end do
end do

RETURN
END SUBROUTINE vorticity
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
  !-- functions -----------
  !real                                  hubeny_real
  !------------------------
!-- initialize -----
latgrids_real = -9999
!-------------------

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
  !-- functions -----------
  !real                                  hubeny_real
  !------------------------
!-- initialize --
longrids_real = -9999
!----------------

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
FUNCTION latgrids(lat, dlat, thdist)
  implicit none
  !-- for input -----------
  double precision                      thdist   ! [m]
!f2py intent(in)                        thdist
  double precision                      lat, dlat
!f2py intent(in)                        lat, dlat
  !-- for output ----------
  integer                               latgrids 
!f2py intent(out)                       latgrids
  !-- for calc  -----------
  integer                               i
  double precision                      dist, lat2
  double precision                      dist_pre
  !-- functions -----------
  !double precision                      hubeny
  !------------------------

!-- initialize ----
latgrids = -9999
!-------------------


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
  integer                               longrids 
!f2py intent(out)                       longrids
  !-- for calc  -----------
  integer                               i
  double precision                      dist, lon2
  double precision                      dist_pre
  !-- functions -----------
  !double precision                      hubeny
  !------------------------

!-- initialize  -----
longrids = -9999
!--------------------

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
SUBROUTINE gridrange_real(lat, dlat, dlon, thdist, ngrids, sgrids, xgrids)
  implicit none
  !-- for input -----------
  real                                  thdist   ! [km]
!f2py intent(in)                        thdist
  real                                  lat, dlat, dlon
!f2py intent(in)                        lat, dlat, dlon
  !-- for output ----------
  integer                               ngrids, sgrids, xgrids
!f2py intent(out)                       ngrids, sgrids, xgrids
  !-- for calc  -----------
  integer                               i
  real                                  dist, lat2, lon2
  !------------------------
do i = 1, 100000
  lat2 = lat + dlat * i
  dist = hubeny_real(lat, 0.0, lat2, 0.0)
  if (dist .gt. thdist) then
    ngrids = i
    exit
  end if
end do
do i = 1, 100000
  lat2 = lat - dlat * i
  dist = hubeny_real(lat, 0.0, lat2, 0.0)
  if (dist .gt. thdist) then
    sgrids = i
    exit
  end if
end do
do i = 1, 100000
  lon2 = dlon * i
  dist = hubeny_real(lat, 0.0, lat, lon2)
  if (dist .gt. thdist) then
    xgrids = i
    exit
  end if 
end do
if (xgrids.gt.int(360.0*0.5/dlon))then
  xgrids = int(360.0*0.5/dlon)
end if
RETURN
END SUBROUTINE gridrange_real

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
!!*****************************************************************
FUNCTION hubeny_real(lat1, lon1, lat2, lon2)
  implicit none
  !-- for input -----------
  real                                  lat1, lon1, lat2, lon2
!f2py intent(in)                        lat1, lon1, lat2, lon2
  !-- for output-----------
  real                                  hubeny_real  ! (m)
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
RETURN
END FUNCTION hubeny_real

!*****************************************************************
FUNCTION hubeny(lat1, lon1, lat2, lon2)
  implicit none
  !-- for input -----------
  double precision                      lat1, lon1, lat2, lon2
!f2py intent(in)                        lat1, lon1, lat2, lon2
  !-- for output-----------
  double precision                      hubeny   ! (m)
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
  if (ix .ge. 1) then
    roundx = ix - int( (ix -1)/nx )* nx
  else
    roundx = nx - abs(mod(ix,nx))
  end if 
RETURN
END FUNCTION roundx
!*****************************************************************
!*********************************************************
SUBROUTINE ixy2iixy_saone(ix, iy, iix, iiy)
!--------------------------
! data array order should be "South->North" & "West->East"
! data array : nx= 360, ny= 180
!--------------------------
implicit none
!--- input -----------
integer             ix, iy
!f2py intent(in)    ix, iy
!--- output ----------
integer             iix, iiy
!f2py intent(out)   iix, iiy
!--- calc  -----------
!---------------------
if (iy .le. 0)then
  iiy = 1 - iy
  iix = ix + 180
else if (iy .ge. 181) then
  iiy = 2*180 - iy +1
  iix = ix + 180
else
  iiy = iy
  iix = ix
end if
!
if (iix .ge. 361) then
  iix = mod(iix, 360)
else if (iix .le. 0) then
  iix = 360 - mod(abs(iix), 360)
end if
!
return
END SUBROUTINE ixy2iixy_saone
!*********************************************************
!*****************************************************************
!*****************************************************************
!*****************************************************************
!*****************************************************************
!*****************************************************************
!*****************************************************************
!*****************************************************************
!*****************************************************************
end module ctrack_fsub
