from mpl_toolkits.basemap import Basemap
import ctrack_para
import ctrack_func as func
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
diyear  = {"his": iyear_his, "fut": iyear_fut}
deyear  = {"his": eyear_his, "fut": eyear_fut}
#***************************************
(imon, emon)  = ctrack_para.ret_im_em(season)
#***************************************
dexpr   = {"his": "historical", "fut": "rcp85"}
#***************************************
lera    = ["fut", "his"]
ldirvar = ["mw"]
laccvar = ["acc.mw"]
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
ddir_root["his"] = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d"%(model, dexpr["his"], ens, thdura, imon, emon, nclass, cmin )

ddir_root["fut"] = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d"%(model, dexpr["fut"], ens, thdura, imon, emon, nclass, cmin)

ddir_root["dif"] = "/media/disk2/out/CMIP5/day/%s/dif/%s/%04d-%04d.%04d-%04d/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d"%(model, dexpr["fut"], diyear["his"], deyear["his"], diyear["fut"], deyear["fut"], thdura, imon, emon, nclass, cmin)

#ddir_root["his"] = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/wfpr"%(model, dexpr["his"], ens, thdura)
#
#ddir_root["fut"] = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/wfpr"%(model, dexpr["fut"], ens, thdura)

#ddir_root["dif"] = "/media/disk2/out/CMIP5/day/%s/dif/%s/%04d-%04d.%04d-%04d/tracks/dura%02d/wfpr"%(model, dexpr["fut"], iyear_his, eyear_his, iyear_fut, eyear_fut, thdura)
#-----
ddir  = {}
dname = {}
for era in lera + ["dif"]:
  for var in ldirvar:
    #----
    ddir[era, var]  =  ddir_root[era] + "/%s"%(var)
    #---
    func.mk_dir(ddir[era, var])

#**********************
# names for each class
#----------------------
dname  = {}
for era in lera:
  expr = dexpr[era]
  for var in ldirvar:
    for iclass in lclass + [-1]:
      dname[era, var, iclass] =  ddir[era, var] + "/%s.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(var, xth, cmin, iclass, nclass, crad, nwbin, season, model, expr, ens )
#-----------
# names for acc
#-----------
for era in lera:
  expr  = dexpr[era]
  for var in ldirvar:
    for iclass in lclass[1:]:
      accvar = "acc."+var
      dname[era, accvar, iclass] = ddir[era, var] + "/%s.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(accvar, xth, cmin, iclass, nclass, crad, nwbin, season, model, expr, ens )
#**********************
# names for output
#----------------------
era    = "dif"
doname = {}
for dirvar in ldirvar:
  #----
  for iclass in lclass + [-1]: 
    odir                       =  ddir[era, dirvar]
    accvar                     =  "acc." + dirvar
    ltempvar                   = [dirvar, accvar]
    #-----
    for var in ltempvar:

      doname["dif", var, iclass] = odir +  "/dif.%s.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(var, xth, cmin, iclass, nclass, crad, nwbin, season, model, "historical", ens)

      doname["frac", var, iclass] = odir + "/frac.dif.%s.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(var, xth, cmin, iclass, nclass, crad, nwbin, season, model, "historical", ens)
#****************************************
da3in            = {}
#**********************
# read 
#----------------------
for var in ldirvar + laccvar:
  for iclass in lclass + [-1]:
    #----
    if ( var in laccvar )&( iclass in [-1, 0, 1, lclass[-1]]):
      continue 
    #----
    da3in["his"]     = fromfile( dname["his", var, iclass], float32)
    da3in["fut"]     = fromfile( dname["fut", var, iclass], float32)
    #-------------
    # calc 
    #-------------
    a3dif            = da3in["fut"] - da3in["his"]
    #----
    ## ! frac = dif / abs( his )
    #a3frac           = a3dif / ma.masked_equal( map( abs, da3in["his"]), 0.0)
    #a3frac           = a3frac.filled(0.0)
    
    #-- write --------------
    a3dif.tofile( doname["dif", var, iclass])
    #a3frac.tofile(doname["frac", var, iclass])

#*************************************
# draw picts
#-------------------------------------
#  read orography
#----------------------
orogdir_root = "/media/disk2/data/CMIP5/bn/orog/fx/%s/%s/r0i0p0"%(model, expr)
orogname     = orogdir_root + "/orog_fx_%s_%s_r0i0p0.bn"%(model, expr)
a2orog         = fromfile(orogname, float32).reshape(ny,nx)
#---------------
# colormap
#---------------
dcm  = {}
for var in ["mw", "acc.mw"]:
  dcm[var] = "RdBu"


for var in ["mw", "acc.mw"]:
  for era in lera:
    for iclass in lclass + [-1]:
      if ( var in laccvar) &(iclass in [0,1,-1, lclass[-1]]):
        continue
      #--
      #for vartype in ["dif", "frac"]:
      for vartype in ["dif"]:

        #-- prep for map -----
        figname = doname[vartype, var, iclass][:-3] + ".png"
        adat    = fromfile(doname[vartype, var, iclass], float32).reshape(nwbin, ny, nx)[0]
        adat    = ma.masked_where( a2orog >= thorog, adat)
        adat    = ma.masked_equal(adat, 0.0)
        # ! convert w -> -w
        adat    = -adat
        figmap  = plt.figure()
        axmap   = figmap.add_axes([0, 0, 1.0, 1.0])
        M       = Basemap(resolution="l", llcrnrlat=-90.0, llcrnrlon=0.0, urcrnrlat=90.0, urcrnrlon=360.0, ax=axmap)

        #-- prep for colorbar ---
        cbarname= figname[:-4] + ".cbar.png"
        figcbar = plt.figure(figsize=(1,5))
        axcbar  = figcbar.add_axes([0, 0, 0.4, 1.0])

        #------------------------
        if vartype == "frac": 
          im       = M.imshow(adat, origin="lower", vmin=-1.0, vmax=1.0)
        else: 
          bnd      = [-0.04, -0.03, -0.02, -0.01, 0.01, 0.02, 0.03, 0.04]
          bnd_cbar = [-1.0e+40] + bnd + [1.0e+40]

          im       = M.imshow(adat, origin="lower", norm=BoundaryNormSymm(bnd), cmap=dcm[var])
          stitle   = "%s (-1 x %s) c%02d, P:%s"%(vartype, var,iclass,  xth)
          axmap.set_title(stitle)

          figcbar.colorbar(im, boundaries = bnd_cbar, extend ="both", cax=axcbar)
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
        

