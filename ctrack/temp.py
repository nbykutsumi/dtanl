from numpy import *
from ctrack_fsub import *

radkm  = 1000.0
nx,ny  = 360,180
ix = 140
iy = 90+36
thdist = 1000.0* 1000.0
miss   = -9999.0
lat_first = -89.5
dlat      = 1.0
dlon      = 1.0

a = ctrack_fsub.mk_territory_point_saone(nx,ny,ix,iy,thdist,miss,lat_first,dlat,dlon).T
print a
