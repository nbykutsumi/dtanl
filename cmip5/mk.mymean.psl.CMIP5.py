from numpy import *
from netCDF4 import *
import datetime
import calendar, os
import cmip_para
#--------------
#lmodel=["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
#lmodel     = ["HadGEM2-ES","IPSL-CM5A-MR"]
lmodel     = ["MRI-CGCM3"]
#lexpr = ["historical","rcp85"]
lexpr = ["historical"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
##--------------


ny    = 180
nx    = 360
lmon  = range(1,12+1)

var        = "psl"
dattype    = "6hrPlev"
stepday    = 0.25  # 6-hour
imon       = 1
iday       = 1
#********************************************
def mk_dir(sdir):
  if not os.access(sdir , os.F_OK):
    os.mkdir(sdir)
#********************************************
#--------------------------------------------
for expr, model in [[expr,model] for expr in lexpr for model in lmodel]:
  ihour      = cmip_para.ret_lhour_6hr_cmip(model)[0]
  iyear,eyear = dyrange[expr]
  lyear = range(iyear,eyear+1)
  ens        = cmip_para.ret_ens(model, expr, var)
  sunit, scalendar = cmip_para.ret_unit_calendar(model,expr)
  #-- initialize  -----------------------------
  da2mean = {}
  for mon in range(0, 12+1):
    da2mean[mon] = zeros([ny, nx], float32)
  #--------------------------------------------
  dtimes  = {}
  for mon in range(0, 12+1):
    dtimes[mon] = 0
  #--------------------------------------------
  for year_loop in lyear:
    print model,expr,year_loop
    idtime  = datetime.datetime(year_loop,imon,iday,ihour)
    itnum   = date2num(idtime, sunit, scalendar)
    dtime   = idtime
    tnum    = itnum - stepday
    while 1==1:
      tnum  = tnum + stepday
      dtime = num2date(tnum, sunit, scalendar)
      year,mon,day,hour,min = dtime.year, dtime.month, dtime.day, dtime.hour, dtime.minute
      #-- check --
      if year != year_loop:
        break
      #-----------
      #print model,year,mon,day,hour,min
      #----
      idir_root  = "/media/disk2/data/CMIP5/sa.one.%s.%s/psl"%(model,expr)
      idir    =  idir_root + "/%04d%02d"%(year, mon)
      dtimes[0]     = dtimes[0] + 1
      dtimes[mon]   = dtimes[mon] + 1
  
      stime         = "%04d%02d%02d%02d%02d"%(year, mon, day, hour, min)
      iname         =  idir + "/%s.%s.%s.sa.one"%(var, ens, stime)
      a2in          = fromfile( iname , float32).reshape(ny, nx)
      da2mean[mon]  = da2mean[mon] + a2in
      da2mean[0]    = da2mean[0]   + a2in
  #------------------------------
  odir  = "/media/disk2/data/CMIP5/sa.one.%s.%s/psl.my.mean"%(model,expr)
  mk_dir(odir)
  for mon in range(0, 12+1):
    
    da2mean[mon] = da2mean[mon] / dtimes[mon]
    soname       = odir + "/%s.%s.%s.%s.0000%02d.sa.one"%(var,model,expr,ens, mon)
    da2mean[mon].tofile(soname)
    print soname
  
  #------------------------------
