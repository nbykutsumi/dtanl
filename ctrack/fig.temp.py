from mpl_toolkits.basemap import Basemap
from numpy import *
import matplotlib.pyplot as plt
from cf.plot import *
#----------------------
dir_dif="/media/disk2/out/CMIP5/day/NorESM1-M/dif/rcp85/1990-1999.2086-2095/tracks/dura24/wfpr"

#bnd_mp       = [-3.0, -2.0, -1.0, -0.1, 0.1, 1.0, 2.0, 3.0]
bnd_mp       = [-2.0, -1.0, -0.1, 0.1, 1.0, 2.0]
sdif_mp   = dir_dif + "/mp/dif.mp.p00.00.c-1.04.r1000.nw17_DJF_day_NorESM1-M_historical_r1i1p1.bn"
adif_mp   = fromfile(sdif_mp, float32).reshape(17,96,144)[0]
adif_mp   = adif_mp * 60.*60.*24


M      = Basemap(resolution="i", llcrnrlat=20.0, urcrnrlat=90, llcrnrlon=0.0, urcrnrlon=360)

im_mp     = M.imshow(adif_mp, origin="lower", norm=BoundaryNormSymm(bnd_mp), cmap="RdBu")

M.drawcoastlines()
bnd_cbar   = [-1.0e+20] + bnd_mp + [1.0e+20]
plt.colorbar(im_mp, boundaries=bnd_cbar, extend="both")
plt.show()

