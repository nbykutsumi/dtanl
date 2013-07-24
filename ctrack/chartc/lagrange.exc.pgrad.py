from numpy import *
import os, calendar
import matplotlib.pyplot as plt
import cf
from ctrack_fsub import *
import ctrack_func
#*************************************************************
iyear     = 2004
eyear     = 2004
nx_org    = 360
ny_org    = 180
#lmodel = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
#lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3","test.1.5deg","test.10deg","test.5deg","test.3deg"]
lmodel = ["org"]
#lmodel = ["test.1.5deg","test.10deg","test.5deg","test.3deg"]
lmon      = [1,3,5,7,9,11]
#lmon      = [1]
iday      = 1
singleday = False
#singleday = True
#lhour     = [0, 12]
lhour     = [0,12]
var       = "PRMSL"
#var       = "UGRD"
plev      = 850
#---------------------
#---------------------
radkm         = 300.0  # analysis resolution [km]
lenout        = nx_org*ny_org * 0.1
#-------------------------------------------
miss          = -9999.0
#------------------------------------------
#*************************************************************
didir_root   = {}
#-------
odir   = "/media/disk2/out/obj.valid/exc.pgrad"
ctrack_func.mk_dir(odir)
#---- lat and lon data :original ----------

lat_org_first   = -89.5
lon_org_first   = 0.5
lat_org_last    = 89.5
lon_org_last    = 359.5
dlat_org        = 1.0
dlon_org        = 1.0

a1lat_org       = arange(lat_org_first, lat_org_last + dlat_org*0.5, dlat_org)
a1lon_org       = arange(lon_org_first, lon_org_last + dlon_org*0.5, dlon_org)
#------------------------------------------
def ret_nomiss(x):
  return x !=miss
def del_miss(a1v):
  return filter(ret_nomiss, a1v)

#------------------------------------------
imodel = -1
for model in lmodel:
  imodel = imodel + 1
  #---- dummy ------------------------------
  a1v  =  array([])
  #---------------------
  for year in range(iyear, eyear+1):
    for mon in lmon:
      print model, year, mon
      #----------
      dir_root = "/media/disk2/data/JRA25/sa.one.%s/6hr"%(model)
      #-----------------
      if singleday == True:
        eday = iday
      else:
        eday = calendar.monthrange(year,mon)[1]
      #-----------------
      for day in range(1, eday+1):
        for hour in lhour:
          #--- pos file --------
          posdir   = "/media/disk2/out/chart/ASAS/exc/%04d%02d"%(year, mon)
          posname  = posdir + "/front.ASAS.%04d.%02d.%02d.%02d.sa.one"%(year,mon,day,hour)
          a2pos    = ma.masked_equal(fromfile(posname, float32).reshape(ny_org,nx_org), 0.0).filled(miss)
          #--- name ------------
          diname          = {}
          diname["PRMSL"]  = dir_root + "/PRMSL/%04d%02d/anl_p.PRMSL.%04d%02d%02d%02d.sa.one"%(year,mon,year,mon,day,hour)
          #
          pslorgdir       = "/media/disk2/data/JRA25/sa.one.org/6hr/PRMSL/%04d%02d/"%(year,mon)
          pslorgname      = pslorgdir  + "/anl_p.PRMSL.%04d%02d%02d%02d.sa.one"%(year,mon,day,hour)
          #--- load ------------
          da2in           = {}
          da2in["PRMSL"]  = fromfile( diname["PRMSL"], float32).reshape(ny_org, nx_org)
          a2pslorg        = fromfile( pslorgname,      float32).reshape(ny_org, nx_org)
          #--- 
          a1v_tmp  = ctrack_fsub.check_pgrad_saone( da2in["PRMSL"].T, a2pslorg.T, a2pos.T, radkm, lenout, miss)
          a1v_tmp  = del_miss(a1v_tmp)
          a1v      = r_[a1v, a1v_tmp]
          
          #
  #-- make string data --
  a1v  = sort(a1v)
  num  = len(a1v)
  sout = "pgrad(hPa/300km),fraction\n"
  for i in range(len(a1v)):
    sout = sout + "%.3f,%.3f\n"%(a1v[i], float(i)/num)
  #-- write to file -----
  soname  = odir + "/cum.pgrad.%s.%04d-%04d.csv"%(model,iyear,eyear)
  f = open(soname, "w"); f.write(sout); f.close()
  print soname

