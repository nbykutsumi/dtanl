from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib
from numpy import *
import calendar
import ctrack_para
import ctrack_func
import sys, os
import gsmap_func
from cf.plot import *
import datetime
#--------------------------------------
if len(sys.argv) > 1:
  year  = int(sys.argv[1])
  mon   = int(sys.argv[2])
  day   = int(sys.argv[3])
  hour  = int(sys.argv[4])
  lllat = float(sys.argv[5])
  urlat = float(sys.argv[6])
  lllon = float(sys.argv[7])
  urlon = float(sys.argv[8])
  plev = float(sys.argv[9])
  cbarflag = sys.argv[10]
  thdura = float(sys.argv[11])

else:
  year  = 2004
  mon   = 7
  day   = 18
  hour  = 0
  #local region ------
  #corner points should be
  #at the center of original grid box
  #lllat   = 20.
  #urlat   = 60.
  #lllon   = 110.
  #urlon   = 160.
  lllat   = 0.0
  urlat   = 89.
  lllon   = 50.
  urlon   = 280.
  thdura  = 6
  plev    = 250 *100.0   #(Pa)
  #plev    = 850 *100.0   #(Pa)
  #plev    = 500 *100.0   #(Pa)
  cbarflag= "True"

#**********************************************
def shifttime(year, mon, day, hour, hour_inc):
  now         = datetime.datetime(year, mon, day, hour)
  dhour       = datetime.timedelta(hours = hour_inc)
  target      = now + dhour
  year_target = target.year
  mon_target  = target.month
  day_target  = target.day
  hour_target = target.hour
  return (year_target, mon_target, day_target, hour_target)
#**********************************************
#---------------------
ny      = 180
nx      = 360

miss_int= -9999


stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)

sodir_root    = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/%02dh"%(thdura)
sodir         = sodir_root + "/%04d%02d/baiu/%02d"%(year, mon, day)
ctrack_func.mk_dir(sodir)

soname        = sodir + "/tenkizu.wind.%04d.%02d.%02d.%02d.%04dhPa.png"%(year, mon, day, hour, plev*0.01)
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
#--- value ------------------
a2v           = zeros([ny, nx])
a2num         = zeros([ny, nx])
a2one         = ones([ny, nx])
#
lhour_inc     = [0]
for hour_inc in lhour_inc:
  (year_t, mon_t, day_t, hour_t) = shifttime(year, mon, day, hour, hour_inc)
  print day, year_t, mon_t, day_t, hour_t
  idir_root  = "/media/disk2/data/JRA25/sa.one/6hr"
  udir       = idir_root + "/UGRD/%04d%02d"%(year_t, mon_t)
  vdir       = idir_root + "/VGRD/%04d%02d"%(year_t, mon_t)
  uname      = udir + "/anal_p25.UGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev*0.01, year_t, mon_t, day_t, hour_t)
  vname      = vdir + "/anal_p25.VGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev*0.01, year_t, mon_t, day_t, hour_t)
  a2u_t      = fromfile(uname, float32).reshape(180, 360)
  a2v_t      = fromfile(vname, float32).reshape(180, 360)

a2u          = a2u_t
a2v          = a2v_t
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
a2u_trans    = M.transform_scalar( a2u,   a1lon, a1lat, nnx, nny) 
a2v_trans    = M.transform_scalar( a2v,   a1lon, a1lat, nnx, nny) 
#--- 
a2psl_trans  = M.transform_scalar( a2psl, a1lon, a1lat, nnx, nny)
#

#-- boundaries ----------
#bnd        = [1,3,5,7,9,11,13,15,17]
bnd        = list(arange(0,21+1,3))
bnd_cbar   = [-1.0e+40] + bnd + [1.0e+40]

#-- color ---------------
#scm      = "rainbow"
scm      = "Spectral_r"
#scm      = "gist_rainbow"
cminst   = matplotlib.cm.get_cmap(scm, len(bnd))
acm      = cminst( arange( len(bnd) ) )
lcm      = [[1,1,1,1]]+ acm.tolist()
mycm      = matplotlib.colors.ListedColormap( lcm )
##-- vector imshow --------
#im       = M.quiver(LONS, LATS, a2u_trans, a2v_trans, angles="xy")

#-- imshow    -----------
#a2wind_trans = (a2u_trans**2.0 + a2v_trans**2.0)**0.5
a2wind_trans = a2u_trans

im       = M.imshow(a2wind_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")

#-- contour   -----------
#print "contour"
#llevels  = arange(900.0, 1100.0, 2.0).tolist()
#im       = M.contour(LONS, LATS, a2psl_trans, latlon=True, levels=llevels,  colors="k")
#plt.clabel(im, fontsize=9, inline=1, fmt="%d")
#
##-- plot cyclone centers ---
#print "plot cyclone centers"
#for iclass in lclass[1:]:
#  if (len(dcenter[iclass]) ==  0.0):
#    continue
#  #-----------
#  for latlon in dcenter[iclass]:
#    lat = latlon[0]
#    lon = latlon[1]
#    M.scatter( lon, lat, color="r", marker="o", s=100)
#    x_plot, y_plot = M(lon, lat+0.5)
#    plt.text(x_plot, y_plot, "%d"%(iclass), color="r", fontsize=15)

#-- coastline ---------------
print "coastlines"
M.drawcoastlines()

#-- meridians and parallels
M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1]) 
M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0]) 
#-- title -------------------
stitle   = "wind %d hPa"%(plev*0.01)
stitle   = stitle + "\n" +"%04d-%02d-%02d  UTC %02d:00 (JST %02d:00)"%(year, mon, day, hour, hour+9)
axmap.set_title("%s"%(stitle))

#-- save --------------------
print "save"
plt.savefig(soname)
plt.clf()
print soname
#-------------------

# for colorbar ---
if cbarflag == "True":
  figmap   = plt.figure()
  axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
  M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
  a2v_trans    = M.transform_scalar( a2v,   a1lon, a1lat, nnx, nny) 
  im       = M.imshow(a2v_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm)

  figcbar   = plt.figure(figsize=(5, 0.6))
  axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
  bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
  plt.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar, orientation="horizontal")
  #plt.colorbar(im, boundaries= bnd_cbar, extend="max", cax=axcbar, orientation="horizontal")

  cbarname  = sodir[:-3] + "/cbar.%s.png"%("wind")
  figcbar.savefig(cbarname)
  
#***************************************
      
      
