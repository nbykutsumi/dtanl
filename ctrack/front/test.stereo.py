from mpl_toolkits.basemap import Basemap, cm
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import chart_para
import ctrack_func
from numpy import *
from chart_fsub import *
import subprocess
import os
from cf.plot import *
import datetime
#-- domain mask ----------------------------
plt.clf()
#-------------------------------------------
#-- x and y data -----
region = "ASAS"
year   = 2006
mon    = 4
nx_fig,ny_fig    = chart_para.ret_nxnyfig(region, year, mon)
paradate      = datetime.date(year,mon,1)
#** draw saone fronts ******************

# Basemap #
figmap = plt.figure(figsize=(8,8))
axmap  = figmap.add_axes([0.1,0.1,0.8,0.8])

## rectangular projection -------------------------
#lllon_rect, lllat_rect, urlon_rect, urlat_rect \
#           = chart_para.ret_domain_corner_rect(region)
#xdom_saone_first, xdom_saone_last, ydom_saone_first, ydom_saone_last = chart_para.ret_xydom_saone_rect_first_last(region)
#M   = Basemap( resolution="l", llcrnrlat=lllat_rect+2.0, llcrnrlon=lllon_rect, urcrnrlat=urlat_rect+2.0, urcrnrlon=urlon_rect, ax=axmap)

# stereo projection -------------------------
lon0,lat0  = chart_para.ret_lonlat_center(region)
latts      = chart_para.ret_latts(region, year, mon)
lllon, lllat, urlon, urlat \
           = chart_para.ret_domain_corner(region,year,mon)
M   = Basemap(projection="stere", lon_0=lon0, lat_0=lat0, lat_ts=latts,\
            llcrnrlat=lllat, urcrnrlat=urlat, llcrnrlon=lllon, urcrnrlon=urlon,\
            rsphere=6371200.,resolution="l",area_thresh=10000)

# coastlines #
M.drawcoastlines()

# draw parallels #
parallels = arange(0.,90,10.)
M.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)

# draw meridians #
meridians = arange(0.,360.,10.)
M.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
plt.savefig("./test.png")


