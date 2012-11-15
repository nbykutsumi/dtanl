from dtanl_fsub import *
from numpy import *
import ctrack_func
import ctrack_para
import matplotlib.pyplot as plt
import matplotlib
import sys,os
from cf.plot import *
#---------------------------
year  = 2004
mon   = 2
day   = 22
hour  = 12
#plev  = 850*100.0
#plev  = 925*100.0
#plev  = 500*100.0
#plev  = 300*100.0
#plev  = 400*100.0
#lplev = [925*100.0, 850*100.0, 700*100.0, 600*100.0, 500*100.0, 400*100.0, 300*100.0]
#lplev = [925*100.0, 850*100.0,  700*100, 500*100.0,300*100 ]
lplev = [925*100.0, 850*100.0,  700*100, 500*100.0]
#lplev = [925*100.0, 500*100 ]
lprtype = ["JRA"]
vtype = "wbgrad"
thdura= 24
tname = "/media/disk2/data/JRA25/sa.one/6hr/TMP/%04d%02d/anal_p25.TMP.0850hPa.%04d%02d%02d%02d.sa.one"%(year, mon, year, mon, day, hour)
qname = "/media/disk2/data/JRA25/sa.one/6hr/SPFH/%04d%02d/anal_p25.SPFH.0850hPa.%04d%02d%02d%02d.sa.one"%(year, mon, year, mon, day, hour)


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


#--- dummy --------
da2v = {}
#------------------
for plev in lplev:
  a2t    = fromfile(tname, float32).reshape(180,360)
  a2q    = fromfile(qname, float32).reshape(180,360)
  a2wb     = dtanl_fsub.mk_a2wetbulbtheta(plev, a2t.T, a2q.T).T
  a2gradwb = dtanl_fsub.mk_a2grad_abs_saone(a2wb.T).T
  
  cbarflag = True


  ny      = 180
  nx      = 360
  # local region ------
  #
  # corner points should be
  # at the center of original grid box
  lllat   = 20.
  urlat   = 60.
  lllon   = 110.
  urlon   = 160.

  miss_int= -9999


  stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)

  sodir_root    = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/%02dh"%(thdura)
  sodir         = sodir_root + "/%04d%02d"%(year, mon)
  ctrack_func.mk_dir(sodir)

  #soname        = sodir + "/tenkizu.%04d.%02d.%02d.%02d.%s.png"%(year, mon, day, hour, vtype)
  soname        = sodir + "/wbgrad.tenkizu.%04d.%02d.%02d.%02d.%04dhPa.%s.png"%(year, mon, day, hour, plev*0.01, vtype)

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
  if vtype == "wbgrad":
    a2v           = a2gradwb * 1000.0*100.0 # [K/100km]
  #
  da2v[plev] = a2v
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
  ##************************
  ## for mapping
  #nnx        = int( (urlon - lllon)/dlon)
  #nny        = int( (urlat - lllat)/dlat)
  #a1lon_loc  = linspace(lllon, urlon, nnx)
  #a1lat_loc  = linspace(lllat, urlat, nny)
  #LONS, LATS = meshgrid( a1lon_loc, a1lat_loc)
  ##------------------------
  ## Basemap
  ##------------------------
  #print "Basemap"
  #plt.clf()
  #figmap   = plt.figure()
  #axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
  #M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)

  ##-- transform -----------
  #print "transform"
  #a2psl_trans  = M.transform_scalar( a2psl, a1lon, a1lat, nnx, nny)
  #a2v_trans    = M.transform_scalar( a2v,   a1lon, a1lat, nnx, nny)

  ##-- boundaries ----------
  #bnd        = [0.5,1.0,1.3,1.6,1.9,2.1,2.4]
  #bnd_cbar   = [-1.0e+40] + bnd + [1.0e+40]
  ##-- color ---------------
  ##scm      = "gist_stern_r"
  ##scm      = "jet"
  #scm      = "Spectral_r"
  #cm_inst  = matplotlib.cm.get_cmap(scm, len(bnd)+1)
  #acm      = cm_inst( arange(len(bnd)+1) )
  #lcm      = acm.tolist()
  #mycm     = matplotlib.colors.ListedColormap( lcm )
  ##mycm     = "jet"
  ##-- value imshow --------
  #im       = M.imshow(a2v_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")
  ##im       = M.imshow(a2v_trans, origin="lower", cmap=mycm, interpolation="nearest")

  ##-- contour   -----------
  #print "contour"
  #llevels  = arange(900.0, 1100.0, 2.0).tolist()
  #im       = M.contour(LONS, LATS, a2psl_trans, latlon=True, levels=llevels,  colors="k")
  #plt.clabel(im, fontsize=9, inline=1, fmt="%d")

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

  ##-- coastline ---------------
  #print "coastlines"
  #M.drawcoastlines()
  ##-- meridians and parallels
  #M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1])
  #M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0])
  ##-- title -------------------
  #axmap.set_title("%04d-%02d-%02d  JST %02d:00 %04dhPa"%(year, mon, day, hour, plev*0.01))

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
  #  a2v_trans    = M.transform_scalar( a2v,   a1lon, a1lat, nnx, nny)
  #  im       = M.imshow(a2v_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm)
  #  #im       = M.imshow(a2v_trans, origin="lower", cmap=mycm)

  #  figcbar   = plt.figure(figsize=(5, 0.6))
  #  axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
  #  bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
  #  plt.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar, orientation="horizontal")
  #  #plt.colorbar(im, extend="both", cax=axcbar, orientation="horizontal")

  #  cbarname  = sodir + "/cbar.grad.%s.png"%(vtype)
  #  figcbar.savefig(cbarname)

for prtype in lprtype:
  #****************************************
  # read precip data
  #----------------------------------------
  a2pr          = zeros([ny, nx])
  a2num         = zeros([ny, nx])
  a2one         = ones([ny, nx])
  #
  if prtype == "GSMaP":
    lhour_inc     = [-3, 0, 3, 6]
    for hour_inc in lhour_inc:
      (year_t, mon_t, day_t, hour_t) = shifttime(year, mon, day, hour, hour_inc)
      print day, year_t, mon_t, day_t, hour_t
      vdir_root  = "/media/disk2/data/GSMaP/sa.one/3hr/ptot"
      vdir       = vdir_root + "/%04d%02d"%(year_t, mon_t)
      vname      = vdir + "/gsmap_mvk.3rh.%04d%02d%02d.%02d00.v5.222.1.sa.one"%(year_t, mon_t, day_t, hour_t)
      a2pr_t      = fromfile(vname, float32).reshape(120, 360)
      a2pr_t      = gsmap_func.gsmap2global_one(a2pr_t, -9999.0)
      a2num_t    = ma.masked_where(a2pr_t ==-9999.0, a2one).filled(0.0)
      a2num      = a2num + a2num_t
      a2pr        = a2pr + ma.masked_equal(a2pr_t, -9999.0)
    #--
    #a2pr        = ma.masked_where(a2num < len(lhour_inc), a2pr)/a2num
    a2pr        = a2pr / len(lhour_inc)
    a2pr        = a2pr*60*60*24.0
    a2pr        = a2pr.filled(-9999.0)
    a2mask     = a2pr
  #--
  if prtype == "GPCP1DD":
    vdir_root     = "/media/disk2/data/GPCP1DD/data/1dd"
    vdir          = vdir_root + "/%04d"%(year)
    vname         = vdir + "/gpcp_1dd_v1.1_p1d.%04d%02d%02d.bn"%(year, mon, day)
    a2pr           = fromfile(vname, float32).reshape(ny, nx)
    a2pr           = flipud(a2pr)

  if prtype == "JRA":
    lhour_inc     = [0,6]
    for hour_inc in lhour_inc:
      (year_t, mon_t, day_t, hour_t) = shifttime(year, mon, day, hour, hour_inc)
      print day, year_t, mon_t, day_t, hour_t

      vdir_root     = "/media/disk2/data/JRA25/sa.one/6hr/PR"
      vdir          = vdir_root + "/%04d%02d"%(year_t, mon_t)
      vname         = vdir + "/fcst_phy2m.PR.%04d%02d%02d%02d.sa.one"%(year_t, mon_t, day_t, hour_t)
      a2pr_t         = fromfile(vname, float32).reshape(ny, nx)
      a2pr           = a2pr + a2pr_t
    #--
    a2pr           = a2pr / len(lhour_inc)
    a2pr           = a2pr * 60*60*24.0

  #----------------------------**************************************
  # for cross-section 
  #---------------------------------------
  def lat2y(lat):
    y = int((lat - (-90.0))/dlat)
    return y
  def lon2x(lon):
    x = int((lon - (0.0))/dlat)
    return x
  #-----------
  cslat  = 34.5
  cslon  = 143.5
  csy    = lat2y(cslat)
  csx    = lon2x(cslon)
  csxmin = lon2x(lllon)
  csxmax = lon2x(urlon)
  csymin = lat2y(lllat)
  csymax = lat2y(urlat)
  
  da1v_x = {}
  da1v_y = {}
  
  a1lon_dom = a1lon[csxmin:csxmax+1]
  a1lat_dom = a1lat[csymin:csymax+1]

  #--- horisontal -----------
  plt.clf()
  f, aax = plt.subplots(len(lplev)+1, sharex=True, figsize=(6,10))
   
  iplev = -1
  for plev in lplev[::-1]:
    iplev = iplev + 1
    pos   = int("%d%d%d"%(len(lplev),1,iplev+1))
    #
    a1v = da2v[plev][csy]
    da1v_x[plev] = a1v[csxmin:csxmax+1]
    #
    aax[iplev].plot(a1lon_dom, da1v_x[plev])
    aax[iplev].set_ylim(0, 4)
    aax[iplev].set_xlim(a1lon_dom[0]-1, a1lon_dom[-1])
    
    #-- title for each axis --
    aax[iplev].set_title("%d hPa"%(plev*0.01))
    #text(3,3,"AAAAAA")
    #-- ylabel ----
    #aax[iplev].set_ylabel("abs.grad.of\nwet.bulb.theta\n(K/100km)")
    aax[iplev].set_ylabel("(K/100km)")
 
  #- precip --
  a1pr_dom = a2pr[csy][csxmin:csxmax+1]
  aax[-1].plot(a1lon_dom,  a1pr_dom)
  aax[-1].set_xlim(a1lon_dom[0]-1, a1lon_dom[-1])
  aax[-1].set_ylim(0,60)
  aax[-1].set_ylabel("precip\n(mm day-1)")
  #-- title for precip --
  aax[-1].set_title("surface precipitation")
  #----------- 
  #f.subplots_adjust(hspace=0.05)
  #-- super title --
  suptitle("lat=%s"%(cslat))
  #-- save -----
  csname = sodir + "/cross.lat.%s.%s.png"%(cslat, prtype)
  f.savefig(csname)
  print csname
  plt.show()

  #--- meridional -----------
  plt.clf()
  f, aax = plt.subplots(len(lplev)+1, sharex=True, figsize=(6,10))
   
  iplev = -1
  for plev in lplev[::-1]:
    iplev = iplev + 1
    pos   = int("%d%d%d"%(len(lplev),1,iplev+1))
    #
    a1v = da2v[plev][:,csx]
    da1v_y[plev] = a1v[csymin:csymax+1]
    #
    aax[iplev].plot(a1lat_dom, da1v_y[plev])
    aax[iplev].set_ylim(0, 4)
    aax[iplev].set_xlim(a1lat_dom[0]-1, a1lat_dom[-1])
    
    #-- title for each axis --
    aax[iplev].set_title("%d hPa"%(plev*0.01))
    #text(3,3,"AAAAAA")
    #-- ylabel ----
    #aax[iplev].set_ylabel("abs.grad.of\nwet.bulb.theta\n(K/100km)")
    aax[iplev].set_ylabel("(K/100km)")
 
  #- precip --
  a1pr_dom = a2pr[:,csx][csymin:csymax+1]
  aax[-1].plot(a1lat_dom,  a1pr_dom)
  aax[-1].set_xlim(a1lat_dom[0]-1, a1lat_dom[-1])
  aax[-1].set_ylim(0,60)
  aax[-1].set_ylabel("precip\n(mm day-1)")
  #-- title for precip --
  aax[-1].set_title("surface precipitation")
  #----------- 
  #f.subplots_adjust(hspace=0.05)
  #-- super title --
  suptitle("lon=%s"%(cslon))
  #-- save -----
  csname = sodir + "/cross.lon.%s.%s.png"%(cslon, prtype)
  f.savefig(csname)
  print csname
  plt.show()
