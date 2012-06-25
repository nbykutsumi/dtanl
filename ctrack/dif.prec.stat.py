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
#***************************************
lonlatinfo = ctrack_para.ret_lonlatinfo(model)
[lon_first, lat_first, dlon, dlat] = lonlatinfo
#
dlwbin      = ctrack_para.ret_dlwbin()
liw         = dlwbin.keys()
nwbin       = len(liw)
#***************************************

diyear = {"his": iyear_his, "fut": iyear_fut}
deyear = {"his": eyear_his, "fut": eyear_fut}
#***************************************
dexpr  = {"his": "historical", "fut": "rcp85"}
lcrad  = ctrack_para.ret_lcrad()
#***************************************
# class
#-----------------------------
dpgradrange   = ctrack_para.ret_dpgradrange()
lclass        = dpgradrange.keys()
nclass        = len(lclass) -1
#***************************************
# region bound
#---------------------------------------
dbound = ctrack_para.ret_dbound()
lreg   = dbound.keys()

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
ddir_root["fut"] = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/wfpr"%(model, dexpr["fut"],ens, thdura)
ddir_root["dif"] = "/media/disk2/out/CMIP5/day/%s/dif/%s/%04d-%04d.%04d-%04d/tracks/dura%02d/wfpr"%(model, dexpr["fut"], iyear_his, eyear_his, iyear_fut, eyear_fut, thdura)
csvdir_root      = ddir_root["dif"] + "/csv"
#-------------
#**********************
# names for input files
#----------------------
dspname    = {}
dnumname  = {}
ddensname  = {}
for crad in lcrad:
  crad = crad * 0.001
  for era in ["his", "fut"]:
    #------------
    iyear = diyear[era]
    eyear = deyear[era]
    #------------
    for year in range(iyear, eyear+1):
      for iclass in lclass:
        dspname[crad, era, year, iclass]     = ddir_root[era]  + "/sp/%04d/sp.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(year, xth, iclass, nclass, crad, nwbin, season, model, dexpr[era], ens)
        dnumname[crad, era, year, iclass]     = ddir_root[era]  + "/num/%04d/num.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(year, xth, iclass, nclass, crad, nwbin, season, model, dexpr[era], ens)
#****************************************
dlp     = {}  # precipitation intensity conditioned on cyclone
dlsp    = {}  # total precipitation per season conditioned on cyclone
dlnum   = {}
dp_reg  = {}
dsp_reg = {}
dtv_p   = {}  # t-value for precip intensity
dtv_sp  = {}  # t-value for total precip
dfc_p   = {}  # fractional change of p
dfc_sp  = {}  # fractional change of sp

sp2     = 0.0
n       = 0.0
for crad in lcrad:
  crad = crad * 0.001
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
        dlp[reg, era, iclass]  = []
        dlsp[reg, era, iclass] = []
        iyear  = diyear[era]
        eyear  = deyear[era]
        #--------------------------
        for year in range(iyear, eyear + 1):
          #***************
          # read
          #---------------
          a2sp  =  fromfile(dspname[crad, era, year, iclass], float32).reshape(nwbin, ny, nx)[0]
          a2num =  fromfile(dnumname[crad, era, year, iclass], float32).reshape(nwbin, ny, nx)[0]
          #***************
          # make precip intensity
          #---------------
          a2p   = (a2sp / ma.masked_equal(a2num, 0.0) ).filled(0.0)
          #---------------
          # mask
          #---------------
          a2p_tmp = ma.masked_where( a2regionmask ==0.0, a2p)
          a2p_tmp = ma.masked_equal(a2p_tmp, 0.0)
          a2p_tmp = ma.masked_invalid(a2p_tmp)
          a2sp_tmp = ma.masked_where(a2regionmask ==0.0, a2sp)
          a2sp_tmp = ma.masked_equal(a2sp_tmp, 0.0)
          a2sp_tmp = ma.masked_invalid(a2sp_tmp)
          #
          #---------------
          # mean value
          #---------------
          dlp[reg, era, iclass].append( a2p_tmp.mean() )
          dlsp[reg, era, iclass].append( a2sp_tmp.mean() )
        #-----------------
        # calc regional mean
        #-----------------
        dp_reg[reg, era, iclass]       = mean(dlp[reg, era, iclass])
        dsp_reg[reg, era, iclass]       = mean(dlsp[reg, era, iclass])
        #-----------------
      #-----------------
      # calc t-value
      #-----------------
      dtv_p[reg, iclass] = func.ret_tv_difmean(dlp[reg, "fut",iclass], dlp[reg, "his",iclass])
      dtv_sp[reg, iclass] = func.ret_tv_difmean(dlsp[reg, "fut",iclass], dlsp[reg, "his",iclass])
      print iclass, dtv_p[reg, iclass]
      #-----------------
      # calc difference of regional mean
      #-----------------
      dfc_p[reg, iclass] = (mean(dlp[reg, "fut", iclass]) - mean(dlp[reg, "his", iclass]))/mean(dlp[reg,"his",iclass]) * 100.0
      dfc_sp[reg, iclass] = (mean(dlsp[reg, "fut", iclass]) - mean(dlsp[reg, "his", iclass]))/mean(dlsp[reg,"his",iclass]) * 100.0
  
  #****************************************
  # write csv
  #----------------------------------------
  csvdir = csvdir_root 
  
  func.mk_dir(csvdir)
  
  #------------
  for reg in lreg:
    #--------
    # name
    #--------
    statname_p  = csvdir + "/prec.stat.%s.p%05.2f.cn%02d.r%04d._%s_day_%s_%s_%s.csv"%(reg, xth, nclass, crad, season, model, dexpr[era], ens)
    statname_sp  = csvdir + "/tot-prec.stat.%s.p%05.2f.cn%02d.r%04d._%s_day_%s_%s_%s.csv"%(reg, xth, nclass, crad, season, model, dexpr[era], ens)
    #--------
    sstat_p = "class,his,fut,frac.chng,t\n"
    sstat_sp = "class,his,fut,frac.chng,t\n"
    for iclass in lclass:
      sstat_p  = sstat_p  + "%s,%s,%s,%s,%s"%( iclass, dp_reg[reg, "his", iclass], dp_reg[reg, "fut", iclass], dfc_p[reg, iclass], dtv_p[reg, iclass]) + "\n"
      sstat_sp = sstat_sp + "%s,%s,%s,%s,%s"%( iclass, dsp_reg[reg, "his", iclass], dsp_reg[reg, "fut", iclass], dfc_sp[reg, iclass], dtv_sp[reg, iclass]) + "\n"
    #--------
    # write
    #--------
    f = open(statname_p, "w")
    f.write(sstat_p)
    f.close()
    print statname_p
    #
    f = open(statname_sp, "w")
    f.write(sstat_sp)
    f.close()
    #--------
  
  
  
