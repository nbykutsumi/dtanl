import cmip_func
import cmip_para
import netCDF4
import datetime, sys

model   = "HadGEM2-ES"
sunit, scalendar = cmip_para.ret_unit_calendar(model, "historical")
print sunit, scalendar

stepday = 0.25
lmon  = [1,2,3]
a1dtime, a1tnum = cmip_func.ret_times(1995,1996,lmon, sunit,scalendar,stepday)

print a1dtime
