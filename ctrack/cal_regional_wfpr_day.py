import ctrack_para
import ctrack_func as func
from numpy import *
import matplotlib
import matplotlib.pyplot as plt
#**************************************
tstp  = "day"
model = "NorESM1-M"
expr  = "historical"
ens   = "r1i1p1"
nx    = 144
ny    = 96
crad  = 1000
#crad  = 1500
season = "DJF"
lon_first = -180.0
lat_first = -90.0
dlon     = 2.5
dlat     = 1.8947368
thorog   = 1500.0
thdura   = 24

miss_dbl = -9999.0
#**************************************
dpgradrange = ctrack_para.ret_dpgradrange()
lclass      = dpgradrange.keys()
nclass      = len(lclass)
#
dlwbin      = ctrack_para.ret_dlwbin()
liw         = dlwbin.keys()
nwbin       = len(liw)
#
#lxth        = ctrack_para.ret_lxth
lxth        = [50.0, 70.0]
#**************************************
dir_root = "/media/disk2/out/CMIP5/%s/%s/%s/%s/tracks/dura%02d/wfpr"%(tstp, model, expr, ens, thdura)
pictdir = dir_root + "/pict/c%02dclasses"%(nclass)
numdir = dir_root + "/num"
spdir  = dir_root + "/sp"
sp2dir = dir_root + "/sp2"
swdir  = dir_root + "/sw"
sw2dir = dir_root + "/sw2"
#
func.mk_dir(pictdir)
#**************************************
#--------------------
# make lwvalue
#--------------------
lwbin = []
for iw in liw:
  lwbin.append(mean(dlwbin[iw]))
#
lwbin[0]  = -9999.0
lwbin[1]  = lwbin[2]  - (lwbin[3] - lwbin[2])
lwbin[-1] = lwbin[-2] + (lwbin[3] - lwbin[2])
#*****************************************************
# FUNCTIONS
#*****************************************************
def mk_region_mask(lat_min, lat_max, lon_min, lon_max, nx, ny, lat_first, lon_first, dlat, dlon):
  #--- xmin ----------
  if (lon_first <= lon_min):
    xmin = int( (lon_min - lon_first + dlon*0.5) /dlon)
  else:
    if ( (lon_min - lon_first + dlon*0.5)%dlon == 0.0):
      xmin = int((lon_min - lon_first + dlon *0.5)/dlon)
    else:
      xmin = int((lon_min - lon_first + dlon *0.5)/dlon) -1
  #--- xmax ----------
  if (lon_first <= lon_max):
    if ( (lon_max - lon_first + dlon*0.5)%dlon == 0.0):
      xmax = int( (lon_max - lon_first + dlon*0.5) /dlon) -1
    else:
      xmax = int( (lon_max - lon_first + dlon*0.5) /dlon)
  else:
    xmax = int((lon_max - lon_first + dlon *0.5)/dlon) -1
  #--- ymin ----------
  if (lat_first <= lat_min):
    ymin = int( (lat_min - lat_first + dlat*0.5) /dlat)
  else:
    if ( (lat_min - lat_first + dlat*0.5)%dlat == 0.0):
      ymin = int((lat_min - lat_first + dlat *0.5)/dlat)
    else:
      ymin = int((lat_min - lat_first + dlat *0.5)/dlat) -1
  #--- ymax ----------
  if (lat_first <= lat_max):
    if ( (lat_max - lat_first + dlat*0.5)%dlat == 0.0):
      ymax = int( (lat_max - lat_first + dlat*0.5) /dlat) -1
    else:
      ymax = int( (lat_max - lat_first + dlat*0.5) /dlat)
  else:
    ymax = int((lat_max - lat_first + dlat *0.5)/dlat) -1
  #-----------
  a2regionmask  = zeros(nx*ny).reshape(ny, nx)
  if ( ( xmin >= 0 ) and (xmax >= 0)):
    a2regionmask[ymin:ymax+1, xmin:xmax+1] = 1.0
  elif ( ( xmin < 0) and (xmax >= 0) ):
    a2regionmask[ymin:ymax+1, nx + xmin: nx] = 1.0
    a2regionmask[ymin:ymax+1, 0:xmax+1] = 1.0
  else:
    a2regionmask[ymin:ymax+1, nx + xmin: nx + xmax +1] = 1.0
  return a2regionmask

#*****************************************************
#  read orography
#----------------------
orogdir_root = "/media/disk2/data/CMIP5/bn/orog/fx/%s/%s/r0i0p0"%(model, expr)
orogname     = orogdir_root + "/orog_fx_%s_%s_r0i0p0.bn"%(model, expr)
a2orog         = fromfile(orogname, float32).reshape(ny,nx)
#*****************************************************
# make region mask
#*****************************************************
#lat_min  = 30.0
#lat_max  = 45.0
#lon_min  = -120
#lon_max  = -40

lat_min  = 20.0
lat_max  = 50.0
lon_min  = 20
lon_max  = 80



#--
a2regionmask = mk_region_mask(lat_min, lat_max, lon_min, lon_max, nx, ny, lat_first, lon_first, dlat, dlon)
a2regionmask = ma.masked_where(a2orog > thorog, a2regionmask).filled(0.0)
#
a3regionmask = zeros(nwbin* ny* nx).reshape(nwbin, ny, nx)
for iw in liw:
  a3regionmask[iw] = a2regionmask
#**************************************
# names
#--------------------------------------
# name for num
#-------------------
dnumname = {}
#for iclass in lclass:
for iclass in [-1] + lclass:
  dnumname[iclass] = numdir + "/num.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, iclass, nclass, crad, nwbin, season, tstp, model, expr, ens)
#-------------------
# name for sp
#-------------------
dspname = {}
#for iclass in lclass:
for iclass in [-1] + lclass:
  dspname[iclass] = spdir + "/sp.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, iclass, nclass, crad, nwbin, season, tstp, model, expr, ens)
#-------------------
# name for sp2
#-------------------
dsp2name = {}
#for iclass in lclass:
for iclass in [-1] + lclass:
  dsp2name[iclass] = sp2dir + "/sp2.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, iclass, nclass, crad, nwbin, season, tstp, model, expr, ens)
#-------------------
# name for sw
#-------------------
dswname = {}
#for iclass in lclass:
for iclass in [-1] + lclass:
  dswname[iclass] = swdir + "/sw.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, iclass, nclass, crad, nwbin, season, tstp, model, expr, ens)
#-------------------
# name for sw2
#-------------------
dsw2name = {}
#for iclass in lclass:
for iclass in [-1] + lclass:
  dsw2name[iclass] = sw2dir + "/sw2.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, iclass, nclass, crad, nwbin, season, tstp, model, expr, ens)

#**************************************
# read data
#--------------------------------------
# read num
#-----------------
da3num   = {}
#for iclass in lclass:
for iclass in [-1] + lclass:
  da3num[iclass] = fromfile(dnumname[iclass], float32).reshape(nwbin, ny, nx)
#-----------------
# read sp
#-----------------
da3sp   = {}
#for iclass in lclass:
for iclass in [-1] + lclass:
  da3sp[iclass] = fromfile(dspname[iclass], float32).reshape(nwbin, ny, nx)
#-----------------
# read sp2
#-----------------
da3sp2   = {}
#for iclass in lclass:
for iclass in [-1] + lclass:
  da3sp2[iclass] = fromfile(dsp2name[iclass], float32).reshape(nwbin, ny, nx)
#-----------------
# read sw
#-----------------
da3sw   = {}
#for iclass in lclass:
for iclass in [-1] + lclass:
  da3sw[iclass] = fromfile(dswname[iclass], float32).reshape(nwbin, ny, nx)
#-----------------
# read sw2
#-----------------
da3sw2   = {}
#for iclass in lclass:
for iclass in [-1] + lclass:
  da3sw2[iclass] = fromfile(dsw2name[iclass], float32).reshape(nwbin, ny, nx)

#**************************************
# mask
#--------------------------------------
# for num
#---------
da3num_reg = {}
#for iclass in lclass:
for iclass in [-1] + lclass:
  da3num_reg[iclass] = ma.masked_where(a3regionmask ==0.0, da3num[iclass])
#---------
# for sp
#---------
da3sp_reg = {}
#for iclass in lclass:
for iclass in [-1] + lclass:
  da3sp_reg[iclass] = ma.masked_where(a3regionmask ==0.0, da3sp[iclass])
#---------
# for sp2
#---------
da3sp2_reg = {}
#for iclass in lclass:
for iclass in [-1] + lclass:
  da3sp2_reg[iclass] = ma.masked_where(a3regionmask ==0.0, da3sp2[iclass])
#---------
# for sw
#---------
da3sw_reg = {}
#for iclass in lclass:
for iclass in [-1] + lclass:
  da3sw_reg[iclass] = ma.masked_where(a3regionmask ==0.0, da3sw[iclass])
#---------
# for sw2
#---------
da3sw2_reg = {}
#for iclass in lclass:
for iclass in [-1] + lclass:
  da3sw2_reg[iclass] = ma.masked_where(a3regionmask ==0.0, da3sw2[iclass])

#**************************************
# regional num
#--------------------------------------
dlnum = {}
anum_reg = zeros(nclass*nwbin).reshape(nclass, nwbin)
#for iclass in lclass:
for iclass in [-1] + lclass:
  dlnum[iclass] = []
  for iw in liw:
    num = da3num_reg[iclass][iw].sum() 
    dlnum[iclass].append(num)
    anum_reg[iclass, iw] = num
#--------------------------------------    
# regional sp
#--------------------------------------
dlsp  = {}
asp_reg = zeros(nclass*nwbin).reshape(nclass, nwbin)
#for iclass in lclass:
for iclass in [-1] + lclass:
  dlsp[iclass] = []
  for iw in liw:
    sp  = da3sp_reg[iclass][iw].sum()
    dlsp[iclass].append(sp)
    asp_reg[iclass, iw] = sp
#--------------------------------------    
# regional sp2
#--------------------------------------
dlsp2  = {}
#for iclass in lclass:
for iclass in [-1] + lclass:
  dlsp2[iclass] = []
  for iw in liw:
    sp2  = da3sp2_reg[iclass][iw].sum()
    dlsp2[iclass].append(sp2)
#--------------------------------------    
# regional sw
#--------------------------------------
dlsw  = {}
#for iclass in lclass:
for iclass in [-1] + lclass:
  dlsw[iclass] = []
  for iw in liw:
    sw  = da3sw_reg[iclass][iw].sum()
    dlsw[iclass].append(sw)
#--------------------------------------    
# regional sw2
#--------------------------------------
dlsw2  = {}
#for iclass in lclass:
for iclass in [-1] + lclass:
  dlsw2[iclass] = []
  for iw in liw:
    sw2  = da3sw2_reg[iclass][iw].sum()
    dlsw2[iclass].append(sw2)

#**************************************
# calc average intensity
#--------------------------------------
# precip intensity
#----------------
dlp    = {}
for iclass in lclass:
  dlp[iclass] = range(nwbin)
  for iw in liw:
    if dlnum[iclass][iw] == 0.0:
      dlp[iclass][iw] = miss_dbl
    else:
      dlp[iclass][iw] = dlsp[iclass][iw] / dlnum[iclass][iw]
#
ap = zeros(nclass*nwbin).reshape(nclass, nwbin)
for iclass in lclass:
  for iw in liw:
    ap[iclass, iw] = dlp[iclass][iw]
#----------------
# w intensity
#----------------
dlw   = {}
for iclass in lclass:
  dlw[iclass]  = range(nwbin)
  for iw in liw:
    if dlnum[iclass][iw]  == 0.0:
      dlw[iclass][iw]  = miss_dbl
    else:
      dlw[iclass][iw]  = dlsw[iclass][iw] / dlnum[iclass][iw]

#
aw = zeros(nclass*nwbin).reshape(nclass, nwbin)
for iclass in lclass:
  for iw in liw:
    aw[iclass, iw] = dlw[iclass][iw]
#--------------------------------------
# calc relative frequency
#--------------------------------------
dlrnum   = {}
for iclass in lclass:
  dlrnum[iclass] = range(nwbin)
  snum  = sum(dlnum[iclass])
  for iw in liw:
    if snum == 0.0:
      dlrnum[iclass][iw] = miss_dbl
    else:
      dlrnum[iclass][iw] = dlnum[iclass][iw] / snum
#**************************************
# calc sigma
#--------------------------------------
# sigma precip
#----------------
dlsig_p = {}
for iclass in lclass:
  dlsig_p[iclass] = range(nwbin)
  for iw in liw:
    n = dlnum[iclass][iw]
    if n == 0.0:
      sig = miss_dbl
    else:
      sx2 = dlsp2[iclass][iw] 
      mx  = dlp[iclass][iw]
      sig = sqrt( (sx2 - n*mx*mx)/n )
    #
    dlsig_p[iclass][iw] = sig
#
asig_p = zeros(nclass*nwbin).reshape(nclass, nwbin)
for iclass in lclass:
  for iw in liw:
    asig_p[iclass, iw] = dlsig_p[iclass][iw]


#----------------
# sigma omega
#----------------
dlsig_w = {}
for iclass in lclass:
  dlsig_w[iclass] = range(nwbin)
  for iw in liw:
    n = dlnum[iclass][iw]
    if n == 0.0:
      sig = miss_dbl
    else:
      sx2 = dlsw2[iclass][iw]
      mx  = dlw[iclass][iw]
      sig = sqrt( (sx2 - n*mx*mx)/n )
    #
    dlsig_w[iclass][iw] = sig
#
asig_w = zeros(nclass*nwbin).reshape(nclass, nwbin)
for iclass in lclass:
  for iw in liw:
    asig_w[iclass, iw] = dlsig_w[iclass][iw]
#**************************************
# make pict
#**************************************
if xth in [0.0]:
  #-----------------
  # c-p
  #-----------------
  plt.clf()
  c_p_name = pictdir  + "/p%05.2f.r%04d.c.p.cn%02d.png"%(xth, crad, nclass)
  lx  = lclass[1:]
  ly  = ap[1:,0]
  #
  plt.plot(lx, ly)
  #
  ye  = asig_p[1:,0]
  plt.errorbar(lx, ly, yerr = ye)
  plt.xlim(0, nclass)
  #
  plt.savefig(c_p_name)
  #-----------------
  # c-rp
  #-----------------
  plt.clf()
  c_rp_name = pictdir  + "/p%05.2f.r%04d.c.rp.cn%02d.png"%(xth, crad, nclass)
  #--
  sp  = sum(dlsp[-1])
  lx  = array(lclass[1:])
  ly  = sum(asp_reg[1:], axis=1) / sp
  plt.bar(lx-0.5, ly)
  #---
  lcrp = []  # cumulative relative precipitation
  cp = 0.0
  for iclass in lclass[1:]:
    cp = cp + sum(asp_reg[iclass])
    lcrp.append(cp)
  lcrp = lcrp / sp
  plt.plot(lx, lcrp)
  #---
  plt.xlim(0, nclass)
  plt.savefig(c_rp_name)
  #-----------------
  # c-w 
  #-----------------
  plt.clf()
  c_w_name = pictdir  + "/p%05.2f.r%04d.c.w.cn%02d.png"%(xth, crad, nclass)
  lx  = lclass[1:]
  ly  = -1.0*aw[1:,0]
  #
  plt.plot(lx, ly)
  #
  ye  = asig_w[1:, 0]
  plt.errorbar(lx, ly, yerr = ye)
  plt.xlim(0, nclass)
  #
  plt.savefig(c_w_name)
  #-----------------
  # c-n
  #-----------------
  plt.clf()
  c_n_name = pictdir  + "/p%05.2f.r%04d.c.n.cn%02d.png"%(pxth, crad, nclass)
  lx  = lclass[1:]
  ly  = sum(anum_reg, axis=1)[1:]
  #-
  plt.plot(lx, ly)
  #
  plt.xlim(0, nclass)
  #
  plt.savefig(c_n_name)
  print c_n_name
  #-----------------
  # c-rn
  #-----------------
  plt.clf()
  c_rn_name = pictdir  + "/p%05.2f.r%04d.c.rn.cn%02d.png"%(xth, crad, nclass)
  lx  = lclass[1:]
  ly  = (sum(anum_reg, axis=1)/anum_reg.sum())[1:]
  #-
  plt.plot(lx, ly)
  #
  plt.xlim(0, nclass)
  #
  plt.savefig(c_rn_name)
  print c_rn_name
  #-----------------
  # w-p 
  #-----------------
  #for iclass in lclass:
  for iclass in [0]:
    plt.clf()
    w_p_name = pictdir  + "/p%05.2f.r%04d.w.p.c%02d.%02d.png"%(xth, crad, iclass,nclass)
    #
    ly  = ap[iclass][1:]
    #lx  = -ma.masked_equal(aw[iclass][1:], miss_dbl).filled(-miss_dbl)
    lx  = ma.masked_where(ly ==miss_dbl, lwbin[1:]).filled(miss_dbl)
    lye = asig_p[iclass][1:]
    #
    #
    lx  = func.del_miss(lx,  miss_dbl)
    ly  = func.del_miss(ly,  miss_dbl)
    lye = func.del_miss(lye, miss_dbl)
    #
    plt.plot(lx, ly)
    ##
    plt.errorbar(lx, ly, yerr = lye)
    ##
    plt.savefig(w_p_name)
  #-----------------------------
  # put all into one figure
  #-----------
  plt.clf()
  dplt = {}
  w_p_name = pictdir  + "/p%05.2f.r%04d.w.p.cmulti.%02d.png"%(xth, crad, nclass)
  for iclass in lclass[1:]:
    #
    ly  = ap[iclass][1:]
    #lx  = -ma.masked_equal(aw[iclass][1:], miss_dbl).filled(miss_dbl)
    lx  = ma.masked_where(ly ==miss_dbl, lwbin[1:]).filled(miss_dbl)
    lye = asig_p[iclass][1:]
    #
    #
    lx  = func.del_miss(lx,  miss_dbl)
    ly  = func.del_miss(ly,  miss_dbl)
    lye = func.del_miss(lye, miss_dbl)
    #
    plt.plot(lx, ly)
    ##
    dplt[iclass] = plt.errorbar(lx, ly, yerr = lye, label="%02d"%(iclass))
    ##
  #--
  llegend = map(str, lclass[1:])
  plt.legend(loc="upper left")
  #plt.legend( dplt.values(), llegend, "upper left")
  plt.savefig(w_p_name)
  #*******************************
  #-----------------
  # w-n
  #-----------------
  for iclass in [0]:
    plt.clf()
    w_n_name = pictdir  + "/p%05.2f.r%04d.w.n.c%02d.%02d.png"%(xth, crad, iclass,nclass)
    #
    ly  = array(dlnum[iclass][1:])
    #lx  = -ma.masked_equal(aw[iclass][1:], miss_dbl).filled(miss_dbl)
    lx  = ma.masked_where(ly ==0.0, lwbin[1:]).filled(miss_dbl)
    #
    lx  = func.del_miss(lx,  miss_dbl)
    ly  = func.del_miss(ly,  0.0)
    #
    plt.plot(lx, ly)
    ##
    plt.savefig(w_n_name)
  #-----------------------------
  # w-n : put all into one figure
  #-----------
  plt.clf()
  dplt = {}
  w_n_name = pictdir  + "/p%05.2f.r%04d.w.n.cmulti.%02d.png"%(xth, crad, nclass)
  for iclass in lclass[1:]:
    #
    ly  = array(dlnum[iclass][1:])
    #lx  = -ma.masked_equal(aw[iclass][1:], miss_dbl).filled(miss_dbl)
    lx  = ma.masked_where(ly ==0.0, lwbin[1:]).filled(miss_dbl)
    #
    lx  = func.del_miss(lx,  miss_dbl)
    ly  = func.del_miss(ly,  0.0)
    #
    dplt[iclass] = plt.plot(lx, ly)
    ##
  #--
  llegend = map(str, lclass[1:])
  plt.legend( dplt.values(), llegend, "upper right")
  plt.savefig(w_n_name)
  #*******************************
  #-----------------
  # w-rn,  relative frequency
  #-----------------
  for iclass in [0]:
    plt.clf()
    w_rn_name = pictdir  + "/p%05.2f.r%04d.w.rn.c%02d.%02d.png"%(xth, crad, iclass,nclass)
    #
    ly  = array(dlrnum[iclass][1:])
    #lx  = -ma.masked_equal(aw[iclass][1:], miss_dbl).filled(miss_dbl)
    lx  = ma.masked_where(ly ==0.0, lwbin[1:]).filled(miss_dbl)
    #
    lx  = func.del_miss(lx,  miss_dbl)
    ly  = func.del_miss(ly,  0.0)
    #
    plt.plot(lx, ly)
    ##
    plt.savefig(w_rn_name)
  #-----------------------------
  # w-rn : put all into one figure
  #-----------
  plt.clf()
  dplt = {}
  w_rn_name = pictdir  + "/p%05.2f.r%04d.w.rn.cmulti.%02d.png"%(xth, crad, nclass)
  for iclass in lclass[1:]:
    #
    ly  = array(dlrnum[iclass][1:])
    #lx  = -ma.masked_equal(aw[iclass][1:], miss_dbl).filled(miss_dbl)
    lx  = ma.masked_where(ly ==0.0, lwbin[1:]).filled(miss_dbl)
    #
    lx  = func.del_miss(lx,  miss_dbl)
    ly  = func.del_miss(ly,  0.0)
    #
    dplt[iclass] = plt.plot(lx, ly)
    ##
  #--
  llegend = map(str, lclass[1:])
  plt.legend( dplt.values(), llegend, "upper right")
  plt.savefig(w_rn_name)
#------------------------------------------------------
#-----------------
# c-rp
#-----------------
plt.clf()
c_rp_name = pictdir  + "/p%05.2f.r%04d.c.rp.cn%02d.png"%(xth, crad, nclass)
#--
sp  = sum(dlsp[-1])
lx  = array(lclass[1:])
ly  = sum(asp_reg[1:], axis=1) / sp
plt.bar(lx-0.5, ly)
#---
lcrp = []  # cumulative relative precipitation
cp = 0.0
for iclass in lclass[1:]:
  cp = cp + sum(asp_reg[iclass])
  lcrp.append(cp)
lcrp = lcrp / sp
plt.plot(lx, lcrp)
#---
plt.xlim(0, nclass)
plt.savefig(c_rp_name)

