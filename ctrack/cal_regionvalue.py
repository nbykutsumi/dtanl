from ctrack import *
from numpy import *
import ctrack_para
import calendar
import datetime
import os, sys

#####################################################
# functions
#####################################################
def mk_dir(sdir):
  try:
    os.makedirs(sdir)
  except:
    pass
#####################################################
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
#####################################################



#####################################################
#    MAIN
#####################################################
##***************************

if ( len(sys.argv) >1):
  model       = sys.argv[1]
  expr        = sys.argv[2]
  ens         = sys.argv[3]
  tstp        = sys.argv[4]
  season      = sys.argv[5]
  nx          = int(sys.argv[6])
  ny          = int(sys.argv[7])
  lon_first   = float(sys.argv[9])
  lat_first   = float(sys.argv[10])
  dlon        = float(sys.argv[11])
  dlat        = float(sys.argv[12])
  miss_dbl    = float(sys.argv[13])
  miss_int    = float(sys.argv[14])
  thdura      = int(sys.argv[15])
  thorog      = float(sys.argv[16])

  #------ 
  lseason     = ctrack_para.ret_lseason()
  lcrad       = ctrack_para.ret_lcrad()
  dpgradrange = ctrack_para.ret_dpgradrange()
  lclass      = dpgradrange.keys()
  daggname    = {}
  dwapname    = {}
  dwapupname  = {}
  csvname     = {}
#-----------------------------
else:
  model       = "NorESM1-M"
  expr        = "historical"
  ens         = "r1i1p1"
  tstp        = "day"
  season      = "DJF"
  nx          = 144
  ny          = 96
  lon_first   = -180.0
  lat_first   = -90.0
  dlon        = 2.5
  dlat        = 1.8947368
  miss_dbl    = -9999.0
  miss_int    = -9999
  thdura      = 24
  thorog      = 1500.0
  lseason = ["DJF"]
  #lcrad        = [500*1000.0]
  lcrad       = [500*1000.0, 1000*1000.0, 1500*1000.0, 2000.0*1000.0]
  dpgradrange = ctrack_para.ret_dpgradrange()
  lclass      = dpgradrange.keys()
#********************************************************
dir_root   = "/media/disk2/out/CMIP5/%s/%s/%s/%s/tracks/aggr.pr"%(tstp, model, expr, ens)
daggname   = {}
dwapname   = {}
dwapupname = {}
dcountname = {}
for crad in lcrad:
  for season in lseason:
    for i in range(len(lclass)):
      iclass = lclass[i]
      #------------
      # name for agg
      #------------
      aggdir = dir_root + "/pr" 
      daggname[crad, season, iclass] = aggdir + "/aggr.pr.c%02d.r%04d_%s_%s_%s_%s_%s.bn"%(iclass, crad*0.001, season, tstp, model, expr, ens)
      #------------
      # name for wap
      #------------
      wapdir = dir_root + "/wap"
      dwapname[crad, season, iclass] = wapdir + "/wap.c%02d.r%04d_%s_%s_%s_%s_%s.bn"%(iclass, crad*0.001, season, tstp, model, expr, ens)
      #------------
      # name for wapup
      #------------
      wapupdir = dir_root + "/wapup"
      dwapupname[crad, season, iclass] = wapupdir + "/wapup.c%02d.r%04d_%s_%s_%s_%s_%s.bn"%(iclass, crad*0.001, season, tstp, model, expr, ens)
      #------------
      # name for count
      #------------
      countdir = dir_root + "/count.cyclone"
      dcountname[crad, season, iclass] = countdir + "/count.cyclone.c%02d.r%04d_%s_%s_%s_%s_%s.bn"%(iclass, crad*0.001, season, tstp, model, expr, ens)
#------
csvdir     = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/csv"%(model, expr, ens)
mk_dir(csvdir)
#------
csvname       = csvdir + "/aggr.pr.csv"
csvname_wap   = csvdir + "/aggr.wap.csv"
csvname_wapup = csvdir + "/aggr.wapup.csv"
csvname_count = csvdir + "/aggr.count.csv"
#***********************************




#***************************************************
# make csv
#***************************************************
# make csv
#----------------------------
# read data # agg
#----------------
pr_reg    = {}
wap_reg   = {}
wapup_reg = {}
count_reg = {}
for crad in lcrad:
  for season in lseason:
    #----------------
    # agg
    #----------------
    da2agg = {}
    for iclass in lclass:
      da2agg[iclass] = fromfile( daggname[crad, season, iclass], float32).reshape(ny, nx)
    #----------------
    # wap
    #----------------
    da2wap = {}
    for iclass in lclass:
      da2wap[iclass] = fromfile( dwapname[crad, season, iclass], float32).reshape(ny, nx)
    #----------------
    # wapup
    #----------------
    da2wapup = {}
    for iclass in lclass:
      da2wapup[iclass] = fromfile( dwapupname[crad, season, iclass], float32).reshape(ny, nx)
    #----------------
    # count
    #----------------
    da2count = {}
    for iclass in lclass:
      da2count[iclass] = fromfile( dcountname[crad, season, iclass], float32).reshape(ny, nx)
    #----------------
    # make region mask
    #----------------
    #----
    #lat_min  = 30.0
    #lat_max  = 45.0
    #lon_min  = 120
    #lon_max  = 180
    lat_min  = 30.0
    lat_max  = 45.0
    lon_min  = -120
    lon_max  = -40
    #--
    a2regionmask = mk_region_mask(lat_min, lat_max, lon_min, lon_max, nx, ny, lat_first, lon_first, dlat, dlon)

    #----------------
    for iclass in lclass:
      #----------------
      # agg
      #----------------
      a2agg          =  ma.masked_where(a2regionmask == 0.0, da2agg[iclass])
      a2agg          =  ma.masked_equal(a2agg, miss_dbl)
      pr_reg[crad, season, iclass] = a2agg.mean()
      #pr_reg[crad, season, iclass] = a2agg.max()
      pr_reg[crad, season, iclass] = pr_reg[crad, season, iclass] * 60*60*24.0
      #----------------
      # wap
      #----------------
      a2wap          =  ma.masked_where(a2regionmask == 0.0, da2wap[iclass])
      a2wap          =  ma.masked_equal(a2wap, miss_dbl)
      wap_reg[crad, season, iclass] = a2wap.mean()
      #----------------
      # wapup
      #----------------
      a2wapup        =  ma.masked_where(a2regionmask == 0.0, da2wapup[iclass])
      a2wapup        =  ma.masked_equal(a2wapup, miss_dbl)
      wapup_reg[crad, season, iclass] = a2wapup.mean()
      #----------------
      # count
      #----------------
      a2count          =  ma.masked_where(a2regionmask == 0.0, da2count[iclass])
      a2count          =  ma.masked_equal(a2count, miss_dbl)
      count_reg[crad, season, iclass] = a2count.mean()
      #count_reg[crad, season, iclass] = a2count.sum()
      #count_reg[crad, season, iclass] = a2count.max()


#-----------------------
# make output string for agg
#-----------------------
dsout_pr = {}
#-------------------------------
for iseason in lseason:
  dsout_pr[iseason] = "%s,"%(iseason) + ",".join(map(str, lcrad)) + "\n"
  #---------------------------------
  for iclass in lclass:
    dsout_pr[iseason] = dsout_pr[iseason] + "%02d"%(iclass)
    #----------------------------------
    for crad in lcrad:
      dsout_pr[iseason] = dsout_pr[iseason] + ",%f"%(pr_reg[crad, season, iclass])
    #---
    dsout_pr[iseason] = dsout_pr[iseason] + "\n"
  #-----
  print dsout_pr[iseason]
#-------
sout_pr = ""
for iseason in lseason:
  sout_pr = sout_pr + dsout_pr[iseason] + "\n"
#-------
sout_pr = sout_pr.strip()
print sout_pr  
#-------
f = open(csvname, "w")
f.write(sout_pr)
f.close()

#-----------------------
# make output string for wap
#-----------------------
dsout_wap = {}
#-------------------------------
for iseason in lseason:
  dsout_wap[iseason] = "%s,"%(iseason) + ",".join(map(str, lcrad)) + "\n"
  #---------------------------------
  for iclass in lclass:
    dsout_wap[iseason] = dsout_wap[iseason] + "%02d"%(iclass)
    #----------------------------------
    for crad in lcrad:
      dsout_wap[iseason] = dsout_wap[iseason] + ",%f"%(wap_reg[crad, season, iclass])
    #---
    dsout_wap[iseason] = dsout_wap[iseason] + "\n"
  #-----
  print dsout_wap[iseason]
#-------
sout_wap = ""
for iseason in lseason:
  sout_wap = sout_wap + dsout_wap[iseason] + "\n"
#-------
sout_wap = sout_wap.strip()
print sout_wap  
#-------
f = open(csvname_wap, "w")
f.write(sout_wap)
f.close()

#-----------------------
# make output string for wapup
#-----------------------
dsout_wapup = {}
#-------------------------------
for iseason in lseason:
  dsout_wapup[iseason] = "%s,"%(iseason) + ",".join(map(str, lcrad)) + "\n"
  #---------------------------------
  for iclass in lclass:
    dsout_wapup[iseason] = dsout_wapup[iseason] + "%02d"%(iclass)
    #----------------------------------
    for crad in lcrad:
      dsout_wapup[iseason] = dsout_wapup[iseason] + ",%f"%(wapup_reg[crad, season, iclass])
    #---
    dsout_wapup[iseason] = dsout_wapup[iseason] + "\n"
  #-----
  print dsout_wapup[iseason]
#-------
sout_wapup = ""
for iseason in lseason:
  sout_wapup = sout_wapup + dsout_wapup[iseason] + "\n"
#-------
sout_wapup = sout_wapup.strip()
print sout_wapup  
#-------
f = open(csvname_wapup, "w")
f.write(sout_wapup)
f.close()



#-----------------------
# make output string for count
#-----------------------
dsout_count = {}
#-------------------------------
for iseason in lseason:
  dsout_count[iseason] = "%s,"%(iseason) + ",".join(map(str, lcrad)) + "\n"
  #---------------------------------
  for iclass in lclass:
    dsout_count[iseason] = dsout_count[iseason] + "%02d"%(iclass)
    #----------------------------------
    for crad in lcrad:
      dsout_count[iseason] = dsout_count[iseason] + ",%f"%(count_reg[crad, season, iclass])
    #---
    dsout_count[iseason] = dsout_count[iseason] + "\n"
  #-----
  print dsout_count[iseason]
#-------
sout_count = ""
for iseason in lseason:
  sout_count = sout_count + dsout_count[iseason] + "\n"
#-------
sout_count = sout_count.strip()
print sout_count  
#-------
f = open(csvname_count, "w")
f.write(sout_count)
f.close()


