from numpy import *

#--------------------------------------------
def a_to_s(a1in, sep=" "):
  s   = (sep).join(map(str, a1in))
  return s
#--------------------------------------------
def ret_sline(smodel, dlat, dlon):
  a1lat  = arange(-90.0+dlat*0.5, 90.0-dlat*0.5+0.001, dlat)
  a1lon  = arange(0.0+dlon*0.5, 360.0-dlon*0.5+0.001, dlon)
  nlat   = len(a1lat)
  nlon   = len(a1lon)
  
  slat   = a_to_s(a1lat, " ")
  slon   = a_to_s(a1lon, " ")
  sline  = smodel + "," + svar + "," + "(%d %d)"%(nlat, nlon)\
          + "," + str(dlat) + "," + str(dlon) \
          + "," + slat + "," + slon\
          + "," + "-" + "," + "-" + "\n"
  return sline
#--------------------------------------------
odir = "/home/utsumi/mnt/iis.data1/utsumi/CMIP5"
svar = "psl"

sout   = ""
#--- 1.5deg --------
smodel = "test.1.5deg"
dlat   = 1.5
dlon   = 1.5
sline  = ret_sline(smodel, dlat, dlon)
sout   = sout + sline
#--- 3deg --------
smodel = "test.3deg"
dlat   = 3.0
dlon   = 3.0
sline  = ret_sline(smodel, dlat, dlon)
sout   = sout + sline
#--- 5deg --------
smodel = "test.5deg"
dlat   = 5.0
dlon   = 5.0
sline  = ret_sline(smodel, dlat, dlon)
sout   = sout + sline
#--- 10deg --------
smodel = "test.10deg"
dlat   = 10.0
dlon   = 10.0
sline  = ret_sline(smodel, dlat, dlon)
sout   = sout + sline


#
#-- save -----
slabel  = "model,var,(nlat nlon),mdlat,mdlon,lat,lon,dlat,dlon\n"
sout    = slabel + sout
soname  = odir   + "/list.test.csv"
f = open(soname, "w");    f.write(sout);    f.close();  print soname
