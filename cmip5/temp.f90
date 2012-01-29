module ctrack
SUBROUTINE temp(a1lon,nx)
  implicit none
  integer                                nx
  double precision,dimension(nx)      :: a1lon
!f2py intent(in)

print *,a1lon
RETURN
END SUBROUTINE ctrack
end module ctrack
