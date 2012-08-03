from numpy import *
from  mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
#-----------------------
ny = 96
nx = 144

yres = 180.0 / (ny+1)
xres = 360.0 / nx
lats = linspace(-90.0, 90.0, ny)
lons = linspace(0.0, 360.0 - 360.0/nx, nx)
lllat  = 20.0
lllon  = 120.0
urlat  = 50.0
urlon  = 160.0

nnx    = int( (urlon - lllon)/ xres)
nny    = int( (urlat - lllat)/ yres)
#-----------------------
dir_his = "/media/disk2/out/CMIP5/day/NorESM1-M/historical/r1i1p1/tracks/dura24/wfpr/mp"
shis   = dir_his + "/mp.p00.00.c01.04.r1000.nw17_DJF_day_NorESM1-M_historical_r1i1p1.bn"
adatin = fromfile(shis, float32).reshape(17,96,144)[0]
#
figmap = plt.figure()
axmap  = figmap.add_axes([0.1, 0.1, 0.8, 0.8])
M      = Basemap(resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
#--

adat   = M.transform_scalar(adatin, lons, lats, nnx, nny)



#--
im     = M.imshow(adat, origin="lower", cmap="RdBu", interpolation="nearest")
M.drawcoastlines()
#
plt.savefig("a2.png")
plt.show()
