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

mnum_min    = 1.0
#---------------------------------------
lats        = linspace(-90.0, 90.0, ny)
lons        = linspace(0.0, 360.0 - 360.0/nx, nx)
lllat       = -90.0
lllon       = 0.0
urlat       = 90.0
urlon       = 360.0
#
nnx         = int( (urlon - lllon)/ dlon)
nny         = int( (urlat - lllat)/ dlat)
#***************************************
diyear  = {"his": iyear_his, "fut": iyear_fut}
deyear  = {"his": eyear_his, "fut": eyear_fut}
#***************************************
(imon, emon)  = ctrack_para.ret_im_em(season)
#***************************************
dexpr   = {"his": "historical", "fut": "rcp85"}
#***************************************
lera    = ["fut", "his"]
lvar    = ["pap", "capep"]
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
#  read orography
#----------------------
orogdir_root = "/media/disk2/data/CMIP5/bn/orog/fx/%s/%s/r0i0p0"%(model, "historical")
orogname     = orogdir_root + "/orog_fx_%s_%s_r0i0p0.bn"%(model, "historical")
a2orog         = fromfile(orogname, float32).reshape(ny,nx)

#*******************************************************************
# dirs
#-------------------------
ddir_root        = {}
ddir_root["his"] = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d"%(model, dexpr["his"], ens, thdura, imon, emon, nclass, cmin )

ddir_root["fut"] = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d"%(model, dexpr["fut"], ens, thdura, imon, emon, nclass, cmin)

ddir_root["dif"] = "/media/disk2/out/CMIP5/day/%s/dif/%s/%04d-%04d.%04d-%04d/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d"%(model, dexpr["fut"], diyear["his"], deyear["his"], diyear["fut"], deyear["fut"], thdura, imon, emon, nclass, cmin)

#-----
ddir  = {}
dname = {}
for era in lera + ["dif"]:
  for var in lvar:
    #----
    ddir[era, var]  =  ddir_root[era] + "/%s"%(var)
    #---
    func.mk_dir(ddir[era, var])

#**********************
# names for input
#----------------------
dname    = {}
daccname = {}
for era in lera:
  expr = dexpr[era]
  for var in lvar:
    for iclass in lclass + [-1]:
      dname[era, var, iclass] =  ddir[era, var] + "/%s.p%05.2f.cmin%04d.c%02d.%02d.r%04d.%s_day_%s_%s_%s.bn"%(var, xth, cmin, iclass, nclass, crad, season, model, expr, ens )
      #---
      if iclass in lclass[2:]:
        daccname[era, var, iclass] =  ddir[era, var] + "/acc.%s.p%05.2f.cmin%04d.c%02d.%02d.r%04d.%s_day_%s_%s_%s.bn"%(var, xth, cmin, iclass, nclass, crad, season, model, expr, ens )
#**********************
# names for output
#----------------------
era    = "dif"
for var in lvar:
  #----
  for iclass in lclass + [-1]: 
    for var in lvar:
      odir   =  ddir[era, var]
      dname["dif", var, iclass] = odir +  "/dif.%s.p%05.2f.cmin%04d.c%02d.%02d.r%04d.%s_day_%s_%s_%s.bn"%(var, xth, cmin, iclass, nclass, crad, season, model, "historical", ens)
      daccname["dif", var, iclass] = odir +  "/dif.acc.%s.p%05.2f.cmin%04d.c%02d.%02d.r%04d.%s_day_%s_%s_%s.bn"%(var, xth, cmin, iclass, nclass, crad, season, model, "historical", ens)

#****************************************
da2in            = {}
#**********************
# read 
#----------------------
for acckey in ["T", "F"]:
  for var in lvar:
    for iclass in lclass + [-1]:
      #----
      if (acckey == "T")&(iclass not in lclass[2:]):
        continue 
      #----
      if acckey == "F":
        da2in["his"]     = fromfile( dname["his", var, iclass], float32)
        da2in["fut"]     = fromfile( dname["fut", var, iclass], float32)
      elif acckey == "T":
        da2in["his"]     = fromfile( daccname["his", var, iclass], float32)
        da2in["fut"]     = fromfile( daccname["fut", var, iclass], float32)
      #-------------
      # calc 
      #-------------
      a2dif            = da2in["fut"] - da2in["his"]
      #----
      if acckey   == "F":
        a2dif.tofile( dname["dif", var, iclass])
      elif acckey == "T":
        a2dif.tofile( daccname["dif", var, iclass])

#*************************************
# draw picts
#-------------------------------------
#  read orography
#----------------------
orogdir_root = "/media/disk2/data/CMIP5/bn/orog/fx/%s/%s/r0i0p0"%(model, expr)
orogname     = orogdir_root + "/orog_fx_%s_%s_r0i0p0.bn"%(model, expr)
a2orog         = fromfile(orogname, float32).reshape(ny,nx)
#---------------
mnumdir = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d/mnum"%(model, expr, ens, thdura, imon, emon, nclass, cmin)

for acckey in ["T", "F"]:
  for var in lvar:
    da2mnum_his   = {}
    for iclass in lclass + [-1]:
      #--------------
      if (acckey == "T")&(iclass not in lclass[2:]):
        continue
      #*************************************
      # read mnum
      #-------------------------------------
      print iclass

      if iclass == -1:
        da2mnum_his[iclass]  = ones([ny, nx], float32)*1.0e+10
      else:
        #-----
        if acckey   == "F":
          mnumname  = mnumdir + "/mnum.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad, nwbin, season, model, expr, ens)

        elif acckey == "T":
          mnumname  = mnumdir + "/acc.mnum.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad, nwbin, season, model, expr, ens)
        #-----
        da2mnum_his[iclass]  = fromfile(mnumname, float32).reshape(nwbin, ny, nx)[0]

      #-- prep for map -----
      if acckey   == "F":
        figname = dname["dif", var, iclass][:-3] + ".png"
      elif acckey == "T":
        figname = daccname["dif", var, iclass][:-3] + ".png"
      #--
      adat    = fromfile(dname["dif", var, iclass], float32).reshape(ny, nx)
      adat    = ma.masked_where( a2orog >= thorog, adat)
      adat    = ma.masked_equal(adat, 0.0)

      figmap  = plt.figure()
      axmap   = figmap.add_axes([0, 0, 1.0, 1.0])
  
      #--------------------- 
      M       = Basemap(resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
  
      #-- transform --------
      adat_trans   = M.transform_scalar(adat, lons, lats, nnx, nny)
      a2mask_trans = M.transform_scalar(da2mnum_his[iclass], lons, lats, nnx, nny)
  
      #-- prep for colorbar ---
      cbarname= figname[:-4] + ".cbar.png"
      figcbar = plt.figure(figsize=(1,5))
      axcbar  = figcbar.add_axes([0, 0, 0.3, 1.0])
  
      #------------------------
      im       = M.imshow(adat, origin="lower", vmin=-1.0, vmax=1.0, interpolation="nearest")
      bnd      = [-400, -200, -100, -50, -30, -20, -10, 0, 10, 20, 30, 50, 100, 200, 400]
      bnd_cbar = [-1.0e+40] + bnd + [1.0e+40]
  
      im       = M.imshow(adat_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap="RdBu", interpolation="nearest")
      stitle   = "dif %s (J/kg) c%02d P%f"%(var,iclass,  xth)
      axmap.set_title(stitle)
  
      figcbar.colorbar(im, boundaries = bnd_cbar, extend ="both", cax=axcbar)
      #-- superimpose shade(mask) -----
      cmshade = matplotlib.colors.ListedColormap([(0.8, 0.8, 0.8), (0.8, 0.8, 0.8)])
      ashade  = ma.masked_where(a2mask_trans > mnum_min, a2mask_trans)
      im      = M.imshow(ashade, origin="lower", cmap=cmshade, interpolation="nearest")
  
      #
      #--------
      M.drawcoastlines()
      figmap.savefig(figname)
      figmap.clf()
      print figname
      #-------- 
      figcbar.savefig(cbarname)
      #-------- 
      figcbar.clf() 
         
  
