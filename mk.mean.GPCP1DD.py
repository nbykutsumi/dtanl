from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from cf.plot import *
from numpy import *
import ctrack_para
import ctrack_func
import calendar
import sys

if len(sys.argv) >1:
  iyear = int(sys.argv[1])
  eyear = int(sys.argv[2])
  season= sys.argv[3] 
  lseason= [season]
else:
  iyear    = 2000
  eyear    = 2004
  lseason  = [1,2,3,4,5,6,7,8,9,10,11,12]

#-----------------
prtype   = "GPCP1DD"
ny       = 180
nx       = 360
miss_in  = -99999.
#-----------------
lllat    = -90.0
urlat    = 90.0
lllon    = 0.0
urlon    = 360.0

#-----------------
for season in lseason:
  #----
  if not season in ["DJF","MAM","JJA","SON","ALL"]:
    season = int(season)
  #----
  lmon     = ctrack_para.ret_lmon(season)
  #idir_root = "/media/disk2/data/GPCP1DD/data/1dd"
  idir_root = "/media/disk2/data/GPCP1DD/v1.2/1dd"
  sodir     = idir_root + "/mean"
  ctrack_func.mk_dir(sodir)
  soname = sodir + "/gpcp_1dd_v1.2_p1d.%04d-%04d.%s.bn"%(iyear, eyear,season)
  times  = 0
  a2out  = zeros([ny, nx], float32)
  for year in range(iyear, eyear+1):
    for mon in lmon:
      print year, mon
      eday  = calendar.monthrange(year, mon)[1]
      for day in range(1, eday+1):
        times  = times + 1
  
        symd   = "%04d%02d%02d"%(year, mon, day)
        idir   = idir_root + "/%04d"%(year)
        siname = idir + "/gpcp_1dd_v1.2_p1d.%s.bn"%(symd)
        a2in   = fromfile(siname, float32).reshape(ny, nx)
        a2in   = ma.masked_equal(a2in, miss_in).filled(0.0)
        a2out  = a2out + a2in
  #------------------------
  a2out  = a2out / times
  a2out.tofile(soname)
  print soname
  
  #--- figure -------
  a2dat     = fromfile(soname, float32).reshape(ny, nx)
  a2dat     = flipud(a2dat)
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
  parallels = 60.0
  M.drawmeridians(arange(0, 360.0 + 5.0, meridians), labels=[0, 0, 0, 1])
  M.drawparallels(arange(-90.0, 90.0+1, parallels), labels=[1, 0, 0, 0])

  #- title --
  stitle    = "%s %s"%(prtype, season)
  axmap.set_title(stitle)

  # save ---
  figname  = soname[:-3] + ".png"
  figmap.savefig(figname)
  print figname

  # prep for colorbar ---
  figcbar   = plt.figure(figsize=(5, 0.6))
  axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
  bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
  plt.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar, orientation="horizontal")

  cbarname  = soname[:-3] + ".cbar.png"
  figcbar.savefig(cbarname)
  #-------------------
  plt.clf()

