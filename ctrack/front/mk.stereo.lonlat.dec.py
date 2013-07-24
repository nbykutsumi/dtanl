from mpl_toolkits.basemap import Basemap, cm
from numpy import *
import matplotlib.pyplot as plt
import chart_para
#********************************************
region = "ASAS"
#ydom_last  = 834
miss       = -9999.0

#lperiod    = [[2000,1],[2006,1],[2006,3]]
lperiod    = [[2000,1]]

ny_dec, nx_dec = (700,1600)
#-------------------
#odir  = "/home/utsumi/bin/dtanl/ctrack/chart"
odir  = "/media/disk2/out/chart/ASAS/const"

for period in lperiod:
  #------------------
  year, mon = period
  #------------------
  nx,ny      = chart_para.ret_nxnyfig(region, year, mon)
  lon0,lat0  = chart_para.ret_lonlat_center(region)
  latts      = chart_para.ret_latts(region, year, mon)
  lllon, lllat, urlon, urlat \
             = chart_para.ret_domain_corner(region, year, mon)
  
  xdom_first, xdom_last, ydom_first, ydom_last \
             = chart_para.ret_xydom_first_last(region, year, mon)

  nxdom      = xdom_last - xdom_first +1
  nydom      = ydom_last - ydom_first +1
  #------------------
  oname_lon = odir + "/stereo.lon.ASAS.%04d.%02d.bn"%(year,mon)
  oname_lat = odir + "/stereo.lat.ASAS.%04d.%02d.bn"%(year,mon)
  figname_lon = odir + "/stereo.lon.ASAS.%04d.%02d.png"%(year,mon)
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
  
  
  m.imshow(a2lon_dom, interpolation="nearest")
  plt.colorbar()
  plt.savefig(figname_lon)
  print figname_lon
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
  # make lat lon fig --> dec 
  # make x    y  fig --> dec
  #*******************************************************
  a2corres_lat    = ones([ny,nx], float32)*miss
  a2corres_lon    = ones([ny,nx], float32)*miss
  a2corres_x_fort = ones([ny,nx], float32)*miss
  a2corres_y_fort = ones([ny,nx], float32)*miss
  
  a2domainmask_dec= zeros([ny_dec,nx_dec], float32)
  #
  lon_first_dec = 60.05
  lat_first_dec = 0.05
  dlat_dec      = 0.1
  dlon_dec      = 0.1
  #--
  for iy in range(ydom_first, ydom_last+1):
    print "iy=",iy
    for ix in range(xdom_first, xdom_last+1):
      lat_org   = a2lat[iy,ix]
      lon_org   = a2lon[iy,ix]
      lat_dec   = lat_first_dec + int((lat_org - lat_first_dec + 0.5*dlat_dec) / dlat_dec)*dlat_dec
      lon_dec   = lon_first_dec + int((lon_org - lon_first_dec + 0.5*dlon_dec) / dlon_dec)*dlon_dec
      y_dec_fort   = int( (lat_org - lat_first_dec + 0.5*dlat_dec) / dlat_dec) + 1
      x_dec_fort   = int( (lon_org - lon_first_dec + 0.5*dlon_dec) / dlon_dec) + 1
      #
      if (x_dec_fort <= nx_dec) & (y_dec_fort <= ny_dec):
        a2corres_lat[iy,ix] = lat_dec
        a2corres_lon[iy,ix] = lon_dec
        #
        a2corres_x_fort[iy,ix] = x_dec_fort
        a2corres_y_fort[iy,ix] = y_dec_fort
    
        #-- domain_mask_dec #
        #a2domainmask_dec[y_dec_fort-1, x_dec_fort-1] = 1.0
      
  
  #--
  oname_lon_corres = odir + "/stereo.lon.fig2dec.ASAS.%04d.%02d.bn"%(year,mon)
  oname_lat_corres = odir + "/stereo.lat.fig2dec.ASAS.%04d.%02d.bn"%(year,mon)
  oname_x_corres   = odir + "/stereo.xfort.fig2dec.ASAS.%04d.%02d.bn"%(year,mon)
  oname_y_corres   = odir + "/stereo.yfort.fig2dec.ASAS.%04d.%02d.bn"%(year,mon)
  #oname_domainmask_dec = odir + "/domainmask_dec.ASAS.%04d.%02d.bn"%(year,mon)
  #
  figname_lon_corres = odir + "/stereo.lon.fig2dec.ASAS.%04d.%02d.png"%(year,mon)
  # 
  a2corres_lat.tofile( oname_lat_corres )
  a2corres_lon.tofile( oname_lon_corres )
  #
  a2corres_x_fort.tofile( oname_x_corres )
  a2corres_y_fort.tofile( oname_y_corres )
  print oname_x_corres
  #a2domainmask_dec.tofile( oname_domainmask_dec )
  #print oname_domainmask_dec




