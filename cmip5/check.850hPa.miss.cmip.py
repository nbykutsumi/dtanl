from netCDF4 import *
from numpy import *
import os
#-------------------------------
lmodel    = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
#lmodel = ["MIROC5"]

ncdir_root = "/home/utsumi/mnt/iis.data2/CMIP5/cmip5.working"
miss  = -9999.0

sout  = ""
for model in lmodel:
  #------------------
  # NetCDF
  #------------------
  ncdir = ncdir_root + "/%s.historical"%(model)
  lfile = os.listdir(ncdir)
  for line in lfile:
    if line[:4] == "orog":
      #------------------
      # orog
      #------------------
      orogname = ncdir + "/%s"%(line)
      print orogname
    
      a2orog   = Dataset(orogname,"r").variables["orog"][:]
      maxorog  = a2orog.max()
      a2orog   = ma.masked_not_equal(a2orog,maxorog).filled(miss)
      ny,nx    = shape(a2orog)
      for iytmp in range(ny):
        for ixtmp in range(nx):
          if a2orog[iytmp,ixtmp] != miss:
            iy,ix = iytmp,ixtmp 
    #------------------

    if line[0:10] == "ta_6hrPlev":
      #----------------
      sitime  = line.split("_")[5]
      iyear   = int(sitime[:4])
      if iyear < 1980:
        continue
      #----------------

      ncname = ncdir + "/%s"%(line)
      nc    = Dataset(ncname)
      lta   = nc.variables["ta"][0][:,iy,ix]
      #------------------------
      # check time
      #------------------------
      ntime = nc.variables["time"][0]
      sunits = nc.variables["time"].units
      scalendar = nc.variables["time"].calendar
      ncdate = num2date(ntime, sunits, scalendar)
      year   = ncdate.year
      mon    = ncdate.month
      day    = ncdate.day
      hour   = ncdate.hour
      min    = ncdate.minute
      break
  ##------------------
  #bindir = "/media/disk2/data/CMIP5/sa.one.%s.historical/ta/%04d%02d"%(model,year,mon)
  #binname = bindir + "/ta.0850hPa.r1i1p1.%04d%02d%02d%02d%02d.sa.one"%(year,mon,day,hour,min)
  #if os.path.exists(binname):
  #  a2bin   = fromfile(binname,float32).reshape(180,360)
  #  vbin    = a2bin[iy,ix]
  #else:
  #  vbin    = ""
  #  print "nofile",binname
  ##------------------
  #stemp   = "%s,%s,"%(model,vbin) + ",".join( map(str,lta)) + "\n"
  stemp   = "%s,%s,"%(model,maxorog) + ",".join( map(str,lta)) + "\n"
  sout    = sout + stemp
#--------------------
print sout
