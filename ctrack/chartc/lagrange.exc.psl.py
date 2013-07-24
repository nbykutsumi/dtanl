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
lmodel = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3","test.1.5deg","test.10deg","test.5deg","test.3deg"]
#lmodel = ["HadGEM2-ES","IPSL-CM5B-LR"]
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
dkm           = 50.0  # analysis resolution [km]
lenout        = 40
#-------------------------------------------
miss          = -9999.0
#------------------------------------------
da2temp = {}
#*************************************************************
didir_root   = {}
#-------
odir_base      = "/media/disk2/out/obj.valid"

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
imodel = -1
for model in lmodel:
  imodel = imodel + 1
  #---- dummy ------------------------------
  a1sv   =  zeros(lenout)
  a1sv2  =  zeros(lenout)
  a1num  =  zeros(lenout)
  a1mv   =  zeros(lenout)
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
          if var != "PRMSL":
            diname[var]  = dir_root + "/%s/%04d%02d/anl_p.%s.%04dhPa.%04d%02d%02d%02d.sa.one"%(var,year,mon,var,plev,year,mon,day,hour)
        
          #--- load ------------
          da2in           = {}
          da2in["PRMSL"]  = fromfile( diname["PRMSL"], float32).reshape(ny_org, nx_org)
          da2in[var]      = fromfile( diname[var], float32).reshape(ny_org, nx_org)
          #print diname[var]
          #da2temp[imodel]  = da2in[var]
          #--- 
          lout  = ctrack_fsub.vs_dist_dv_saone( da2in[var].T, a2pos.T, dkm, lenout, miss)
          a1sv_tmp  = lout[0]
          a1sv2_tmp = lout[1]
          a1num_tmp = lout[2]
          #
          a1sv  = a1sv   + a1sv_tmp
          a1sv2 = a1sv2  + a1sv2_tmp
          a1num = a1num  + a1num_tmp
  
  #----------------------------------------------
  # S.D.
  #-------------------
  a1sv  = ma.masked_where(a1num==0.0, a1sv)
  a1vs2 = ma.masked_where(a1num==0.0, a1sv2)
  a1mv  = a1sv / a1num
  a1sd  = ( (a1sv2 -2.0*a1mv*a1sv + a1num*a1mv*a1mv)/a1num) **0.5
  
  
  #-- write to file --
  stitle = "dist(km),var,S.D\n"
  sout   = stitle
  for i in range(len(a1sv)):
    dist = dkm * i   # i = 0,1,2,...
    #-------------
    if a1num[i] == 0.0:
      mv   = miss
      sd   = miss
    elif var == "PRMSL":
      mv   = a1mv[i] *0.01
      sd   = a1sd[i] *0.01
    else:
      mv   = a1mv[i]
      sd   = a1sd[i]
    #-------------
    sout   = sout + "%04d,%f,%f\n"%(dist, mv, sd)
  #
  odir     = odir_base + "/exc.%s"%(var)
  ctrack_func.mk_dir(odir)
  csvname  = odir + "/%s.%s.%04d-%04d.csv"%(var,model,iyear,eyear)
  f = open(csvname,"w"); f.write(sout); f.close()
  print  csvname
