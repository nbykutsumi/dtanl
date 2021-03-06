from numpy import *
import netCDF4
import os, sys
import calendar, datetime
import cmip_para, cmip_func
#******************************************************
#******************************************************
#lmodel = ["HadGEM2-ES","IPSL-CM5A-MR"]
#lmodel=["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel = ["CCSM4"]
#lexpr  = ["historical","rcp85"]
#lexpr  = ["historical"]
lexpr  = ["historical"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
#------

#lvar   = ["ua","va"]
lvar   = ["va"]
plev   = 500

#****************************************************
lmon   = range(1,12+1)
nx     = 360
ny     = 180
stepday = 0.25
dw     = 3
ltnumdelta = arange(-dw, dw+stepday*0.1, stepday)
miss   = -9999.0
#####################################################
# Functions
#####################################################
def check_file(sname):
  if not os.access(sname, os.F_OK):
    print "no file:",sname
    sys.exit()
#####################################################
def mk_dir(sdir):
  try:
    os.makedirs(sdir)
  except:
    pass
#******************************************************
def date_slide(year,mon,day, daydelta):
  today       = datetime.date(year, mon, day)
  target      = today + datetime.timedelta(daydelta)
  targetyear  = target.year
  #***********
  if ( calendar.isleap(targetyear) ):
    leapdate   = datetime.date(targetyear, 2, 29)
    #---------
    if (target <= leapdate) & (leapdate < today):
      target = target + datetime.timedelta(-1)
    elif (target >= leapdate ) & (leapdate > today):
      target = target + datetime.timedelta(1)
  #-----------
  return target
  
#******************************************************

for expr, model, var in [[expr,model,var] for expr in lexpr for model in lmodel for var in lvar]:
  #----------------------
  iyear, eyear     = dyrange[expr]
  sunit, scalendar = cmip_para.ret_unit_calendar(model, expr)
  ens              = cmip_para.ret_ens(model,expr,var)
  a1dtime,a1tnum   = cmip_func.ret_times(iyear,eyear,lmon,sunit,scalendar,stepday,model=model)
  lhour            = cmip_para.ret_lhour_6hr_cmip(model)
  mhour            = lhour[1]  # middle time of day
  #----------------------
  for dtime, tnum in map(None, a1dtime, a1tnum):
    #*************
    year,mon,day,hour = dtime.year, dtime.month, dtime.day, dtime.hour

    #--- check hour --
    if hour != mhour:
      continue
    #-----------------
    stime      = "%04d%02d%02d0000"%(year,mon,day)
    #----
    idir_root  = "/media/disk2/data/CMIP5/sa.one.%s.%s/%s"%(model,expr,var)
    idir       =  idir_root + "/%04d%02d"%(year, mon)
    odir_root  = "/media/disk2/data/CMIP5/sa.one.%s.%s/%s.run.mean"%(model,expr,var)
    odir       = odir_root + "/%04d%02d"%(year, mon)
    mk_dir(odir)
    #***********
    #*********************
    # start running mean
    #*********************
    # dummy
    #********
    aout  = zeros(ny*nx)
    aout  = array( aout , float32)
    ntimes = 0
    #********
    for tnumdelta in ltnumdelta:
      tnumt      = tnum + tnumdelta
      dtimet     = netCDF4.num2date( tnumt, sunit, scalendar)
      yeart      = dtimet.year
      mont       = dtimet.month
      dayt       = dtimet.day
      hourt      = dtimet.hour
      #-------------------
      idir       = idir_root + "/%04d%02d"%(yeart,  mont)
      ntimes = ntimes + 1
      stimet     = "%04d%02d%02d%02d00"%(yeart, mont, dayt, hourt)
      iname  = idir + "/%s.%04dhPa.%s.%s.sa.one"%(var, plev, ens, stimet)
      if not os.access(iname, os.F_OK):
        print "no file", iname
        ntimes = ntimes - 1
        continue
      #--------------------
      # add 
      #--------------------
      ain   = ma.masked_equal(fromfile(iname, float32), miss)
      aout  = aout + ain
    #*****************
      aout    = ma.masked_array(aout / ntimes).filled(miss)
    oname  = odir + "/run.mean.%s.%04dhPa.%s.%s.sa.one"%(var, plev, ens, stime)
    print oname
    aout.tofile(oname)
  


