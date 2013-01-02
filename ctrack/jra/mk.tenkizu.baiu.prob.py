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
from dtanl_fsub import *
from baiu_para import *
#-----------------------
iyear = 2004
eyear = 2004
imon  = 1
emon  = 12
iday  = 1
hour  = 0

contflag = "False"
cbarflag = "True"
#-----------------------------
miss_out  = -9999.0
ny  = 180
nx  = 360

sodir_root    = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/%02dh"%(thdura)
sodir         = sodir_root + "/mean"
cbardir       = sodir
#sodir         = sodir_root + "/%04d%02d/baiu"%(year, mon)
#cbardir       = sodir

ctrack_func.mk_dir(sodir)

dlat    = 1.0
dlon    = 1.0
a1lat   = arange(-89.5, 89.5  + dlat*0.1, dlat)
a1lon   = arange(0.5,   359.5 + dlon*0.1, dlon)

meridians = 10.0
parallels = 10.0

#************************
# for mapping
nnx        = int( (urlon - lllon)/dlon)
nny        = int( (urlat - lllat)/dlat)
a1lon_loc  = linspace(lllon, urlon, nnx)
a1lat_loc  = linspace(lllat, urlat, nny)
LONS, LATS = meshgrid( a1lon_loc, a1lat_loc)

#************************
# FUNCTIONS
#************************
def domain_xy_saone(lllat, urlat, lllon, urlon):
  lat_first = -89.5
  lon_first = 0.5
  dlat  = 1.0
  dlon  = 1.0
  ydom_first  = int( (lllat - lat_first + 0.5*dlat)/dlat)
  ydom_last   = int( (urlat - lat_first + 0.5*dlat)/dlat)
  xdom_first  = int( (lllon - lon_first + 0.5*dlon)/dlon)
  xdom_last   = int( (urlon - lon_first + 0.5*dlon)/dlon)
  return (ydom_first, ydom_last, xdom_first, xdom_last)
#---------------
def extract_domain_saone(a2in, lllat, urlat, lllon, urlon):
  (ydom_first, ydom_last, xdom_first, xdom_last) = domain_xy_saone(lllat, urlat, lllon, urlon)
  a2out = a2in[ydom_first:ydom_last+1, xdom_first:xdom_last+1]
  return a2out 
#---------------
# baiu locator :contour
#---------------
def mk_baiu_loc_contour(a2thermo, a2gradthermo, thfmask1, thfmask2):
  a2fmask1 = dtanl_fsub.mk_a2frontmask1(a2thermo.T).T
  a2fmask2 = dtanl_fsub.mk_a2frontmask2(a2thermo.T).T
  a2fmask1 = a2fmask1 * (1000.0*100.0)**2.0  #[(100km)-2]
  a2fmask2 = a2fmask2 * (1000.0*100.0)       #[(100km)-1]
 
  (a2grad2x, a2grad2y) = dtanl_fsub.mk_a2grad_saone(a2gradthermo.T)
  a2grad2x = a2grad2x.T
  a2grad2y = a2grad2y.T
  a2loc    = dtanl_fsub.mk_a2axisgrad(a2grad2x.T, a2grad2y.T).T
  
  a2loc    = ma.masked_where(a2fmask1 < thfmask1, a2loc)
  a2loc    = ma.masked_where(a2fmask2 < thfmask2, a2loc)
  a2loc  = ma.masked_where(a2u850 < u850min, a2loc)
  a2loc  = ma.masked_where(a2uup < uup_min, a2loc)
  a2loc  = ma.masked_where(a2q < qmin, a2loc)
  return a2loc

#---------------
# baiu locator
#---------------
def mk_baiu_loc(a2thermo, a2gradthermo, thfmask1, thfmask2):
  a2fmask1 = dtanl_fsub.mk_a2frontmask1(a2thermo.T).T
  a2fmask2 = dtanl_fsub.mk_a2frontmask2(a2thermo.T).T
  a2fmask1 = a2fmask1 *(1000.0*100.0)**2.0  #[(100km)-2]
  a2fmask2 = a2fmask2 *(1000.0*100.0)       #[(100km)-1]

  a2loc    = a2gradthermo  
  a2loc    = ma.masked_where(a2fmask1 < thfmask1, a2loc)
  a2loc    = ma.masked_where(a2fmask2 < thfmask2, a2loc)
  a2loc  = ma.masked_where(a2q < qmin, a2loc)
  a2loc  = ma.masked_where(a2u850 < u850min, a2loc)
  a2loc  = ma.masked_where(a2uup < uup_min, a2loc)
  return a2loc

#---------------
# baiu locator with speed
#---------------
def mk_baiu_loc_speed(a2thermo, a2gradthermo, thfmask1, thfmask2):
  a2fmask1 = dtanl_fsub.mk_a2frontmask1(a2thermo.T).T
  a2fmask2 = dtanl_fsub.mk_a2frontmask2(a2thermo.T).T
  a2fmask1 = a2fmask1 *(1000.0*100.0)**2.0  #[(100km)-2]
  a2fmask2 = a2fmask2 *(1000.0*100.0)       #[(100km)-1]

  a2loc  = a2gradthermo  
  a2loc  = ma.masked_where(a2fmask1 < thfmask1, a2loc)
  a2loc  = ma.masked_where(a2fmask2 < thfmask2, a2loc)
  a2loc  = ma.masked_where(a2q < qmin, a2loc)
  a2loc  = ma.masked_where(a2u850 < u850min, a2loc)
  a2loc  = ma.masked_where(a2uup < uup_min, a2loc)
  return a2loc

#***************
# drawing function
#---------------
def mk_regmap(a2in, bnd, scm, stitle, soname, cbarname, miss_out):
  #------------------------
  # Basemap
  #------------------------
  print "Basemap"
  figmap   = plt.figure()
  axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
  M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
  
  #-- transform -----------
  print "transform"
  a2value_trans    = M.transform_scalar( a2in,   a1lon, a1lat, nnx, nny)
  a2value_trans    = a2value_trans.filled(miss_out)
  #-- boundaries ----------
  bnd_cbar   = [-1.0e+40] + bnd + [1.0e+40]
  
  #-- color ---------------
  cminst   = matplotlib.cm.get_cmap(scm, len(bnd))
  acm      = cminst( arange( len(bnd) ) )
  lcm      = [[1,1,1,1]]+ acm.tolist()
  mycm     = matplotlib.colors.ListedColormap( lcm )
  
  #-- imshow    -----------
  im       = M.imshow(a2value_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")

  #-- shade     -----------
  a2shade_trans = ma.masked_not_equal(a2value_trans, miss_out)
  cmshade       = matplotlib.colors.ListedColormap([(0.8,0.8,0.8), (0.8,0.8,0.8)])
  im            = M.imshow(a2shade_trans, origin="lower", cmap=cmshade) 
  
  #-- coastline ---------------
  print "coastlines"
  M.drawcoastlines()
  
  #-- meridians and parallels
  M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1])
  M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0])
  #-- title -------------------
  axmap.set_title("%s"%(stitle))
  #-- save --------------------
  plt.savefig(soname)
  print soname 
  # for colorbar ---
  if cbarflag == "True":
    figmap   = plt.figure()
    axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
    M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
    a2v_trans    = M.transform_scalar( a2in,   a1lon, a1lat, nnx, nny)
    im       = M.imshow(a2value_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm)
  
    figcbar   = plt.figure(figsize=(5, 0.6))
    axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
    bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
    plt.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar, orientation="horizontal")
    figcbar.savefig(cbarname)

#*************************************************
def mk_regmap_contour(a2in, bnd, scm, stitle, soname, cbarname, miss_out):
  #------------------------
  # Basemap
  #------------------------
  print "Basemap"
  figmap   = plt.figure()
  axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
  M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
  
  #-- transform -----------
  print "transform"
  a2value_trans    = M.transform_scalar( a2in,   a1lon, a1lat, nnx, nny)
  a2value_trans    = a2value_trans.filled(miss_out)

  #-- to contour ----------
  a2value_trans    = dtanl_fsub.mk_a2contour_regional(a2value_trans.T, 0.0, 0.0, -9999.0).T

  #-- boundaries ----------
  bnd_cbar   = [-1.0e+40] + bnd + [1.0e+40]
  
  #-- color ---------------
  cminst   = matplotlib.cm.get_cmap(scm, len(bnd))
  acm      = cminst( arange( len(bnd) ) )
  lcm      = [[1,1,1,1]]+ acm.tolist()
  mycm     = matplotlib.colors.ListedColormap( lcm )
  
  #-- imshow    -----------
  im       = M.imshow(a2value_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")

  #-- shade     -----------
  a2shade_trans = ma.masked_not_equal(a2value_trans, miss_out)
  cmshade       = matplotlib.colors.ListedColormap([(0.8,0.8,0.8), (0.8,0.8,0.8)])
  im            = M.imshow(a2shade_trans, origin="lower", cmap=cmshade) 
  
  #-- coastline ---------------
  print "coastlines"
  M.drawcoastlines()
  
  #-- meridians and parallels
  M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1])
  M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0])
  #-- title -------------------
  axmap.set_title("%s"%(stitle))
  #-- save --------------------
  plt.savefig(soname)
  print soname 
  # for colorbar ---
  if cbarflag == "True":
    figmap   = plt.figure()
    axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
    M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
    a2v_trans    = M.transform_scalar( a2in,   a1lon, a1lat, nnx, nny)
    im       = M.imshow(a2value_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm)
  
    figcbar   = plt.figure(figsize=(5, 0.6))
    axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
    bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
    plt.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar, orientation="horizontal")
    figcbar.savefig(cbarname)
 
#******************************************************
(ydom_first, ydom_last, xdom_first, xdom_last) = domain_xy_saone(lllat,urlat, lllon, urlon)
nydom  = ydom_last - ydom_first + 1
nxdom  = xdom_last - xdom_first + 1

a2one        = ones([ny,nx],  float32)
a2ysect_dom  = zeros([nydom], float32)
lxticks       = []
ntimes   = 0
#------------------------------------------------------
for mon in range(imon, emon+1):
  print year, mon
  a2prob_map   = zeros([ny,nx], float32)
  nprob_map    = 0
  for year in range(iyear, eyear+1):
    eday  = calendar.monthrange(year, mon)[1]
    for day in range(iday, eday+1):
      #------------------------------
      nprob_map   = nprob_map + 1
      ntimes      = ntimes + 1 
      stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)
      lxticks.append("%04d.%02d.%02d"%(year, mon, day))
      #******************************************************
      #-- U wind at 850hPa ---------------------------
      plev_temp  = 850*100.0
      idir_root  = "/media/disk2/data/JRA25/sa.one/6hr"
      idir       = idir_root + "/UGRD/%04d%02d"%(year, mon)
      uname850   = idir + "/anal_p25.UGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_temp*0.01, year, mon, day, hour)
      a2u850     = fromfile(uname850, float32).reshape(ny,nx)
      
      #-- U wind at upper level ---------------------------
      idir_root  = "/media/disk2/data/JRA25/sa.one/6hr"
      idir       = idir_root + "/UGRD/%04d%02d"%(year, mon)
      uupname   = idir + "/anal_p25.UGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_up*0.01, year, mon, day, hour)
      a2uup     = fromfile(uupname, float32).reshape(ny,nx)
      
      #-- q: mixing ratio --------------------------
      qname = "/media/disk2/data/JRA25/sa.one/6hr/SPFH/%04d%02d/anal_p25.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
      a2q   = fromfile(qname, float32).reshape(ny,nx)
      
      #-- t: mixing ratio --------------------------
      tname = "/media/disk2/data/JRA25/sa.one/6hr/TMP/%04d%02d/anal_p25.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
      a2t   = fromfile(tname, float32).reshape(ny,nx)
      
      #-- theta_e -----------------------------------
      a2theta_e = dtanl_fsub.mk_a2theta_e(plev, a2t.T, a2q.T).T
      #-- grad.theta_e ------------------------------------
      a2thermo         = a2theta_e
      a2gradtheta_e    = dtanl_fsub.mk_a2grad_abs_saone(a2thermo.T).T
      
      #**********************************************
      # base: grad.theta_e
      a2gradtheta_e  = a2gradtheta_e
      a2gradtheta_e  = ma.masked_where(a2u850 < u850min, a2gradtheta_e)
      a2gradtheta_e  = ma.masked_where(a2q < qmin, a2gradtheta_e)
      a2gradtheta_e  = a2gradtheta_e * 1000.0*100.0 # [K (100km)-1]
      
      ##**********************************************
      # front locator: theta_e
      a2thermo             = a2theta_e # K
      a2gradthermo         = a2gradtheta_e   # K/100km
      thfmask1 = thfmasktheta1
      thfmask2 = thfmasktheta2
      #------
      if contflag == "True":
        a2loc    = mk_baiu_loc_contour(a2thermo, a2gradthermo, thfmask1, thfmask2)
      else:
        a2loc    = mk_baiu_loc(a2thermo, a2gradthermo, thfmask1, thfmask2)
      #------
      a2prob_map_temp= ma.masked_where(a2loc.mask ==True, a2one).filled(0.0)
      a2prob_map     = a2prob_map + a2prob_map_temp

      #--- stack ----------
      a2ysect_dom_temp   = extract_domain_saone(a2prob_map_temp, lllat, urlat, lllon, urlon)
      a2ysect_dom_temp   = mean(a2ysect_dom_temp, axis=1)
      a2ysect_dom        = c_[a2ysect_dom, a2ysect_dom_temp]

  #-------------
  a2prob_map = a2prob_map / nprob_map
  a2prob_map = ma.masked_equal( a2prob_map, +88888)

  #******************************
  #--- save : map
  soname  = sodir + "/prob.baiu.map.%04d-%04d.%02d.bn"%(iyear, eyear, mon)
  
  #(a2prob_map.filled(miss_out)).tofile(soname)
  
  #--- fig : map ------
  figname = soname[:-3] + ".png"
  vtype      = "prob.baiu"
  bnd        = list(arange(0.0, 1.0+0.01, 0.1))
  
  scm        = "gray_r"
  stitle     = "%s\n %04d-%04d, mon:%02d"%(vtype, iyear, eyear, mon)
  stitle     = stitle + "ulev:%dhPa  u850:%3.2f  uup:%3.2f  q:%4.3f M2:%3.2f\n"%(plev_up*0.01, u850min, uup_min, qmin, thfmask2)
  stitle     = stitle + "%04d-%02d-%02d  UTC %02d:00 (JST %02d:00)"%(year, mon, day, hour, hour+9)
  cbarname   = cbardir + "/cbar.%s.png"%(vtype)
  
  mk_regmap(a2prob_map, bnd, scm, stitle, figname, cbarname, miss_out)
  print figname
#***********************************
#  time-latitude section
#----------------------------------
plt.clf()
vtype    = "time-lat section"
timestep = 20
latstep  = 10
lyticks  = arange(lllat, urlat+0.01)
bnd      = list(arange(0.0, 0.7+0.01, 0.1))
scm      = "gray_r"
stitle     = "%s\n %04d-%04d, mon:%02d-%02d"%(vtype, iyear, year, imon, emon)
stitle     = stitle + "ulev:%dhPa  u850:%3.2f  uup:%3.2f  q:%4.3f M2:%3.2f\n"%(plev_up*0.01, u850min, uup_min, qmin, thfmask2)
stitle     = stitle + "%04d-%02d-%02d  UTC %02d:00 (JST %02d:00)"%(year, mon, day, hour, hour+9)

figname_sect   = sodir + "/prob.baiu.time-lat.%04d-%04d.%02d-%02d.png"%(iyear, eyear, imon, emon)
cbarname_sect  = cbardir + "/cbar.%s.png"%(vtype)

#-- imshow --
figsect  = plt.figure(figsize=(6,5))
axsect   = figsect.add_axes([0.2, 0.2, 0.8, 0.9])
im       = imshow( a2ysect_dom, norm=BoundaryNormSymm(bnd), cmap=scm, origin="lower", interpolation="nearest")
#-- ticks ---
xticks( range(len(lxticks))[::timestep], lxticks[::timestep], rotation=90 )
yticks( range(len(lyticks))[::latstep],  lyticks[::latstep] )
#-- title ---
#axsect.set_title(stitle)

#-- save  ---
figsect.savefig( figname_sect)
print figname_sect

#-- color bar ------
bnd_cbar = bnd

figcbar = plt.figure(figsize=(5, 0.6))
axcbar  = figcbar.add_axes([0, 0.4, 1.0, 0.6])
plt.colorbar( im, boundaries=bnd_cbar, extend="both", cax=axcbar,orientation="horizontal")
figcbar.savefig( cbarname_sect)

