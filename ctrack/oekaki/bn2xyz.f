c**********************************************************************
c     hlf2xyz 
c
c     By : s_wata
c     On : 2010/11
c     At : IIS, The University of Tokyo
c
c**********************************************************************
c     Definition
c**********************************************************************
c
      implicit none
c input
      real             x, y
      integer          nx, ny
      parameter        (nx=144)
      parameter        (ny=96)
      real             lon(nx)
      real             lat(ny)
      real             a(nx,ny)
      character*384     input
      character*384    output

c local
      integer          i,j,k,l
c
c**********************************************************************
c
c**********************************************************************
c
      call getarg(1,input)

c      write (*,*) input

      open (15, file=input,
     &      status='unknown',
     &      form='unformatted',access='direct',
     &      recl=nx*ny)    !! input

      read(15,rec=1) ((a(i,j),i=1,144), j=1,96 )

      do x=1,nx   !! calculate lon & lat
       lon(x) = (x-1)*2.5
c       write (*,*) lon(x)
      end do

      do y=1,ny
       lat(y) = (y-1)*1.8947-90
c       write (*,*) lat(y)
      end do


      do k=1,ny
        do l=1,nx
c         write (16, '(f8.4,f9.4,f12.5)') lon(l),lat(k),a(l,k)
          write (*,'(f8.4,f9.4,f11.4)') lon(l),lat(k),a(l,k)
        end do
      end do

c
      close(15)

      end

