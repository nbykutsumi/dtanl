module dtanl_cmip_sbs

CONTAINS
!*********************************************************************
!* SUBROUTINE & FUNCTION
!*********************************************************************
SUBROUTINE swa_profile(rPlcl, r1lev, r1wap, r1dqdp, nz, r1swa)
  implicit none
  !** for input -------------------------------------------
  integer                                      nz
  double precision                             rPlcl
!f2py intent(in)                               rPlcl
  double precision,dimension(nz)            :: r1lev, r1wap, r1dqdp
!f2py intent(in)                               r1lev, r1wap, r1dqdp

  !** for output ------------------------------------------
  double precision,dimension(nz)            :: r1swa
!f2py intent(out)                           :: r1swa

  !** for calculation -------------------------------------
  integer                                      iz, iz_scnd
  double precision                             dqdp_lcl, dqdp_b, dqdp_t
  double precision                             wap_lcl, wap_b, wap_t
  double precision                             Pb, Pt
!----------------------------------------------------------
iz_scnd = findiz_scnd(nz, r1lev, rPlcl)
!----------------------------------------------------------
! from iz = 1 to iz_scnd -1
!----------------------------------------------------------
do iz = 1,iz_scnd -1
  r1swa(iz) = 0.0d0
end do
!----------------------------------------------------------
! from Plcl to iz_scnd
!----------------------------------------------------------
dqdp_lcl = linear_interpolate( rPlcl, r1lev(iz_scnd-1), r1lev(iz_scnd), r1dqdp(iz_scnd-1), r1dqdp(iz_scnd))
wap_lcl  = linear_interpolate( rPlcl, r1lev(iz_scnd-1), r1lev(iz_scnd), r1wap(iz_scnd-1), r1wap(iz_scnd))
!
Pb   = rPlcl
Pt   = r1lev(iz_scnd)
dqdp_b = dqdp_lcl
dqdp_t = r1dqdp(iz_scnd)
wap_b  = wap_lcl
wap_t  = r1wap(iz_scnd)
!
r1swa(iz_scnd) = cal_swa(Pb, Pt, dqdp_b, dqdp_t, wap_b, wap_t)
!----------------------------------------------------------
! from iz_scnd +1 to nz
!----------------------------------------------------------
do iz = iz_scnd +1, nz
  Pb = r1lev(iz -1)
  Pt = r1lev(iz)
  dqdp_b = r1dqdp(iz -1)
  dqdp_t = r1dqdp(iz)
  wap_b  = r1wap(iz -1)
  wap_t  = r1wap(iz)
  !
  r1swa(iz) = cal_swa(Pb, Pt, dqdp_b, dqdp_t, wap_b, wap_t)
end do
!----------------------------------------------------------
RETURN
END SUBROUTINE swa_profile
!*********************************************************************
SUBROUTINE scale_profile(rPlcl, r1lev, r1wap1, r1wap2, r1dqdp1, r1dqdp2, nz, r1sdwa, r1swda)
  implicit none
  !** for input --------------------------------------------
  integer                                      nz
  double precision                             rPlcl
!f2py                                          rPlcl
  double precision,dimension(nz)            :: r1lev, r1wap1, r1wap2, r1dqdp1, r1dqdp2
!f2py                                       :: r1lev, r1wap1, r1wap2, r1dqdp1, r1dqdp2

  !** for output -------------------------------------------
  double precision,dimension(nz)            :: r1sdwa, r1swda
!f2py intent(out)                              r1sdwa, r1swda

  !** for calculation --------------------------------------
  integer                                      iz, iz_scnd
  double precision                             dqdp_lcl1, dqdp_lcl2
  double precision                             wap_lcl1, wap_lcl2
  double precision                             Pb, Pt
  double precision                             dqdp_b1, dqdp_b2, dqdp_t1, dqdp_t2
  double precision                             wap_b1,  wap_b2,  wap_t1,  wap_t2
!-----------------------------------------------------------
iz_scnd = findiz_scnd(nz, r1lev, rPlcl)
!-----------------------------------------------------------
! from iz = 1 to iz_scnd -1
!-----------------------------------------------------------
do iz = 1,iz_scnd -1
  r1sdwa(iz) = 0.0d0
end do
!-----------------------------------------------------------
! from Plcl to iz_scnd
!-----------------------------------------------------------
dqdp_lcl1 = linear_interpolate( rPlcl, r1lev(iz_scnd-1), r1lev(iz_scnd), r1dqdp1(iz_scnd-1), r1dqdp1(iz_scnd))
dqdp_lcl2 = linear_interpolate( rPlcl, r1lev(iz_scnd-1), r1lev(iz_scnd), r1dqdp2(iz_scnd-1), r1dqdp2(iz_scnd))
!
wap_lcl1  = linear_interpolate( rPlcl, r1lev(iz_scnd-1), r1lev(iz_scnd), r1wap1(iz_scnd-1), r1wap1(iz_scnd))
wap_lcl2  = linear_interpolate( rPlcl, r1lev(iz_scnd-1), r1lev(iz_scnd), r1wap2(iz_scnd-1), r1wap2(iz_scnd))
!
Pb = rPlcl
Pt = r1lev(iz_scnd)
dqdp_b1 = dqdp_lcl1
dqdp_b2 = dqdp_lcl2
dqdp_t1 = r1dqdp1(iz_scnd)
dqdp_t2 = r1dqdp2(iz_scnd)
wap_b1  = wap_lcl1
wap_b2  = wap_lcl2
wap_t1  = r1wap1(iz_scnd)
wap_t2  = r1wap2(iz_scnd)
!
r1sdwa(iz_scnd) = cal_sdwa(Pb, Pt, dqdp_b1, dqdp_t1, wap_b1, wap_t1, wap_b2, wap_t2)
!
r1swda(iz_scnd) = cal_swda(Pb, Pt, dqdp_b1, dqdp_t1, dqdp_b2, dqdp_t2, wap_b1, wap_t1)
!-----------------------------------------------------------
! from iz_scnd + 1 to nz
!-----------------------------------------------------------
do iz = iz_scnd+1, nz
  Pb = r1lev(iz - 1)
  Pt = r1lev(iz)
  dqdp_b1 = r1dqdp1(iz -1)
  dqdp_b2 = r1dqdp2(iz -1)
  dqdp_t1 = r1dqdp1(iz)
  dqdp_t2 = r1dqdp2(iz)
  wap_b1  = r1wap1(iz-1)
  wap_b2  = r1wap2(iz-1)
  wap_t1  = r1wap1(iz)
  wap_t2  = r1wap2(iz)
  !
  r1sdwa(iz) = cal_sdwa(Pb, Pt, dqdp_b1, dqdp_t1, wap_b1, wap_t1, wap_b2, wap_t2)
  !
  r1swda(iz) = cal_swda(Pb, Pt, dqdp_b1, dqdp_t1, dqdp_b2, dqdp_t2, wap_b1, wap_t1)
! 
end do
!-----------------------------------------------------------
  

!-----------------------------------------------------------
END SUBROUTINE scale_profile
!*********************************************************************
SUBROUTINE omega_profile(rmiss, rPsfc, rPlcl, r1lev_c, r1lev_f, r1wap_c, nz_c, nz_f, r1wap_f)
  implicit none
  !** for input   ------------------------------------------
  integer                                      nz_c
  integer                                      nz_f

  double precision,dimension(nz_c)          :: r1lev_c
!f2py intent(in)                               r1lev_c
  double precision,dimension(nz_f)          :: r1lev_f
!f2py intent(in)                               r1lev_f 

  double precision                             rmiss, rPsfc, rPlcl
!f2py intent(in)                               rmiss, rPsfc, rPlcl

  double precision,dimension(nz_c)          :: r1wap_c
!f2py intent(in)                               r1wap_c


  !** for output  ------------------------------------------
  double precision,dimension(nz_f)          :: r1wap_f
!f2py intent(out)                              r1wap_f

  !** for calc    ------------------------------------------
  integer                                      iz, iz_btm
  double precision                             P
  double precision,parameter                :: dP_cal = 100.0d0  ![Pa]
!-----------------------------------------------------------
iz_btm = findiz_btm(nz_c, r1lev_c, rPsfc)
do iz = 1, nz_f
  P = r1lev_f(iz)
  r1wap_f(iz) = omega_atP(nz_c, iz_btm, r1wap_c, r1lev_c, rPsfc, P, rmiss)
end do

if ( -r1lev_f(nz_f) .gt. -r1lev_c(nz_c) )then
  do iz = 1, nz_f
    if ( -r1lev_f(iz) .gt. -r1lev_c(nz_c) )then
      r1wap_f(iz) = rmiss
    end if
  end do
end if

END SUBROUTINE omega_profile
!*********************************************************************
SUBROUTINE dqdp_profile(flag_fill, rmiss, rPsfc, rTsfc, rqsfc, rPlcl, r1lev_f, nz_f, r1dqdp)
  implicit none
  !
  integer                                      nz_f
  integer                                      flag_fill
!f2py intent(in)                               flag_fill
  double precision                             rmiss
!f2py intent(in)                               rmiss
  double precision                             rPsfc, rTsfc, rqsfc, rPlcl
!f2py intent(in)                               rPsfc, rTsfc, rqsfc, rPlcl
  double precision,dimension(nz_f)          :: r1lev_f
!f2py intent(in)                               r1lev_f

  !** for output---------------------------------------------
  double precision,dimension(nz_f)          :: r1dqdp
!f2py intent(out)                              r1dqdp

  !** for calculation ---------------------------------------
  integer                                      iz
  double precision                             P, rTlcl
  double precision,dimension(nz_f)          :: r1T
  double precision,parameter                :: dP_cal = 100.0d0  ![Pa]
  integer                                      iz_scnd
!-----------------------------------------
rTlcl = T1toT2dry(rTsfc, rPsfc, rPlcl)
iz_scnd = findiz_scnd( nz_f, r1lev_f, rPlcl)
!-----------------------------
! from from lcl to iz_scnd
!-----------------------------
r1T(iz_scnd)     =  moistadiabat(rPlcl,rTlcl, r1lev_f(iz_scnd), dP_cal)
r1dqdp(iz_scnd)  =  cal_rdqdP( r1lev_f(iz_scnd), r1T(iz_scnd), dP_cal)
!-----------------------------
! from iz_scnd +1  to nz
!-----------------------------
if (iz_scnd+1 .le. nz_f) then
  do iz = iz_scnd+1, nz_f
    P          = r1lev_f(iz)
    r1T(iz)    = moistadiabat(r1lev_f(iz-1), r1T(iz-1), r1lev_f(iz), dP_cal)
    r1dqdp(iz) = cal_rdqdP(P, r1T(iz), dP_cal)
  end do
end if
!-----------------------------
! iz = iz_scnd -1 to 1
!-----------------------------
if (iz_scnd .ge. 2) then
  if (flag_fill .eq. 1) then
    do iz = iz_scnd-1, 1, -1
      r1T(iz)    = moistadiabat(r1lev_f(iz+1), r1T(iz+1), r1lev_f(iz), dP_cal)
      r1dqdp(iz) = cal_rdqdP( r1lev_f(iz), r1T(iz), dP_cal)
    end do
  else if (flag_fill .eq. 0) then
    do iz = iz_scnd-1, 1, -1
      r1T(iz)    = rmiss
      r1dqdp(iz) = rmiss
    end do
  else
    print *,"check!!  flag_fill=",flag_fill
    stop
  end if
end if
!-----------------------------
!-----------------------------
RETURN
END SUBROUTINE dqdp_profile
!*********************************************************************
SUBROUTINE dpxdqdp_profile(rPlcl, r1dqdp, r1lev, nz, r1dpxdqdp)
  implicit none
  !-- input -------------------
  integer                             nz
  double precision                    rPlcl
!f2py intent(in)                      rPlcl
  double precision,dimension(nz)   :: r1dqdp, r1lev
!f2py intent(iz)                      r1dqdp, r1lev
  !-- output ------------------
  double precision,dimension(nz)   :: r1dpxdqdp
!f2py intent(out)                     r1dpxdqdp
  !-- for calculation ---------
  integer                             iz, iz_scnd
  double precision                    dp
!------------------------------
iz_scnd  = findiz_scnd( nz, r1lev, rPlcl)

do iz = 1,iz_scnd-1 
  r1dpxdqdp(iz) = r1dqdp(iz)
end do
!------------------
! for iz_scnd
!------------------
if (iz_scnd .lt. nz)then
  dp = (rPlcl - r1lev(iz_scnd)) + ( r1lev(iz_scnd) - r1lev(iz_scnd +1) )/2.0d0
else
  dp = (rPlcl - r1lev(iz_scnd))
end if
r1dpxdqdp(iz_scnd) = dp * r1dqdp(iz_scnd) 
!------------------
! from iz_scnd + 1 to nz
!------------------
if (iz_scnd .eq. nz)then
  dp = ( r1lev(iz_scnd -1) - r1lev(iz_scnd) )/2.0d0
  r1dpxdqdp(iz_scnd) = dp * r1dqdp(iz_scnd)
else
  do iz = iz_scnd + 1, nz
    dp = ( r1lev(iz_scnd -1) - r1lev(iz_scnd +1) )/2.0d0
    r1dpxdqdp(iz) = dp * r1dqdp(iz)
  end do
end if
!------------------
RETURN
END SUBROUTINE dpxdqdp_profile
!*********************************************************************
SUBROUTINE dqdp_profile_epl(rPlcl, rPsfc, rTsfc, r1lev_c, r1lev_f, r1T_c, nzc, nzf, r1dqdp_f)

  implicit none
  !-- input -------------------
  integer                             nzc, nzf
  double precision                    rPlcl, rPsfc, rTsfc
!f2py intent(in)                      rPlcl, rPsfc, rTsfc
  double precision,dimension(nzc)  :: r1lev_c, r1T_c
!f2py intent(in)                      r1lev_c, r1T_c
  double precision,dimension(nzf)  :: r1lev_f
!f2py intent(in)                      r1lev_f

  !-- output ------------------
  double precision,dimension(nzf)  :: r1dqdp_f
!f2py intent(out)                     r1dqdp_f

  !----------------------------
  ! for calculation
  !----------------------------
  integer                             izc, izf, izc_btm, izf_btm, izc_scnd, izf_scnd
  integer                             izf_acs   ! izf at Above izC_Scnd
  double precision,dimension(nzc)  :: r1dqdp_c
  double precision                    rdqdp_sfc, rdqdp_lw, rdqdp_up
  double precision                    rTlcl, rdqdp_lcl
  double precision                    p_up, p_lw
  double precision,parameter       :: dP_cal = 100.0d0  ![Pa]
!------------------------------
!print *,"r1T_c", r1T_c
izc_btm = findiz_btm(nzc, r1lev_c, rPsfc)
!------------------------
! izc = 1 to izc_btm
!------------------------
if (izc_btm .gt. 1)then
  do izc = 1, izc_btm-1
    r1dqdp_c(izc) = 0.0d0
  end do
end if
!------------------------
! at Psfc
!------------------------
rdqdp_sfc = cal_rdqdP( rPsfc, rTsfc, dP_cal)
!------------------------
do izc = 1,nzc
  r1dqdp_c(izc) = cal_rdqdP( r1lev_c(izc), r1T_c(izc), dP_cal)
  !print *,"lev, T, rdqdp",r1lev_c(izc), r1T_c(izc), r1dqdp_c(izc)
enddo
!-----------------------------
!make r1dqdp_f
!-----------------------------
izc_scnd  = findiz_scnd( nzc, r1lev_c, rPlcl)
izf_scnd  = findiz_scnd( nzf, r1lev_f, rPlcl)
rTlcl     = T1toT2dry(rTsfc, rPsfc, rPlcl)
rdqdp_lcl = cal_rdqdP( rPlcl, rTlcl, dP_cal )
!------------------
if (izf_scnd .gt. 1)then
  do izf = 1,izf_scnd-1
    r1dqdp_f(izf) = 0.0d0
  enddo
endif
!-------------
! from izf_scnd to the level below or equal to izc_scnd
!-------------
p_lw = rPlcl
p_up = r1lev_c(izc_scnd)
rdqdp_lw = rdqdp_lcl
rdqdp_up = r1dqdp_c(izc_scnd)
izf = izf_scnd - 1
do while (-r1lev_f(izf) .le. -r1lev_c(izc_scnd) )
   izf = izf + 1
   r1dqdp_f(izf) = linear_interpolate( r1lev_f(izf), p_lw, p_up, rdqdp_lw, rdqdp_up )
enddo
!-------------
izf_acs = izf + 1

izc = izc_scnd
p_lw = r1lev_c(izc)
p_up = r1lev_c(izc+1)
rdqdp_lw = r1dqdp_c(izc)
rdqdp_up = r1dqdp_c(izc+1)
!
do izf = izf_acs, nzf
   do while (-r1lev_f(izf) .gt. -p_up)
     izc  = izc + 1
     p_lw = r1lev_c(izc )
     p_up = r1lev_c(izc + 1 )
     rdqdp_lw = r1dqdp_c(izc)
     rdqdp_up = r1dqdp_c(izc + 1 )
   end do
   r1dqdp_f(izf) = linear_interpolate( r1lev_f(izf), p_lw, p_up, rdqdp_lw, rdqdp_up )
   
enddo
!-----------------------------
RETURN
END SUBROUTINE dqdp_profile_epl
!*********************************************************************
FUNCTION cal_swadlcl(rPlcl1, rPlcl2, r1lev, r1wap, r1dqdp, nz)
!*********************************************************************
  implicit none
  !-- for input ------
  integer                                     nz
  double precision                            rPlcl1, rPlcl2
!f2py intent(in)                              rPlcl1, rPlcl2
  double precision,dimension(nz)           :: r1lev, r1wap, r1dqdp
!f2py intent(in)                              r1lev, r1wap, r1dqdp

  !-- for output -----
  double precision                            cal_swadlcl
!f2py intent(out)                             cal_swadlcl
  
  !-- for calculation --
  integer                                     iz_scnd
  double precision                            dPlcl, rwap_lcl1, dqdp_lcl1
!---------------------
iz_scnd = findiz_scnd(nz, r1lev, rPlcl1)
!---------------------
dPlcl = rPlcl2 - rPlcl1
rwap_lcl1 = linear_interpolate(rPlcl1, r1lev(iz_scnd-1), r1lev(iz_scnd), r1wap(iz_scnd-1), r1wap(iz_scnd))
rwap_lcl1 = -plus2zero(rwap_lcl1)
!
dqdp_lcl1 = linear_interpolate(rPlcl1, r1lev(iz_scnd-1), r1lev(iz_scnd), r1dqdp(iz_scnd-1), r1dqdp(iz_scnd))

cal_swadlcl = -rwap_lcl1 * dqdp_lcl1 * dPlcl
!
RETURN
END FUNCTION cal_swadlcl
!*********************************************************************
FUNCTION cal_swa(Pb, Pt, dqdp_b, dqdp_t, wap_b, wap_t)
  implicit none
  !-- for input -----
  double precision               Pb, Pt
!f2py intent(in)                 Pb, Pt
  double precision               dqdp_b, dqdp_t, wap_b, wap_t
!f2py intent(in)                 dqdp_b, dqdp_t, wap_b, wap_t

  !-- for output ----
  double precision               cal_swa

  !-- for calculation ---
  double precision               xb, xt, yb, yt
  double precision               Px
  double precision               A_b, A_t
  double precision               wap_x, w_b, w_t
  double precision               dqdp_x
  double precision               swa_seg1, swa_seg2
!----------------------
! estimate Px
!----------------------
if ( (wap_b *wap_t) .lt. 0.0d0) then
  xb = Pb
  xt = Pt
  yb = wap_b
  yt = wap_t
  Px = xb - yb*(xt -xb)/(yt - yb)
else
  Px = Pb
end if
wap_x  = linear_interpolate(Px, Pb, Pt, wap_b, wap_t)
dqdp_x = linear_interpolate(Px, Pb, Pt, dqdp_b, dqdp_t)
!---------------------
! from Pb to Px
!---------------------
A_b = dqdp_b
A_t = dqdp_x
w_b = -1.0d0 *plus2zero( wap_b )
w_t = -1.0d0 *plus2zero( wap_x )
swa_seg1  = -integral_linear_AB(A_b, A_t, w_b, w_t, Pb, Px)
!---------------------
! from Px to Pt
!---------------------
A_b = dqdp_x
A_t = dqdp_t
w_b = -1.0d0 *plus2zero( wap_x )
w_t = -1.0d0 *plus2zero( wap_t )
swa_seg2  = -integral_linear_AB(A_b, A_t, w_b, w_t, Px, Pt)
!---------------------
cal_swa = swa_seg1 + swa_seg2
!---------------------
RETURN
END FUNCTION cal_swa
!*********************************************************************
FUNCTION cal_swda(Pb, Pt, dqdp_b1, dqdp_t1, dqdp_b2, dqdp_t2, wap_b, wap_t)
  implicit none
  !-- for input ------
  double precision               Pb, Pt
!f2py intent(in)                 Pb, Pt
  double precision               dqdp_b1, dqdp_b2, dqdp_t1, dqdp_t2
!f2py intent(in)                 dqdp_b1, dqdp_b2, dqdp_t1, dqdp_t2
  double precision               wap_b, wap_t
!f2py intent(in)                 wap_b, wap_t

  !-- for output -----
  double precision               cal_swda
!f2py intent(out)                cal_swda

  !-- for calculation -----
  double precision               xb, xt, yb, yt
  double precision               Px, dqdp_x1, dqdp_x2, wap_x
  double precision               A_b1, A_b2, A_t1, A_t2, dA_b, dA_t
  double precision               w_b, w_t
  double precision               swda_seg1, swda_seg2 
!-----------------------------
! estimate Px
!-----------------------------
if ( (wap_b * wap_t) .lt. 0.0d0)then
  xb = Pb
  xt = Pt
  yb = wap_b
  yt = wap_t
  Px = xb - yb*(xt - xb)/(yt -yb)
else
  Px = Pb
end if
wap_x  = linear_interpolate(Px, Pb, Pt, wap_b, wap_t)
dqdp_x1 = linear_interpolate(Px, Pb, Pt, dqdp_b1, dqdp_t1)
dqdp_x2 = linear_interpolate(Px, Pb, Pt, dqdp_b2, dqdp_t2)
!-------------------------------------
! from Pb to Px
!-------------------------------------
A_b1 = dqdp_b1
A_b2 = dqdp_b2
A_t1 = dqdp_x1
A_t2 = dqdp_x2
dA_b = A_b2 - A_b1
dA_t = A_t2 - A_t1
w_b  = -1.0d0 *plus2zero( wap_b )
w_t  = -1.0d0 *plus2zero( wap_x )
swda_seg1 = -integral_linear_AB(dA_b, dA_t, w_b, w_t, Pb, Px)

!-------------------------------------
! from Pb to Px
!-------------------------------------
A_b1 = dqdp_x1
A_b2 = dqdp_x2
A_t1 = dqdp_t1
A_t2 = dqdp_t2
dA_b = A_b2 - A_b1
dA_t = A_t2 - A_t1
w_b  = -1.0d0 *plus2zero( wap_x )
w_t  = -1.0d0 *plus2zero( wap_t ) 
swda_seg2 = -integral_linear_AB(dA_b, dA_t, w_b, w_t, Px, Pt)
!--------------------------------
cal_swda = swda_seg1 + swda_seg2
!--------------------------------
END FUNCTION cal_swda
!*********************************************************************
FUNCTION cal_sdwa(Pb, Pt, dqdp_b, dqdp_t, wap_b1, wap_t1, wap_b2, wap_t2)
  implicit none
  !-- for input -------
  double precision               Pb, Pt
!f2py intent(in)                 Pb, Pt
  double precision               dqdp_b, dqdp_t
!f2py intent(in)                 dqdp_b, dqdp_t
  double precision               wap_b1, wap_t1, wap_b2, wap_t2
!f2py intent(in)                 wap_b1, wap_t1, wap_b2, wap_t2
  !-- for output ------
  double precision               cal_sdwa
!f2py intent(out)                cal_sdwa
  !---for caluculation-
  double precision               Px_tmp1, Px_tmp2, Px_b, Px_t
  double precision               w_b1, w_b2, w_t1, w_t2
  double precision               A_b, A_t
  double precision               dw_b, dw_t
  double precision               xb, xt, yb, yt
  double precision               sdwa
  double precision               sdwa_seg1, sdwa_seg2,sdwa_seg3
!----------------------
!----------------------
! estimate Px_b, Px_t
!----------------------
if ( (wap_b1 * wap_t1) .lt. 0.0d0 )then
  xb = Pb
  xt = Pt
  yb = wap_b1
  yt = wap_t1
  Px_tmp1 = xb - yb* (xt - xb)/(yt - yb)
else
  Px_tmp1 = Pb
end if
!
if ( (wap_b2 * wap_t2) .lt. 0.0d0 )then
  xb = Pb
  xt = Pt
  yb = wap_b2
  yt = wap_t2
  Px_tmp2 = xb - yb* (xt - xb)/(yt - yb)
else
  Px_tmp2 = Pb
end if

if (-Px_tmp1 .le. -Px_tmp2)then
  Px_b = Px_tmp1
  Px_t = Px_tmp2
else
  Px_b = Px_tmp2
  Px_t = Px_tmp1
end if

!sdwa = 0.0d0
!----------------------
! from Pb to Px_b
!----------------------
A_b  = dqdp_b
A_t  = linear_interpolate(Px_b, Pb, Pt, dqdp_b, dqdp_t)
w_b1 = -1.0d0 *plus2zero(wap_b1)
w_b2 = -1.0d0 *plus2zero(wap_b2)
w_t1 = -1.0d0 *plus2zero( linear_interpolate(Px_b, Pb, Pt, wap_b1, wap_t1) )
w_t2 = -1.0d0 *plus2zero( linear_interpolate(Px_b, Pb, Pt, wap_b2, wap_t2) )
dw_b = w_b2 - w_b1
dw_t = w_t2 - w_t1
sdwa_seg1 = -integral_linear_AB(A_b, A_t, dw_b, dw_t, Pb, Px_b)
!----------------------
! from Px_b to Px_t
!----------------------
A_b  = linear_interpolate(Px_b, Pb, Pt, dqdp_b, dqdp_t)
A_t  = linear_interpolate(Px_t, Pb, Pt, dqdp_b, dqdp_t)
w_b1 = -1.0d0 *plus2zero( linear_interpolate(Px_b, Pb, Pt, wap_b1, wap_t1) )
w_b2 = -1.0d0 *plus2zero( linear_interpolate(Px_b, Pb, Pt, wap_b2, wap_t2) )
w_t1 = -1.0d0 *plus2zero( linear_interpolate(Px_t, Pb, Pt, wap_b1, wap_t1) )
w_t2 = -1.0d0 *plus2zero( linear_interpolate(Px_t, Pb, Pt, wap_b2, wap_t2) )
dw_b = w_b2 - w_b1
dw_t = w_t2 - w_t1
sdwa_seg2 = -integral_linear_AB(A_b, A_t, dw_b, dw_t, Px_b, Px_t)
!----------------------
! from Px_t to Pt
!----------------------
A_b  = linear_interpolate(Px_t, Pb, Pt, dqdp_b, dqdp_t)
A_t  = dqdp_t
w_b1 = -1.0d0 *plus2zero( linear_interpolate(Px_t, Pb, Pt, wap_b1, wap_t1) )
w_b2 = -1.0d0 *plus2zero( linear_interpolate(Px_t, Pb, Pt, wap_b2, wap_t2) )
w_t1 = -1.0d0 *plus2zero( wap_t1)
w_t2 = -1.0d0 *plus2zero( wap_t2)

dw_b = w_b2 - w_b1
dw_t = w_t2 - w_t1
sdwa_seg3 = -integral_linear_AB(A_b, A_t, dw_b, dw_t, Px_t, Pt)
!----------------------
cal_sdwa = sdwa_seg1 + sdwa_seg2 + sdwa_seg3
!----------------------
RETURN
END FUNCTION cal_sdwa
!*********************************************************************
FUNCTION plus2zero(x)
  implicit none
  !---------
  double precision            x
!f2py intent(in)              x
  double precision            plus2zero
!f2py intent(out)             plus2zero

!---------
if ( x .gt. 0.0d0) then
  plus2zero = 0.0d0
else
  plus2zero = x
end if
RETURN
END FUNCTION plus2zero
!*********************************************************************
FUNCTION linear_interpolate(x, x1, x2, y1, y2)
  implicit none
  !----
  double precision               x, x1, x2, y1, y2
!f2py intent(in)                 x, x1, x2, y1, y2
  !
  double precision               linear_interpolate
!f2py intent(out)                linear_interpolate
!--------------------------------------------
if (x1 .eq. x2)then
  linear_interpolate = y1
else
  linear_interpolate = (y2 - y1) / (x2 -x1)*(x - x1) + y1
end if
RETURN
END FUNCTION linear_interpolate
!*********************************************************************

!*********************************************************************
FUNCTION integral_linear_AB(Ai,Ae,Bi,Be, Pi, Pe)
  implicit none
  !---------------------------------------
  !  A = Ai + alpha * (P - Pi),  alpha = (Ae - Ai)/(Pe - Pi)
  !  B = Bi + beta  * (P - Pi),  beta  = (Be - Bi)/(Pe - Pi)
  !
  !  A*B = {Ai + alpha*(P - Pi)}*{Bi + beta(P - Pi)}
  !  
  !  S(A*B)dP from Pi to Pe
  !      = Ai*Bi*Pe 
  !       + 1.0/2.0 *(Ai*beta + Bi*alpha)*(Pe - Pi)**2.0
  !       + 1.0/3.0 * aplha * beta *(Pe - Pi)**3.0
  !       - Ai*Bi*Pi 
  !---------------------------------------
  !-- for input --------
  double precision               Ai, Ae, Bi, Be, Pi, Pe
!f2py intent(in)                 Ai, Ae, Bi, Be, Pi, Pe
  !-- for output -------
  double precision               integral_linear_AB
!f2py intent(out)                integral_linear_AB
  !-- for calculation --
  double precision               alpha, beta
!  !---------------------
if ( Pi .eq. Pe)then
  integral_linear_AB = 0.0d0
else
  alpha = (Ae - Ai) / (Pe - Pi)
  beta  = (Be - Bi) / (Pe - Pi)
  integral_linear_AB &
    = Ai*Bi*Pe &
      + 1.0d0/2.0d0 *(Ai*beta + Bi*alpha)*((Pe - Pi)**2.0d0) &
      + 1.0d0/3.0d0 * alpha *beta *((Pe - Pi)**3.0d0) &
      - Ai*Bi*Pi
end if

RETURN
END FUNCTION integral_linear_AB
!*********************************************************************
FUNCTION integral_x_a_x_b(a, b, xi, xe)
  implicit none
!------------------------------------------------
! S{(x -a)(x -b)}dx , from xi to xe
!
!  =  1/3*(xe^3 - xi^3) - (a+b)/2 *(xe^2 - xi^2) + a*b*(xe - xi)
!------------------------------------------------
  !-- for input -----
  double precision               xi, xe, a, b
!f2py intent(in)                 xi, xe, a, b
  !-- for output ----
  double precision               integral_x_a_x_b
!------------------------------------------------
integral_x_a_x_b = 1.0d0 / 3.0d0 * (xe**3.0d0 - xi**3.0d0)&
                  -(a+b) / 2.0d0 * (xe**2.0d0 - xi**2.0d0)&
                  + a*b * (xe - xi)
RETURN
END FUNCTION integral_x_a_x_b
!*********************************************************************
FUNCTION omega_atP(nz, iz_btm, r1wap, r1lev, rPsfc, rP, rmiss)
  implicit none
  integer                           nz
  integer                           iz_btm
!f2py intent(in)                    iz_btm
  double precision,dimension(nz) :: r1wap, r1lev
!f2py intent(in)                    r1wap, r1lev
  double precision                  rPsfc, rP, rmiss
!f2py intent(in)                    rPsfc, rP, rmiss
  !---- for calculation -----------
  integer                           iz_scnd
  !---- for output ----------------
  double precision                  omega_atP
!----------------------------------
if ( -rP .lt. -rPsfc ) then
  omega_atP = rmiss
else if ( -rP .lt. -r1lev(iz_btm) ) then
  omega_atP = r1wap(iz_btm) + ( rP - r1lev(iz_btm) )&
                  *(0.0d0 - r1wap(iz_btm))/(rPsfc - r1lev(iz_btm))
else
  iz_scnd = findiz_scnd( nz, r1lev, rP )
  omega_atP =r1wap(iz_scnd)&
             + ( r1wap(iz_scnd -1) - r1wap(iz_scnd) )&
             /( r1lev(iz_scnd -1) - r1lev(iz_scnd) )&
             *( rP - r1lev(iz_scnd) )

end if
RETURN
END FUNCTION omega_atP
!*********************************************************************
FUNCTION findiz_btm(nz, r1lev, rPsfc)
  implicit none
  !--- for input -------
  integer                                       nz
  double precision,dimension(nz)             :: r1lev
!f2py intent(in)                                r1lev
  double precision                              rPsfc
!f2py intent(in)                                rPsfc
  !--- for calc  -------
  integer                                       iz
  !--- for output ------
  integer                                       findiz_btm
!f2py intent(out)                               findiz_btm
!
do iz = 1, nz
  if( -rPsfc .le. -r1lev(iz) ) then
    findiz_btm = iz
    exit
  elseif (iz .eq. nz) then
    findiz_btm = nz
    exit
  end if
end do
return
END FUNCTION findiz_btm
!*********************************************************************
FUNCTION findiz_scnd( nz, r1lev, rPlcl )
  implicit none
  integer                                      nz
  double precision,dimension(nz)           ::  r1lev
  double precision                             rPlcl
  integer                                      iz, findiz_scnd
!
do iz =1,nz
  if (r1lev(iz) .le. rPlcl)then
    findiz_scnd = iz
    exit
  elseif (iz .eq. nz) then
    findiz_scnd = -9999d0
  end if
end do
RETURN
END FUNCTION findiz_scnd

!*********************************************************************
FUNCTION cal_rdqdP(rP, rT, dP)
  implicit none
  double precision                   rP, rT, dP
!f2py intent(in)         rP, rT, dP         ! rP : [Pa], not in [hPa]
!--------
  double precision                   rP1, rP2, rT1, rT2, rqs1, rqs2
  double precision                   cal_rdqdP          ! [(g/g)/Pa], not in [(g/g)/hPa]   
!f2py intent(out)        cal_rdqdP 
!-------------------
rP1 = rP
rP2 = rP - dP
rT1 = rT
rT2 = moistadiabat(rP1, rT1, rP2, dP)
rqs1 = cal_qs(rT1, rP1)
rqs2 = cal_qs(rT2, rP2)
cal_rdqdP = (rqs2 -rqs1)/(rP2 - rP1)
!!
RETURN
END FUNCTION cal_rdqdP
!*********************************************************************
FUNCTION cal_q(rT, rP, rRH)
  implicit none
  !--------------
  double precision                  rT, rP, rRH     ! rP:[Pa], rRH:[%]
!f2py intent(in)        rT, rP, rRH
  !----
  double precision,parameter     :: repsi = 0.62185d0
  double precision                  res, re
  double precision                  cal_q
!f2py intent(out)       cal_q
  !---------------
res = cal_es(rT)
re  = rRH *0.01d0* res
cal_q = repsi * re / (rP - re)
!
RETURN
END FUNCTION cal_q
!*********************************************************************
FUNCTION lcl(rPsfc, rTsfc, rqsfc)
!###########################################################
! original code was obtained from
! http://www1.doshisha.ac.jp/~jmizushi/program/Fortran90/4.2.txt
! modified by: N.Utsumi
! f(x)=x**3+6*x**2+21*x+32
!###########################################################
implicit none
double precision                  rPsfc, rTsfc, rqsfc   ! rPsfc:[Pa]
!f2py intent(in)      rPsfc, rTsfc, rqsfc
double precision                  lcl
!f2py intent(out)     lcl
double precision      dPsfc_hPa, dTsfc, dq
double precision      x, xk, fx
double precision      delta
integer               k
INTEGER,PARAMETER :: KMAX=200
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
print *, "Psfc=",dPsfc_hPa
print *, "Tsfc=",dTsfc
print *, "q=",dq
print *, "fx=",fx
if (.not.isnan(x)) then
  STOP
endif

100 CONTINUE
!
if (isnan(x) ) then
  lcl = x    ! lcl = nan
else
  lcl = dble(x) *100.0d0  ! [hPa] -> [Pa]
endif
!-----------------
! for the case: lcl is lower than the surface (RH > 100%)
!-----------------
if (-lcl .lt. -rPsfc) then
  lcl = rPsfc
endif
!-----------------
return
END FUNCTION lcl
!**************************************************************
FUNCTION func(P, Psfc, Tsfc, q)
  implicit none
  double precision      P, Psfc, Tsfc, q
  double precision      f1, f2, func
  double precision      L
!
  double precision :: T0    = 273.16d0  !(K)
  double precision :: e0    = 6.1173d0  !(hPa)
  double precision :: Rv    = 461.7d0   !(J kg^-1 K^-1)
  !double precision :: Lv    = 2.500d6 !(J kg^-1)
  double precision :: epsi  = 0.62185d0 !(-)
  double precision :: Rd    = 287.04d0  !(J kg^-1 K^-1)
  double precision :: Cpd   = 1004.67d0 !(J kg^-1 K^-1)
!
L = dble(cal_latentheat( dble(Tsfc) ))
f1 = (1d0/T0 - Rv/L *log( q * P /( e0*(epsi + q) ) ) )**-1d0
f2 = Tsfc * ( P / Psfc )**(Rd/Cpd)
func = f1 - f2
RETURN
END FUNCTION func
!**************************************************************
FUNCTION fnewton(P, Psfc, Tsfc, q)
  implicit none
  double precision       P, Psfc, Tsfc, q
  double precision       f1, f2, func
  double precision       df1_P, df2_P, df_P
  double precision       fnewton

!
  double precision    L
  double precision :: T0    = 273.16d0  !(K)
  double precision :: e0    = 6.1173d0  !(hPa)
  double precision :: Rv    = 461.7d0   !(J kg^-1 K^-1)
  !double precision :: Lv    = 2.500d6 !(J kg^-1)
  double precision :: epsi  = 0.62185d0 !(-)
  double precision :: Rd    = 287.04d0  !(J kg^-1 K^-1)
  double precision :: Cpd   = 1004.67d0 !(J kg^-1 K^-1)
!
L = dble(cal_latentheat( dble(Tsfc) ))
f1 = (1d0/T0 - Rv/L *log( q * P /( e0*(epsi + q) ) ) )**-1d0
f2 = Tsfc * ( P / Psfc )**(Rd/Cpd)
func = f1 - f2
!
df1_P = 1d0/P * Rv/L *(1/T0 - Rv/L*log( q*P /(e0*(epsi + q)) ) )**-2d0
df2_P = Tsfc* (1d0/Psfc)**(Rd/Cpd) * Rd/Cpd * (P **(Rd/Cpd -1d0))
df_P  = df1_P - df2_P
!
fnewton = P - func / df_P
RETURN
END FUNCTION fnewton
!**************************************************************
!**************************************************************
!*********************************************************************
FUNCTION moistadiabat(rP1,rT1, rP2, dP)
  implicit none
  double precision                       rP1, rP2, rT1, dP
!f2py intent(in)             rP1, rP2, rT1, dP
  double precision                       rP, rT
  double precision                       rsign
  double precision                       rTnext, rT2, dT_dP
  double precision                       moistadiabat
!f2py intent(out)            moistadiabat
  integer                    ip, np
!
  double precision                       rtemp
!
if (rP1 .ge. rP2) then
  rsign = 1.0d0
else
  rsign = -1.0d0
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
!*********************************************************************
FUNCTION dT_dP_moist(rP, rT)
  implicit none
  double precision                        rP, rT
!f2py                         rP, rT
  double precision                        res, rqs        ! rP:[Pa], not [hPa]
  double precision                        dT_dP_moist     ! [K/Pa], not [K/hPa]
!f2py                         dT_dP_moist
!** parameters ******
  double precision                          L, a, b, c
  double precision,parameter            ::  epsi = 0.62185d0
  double precision,parameter            ::  cp   = 1004.67d0
  double precision,parameter            ::  Rd   = 287.04d0
  !double precision,parameter            ::  a0 = 0.28571d0
  !double precision,parameter            ::  b0 = 1.347e7d0
  !double precision,parameter            ::  c0 = 2488.4d0
  double precision                          rtemp
!********************
L = cal_latentheat(rT)
a = Rd / cp
b = epsi *(L**2d0)/(cp*Rd)
c = L/cp
rqs = cal_qs(rT, rP)
dT_dP_moist = (a * rT + c *rqs)/( rP *(1d0 + b*rqs/(rT**2d0) ) )
!
RETURN
END FUNCTION dT_dP_moist
!*********************************************************************
FUNCTION cal_qs(rT, rP)
  implicit none
  double precision                 rT, rP
!f2py intent(in)       rT, rP
  double precision                 res
  double precision                 cal_qs
!f2py intent(out)      cal_qs
  double precision,parameter    :: repsi = 0.62185d0
!
res = cal_es(rT)
cal_qs = repsi * res / (rP - res)
RETURN
END FUNCTION cal_qs
!*********************************************************************
FUNCTION T1toT2dry(rT1, rP1, rP2)
  implicit none
  double precision                 rT1, rP1, rP2
!f2py intent(in)       rT1, rP1, rP2   
  double precision                 T1toT2dry, rT2
!f2py intent(out)      T1toT2dry
  double precision              :: Rd    = 287.04d0  !(J kg^-1 K^-1)
  double precision              :: Cpd   = 1004.67d0 !(J kg^-1 K^-1)
!
rT2 = rT1 * (rP2/rP1)**(Rd/Cpd)
T1toT2dry = rT2
END FUNCTION T1toT2dry
!*********************************************************************
FUNCTION cal_es(rT)
  double precision rT
  double precision cal_es
!
  double precision                          L
  double precision,parameter            ::  rT0 = 273.16d0
  double precision,parameter            ::  res0= 611.73d0 ![Pa]
  !double precision,parameter            ::  Lv  = 2.5d6  ![J kg-1]
  double precision,parameter            ::  Rv  = 461.7d0 ![J K-1 kg -1]
!
L = cal_latentheat(rT)
cal_es = res0 * exp( L/Rv *(1.0d0/rT0 - 1.0d0/rT))
RETURN
END FUNCTION cal_es
!*********************************************************************
FUNCTION cal_latentheat(rT)
  implicit none
  double precision                  rT
  double precision,parameter     :: Lv = 2.5d6  ! for vaporization
  double precision,parameter     :: Ld = 2.834d6 ! for sublimation
  !double precision,parameter     :: rTliq = 273.15d0           !   0 deg.C
  !double precision,parameter     :: rTice = 250.15d0           ! -23 deg.C
  !double precision,parameter     :: rTliq = 0.0d0              ! -273.15 deg.C
  !double precision,parameter     :: rTice = 0.0d0              ! -273.15
  double precision,parameter     :: rTliq = 273.15d0           ! -273.15 deg.C
  double precision,parameter     :: rTice = 273.15d0 -50.0d0   ! -273.15
  !double precision,parameter     :: rTliq = 273.15d0 +100d0     ! 100 deg.C
  !double precision,parameter     :: rTice = 273.15d0 +100d0     ! 100
  double precision               cal_latentheat
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
!*********************************************************************
FUNCTION Psea2Psfc(Tsfc, qsfc, zsfc, Psea)
  implicit none
  double precision              Tsfc, qsfc, zsfc, Psea
!f2py intent(in)                Tsfc, qsfc, zsfc, Psea
  double precision              Psea2Psfc, Psfc
!f2py intent(out)                Psea2Psfc
  double precision              Tvsfc  ! virtual temperature
  double precision              Tvm    ! mean virtual temperature
  double precision,parameter :: lapse_e = 0.0065d0   ! [K/m]
  double precision,parameter :: g       = 9.80665d0  ! [m/s^2]
  double precision,parameter :: Rd      = 287.04d0   !(J kg^-1 K^-1)
!
Tvsfc = Tsfc * (1.0d0 + 0.61d0*qsfc)
Tvm   =  Tvsfc + 1.0d0/2.0d0 *(1.0d0 + 0.61d0*qsfc)*lapse_e * zsfc
!
Psfc  = Psea * exp(-g*zsfc/(Rd*Tvm))
Psea2Psfc = Psfc
!
RETURN
END FUNCTION Psea2Psfc
!*********************************************************************
!*********************************************************************
!*********************************************************************



end module dtanl_cmip_sbs
