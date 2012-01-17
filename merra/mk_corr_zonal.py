from numpy import *
import os
#--------------------------------------
iyear  = 2001
eyear  = 2010
imon = 1
emon = 12
moedel = "MERRA"
ny = 144
nx = 288
y0 = -89.375
dy = 1.25
lscaletype = ["swa","fromsurface"]
#--------------------------------------
#************************
def y2lat(iy, y0, dy):
  lat = y0 + iy*dy
  return lat 
#************************
def write_string(s, soname):
  f = open(soname, "w")
  f.write(s)
  f.close()
#************************
#open land-sea data
#-------------------
slandsea = "/media/disk2/data/MERRA/bn/const/MERRA.landsea.Cx.bn"
alandsea = fromfile(slandsea, float32).reshape(ny, nx)
#************************
sodir = "/media/disk2/out/MERRA/day/scales/validate/%04d-%04d/%02d-%02d"%(iyear, eyear, imon, emon)
#************************
for scaletype in lscaletype:
  #************************
  # output file name
  #------------------------
  #-----
  if scaletype == "swa":
    soname_all   = sodir + "/zonal.corr.pMERRA.%04d-%04d.%02d-%02d.csv"%(iyear, eyear, imon, emon)
    soname_land  = sodir + "/zonal.corr.pMERRA.%04d-%04d.%02d-%02d.land.csv"%(iyear, eyear, imon, emon)
  #-----
  elif scaletype == "fromsurface":
    soname_all   = sodir + "/zonal.corr.pMERRA.%04d-%04d.%02d-%02d.FS.csv"%(iyear, eyear, imon, emon)
    soname_land  = sodir + "/zonal.corr.pMERRA.%04d-%04d.%02d-%02d.FS.land.csv"%(iyear, eyear, imon, emon)
  #************************
  sidir_root = "/media/disk2/out/MERRA/day/scales/validate/%04d-%04d/%02d-%02d"%(iyear, eyear, imon, emon)
  #************************
  #**********************
  # corr map file name
  #----------------------
  if scaletype == "swa":
    scorrmap = sidir_root + "/corr.pMERRA.%04d-%04d.%02d-%02d.bn"%(iyear, eyear, imon, emon)
  #-------
  elif scaletype == "fromsurface":
    scorrmap = sidir_root + "/corr.pMERRA.%04d-%04d.%02d-%02d.FS.bn"%(iyear, eyear, imon, emon)
  #**********************
  # open corr map
  #----------------------
  acorr_all  = fromfile(scorrmap, float32).reshape(ny, nx)
  acorr_land = ma.masked_where(alandsea == 0.0, acorr_all)
  #**********************
  sout_all  = ""
  sout_land = ""
  for iy in range(ny):
    lat = y2lat( iy, y0, dy)
    sout_all  = sout_all  + "%s,%s,%.3f\n"%(iy, lat, mean(acorr_all[iy,:]) )
    sout_land = sout_land + "%s,%s,%.3f\n"%(iy, lat, mean(acorr_land[iy,:]) )
  #**********************
  # write
  #----------------------
  write_string(sout_all , soname_all)
  write_string(sout_land, soname_land)
  #----------------
  print soname_all
