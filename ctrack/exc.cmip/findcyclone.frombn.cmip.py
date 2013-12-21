from ctrack_fsub import *
from numpy import *
import calendar
import os, sys
import netCDF4
import ctrack_func, cmip_func
import ctrack_para, cmip_para
#--------------------------------------------------
#lmodel=["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3","MRI-CGCM3"]
lmodel=["IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3","MRI-CGCM3"]

#lmodel = ["HadGEM2-ES"]

#-----------
#lexpr  = ["historical","rcp85"]
#lexpr  = ["rcp85"]
lexpr  = ["historical"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
#-----------

lmon        = range(1,12+1)
nx_one      = 360
ny_one      = 180
miss        = -9999.0
thorog      = 1500.0     #[m]
stepday = 0.25
#####################################################
# functions
#####################################################
def ret_a1lat_bn(psldir_bn_root):
  iname = psldir_bn_root + "/lat.txt"
  f=open(iname, "r"); lines=f.readlines(); f.close()
  a1lat_bn = map(float, lines)
  return a1lat_bn
#####################################################
def ret_a1lon_bn(psldir_bn_root):
  iname = psldir_bn_root + "/lon.txt"
  f=open(iname, "r"); lines=f.readlines(); f.close()
  a1lon_bn = map(float, lines)
  return a1lon_bn
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
  ny_bn, nx_bn    = cmip_para.ret_nynx_cmip(model)
  #****************************************************
  # dir_root
  #---------------
  psldir_bn_root  = "/media/disk2/data/CMIP5/bn.%s.%s/psl"%(model,expr)
  psldir_one_root = "/media/disk2/data/CMIP5/sa.one.%s.%s/psl"%(model,expr)
  pslmeandir_root = "/media/disk2/data/CMIP5/bn.%s.%s/psl.my.mean"%(model,expr)
  orogdir_root    = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog"%(model,expr)


  #-- out ---
  pgraddir_root   = "/media/disk2/out/CMIP5/bn.sa.one.%s.%s/6hr/pgrad"%(model,expr)
  ctrack_func.mk_dir(pgraddir_root) 
  #****************************************************
  # lat, lon data
  #----------------------
  a1lat_bn    = ret_a1lat_bn(psldir_bn_root)
  a1lon_bn    = ret_a1lon_bn(psldir_bn_root)
  a1lat_one   = arange(-89.5,89.5+0.001, 1.0)
  a1lon_one   = arange(0.5,359.5+0.001,  1.0) 
  
  #****************************************************
  #  orog data
  #--------------
  orogdir  = orogdir_root
  orogname = orogdir       + "/orog.%s.sa.one"%(model)
  a2orog   = fromfile(orogname, float32).reshape(ny_one, nx_one)
  #**************************************************
  # Mean Sea Level Pressure
  #------------------------
  #pslmeanname = pslmeandir_root + "/psl.MIROC5.historical.r1i1p1.000000.sa.bn"
  pslmeanname = pslmeandir_root + "/psl.%s.%s.%s.000000.bn"%(model,expr,ens)
  a2pslmean_bn= fromfile(pslmeanname, float32).reshape(ny_bn, nx_bn)
  #************************
  # time loop
  #------------------------
  a1dtime,a1tnum  = cmip_func.ret_times(iyear,eyear,lmon,sunit,scalendar,stepday,model=model) 
  for dtime, tnum in map(None, a1dtime, a1tnum): 
    year,mon,day,hour = dtime.year, dtime.month, dtime.day, dtime.hour
    #---------
    # dirs
    #---------
    psldir_bn   = psldir_bn_root   + "/%04d%02d"%(year, mon)
    psldir_one  = psldir_one_root  + "/%04d%02d"%(year, mon)
    pgraddir = pgraddir_root + "/%04d%02d"%(year, mon)
    mk_dir(pgraddir)

    #***************************************
    #* names
    #---------------------------------------
    stimeh  = "%04d%02d%02d%02d00"%(year,mon,day,hour)

    pslname_bn   = psldir_bn  + "/psl.%s.%s.bn"    %(ens, stimeh)
    pslname_one  = psldir_one + "/psl.%s.%s.sa.one"%(ens, stimeh)
    check_file(pslname_bn)
    check_file(pslname_one)
    pgradname    = pgraddir   + "/pgrad.%s.%s.sa.one"%(ens, stimeh)
    #***************************************
    # find cyclone center
    #***************************************
    a2psl_bn  = fromfile(pslname_bn,   float32).reshape(ny_bn, nx_bn)
    a2dpsl_bn = a2psl_bn - a2pslmean_bn

    a2psl_one = fromfile(pslname_one, float32).reshape(ny_one, nx_one)
    #-- find potential C-center ---
    a2loc_one = ctrack_fsub.find_potcyclone_frombn(a2dpsl_bn.T, a1lat_bn, a1lon_bn, miss, miss).T

    #-- calc pgrad of each center --
    a2pgrad = ctrack_fsub.mk_grad_cyclone_saone(a2loc_one.T, a2psl_one.T, a1lat_one, a1lon_one, miss, miss).T

    #-------------------------------
    a2pgrad = ma.masked_where(a2orog > thorog, a2pgrad).filled(miss)
    a2pgrad.tofile(pgradname)
  
    print pgradname



 
