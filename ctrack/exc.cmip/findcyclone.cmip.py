from ctrack_fsub import *
from numpy import *
import calendar
import os, sys
import netCDF4, cmip_para, cmip_func
#--------------------------------------------------
#lmodel=["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]

lmodel = ["CCSM4"]

#-----------
#lexpr  = ["historical","rcp85"]
#lexpr  = ["rcp85"]
lexpr  = ["historical"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
#-----------

lmon        = range(1,12+1)
nx          = 360
ny          = 180
miss        = -9999.0
thorog      = 1500.0     #[m]
stepday = 0.25
#####################################################
# functions
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
#################################################
def mk_dir_tail(var, tstp, model, expr, ens):
  odir_tail = var + "/" + tstp + "/" +model + "/" + expr +"/"\
       +ens
  return odir_tail
#####################################################
def mk_namehead(var, tstp, model, expr, ens):
  namehead = var + "_" + tstp + "_" +model + "_" + expr +"_"\
       +ens
  return namehead
#****************************************************
def read_txtlist(iname):
  f = open(iname, "r")
  lines = f.readlines()
  f.close()
  lines = map(float, lines)
  aout  = array(lines, float32)
  return aout
#****************************************************
for expr, model in [[expr, model] for expr in lexpr for model in lmodel]:
  #---------------
  iyear, eyear     = dyrange[expr]
  ens              = cmip_para.ret_ens(model,expr,"psl")
  sunit, scalendar = cmip_para.ret_unit_calendar(model, expr)
  #****************************************************
  # dir_root
  #---------------
  psldir_root     = "/media/disk2/data/CMIP5/sa.one.%s.%s/psl"%(model,expr)
  pslmeandir_root = "/media/disk2/data/CMIP5/sa.one.%s.%s/psl.my.mean"%(model,expr)
  orogdir_root    = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog"%(model,expr)


  #-- out ---
  pgraddir_root   = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/pgrad"%(model,expr)
  
  #****************************************************
  # lat, lon data
  #----------------------
  a1lat       = arange(-89.5,89.5+0.001, 1.0)
  a1lon       = arange(0.5,359.5+0.001,  1.0) 
  
  #****************************************************
  #  orog data
  #--------------
  orogdir  = orogdir_root
  orogname = orogdir       + "/orog.%s.sa.one"%(model)
  a2orog   = fromfile(orogname, float32).reshape(ny, nx)
  #**************************************************
  # Mean Sea Level Pressure
  #------------------------
  #pslmeanname = pslmeandir_root + "/psl.MIROC5.historical.r1i1p1.000000.sa.one"
  pslmeanname = pslmeandir_root + "/psl.%s.%s.%s.000000.sa.one"%(model,expr,ens)
  a2pslmean = fromfile(pslmeanname, float32).reshape(ny, nx)
  #************************
  # time loop
  #------------------------
  a1dtime,a1tnum  = cmip_func.ret_times(iyear,eyear,lmon,sunit,scalendar,stepday,model=model) 
  for dtime, tnum in map(None, a1dtime, a1tnum): 
    year,mon,day,hour = dtime.year, dtime.month, dtime.day, dtime.hour
    #---------
    # dirs
    #---------
    psldir   = psldir_root   + "/%04d%02d"%(year, mon)
    pgraddir = pgraddir_root + "/%04d%02d"%(year, mon)
    mk_dir(pgraddir)

    #***************************************
    #* names
    #---------------------------------------
    stimeh  = "%04d%02d%02d%02d00"%(year,mon,day,hour)

    pslname   = psldir + "/psl.%s.%s.sa.one"%(ens, stimeh)
    check_file(pslname)
    pgradname = pgraddir + "/pgrad.%s.%s.sa.one"%(ens, stimeh)
    #***************************************
    # find cyclone center
    #***************************************
    
    a2psl   = fromfile(pslname,   float32).reshape(ny, nx)
    a2dpsl  = a2psl - a2pslmean
    a2dpsl   = ma.masked_where(a2orog > thorog , a2dpsl).filled(miss)
    findcyclone_out = ctrack_fsub.findcyclone_real(a2dpsl.T, a1lat, a1lon, -9999.0, miss)
    a2pgrad = findcyclone_out[1].T
    a2pgrad.tofile(pgradname)
  
    print pgradname



 
