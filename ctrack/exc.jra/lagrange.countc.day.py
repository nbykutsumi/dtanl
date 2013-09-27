from numpy import *
from ctrack_fsub import *
import ctrack_para
import ctrack_func
import os, calendar, datetime
import matplotlib.pyplot as plt
import cf
import gsmap_func
import aphro_func
#*************************************************************
iyear     = 2001
eyear     = 2004
season    = "DJF"
tstp      = "6hr"
nx_org    = 360
ny_org    = 180

var       = "pr"
aphromask = "TRUE"
lmon      = ctrack_para.ret_lmon(season)
#lmon      = [1]
#thgrad_min    = 500.0  # Pa/1000km
#thgrad_max    = 1000.0 # Pa/1000km
dpgradrange   = ctrack_para.ret_dpgradrange()
lclass        = dpgradrange.keys()
#-------------------------------------------
miss_out  = -9999.0
miss_gpcp = -99999.
#------------------------------------------
dkm           = 100.0  # equal area grid resolution [km]
nradeqgrid    = 30
nx_eqgrid     = nradeqgrid*2 + 1
ny_eqgrid     = nradeqgrid*2 + 1
#---------------------
#latmin    = -14.0
#latmax    = 54.0
#lonmin    = 60.0
#lonmax    = 149.5

latmin    = 30.0
#latmax    = 54.0
latmax    = 38.5
lonmin    = 60.0
lonmax    = 149.5

#latmin    = 30.0
#latmax    = 60.0
#lonmin    = 120.
#lonmax    = 240.

#latmin    = 32.0
#latmax    = 34.0
#lonmin    = 136.0
#lonmax    = 138.0

#latmin    = 38.0
#latmax    = 40.0
#lonmin    = 136.0
#lonmax    = 138.0

#---------------------
def readlatlon(fname):
  f = open(fname, "r")
  lines = f.readlines()
  f.close()
  lines = map(float, lines)
  return lines
#--------
def latlon2yx(lat, lon, lat_first, lon_first, dlat, dlon):
  iy    = int( (lat + 0.5*dlat - lat_first)/dlat )
  ix    = int( (lon + 0.5*dlon - lon_first)/dlon )
  return iy, ix

sreg="%02d.%02d.%03d.%03d"%(latmin, latmax, lonmin, lonmax)
#*************************************************************
#---------------------
didir_root   = {}
#---------------------------------
didir_root["life"]   = "/media/disk2/out/JRA25/sa.one/6hr" + "/%s"%("life")
didir_root["pgrad"]  = "/media/disk2/out/JRA25/sa.one/6hr" + "/%s"%("pgrad")
didir_root["wap"]    = "/media/disk2/out/JRA25/sa.one/6hr" + "/%s"%("wap")

#-------
if aphromask =="TRUE":
  odir         = "/home/utsumi/bin/dtanl/ctrack/temp/%s/day/land/%s/portion"%(season, sreg)
else:
  odir         = "/home/utsumi/bin/dtanl/ctrack/temp/%s/day/nomask/%s/portion"%(season, sreg)
#-------
ctrack_func.mk_dir(odir) 
#---- lat and lon data :original ----------

lat_org_first   = -89.5
lon_org_first   = 0.5
lat_org_last    = 89.5
lon_org_last    = 359.5

dlat_org        = 1.0
dlon_org        = 1.0

a1lat_org       = arange(lat_org_first, lat_org_last + dlat_org*0.5, dlat_org)
a1lon_org       = arange(lon_org_first, lon_org_last + dlon_org*0.5, dlon_org)

#---- lat and lon data : finner ---------
lat_fin_first = -89.95
lon_fin_first = 0.05
lat_fin_last  = 89.95
lon_fin_last  = 359.95

dlat_fin      = 0.2
dlon_fin      = 0.2
a1lat_fin     = arange(lat_fin_first, lat_fin_last + dlat_fin*0.5, dlat_fin)
a1lon_fin     = arange(lon_fin_first, lon_fin_last + dlon_fin*0.5, dlon_fin)

#------------------------------------------
ymin_org      = int( (latmin - lat_org_first)/dlat_org )
ymax_org      = int( (latmax - lat_org_first)/dlat_org )
if lonmin >= 0.0:
  xmin_org      = int( (lonmin - (lon_org_first-0.5*dlon_org))/dlon_org )
  xmax_org      = int( (lonmax - (lon_org_first-0.5*dlon_org))/dlon_org )
else:
  xmin_org      = int( (lonmin + 0.0001 - (lon_org_first + 0.5*dlon_org ))/dlon_org )
  xmax_org      = int( (lonmax + 0.0001 - (lon_org_first + 0.5*dlon_org ))/dlon_org )

lx_org      = range(xmin_org, xmax_org+1)
ly_org      = range(ymin_org, ymax_org+1)

#---- dummy ------------------------------
dcount = {}
for iclass in lclass:
  dcount[iclass] = 0
#-----------------------------------------
for year in range(iyear, eyear+1):
  for mon in lmon:
    eday  = calendar.monthrange(year, mon)[1]
    #-----------------
    for day in range(1, eday+1):
    #for day in range(28, eday+1):
      print lclass, iclass, year, mon, day, "eday=",eday
      print "lmon=" , lmon
      #for hour in lhour:
      for hour in [12]:
        #---------------------
        if ((year==iyear)&(mon==1)&(day==1)):
          continue
        if ((year==eyear)&(mon==12)&(day==31)):
          continue
        #---------------------
        didir = {}
        for var_temp in ["life", "pgrad"]:
          didir[var_temp] = didir_root[var_temp] + "/%04d%02d"%(year, mon)
        #----------
        diname = {} 
        diname["life"]  = didir["life"]  + "/life.%04d%02d%02d%02d.sa.one"%(year, mon, day, hour)
        diname["pgrad"] = didir["pgrad"] + "/pgrad.%04d%02d%02d%02d.sa.one"%(year, mon, day, hour)
        #---------------
        da2in = {}
        da2in["pgrad"]  = fromfile(diname["pgrad"],float32).reshape(ny_org, nx_org)
        #da2in["life"]   = fromfile(diname["life"], int32).reshape(ny_org, nx_org)

        #--- cyclone center data -------------
        da2in["center"] = ma.masked_less(da2in["pgrad"], 0.0).filled(0.0)
        da2in["center"] = ma.masked_greater(da2in["center"], 0.0).filled(1.0)
        #-------------------------------------
        for iy_org in ly_org:
          for ix_org in lx_org:
            #-------------
            if (da2in["pgrad"][iy_org, ix_org] <= 0):
              continue
            for iclass in lclass:
              thgrad_min = dpgradrange[iclass][0]
              thgrad_max = dpgradrange[iclass][1]
              
              if thgrad_min <= da2in["pgrad"][iy_org, ix_org] < thgrad_max:
                dcount[iclass] = dcount[iclass] +1
                
#-- data --------------
sout = "%04d-%04d %s %dmons\n"%(iyear, eyear, season, len(lmon))
for iclass in lclass:
  sout = sout + "class%02d, %d\n"%(iclass, dcount[iclass])
#-- save --------------
name_csv = odir + "/num.cyclones.csv"
f = open(name_csv, "w")
f.write(sout)
f.close()
print name_csv

