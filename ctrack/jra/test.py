from mpl_toolkits.basemap import Basemap, cm
# requires netcdf4-python (netcdf4-python.googlecode.com)
import numpy as np
import matplotlib.pyplot as plt

nx   = 300
ny   = 200
lon0 = 140.0  # center
lat0 = 40.0   # center
lllon=106.5
lllat=0.5
urlon=208.0
urlat=41.0



fig = plt.figure(figsize=(8,8))
ax = fig.add_axes([0.1,0.1,0.8,0.8])
m = Basemap(projection="stere", lon_0=lon0, lat_0=90, lat_ts=lat0,\
            llcrnrlat=lllat, urcrnrlat=urlat, llcrnrlon=lllon, urcrnrlon=urlon,\
            rsphere=6371200.,resolution="l",area_thresh=10000)
m.drawcoastlines()
# draw parallels.
parallels = np.arange(0.,90,10.)
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
# draw meridians
meridians = np.arange(0.,360.,10.)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
lons, lats = m.makegrid(nx,ny)
