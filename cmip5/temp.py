from ctrack import *
from numpy import *

ix1 = 30
iy1 = 40
xgrids = 3
ygrids = 2
nx = 7
ny = 7
imiss = -9999

tout = ctrack.mk_a1xa1y(ix1, iy1, xgrids, ygrids, nx, ny, imiss)


a1x = tout[0]
a1y = tout[1]
for i in range(len(a1x)):
  print "x,y=",a1x[i], a1y[i]
