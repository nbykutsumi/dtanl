from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from numpy import *
import calendar
import ctrack_para
import ctrack_func
import sys, os
#--------------------------------------
#year    = 2001
#mon     = 1
#day     = 1
#hour    = 12

if len(sys.argv) >1:
  year    = int(sys.argv[1])
  iyear   = year
  eyear   = year
  season  = int(sys.argv[2])
  iday    = int(sys.argv[3])
  eday    = int(sys.argv[4])
else:
  print "cmd [year] [mon] [iday] [eday]"
  sys.exit()
#----
ny      = 180
nx      = 360

miss_int= -9999
# local region ------
#
# corner points should be
# at the center of original grid box

lllat   = 25.
urlat   = 60.
lllon   = 110.
urlon   = 180.

#lllat   = -89.5
#urlat   = 89.5
#lllon   = 0.5
#urlon   = 359.5

thdura  = 72

#----------------------------
lmon = ctrack_para.ret_lmon(season)
#lmon = [1]
#----------------------------
dlat    = 1.0
dlon    = 1.0
a1lat   = arange(-89.5, 89.5 +dlat*0.5,  dlat)
a1lon   = arange(0.5,   359.5 +dlon*0.5, dlon)
#----------------------------
#----------------------------

psldir_root     = "/media/disk2/out/chart/ASAS/exc"
lifedir_root    = "/media/disk2/out/chart/ASAS/exc/life"
nextposdir_root = "/media/disk2/out/chart/ASAS/exc/nextpos"

#************************************
ltrack     = []
#------------------------------------
for year in [year]:
  for mon in lmon:
    ##############
    for day in range(iday, eday+1):
    #for day in range(31, 31+1):
      print year, mon, day
      for hour in [0, 12]:

        stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)

        psldir          = psldir_root     + "/%04d%02d"%(year, mon)
        lifedir         = lifedir_root    + "/%04d%02d"%(year, mon)
        nextposdir      = nextposdir_root + "/%04d%02d"%(year, mon)
        
        pslname         = psldir     + "/exc.ASAS.%04d.%02d.%02d.%02d.sa.one"%(year,mon,day,hour)
        lifename        = lifedir    + "/life.%s.sa.one"%(stime)
        nextposname     = nextposdir + "/nextpos.%s.sa.one"%(stime)
        
        a2psl           = fromfile(pslname,   float32).reshape(ny, nx)
        a2life          = fromfile(lifename,  int32).reshape(ny, nx)
        a2nextpos       = fromfile(nextposname,  int32).reshape(ny, nx)
        #************************
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
            ##-- check duration -----
            #life  = a2life[iy, ix]
            #dura  = ctrack_func.solvelife_point_py(life, miss_int)[1]
            #if  (dura < thdura):
            #  continue
        
            #-----------------------
            nextpos   = a2nextpos[iy, ix]
            x_next, y_next = ctrack_func.fortpos2pyxy(nextpos, nx, miss_int)
            if ( (x_next == miss_int) & (y_next == miss_int) ):
              continue
            #------
            lat_next  = a1lat[y_next]
            lon_next  = a1lon[x_next]
            #
            ltrack.append([[year, mon, day, hour],[lat, lon, lat_next, lon_next]])
            print lat_next, lon_next        
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
axmap    = figmap.add_axes([0.1, 0.1, 0.8, 0.8])
M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)

#-- draw cyclone tracks ------
itemp = 1
#-----------
for track in ltrack:
  itemp = itemp + 1
  year = track[0][0]
  mon  = track[0][1]
  day  = track[0][2]
  hour = track[0][3]

  lat1 = track[1][0]
  lon1 = track[1][1]
  lat2 = track[1][2]
  lon2 = track[1][3]

  scol="r"

  #------------------------------------
  if abs(lon1 - lon2) >= 180.0:
    #--------------
    if (lon1 > lon2):
      lon05_1  = 360.0
      lon05_2  = 0.0
      lat05    = lat1 + (lat2 - lat1)/(lon05_1 - lon1 + lon2 - lon05_2)*(lon05_1 - lon1)
    elif (lon1 < lon2):
      lon05_1  = 0.0
      lon05_2  = 360.0
      lat05    = lat1 + (lat2 - lat1)/(lon05_1 - lon1 + lon2 - lon05_2)*(lon05_1 - lon1)
    #--------------
    M.plot( (lon1, lon05_1), (lat1, lat05), linewidth=1, color=scol)
    M.plot( (lon05_2, lon2), (lat05, lat2), linewidth=1, color=scol)
    #--------------
  else:
    M.plot( (lon1, lon2), (lat1, lat2), linewidth=1, color=scol)
  #
  xtext, ytext = M(lon1,lat1)
  plt.text(xtext,ytext-1, "%02d.%02d"%(day,hour) ,fontsize=12, rotation=-90)

#-- coastline ---------------
print "coastlines"
M.drawcoastlines(color="k")

# draw parallels #
parallels = arange(0.,90,10.)
M.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)

# draw meridians #
meridians = arange(0.,360.,10.)
M.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)


#-- save --------------------
print "save"
sodir   = "/media/disk2/out/cyclone/exc.track/JPN"
soname  = sodir + "/exc.tracklines.JPN.chartc.%04d.%02d.%02d-%02d.png"%(year,season, iday, eday)
plt.savefig(soname)
plt.clf()
print soname
plt.clf()
