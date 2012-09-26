from numpy import *

a = 5.0
ny   = 96
nx   = 144
a2pr    = zeros([ny, nx], float32)
a2pgrad = ones([ny, nx], float32) * -9999.0

yc  = 48
xc  = 3
for iy in range(0, ny):
  for ix in range(0, nx):
    # vpr  = 1.0 - ((ix -xc)**2 + (iy - yc)**2)**0.5 
    vpr  = cos(2*pi*(ix-xc)/nx) * cos( 2*pi*(iy -yc)/ny)
    #vpr  = cos(2*pi*(ix-xc)/nx)
    a2pr[iy, ix] = vpr

a2pgrad[yc, xc] = 1000.0

a2pr.tofile("/home/utsumi/bin/dtanl/ctrack/temp/pr.bn")
a2pgrad.tofile("/home/utsumi/bin/dtanl/ctrack/temp/pgrad.bn")


