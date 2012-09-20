from numpy import *

def fig_corr(a3in, latmin_g, latmax_g, lonmin_g, lonmax_g, dlat_g, dlon_g, ny_g, nx_g, latmin_l, latmax_l, lonmin_l, lonmax_l, latmin_s, lonmin_s, dlat_s, dlon_s, ny_s, nx_s, lat, lon):

  #-- matching latlon, n_orgiginal, n_compressed ----
  iname_pr   = "/media/disk2/data/aphro/DPREC/AphroJP_V1207_DPREC.1997"
  a2pr_temp  = fromfile(iname_pr, float32).reshape(365, ny_s, nx_s)[0]
  dnorg_ncomp = {}
  norg_s  = -1
  ncomp_s = -1
  for iy in range(ny_s):
    for ix in range(nx_s):
      norg_s  = norg_s + 1
      if a2pr_temp[iy, ix] >=0.0:
        ncomp_s = ncomp_s + 1
        dnorg_ncomp[norg_s] = ncomp_s
  
  def latlon2yx_l(lat, lon):
    print lat, lon
    x_l = int((lon - lonmin_l)/ dlon_g)
    y_l = int((lat - latmin_l)/ dlat_g)
    return (y_l, x_l)
  
  def latlon2ncomp_s(lat, lon):
    x_s = int((lon - lonmin_s)/ dlon_s)
    y_s = int((lat - latmin_s)/ dlat_s)
  
    norg_s  = y_s* nx_s + x_s
    #return y_s, x_s
    ncomp_s = dnorg_ncomp[norg_s]
    return ncomp_s
  #----------------------------------------
  from mpl_toolkits.basemap import Basemap
  import matplotlib.pyplot as plt
  
  #lat = 33.0
  #lon = 131.0
  (y_l, x_l)   = latlon2yx_l(lat, lon)
  ncomp_s      = latlon2ncomp_s( lat, lon)
  #a2in         = a3corr[ncomp_s]
  a2in         = a3in[ncomp_s]
  
  lats         = linspace(latmin_l, latmax_l, ny_l)
  lons         = linspace(lonmin_l, lonmax_l, nx_l)
  LONS, LATS   = meshgrid(lons, lats) 
  #



  #---------------
  # -- basemap
  #---------------
  figmap  = plt.figure()
  axmap   = figmap.add_axes([0, 0.1, 1.0, 0.8])
  M    = Basemap(resolution="l", llcrnrlat=latmin_l, llcrnrlon=lonmin_l, urcrnrlat=latmax_l, urcrnrlon=lonmax_l, ax=axmap)
  
  llevels      = arange(-1.0, 0.0, 0.1).tolist() + arange(0.1, 1.01, 0.1).tolist()
  lstyles      = ["dashed"]*10 + ["solid"]*10
  #llevels      = [-0.1, 0.0, 0.1]
  im           = M.contour(LONS,LATS, a2in, latlon=True, colors="k", levels=llevels, linestyles = lstyles) 
  #im           = M.imshow(a2in, origin="lower")
  plt.clabel(im, fontsize=9, inline=1)

 
  M.scatter(lon, lat, color="k", marker="^")
  
  M.drawcoastlines()

  #plt.colorbar(im)

  sodir        = "/media/disk2/out/MERRA/day/ctrack/corr/fig"
  soname       = sodir + "/MERRA.corr.pr.psl.%s.lat%06.3f.lon%06.3f.png"%(season, lat, lon)
  plt.savefig(soname)
  #plt.savefig("./temp.png")
  plt.clf()
  print soname


#***************************************************************
#def fig_corr_simple(lat, lon):

season     = "DJF"
lat        = 37.0
lon        = 138.0

#lat        = 34.0
#lon        = 136.0

ncomp_s    = 17145

latmin_g   = -89.375
lonmin_g   = -179.375

latmax_g   = 89.375
lonmax_g   = 179.375

dlat_g        = 1.25
dlon_g        = 1.25
nx_g          = 288
ny_g          = 144


#---- small domain -----------
latmin_s       = 24.0  + 0.025
lonmin_s       = 123.0 + 0.025
latmax_s       = 46.0  - 0.025
lonmax_s       = 146   - 0.025

dlat_s         = 0.05
dlon_s         = 0.05

nx_s           = 460
ny_s           = 440

#---- large domain -----------
latmin_l       = 15.0
latmax_l       = 75.0
lonmin_l       = 105.0
lonmax_l       = 160.0

ymin_l         = int((latmin_l + dlat_g*0.5 - latmin_g)/dlat_g)
ymax_l         = int((latmax_l + dlat_g*0.5 - latmin_g)/dlat_g)
xmin_l         = int((lonmin_l + dlon_g*0.5 - lonmin_g)/dlon_g)
xmax_l         = int((lonmax_l + dlon_g*0.5 - lonmin_g)/dlon_g)

ny_l           = ymax_l - ymin_l +1
nx_l           = xmax_l - xmin_l +1
#--------------------------------------

#-----------------------------
idir           = "/media/disk2/out/MERRA/day/ctrack/corr"
iname          = idir + "/MERRA.corr.pr.psl.%s.%s.bn"%(season, ncomp_s)
a3in           = fromfile(iname, float32).reshape(ncomp_s, ny_l, nx_l)

#-----------------------------
#-----------------------------
fig_corr(a3in, latmin_g, latmax_g, lonmin_g, lonmax_g, dlat_g, dlon_g, ny_g, nx_g, latmin_l, latmax_l, lonmin_l, lonmax_l, latmin_s, lonmin_s, dlat_s, dlon_s, ny_s, nx_s, lat, lon)



