from mpl_toolkits.basemap import Basemap
import ctrack_para
import ctrack_func as func
import matplotlib
import matplotlib.pyplot as plt
from numpy import *
import os, sys
from cf.plot import *
#***************************************
iyear_his   = 1990
eyear_his   = 1999
iyear_fut   = 2086
eyear_fut   = 2095 
nx          = 144
ny          = 96
model       = "NorESM1-M"
ens         = "r1i1p1"
thdura      = 24
season      = "DJF"
lon_first   = 0.0
lat_first   = -90.0
dlon        = 2.5
dlat        = 1.8947368

xth         = 0.0
crad        = 1000.0
thorog      = 1500.0
#***************************************
# for mapping
lats        = linspace(-90.0, 90.0, ny)
lons        = linspace(0.0, 360.0 - 360.0/nx, nx)

lllat       = -90.0
lllon       = 0.0
urlat       = 90.0
urlon       = 360.0

meridians   = 30.0
parallels   = 30.0

nnx         = int( (urlon - lllon)/ dlon)
nny         = int( (urlat - lllat)/ dlat)
#***************************************
mnum_min    = 1.0
#***************************************
diyear  = {"his": iyear_his, "fut": iyear_fut}
deyear  = {"his": eyear_his, "fut": eyear_fut}
#***************************************
(imon, emon) = ctrack_para.ret_im_em(season)
#***************************************
dexpr   = {"his": "historical", "fut": "rcp85", "dif":"historical"}
expr = dexpr["his"]
#***************************************
lera    = ["fut", "his"]
ldirvar = ["xyz","nxyz"]
dlvar   = {}
dlvar["xyz"]  = ["dpdf_c", "dpdf_w", "dp_w"]
dlvar["nxyz"] = ["dnxyz", "ndpdf_c", "ndpdf_w", "ndp_w"]
#***************************************
# class
#-----------------------------
dpgradrange   = ctrack_para.ret_dpgradrange()
cmin          = dpgradrange[0][0]
lclass        = dpgradrange.keys()
nclass        = len(lclass) -1
#***************************************
# wbin
#-----------------------------
dlwbin        = ctrack_para.ret_dlwbin()
liw           = dlwbin.keys()
nwbin         = len(liw)
#***************************************
oekakidir     = "/home/utsumi/bin/dtanl/ctrack/oekaki"
#***************************************
#  read orography
#----------------------
orogdir_root = "/media/disk2/data/CMIP5/bn/orog/fx/%s/%s/r0i0p0"%(model, "historical")
orogname     = orogdir_root + "/orog_fx_%s_%s_r0i0p0.bn"%(model, "historical")
a2orog         = fromfile(orogname, float32).reshape(ny,nx)

#*******************************************************************
# dirs
#-------------------------
ddir_root        = {}

for era in ["his","fut"]:
  ddir_root[era] = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d"%(model, dexpr[era], ens, thdura, imon, emon, nclass, cmin )

ddir_root["dif"] = "/media/disk2/out/CMIP5/day/%s/dif/%s/%04d-%04d.%04d-%04d/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d"%(model, dexpr["fut"], diyear["his"], deyear["his"], diyear["fut"], deyear["fut"], thdura, imon, emon, nclass, cmin)

#-----

ddir  = {}
dname = {}
for era in ["his", "fut", "dif"]:
  for dirvar in ldirvar + ["mnum","mp","sp_season"]:
    #----
    ddir[era, dirvar]  =  ddir_root[era] + "/%s"%(dirvar)
    #---
    func.mk_dir(ddir[era, dirvar])

#**********************
# names for each class
#----------------------
dname  = {}
for dirvar in ldirvar:
  for var in dlvar[dirvar]:
    for iclass in lclass + [-1]:
      dname[dirvar, var, iclass] =  ddir[era, dirvar] + "/up.%s.p%05.2f.cmin%04d.up%02d.c00.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(var, xth, cmin, iclass, nclass, crad, nwbin, season, model, expr, ens )
#**********************
# name for various data
#----------------------
ddatname = {}
for era in lera+["dif"]:
  for var in ["mnum", "mp", "sp_season"]:
    for class_lb in lclass:
      ddatname[era, var, class_lb] =  ddir[era, var] + "/acc.%s.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(var, xth, cmin, class_lb, nclass, crad, nwbin, season, model, dexpr[era], ens )

#**********************
# names for output
#----------------------
era    = "dif"
doname = {}
for dirvar in ldirvar:
  #----
  for iclass in lclass[1:]: 
    odir   =  ddir[era, dirvar]
    #-----
    doname[dirvar, iclass] = odir +  "/up.sdscale.p%05.2f.cmin%04d.up%02d.c00.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad, nwbin, season, model, "historical", ens)

#****************************************
a3zero     = zeros([ny, nx], float32)
for dirvar in ldirvar:
  lvar             = dlvar[dirvar]
  da3in            = {}
  da3out           = {}
  print dirvar
  for iclass in lclass[1:]:
    #**********************
    # read 
    #----------------------
    for var in dlvar[dirvar]:
      da3in[var, iclass]  = fromfile(dname[dirvar, var, iclass], float32).reshape(ny, nx)
    #----------------------
    # calc
    #----------------------
    da3out["sum.scale", iclass] = a3zero
    for var in lvar:
      da3out["sum.scale", iclass] = da3out["sum.scale", iclass] + da3in[var, iclass]
    
    #-- write --------------
    da3out["sum.scale", iclass].tofile( doname[dirvar, iclass])
    #*************************************
    # read mnum
    #-----------------
    a2mnum  = fromfile(ddatname["his", "mnum", iclass], float32).reshape(nwbin, ny, nx)[0]


    
    #*************************************
    # draw picts
    #-------------------------------------
    a2mask    = a2mnum
    #--------------
    cm        = "RdBu"
    #--------------
    datname = doname[dirvar, iclass]
    figname = datname[:-3] + ".png"
    a       = fromfile(doname[dirvar, iclass], float32).reshape(ny, nx)
    a       = a* 60.0*60.0*24.0
    #--------
    a       = ma.masked_where( a2orog >= thorog, a)
    ##------------------------
    figmap  = plt.figure()
    axmap   = figmap.add_axes([0, 0.1, 1.0, 0.8])
    M       = Basemap(resolution = "l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
  
    # transform ---
    a_trans = M.transform_scalar(a, lons, lats, nnx, nny)
    a2mask_trans = M.transform_scalar(a2mask, lons, lats, nnx, nny)

    #-- mask mnum_his < xxxx-----
    #a_trans = ma.masked_where(a2mask_trans < mnum_min, a_trans)
    a_trans = ma.masked_invalid(a_trans)

    #--- prep for colorbar --
    cbarname  = datname[:-3] + "cbar.png"
    figcbar   = plt.figure(figsize=(1,5))
    axcbar    = figcbar.add_axes([0,0,0.4,1.0])

    #------------------------
    if dirvar in ["xyz"]:
      bnd     = [-3.0, -2.0, -1.0, -0.5, 0.5, 1.0, 2.0, 3.0]
    elif dirvar in ["nxyz"]:
      bnd     = [-90.0, -70.0, -50.0, -30.0, -10.0, 10.0, 30.0, 50.0, 70.0, 90.0]
    #------------------------
    im      = M.imshow(a_trans, origin ="lower", norm=BoundaryNormSymm(bnd), cmap=cm, interpolation="nearest")
    bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
    plt.colorbar(im, boundaries = bnd_cbar, extend="both", cax=axcbar)

    #-- superimpose shade(mask) -----
    cmshade   = matplotlib.colors.ListedColormap([(0.8, 0.8, 0.8), (0.8, 0.8, 0.8)])
    ashade    = ma.masked_where(a2mask_trans > mnum_min, a2mask_trans)
    im        = M.imshow(ashade, origin="lower", cmap=cmshade, interpolation="nearest")
    #-----
    stitle    = "dscale_%s up%02d nc%02d, P%s"%(dirvar, iclass, nclass,xth)
    axmap.set_title(stitle)
    M.drawcoastlines()

    # draw lat/lon grid lines
    #M.drawmeridians(arange(0,360,meridians),  labels=[0, 0, 0, 1])
    #M.drawparallels(arange(-90,90,parallels), labels=[1, 0, 0, 0])
    figmap.savefig(figname)
    print figname

    figcbar.savefig(cbarname)
    plt.clf()
  #----------------------

