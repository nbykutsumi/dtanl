subroutine func1(n,x,y)
implicit none
integer  n
real,dimension(n)   :: x
!f2py intent(in) x
real,dimension(n)   :: y
!f2py intent(out)
print *,"n=",n
print *,"x=",x
y = x*20.0
print *,"y=x*20.0=",y
end


!subroutine func2(x,y,n)
!implicit none
!integer  n
!real*8  x(n)
!real*8  y(n)
!integer i
!write(*,*) "func2 is called from sample1.f"
!do i = 1,n
!  y(i) = x(i)**2
!end do
!end
