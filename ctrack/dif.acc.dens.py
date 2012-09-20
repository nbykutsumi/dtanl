import ctrack_para
import ctrack_func as func
from numpy import *
import os, sys

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

xth         = 0.0
crad        = 1000.0

(imon, emon) = ctrack_para.ret_im_em(season)
mons         = ctrack_para.ret_mons(season)
#***************************************
diyear = {"his": iyear_his, "fut": iyear_fut}
deyear = {"his": eyear_his, "fut": eyear_fut}
#***************************************
dexpr  = {"his": "historical", "fut": "rcp85"}

#***************************************
# class
#-----------------------------
dpgradrange   = ctrack_para.ret_dpgradrange()
cmin          = dpgradrange[0][0]
lclass        = dpgradrange.keys()
nclass        = len(lclass) -1
#***************************************
# wbin
#----------------------
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
ddir_root["fut"] = "/media/disk2/out/CMIP5/day/%s/rcp85/%s/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d"%(model, ens, thdura, imon, emon, nclass, cmin )
ddir_root["his"] = "/media/disk2/out/CMIP5/day/%s/historical/%s/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d"%(model, ens, thdura, imon, emon, nclass, cmin )
csvdir           = "/media/disk2/out/CMIP5/day/%s/dif/rcp85/%04d-%04d.%04d-%04d/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d/csv"%(model, iyear_his, eyear_his, iyear_fut, eyear_fut, thdura, imon, emon, nclass, cmin)
#-------------
ddir  = {}
for era in ["his", "fut"]:
  for var in ["num"]:
    #------------
    iyear = diyear[era]
    eyear = deyear[era]
    #------------
    for year in range(iyear, eyear+1) + [0]:
      ddir[era, var, year]  = ddir_root[era] + "/%s/%04d"%(var, year)

#**********************
# names for each class
#----------------------
ddensname  = {}
for era in ["his", "fut"]:
  #------------
  iyear = diyear[era]
  eyear = deyear[era]
  #------------
  for year in range(iyear, eyear+1) + [0]:
    for iclass in lclass:
      ddensname[era, year, iclass]     = ddir[era, "num", year]  + "/dens.area.dura%02d.nc%02d.c%02d_%s_6hr_%s_%s_%s.bn"%(thdura, nclass, iclass, season, model, dexpr[era], ens)
      ddensname[era, year, iclass]     = ddir[era, "num", year]  + "/num.p00.00.cmin0001.c02.04.r1000.nw17_DJF_day_NorESM1-M_historical_r1i1p1.bn"
      ddensname[era, year, iclass]     = ddir[era, "num", year]  + "/num.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad, nwbin, season, model, dexpr[era], ens)
 
 
#****************************************
# regional dif
#----------------------------------------
dbound   = ctrack_para.ret_dbound()
lreg     = dbound.keys()
#******************
#
#------------------
dfcm    = {}
dmv     = {}
dtv     = {}
dlv     = {}
for reg in lreg:
  print reg
  #******************
  # regionmask
  #------------------
  [lat_min, lat_max, lon_min, lon_max] = dbound[reg]

  a2regionmask  = func.mk_region_mask(lat_min, lat_max, lon_min, lon_max, nx, ny, lat_first, lon_first, dlat, dlon)
  #--------------------
  for iclass in lclass:
    for era in ["his", "fut"]:
      #--------------------------
      dlv[reg, era, iclass] = []
      iyear  = diyear[era]
      eyear  = deyear[era]
      #--------------------------
      for year in range(iyear, eyear + 1):
        #***************
        # read
        #---------------
        a2dens  =  fromfile(ddensname[era, year, iclass], float32).reshape(nwbin, ny, nx)[0]
        #---------------
        # mask
        #---------------
        a2dens_tmp = ma.masked_where( a2regionmask ==0.0, a2dens)
        a2dens_tmp = ma.masked_invalid(a2dens_tmp)
        print iclass, a2dens_tmp.mean()
        #---------------
        # mean dens
        #---------------
        dlv[reg, era, iclass].append( a2dens_tmp.mean()/mons )
      #-----------------
      # calc regional mean
      #-----------------
      dmv[reg, era, iclass]       = mean(dlv[reg, era, iclass])
      #-----------------
    #-----------------
    # calc t-value
    #-----------------
    dtv[reg, iclass] = func.ret_tv_difmean(dlv[reg, "his",iclass], dlv[reg, "fut",iclass])
    print iclass, dtv[reg, iclass]
    #-----------------
    # calc difference of regional mean
    #-----------------
    dfcm[reg, iclass] = (mean(dlv[reg, "fut", iclass]) - mean(dlv[reg, "his", iclass]))/mean(dlv[reg,"his",iclass]) * 100.0

#****************************************
# write csv
#----------------------------------------
func.mk_dir(csvdir)

#------------
for reg in lreg:
  #--------
  # name
  #--------
  statname = csvdir + "/dens.stat.%s.csv"%(reg)
  #--------
  sstat = "class,his,fut,frac.chng,t\n"
  for iclass in lclass:
    sstat = sstat + "%s,%s,%s,%s,%s"%( iclass, dmv[reg, "his", iclass], dmv[reg, "fut", iclass], dfcm[reg, iclass], dtv[reg, iclass]) + "\n"
  #--------
  # write
  #--------
  f = open(statname, "w")
  f.write(sstat)
  f.close()
  print statname 




