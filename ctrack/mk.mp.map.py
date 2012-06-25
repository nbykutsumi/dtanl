import ctrack_para
import ctrack_func as func
from numpy import *
import os, sys

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
#***************************************
diyear  = {"his": iyear_his, "fut": iyear_fut}
deyear  = {"his": eyear_his, "fut": eyear_fut}
#***************************************
dexpr   = {"his": "historical", "fut": "rcp85"}
#***************************************
lera    = ["fut", "his"]
lvar    = ["num", "sp", "mp"]
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
    if (var == "mp"):
      func.mk_dir(ddir[era, var])
#**********************
# names for each class
#----------------------
dname  = {}
for era in lera:
  expr = dexpr[era]
  for var in lvar:
    for iclass in lclass:
      dname[era, var, iclass] =  ddir[era, var] + "/%s.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(var, xth, iclass, nclass, crad, nwbin, season, model, expr, ens )
#****************************************
da3num  = {}
da3sp   = {}
da3mp   = {}

for era in lera:
  #**********************
  # read 
  #----------------------
  for iclass in lclass:
    print "iclass",iclass
    da3num[era, iclass]    = fromfile(dname[era, "num", iclass], float32).reshape(nwbin, ny, nx)
    da3sp[era, iclass]     = fromfile(dname[era, "sp",  iclass], float32).reshape(nwbin, ny, nx)
    #----------------------
    da3mp[era, iclass]     = da3sp[era, iclass] / ma.masked_equal( da3num[era, iclass], 0.0)
    da3mp[era, iclass]     = da3mp[era, iclass].filled(0.0)
    #----------------------
    # write
    #----------------------
    da3mp[era, iclass].tofile(dname[era, "mp", iclass])
    
