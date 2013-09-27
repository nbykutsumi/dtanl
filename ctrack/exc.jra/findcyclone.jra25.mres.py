from ctrack_fsub import *
from numpy import *
import calendar
import os, sys
#--------------------------------------------------
tstp        = "6hr"
hinc        = 6
iyear       = 1996
eyear       = 2012
imon        = 1
emon        = 12
nx          = 360
ny          = 180
miss        = -9999.0
thorog      = 1500.0     #[m]
#lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
#lmodel = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3","org"]
lmodel = ["org"]
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
for model in lmodel:
  #****************************************************
  # dir_root
  #---------------
  psldir_root     = "/media/disk2/data/JRA25/sa.one.%s/%s/PRMSL"%(model,tstp)
  pslmeandir_root = "/media/disk2/data/JRA25/sa.one.%s/my.mean/PRMSL"%(model)
  orogdir_root    = "/media/disk2/data/JRA25/sa.one.125/const/topo"
  axisdir_root    = psldir_root
  #-- out ---
  if model == "org":
    pmeandir_root   = "/media/disk2/out/JRA25/sa.one.anl_p/%s/pmean"%(tstp)
    pgraddir_root   = "/media/disk2/out/JRA25/sa.one.anl_p/%s/pgrad"%(tstp)
  else:
    pmeandir_root   = "/media/disk2/out/JRA25/sa.one.%s/%s/pmean"%(model,tstp)
    pgraddir_root   = "/media/disk2/out/JRA25/sa.one.%s/%s/pgrad"%(model,tstp)
  
  #****************************************************
  # read lat, lon data
  #----------------------
  #axisdir    = axisdir_root  + "/%04d%02d"%(iyear, imon)
  #latname    = axisdir  + "/lat.txt"
  #lonname    = axisdir  + "/lon.txt"
  #a1lat      = read_txtlist(latname)
  #a1lon      = read_txtlist(lonname)
  a1lat       = arange(-89.5,89.5+0.001, 1.0)
  a1lon       = arange(0.5,359.5+0.001,  1.0) 
  
  #****************************************************
  #  orog data
  #--------------
  orogdir  = orogdir_root
  orogname = orogdir       + "/topo.sa.one"
  a2orog   = fromfile(orogname, float32).reshape(ny, nx)
  #**************************************************
  # Mean Sea Level Pressure
  #------------------------
  pslmeanname = pslmeandir_root + "/anl_p.PRMSL.0000000000.sa.one"
  a2pslmean = fromfile(pslmeanname, float32).reshape(ny, nx)
  #------------------------
  for year in range(iyear, eyear+1):
    #---------
    for mon in range(imon, emon+1):
      #---------
      # dirs
      #---------
      psldir   = psldir_root   + "/%04d%02d"%(year, mon)
      pmeandir = pmeandir_root + "/%04d%02d"%(year, mon)
      pgraddir = pgraddir_root + "/%04d%02d"%(year, mon)
      mk_dir(pmeandir)
      mk_dir(pgraddir)
  
      ed = calendar.monthrange(year,mon)[1]
      ##############
      for day in range(1, ed+1):
      #for day in range(28, ed+1):
        for hour in range(0, 23+1, hinc):
          stimeh  = "%04d%02d%02d%02d"%(year,mon,day,hour)
          #***************************************
          #* names
          #---------------------------------------
          pslname   = psldir + "/anl_p.PRMSL.%s.sa.one"%(stimeh)
          check_file(pslname)
          pmeanname = pmeandir + "/pmean.%s.sa.one"%(stimeh)
          pgradname = pgraddir + "/pgrad.%s.sa.one"%(stimeh)
  
          #***************************************
          #***************************************
          # make pmean
          #***************************************
        
          a2psl   = fromfile(pslname,   float32).reshape(ny, nx)
          a2dpsl  = a2psl - a2pslmean
          a2dpsl   = ma.masked_where(a2orog > thorog , a2dpsl).filled(miss)
          findcyclone_out = ctrack_fsub.findcyclone_real(a2dpsl.T, a1lat, a1lon, -9999.0, miss)
          a2pgrad = findcyclone_out[1].T
          a2pgrad.tofile(pgradname)

          #a2pmean = findcyclone_out[0].T + a2pslmean
          #a2pmean.tofile(pmeanname)
  
          print pgradname



 
