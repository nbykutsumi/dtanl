from ctrack_fsub import *
from numpy import *
import ctrack_para
import os, calendar
import matplotlib.pyplot as plt
#*************************************************************
iyear     = 1990
eyear     = 1999
season    = "DJF"
model     = "NorESM1-M"
tstp     = "6hr"
expr      = "historical"
ens       = "r1i1p1"
nx        = 144
ny        = 96
nz        = 8
iz500     = 3

lat_first = -90.0
lon_first = 0.0
dlat      = 1.8947368
dlon      = 2.5

#thgrad_min    = 500.0  # Pa/1000km
thgrad_min    = 1000.0  # Pa/1000km
thgrad_max    = 2000.0  # Pa/1000km
#---------------------
radx      = 4
rady      = 5

#latmin    = 30.0
#latmax    = 46.0
#lonmin    = 100.
#lonmax    = 160.

latmin    = 32.0
latmax    = 34.0
lonmin    = 136.0
lonmax    = 138.0


#latmin    = 38.0
#latmax    = 40.0
#lonmin    = 136.0
#lonmax    = 138.0



sreg="%02d.%02d.%03d.%03d"%(latmin, latmax, lonmin, lonmax)
#---------------------
miss_out  = -9999.0
#------------------------------------------
lmon      = ctrack_para.ret_lmon(season)
lhour     = [0, 6, 12, 18]

#------------------------------------------
ymin      = int( (latmin - lat_first)/dlat )
ymax      = int( (latmax - lat_first)/dlat )
if lonmin >= 0.0:
  xmin      = int( (lonmin - (lon_first-0.5*dlon))/dlon )
  xmax      = int( (lonmax - (lon_first-0.5*dlon))/dlon )
else:
  xmin      = int( (lonmin + 0.0001 - (lon_first + 0.5*dlon ))/dlon )
  xmax      = int( (lonmax + 0.0001 - (lon_first + 0.5*dlon ))/dlon )

print xmin, xmax
#------------------------------------------
#------------------------------------------
lx          = range(xmin + nx, xmax+1 +nx)
ly          = range(ymin, ymax+1)
#*************************************************************
idir_root1           = "/media/disk2/data/CMIP5/bn"
idir_root2           = "/media/disk2/out/CMIP5/6hr/%s/%s/%s"%(model, expr, ens)
#
didir_root   = {}
didir_root["pr"]     = idir_root1 + "/%s/%s/%s/%s/%s"%("pr", tstp, model, expr, ens)
didir_root["life"]   = idir_root2 + "/%s"%("life")
didir_root["pgrad"]  = idir_root2 + "/%s"%("pgrad")
didir_root["wap"]    = idir_root1 + "/%s"%("wap")

da2out ={}
da2out["pr"]         = zeros([2*rady+1, 2*radx+1], float32)
da2out["wap"]        = zeros([2*rady+1, 2*radx+1], float32)
da2out["temp"]       = zeros([2*rady+1, 2*radx+1], float32)

i = 0
for year in range(iyear, eyear+1):
  #----------
  didir    = {}
  for var in ["pr", "life", "pgrad","wap"]:
    if var == "wap":
      didir[var] = didir_root[var] + "/day/%s/%s/%s/%04d"%(model, expr, ens, year)
    else:
      didir[var] = didir_root[var] + "/%04d"%(year)
  #----------
  for mon in lmon:

    #-- no leap ------
    if (mon ==2):
      eday = 28
    else:
      eday  = calendar.monthrange(year, mon)[1]
    #-----------------
    for day in range(1, eday+1):
      print year, mon, day
      for hour in lhour:
        #---------------------
        diname          = {}
        diname["pr"]    = didir["pr"]    + "/%s_6hr_%s_%s_%s_%04d%02d%02d%02d.bn"%("pr", model, expr, ens, year, mon, day, hour)
        diname["life"]  = didir["life"]  + "/%s_6hr_%s_%s_%s_%04d%02d%02d%02d.bn"%("life", model, expr, ens, year, mon, day, hour)
        diname["pgrad"] = didir["pgrad"] + "/%s_6hr_%s_%s_%s_%04d%02d%02d%02d.bn"%("pgrad", model, expr, ens, year, mon, day, hour)
        diname["wap"]   = didir["wap"] + "/%s_day_%s_%s_%s_%04d%02d%02d00.bn"%("wap", model, expr, ens, year, mon, day)
        #---------------------
        da2in           = {}
        da2in["pr"]     = fromfile(diname["pr"],   float32).reshape(ny, nx)
        da2in["life"]   = fromfile(diname["life"], int32).reshape(ny, nx)
        da2in["pgrad"]  = fromfile(diname["pgrad"],float32).reshape(ny, nx)
        da2in["wap"]    = fromfile(diname["wap"],float32).reshape(nz, ny, nx)[iz500]
        #---------------------
        da2in_temp           = {}
        da2in_temp["pr"]     = c_[da2in["pr"], da2in["pr"], da2in["pr"]]
        da2in_temp["life"]   = c_[da2in["life"], da2in["life"], da2in["life"]]
        da2in_temp["pgrad"]  = c_[da2in["pgrad"], da2in["pgrad"], da2in["pgrad"]]
        da2in_temp["wap"]    = c_[da2in["wap"], da2in["wap"], da2in["wap"]]

        da2in_temp["center"] = ma.masked_less(da2in_temp["pgrad"], 0.0).filled(0.0)
        da2in_temp["center"] = ma.masked_greater(da2in_temp["center"], 0.0).filled(1.0)

        for iy in ly:
          for ix in lx:

            #if da2in_temp["pgrad"][iy, ix] >=thgrad:
            if thgrad_min <= da2in_temp["pgrad"][iy, ix] < thgrad_max:

              i = i+1
              #--------------------------------
              da2out_temp = {}
              da2out_temp["pr"]   = zeros([2*rady+1, 2*radx+1], float32)
              da2out_temp["wap"]  = zeros([2*rady+1, 2*radx+1], float32)
              da2out_temp["temp"] = zeros([2*rady+1, 2*radx+1], float32)
              for dy in range(-rady, rady+1):
           
                iiy = iy + dy
                if (iiy <0) or (iiy > ny-1):
                  da2out_temp["pr"][rady + dy,:] = 0.0
                  da2out_temp["wap"][rady + dy,:] = 0.0
                  continue

                for dx in range(-radx, radx+1):
                  da2out_temp["temp"][rady + dy, radx + dx] = da2in_temp["center"][iiy, iix]

                  iix =ix + dx
                  da2out_temp["pr"][rady + dy, radx + dx] = da2in_temp["pr"][iiy, iix]
                  da2out_temp["wap"][rady + dy, radx + dx] = da2in_temp["wap"][iiy, iix]
              #--------------------------------
              da2out["pr"] = da2out["pr"] + da2out_temp["pr"]
              da2out["wap"] = da2out["wap"] + da2out_temp["wap"]
              da2out["temp"] = da2out["temp"] + da2out_temp["temp"]
              #----------------------------------
              plt.imshow(da2out_temp["pr"]*60*60*24.0, origin="lower", interpolation="nearest", vmax=15.0)
              plt.colorbar()

              name_temp = "./temp/pr.%s.%d.png"%(sreg,i)
              savefig(name_temp)
              clf()

#----------------------------------------------
da2out["pr"] = da2out["pr"] / i
da2out["wap"] = da2out["wap"] / i
da2out["temp"] = da2out["temp"] / i

plt.imshow(da2out["pr"]*60*60*24.0, origin="lower", interpolation="nearest", vmax=15.0)
plt.colorbar()
name_mean = "./temp/mean.pr.%s.png"%(sreg)
savefig(name_mean)
clf()
