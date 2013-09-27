from numpy import *
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import ctrack_para

year = 2008
mon  = 6
day  = 5
hour = 0

lllat   = 0.
urlat   = 30.
lllon   = 50.
urlon   = 100.0

dpgradrange  = ctrack_para.ret_dpgradrange()
lclass  = dpgradrange.keys()
nclass  = len(lclass)
thpgrad = dpgradrange[0][0]

nx,ny   = (360,180)
model   = "org"
pgraddir_root ="/media/disk2/out/JRA25/sa.one.%s/6hr/pgrad"%(model)
stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)
#
pgraddir     = pgraddir_root + "/%04d%02d"%(year,mon)
pgradname       = pgraddir   + "/pgrad.%s.sa.one"%(stime)
a2pgrad         = fromfile(pgradname, float32).reshape(ny, nx)
a2pgrad         = ma.masked_equal(a2pgrad, -9999.0)
a2pgrad         = ma.masked_less(a2pgrad, dpgradrange[2][0])
#


a2dat   = a2pgrad
figmap  = plt.figure()
axmap   = figmap.add_axes([0, 0, 1.0, 1.0])
M       = Basemap(resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
im      = M.imshow(a2dat, origin="lower")
M.drawcoastlines()

# draw parallels #
parallels = arange(0.,90,10.)
M.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)

# draw meridians #
meridians = arange(0.,360.,10.)
M.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)

#- title -
stitle  = "%04d-%02d-%02d-%02dh"%(year,mon,day,hour)
axmap.set_title(stitle)

odir = "/media/disk2/out/cyclone/exc.track/INDIA"
oname = odir + "/tmp.png"
figmap.savefig(oname)
