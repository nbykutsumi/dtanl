from mpl_toolkits.basemap import Basemap
import ctrack_para
import ctrack_func as func
import matplotlib.pyplot as plt
from numpy import *
import os, sys
from cf.plot import *
#***************************************
iyear_his   = 1980
eyear_his   = 1999
iyear_fut   = 2076
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

xth         = 00.0
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
lvar    = ["num", "sp", "mp","sp_season","cfrac.sp", "cfrac.num"]
laccvar = ["acc.mp", "acc.sp_season", "acc.cfrac.sp", "acc.cfrac.num"]
lfracvar= ["cfrac.sp", "cfrac.num", "acc.cfrac.sp","acc.cfrac.num"]
lallvar = list( set(lvar + laccvar + lfracvar) )
lprvar  = ["sp", "mp", "sp_season", "acc.mp", "acc.sp_season"]
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
#
#ddir_root["his"] = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/wfpr"%(model, dexpr["his"], ens, thdura)
#
#ddir_root["fut"] = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/wfpr"%(model, dexpr["fut"], ens, thdura)
#-----
ddir  = {}
dname = {}
for era in lera:
  for var in lvar:
    ddir[era, var]  =  ddir_root[era] + "/%s"%(var)
    if (var in ["mp", "sp_season", "cfrac.sp", "cfrac.num"]):
      func.mk_dir(ddir[era, var])
      print ddir[era, var]
#**********************
# names for each class
#----------------------
dname  = {}
for era in lera:
  expr = dexpr[era]
  for var in lvar:
    for iclass in lclass + [-1]:
      dname[era, var, iclass] =  ddir[era, var] + "/%s.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(var, xth, cmin, iclass, nclass, crad, nwbin, season, model, expr, ens )
#-----------
# names for acc
#-----------
for era in lera:
  expr  = dexpr[era]
  for var in lvar:
    for iclass in lclass[1:]:
      accvar = "acc."+var
      dname[era, accvar, iclass] = ddir[era, var] + "/%s.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(accvar, xth, cmin, iclass, nclass, crad, nwbin, season, model, expr, ens )
#****************************************
da3num           = {}
da3sp            = {}
da3mp            = {}
da3sp_season     = {}
da3cfrac_sp      = {}
da3cfrac_num     = {}
for era in lera:
  #**********************
  # read 
  #----------------------
  for iclass in lclass + [-1]:
    print "iclass",iclass
    da3num[era, iclass]       = fromfile(dname[era, "num", iclass], float32).reshape(nwbin, ny, nx)
    da3sp[era, iclass]        = fromfile(dname[era, "sp",  iclass], float32).reshape(nwbin, ny, nx)
  #**********************
  # calc
  #----------------------
  for iclass in lclass + [-1]:
    #--- mp: mean precip per cyclone-event, (mm / event) ---
    da3mp[era, iclass]        = da3sp[era, iclass] / ma.masked_equal( da3num[era, iclass], 0.0)
    da3mp[era, iclass]        = da3mp[era, iclass].filled(0.0)
    #--- sp_season: sum of precipitation conditioned on cyclone-event per season -----
    da3sp_season[era, iclass] = da3sp[era, iclass] / (deyear[era] - diyear[era] + 1) 
    #--- cfrac.sp  -----------
    if iclass != -1:
      da3cfrac_sp[era, iclass]     = da3sp[era, iclass] / ma.masked_equal( da3sp[era, -1], 0.0)
      da3cfrac_sp[era, iclass]     = da3cfrac_sp[era, iclass].filled(0.0)
    #--- cfrac.num -----------
    if iclass != -1:
      da3cfrac_num[era, iclass]    = da3num[era, iclass]/ ma.masked_equal( da3num[era, -1], 0.0)
      da3cfrac_num[era, iclass]    = da3cfrac_num[era, iclass].filled(0.0)


    #----------------------
    # write
    #----------------------
    da3mp[era, iclass].tofile(dname[era, "mp", iclass])
    da3sp_season[era, iclass].tofile(dname[era, "sp_season", iclass])
    #--
    if iclass == -1:
      continue
    #--
    da3cfrac_sp[era, iclass].tofile(dname[era, "cfrac.sp", iclass])
    da3cfrac_num[era, iclass].tofile(dname[era, "cfrac.num", iclass])
#-------------
# accumulate precip of each class
#-------------
for var in lvar:
  #-----
  if var in ["num", "sp"]:
    continue
  #-----
  accvar  = "acc."+var
  for era in lera:
    for iclass in lclass[2:]:
      aacc_out    = zeros(nwbin*ny*nx, float32)
      asp_acc     = zeros(nwbin*ny*nx, float32)
      anum_acc    = zeros(nwbin*ny*nx, float32)
      #---
      for acc_class in range(iclass, lclass[-1]+1):
        asp   = fromfile(dname[era, "sp", acc_class], float32)
        anum  = fromfile(dname[era, "num", acc_class], float32)
        #
        asp_acc    = asp_acc  + asp
        anum_acc   = anum_acc + anum
      #
      if   var == "mp":
        aacc_out     = asp_acc / ma.masked_equal(anum_acc, 0.0)
      elif var == "sp_season":
        aacc_out     = asp_acc / (deyear[era] - diyear[era] +1)
      elif var == "cfrac.sp":
        aacc_out     = asp_acc / ma.masked_equal( da3sp[era, -1].flatten(), 0.0)
      elif var == "cfrac.num":
        aacc_out     = anum_acc/ ma.masked_equal( da3num[era, -1].flatten(), 0.0)
      #---
      try:
        aacc_out     = aacc_out.filled(0.0)
      except AttributeError:
        pass
      #
      aacc_out.tofile(dname[era, accvar, iclass])

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
#---------------
dcm = {}
for var in lallvar:
  if var in lprvar:
    dcm[var]  = "jet_r"
    #dcm[var]  = "BuPu"
  else:
    dcm[var]  = "jet"
    #dcm[var]  = "BuPu_r"

#-------------------
for var in ["mp", "sp_season", "acc.mp", "acc.sp_season","cfrac.sp","acc.cfrac.sp", "cfrac.num", "acc.cfrac.num"]:
  for era in lera:
    for iclass in lclass + [-1]:
      if ( var in laccvar) &(iclass in [0,1,-1]):
        continue
      if ( var in lfracvar) &(iclass in [-1]):
        continue
      #--
      figname = dname[era, var, iclass][:-3] + ".png"
      adat    = fromfile(dname[era, var, iclass], float32).reshape(nwbin, ny, nx)[0]
      #--------
      if not (var in lfracvar):
        adat    = adat*60*60*24.0
      #--------
      adat    = ma.masked_where( a2orog >= thorog, adat)
      adat    = ma.masked_equal(adat, 0.0)
      #----
      if var in ["mp", "acc.mp"]:
        bnd       = range(1, 15, 1)
        vvmin      = bnd[0]
        adat      = ma.masked_less(adat, vvmin)
        im        = M.imshow(adat, origin="lower", norm=BoundaryNormSymm(bnd), cmap=dcm[var] )
        bnd_cbar  = bnd + [1.0e+40]
        plt.colorbar(boundaries = bnd_cbar, extend="max")

      elif var in ["sp_season", "acc.sp_season"]:
        bnd       = range(0,360+10, 20)
        vvmin     = bnd[0]
        adat      = ma.masked_less(adat, vvmin)
        im        = M.imshow(adat, origin="lower", norm=BoundaryNormSymm(bnd), cmap=dcm[var] )
        bnd_cbar  = bnd + [1.0e+40]
        plt.colorbar(boundaries = bnd_cbar, extend="max")

      elif var in lfracvar:
        bnd       = arange(0, 1.0 + 0.01, 0.1)
        vvmin     = bnd[0]
        adat      = ma.masked_less(adat, vvmin)
        im        = M.imshow(adat, origin="lower", norm=BoundaryNormSymm(bnd), cmap=dcm[var] , interpolation="nearest")
        bnd_cbar  = bnd
        plt.colorbar(boundaries = bnd_cbar)
      else:
        im      = M.imshow(adat, origin="lower")
        
      #
      M.drawcoastlines()
      plt.savefig(figname)
      print figname
      plt.clf()
      
      


