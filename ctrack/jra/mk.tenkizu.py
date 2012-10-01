from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from numpy import *
import calendar
import ctrack_para
import ctrack_func
import sys, os
#--------------------------------------

#**********************************************
def tenkizu_single(year, mon, day, hour):
  ny      = 180
  nx      = 360
  # local region ------
  #
  # corner points should be
  # at the center of original grid box
  lllat   = 20.
  urlat   = 50.
  lllon   = 110.
  urlon   = 165.
  
  thdura  = 24
  miss_int= -9999


  stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)

  sodir_root    = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu"
  sodir         = sodir_root + "/%04d%02d"%(year, mon)
  ctrack_func.mk_dir(sodir)

  soname        = sodir + "/tenkizu.%s.png"%(stime)
  #----------------------------
  dlat    = 1.0
  dlon    = 1.0
  a1lat   = arange(-89.5, 89.5  + dlat*0.1, dlat)
  a1lon   = arange(0.5,   359.5 + dlon*0.1, dlon)

  meridians = 10.0
  parallels = 10.0

  #----------------------------
  dpgradrange  = ctrack_para.ret_dpgradrange()
  lclass  = dpgradrange.keys()
  nclass  = len(lclass)
  thpgrad = dpgradrange[0][0]
  #----------------------------
  
  
  psldir_root     = "/media/disk2/data/JRA25/sa.one/6hr/PRMSL"
  pgraddir_root   = "/media/disk2/out/JRA25/sa.one/6hr/pgrad"
  lifedir_root    = "/media/disk2/out/JRA25/sa.one/6hr/life"
  
  psldir          = psldir_root   + "/%04d%02d"%(year, mon)
  pgraddir        = pgraddir_root + "/%04d%02d"%(year, mon)
  lifedir         = lifedir_root  + "/%04d%02d"%(year, mon)
  
  pslname         = psldir   + "/fcst_phy2m.PRMSL.%s.sa.one"%(stime)
  pgradname       = pgraddir + "/pgrad.%s.sa.one"%(stime)
  lifename        = lifedir  + "/life.%s.sa.one"%(stime)
  
  a2psl           = fromfile(pslname,   float32).reshape(ny, nx)
  a2pgrad         = fromfile(pgradname, float32).reshape(ny, nx)
  a2life          = fromfile(lifename,  int32).reshape(ny, nx)
  #************************
  # PSL Pa --> hPa
  a2psl           = a2psl * 0.01
  
  dcenter  = {}
  for iclass in lclass:
    dcenter[iclass] = []
  #------------------------
  for iy in range(0, ny):
    #---------------
    lat       = a1lat[iy]
    if ((lat < lllat) or (urlat < lat)):
      continue
    #---------------
    for ix in range(0, nx):
      #-------------
      lon     = a1lon[ix]
      if ((lon < lllon) or (urlon < lon)):
        continue
      #-------------
      pgrad   = a2pgrad[iy, ix]
      #------
      if (pgrad < thpgrad):
        continue
  
      #-- check duration -----
      life  = a2life[iy, ix]
      dura  = ctrack_func.solvelife_point_py(life, miss_int)[1]
      if  (dura < thdura):
        continue
  
      #-----------------------
      for iclass in lclass[1:]:
        pgrad_min = dpgradrange[iclass][0]
        pgrad_max = dpgradrange[iclass][1]
        if (pgrad_min <= pgrad < pgrad_max):
          dcenter[iclass].append([lat, lon])
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
  
  #-- transform -----------
  print "transform"
  a2psl_trans  = M.transform_scalar( a2psl, a1lon, a1lat, nnx, nny)
  
  #-- contour   -----------
  print "contour"
  llevels  = arange(900.0, 1100.0, 2.0).tolist()
  im       = M.contour(LONS, LATS, a2psl_trans, latlon=True, levels=llevels,  colors="k")
  plt.clabel(im, fontsize=9, inline=1, fmt="%d")
  
  #-- plot cyclone centers ---
  print "plot cyclone centers"
  for iclass in lclass[1:]:
    if (len(dcenter[iclass]) ==  0.0):
      continue
    #-----------
    for latlon in dcenter[iclass]:
      lat = latlon[0]
      lon = latlon[1]
      M.scatter( lon, lat, color="r", marker="o", s=100)
      x_plot, y_plot = M(lon, lat+0.5)
      plt.text(x_plot, y_plot, "%d"%(iclass), color="r", fontsize=15)
  
  #-- coastline ---------------
  print "coastlines"
  M.drawcoastlines()

  #-- meridians and parallels
  M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1]) 
  M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0]) 
  #-- save --------------------
  print "save"
  plt.savefig(soname)
  plt.clf()
  print soname
#***************************************

iyear   = 2001
eyear   = 2001
imon    = 1
emon    = 12

iday    = 1

for year in range(iyear, eyear+1):
  for mon in range(imon, emon+1):
    ##############
    # no leap
    ##############
    if (mon==2)&(calendar.isleap(year)):
      eday = calendar.monthrange(year,mon)[1] -1
    else:
      eday = calendar.monthrange(year,mon)[1]
    #-------------
    for day in range(iday, eday+1):
      print year, mon
      for hour in [12]:
        tenkizu_single(year, mon, day, hour)
