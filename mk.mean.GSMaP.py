from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.colors
from cf.plot import *
from numpy import *
import ctrack_para
import calendar
import gsmap_func

iyear    = 2001
eyear    = 2004
lseason   = ["DJF", "ALL"]
prtype   = "GSMaP"
lhour    = [0,3,6,9,12,15,18,21]
ny       = 120
nx       = 360
ny_glob  = 180
nx_glob  = 360
miss_in  = -9999.

lllat    = -60.0
urlat    = 60.0
lllon    = 0.0
urlon    = 360.0

for season in lseason:
  lmon     = ctrack_para.ret_lmon(season)
  idir_root = "/media/disk2/data/GSMaP/sa.one/3hr/ptot"
  soname = idir_root + "/gsmap_mvk.%04d-%04d.%s.sa.one"%(iyear, eyear,season)
  
  times  = 0
  
  a2out  = zeros([ny, nx], float32)
  #for year in range(iyear, eyear+1):
  #  for mon in lmon:
  #    print year, mon
  #    eday  = calendar.monthrange(year, mon)[1]
  #    for day in range(1, eday+1):
  #      for hour in lhour:
  #        times  = times + 1
  #
  #        symd   = "%04d%02d%02d"%(year, mon, day)
  #        idir   = idir_root + "/%04d%02d"%(year, mon)
  #        siname = idir + "/gsmap_mvk.3rh.%s.%02d00.v5.222.1.sa.one"%(symd, hour)
  #        a2in   = fromfile(siname, float32).reshape(ny, nx)
  #        a2in   = ma.masked_equal(a2in, miss_in).filled(0.0)
  #        a2out  = a2out + a2in
  ##------------------------
  #a2out  = a2out / times
  #a2out  = gsmap_func.gsmap2global_one(a2out, miss_in)
  #
  #a2out.tofile(soname)
  #print soname

  #--- figure -------
  a2dat     = fromfile(soname, float32).reshape(ny_glob, nx_glob)
  a2dat     = a2dat[30:150]
  a2dat     = a2dat * 60*60*24.0
  # basemap --
  figmap    = plt.figure()
  axmap     = figmap.add_axes([0.1, 0.1, 0.9, 0.8])
  M         = Basemap(resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap) 
  # boundaries --
  bnd       = [1,3,5,7,9,11,13,15]
  bnd_cbar  = [-1.0e+40] + [1,3,5,7,9,11,13,15] + [1.0e+40]
  
  # color --
  scm       = "jet_r"
  #scm       = "gist_ncar_r"

  # draw ---
  #im        = M.imshow(a2dat, origin="lower", norm=BoundaryNormSymm(bnd), extend="both", cmap="RdBu")
  im        = M.imshow(a2dat, origin="lower", norm=BoundaryNormSymm(bnd), cmap=scm)
  M.drawcoastlines()

  # meridians and parallels
  meridians = 60.0
  parallels = 30.0
  M.drawmeridians(arange(lllon, urlon + 5.0, meridians), labels=[0, 0, 0, 1])
  M.drawparallels(arange(lllat, urlat+1, parallels), labels=[1, 0, 0, 0])

  #- title --
  stitle    = "%s %s"%(prtype, season)
  axmap.set_title(stitle)
  
  # save ---
  figname  = soname[:-4] + ".png"
  figmap.savefig(figname)
  print figname

  # for colorbar ---
  figcbar   = plt.figure(figsize=(5, 0.6))
  axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
  bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
  plt.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar, orientation="horizontal")

  cbarname  = soname[:-4] + ".cbar.png"
  figcbar.savefig(cbarname)
  #-------------------
  plt.clf()

