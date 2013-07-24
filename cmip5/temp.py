import cmip_func
from netCDF4 import *

idir  = "/home/utsumi/mnt/iis.data2/CMIP5/cmip5.working/MIROC5.historical"
iname = idir + "/" +"va_6hrPlev_MIROC5_historical_r1i1p1_1973010100-1973123118.nc"
nc    = Dataset(iname, "r", format="NETCDF")
time1 = nc.variables["time"][0]
time2 = nc.variables["time"][1]
time3 = nc.variables["time"][-1]

time1t = cmip_func.date2cmiptime(1973,1,1,0,0)
time2t = cmip_func.date2cmiptime(1973,1,1,6,0)
time3t = cmip_func.date2cmiptime(1973,12,31,18,0)

time1r = cmip_func.cmiptime2date(time1)
time2r = cmip_func.cmiptime2date(time2)
time3r = cmip_func.cmiptime2date(time3)


print time1, time1t, time1r
print time2, time2t, time2r
print time3, time3t, time3r

l = cmip_func.ret_filedate("ua","6hrPlev","MIROC5","historical","r1i1p1",1972,5,1,0,0,1973,5,5,0,0,noleapflag=True)
print l
