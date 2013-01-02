from mpl_toolkits.basemap import Basemap, cm
from numpy import *
import matplotlib.pyplot as plt
import chart_para
#********************************************
region = "ASAS"
nx,ny      = chart_para.ret_nxnyfig(region)
lon0,lat0  = chart_para.ret_lonlat_center(region)
latts      = chart_para.ret_latts(region)
lllon, lllat, urlon, urlat \
           = chart_para.ret_domain_corner(region)

xdom_first, xdom_last, ydom_first, ydom_last \
           = chart_para.ret_xydom_first_last(region)

#nx   = 1300
#ny   = 900
#lon0 = 140.0  # center
#lat0 = 90.0   # center
#latts= 40.0
#
#lllon=106.5
#lllat=0.5
#urlon=208.0
#urlat=41.0
#
#xdom_first = 74
#xdom_last  = 1228
#ydom_first = 55
#ydom_last  = 834
nxdom      = xdom_last - xdom_first +1
nydom      = ydom_last - ydom_first +1
miss       = -9999.0
#-------------------
odir  = "/home/utsumi/bin/dtanl/ctrack/chart"
oname_lon = odir + "/stereo.lon.ASAS.bn"
oname_lat = odir + "/stereo.lat.ASAS.bn"
figname_lon = odir + "/stereo.lon.ASAS.png"
#**********************
fig = plt.figure(figsize=(8,8))
ax = fig.add_axes([0.1,0.1,0.8,0.8])
m = Basemap(projection="stere", lon_0=lon0, lat_0=lat0, lat_ts=latts,\
            llcrnrlat=lllat, urcrnrlat=urlat, llcrnrlon=lllon, urcrnrlon=urlon,\
            rsphere=6371200.,resolution="l",area_thresh=10000)
m.drawcoastlines()
# draw parallels.
parallels = arange(0.,90,10.)
m.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
# draw meridians
meridians = arange(0.,360.,10.)
m.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
a2lon_dom, a2lat_dom = m.makegrid(nxdom,nydom)

#-- correct a2lon  west degree --> east degree
a2lon_dom  = ma.masked_greater_equal(a2lon_dom, 0.0) \
            + ones([nydom, nxdom],float32)*360.0
a2lon_dom  = a2lon_dom.data


#m.imshow(a2lon_dom, interpolation="nearest")
#plt.colorbar()
#plt.savefig(figname_lon)
#**********************
a2lon     = ones([ny,nx],float32)*miss
a2lat     = ones([ny,nx],float32)*miss

#----------------------
a2lon[ydom_first:ydom_first+nydom,xdom_first:xdom_first+nxdom] = a2lon_dom
a2lat[ydom_first:ydom_first+nydom,xdom_first:xdom_first+nxdom] = a2lat_dom
#
a2lon.tofile(oname_lon)
a2lat.tofile(oname_lat)



#*******************************************************
# make lat lon fig --> saone
# make x    y  fig --> saone
#*******************************************************
a2corres_lat    = ones([ny,nx], float32)*miss
a2corres_lon    = ones([ny,nx], float32)*miss
a2corres_x_fort = ones([ny,nx], float32)*miss
a2corres_y_fort = ones([ny,nx], float32)*miss
#
lon_first_saone = 0.5
lat_first_saone = -89.5
dlat_saone      = 1.0
dlon_saone      = 1.0
#--
for iy in range(ydom_first, ydom_last+1):
  for ix in range(xdom_first, xdom_last+1):
    lat_org   = a2lat[iy,ix]
    lon_org   = a2lon[iy,ix]
    lat_saone = lat_first_saone + int((lat_org - lat_first_saone + 0.5*dlat_saone) / dlat_saone)*dlat_saone
    lon_saone = lon_first_saone + int((lon_org - lon_first_saone + 0.5*dlon_saone) / dlon_saone)*dlon_saone
    y_saone_fort   = int( (lat_org - lat_first_saone + 0.5*dlat_saone) / dlat_saone) + 1
    x_saone_fort   = int( (lon_org - lon_first_saone + 0.5*dlon_saone) / dlon_saone) + 1
    #
    a2corres_lat[iy,ix] = lat_saone
    a2corres_lon[iy,ix] = lon_saone
    #
    a2corres_x_fort[iy,ix] = x_saone_fort
    a2corres_y_fort[iy,ix] = y_saone_fort

#--
oname_lon_corres = odir + "/stereo.lon.fig2saone.ASAS.bn"
oname_lat_corres = odir + "/stereo.lat.fig2saone.ASAS.bn"
oname_x_corres   = odir + "/stereo.xfort.fig2saone.ASAS.bn"
oname_y_corres   = odir + "/stereo.yfort.fig2saone.ASAS.bn"
#
figname_lon_corres = odir + "/stereo.lon.fig2saone.ASAS.png"
# 
a2corres_lat.tofile( oname_lat_corres )
a2corres_lon.tofile( oname_lon_corres )
#
a2corres_x_fort.tofile( oname_x_corres )
a2corres_y_fort.tofile( oname_y_corres )
#

