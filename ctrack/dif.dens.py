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
#***************************************
diyear = {"his": iyear_his, "fut": iyear_fut}
deyear = {"his": eyear_his, "fut": eyear_fut}
#***************************************
dexpr  = {"his": "historical", "fut": "rcp85"}

#***************************************
# class
#-----------------------------
dpgradrange   = ctrack_para.ret_dpgradrange()
lclass        = dpgradrange.keys()
nclass        = len(lclass) -1
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
ddir_root["fut"] = "/media/disk2/out/CMIP5/6hr/%s/rcp85/%s/tracks/map"%(model, ens)
ddir_root["his"] = "/media/disk2/out/CMIP5/6hr/%s/historical/%s/tracks/map"%(model, ens)
ddir_root["dif"] = "/media/disk2/out/CMIP5/6hr/%s/dif/%s/tracks/map"%(model, ens)
csvdir_root      = "/media/disk2/out/CMIP5/6hr/%s/dif/%s/tracks/csv"%(model, ens)
#-------------
ddir  = {}
for era in ["his", "fut"]:
  #------------
  iyear = diyear[era]
  eyear = deyear[era]
  #------------
  for year in range(iyear, eyear+1) + [0]:
    ddir[era, year]  = ddir_root[era] + "/%04d"%(year)
#---
ddir["dif"] = ddir_root["dif"] + "/%04d.%04d-%04d.%04d"%(diyear["his"], deyear["his"], diyear["fut"], deyear["fut"])
#
func.mk_dir(ddir["dif"])
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
      ddensname[era, year, iclass]     = ddir[era, year]  + "/dens.area.dura%02d.nc%02d.c%02d_%s_6hr_%s_%s_%s.bn"%(thdura, nclass, iclass, season, model, dexpr[era], ens)
#----------------
# name for dif
#----------------
ddifname    = {}
for iclass in lclass:
  ddifname[iclass]   = ddir["dif"]  + "/dens.area.dura%02d.nc%02d.c%02d_%s_6hr_%s_dif_%s.bn"%(thdura, nclass, iclass, season, model, ens)
  
#****************************************
for iclass in lclass:
  #**********************
  # read 
  #----------------------
  a2his    = fromfile(ddensname["his", 0, iclass], float32)
  a2fut    = fromfile(ddensname["fut", 0, iclass], float32)
  #----------------------
  a2dif    = a2fut - a2his
  #----------------------
  # write
  #----------------------
  a2dif.tofile(ddifname[iclass])
  print ddifname[iclass]
##****************************************
## make pict
##----------------------------------------
#cmd          = oekakidir + "/track.gmt.py"
#cptfile      = oekakidir + "/cpt/polar.inv.-1.1.cpt"
##-----------------
#print "-----------------------------------"
#print "make pict"
#for iclass in lclass:
#  #---------------
#  iname       = ddifname[iclass]
#  pngname     = ddifname[iclass][:-3] + ".png"
#  psfile      = ddifname[iclass][:-3] + ".ps"
#  title       = "dif"
#  scalestep   = 0.2
#  overscale   = 1 
#  #---------------
#  os.system("python %s %s %s %s %s %s %s"%(\
#           cmd                  \
#          ,iname                \
#          ,cptfile              \
#          ,pngname              \
#          ,title                \
#          ,scalestep            \
#          ,overscale            \
#          ))       
#  print pngname 
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
        a2dens  =  fromfile(ddensname[era, year, iclass], float32).reshape(96,144)
        #---------------
        # mask
        #---------------
        a2dens_tmp = ma.masked_where( a2regionmask ==0.0, a2dens)
        a2dens_tmp = ma.masked_invalid(a2dens_tmp)
        #---------------
        # mean dens
        #---------------
        dlv[reg, era, iclass].append( a2dens_tmp.mean() )
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
csvdir = csvdir_root + "/%04d.%04d-%04d.%04d"%(diyear["his"], deyear["his"], diyear["fut"], deyear["fut"])

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




