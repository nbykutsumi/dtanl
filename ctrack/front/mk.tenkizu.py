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
#vtype   = "GSMaP"
#vtype   = "GPCP1DD"
#lvtype   = ["JRA"]
lvtype   = ["GSMaP", "JRA"]
#lvtype   = ["GSMaP","JRA"]

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
else:
  year   = 2004
  mon    = 9
  day    = 29
  hour   = 0
  #plev    = 850*100   #(Pa)
  plev    = 925*100   #(Pa)
  cbarflag = "True"
  thdura  = 6
  # local region ------
  # corner points should be
  # at the center of original grid box
  lllat   = 20.
  urlat   = 60.
  lllon   = 110.
  urlon   = 160.


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

for vtype in lvtype:
  ny      = 180
  nx      = 360
  miss_int= -9999
  stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)
  sodir_root    = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/%02dh"%(thdura)
  #sodir         = sodir_root + "/%04d%02d"%(year, mon)
  sodir         = "/home/utsumi/temp"
  ctrack_func.mk_dir(sodir)
  
  soname        = sodir + "/tenkizu.%04d.%02d.%02d.%02d.%s.png"%(year, mon, day, hour, vtype)
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
  if vtype == "GSMaP":
    lhour_inc     = [-3, 0, 3, 6]
    for hour_inc in lhour_inc:
      (year_t, mon_t, day_t, hour_t) = shifttime(year, mon, day, hour, hour_inc)
      print day, year_t, mon_t, day_t, hour_t
      vdir_root  = "/media/disk2/data/GSMaP/sa.one/3hr/ptot"
      vdir       = vdir_root + "/%04d%02d"%(year_t, mon_t)
      vname      = vdir + "/gsmap_mvk.3rh.%04d%02d%02d.%02d00.v5.222.1.sa.one"%(year_t, mon_t, day_t, hour_t)
      a2v_t      = fromfile(vname, float32).reshape(120, 360)
      a2v_t      = gsmap_func.gsmap2global_one(a2v_t, -9999.0)
      a2num_t    = ma.masked_where(a2v_t ==-9999.0, a2one).filled(0.0)
      a2num      = a2num + a2num_t
      a2v        = a2v + ma.masked_equal(a2v_t, -9999.0)
    #--
    #a2v        = ma.masked_where(a2num < len(lhour_inc), a2v)/a2num
    a2v        = a2v / len(lhour_inc)
    a2v        = a2v*60*60*24.0
    a2v        = a2v.filled(-9999.0)
    a2mask     = a2v
  
  
    if day == 22:
      array(a2v,float32).tofile("./temp.sa.one")
      array(a2num, float32).tofile("./num.sa.one")
  
  if vtype == "GPCP1DD":
    vdir_root     = "/media/disk2/data/GPCP1DD/data/1dd"
    vdir          = vdir_root + "/%04d"%(year)
    vname         = vdir + "/gpcp_1dd_v1.1_p1d.%04d%02d%02d.bn"%(year, mon, day)
    a2v           = fromfile(vname, float32).reshape(ny, nx)
    a2v           = flipud(a2v)
  
  if vtype == "JRA":
    lhour_inc     = [0,6]
    for hour_inc in lhour_inc:
      (year_t, mon_t, day_t, hour_t) = shifttime(year, mon, day, hour, hour_inc)
      print day, year_t, mon_t, day_t, hour_t
  
      vdir_root     = "/media/disk2/data/JRA25/sa.one/6hr/PR"
      vdir          = vdir_root + "/%04d%02d"%(year_t, mon_t)
      vname         = vdir + "/fcst_phy2m.PR.%04d%02d%02d%02d.sa.one"%(year_t, mon_t, day_t, hour_t)
      a2v_t         = fromfile(vname, float32).reshape(ny, nx)
      a2v           = a2v + a2v_t
    #--
    a2v           = a2v / len(lhour_inc)
    a2v           = a2v * 60*60*24.0
  
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
  if vtype in ["GSMaP"]:
    a2v_trans    = M.transform_scalar( ma.masked_equal(a2v, -9999.0),   a1lon, a1lat, nnx, nny).data
    a2mask_trans = M.transform_scalar( ma.masked_equal(a2mask, -9999.0), a1lon, a1lat, nnx, nny).data
  
  else:
    a2v_trans    = M.transform_scalar( a2v,   a1lon, a1lat, nnx, nny) 
  #--- 
  a2psl_trans  = M.transform_scalar( a2psl, a1lon, a1lat, nnx, nny)
  #
  
  #-- boundaries ----------
  if vtype in ["GSMaP", "GPCP1DD", "JRA"]:
    #bnd        = [1,3,5,7,9,11,13,15,17]
    bnd        = [1,5,10,15,20,25,30,35,40,45,50,55,60]
    bnd_cbar   = [-1.0e+40] + bnd + [1.0e+40]
  
  #-- color ---------------
  #scm      = "gist_stern_r"
  #scm      = "gist_ncar_r"
  #scm      = "jet"
  #scm      = "rainbow"
  scm      = "Spectral_r"
  #scm      = "gist_rainbow"
  cminst   = matplotlib.cm.get_cmap(scm, len(bnd))
  acm      = cminst( arange( len(bnd) ) )
  lcm      = [[1,1,1,1]]+ acm.tolist()
  mycm      = matplotlib.colors.ListedColormap( lcm )
  #-- value imshow --------
  im       = M.imshow(a2v_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")
  
  #-- superimpose shape (mask) ---
  if vtype in ["GSMaP"]:
    cmshade  = matplotlib.colors.ListedColormap([(0.8, 0.8, 0.8), (0.8, 0.8, 0.8)])
    a2shade  = ma.masked_where(a2mask_trans != -9999.0, a2mask_trans)
    im       = M.imshow(a2shade, origin="lower", cmap=cmshade, interpolation="nearest")
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
  #-- title -------------------
  stitle   = "%s"%(vtype)
  stitle   = stitle + "\n" +"%04d-%02d-%02d  UTC %02d:00 (JST %02d:00)"%(year, mon, day, hour, hour+9)
  axmap.set_title("%s"%(stitle))
  
  #-- save --------------------
  print "save"
  plt.savefig(soname)
  plt.clf()
  print soname
  #-------------------
  
  # for colorbar ---
  if cbarflag == True:
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
  
    cbarname  = sodir + "/cbar.%s.png"%(vtype)
    figcbar.savefig(cbarname)
  

