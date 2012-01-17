program temp
integer     iz
real,dimension(5)      :: r1a
do iz = 1,5
  r1a(iz) = real(iz)
end do
print *,r1a
if (r1a(3) .eq. 2.0)then
  r1a(3) = -9999.0
endif
print r1a
end program
