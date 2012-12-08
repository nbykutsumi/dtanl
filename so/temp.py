from dtanl_fsub import *
from numpy import *
import ctrack_func
import ctrack_para
import matplotlib.pyplot as plt
import matplotlib
import sys,os
import datetime
from cf.plot import *
#---------------------------
lllat   = 20.
urlat   = 60.
lllon   = 110.
urlon   = 160.

dlat    = 1.0
dlon    = 1.0
a1lat   = arange(-89.5, 89.5  + dlat*0.1, dlat)
a1lon   = arange(0.5,   359.5 + dlon*0.1, dlon)

meridians = 10.0
parallels = 10.0

v = 1000.0


idir = "/media/disk2/data/JRA25/sa.one/6hr/PRMSL/200407"
iname = idir + "/anal_p25.PRMSL.2004070100.sa.one"

a2psl = fromfile(iname, float32).reshape(180,360)*0.01
#a2cont = dtanl_fsub.mk_a2contour(a2psl.T, v).T

#************************
# for mapping
nnx        = int( (urlon - lllon)/dlon)
nny        = int( (urlat - lllat)/dlat)
a1lon_loc  = linspace(lllon, urlon, nnx)
a1lat_loc  = linspace(lllat, urlat, nny)
LONS, LATS = meshgrid( a1lon_loc, a1lat_loc)
#------------------------
# Basemap
#------------------------
print "Basemap"
figmap   = plt.figure()
axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)

#---------------------------
a2psl_trans = M.transform_scalar(a2psl, a1lon, a1lat, nnx, nny)
a2cont_trans = dtanl_fsub.mk_a2contour_regional(a2psl_trans.T, v).T
#a2cont_trans = M.transform_scalar(a2cont, a1lon, a1lat, nnx, nny)

#---------------------------
im    = M.imshow(a2cont_trans, origin="lower", interpolation="nearest")
M.drawcoastlines()
#-- meridians and parallels
M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1])
M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0])

figname = "./temp.png"
plt.savefig(figname)
plt.clf()
print figname

#------------------------
# Basemap
#------------------------
print "Basemap"
figmap   = plt.figure()
axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
#---------------------------
a2psl_trans = M.transform_scalar(a2psl, a1lon, a1lat, nnx, nny)
a2cont_trans = dtanl_fsub.mk_a2contour_regional(a2psl_trans.T, v).T
#im    = M.imshow(a2psl, origin="lower", interpolation="nearest")
im    = M.contour(LONS, LATS, a2psl_trans, latlon=True)
M.drawcoastlines()
#-- meridians and parallels
M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1])
M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0])

figname = "./temp2.png"
plt.savefig(figname)
plt.clf()
print figname
