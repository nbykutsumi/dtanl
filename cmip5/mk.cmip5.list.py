import sys, os
import cmip_func
from netCDF4 import *
#************************************
lmodel    = ["MIROC5","CCSM4","CNRM-CM5","CSIRO-Mk3-6-0","GFDL-CM3","HadGEM2-ES","IPSL-CM5A-MR","IPSL-CM5B-LR","MPI-ESM-MR","NorESM1-M"]
#lexpr     = ["historical","rcp85"]
lexpr     = ["historical"]

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
      print sfile
      #***************
      # cmiptime
      #---------------
      if dattype == "fx":
        cmiptime0  = miss
        cmiptime1  = miss
      else:
        try:
          nc         = Dataset(idir+"/"+sfile, "r", format="NETCDF")
          cmiptime0  = nc.variables["time"][0]
          cmiptime1  = nc.variables["time"][-1]
          nc.close()
        except RuntimeError:
          print "error",sfile
          os.system("ls -l %s/%s"%(idir,sfile))
          sys.exit() 
      #******************
      # fx
      #-----
      if dattype == "fx":
        fyear0,fmon0,fday0,fhour0,fmin0 = miss,miss,miss,miss,miss
        fyear1,fmon1,fday1,fhour1,fmin1 = miss,miss,miss,miss,miss
      #******************
      # others
      #-----
      else:
        fyear0,fmon0,fday0,fhour0,fmin0 = cmip_func.cmiptime2date(cmiptime0, noleapflag=True)
        fyear1,fmon1,fday1,fhour1,fmin1 = cmip_func.cmiptime2date(cmiptime1, noleapflag=True)

        ##-- date -------
        #sdate      = ldat[5].split(".")[0]
        #sdate0     = sdate.split("-")[0]
        #sdate1     = sdate.split("-")[1]
        ##
        #fyear0  = int(sdate0[:4])
        #fmon0   = int(sdate0[4:6])
        #fyear1  = int(sdate1[:4])
        #fmon1   = int(sdate1[4:6])
        ##-------
        ##if dattype in ["Amon"]:
        #if len(sdate0) == 6:
        #  fday0   = miss
        #  fhour0  = miss
        #  fmin0   = miss
        #  fday1   = miss
        #  fhour1  = miss
        #  fmin1   = miss
        ##elif dattype in ["day"]:
        #elif len(sdate0) == 8:
        #  fday0   = int(sdate0[6:8])
        #  fhour0  = miss
        #  fmin0   = miss
        #  fday1   = int(sdate1[6:8])
        #  fhour1  = miss
        #  fmin1   = miss
        ##elif dattype in ["3hr"]:
        #elif len(sdate0) == 12:
        #  fday0   = int(sdate0[6:8])
        #  fhour0  = int(sdate0[8:10])
        #  fmin0   = int(sdate0[10:12])
        #  fday1   = int(sdate1[6:8])
        #  fhour1  = int(sdate1[8:10])
        #  fmin1   = int(sdate1[10:12])
        ##else:
        #elif len(sdate0) == 10:
        #  fday0   = int(sdate0[6:8])
        #  fhour0  = int(sdate0[8:10])
        #  fmin0   = miss
        #  fday1   = int(sdate1[6:8])
        #  fhour1  = int(sdate1[8:10])
        #  fmin1   = miss
        ##-------
        sout_tmp = "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"\
                 %(var, dattype, model, expr, ens\
                  ,fyear0,fmon0,fday0,fhour0,fmin0,cmiptime0\
                  ,fyear1,fmon1,fday1,fhour1,fmin1,cmiptime1\
                  ,sfile)
        sout  = sout + sout_tmp
    #**********************
    #-- write to file -----
    odir    = "/home/utsumi/mnt/iis.data2/CMIP5/cmip5.working"
    soname  = odir + "/%s.%s.list.csv"%(model,expr)
    f       = open(soname, "w")
    f.write(sout)
    f.close()
    print soname






