import sys, os
import cmip_func
from netCDF4 import *
#************************************
#lmodel    = ["MRI-CGCM3","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
#lmodel    = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
#lmodel    = ["CNRM-CM5","inmcm4","MPI-ESM-MR","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel    = ["MRI-CGCM3"]
lexpr     = ["historical","rcp85"]
#lexpr     = ["rcp85"]

idir_root = "/home/utsumi/mnt/iis.data2/CMIP5/cmip5.working"
miss      = -9999
#************************************
for model in lmodel:
  for expr in lexpr:
    idir   = idir_root + "/%s.%s"%(model, expr)

    sout  = ""
    #**************************
    #-- file list
    #--------------------------
    lsfile  = os.listdir(idir)
    lsfile.sort()
    #--------------------------
    for sfile in lsfile:
      #--------------
      if sfile[-3:] != ".nc":
        continue
      #-- split -----
      ldat       = sfile.split("_")
      if len(ldat) <2:
        continue
      #---------------
      var        = ldat[0]
      dattype    = ldat[1]
      model      = ldat[2]
      expr       = ldat[3]
      ens        = ldat[4]

      #--- skip "6hrLev" -----
      # without this part, "RuntimeError" is raised for MIROC5 rcp85
      if dattype == "6hrLev":
        continue
      #--------------------      
      print sfile
      #***************
      # cmiptime
      #---------------
      # fx
      #-----
      if dattype == "fx":
        date0  = miss
        date1  = miss
 
        scalendartype = "fx"
        fyear0,fmon0,fday0,fhour0,fmin0 = miss,miss,miss,miss,miss
        fyear1,fmon1,fday1,fhour1,fmin1 = miss,miss,miss,miss,miss
        sunits    = "None"
        scalendar = "None"
      #******************
      # others
      #-----
      else:
        try:
          nc         = Dataset(idir+"/"+sfile, "r", format="NETCDF")
          cmiptime = nc.variables["time"] 
          cmiptime0 = cmiptime[0]
          cmiptime1 = cmiptime[-1]
        
          date0  = num2date(cmiptime0, units=cmiptime.units, calendar=cmiptime.calendar)
          date1  = num2date(cmiptime1, units=cmiptime.units, calendar=cmiptime.calendar)

          #---------------------------
        except RuntimeError:
          print "error",sfile
          os.system("ls -l %s/%s"%(idir,sfile))
          sys.exit() 
        #-----------------------------
        fyear0,fmon0,fday0,fhour0,fmin0 = date0.year, date0.month, date0.day, date0.hour, date0.minute
        fyear1,fmon1,fday1,fhour1,fmin1 = date1.year, date1.month, date1.day, date1.hour, date1.minute
        sunits    = cmiptime.units
        scalendar = cmiptime.calendar
        #--
        sout_tmp = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"\
                 %(var, dattype, model, expr, ens\
                  ,fyear0,fmon0,fday0,fhour0,fmin0,date0\
                  ,fyear1,fmon1,fday1,fhour1,fmin1,date1\
                  ,sunits, scalendar, sfile)
        sout  = sout + sout_tmp
    #**********************
    #-- write to file -----
    odir    = "/home/utsumi/mnt/iis.data2/CMIP5/cmip5.working"
    soname  = odir + "/%s.%s.list.csv"%(model,expr)
    f       = open(soname, "w")
    f.write(sout)
    f.close()
    print soname






