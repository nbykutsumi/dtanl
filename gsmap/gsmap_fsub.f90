MODULE gsmap_fsub

CONTAINS
!*********************************************************
SUBROUTINE saone2dec(a2in, a2out)
implicit none
!---- input --------
real,dimension(360,180)         :: a2in
!f2py intent(in)                   a2in
!---- out ----------
real,dimension(3600,1800)       :: a2out
!f2py intent(out)                  a2out
!---- calc ---------
integer            ix,iy, iix,iiy
!-------------------
do iy = 1,180
  do ix = 1,360
    do iiy = (iy-1)*10+1, iy*10
      do iix = (ix-1)*10+1, ix*10
        a2out(iix,iiy) = a2in(ix,iy)
      end do
    end do
  end do
end do
!-------------------
return
END SUBROUTINE saone2dec
!*********************************************************


!*********************************************************
SUBROUTINE saone_gsmap2dec_gsmap(a2in, a2out)
implicit none
!---- input --------
real,dimension(360,120)         :: a2in
!f2py intent(in)                   a2in
!---- out ----------
real,dimension(3600,1200)       :: a2out
!f2py intent(out)                  a2out
!---- calc ---------
integer            ix,iy, iix,iiy
!-------------------
do iy = 1,120
  do ix = 1,360
    do iiy = (iy-1)*10+1, iy*10
      do iix = (ix-1)*10+1, ix*10
        a2out(iix,iiy) = a2in(ix,iy)
      end do
    end do
  end do
end do
!-------------------
return
END SUBROUTINE saone_gsmap2dec_gsmap
!*********************************************************
END MODULE gsmap_fsub
