from numpy import *
from mpl_toolkits.basemap import Basemap
import ctrack_func
import ctrack_para
import matplotlib.pyplot as plt

#-------------------------------
iyear = 2004
eyear = 2004
lhour = [0,6,12,18]
season= "ALL"
ny    = 180
nx    = 360
dlat  = 1.0
dlon  = 1.0
idir ="/media/disk2/data/ibtracs/v03r04"
odir_root ="/media/disk2/out/ibtracs/sa.one"

#lllat   = -80.0
#urlat   = 80.0
#lllon   = 0.0
#urlon   = 360.0


lllat   = -80.0
urlat   = 80.0
lllon   = 0.0
urlon   = 360.0

#------------------
ddat  = {}
for year in range(iyear, eyear+1):
  siname = idir + "/Year.%04d.ibtracs_all.v03r04.csv"%(year)
  #-- open -------
  f = open(siname, "r")
  lines = f.readlines()
  f.close()
  #-- init dictionary --
  lmon  = ctrack_para.ret_lmon(season)
  #-- csv data loop -------------
  for line in lines[3:]:
    line     = line.split(",")
    isotime  = line[6].split(" ")
    date     = map(int, isotime[0].split("-"))
    mon      = date[1]
    hour     = int(isotime[1].split(":")[0])
    #--- check hour --
    if hour not in lhour:
      continue
    #--- check nature --
    nature   = line[7].strip()
    if nature not in ["TS"]:
      continue
    #-----------------
    tcname   = line[5].strip()
    tcid     = line[0]
    lat      = float(line[16])
    lon      = float(line[17])
    if (lon < 0.0):
      lon = 360.0 + lon
    ldat_temp = [lat, lon, tcname] 
    if tcid not in ddat.keys():
      ddat[tcid] = []
    else:
      ddat[tcid].append(ldat_temp)


#**********************************************
#---- Draw tc track lines -------------------
#**********************************************
# for mapping
nnx        = int( (urlon - lllon)/dlon)
nny        = int( (urlat - lllat)/dlat)
a1lon_loc  = linspace(lllon, urlon, nnx)
a1lat_loc  = linspace(lllat, urlat, nny)
LONS, LATS = meshgrid( a1lon_loc, a1lat_loc)
#------------------------
# Basemap
#------------------------
plt.clf()
print "Basemap"
figmap   = plt.figure()
axmap    = figmap.add_axes([0.1, 0.1, 0.9, 0.8])
M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
#---- para ---------------
scol = "r"
#*************\***********
for tcid in ddat.keys():
  lines = ddat[tcid]
  for i in range(len(lines)):
    #----------
    if i == len(lines)-1:
      continue
    #----------
    line_now = lines[i]
    line_nxt = lines[i+1]
    lat1     = line_now[0]
    lon1     = line_now[1] 
    lat2     = line_nxt[0]
    lon2     = line_nxt[1] 

    #------------------------------------
    if abs(lon1 - lon2) >= 180.0:
      #--------------
      print tcid,lat1,lat2, lon1,lon2


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

#-- coastline ---------------
print "coastlines"
M.drawcoastlines(color="k")

#-- meridians and parallels
meridians = 10.0
parallels = 10.0
M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1], rotation=90)
M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0])

#---- title --
stitle  = "best track: %04d-%04d season:%s"%(iyear, eyear, season)
axmap.set_title(stitle)
#--- save ---
odir   = odir_root + "/%04d-%04d/%s"%(iyear,eyear, season)
ctrack_func.mk_dir(odir) 
soname = odir + "/tclines.ibtracs_all.v03r04.%04d-%04d.%s.png"%(iyear,eyear,season)
plt.savefig(soname)
print soname
#--------------------
 
