from dtanl_fsub import *
from numpy import *
import ctrack_func
import ctrack_para
import matplotlib.pyplot as plt
import matplotlib
import sys,os
import datetime
from cf.plot import *
import Image
#---------------------------
if len(sys.argv) >1:
  year  = int(sys.argv[1])
  mon   = int(sys.argv[2])
  day   = int(sys.argv[3])
  hour  = int(sys.argv[4])
  lllat = float(sys.argv[5])
  urlat = float(sys.argv[6])
  lllon = float(sys.argv[7])
  urlon = float(sys.argv[8])
  plev  = float(sys.argv[9])
  cbarflag = sys.argv[10]
  thdura = float(sys.argv[11])
else:
  year  = 2004
  mon   = 7
  day   = 18
  hour  = 0
  
  # local region ------
  # corner points should be
  # at the center of original grid box
  lllat   = 0.
  urlat   = 60.
  lllon   = 60.
  urlon   = 160.
  #plev    = 925*100.0  #(Pa)
  plev    = 850*100.0  #(Pa)
  cbarflag= "True"
  thdura= 6
#----------------------------

cslat  = 36.5
cslon  = 150.5
ny      = 180
nx      = 360

#--------------------
miss_int= -9999

#lplev = [925*100.0, 850*100.0, 700*100.0, 600*100.0, 500*100.0, 400*100.0, 300*100.0]
#lplev = [925*100.0, 850*100.0,  700*100, 500*100.0,300*100 ]
#lplev = [925*100.0, 850*100.0,  700*100, 500*100.0]
#lplev = [850*100.0]
lplev = [plev] # [Pa]
lprtype = ["JRA"]
vtype = "grad.t"

#lthfmask0  = [0.2,0.5,1.0]
lthfmask0  = [1.0e+5]

#lthfmask1 = [0.0, 0.1, 0.2, 0.3]
#lthfmask1 = [0.12,0.15,0.17]
#lthfmask1 = [0.05, 0.15, 0.3]
lthfmask1 = [0.03, 0.05, 0.1]
#thfmask1 = 0.0
#thfmask1 = 0.1
#thfmask1 = 0.2
#thfmask1 = 0.3
#thfmask1 = 0.5

#lthfmask2 = [0.0]
#lthfmask2 = [0.1]
#lthfmask2 = [0.4]
#lthfmask2 = [0.75]
#lthfmask2 = [1.0]
lthfmask2 = [0.1, 0.2, 0.3]

tname = "/media/disk2/data/JRA25/sa.one/6hr/TMP/%04d%02d/anal_p25.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
qname = "/media/disk2/data/JRA25/sa.one/6hr/SPFH/%04d%02d/anal_p25.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)


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
da2v  = {}
da2v2 = {}
da2loc= {}
da2fmask1 = {}
da2fmask2 = {}
#------------------
for plev in lplev:
  a2t    = fromfile(tname, float32).reshape(180,360)
  a2q    = fromfile(qname, float32).reshape(180,360)
  a2wb     = dtanl_fsub.mk_a2wetbulbtheta(plev, a2t.T, a2q.T).T
  a2thermo     = a2t
  a2gradthermo = dtanl_fsub.mk_a2grad_abs_saone(a2t.T).T
  #-- locator ---
  #a2gradthermo2 = dtanl_fsub.mk_a2grad_abs_saone(a2gradthermo.T).T
  (a2grad2x, a2grad2y) = dtanl_fsub.mk_a2grad_saone(a2gradthermo.T)
  a2grad2x = a2grad2x.T
  a2grad2y = a2grad2y.T
  a2loc    = dtanl_fsub.mk_a2axisgrad(a2grad2x.T, a2grad2y.T).T
  #(a2axis_x, a2axis_y) = dtanl_fsub.mk_a2meanunitaxis( 2grad2x.T, a2grad2x.T
  a2fmask1 = dtanl_fsub.mk_a2frontmask1(a2thermo.T).T
  a2fmask2 = dtanl_fsub.mk_a2frontmask2(a2thermo.T).T

  cbarflag = True



  stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)

  sodir_root    = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/%02dh"%(thdura)
  sodir         = sodir_root + "/%04d%02d/front/%02d"%(year, mon, day)
  ctrack_func.mk_dir(sodir)

  #soname        = sodir + "/tenkizu.%04d.%02d.%02d.%02d.%s.png"%(year, mon, day, hour, vtype)
  soname        = sodir + "/grad.t.tenkizu.%04d.%02d.%02d.%02d.%04dhPa.%s.png"%(year, mon, day, hour, plev*0.01, vtype)
  #name_grad2    = sodir + "/grad2.wb.tenkizu.%04d.%02d.%02d.%02d.%04dhPa.%s.png"%(year, mon, day, hour, plev*0.01, vtype)

  #name_loc      = sodir + "/loc.wb.tenkizu.%04d.%02d.%02d.%02d.%04dhPa.%s.png"%(year, mon, day, hour, plev*0.01, vtype)
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
  a2v           = a2gradthermo * 1000.0*100.0         # [K (100km)-1]
  a2loc         = a2loc * (1000.0*100.0)**3.0     # [K (100km)-3]
  a2fmask1      = a2fmask1 * (1000.0*100.0)**2.0  # [K (100km)-2]
  a2fmask2      = a2fmask2 * (1000.0*100.0)       # [K (100km)-1]
  #
  da2v[plev]   = a2v
  da2loc[plev] = a2loc
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
  #************************
  #if plev not in [850*100.0]:
  #  continue
  #************************
  # for mapping
  nnx        = int( (urlon - lllon)/dlon)
  nny        = int( (urlat - lllat)/dlat)
  a1lon_loc  = linspace(lllon, urlon, nnx)
  a1lat_loc  = linspace(lllat, urlat, nny)
  LONS, LATS = meshgrid( a1lon_loc, a1lat_loc)
  #-- boundaries ----------
  bnd        = [0.1, 0.4, 0.7, 1.0,1.3,1.6,1.9,2.1,2.4]
  bnd_cbar   = [-1.0e+40] + bnd + [1.0e+40]
  #-- color ---------------
  #scm      = "gist_stern_r"
  #scm      = "OrRd_r"
  scm      = "Spectral_r"
  cm_inst  = matplotlib.cm.get_cmap(scm, len(bnd)+1)
  acm      = cm_inst( arange(len(bnd)+1) )
  lcm      = acm.tolist()
  mycm     = matplotlib.colors.ListedColormap( lcm )
  #mycm     = "jet"

  #********************************
  #*** grad *
  #********************************
  #------------------------
  # Basemap
  #------------------------
  print "Basemap"
  plt.clf()
  figmap   = plt.figure()
  axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
  M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)

  #-- transform -----------
  print "transform"
  a2psl_trans  = M.transform_scalar( a2psl, a1lon, a1lat, nnx, nny)
  a2v_trans    = M.transform_scalar( a2v,   a1lon, a1lat, nnx, nny)
  #a2v2_trans   = M.transform_scalar( a2v2,   a1lon, a1lat, nnx, nny)

  #-- value imshow --------
  im       = M.imshow(a2v_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")

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

  #-- coastline ---------------
  print "coastlines"
  M.drawcoastlines()
  #-- meridians and parallels
  M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1])
  M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0])
  #-- title -------------------
  axmap.set_title("%04d-%02d-%02d  UTC %02d:00 (JST %02d:00) %04dhPa"%(year, mon, day, hour, hour+9, plev*0.01))

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
    #im       = M.imshow(a2v_trans, origin="lower", cmap=mycm)

    figcbar   = plt.figure(figsize=(5, 0.6))
    axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
    bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
    plt.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar, orientation="horizontal")
    #plt.colorbar(im, extend="both", cax=axcbar, orientation="horizontal")

    cbarname  = sodir[:-3] + "/cbar.grad.%s.png"%(vtype)
    figcbar.savefig(cbarname)

  #********************************
  # loc
  #********************************
  uname      = "/media/disk2/data/JRA25/sa.one/6hr/UGRD/%04d%02d/anal_p25.UGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
  vname      = "/media/disk2/data/JRA25/sa.one/6hr/VGRD/%04d%02d/anal_p25.VGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
  a2uwind    = fromfile(uname, float32).reshape(180,360)
  a2vwind    = fromfile(vname, float32).reshape(180,360)
  a2loc_temp = dtanl_fsub.mk_a2contour(a2loc.T, 0.0, 0.0, -9999.0).T
  a2fspeed   = dtanl_fsub.mk_a2frontspeed(a2wb.T, a2loc_temp.T, a2uwind.T, a2vwind.T, -888888).T

  for thfmask0 in lthfmask0:
    for thfmask2 in lthfmask2:
      #---------------------------
      name_loc_full = sodir[:-3] + "/loc.t.tenkizu.%04d.%02d.%02d.%02d.%04dhPa.%s.M0_%3.2f.join.png"%(year, mon, day, hour, plev*0.01, vtype, thfmask0)
      #
      nsub_x    = 3
      nsub_y    = 3
      subsize_x = 800
      subsize_y = 600
      full_x    = nsub_x * subsize_x
      full_y    = nsub_y * subsize_y
    
      pal  = Image.new( "RGBA", (full_x, full_y))
  
      #---------------------------
      ithfmask1  = -1
      for thfmask1 in lthfmask1:
        ithfmask1 = ithfmask1 + 1
  
        #-- prep for jointed figs --
        name_loc      = sodir + "/loc.t.tenkizu.%04d.%02d.%02d.%02d.%04dhPa.%s.M0_%3.2f.M1_%3.2f.temp.png"%(year, mon, day, hour, plev*0.01, vtype, thfmask0, thfmask1)
        #
        #-- boundaries ----------
        #bnd        = [-0.4,-0.35, -0.3, -0.25, -0.2, -0.15, -0.1, -0.05, 0.05, 0.1, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
        bnd        = list(arange(-10.0, 10.0+1, 2.0))
        #bnd        = [-1.0e+5, -4.0, 4.0, 1.0e+5]
        bnd_cbar   = [-1.0e+40] + bnd + [1.0e+40]
        #-- color ---------------
        #scm      = "gist_stern_r"
        #scm      = "OrRd"
        scm      = "Spectral_r"
        #cm_inst  = matplotlib.cm.get_cmap(scm, len(bnd)+1)
        #acm      = cm_inst( arange(len(bnd)+1) )
        #lcm      = [[1,1,1,1]] + acm.tolist()
        #mycm     = matplotlib.colors.ListedColormap( lcm )
        mycm     = scm
      
        #------------------------
        # Basemap
        #------------------------
        print "Basemap"
        plt.clf()
        figmap   = plt.figure()
        axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
        M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
      
        #-- transform -----------
        print "transform"
        a2psl_trans    = M.transform_scalar( a2psl, a1lon, a1lat, nnx, nny)
        a2fspeed_trans = M.transform_scalar( a2fspeed, a1lon, a1lat, nnx, nny)
        a2psl_trans    = M.transform_scalar( a2psl, a1lon, a1lat, nnx, nny)
        a2loc_trans    = M.transform_scalar( a2loc,   a1lon, a1lat, nnx, nny)
        a2loc_trans    = dtanl_fsub.mk_a2contour_regional(a2loc_trans, 0.0, 0.0, -9999.0)
        a2loc_trans    = ma.masked_where( a2loc_trans != 0.0, a2fspeed_trans).filled(-9999.0)
        a2v_trans      = M.transform_scalar( a2v,   a1lon, a1lat, nnx, nny)
        a2fmask1_trans = M.transform_scalar( a2fmask1, a1lon, a1lat, nnx, nny)
        a2fmask2_trans = M.transform_scalar( a2fmask2, a1lon, a1lat, nnx, nny)
        #-- value imshow --------
        #im       = M.imshow(a2v_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")
        #-- locator -----
        #a2loc_trans = ma.masked_outside(a2loc_trans, -thfmask0, thfmask0).filled(-9999.0)
        a2loc_trans = ma.masked_where(a2fmask1_trans < thfmask1, a2loc_trans).filled(-9999.0)
        a2loc_trans = ma.masked_where(a2fmask2_trans < thfmask2, a2loc_trans).filled(-9999.0)
        #im          = M.contour(LONS, LATS, a2loc_trans, latlon=True, levels=[-10e+10, 0.0, 10e+10], colors="r")
        im       = M.imshow(ma.masked_equal(a2loc_trans, -9999.0), origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")

        #-- Mask -----------------
        a2mask_trans = ma.masked_not_equal(a2loc_trans, -9999.0)
        cmshade      = matplotlib.colors.ListedColormap([(0.8, 0.8, 0.8), (0.8, 0.8, 0.8)])
        im           = M.imshow(a2mask_trans, origin="lower",cmap=cmshade)
        ##-- contour PSL ----------
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
      
        #-- coastline ---------------
        print "coastlines"
        M.drawcoastlines()
        #-- meridians and parallels
        M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1])
        M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0])
        #-- title -------------------
        axmap.set_title("%04d-%02d-%02d  UTC %02d:00 (JST %02d:00) %04dhPa \n M0 %3.2f, M1 %3.2f"%(year, mon, day, hour, hour+9, plev*0.01, thfmask0, thfmask1))
      
        #-- save --------------------
        print "save"
        plt.savefig(name_loc)
        plt.clf()
        print name_loc
        #-------------------
      
        # for colorbar ---
        if cbarflag == True:
          figmap   = plt.figure()
          axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
          M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
          a2v_trans= M.transform_scalar( a2v,   a1lon, a1lat, nnx, nny)
          im       = M.imshow(a2v_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm)
      
          figcbar   = plt.figure(figsize=(5, 0.6))
          axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
          bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
          plt.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar, orientation="horizontal")
          #plt.colorbar(im, extend="both", cax=axcbar, orientation="horizontal")
      
          cbarname  = sodir[:-3] + "/cbar.loc.%s.png"%(vtype)
          figcbar.savefig(cbarname)
        #-------------------
        imtemp      = Image.open(name_loc)
        imtemp      = imtemp.resize((subsize_x, subsize_y))
        #
        isub_x      = mod(ithfmask1, nsub_x)
        isub_y      = int(ithfmask1 / nsub_x)
        ulx         = isub_x* subsize_x
        uly         = isub_y* subsize_y
        pal.paste( imtemp, (ulx,uly, ulx+subsize_x, uly+subsize_y))
      #------------------
      #-- gz   ---
      ithfmask1   = ithfmask1 + 1
      #figname = sodir_root +"/%04d%02d/front"%(year,mon) + "/tenkizu.gz.%04d.%02d.%02d.%02d.upper.png"%(year, mon, day, hour)
      figname = sodir + "/tenkizu.gz.%04d.%02d.%02d.%02d.upper.png"%(year, mon, day, hour)
      im_temp     = Image.open(figname)
      isub_x      = mod(ithfmask1, nsub_x)
      isub_y      = int(ithfmask1 / nsub_x)
      ulx         = isub_x* subsize_x
      uly         = isub_y* subsize_y
      pal.paste( im_temp, (ulx,uly, ulx+subsize_x, uly+subsize_y))
      #--
      pal.save(name_loc_full)
      print name_loc_full

      #------------------
      ##-- wind ---
      #ithfmask1   = ithfmask1 + 1
      ##figname = sodir_root +"/%04d%02d/front"%(year,mon) + "/tenkizu.wind.%04d.%02d.%02d.%02d.0850hPa.png"%(year, mon, day, hour)
      #figname = sodir + "/tenkizu.wind.%04d.%02d.%02d.%02d.0850hPa.png"%(year, mon, day, hour)
      #im_temp     = Image.open(figname)
      #isub_x      = mod(ithfmask1, nsub_x)
      #isub_y      = int(ithfmask1 / nsub_x)
      #ulx         = isub_x* subsize_x
      #uly         = isub_y* subsize_y
      #pal.paste( im_temp, (ulx,uly, ulx+subsize_x, uly+subsize_y))
      ##--
      #pal.save(name_loc_full)
      #print name_loc_full

      ##------------------
      #-- wb   ---
      ithfmask1   = ithfmask1 + 1
      #figname = sodir_root +"/%04d%02d/front"%(year,mon) + "/tenkizu.wb.%04d.%02d.%02d.%02d.0850hPa.png"%(year, mon, day, hour)
      figname = sodir + "/tenkizu.wb.%04d.%02d.%02d.%02d.%04dhPa.png"%(year, mon, day, hour, plev*0.01)
      im_temp     = Image.open(figname)
      isub_x      = mod(ithfmask1, nsub_x)
      isub_y      = int(ithfmask1 / nsub_x)
      ulx         = isub_x* subsize_x
      uly         = isub_y* subsize_y
      pal.paste( im_temp, (ulx,uly, ulx+subsize_x, uly+subsize_y))
      #--
      pal.save(name_loc_full)
      print name_loc_full

      #-- temperature & mixing ratio   ---
      ithfmask1   = ithfmask1 + 1
      figname = sodir + "/tenkizu.t.q.%04d.%02d.%02d.%02d.%04dhPa.png"%(year, mon, day, hour, plev*0.01)
      im_temp     = Image.open(figname)
      isub_x      = mod(ithfmask1, nsub_x)
      isub_y      = int(ithfmask1 / nsub_x)
      ulx         = isub_x* subsize_x
      uly         = isub_y* subsize_y
      pal.paste( im_temp, (ulx,uly, ulx+subsize_x, uly+subsize_y))
      #--
      pal.save(name_loc_full)
      print name_loc_full


      #-------------------
      #-- prep --
      for preptype in ["JRA","GSMaP"]:
        ithfmask1   = ithfmask1 + 1
        prepfigname = sodir_root +"/%04d%02d"%(year,mon) + "/tenkizu.%04d.%02d.%02d.%02d.%s.png"%(year, mon, day, hour, preptype)
        imprep      = Image.open(prepfigname)
        isub_x      = mod(ithfmask1, nsub_x)
        isub_y      = int(ithfmask1 / nsub_x)
        ulx         = isub_x* subsize_x
        uly         = isub_y* subsize_y
        pal.paste( imprep, (ulx,uly, ulx+subsize_x, uly+subsize_y))
        #--
        pal.save(name_loc_full)
        print name_loc_full
  

      #-- remove temp --
      for thfmask1 in lthfmask1:
        name_loc      = sodir + "/loc.t.tenkizu.%04d.%02d.%02d.%02d.%04dhPa.%s.M0_%3.2f.M1_%3.2f.temp.png"%(year, mon, day, hour, plev*0.01, vtype, thfmask0, thfmask1)
        os.remove(name_loc)
      #-----------------

#for prtype in lprtype:
#  #****************************************
#  # read precip data
#  #----------------------------------------
#  a2pr          = zeros([ny, nx])
#  a2num         = zeros([ny, nx])
#  a2one         = ones([ny, nx])
#  #
#  if prtype == "GSMaP":
#    lhour_inc     = [-3, 0, 3, 6]
#    for hour_inc in lhour_inc:
#      (year_t, mon_t, day_t, hour_t) = shifttime(year, mon, day, hour, hour_inc)
#      print day, year_t, mon_t, day_t, hour_t
#      vdir_root  = "/media/disk2/data/GSMaP/sa.one/3hr/ptot"
#      vdir       = vdir_root + "/%04d%02d"%(year_t, mon_t)
#      vname      = vdir + "/gsmap_mvk.3rh.%04d%02d%02d.%02d00.v5.222.1.sa.one"%(year_t, mon_t, day_t, hour_t)
#      a2pr_t      = fromfile(vname, float32).reshape(120, 360)
#      a2pr_t      = gsmap_func.gsmap2global_one(a2pr_t, -9999.0)
#      a2num_t    = ma.masked_where(a2pr_t ==-9999.0, a2one).filled(0.0)
#      a2num      = a2num + a2num_t
#      a2pr        = a2pr + ma.masked_equal(a2pr_t, -9999.0)
#    #--
#    #a2pr        = ma.masked_where(a2num < len(lhour_inc), a2pr)/a2num
#    a2pr        = a2pr / len(lhour_inc)
#    a2pr        = a2pr*60*60*24.0
#    a2pr        = a2pr.filled(-9999.0)
#    a2mask     = a2pr
#  #--
#  if prtype == "GPCP1DD":
#    vdir_root     = "/media/disk2/data/GPCP1DD/data/1dd"
#    vdir          = vdir_root + "/%04d"%(year)
#    vname         = vdir + "/gpcp_1dd_v1.1_p1d.%04d%02d%02d.bn"%(year, mon, day)
#    a2pr           = fromfile(vname, float32).reshape(ny, nx)
#    a2pr           = flipud(a2pr)
#
#  if prtype == "JRA":
#    lhour_inc     = [0,6]
#    for hour_inc in lhour_inc:
#      (year_t, mon_t, day_t, hour_t) = shifttime(year, mon, day, hour, hour_inc)
#      print day, year_t, mon_t, day_t, hour_t
#
#      vdir_root     = "/media/disk2/data/JRA25/sa.one/6hr/PR"
#      vdir          = vdir_root + "/%04d%02d"%(year_t, mon_t)
#      vname         = vdir + "/fcst_phy2m.PR.%04d%02d%02d%02d.sa.one"%(year_t, mon_t, day_t, hour_t)
#      a2pr_t         = fromfile(vname, float32).reshape(ny, nx)
#      a2pr           = a2pr + a2pr_t
#    #--
#    a2pr           = a2pr / len(lhour_inc)
#    a2pr           = a2pr * 60*60*24.0
#
#  #***************************************
#  # for cross-section : grad
#  #---------------------------------------
#  def lat2y(lat):
#    y = int((lat - (-90.0))/dlat)
#    return y
#  def lon2x(lon):
#    x = int((lon - (0.0))/dlat)
#    return x
#  #-----------
#  csy    = lat2y(cslat)
#  csx    = lon2x(cslon)
#  csxmin = lon2x(lllon)
#  csxmax = lon2x(urlon)
#  csymin = lat2y(lllat)
#  csymax = lat2y(urlat)
#  
#  da1v_x = {}
#  da1v_y = {}
#  
#  a1lon_dom = a1lon[csxmin:csxmax+1]
#  a1lat_dom = a1lat[csymin:csymax+1]
#
#  #--- horisontal -----------
#  plt.clf()
#  f, aax = plt.subplots(len(lplev)+1, sharex=True, figsize=(6,10))
#   
#  iplev = -1
#  for plev in lplev[::-1]:
#    iplev = iplev + 1
#    pos   = int("%d%d%d"%(len(lplev),1,iplev+1))
#    #
#    a1v = da2v[plev][csy]
#    da1v_x[plev] = a1v[csxmin:csxmax+1]
#    #
#    aax[iplev].plot(a1lon_dom, da1v_x[plev])
#    aax[iplev].set_ylim(0, 4)
#    aax[iplev].set_xlim(a1lon_dom[0]-1, a1lon_dom[-1])
#    
#    #-- title for each axis --
#    aax[iplev].set_title("%d hPa"%(plev*0.01))
#    #text(3,3,"AAAAAA")
#    #-- ylabel ----
#    #aax[iplev].set_ylabel("abs.grad.of\nwet.bulb.theta\n(K/100km)")
#    aax[iplev].set_ylabel("(K/100km)")
# 
#  #- precip --
#  a1pr_dom = a2pr[csy][csxmin:csxmax+1]
#  aax[-1].plot(a1lon_dom,  a1pr_dom)
#  aax[-1].set_xlim(a1lon_dom[0]-1, a1lon_dom[-1])
#  aax[-1].set_ylim(0,60)
#  aax[-1].set_ylabel("precip\n(mm day-1)")
#  #-- title for precip --
#  aax[-1].set_title("surface precipitation")
#  #----------- 
#  #f.subplots_adjust(hspace=0.05)
#  #-- super title --
#  plt.suptitle("lat=%s"%(cslat))
#  #-- save -----
#  csname = sodir + "/cross.%04d.%02d.%02d.%02d.lat.%s.%s.png"%(year, mon, day, hour, cslat, prtype)
#  f.savefig(csname)
#  print csname
#
#  #--- meridional -----------
#  plt.clf()
#  f, aax = plt.subplots(len(lplev)+1, sharex=True, figsize=(6,10))
#   
#  iplev = -1
#  for plev in lplev[::-1]:
#    iplev = iplev + 1
#    pos   = int("%d%d%d"%(len(lplev),1,iplev+1))
#    #
#    a1v = da2v[plev][:,csx]
#    da1v_y[plev] = a1v[csymin:csymax+1]
#    #
#    aax[iplev].plot(a1lat_dom, da1v_y[plev])
#    aax[iplev].set_ylim(0, 4)
#    aax[iplev].set_xlim(a1lat_dom[0]-1, a1lat_dom[-1])
#    
#    #-- title for each axis --
#    aax[iplev].set_title("%d hPa"%(plev*0.01))
#    #text(3,3,"AAAAAA")
#    #-- ylabel ----
#    #aax[iplev].set_ylabel("abs.grad.of\nwet.bulb.theta\n(K/100km)")
#    aax[iplev].set_ylabel("(K/100km)")
# 
#  #- precip --
#  a1pr_dom = a2pr[:,csx][csymin:csymax+1]
#  aax[-1].plot(a1lat_dom,  a1pr_dom)
#  aax[-1].set_xlim(a1lat_dom[0]-1, a1lat_dom[-1])
#  aax[-1].set_ylim(0,60)
#  aax[-1].set_ylabel("precip\n(mm day-1)")
#  #-- title for precip --
#  aax[-1].set_title("surface precipitation")
#  #----------- 
#  #f.subplots_adjust(hspace=0.05)
#  #-- super title --
#  plt.suptitle("lon=%s"%(cslon))
#  #-- save -----
#  csname = sodir + "/cross.%04d.%02d.%02d.%02d.lon.%s.%s.png"%(year, mon, day, hour, cslon, prtype)
#  f.savefig(csname)
#  print csname
#
#
#  #***************************************
#  # for cross-section : loc
#  #---------------------------------------
#  def lat2y(lat):
#    y = int((lat - (-90.0))/dlat)
#    return y
#  def lon2x(lon):
#    x = int((lon - (0.0))/dlat)
#    return x
#  #-----------
#  csy    = lat2y(cslat)
#  csx    = lon2x(cslon)
#  csxmin = lon2x(lllon)
#  csxmax = lon2x(urlon)
#  csymin = lat2y(lllat)
#  csymax = lat2y(urlat)
#  
#  da1v_x = {}
#  da1v_y = {}
#  
#  a1lon_dom = a1lon[csxmin:csxmax+1]
#  a1lat_dom = a1lat[csymin:csymax+1]
#
#  #--- horisontal -----------
#  plt.clf()
#  f, aax = plt.subplots(len(lplev)+1, sharex=True, figsize=(6,10))
#   
#  iplev = -1
#  for plev in lplev[::-1]:
#    iplev = iplev + 1
#    pos   = int("%d%d%d"%(len(lplev),1,iplev+1))
#    #-- value ------
#    a1v = da2loc[plev][csy]
#    da1v_x[plev] = a1v[csxmin:csxmax+1]
#    #
#    aax[iplev].plot(a1lon_dom, da1v_x[plev])
#    aax[iplev].plot([-1.0e+10, 1.0e+10],[0.0,0.0],color="gray" )
#    aax[iplev].set_ylim(-2, 2)
#    aax[iplev].set_xlim(a1lon_dom[0]-1, a1lon_dom[-1])
#    
#    #-- title for each axis --
#    aax[iplev].set_title("%d hPa"%(plev*0.01))
#    #text(3,3,"AAAAAA")
#    #-- ylabel ----
#    #aax[iplev].set_ylabel("abs.grad.of\nwet.bulb.theta\n(K/100km)")
#    aax[iplev].set_ylabel("(K (100km)-3")
# 
#  #- precip --
#  a1pr_dom = a2pr[csy][csxmin:csxmax+1]
#  aax[-1].plot(a1lon_dom,  a1pr_dom)
#  aax[-1].set_xlim(a1lon_dom[0]-1, a1lon_dom[-1])
#  aax[-1].set_ylim(0,60)
#  aax[-1].set_ylabel("precip\n(mm day-1)")
#  #-- title for precip --
#  aax[-1].set_title("surface precipitation")
#  #----------- 
#  #f.subplots_adjust(hspace=0.05)
#  #-- super title --
#  plt.suptitle("lat=%s"%(cslat))
#  #-- save -----
#  csname = sodir + "/cross_loc.%04d.%02d.%02d.%02d.lat.%s.%s.png"%(year, mon, day, hour, cslat, prtype)
#  f.savefig(csname)
#  print csname
#
#  #--- meridional -----------
#  plt.clf()
#  f, aax = plt.subplots(len(lplev)+1, sharex=True, figsize=(6,10))
#   
#  iplev = -1
#  for plev in lplev[::-1]:
#    iplev = iplev + 1
#    pos   = int("%d%d%d"%(len(lplev),1,iplev+1))
#    #
#    a1v = da2loc[plev][:,csx]
#    da1v_y[plev] = a1v[csymin:csymax+1]
#    #
#    aax[iplev].plot(a1lat_dom, da1v_y[plev])
#    aax[iplev].plot([-1.0e+10, 1.0e+10],[0.0,0.0],color="gray" )
#    aax[iplev].set_ylim(-2, 2)
#    aax[iplev].set_xlim(a1lat_dom[0]-1, a1lat_dom[-1])
#    
#    #-- title for each axis --
#    aax[iplev].set_title("%d hPa"%(plev*0.01))
#    #text(3,3,"AAAAAA")
#    #-- ylabel ----
#    #aax[iplev].set_ylabel("abs.grad.of\nwet.bulb.theta\n(K/100km)")
#    aax[iplev].set_ylabel("(K (100km)-3")
# 
#  #- precip --
#  a1pr_dom = a2pr[:,csx][csymin:csymax+1]
#  aax[-1].plot(a1lat_dom,  a1pr_dom)
#  aax[-1].set_xlim(a1lat_dom[0]-1, a1lat_dom[-1])
#  aax[-1].set_ylim(0,60)
#  aax[-1].set_ylabel("precip\n(mm day-1)")
#  #-- title for precip --
#  aax[-1].set_title("surface precipitation")
#  #----------- 
#  #f.subplots_adjust(hspace=0.05)
#  #-- super title --
#  plt.suptitle("lon=%s"%(cslon))
#  #-- save -----
#  csname = sodir + "/cross_loc.%04d.%02d.%02d.%02d.lon.%s.%s.png"%(year, mon, day, hour, cslon, prtype)
#  f.savefig(csname)
#  print csname
