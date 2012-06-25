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

thorog = 1500.0
lcrad  = [500.0, 1000.0, 1500.0, 2000.0]
#lcrad  = [1000.0, 1500.0]
thdura = 24
xth    = 0.0
miss_dbl = -9999.0
iclass = 0
#-----------------------------------------------------
wline  = 3.0

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
for crad in lcrad:
  dspname[crad, iclass]  = spdir      + "/sp.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(xth, iclass, nclass, crad, nwbin, season, model, expr, ens)
#--------------
# num names
#--------------
numdir   = dir_root + "/num"
dnumname = {}
for crad in lcrad:
  dnumname[crad, iclass]  = numdir    + "/num.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(xth, iclass, nclass, crad, nwbin, season, model, expr, ens)

#**********************************************
# read data
#----------------------------------------------
# read sp
#-------------
da3sp = {}
for crad in lcrad:
  da3sp[crad, iclass]  = fromfile(dspname[crad, iclass], float32).reshape(nwbin, ny, nx)

#----------------------------------------------
# read num
#-------------
da3num = {}
for crad in lcrad:
  da3num[crad, iclass]  = fromfile(dnumname[crad, iclass], float32).reshape(nwbin, ny, nx)
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
  for crad in lcrad:
    da3sp_reg[crad, iclass]  = ma.masked_where(a3regionmask ==0.0, da3sp[crad, iclass])
  
  #-------------
  # num
  #-------------
  da3num_reg  = {}
  for crad in lcrad:
    da3num_reg[crad, iclass]  = ma.masked_where(a3regionmask == 0.0, da3num[crad, iclass])
  #**********************************************
  # calc mean precipitation intensity
  #----------------------------------------------
  lmp   = []
  for crad in lcrad:
    p   = da3sp_reg[crad, 0].sum() * 60.0*60.0*24.0
    n   = da3num_reg[crad, 0].sum()
    if ( n == 0):
      mp  = miss_dbl
    else:
      mp  = p / n
    #--------
    lmp.append(mp)
  #----
  ax   = ma.masked_where(array(mp) == miss_dbl, array(lcrad))
  amp = array( func.del_miss(lmp, miss_dbl))
    
  #**********************************************
  # output name
  #----------------------------------------------
  crad_mp_name = pictdir  + "/crad-mp.cmulti.p%05.2f.%s.%02d.png"%(xth, reg, nclass)
  
  #**********************************************
  # plot
  #----------------------------------------------
  plt.clf()
  plt.plot(ax, amp, lw = wline)
  #
  plt.ylim(0.0, amp.max()*1.2)
  plt.savefig(crad_mp_name)
  print crad_mp_name
  
  
  
  
