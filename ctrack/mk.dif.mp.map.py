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
(imon, emon) = ctrack_para.ret_im_em(season)
#***************************************
dexpr   = {"his": "historical", "fut": "rcp85"}
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

ddir_root["dif"] = "/media/disk2/out/CMIP5/day/%s/dif/%s/%04d-%04d.%04d-%04d/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d"%(model, dexpr["fut"], diyear["his"], deyear["his"], diyear["fut"], deyear["fut"], thdura, imon, emon, nclass, cmin)

#-----
ddir  = {}
dname = {}
for era in ["dif"]:
  for var in ldirvar:
    #----
    ddir[era, var]  =  ddir_root[era] + "/%s"%(var)
    #---
    func.mk_dir(ddir[era, var])

#**********************
# names for each class
#----------------------
dname  = {}
for era in ["dif"]:
  expr = dexpr[era]
  for var in ldirvar:
    for iclass in lclass + [-1]:
      dname[era, var, iclass] =  ddir[era, var] + "/up.%s.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(var, xth, cmin, iclass, nclass, crad, nwbin, season, model, expr, ens )
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
    doname["xyz", iclass] = odir +  "/up.sdscale.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(var, xth, cmin, iclass, nclass, crad, nwbin, season, model, "historical", ens)

    doname["nxyz",iclass] = odir + "/up.sdnscale.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(var, xth, cmin, iclass, nclass, crad, nwbin, season, model, "historical", ens)
#****************************************
for dirvar in ldirvar:
  da3in            = {}
  #**********************
  # read 
  #----------------------
  for var in dlvar[dirvar]:
    for iclass in lclass + [-1]:
      #----
      #-------------
      # calc 
      #-------------
      a3dif            = da3in["fut"] - da3in["his"]
      #----
      a3frac           = ma.masked_where(da3in["his"]==0.0, a3dif) / da3in["his"]
      a3frac           = a3frac.filled(0.0)
      
      #-- write --------------
      a3dif.tofile( doname["dif", var, iclass])
      a3frac.tofile(doname["frac", var, iclass])
  
  #*************************************
  # draw picts
  #-------------------------------------
  #  read orography
  #----------------------
  orogdir_root = "/media/disk2/data/CMIP5/bn/orog/fx/%s/%s/r0i0p0"%(model, expr)
  orogname     = orogdir_root + "/orog_fx_%s_%s_r0i0p0.bn"%(model, expr)
  a2orog         = fromfile(orogname, float32).reshape(ny,nx)
  #---------------
  # -- basemap
  #---------------
  M    = Basemap(resolution="l", llcrnrlat=-90.0, llcrnrlon=0.0, urcrnrlat=90.0, urcrnrlon=360.0)
  #M    = Basemap(resolution="l", llcrnrlat=30.0, llcrnrlon=0.0, urcrnrlat=90.0, urcrnrlon=360.0)
  #---------------
  # colormap
  #---------------
  dcm  = {}
  for var in lvar:
    if var in lprvar:
      dcm[var] = "RdBu"
    elif var in ["mpgrad"]:
      dcm[var] = "RdBu"
    else:
      dcm[var] = "RdBu_r"
       
  #-------------------
  #for var in ["mp", "sp_season", "acc.mp", "acc.sp_season","cfrac.sp","acc.cfrac.sp", "cfrac.num", "acc.cfrac.num","mnum","acc.mnum"]:
  for var in ldirvar + laccvar:
    for era in lera:
      for iclass in lclass + [-1]:
        if ( var in laccvar) &(iclass in [0,1,-1, lclass[-1]]):
          continue
        if ( var in lfracvar) &(iclass in [-1]):
          continue
        if ( var in ["mnum", "acc.mnum"])&(iclass in [-1]):
          continue
        #--
        for vartype in ["dif", "frac"]:
          figname = doname[vartype, var, iclass][:-3] + ".png"
          adat    = fromfile(doname[vartype, var, iclass], float32).reshape(nwbin, ny, nx)[0]
          #--------
          if ( (var not in lfracvar) & (var not in ["mnum","acc.mnum","mpgrad"])):
            if vartype in ["dif"]:
              adat    = adat*60*60*24.0
          #--------
          adat    = ma.masked_where( a2orog >= thorog, adat)
          adat    = ma.masked_equal(adat, 0.0)
          #----
          if vartype == "frac":
            bnd     = [-0.6, -0.4, -0.2, -0.05, 0.05, 0.2 , 0.4 , 0.6]
            im      = M.imshow(adat, origin="lower", norm=BoundaryNormSymm(bnd), cmap=dcm[var])
            bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
            plt.colorbar(boundaries = bnd_cbar, extend="both")
  
          elif var in ["mp","acc.mp"]:
            bnd     = [-3.0, -2.0, -1.0, -0.5,  0.5 , 1.0, 2.0 , 3.0]
            im      = M.imshow(adat, origin="lower", norm=BoundaryNormSymm(bnd), cmap=dcm[var])
            bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
            plt.colorbar(boundaries = bnd_cbar, extend="both")
  
          elif var in ["mnum", "acc.mnum"]:           
            bnd     = [-9.0, -6.0, -3.0, -1.0, 1.0 , 3.0 , 6.0, 9.0]
            im      = M.imshow(adat, origin="lower", norm=BoundaryNormSymm(bnd), cmap=dcm[var])
            bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
            plt.colorbar(boundaries = bnd_cbar, extend="both")
  
          elif var in ["sp_season", "acc.sp_season"]:
            bnd     = [-50.0, -30.0, -10.0, -5.0, 5.0, 10.0, 30.0, 50.0]
            im      = M.imshow(adat, origin="lower", norm=BoundaryNormSymm(bnd), cmap=dcm[var])
            bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
            plt.colorbar(boundaries = bnd_cbar, extend="both")
          elif var in ["mpgrad"]:
            bnd       = range(-200, 200+1, 20)
            bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
            im      = M.imshow(adat, origin="lower", norm=BoundaryNormSymm(bnd), cmap=dcm[var])
            bnd_cbar  = bnd
            plt.colorbar(im, boundaries = bnd_cbar, extend="both")
          else:
            im      = M.imshow(adat, origin="lower")
            plt.colorbar()
            
          #
          M.drawcoastlines()
          plt.savefig(figname)
          print figname
          plt.clf()
          
          
  
  
