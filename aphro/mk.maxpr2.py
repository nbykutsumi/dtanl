from numpy import *
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from cf.plot import *
#*************************************************
iyear = 1998
eyear = 2011
#eyear = 1999
nyear = eyear - iyear + 1
varkey = 14
nx   = 460
ny   = 440 
nvar = 54
#
lllat   = 24.0
lllon   = 123.0
urlat   = 46.0
urlon   = 146.0
dlon    = 0.05
dlat    = 0.05
#
lats    = linspace(lllat, urlat, ny)
lons    = linspace(lllon, urlon, nx)
#
nnx     = int( (urlon - lllon)/dlon)
nny     = int( (urlat - lllat)/dlat)
#*************************************************
a3temp  = zeros([nyear, ny, nx], float32)
i  = -1
#---------
for year in range(iyear, eyear+1):
  i = i +1
  iname = "./AphroJP_V1207_DPREC_ext.%04d"%(year)
  a2in = fromfile(iname, float32).reshape(nvar, ny, nx)[varkey]
  a3temp[i] = a2in
#---------
a2out = zeros([ny, nx], float32)
for iy in range(0, ny):
  print "iy=",iy
  for ix in range(0, nx):
    a2out[iy, ix] = max(a3temp[:,iy,ix])
#---------
oname   = "./maxpr.bn"
a2out.tofile(oname)

#---------------------------
# for figure
#---------------------------
figmap  = plt.figure()
axmap   = figmap.add_axes([0, 0.1, 1.0, 0.8])
M       = Basemap(resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax= axmap)
#-- transform ----
a2out_trans  = M.transform_scalar(a2out, lons, lats, nnx, nny)

#--- for colorbar ------
bnd      = list(range(0, 600+1, 100))
bnd_cbar = bnd + [1.0e+10]
#-----------------------
print "imshow"
#im       = M.imshow(a2out_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap="jet_r", interpolation="nearest")
im       = M.imshow(a2out_trans, origin="lower", cmap="jet_r", interpolation="nearest")
#plt.colorbar(im, boundaries=bnd_cbar, extend="max")
plt.colorbar(im, extend="max")
#-  superimpose shade -----
print "superimpose"
cmshade  = matplotlib.colors.ListedColormap([(0.8, 0.8, 0.8), (0.8, 0.8, 0.8)])
a2shade  = ma.masked_greater_equal(a2out_trans, 0.0)
im       = M.imshow(a2shade, origin="lower", cmap=cmshade, interpolation="nearest")

#--------------------------
print "drawcoastlines"
M.drawcoastlines()
figname = oname[:-3] + ".png"
figmap.savefig(figname)
print figname
