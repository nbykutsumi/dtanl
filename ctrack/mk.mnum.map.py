import ctrack_para
import ctrack_func
import sys
from numpy import *
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from cf.plot import *
#**********************
if (len(sys.argv) >1):
  model    = sys.argv[1]
  expr     = sys.argv[2]
  ens      = sys.argv[3]
  tstp     = sys.argv[4]
  hinc     = int(sys.argv[5])
  iyear    = int(sys.argv[6])
  eyear    = int(sys.argv[7])
  season   = sys.argv[8]
  nx       = int(sys.argv[9])
  ny       = int(sys.argv[10])
  nz       = int(sys.argv[11])
  miss_dbl = float(sys.argv[12])
  miss_int = int(sys.argv[13])
  crad     = float(sys.argv[14])
  thdura   = int(sys.argv[15])
  thorog   = float(sys.argv[16])
  iz500    = int(sys.argv[17])
  xth      = float(sys.argv[18])
  #---
else:
  model       = "NorESM1-M"
  #expr        = "rcp85"
  expr        = "historical"
  ens         = "r1i1p1"
  tstp        = "6hr"
  hinc        = 6
  iyear       = 1990
  eyear       = 1999
  season      = "DJF"
  nx          = 144
  ny          = 96
  nz          = 8
  miss_dbl    = -9999.0
  miss_int    = -9999
  crad        = 1000.0*1000.0
  thdura      = 24
  thorog      = 1500.0
  iz500       = 3
  xth         = 00.0
dnumname      = {}
dmnumname     = {}
daccmnumname  = {}
dspname       = {}
dsp2name      = {}
dswname       = {}
dsw2name      = {}

#----------------------
lllat         = -90.0
lllon         = 0.0
urlat         = 90.0
urlon         = 360.0 
#----------------------
[iy, ey]    = ctrack_para.ret_iy_ey(expr)
[im, em]    = ctrack_para.ret_im_em(season)
mons        = ctrack_para.ret_mons(season)
dpgradrange = ctrack_para.ret_dpgradrange()
cmin        = dpgradrange[0][0]
#----------------------
lclass      = dpgradrange.keys()
nclass      = len(lclass) -1
#----------------------
dlwbin  = ctrack_para.ret_dlwbin()
nwbin    = len(dlwbin.keys())
for i in dlwbin.keys():
  abin = array(dlwbin[i])*100.0/60.0/60.0/24.0
  dlwbin[i] = abin
#***************************************
#  names for input
#---------------------------------------
datadir     = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d"%(model, expr, ens, thdura, im, em, nclass, cmin)
outdir      = datadir
#
#ctrack_func.mk_dir(outdir)
#-----------
# number of events
#-----------
outdir_num = outdir + "/num"
ctrack_func.mk_dir(outdir_num)
if (dnumname =={}):
  dnumname  = {}
  for iclass in [-1] +lclass:
    dnumname[iclass ] = outdir_num + "/num.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad*0.001, nwbin, season, "day", model, expr, ens)

#-----------
# number of events , annual data
#-----------
for year in range(iy, ey+1):
  outdir_num_ann = outdir + "/num/%04d"%(year)
  ctrack_func.mk_dir(outdir_num_ann)
  for iclass in [-1] +lclass:
    dnumname[year, iclass ] = outdir_num_ann + "/num.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad*0.001, nwbin, season, "day", model, expr, ens)

#-----------
# mean number of events (events /year)
#-----------
outdir_mnum = outdir + "/mnum"
ctrack_func.mk_dir(outdir_mnum)
if (dmnumname =={}):
  dmnumname  = {}
  for iclass in [-1] +lclass:
    dmnumname[iclass ] = outdir_mnum + "/mnum.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad*0.001, nwbin, season, "day", model, expr, ens)
#-----------
# accumulated mean number of events (events /year)
#-----------
outdir_accmnum = outdir + "/mnum"
ctrack_func.mk_dir(outdir_accmnum)
if (daccmnumname =={}):
  daccmnumname  = {}
  for iclass in [-1] +lclass:
    daccmnumname[iclass ] = outdir_accmnum + "/acc.mnum.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad*0.001, nwbin, season, "day", model, expr, ens)

#-----------
# sum of precip
#-----------
outdir_sp = outdir + "/sp"
#ctrack_func.mk_dir(outdir_sp)
if (dspname =={}):
  dspname  = {}
  for iclass in [-1] +lclass:
    dspname[iclass ] = outdir_sp + "/sp.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad*0.001, nwbin, season, "day", model, expr, ens)
#-----------
# sum of w
#-----------
outdir_sw = outdir + "/sw"
#ctrack_func.mk_dir(outdir_sw)
if (dswname =={}):
  dswname  = {}
  for iclass in [-1] +lclass:
    dswname[iclass ] = outdir_sw + "/sw.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad*0.001, nwbin, season, "day", model, expr, ens)
#-----------

#**********************
#  read orography
#----------------------
orogdir_root = "/media/disk2/data/CMIP5/bn/orog/fx/%s/%s/r0i0p0"%(model, expr)
orogname     = orogdir_root + "/orog_fx_%s_%s_r0i0p0.bn"%(model, expr)
a2orog         = fromfile(orogname, float32).reshape(ny,nx)
##**********************
## read pxth data
##----------------------
#if xth != 0.0:
#  prxthdir = "/media/disk2/out/CMIP5/day/%s/%s/%s/prxth/%04d-%04d/%02d-%02d"%(model, expr, ens, iy, ey, im, em)
#  prxthname = prxthdir + "/prxth_day_%s_%s_%s_%06.2f.bn"%(model, expr, ens, xth)
#  a2prxth     = fromfile(prxthname, float32).reshape(ny, nx)

#-----------
# mnum:  Mean cyclone number  ( cyclones / mon)
#-----------
for iclass in lclass:
  mnum       = zeros( nx*ny*nwbin, float32).reshape(nwbin,ny,nx)
  for year in range(iy, ey+1):
    mnum     = mnum + fromfile(dnumname[year, iclass], float32).reshape(nwbin,ny,nx)
  #--
  mnum       = mnum / (ey - iy + 1) / mons
  mnum.tofile( dmnumname[iclass])
#-----------
# acc.mnum: Accumulated Mean cyclone number  ( cyclones / mon)
#-----------
for iclass in lclass[1:]:
  accmnum      = zeros(nx*ny*nwbin, float32).reshape(nwbin,ny,nx)
  for jclass in range(iclass, lclass[-1]+1):
    mnum       = fromfile( dmnumname[jclass], float32).reshape(nwbin, ny, nx)
    accmnum    = accmnum + mnum
  #--------
  accmnum.tofile(daccmnumname[iclass])

#**********************
# make lmon
#**********************
dlmon = {}
dlmon["DJF"] = [12, 1, 2]
dlmon["JJA"] = [6, 7, 8]
dlmon["ALL"] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
lmon = dlmon[season]
#****************************************************
# draw figure
#****************************************************
# basemap
#-----------
M      = Basemap(resolution = "l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon)

##-----------
## mnum (cyclones /year)
##-----------
#for iclass in lclass:
#  mnum      = fromfile(dmnumname[iclass], float32).reshape(nwbin, ny, nx)[0]
#  mnum      = ma.masked_equal(mnum, 0.0)
#  im       = M.imshow(mnum,  origin="lower", vmax=80.0)
#  M.drawcoastlines()
#  plt.colorbar()
#  figname  = dmnumname[iclass][:-3] + ".png"
#  plt.savefig(figname)
#  plt.clf()
#  print figname

#-----------
# accmnum (cyclones /year)
#-----------
for iclass in lclass[1:]:
  adat      = fromfile(daccmnumname[iclass], float32).reshape(nwbin, ny, nx)[0]
  adat      = ma.masked_equal(adat, 0.0)
  #- map -----------
  figmap    = plt.figure()
  axmap     = figmap.add_axes([0, 0, 1.0, 1.0])
  M         = Basemap(resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
  bnd       = list(arange(1,23+1, 2))
  bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
  im        = M.imshow(adat,  origin="lower", norm=BoundaryNormSymm(bnd), cmap="gist_ncar_r")
  M.drawcoastlines()

  stitle    = "cyclones/100*100km2/mon,  grad > %.0fhPa/1000km"%(cmin/100.)
  axmap.set_title(stitle)

  figname  = daccmnumname[iclass][:-3] + ".png"
  figmap.savefig(figname)
  print figname

  #- colorbar ------
  cbarname  = figname[:-4] + "_cbar.png"
  figcbar   = plt.figure(figsize=(1, 6))
  axcbar    = figcbar.add_axes([0.1, 0.1, 0.4, 0.8])
  figcbar.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar) 
  figcbar.savefig(cbarname)
  #-----------------

  figmap.clf()
  figcbar.clf()
