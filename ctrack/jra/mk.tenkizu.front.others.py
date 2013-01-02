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
else:
  singletime = True
  year   = 2004
  mon    = 1
  day    = 5
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

#-----------------------------------------

miss_int= -9999



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

sodir_root    = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/%02dh"%(thdura)
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

#**************************************************************
# equivalent potential temperature
#**************************************************************
tname = "/media/disk2/data/JRA25/sa.one/6hr/TMP/%04d%02d/anal_p25.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
qname = "/media/disk2/data/JRA25/sa.one/6hr/SPFH/%04d%02d/anal_p25.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
a2t    = fromfile(tname, float32).reshape(180,360)
a2q    = fromfile(qname, float32).reshape(180,360)
a2thermo   = dtanl_fsub.mk_a2theta_e(plev, a2t.T, a2q.T).T

soname = sodir + "/tenkizu.thetae.%04d.%02d.%02d.%02d.%04dhPa.png"%(year, mon, day, hour, plev*0.01)
#------------------------
# Basemap
#------------------------
print "Basemap"
figmap   = plt.figure()
axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)

#-- transform -----------
print "transform"
a2thermo_trans    = M.transform_scalar( a2thermo, a1lon, a1lat, nnx, nny) 
#--- 
a2psl_trans  = M.transform_scalar( a2psl, a1lon, a1lat, nnx, nny)
#

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

#-- contour theta_e -----
llevels  = arange(200,400,2)
im       = M.contour(LONS, LATS, a2thermo_trans, latlon=True, levels=llevels, colors="r")
plt.clabel(im, fontsize=9, inline=1, fmt="%d")

#-- contour   -----------
print "contour"
llevels  = arange(900.0, 1100.0, 4.0).tolist()
im       = M.contour(LONS, LATS, a2psl_trans, latlon=True, levels=llevels,  colors="gray")
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
#-- title -------------------
stitle   = "equivalent-potential-temperature [K] at %dhPa"%(plev*0.01)
stitle   = stitle + "\n" +"%04d-%02d-%02d  UTC %02d:00 (JST %02d:00)"%(year, mon, day, hour, hour+9)
axmap.set_title("%s"%(stitle))

#-- save --------------------
print "save"
plt.savefig(soname)
plt.clf()
print soname
##-------------------
## for colorbar ---
#if cbarflag == "True":
#  figmap   = plt.figure()
#  axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
#  M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
#  a2v_trans    = M.transform_scalar( a2wb,   a1lon, a1lat, nnx, nny) 
#  im       = M.imshow(a2v_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm)
#
#  figcbar   = plt.figure(figsize=(5, 0.6))
#  axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
#  bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
#  plt.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar, orientation="horizontal")
#  #plt.colorbar(im, boundaries= bnd_cbar, extend="max", cax=axcbar, orientation="horizontal")
#
#  cbarname  = sodir[:-3] + "/cbar.%s.png"%("wb")
#  figcbar.savefig(cbarname)
#  print cbarname 

###**************************************************************
### thermovariable advection locator :GAtau # from McCann and Whistler 2001
###**************************************************************
#tname = "/media/disk2/data/JRA25/sa.one/6hr/TMP/%04d%02d/anal_p25.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
#qname = "/media/disk2/data/JRA25/sa.one/6hr/SPFH/%04d%02d/anal_p25.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
#uname = "/media/disk2/data/JRA25/sa.one/6hr/UGRD/%04d%02d/anal_p25.UGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
#vname = "/media/disk2/data/JRA25/sa.one/6hr/VGRD/%04d%02d/anal_p25.VGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
#
#a2t    = fromfile(tname, float32).reshape(180,360)
#a2q    = fromfile(qname, float32).reshape(180,360)
#a2uwind= fromfile(uname, float32).reshape(180,360)
#a2vwind= fromfile(vname, float32).reshape(180,360)
#a2thermo   = dtanl_fsub.mk_a2theta_e(plev, a2t.T, a2q.T).T
#a2thermoadv= dtanl_fsub.mk_a2thermoadv(a2thermo.T, a2uwind.T, a2vwind.T).T
#soname = sodir + "/tenkizu.thermoadv.%04d.%02d.%02d.%02d.%04dhPa.png"%(year, mon, day, hour, plev*0.01)
##------------------------
## Basemap
##------------------------
#print "Basemap"
#figmap   = plt.figure()
#axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
#M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
#
##-- transform -----------
#print "transform"
#a2thermoadv_trans    = M.transform_scalar( a2thermoadv, a1lon, a1lat, nnx, nny) 
##--- 
#a2psl_trans  = M.transform_scalar( a2psl, a1lon, a1lat, nnx, nny)
##
#
##-- boundaries ----------
##bnd        = list(arange(230,300+1,3))
##bnd_cbar   = [-1.0e+40] + bnd + [1.0e+40]
#
##-- color ---------------
##scm      = "rainbow"
#scm      = "Spectral_r"
##scm      = "gist_rainbow"
##scm      = "OrRd"
##cminst   = matplotlib.cm.get_cmap(scm, len(bnd))
##acm      = cminst( arange( len(bnd) ) )
##lcm      = [[1,1,1,1]]+ acm.tolist()
##mycm      = matplotlib.colors.ListedColormap( lcm )
#
#mycm  = scm
##-- imshow    -----------
##im       = M.imshow(a2thermoadv_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")
#im       = M.imshow(a2thermoadv_trans, origin="lower",  cmap=mycm, interpolation="nearest", vmin=0.0)
#plt.colorbar(im)
##-- contour   -----------
#print "contour"
#llevels  = arange(900.0, 1100.0, 4.0).tolist()
#im       = M.contour(LONS, LATS, a2psl_trans, latlon=True, levels=llevels,  colors="gray")
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
#
##-- coastline ---------------
#print "coastlines"
#M.drawcoastlines()
#
##-- meridians and parallels
#M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1]) 
#M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0]) 
##-- title -------------------
#stitle   = "thermo-advection locator at %dhPa"%(plev*0.01)
#stitle   = stitle + "\n" +"%04d-%02d-%02d  UTC %02d:00 (JST %02d:00)"%(year, mon, day, hour, hour+9)
#axmap.set_title("%s"%(stitle))
#
##-- save --------------------
#print "save"
#plt.savefig(soname)
#plt.clf()
#print soname
###-------------------
### for colorbar ---
##if cbarflag == "True":
##  figmap   = plt.figure()
##  axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
##  M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
##  a2v_trans    = M.transform_scalar( a2wb,   a1lon, a1lat, nnx, nny) 
##  im       = M.imshow(a2v_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm)
##
##  figcbar   = plt.figure(figsize=(5, 0.6))
##  axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
##  bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
##  plt.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar, orientation="horizontal")
##  #plt.colorbar(im, boundaries= bnd_cbar, extend="max", cax=axcbar, orientation="horizontal")
##
##  cbarname  = sodir[:-3] + "/cbar.%s.png"%("wb")
##  figcbar.savefig(cbarname)
##  print cbarname 
#




##**************************************************************
## mixing ratio
##**************************************************************
#qname = "/media/disk2/data/JRA25/sa.one/6hr/SPFH/%04d%02d/anal_p25.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
#a2q    = fromfile(qname, float32).reshape(180,360)
#a2q    = a2q * 1000.0  # kg/kg --> g/kg
#soname = sodir + "/tenkizu.q.%04d.%02d.%02d.%02d.%04dhPa.png"%(year, mon, day, hour, plev*0.01)
##------------------------
## Basemap
##------------------------
#print "Basemap"
#figmap   = plt.figure()
#axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
#M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
#
##-- transform -----------
#print "transform"
#a2q_trans    = M.transform_scalar( a2q,   a1lon, a1lat, nnx, nny) 
##--- 
#a2psl_trans  = M.transform_scalar( a2psl, a1lon, a1lat, nnx, nny)
##
#
##-- boundaries ----------
##bnd        = [220,225,230,235,240,245,250,255,260,265,270,275,280,285,290,295,300,305,310]
##bnd        = list(arange(230,300+1,3))
#bnd        = list(arange(0.1,20.0+1,1.0))
#bnd_cbar   = [-1.0e+40] + bnd + [1.0e+40]
#
##-- color ---------------
#scm      = "rainbow"
##scm      = "Spectral_r"
##scm      = "Spectral"
##scm      = "spectral_r"
##scm      = "Blues"
##scm      = "gist_rainbow"
##scm      = "OrRd"
#cminst   = matplotlib.cm.get_cmap(scm, len(bnd))
#acm      = cminst( arange( len(bnd) ) )
#lcm      = [[1,1,1,1]]+ acm.tolist()
#mycm      = matplotlib.colors.ListedColormap( lcm )
#
###-- imshow  q  -----------
#im       = M.imshow(a2q_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")
#
####-- contour q  -----------
##print "contour"
##llevels  = arange(0.0, 100.0, 1.0).tolist()
##im       = M.contour(LONS, LATS, a2q_trans, latlon=True, levels=llevels,  colors="k")
##plt.clabel(im, fontsize=9, inline=1, fmt="%d")
#
###-- contour PSL ----------
##print "contour"
##llevels  = arange(900.0, 1100.0, 2.0).tolist()
##im       = M.contour(LONS, LATS, a2psl_trans, latlon=True, levels=llevels,  colors="gray")
##plt.clabel(im, fontsize=9, inline=1, fmt="%d")
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
#
##-- coastline ---------------
#print "coastlines"
#M.drawcoastlines()
#
##-- meridians and parallels
#M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1]) 
#M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0]) 
##-- title -------------------
#stitle   = "Mixing ratio (g/kg)"
#stitle   = stitle + "\n" +"%04d-%02d-%02d  UTC %02d:00 (JST %02d:00)"%(year, mon, day, hour, hour+9)
#axmap.set_title("%s"%(stitle))
#
##-- save --------------------
#print "save"
#plt.savefig(soname)
#plt.clf()
#print soname
##-------------------
## for colorbar ---
#if cbarflag == "True":
#  figmap   = plt.figure()
#  axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
#  M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
#  a2v_trans    = M.transform_scalar( a2q,   a1lon, a1lat, nnx, nny) 
#  im       = M.imshow(a2v_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm)
#
#  figcbar   = plt.figure(figsize=(5, 0.6))
#  axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
#  bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
#  plt.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar, orientation="horizontal")
#  #plt.colorbar(im, boundaries= bnd_cbar, extend="max", cax=axcbar, orientation="horizontal")
#
#  cbarname  = sodir[:-3] + "/cbar.%s.png"%("t.q")
#  figcbar.savefig(cbarname)
#  print cbarname 


##**************************************************************
## geopotential height at 500 hPa & 250 hPa
##**************************************************************
#gzname500 = "/media/disk2/data/JRA25/sa.one/6hr/HGT/%04d%02d/anal_p25.HGT.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, 500, year, mon, day, hour)
#gzname250 = "/media/disk2/data/JRA25/sa.one/6hr/HGT/%04d%02d/anal_p25.HGT.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, 250, year, mon, day, hour)
#a2gz500   = fromfile(gzname500, float32).reshape(180,360)
#a2gz250   = fromfile(gzname250, float32).reshape(180,360)
#
##soname = sodir + "/tenkizu.gz.%04d.%02d.%02d.%02d.%04dhPa.png"%(year, mon, day, hour, plev_temp*0.01)
#soname = sodir + "/tenkizu.gz.%04d.%02d.%02d.%02d.upper.png"%(year, mon, day, hour)
##------------------------
## Basemap
##------------------------
#print "Basemap"
#figmap   = plt.figure()
#axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
#M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
#
##-- transform -----------
#print "transform"
#a2gz500_trans  = M.transform_scalar( a2gz500, a1lon, a1lat, nnx, nny)
#a2gz250_trans  = M.transform_scalar( a2gz250, a1lon, a1lat, nnx, nny)
##
#
##-- boundaries ----------
#bnd        = [250,255,260,265,270,275,280,285,290,295,300,305,310]
#bnd        = list(arange(260,300+1,3))
#bnd_cbar   = [-1.0e+40] + bnd + [1.0e+40]
#
##-- color ---------------
##scm      = "rainbow"
#scm      = "Spectral_r"
##scm      = "gist_rainbow"
##scm      = "OrRd"
#cminst   = matplotlib.cm.get_cmap(scm, len(bnd))
#acm      = cminst( arange( len(bnd) ) )
#lcm      = [[1,1,1,1]]+ acm.tolist()
#mycm      = matplotlib.colors.ListedColormap( lcm )
#
###-- imshow    -----------
##im       = M.imshow(a2gz_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")
#
##-- contour   -----------
#print "contour"
##llevels  = arange(0.0, 1100.0, 2.0).tolist()
#llevels  = arange(3000.0, 15000.0, 60.0).tolist()
#im       = M.contour(LONS, LATS, a2gz500_trans, latlon=True, levels=llevels,  colors="k")
#plt.clabel(im, fontsize=9, inline=1, fmt="%d")
#im       = M.contour(LONS, LATS, a2gz250_trans, latlon=True, levels=llevels,  linestyles="dashed", colors="b")
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
#
##-- coastline ---------------
#print "coastlines"
#M.drawcoastlines()
#
##-- meridians and parallels
#M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1]) 
#M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0]) 
##-- title -------------------
#stitle   = "geopotential height %d hPa & %dhPa"%(500,250)
#stitle   = stitle + "\n" +"%04d-%02d-%02d  UTC %02d:00 (JST %02d:00)"%(year, mon, day, hour, hour+9)
#axmap.set_title("%s"%(stitle))
#
##-- save --------------------
#print "save"
#plt.savefig(soname)
#plt.clf()
#print soname
##-------------------

## for colorbar ---
#if cbarflag == True:
#  figmap   = plt.figure()
#  axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
#  M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
#  a2v_trans    = M.transform_scalar( a2wb,   a1lon, a1lat, nnx, nny) 
#  im       = M.imshow(a2v_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm)
#
#  figcbar   = plt.figure(figsize=(5, 0.6))
#  axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
#  bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
#  plt.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar, orientation="horizontal")
#  #plt.colorbar(im, boundaries= bnd_cbar, extend="max", cax=axcbar, orientation="horizontal")
#
#  cbarname  = sodir[:-3] + "/cbar.%s.png"%("gz")
#  figcbar.savefig(cbarname)
  

##**************************************************************
## temperature and mixing ratio and wind
##**************************************************************
#tname = "/media/disk2/data/JRA25/sa.one/6hr/TMP/%04d%02d/anal_p25.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
#qname = "/media/disk2/data/JRA25/sa.one/6hr/SPFH/%04d%02d/anal_p25.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
#uname = "/media/disk2/data/JRA25/sa.one/6hr/UGRD/%04d%02d/anal_p25.UGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
#vname = "/media/disk2/data/JRA25/sa.one/6hr/VGRD/%04d%02d/anal_p25.VGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
#a2t    = fromfile(tname, float32).reshape(180,360)
#a2q    = fromfile(qname, float32).reshape(180,360)
#a2q    = a2q * 1000.0  # kg/kg --> g/kg
#a2u    = fromfile(uname, float32).reshape(180,360)
#a2v    = fromfile(vname, float32).reshape(180,360)
#
#soname = sodir + "/tenkizu.t.q.%04d.%02d.%02d.%02d.%04dhPa.png"%(year, mon, day, hour, plev*0.01)
##------------------------
## Basemap
##------------------------
#print "Basemap"
#figmap   = plt.figure()
#axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
#M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
#
##-- transform -----------
#print "transform"
#a2t_trans    = M.transform_scalar( a2t,   a1lon, a1lat, nnx, nny) 
#a2q_trans    = M.transform_scalar( a2q,   a1lon, a1lat, nnx, nny) 
#a2u_trans    = M.transform_scalar( a2u,   a1lon, a1lat, nnx, nny) 
#a2v_trans    = M.transform_scalar( a2v,   a1lon, a1lat, nnx, nny) 
##--- 
#a2psl_trans  = M.transform_scalar( a2psl, a1lon, a1lat, nnx, nny)
##
#
##-- boundaries ----------
##bnd        = [220,225,230,235,240,245,250,255,260,265,270,275,280,285,290,295,300,305,310]
##bnd        = list(arange(230,300+1,3))
#bnd        = list(arange(0.1,20.0+1,2.0))
#bnd_cbar   = [-1.0e+40] + bnd + [1.0e+40]
#
##-- color ---------------
#scm      = "rainbow_r"
##scm      = "Spectral_r"
##scm      = "Spectral"
##scm      = "spectral_r"
##scm      = "Blues"
##scm      = "gist_rainbow"
##scm      = "OrRd"
#cminst   = matplotlib.cm.get_cmap(scm, len(bnd))
#acm      = cminst( arange( len(bnd) ) )
#lcm      = [[1,1,1,1]]+ acm.tolist()
#mycm      = matplotlib.colors.ListedColormap( lcm )
#
##-- vector wind ----------
#im       = M.quiver(LONS, LATS, a2u_trans, a2v_trans, angles="xy", color="k")
#
##-- imshow  q  -----------
#im       = M.imshow(a2q_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")
#
###-- contour T -----
##llevels  = arange(200,400,1)
##im       = M.contour(LONS, LATS, a2t_trans, latlon=True, levels=llevels, colors="k", linewidth=20)
##plt.clabel(im, fontsize=9, inline=1, fmt="%d")
#
###-- contour   -----------
##print "contour"
##llevels  = arange(900.0, 1100.0, 2.0).tolist()
##im       = M.contour(LONS, LATS, a2psl_trans, latlon=True, levels=llevels,  colors="gray")
##plt.clabel(im, fontsize=9, inline=1, fmt="%d")
##
###-- plot cyclone centers ---
##print "plot cyclone centers"
##for iclass in lclass[1:]:
##  if (len(dcenter[iclass]) ==  0.0):
##    continue
##  #-----------
##  for latlon in dcenter[iclass]:
##    lat = latlon[0]
##    lon = latlon[1]
##    M.scatter( lon, lat, color="r", marker="o", s=100)
##    x_plot, y_plot = M(lon, lat+0.5)
##    plt.text(x_plot, y_plot, "%d"%(iclass), color="r", fontsize=15)
#
##-- coastline ---------------
#print "coastlines"
#M.drawcoastlines()
#
##-- meridians and parallels
#M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1]) 
#M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0]) 
##-- title -------------------
#stitle   = "Temperature (contour) & Mixing ration (color)"
#stitle   = stitle + "\n" +"%04d-%02d-%02d  UTC %02d:00 (JST %02d:00)"%(year, mon, day, hour, hour+9)
#axmap.set_title("%s"%(stitle))
#
##-- save --------------------
#print "save"
#plt.savefig(soname)
#plt.clf()
#print soname
##-------------------
## for colorbar ---
#if cbarflag == "True":
#  figmap   = plt.figure()
#  axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
#  M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
#  a2v_trans    = M.transform_scalar( a2q,   a1lon, a1lat, nnx, nny) 
#  im       = M.imshow(a2v_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm)
#
#  figcbar   = plt.figure(figsize=(5, 0.6))
#  axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
#  bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
#  plt.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar, orientation="horizontal")
#  #plt.colorbar(im, boundaries= bnd_cbar, extend="max", cax=axcbar, orientation="horizontal")
#
#  cbarname  = sodir[:-3] + "/cbar.%s.png"%("t.q")
#  figcbar.savefig(cbarname)
#  print cbarname 

##**************************************************************
## relative humidity
##**************************************************************
#tname = "/media/disk2/data/JRA25/sa.one/6hr/TMP/%04d%02d/anal_p25.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
#qname = "/media/disk2/data/JRA25/sa.one/6hr/SPFH/%04d%02d/anal_p25.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
#a2t    = fromfile(tname, float32).reshape(180,360)
#a2q    = fromfile(qname, float32).reshape(180,360)
#a2rh   = dtanl_fsub.mk_a2rh(a2t.T, a2q.T, plev).T
#soname = sodir + "/tenkizu.rh.%04d.%02d.%02d.%02d.%04dhPa.png"%(year, mon, day, hour, plev*0.01)
##------------------------
## Basemap
##------------------------
#print "Basemap"
#figmap   = plt.figure()
#axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
#M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
#
##-- transform -----------
#print "transform"
#a2rh_trans    = M.transform_scalar( a2rh,   a1lon, a1lat, nnx, nny) 
##--- 
#a2psl_trans  = M.transform_scalar( a2psl, a1lon, a1lat, nnx, nny)
##
#
##-- boundaries ----------
#bnd        = list(arange(0,100.0+1,10))
#bnd_cbar   = bnd
#
##-- color ---------------
##scm      = "rainbow"
#scm      = "Spectral"
##scm      = "gist_rainbow"
##scm      = "OrRd"
##cminst   = matplotlib.cm.get_cmap(scm, len(bnd))
##acm      = cminst( arange( len(bnd) ) )
##lcm      = [[1,1,1,1]]+ acm.tolist()
##mycm      = matplotlib.colors.ListedColormap( lcm )
#mycm      = scm
#
##-- imshow    -----------
#im       = M.imshow(a2rh_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")
#
##-- contour   -----------
#print "contour"
#llevels  = arange(900.0, 1100.0, 4.0).tolist()
#im       = M.contour(LONS, LATS, a2psl_trans, latlon=True, levels=llevels,  colors="gray")
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
#
##-- coastline ---------------
#print "coastlines"
#M.drawcoastlines()
#
##-- meridians and parallels
#M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1]) 
#M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0]) 
##-- title -------------------
#stitle   = "relative humidity (%)"
#stitle   = stitle + "\n" +"%04d-%02d-%02d  UTC %02d:00 (JST %02d:00)"%(year, mon, day, hour, hour+9)
#axmap.set_title("%s"%(stitle))
#
##-- save --------------------
#print "save"
#plt.savefig(soname)
#plt.clf()
#print soname
###-------------------
## for colorbar ---
#if cbarflag == "True":
#  figmap   = plt.figure()
#  axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
#  M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
#  a2v_trans    = M.transform_scalar( a2rh,   a1lon, a1lat, nnx, nny) 
#  im       = M.imshow(a2v_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm)
#
#  figcbar   = plt.figure(figsize=(5, 0.6))
#  axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
#  bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
#  #plt.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar, orientation="horizontal")
#  plt.colorbar(im, boundaries= bnd_cbar, cax=axcbar, orientation="horizontal")
#
#  cbarname  = sodir[:-3] + "/cbar.%s.png"%("rh")
#  figcbar.savefig(cbarname)
#  print cbarname 


