from numpy import *
from ctrack_fsub import *
import ctrack_para
import os, calendar
import matplotlib.pyplot as plt
import cf
#*************************************************************
iyear     = 1990
eyear     = 1993
season    = "DJF"
model     = "NorESM1-M"
tstp     = "6hr"
expr      = "historical"
ens       = "r1i1p1"
nx_org    = 144
ny_org    = 96
nz_org    = 8
iz500     = 3

var       = "pr"
thgrad_min    = 500.0  # Pa/1000km
thgrad_max    = 1000.0 # Pa/1000km
#thgrad_min    = 1000.0  # Pa/1000km
#thgrad_max    = 2000.0  # Pa/1000km
#---------------------
dkm           = 100.0  # equal area grid resolution [km]
nradeqgrid    = 30

#---------------------
nx_eqgrid     = nradeqgrid*2 + 1
ny_eqgrid     = nradeqgrid*2 + 1
#---------------------
latmin    = 30.0
latmax    = 60.0
lonmin    = 120.
lonmax    = 240.

#latmin    = 32.0
#latmax    = 34.0
#lonmin    = 136.0
#lonmax    = 138.0

#latmin    = 38.0
#latmax    = 40.0
#lonmin    = 136.0
#lonmax    = 138.0
#-------------------------------------------
miss_out  = -9999.0
#------------------------------------------
lmon      = ctrack_para.ret_lmon(season)
lhour     = [0, 6, 12, 18]

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
idir_root1           = "/media/disk2/data/CMIP5/bn"
idir_root2           = "/media/disk2/out/CMIP5/6hr/%s/%s/%s"%(model, expr, ens)
#
didir_root   = {}
didir_root["pr"]     = idir_root1 + "/%s/%s/%s/%s/%s"%("pr", tstp, model, expr, ens)
didir_root["life"]   = idir_root2 + "/%s"%("life")
didir_root["pgrad"]  = idir_root2 + "/%s"%("pgrad")
didir_root["wap"]    = idir_root1 + "/%s"%("wap")

#-------
odir         = "/home/utsumi/bin/dtanl/ctrack/temp"
oname_mean   = odir + "/%s.%s.%04.0f-%04.0f.bn"%(var, sreg, thgrad_min, thgrad_max)

#---- lat and lon data :original ----------
latname      = didir_root["pr"] + "/lat.txt"
lonname      = didir_root["pr"] + "/lon.txt"
a1lat_org    = readlatlon(latname)
a1lon_org    = readlatlon(lonname)

dlat_org       = a1lat_org[1] - a1lat_org[0]
dlon_org       = a1lon_org[1] - a1lon_org[0]

lat_org_first  = a1lat_org[0]
lon_org_first  = a1lon_org[0]

#---- lat and lon data : original ---------
a1lat_fin     = arange(-89.95, 89.95, 0.25)
a1lon_fin     = arange(0.0, 359.95, 0.25)
lat_fin_first = a1lat_fin[0]
lon_fin_first = a1lon_fin[0]
dlat_fin      = a1lat_fin[1] - a1lat_fin[0]
dlon_fin      = a1lon_fin[1] - a1lon_fin[0]

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

#------------------------------------------
#---- dummy ------------------------------
a2sum_eqgrid      = zeros([ny_eqgrid, nx_eqgrid], float32)
a2num_eqgrid      = zeros([ny_eqgrid, nx_eqgrid], float32)
#-----------------------------------------
i = 0
for year in range(iyear, eyear+1):
  #----------
  didir    = {}
  for var_temp in ["pr", "life", "pgrad","wap"]:
    if var_temp == "wap":
      didir[var_temp] = didir_root[var_temp] + "/day/%s/%s/%s/%04d"%(model, expr, ens, year)
    else:
      didir[var_temp] = didir_root[var_temp] + "/%04d"%(year)
  #----------
  for mon in lmon:
  #for mon in [1]:
    #-- no leap ------
    if (mon ==2):
      eday = 28
    else:
      eday  = calendar.monthrange(year, mon)[1]
    #-----------------
    for day in range(1, eday+1):
    #for day in range(1,5):
      print year, mon, day
      for hour in lhour:
        #--- name ------------
        diname          = {}
        diname["pr"]    = didir["pr"]    + "/%s_6hr_%s_%s_%s_%04d%02d%02d%02d.bn"%("pr", model, expr, ens, year, mon, day, hour)
        diname["life"]  = didir["life"]  + "/%s_6hr_%s_%s_%s_%04d%02d%02d%02d.bn"%("life", model, expr, ens, year, mon, day, hour)
        diname["pgrad"] = didir["pgrad"] + "/%s_6hr_%s_%s_%s_%04d%02d%02d%02d.bn"%("pgrad", model, expr, ens, year, mon, day, hour)
        diname["wap"]   = didir["wap"] + "/%s_day_%s_%s_%s_%04d%02d%02d00.bn"%("wap", model, expr, ens, year, mon, day)
        #--- load ------------
        da2in           = {}
        da2in[var]      = fromfile(diname[var],  float32).reshape(ny_org, nx_org)
        da2in["pgrad"]  = fromfile(diname["pgrad"],float32).reshape(ny_org, nx_org)
        #da2in["life"]   = fromfile(diname["life"], int32).reshape(ny_org, nx_org)

        #--- original --> fine grid ---
        a2in_fin        = cf.biIntp(a1lat_org, a1lon_org, da2in[var], a1lat_fin, a1lon_fin)[0] 
        ##--- join data to expand the area -----
        #da2in_temp           = {}
        #da2in_temp["pgrad"]  = c_[da2in["pgrad"], da2in["pgrad"], da2in["pgrad"]]
        ##da2in_temp["life"]   = c_[da2in["life"], da2in["life"], da2in["life"]]

        ##-
        #a2in_fin_temp        = c_[a2in_fin, a2in_fin, a2in_fin]

        #--- cyclone center data -------------
        da2in["center"] = ma.masked_less(da2in["pgrad"], 0.0).filled(0.0)
        da2in["center"] = ma.masked_greater(da2in["center"], 0.0).filled(1.0)
        #-------------------------------------
        for iy_org in ly_org:
          for ix_org in lx_org:
            if thgrad_min <= da2in["pgrad"][iy_org, ix_org] < thgrad_max:
              i = i+1
              print iy_org, ix_org
              #---- project center position original --> fine grid
              lat_org          = a1lat_org[iy_org]
              lon_org          = a1lon_org[ix_org]
              iy_fin, ix_fin   = latlon2yx(lat_org, lon_org, lat_fin_first, lon_fin_first, dlat_fin, dlon_fin)

              iy_fin_fort  = iy_fin + 1
              ix_fin_fort  = ix_fin + 1

              #---- search and project to equal size grids -----
              a2sum_eqgrid_temp, a2num_eqgrid_temp =\
                      ctrack_fsub.eqgrid_aggr(\
                                    a2in_fin.T\
                                  , a1lat_fin\
                                  , a1lon_fin\
                                  , dkm\
                                  , nradeqgrid\
                                  , iy_fin_fort\
                                  , ix_fin_fort) 
 
              a2sum_eqgrid  = a2sum_eqgrid + a2sum_eqgrid_temp.T
              a2num_eqgrid  = a2num_eqgrid + a2num_eqgrid_temp.T

#----------------------------------------------
a2mean_eqgrid  = ma.masked_where(a2num_eqgrid ==0.0, a2sum_eqgrid) / a2num_eqgrid
a2mean_eqgrid  = a2mean_eqgrid.filled(0.0)

#-- save --------------
a2mean_eqgrid.tofile(oname_mean)
#-- figure ---------------------



if var == "pr":
  coef = 60*60*24.0
else:
  coef = 1.0
#--
a2mean_eqgrid = fromfile(oname_mean, float32).reshape(ny_eqgrid, nx_eqgrid)
figname_mean = oname_mean[:-3] + ".png"
plt.clf()
plt.imshow(a2mean_eqgrid * coef, origin="lower", interpolation="nearest", vmin= 0.0, vmax=5.0)
plt.colorbar()
plt.savefig(figname_mean)
plt.clf()
print figname_mean
