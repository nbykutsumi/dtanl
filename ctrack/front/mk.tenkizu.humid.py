from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib
from numpy import *
import calendar
import ctrack_para
import ctrack_func
from dtanl_fsub import *
import sys, os
import gsmap_func
from cf.plot import *
import datetime
#--------------------------------------
if len(sys.argv) >1:
  year  = int(sys.argv[1])
  mon   = int(sys.argv[2])
  day   = int(sys.argv[3])
  hour  = int(sys.argv[4])
  lllat = float(sys.argv[5])
  urlat = float(sys.argv[6])
  lllon = float(sys.argv[7])
  urlon = float(sys.argv[8])
  plev = float(sys.argv[9])   #[Pa]
  cbarflag = sys.argv[10]
  thdura= float(sys.argv[11])
  singletime = True
  sresol     = sys.argv[12]
else:
  singletime = True
  year   = 2004
  mon    = 7
  day    = 13
  hour   = 0
  #plev    = 500*100   #(Pa)
  plev    = 850*100   #(Pa)
  cbarflag = "True"
  thdura  = 6
  # local region ------
  # corner points should be
  # at the center of original grid box
  #lllat   = 20.
  #urlat   = 60.
  #lllon   = 110.
  #urlon   = 160.

  lllat   = 0.0
  urlat   = 80.0
  lllon   = 60.0
  urlon   = 190.0
  sresol  = "anl_p"
#-----------------------------------------

miss_int= -9999

#**********************************************
def mk_a2contour(a2in, llevels="",soname="./temp.png",lllat=-89.5,lllon=0.5,urlat=89.5,urlon=359.5):
soname  = soname_qday
lllon_tmp  = lllon
lllat_tmp  = lllat
urlon_tmp  = urlon
urlat_tmp  = urlat

#------------
# for mapping
nnx        = int( (urlon_tmp - lllon_tmp)/dlon)
nny        = int( (urlat_tmp - lllat_tmp)/dlat)
a1lon_loc  = linspace(lllon_tmp, urlon_tmp, nnx)
a1lat_loc  = linspace(lllat_tmp, urlat_tmp, nny)
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
a2thermo_trans    = M.transform_scalar( a2qday, a1lon, a1lat, nnx, nny) 

#-- boundaries ----------
bnd        = list(arange(230,300+1,3))
bnd_cbar   = [-1.0e+40] + bnd + [1.0e+40]

#-- color ---------------
#scm      = "rainbow"
scm      = "Spectral_r"
#scm      = "gist_rainbow"
#scm      = "OrRd"
cminst   = matplotlib.cm.get_cmap(scm, len(bnd))
acm      = cminst( arange( len(bnd) ) )
lcm      = [[1,1,1,1]]+ acm.tolist()
mycm      = matplotlib.colors.ListedColormap( lcm )

#-- imshow    -----------
#im       = M.imshow(a2thermo_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")

#-- contour thermo -----
llevels  = arange(200,400,2)
#im       = M.contour(LONS, LATS, a2thermo_trans, latlon=True, levels=llevels, colors="r")
im       = M.contour(LONS, LATS, a2thermo_trans, latlon=True, colors="r")
plt.clabel(im, fontsize=9, inline=1, fmt="%d")

#-- coastline ---------------
print "coastlines"
M.drawcoastlines()

#-- meridians and parallels
M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1]) 
M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0]) 
#-- title -------------------
stitle   = "mixing ratio @%d hPa"%(plev*0.01)
stitle   = stitle + "\n" +"%04d-%02d-%02d  UTC %02d:00 (JST %02d:00)"%(year, mon, day, hour, hour+9)
axmap.set_title("%s"%(stitle))

#-- save --------------------
print "save"
plt.savefig(soname)
plt.clf()
print soname

#**************************************************************
# draw:  grad qday 
#------------------------
soname  = soname_gradqday

#lllon_tmp  = lllon
#lllat_tmp  = lllat
#urlon_tmp  = urlon
#urlat_tmp  = urlat

lllon_tmp  = 0.5
lllat_tmp  = -89.5
urlon_tmp  = 359.5
urlat_tmp  = 89.5

#------------
# for mapping
nnx        = int( (urlon_tmp - lllon_tmp)/dlon)
nny        = int( (urlat_tmp - lllat_tmp)/dlat)
a1lon_loc  = linspace(lllon_tmp, urlon_tmp, nnx)
a1lat_loc  = linspace(lllat_tmp, urlat_tmp, nny)
LONS, LATS = meshgrid( a1lon_loc, a1lat_loc)


#------------------------
# Basemap
#------------------------
print "Basemap"
figmap   = plt.figure()
axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
M        = Basemap( resolution="l", llcrnrlat=lllat_tmp, llcrnrlon=lllon_tmp, urcrnrlat=urlat_tmp, urcrnrlon=urlon_tmp, ax=axmap)

#-- transform -----------
print "transform"
a2thermo_trans    = M.transform_scalar( a2gradqday, a1lon, a1lat, nnx, nny) 

#-- boundaries ----------
bnd        = list(arange(230,300+1,3))
bnd_cbar   = [-1.0e+40] + bnd + [1.0e+40]

#-- color ---------------
#scm      = "rainbow"
scm      = "Spectral_r"
#scm      = "gist_rainbow"
#scm      = "OrRd"
cminst   = matplotlib.cm.get_cmap(scm, len(bnd))
acm      = cminst( arange( len(bnd) ) )
lcm      = [[1,1,1,1]]+ acm.tolist()
mycm      = matplotlib.colors.ListedColormap( lcm )

#-- imshow    -----------
#im       = M.imshow(a2thermo_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")

#-- contour thermo -----
llevels  = arange(200,400,2)
#im       = M.contour(LONS, LATS, a2thermo_trans, latlon=True, levels=llevels, colors="r")
im       = M.contour(LONS, LATS, a2thermo_trans, latlon=True, colors="r")
plt.clabel(im, fontsize=9, inline=1, fmt="%d")

#-- coastline ---------------
print "coastlines"
M.drawcoastlines()

#-- meridians and parallels
M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1]) 
M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0]) 
#-- title -------------------
stitle   = "mixing ratio @%d hPa"%(plev*0.01)
stitle   = stitle + "\n" +"%04d-%02d-%02d  UTC %02d:00 (JST %02d:00)"%(year, mon, day, hour, hour+9)
axmap.set_title("%s"%(stitle))

#-- save --------------------
print "save"
plt.savefig(soname)
plt.clf()
print soname


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


stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)

sodir_root    = "/media/disk2/out/JRA25/sa.one.%s/6hr/tenkizu/%02dh"%(sresol, thdura)
sodir         = sodir_root + "/%04d%02d/front/%02d"%(year, mon, day)
ctrack_func.mk_dir(sodir)

#----------------------------
dlat    = 1.0
dlon    = 1.0
a1lat   = arange(-89.5, 89.5  + dlat*0.1, dlat)
a1lon   = arange(0.5,   359.5 + dlon*0.1, dlon)

meridians = 10.0
parallels = 10.0

#----------------------------
#----------------------------

#**************************************************************
# load data
#**************************************************************
tname = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP/%04d%02d/%s.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol, year, mon, sresol, plev*0.01, year, mon, day, hour)
qname = "/media/disk2/data/JRA25/sa.one.%s/6hr/SPFH/%04d%02d/%s.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol, year, mon, sresol, plev*0.01, year, mon, day, hour)
uname = "/media/disk2/data/JRA25/sa.one.anl_p25/6hr/UGRD/%04d%02d/anl_p25.UGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
vname = "/media/disk2/data/JRA25/sa.one.anl_p25/6hr/VGRD/%04d%02d/anl_p25.VGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)

a2t    = fromfile(tname, float32).reshape(180,360)
a2q    = fromfile(qname, float32).reshape(180,360)
#
a2u   =  fromfile(uname, float32).reshape(ny,nx)
a2v   =  fromfile(vname, float32).reshape(ny,nx)


soname_t = sodir + "/tenkizu.t.%04d.%02d.%02d.%02d.%04dhPa.png"%(year, mon, day, hour, plev*0.01)
soname_q = sodir + "/tenkizu.q.%04d.%02d.%02d.%02d.%04dhPa.png"%(year, mon, day, hour, plev*0.01)
soname_qday = sodir + "/tenkizu.qday.%04d.%02d.%02d.%02d.%04dhPa.png"%(year, mon, day, hour, plev*0.01)
soname_gradq = sodir + "/tenkizu.grad.q.%04d.%02d.%02d.%02d.%04dhPa.png"%(year, mon, day, hour, plev*0.01)
soname_gradqday = sodir + "/tenkizu.grad.qday.%04d.%02d.%02d.%02d.%04dhPa.png"%(year, mon, day, hour, plev*0.01)
#------------------------
# make daily q
#------------------------
now    = datetime.datetime(year,mon,day,hour)
a2qday = zeros([ny,nx],float32)
for dhour in [-6,0,6,12]:
  targettime = now + datetime.timedelta(hours=dhour)
  year_t   = targettime.year
  mon_t    = targettime.month
  day_t    = targettime.day
  hour_t   = targettime.hour
  qname_t  = "/media/disk2/data/JRA25/sa.one.%s/6hr/SPFH/%04d%02d/%s.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol, year_t, mon_t, sresol, plev*0.01, year_t, mon_t, day_t, hour_t)
  a2q_t    = fromfile(qname_t, float32).reshape(ny,nx)
  a2qday   = a2qday  + a2q_t
#
a2qday   = a2qday / 4.0


#------------------------
# make daily grad q
#------------------------
a2gradqday  = dtanl_fsub.mk_a2grad_abs_saone(a2qday.T).T

#------------------------
# make vort
#------------------------
a2vort = dtanl_fsub.mk_a2relative_vorticity(a2u.T, a2v.T).T

#------------------------
# make qconverge
#------------------------
a2qu   = a2u * a2q
a2qv   = a2v * a2q
a2convqv  = - dtanl_fsub.mk_a2divergence(a2qu.T, a2qv.T).T

#------------------------
# make q advection
#------------------------
a2advq  = dtanl_fsub.mk_a2thermoadv(a2q.T, a2u.T, a2v.T).T

#------------------------
# make q transport
#------------------------
a2transq  = (a2qu**2.0 + a2qv**2.0)**0.5


#**************************************************************
# draw: mixing ratio
#------------------------
soname  = soname_qday
lllon_tmp  = lllon
lllat_tmp  = lllat
urlon_tmp  = urlon
urlat_tmp  = urlat

#------------
# for mapping
nnx        = int( (urlon_tmp - lllon_tmp)/dlon)
nny        = int( (urlat_tmp - lllat_tmp)/dlat)
a1lon_loc  = linspace(lllon_tmp, urlon_tmp, nnx)
a1lat_loc  = linspace(lllat_tmp, urlat_tmp, nny)
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
a2thermo_trans    = M.transform_scalar( a2qday, a1lon, a1lat, nnx, nny) 

#-- boundaries ----------
bnd        = list(arange(230,300+1,3))
bnd_cbar   = [-1.0e+40] + bnd + [1.0e+40]

#-- color ---------------
#scm      = "rainbow"
scm      = "Spectral_r"
#scm      = "gist_rainbow"
#scm      = "OrRd"
cminst   = matplotlib.cm.get_cmap(scm, len(bnd))
acm      = cminst( arange( len(bnd) ) )
lcm      = [[1,1,1,1]]+ acm.tolist()
mycm      = matplotlib.colors.ListedColormap( lcm )

#-- imshow    -----------
#im       = M.imshow(a2thermo_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")

#-- contour thermo -----
llevels  = arange(200,400,2)
#im       = M.contour(LONS, LATS, a2thermo_trans, latlon=True, levels=llevels, colors="r")
im       = M.contour(LONS, LATS, a2thermo_trans, latlon=True, colors="r")
plt.clabel(im, fontsize=9, inline=1, fmt="%d")

#-- coastline ---------------
print "coastlines"
M.drawcoastlines()

#-- meridians and parallels
M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1]) 
M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0]) 
#-- title -------------------
stitle   = "mixing ratio @%d hPa"%(plev*0.01)
stitle   = stitle + "\n" +"%04d-%02d-%02d  UTC %02d:00 (JST %02d:00)"%(year, mon, day, hour, hour+9)
axmap.set_title("%s"%(stitle))

#-- save --------------------
print "save"
plt.savefig(soname)
plt.clf()
print soname

#**************************************************************
# draw:  grad qday 
#------------------------
soname  = soname_gradqday

#lllon_tmp  = lllon
#lllat_tmp  = lllat
#urlon_tmp  = urlon
#urlat_tmp  = urlat

lllon_tmp  = 0.5
lllat_tmp  = -89.5
urlon_tmp  = 359.5
urlat_tmp  = 89.5

#------------
# for mapping
nnx        = int( (urlon_tmp - lllon_tmp)/dlon)
nny        = int( (urlat_tmp - lllat_tmp)/dlat)
a1lon_loc  = linspace(lllon_tmp, urlon_tmp, nnx)
a1lat_loc  = linspace(lllat_tmp, urlat_tmp, nny)
LONS, LATS = meshgrid( a1lon_loc, a1lat_loc)


#------------------------
# Basemap
#------------------------
print "Basemap"
figmap   = plt.figure()
axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
M        = Basemap( resolution="l", llcrnrlat=lllat_tmp, llcrnrlon=lllon_tmp, urcrnrlat=urlat_tmp, urcrnrlon=urlon_tmp, ax=axmap)

#-- transform -----------
print "transform"
a2thermo_trans    = M.transform_scalar( a2gradqday, a1lon, a1lat, nnx, nny) 

#-- boundaries ----------
bnd        = list(arange(230,300+1,3))
bnd_cbar   = [-1.0e+40] + bnd + [1.0e+40]

#-- color ---------------
#scm      = "rainbow"
scm      = "Spectral_r"
#scm      = "gist_rainbow"
#scm      = "OrRd"
cminst   = matplotlib.cm.get_cmap(scm, len(bnd))
acm      = cminst( arange( len(bnd) ) )
lcm      = [[1,1,1,1]]+ acm.tolist()
mycm      = matplotlib.colors.ListedColormap( lcm )

#-- imshow    -----------
#im       = M.imshow(a2thermo_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")

#-- contour thermo -----
llevels  = arange(200,400,2)
#im       = M.contour(LONS, LATS, a2thermo_trans, latlon=True, levels=llevels, colors="r")
im       = M.contour(LONS, LATS, a2thermo_trans, latlon=True, colors="r")
plt.clabel(im, fontsize=9, inline=1, fmt="%d")

#-- coastline ---------------
print "coastlines"
M.drawcoastlines()

#-- meridians and parallels
M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1]) 
M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0]) 
#-- title -------------------
stitle   = "mixing ratio @%d hPa"%(plev*0.01)
stitle   = stitle + "\n" +"%04d-%02d-%02d  UTC %02d:00 (JST %02d:00)"%(year, mon, day, hour, hour+9)
axmap.set_title("%s"%(stitle))

#-- save --------------------
print "save"
plt.savefig(soname)
plt.clf()
print soname

