from netCDF4 import *
from numpy import *
import os
#--------------------------
lvar_6hrPlev_upper  = ["ua","va","ta"]
lvar_6hrPlev_sfc    = ["psl"]
#--------------------------------------------
def a_to_s(a1in, sep=" "):
  s   = (sep).join(map(str, a1in))
  return s
#------
def mk_a1dif(a1in):
  a1in1 = a1in[:-1]
  a1in2 = a1in[1:]
  a1dif = a1in2 - a1in1
  return a1dif
#--------------------------------------------
idir  = "/home/utsumi/mnt/iis.data1/utsumi/CMIP5"

##***************************************
## 6hrPlev upper
##------------------
#sout  = ""
#for root, dirs, files in os.walk(idir):
#  for sfile in files:
#    if sfile[-3:] == ".nc":
#      #-- check type ----
#      svar   = sfile.split("_")[0]      
#      stype  = sfile.split("_")[1]
#      smodel = sfile.split("_")[2] 
#      #---
#      iname  = root + "/%s"%(sfile)
#      #------------
#      if ((stype == "6hrPlev")&(svar in lvar_6hrPlev_upper)):
#        nc     = Dataset(iname, "r", format="NETCDF")
#        a1lat  = nc.variables["lat"][:]
#        a1lon  = nc.variables["lon"][:]
#        a1plev = nc.variables["plev"][:]
#        #
#        slat   = a_to_s(a1lat,  " ")
#        slon   = a_to_s(a1lon,  " ")
#        splev  = a_to_s(a1plev, " ")
#        #
#        sdlat  = a_to_s( mk_a1dif(a1lat), " ")
#        sdlon  = a_to_s( mk_a1dif(a1lon), " ")
#        #
#        mdlat  = mean(mk_a1dif(a1lat))
#        mdlon  = mean(mk_a1dif(a1lon))
#        #
#        nlat   = len(a1lat)
#        nlon   = len(a1lon)
#        nplev  = len(a1plev)
#        #
#        sline  = smodel + "," + svar + "," + "(%d %d %d)"%(nplev, nlat, nlon)\
#                + "," + str(mdlat) + "," + str(mdlon) \
#                + "," + splev + "," + slat + "," + slon \
#                + "," + sdlat + "," + sdlon + "\n"
#        #
#        sout   = sout + sline
##-- save -----
#slabel  = "model,var,(nplev nlat nlon),mdlat,mdlon,plev,lat,lon,dlat,dlon\n"
#sout    = slabel + sout
#soname  = idir + "/list.6hrPlev.upper.csv"
#f = open(soname, "w");    f.write(sout);    f.close();  print soname

#***************************************
# 6hrPlev sfc
#------------------
sout  = ""
for root, dirs, files in os.walk(idir):
  for sfile in files:
    if sfile[-3:] == ".nc":
      #-- check type ----
      if len(sfile.split("_")) < 3:
        continue
      #------------------
      svar   = sfile.split("_")[0]      
      stype  = sfile.split("_")[1]
      smodel = sfile.split("_")[2] 
      #---
      iname  = root + "/%s"%(sfile)
      #------------
      if ((stype == "6hrPlev")&(svar in lvar_6hrPlev_sfc)):
        nc     = Dataset(iname, "r", format="NETCDF")
        a1lat  = nc.variables["lat"][:]
        a1lon  = nc.variables["lon"][:]
        #
        slat   = a_to_s(a1lat,  " ")
        slon   = a_to_s(a1lon,  " ")
        #
        sdlat  = a_to_s( mk_a1dif(a1lat), " ")
        sdlon  = a_to_s( mk_a1dif(a1lon), " ")
        #
        mdlat  = mean(mk_a1dif(a1lat))
        mdlon  = mean(mk_a1dif(a1lon))
        #
        nlat   = len(a1lat)
        nlon   = len(a1lon)
        #
        sline  = smodel + "," + svar + "," + "(%d %d)"%(nlat, nlon)\
                + "," + str(mdlat) + "," + str(mdlon) \
                + "," + slat + "," + slon\
                + "," + sdlat + "," + sdlon + "\n"
        #
        sout   = sout + sline
#-- save -----
slabel  = "model,var,(nlat nlon),mdlat,mdlon,lat,lon,dlat,dlon\n"
sout    = slabel + sout
soname  = idir + "/list.6hrPlev.sfc.csv"
f = open(soname, "w");    f.write(sout);    f.close();  print soname


