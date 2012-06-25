import ctrack_para
import ctrack_func as func
from numpy import *
import matplotlib.pyplot as plt

nx = 144
ny = 96
model  = "NorESM1-M"
expr   = "historical"
#expr   = "rcp85"
ens    = "r1i1p1"
season = "DJF"

thorog   = 1500.0
crad   = 1000.0
#crad   = 1500.0
thdura = 24

miss_dbl = -9999.0
#*****************************************************
wline    = 3.0

#*****************************************************
lonlatinfo     = ctrack_para.ret_lonlatinfo(model)
[lon_first, lat_first, dlon, dlat] = lonlatinfo
#
dpgradrange    = ctrack_para.ret_dpgradrange()
lclass         = dpgradrange.keys()
nclass         = len(lclass) -1
#
dlwbin         = ctrack_para.ret_dlwbin()
liw            = dlwbin.keys()
nwbin          = len(liw)

lxth   = [0.0, 50.0, 60.0, 70.0, 80.0, 90.0, 99.0]
#lxth   = [50.0, 70.0, 90.0, 99.0]
#*****************************************************

dir_root       = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/wfpr"%(model, expr, ens, thdura)
pictdir        = dir_root + "/pict/c%02dclasses"%(nclass)
func.mk_dir(pictdir)
#*****************************************************
#  read orography
#----------------------
orogdir_root = "/media/disk2/data/CMIP5/bn/orog/fx/%s/%s/r0i0p0"%(model, expr)
orogname     = orogdir_root + "/orog_fx_%s_%s_r0i0p0.bn"%(model, expr)
a2orog         = fromfile(orogname, float32).reshape(ny,nx)
#*****************************************************
# set region
#-----------------------------------------------------
dbound   = ctrack_para.ret_dbound()
lreg     = dbound.keys()

#**********************************************
# names
#----------------------------------------------
# sp names
#-------------
spdir   = dir_root + "/sp"
dspname = {}
for xth in lxth:
  for iclass in [-1] + lclass:
    dspname[xth, iclass]  = spdir      + "/sp.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(xth, iclass, nclass, crad, nwbin, season, model, expr, ens)
#--------------
# num names
#--------------
numdir   = dir_root + "/num"
dnumname = {}
for xth in lxth:
  for iclass in [-1] + lclass:
    dnumname[xth, iclass]  = numdir    + "/num.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(xth, iclass, nclass, crad, nwbin, season, model, expr, ens)

#**********************************************
# read data
#----------------------------------------------
# read sp
#-------------
da3sp = {}
for xth in lxth:
  for iclass in [-1, 0]:
    da3sp[xth, iclass]  = fromfile(dspname[xth, iclass], float32).reshape(nwbin, ny, nx)

#----------------------------------------------
# read num
#-------------
da3num = {}
for xth in lxth:
  for iclass in [-1, 0]:
    da3num[xth, iclass]  = fromfile(dnumname[xth, iclass], float32).reshape(nwbin, ny, nx)
#----------------------------------------------
#*****************************************************
# start reg loop
#-----------------------------------------------------
for reg in lreg:
  #*****************************************************
  # make region mask
  #*****************************************************
  [lat_min, lat_max, lon_min, lon_max] = dbound[reg]
  #--
  a2regionmask = func.mk_region_mask(lat_min, lat_max, lon_min, lon_max, nx, ny, lat_first, lon_first, dlat, dlon)
  a2regionmask = ma.masked_where(a2orog > thorog, a2regionmask).filled(0.0)
  #
  a3regionmask = zeros(nwbin* ny* nx).reshape(nwbin, ny, nx)
  for iw in liw:
    a3regionmask[iw] = a2regionmask

  #**********************************************
  # extract regional domain
  #----------------------------------------------
  # sp
  #-------------
  da3sp_reg  = {}
  for xth in lxth:
    for iclass in [-1,0]:
      da3sp_reg[xth, iclass]  = ma.masked_where(a3regionmask ==0.0, da3sp[xth, iclass])
  
  #-------------
  # num
  #-------------
  da3num_reg  = {}
  for xth in lxth:
    for iclass in [-1,0]:
      da3num_reg[xth, iclass]  = ma.masked_where(a3regionmask == 0.0, da3num[xth, iclass])
  #**********************************************
  # calc fractional cumulative precipitation
  #----------------------------------------------
  lfcp   = []
  for xth in lxth:
    sp   = da3sp_reg[xth, -1].sum()
    sp_c = da3sp_reg[xth, 0].sum() 
    if sp == 0.0:
      fcp  = miss_dbl
    else:
      fcp  = sp_c / sp
    #--------
    lfcp.append(fcp)
  #----
  ax   = ma.masked_where(array(lfcp) == miss_dbl, array(lxth))
  afcp = array( func.del_miss(lfcp, miss_dbl))
    
  #**********************************************
  # output name
  #----------------------------------------------
  xth_fcp_name = pictdir  + "/r%04d.xth-fcp.cmulti.%s.%02d.png"%(crad, reg, nclass)
  
  #**********************************************
  # plot
  #----------------------------------------------
  plt.clf()
  plt.plot(ax, afcp, lw = wline)
  #
  plt.ylim(0.0, 1.0)
  plt.savefig(xth_fcp_name)
  print xth_fcp_name
  
  
  
  
