module tag_fsub

CONTAINS
!***********************************************************
SUBROUTINE solve_tag_4type(a2tag, nx, ny, a2tag_tc, a2tag_c, a2tag_fbc, a2tag_nbc)
implicit none
!--- input  -----------
integer                              nx, ny
!f2py intent(in)                        nx, ny
integer,dimension(nx,ny)          :: a2tag
!f2py intent(in)                     a2tag
!--- output  -----------
integer,dimension(nx,ny)          :: a2tag_tc, a2tag_c, a2tag_fbc, a2tag_nbc
!f2py intent(out)                 :: a2tag_tc, a2tag_c, a2tag_fbc, a2tag_nbc
!--- calc --------------
integer                              ix,iy
integer                              tag, tag_c, tag_tc, tag_fbc, tag_nbc
!-----------------------
a2tag_tc    = 0
a2tag_c     = 0
a2tag_fbc   = 0
a2tag_nbc   = 0
!-----------------------
do iy = 1,ny
  do ix = 1,nx
    if (a2tag(ix,iy).gt.0)then
      tag     =  a2tag(ix,iy)
      tag_tc  =  mod(tag, 10)
      tag_c   = (mod(tag, 100) - tag_tc )/10
      tag_fbc = (mod(tag, 1000) - tag_c*10 - tag_tc )/100
      tag_nbc = (tag - tag_fbc*100 - tag_c*10 - tag_tc) /1000
      !
      a2tag_tc(ix,iy)  = tag_tc
      a2tag_c(ix,iy)   = tag_c
      a2tag_fbc(ix,iy) = tag_fbc
      a2tag_nbc(ix,iy) = tag_nbc
    end if
  end do
end do

return
END SUBROUTINE solve_tag_4type
!***********************************************************
end module tag_fsub
