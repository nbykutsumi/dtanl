from numpy import *
from classtest import BoundaryNorm, BoundaryNormSymm
from matplotlib import colors
import matplotlib.pyplot as plt
from numpy import *
import matplotlib as mpl
from mpl_toolkits.basemap import Basemap

spdir_his      = '/media/disk2/out/CMIP5/day/NorESM1-M/historical/r1i1p1/tracks/dura24/wfpr/sp'
snumdir_his    = '/media/disk2/out/CMIP5/day/NorESM1-M/historical/r1i1p1/tracks/dura24/wfpr/num'

sname_his      = spdir_his   + "/sp.p00.00.c-1.04.r1000.nw17_DJF_day_NorESM1-M_historical_r1i1p1.bn"
snum_his       = snumdir_his + "/num.p00.00.c-1.04.r1000.nw17_DJF_day_NorESM1-M_historical_r1i1p1.bn"


asum_his       = fromfile(sname_his, float32).reshape(17,96,144)[0] *60*60*24
anum_his       = fromfile(snum_his,  float32).reshape(17,96,144)[0]
a_his          = ma.masked_where(anum_his==0.0, asum_his) / anum_his

spdir_fut      = '/media/disk2/out/CMIP5/day/NorESM1-M/rcp85/r1i1p1/tracks/dura24/wfpr/sp'
snumdir_fut    = '/media/disk2/out/CMIP5/day/NorESM1-M/rcp85/r1i1p1/tracks/dura24/wfpr/num'
smpdir_fut     = "/media/disk2/out/CMIP5/day/NorESM1-M/rcp85/r1i1p1/tracks/dura24/wfpr/mp"

sname_fut      = spdir_fut   + "/sp.p00.00.c-1.04.r1000.nw17_DJF_day_NorESM1-M_rcp85_r1i1p1.bn"
snum_fut       = snumdir_fut + "/num.p00.00.c-1.04.r1000.nw17_DJF_day_NorESM1-M_rcp85_r1i1p1.bn"


asum_fut       = fromfile(sname_fut, float32).reshape(17,96,144)[0] *60*60*24
anum_fut       = fromfile(snum_fut,  float32).reshape(17,96,144)[0]
a_fut          = ma.masked_where(anum_fut==0.0, asum_fut) / anum_fut

a_dif          = a_fut - a_his
#a_dif          = a_dif.filled(0.0)

#-------------
smpdir_his     = "/media/disk2/out/CMIP5/day/NorESM1-M/historical/r1i1p1/tracks/dura24/wfpr/mp"
smp_his        = smpdir_his  + "/mp.p00.00.c-1.04.r1000.nw17_DJF_day_NorESM1-M_historical_r1i1p1.bn"
amp_his        = fromfile(smp_his,    float32).reshape(17,96,144)[0] *60*60*24

smpdir_fut     = "/media/disk2/out/CMIP5/day/NorESM1-M/rcp85/r1i1p1/tracks/dura24/wfpr/mp"
smp_fut        = smpdir_fut  + "/mp.p00.00.c-1.04.r1000.nw17_DJF_day_NorESM1-M_rcp85_r1i1p1.bn"
amp_fut        = fromfile(smp_fut,    float32).reshape(17,96,144)[0] *60*60*24

amp_dif        = amp_fut - amp_his

#-------------

cnddir_his     = "/media/disk2/out/CMIP5/day/NorESM1-M/historical/r1i1p1/cnd.mean/pr/1990-1999/12-02"
cnddir_fut     = "/media/disk2/out/CMIP5/day/NorESM1-M/rcp85/r1i1p1/cnd.mean/pr/2086-2095/12-02"

scnd_his       = cnddir_his + "/pr_day_NorESM1-M_historical_r1i1p1_000.00.bn"
scnd_fut       = cnddir_fut + "/pr_day_NorESM1-M_rcp85_r1i1p1_000.00.bn"

acnd_his       = fromfile(scnd_his, float32).reshape(96,144)*60*60*24.0
acnd_fut       = fromfile(scnd_fut, float32).reshape(96,144)*60*60*24.0

acnd_dif       = acnd_fut - acnd_his


M          = Basemap(resolution="l", llcrnrlat=-90.0, llcrnrlon=0.0, urcrnrlat=90.0, urcrnrlon=360.0)
bnd        = [-3.0, -2.0, -1.0, -0.5, 0.5, 1.0, 2.0, 3.0]
im         = M.imshow(a_dif, origin="lower", norm=BoundaryNormSymm(bnd), cmap= "RdBu")
#im         = M.imshow(a1, origin="lower")
M.drawcoastlines()
plt.colorbar()
plt.savefig("a_dif.png")
plt.clf()

M          = Basemap(resolution="l", llcrnrlat=-90.0, llcrnrlon=0.0, urcrnrlat=90.0, urcrnrlon=360.0)
bnd        = [-3.0, -2.0, -1.0, -0.5, 0.5, 1.0, 2.0, 3.0]
im         = M.imshow(amp_dif, origin="lower", norm=BoundaryNormSymm(bnd), cmap= "RdBu")
M.drawcoastlines()
plt.colorbar()
plt.savefig("amp_dif.png")
plt.clf()


M          = Basemap(resolution="l", llcrnrlat=-90.0, llcrnrlon=0.0, urcrnrlat=90.0, urcrnrlon=360.0)
bnd        = [-3.0, -2.0, -1.0, -0.5, 0.5, 1.0, 2.0, 3.0]
im         = M.imshow(acnd_dif, origin="lower", norm=BoundaryNormSymm(bnd), cmap= "RdBu")
M.drawcoastlines()
plt.colorbar()
plt.savefig("acnd_dif.png")
plt.clf()

