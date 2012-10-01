import calendar
import ctrack_para
import ctrack_func
import sys
from numpy import *
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from cf.plot import *
#**********************
iyear       = 2000
eyear       = 2000

tstp        = "6hr"
hinc        = 6
season      = "DJF"
nx          = 360
ny          = 180
nz          = 1
miss_in     = -9999.0
thorog      = 1500.0
thdura      = 0.0
#----------------------
lllat         = -90.0
lllon         = 0.0
urlat         = 90.0
urlon         = 360.0 

#----------------------
dgradrange    = ctrack_para.ret_dpgradrange()
[imon, emon]  = ctrack_para.ret_im_em(season)
lmon          = ctrack_para.ret_lmon(season)
mons          = ctrack_para.ret_mons(season)
dpgradrange   = ctrack_para.ret_dpgradrange()
cmin          = dpgradrange[0][0]
#----------------------
lclass        = dpgradrange.keys()
nclass        = len(lclass) -1

#***************************************
#  names for input
#---------------------------------------
pgrad_dir_root   = "/media/disk2/out/JRA25/sa.one/6hr/pgrad"

densdir          = "/media/disk2/out/JRA25/sa.one/const/cyclone/dura%02d"%(thdura)
ctrack_func.mk_dir(densdir)
#----------------------
# output name
#----------------------
ddensname    = {}
ddensname_up = {}
for iclass in lclass:
  ddensname[iclass]     = densdir + "/cdens.c%02d.%s.sa.one"%(iclass, season)
  ddensname_up[iclass]  = densdir + "/acc.cdens.c%02d.%s.sa.one"%(iclass, season)
  print ddensname[iclass]

#-----------------
# dummy
#-----------------
da2dens    = {}
da2dens_up = {}
for iclass in lclass:
  da2dens[iclass]    = zeros([ny, nx], float32)
  da2dens_up[iclass] = zeros([ny, nx], float32) 
#----
a2one   = ones( [ny, nx], float32)
#-----------------
for year in range( iyear, eyear+1):
  for mon in lmon:
    print year, mon
    #-------------
    # dir
    #-------------
    pgrad_dir    = pgrad_dir_root + "/%04d%02d"%(year, mon)
    ##############
    # no leap
    ##############
    if (mon==2)&(calendar.isleap(year)):
      eday = calendar.monthrange(year,mon)[1] -1
    else:
      eday = calendar.monthrange(year,mon)[1]
    #-------------
    for day in range(1, eday+1):
      for hour in [0, 6, 12, 18]:
        #----------------
        # input name
        #----------------
        stime      =  "%04d%02d%02d%02d"%(year, mon, day, hour)
        pgradname  =  pgrad_dir + "/pgrad.%s.sa.one"%(stime)
 
        #----------------
        a2pgrad    =  fromfile(pgradname, float32).reshape(ny, nx)

        for iclass in lclass:
          #------------
          pgrad_min   = dpgradrange[iclass][0]
          pgrad_max   = dpgradrange[iclass][1]
          #------------
          a2dens_temp = ma.masked_where(a2pgrad ==miss_in, a2one)
          a2dens_temp = ma.masked_where(a2pgrad < pgrad_min , a2dens_temp)
          a2dens_temp = ma.masked_where(pgrad_max <= a2pgrad, a2dens_temp)
          a2dens_temp = a2dens_temp.filled(0.0)

          da2dens[iclass] = da2dens[iclass] + a2dens_temp
          #------------
          a2dens_temp_up = ma.masked_where(a2pgrad ==miss_in, a2one)
          a2dens_temp_up = ma.masked_where(a2pgrad < pgrad_min, a2dens_temp_up)
          a2dens_temp_up = a2dens_temp_up.filled(0.0)
          da2dens_up[iclass] = da2dens_up[iclass] + a2dens_temp_up

#-------
da2dens_up[iclass] = da2dens_up[iclass]/ ( (eyear - iyear +1)*mons)
da2dens[iclass]    = da2dens[iclass]/ ( (eyear - iyear +1)*mons)
#-----------------------------------
for iclass in lclass:
  da2dens[iclass].tofile(ddensname[iclass])
  da2dens_up[iclass].tofile(ddensname_up[iclass])
  print ddensname[iclass] 
 
#  #-----------
#  # accmnum (cyclones /year)
#  #-----------
#  for iclass in lclass[1:]:
#    adat      = fromfile(daccmnumname[iclass], float32).reshape(nwbin, ny, nx)[0]
#    adat      = ma.masked_equal(adat, 0.0)
#    #- map -----------
#    figmap    = plt.figure()
#    axmap     = figmap.add_axes([0, 0, 1.0, 1.0])
#    M         = Basemap(resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
#    bnd       = list(arange(1,23+1, 2))
#    bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
#    im        = M.imshow(adat,  origin="lower", norm=BoundaryNormSymm(bnd))
#    M.drawcoastlines()
#  
#    stitle    = "cyclones/100*100km2/mon,  grad > %.0fhPa/1000km"%(cmin/100.)
#    axmap.set_title(stitle)
#  
#    figname  = daccmnumname[iclass][:-3] + ".png"
#    figmap.savefig(figname)
#    print figname
#  
#    #- colorbar ------
#    cbarname  = figname[:-4] + "_cbar.png"
#    figcbar   = plt.figure(figsize=(1, 6))
#    axcbar    = figcbar.add_axes([0.1, 0.1, 0.4, 0.8])
#    figcbar.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar) 
#    figcbar.savefig(cbarname)
#    #-----------------
#  
#    figmap.clf()
#    figcbar.clf()
