module test

CONTAINS

subroutine f(a)
  implicit none
  !----
  double precision    a
!f2py intent(in)
  print *,"a*2=", a*2
end subroutine f

end module test

