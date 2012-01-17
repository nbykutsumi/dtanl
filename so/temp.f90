module temp

CONTAINS
!*****************
FUNCTION f(x)
  implicit none
  real               x
!f2py intent(in)     x
  real               f
!f2py intent(out)    f
!-----------------
f = x*2
!-----------------
RETURN
END FUNCTION

!*****************
end module temp
