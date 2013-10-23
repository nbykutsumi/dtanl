from netCDF4 import *

idir = "/home/utsumi/mnt/iis.data2/CMIP5/cmip5.working/IPSL-CM5B-LR.historical"
iname = idir + "/va_6hrPlev_IPSL-CM5B-LR_historical_r1i1p1_1950010103-2005123121.nc"
iname = idir + "/ua_6hrPlev_IPSL-CM5B-LR_historical_r1i1p1_1950010103-2005123121.nc"

nc = Dataset(iname, "r")
cmiptime = nc.variables["time"]
flag=0
i   =50000
while flag==0:
  if cmiptime[i] ==0:
    print "last!!", i, cmiptime[i], num2date(cmiptime[i-1], units=cmiptime.units, calendar=cmiptime.calendar )
    flag = 1
  else:
    print i,cmiptime[i], cmiptime[i], num2date(cmiptime[i], units=cmiptime.units, calendar=cmiptime.calendar )
    i = i+1

