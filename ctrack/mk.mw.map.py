from mpl_toolkits.basemap import Basemap
import ctrack_para
import ctrack_func as func
from numpy import *
import os, sys
import matplotlib.pyplot as plt
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
dexpr   = {"his": "historical", "fut": "rcp85"}
#***************************************
lera    = ["fut", "his"]
lvar    = ["num", "sw", "mw"]
laccvar = ["acc.mw"]
#***************************************
# season days
if season =="DJF":
  seasondays = 31 + 28 + 31
#***************************************
# class
#-----------------------------
dpgradrange   = ctrack_para.ret_dpgradrange()
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
ddir_root["his"] = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/wfpr"%(model, dexpr["his"], ens, thdura)

ddir_root["fut"] = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/wfpr"%(model, dexpr["fut"], ens, thdura)
#-----
ddir  = {}
dname = {}
for era in lera:
  for var in lvar:
    ddir[era, var]  =  ddir_root[era] + "/%s"%(var)
    if (var in ["mw"]):
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
      dname[era, var, iclass] =  ddir[era, var] + "/%s.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(var, xth, iclass, nclass, crad, nwbin, season, model, expr, ens )
#-----------
# names for acc
#-----------
for era in lera:
  expr  = dexpr[era]
  for var in lvar:
    for iclass in lclass[1:]:
      accvar = "acc."+var
      dname[era, accvar, iclass] = ddir[era, var] + "/%s.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(accvar, xth, iclass, nclass, crad, nwbin, season, model, expr, ens )
#****************************************
da3num           = {}
da3sw            = {}
da3mw            = {}
for era in lera:
  #**********************
  # read 
  #----------------------
  for iclass in lclass + [-1]:
    print "iclass",iclass
    da3num[era, iclass]       = fromfile(dname[era, "num", iclass], float32).reshape(nwbin, ny, nx)
    da3sw[era, iclass]        = fromfile(dname[era, "sw",  iclass], float32).reshape(nwbin, ny, nx)
  #**********************
  # calc
  #----------------------
  for iclass in lclass + [-1]:
    #--- mw: mean vartical velocity per cyclone-event, (mm / event) ---
    da3mw[era, iclass]        = da3sw[era, iclass] / ma.masked_equal( da3num[era, iclass], 0.0)
    da3mw[era, iclass]        = da3mw[era, iclass].filled(0.0)

    #----------------------
    # write
    #----------------------
    da3mw[era, iclass].tofile(dname[era, "mw", iclass])
    #--
#-------------
# accumulate precip of each class
#-------------
for var in lvar:
  #-----
  if var in ["num", "sw"]:
    continue
  #-----
  accvar  = "acc."+var
  for era in lera:
    for iclass in lclass[2:]:
      aacc_out    = zeros(nwbin*ny*nx, float32)
      asw_acc     = zeros(nwbin*ny*nx, float32)
      anum_acc    = zeros(nwbin*ny*nx, float32)
      #---
      for acc_class in range(iclass, lclass[-1]+1):
        asw   = fromfile(dname[era, "sw", acc_class], float32)
        anum  = fromfile(dname[era, "num", acc_class], float32)
        #
        asw_acc    = asw_acc  + asw
        anum_acc   = anum_acc + anum
      #
      if   var == "mw":
        aacc_out     = asw_acc / ma.masked_equal(anum_acc, 0.0)
      #---
      try:
        aacc_out     = aacc_out.filled(0.0)
      except AttributeError:
        pass
      #---
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
#-------------------
for var in ["mw", "acc.mw"]:
  for era in lera:
    for iclass in lclass + [-1]:
      if ( var in laccvar) &(iclass in [0,1,-1]):
        continue
      #--
      figname = dname[era, var, iclass][:-3] + ".png"
      adat    = fromfile(dname[era, var, iclass], float32).reshape(nwbin, ny, nx)[0]
      #--------
      adat    = ma.masked_where( a2orog >= thorog, adat)
      adat    = ma.masked_equal(adat, 0.0)
      #----
      plt.jet()
      im      = M.imshow(adat, origin="lower",vmin=-0.25, vmax=0.25)
        
      #
      M.drawcoastlines()
      plt.colorbar()
      plt.savefig(figname)
      print figname
      plt.clf()
      
      


