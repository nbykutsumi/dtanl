###############################################
import os
import sys
import calendar
from glob import *
from netCDF4 import *
from numpy import *
#----------------------------------------------
lvar = ["prectot","ps","qv10m","t10m"]
#lvar = ["h","omega"]
#lvar = ["h","omega","prectot","ps","qv10m","t10m"]
lvarchange = ["prectot","ps","qv10m","slp","t10m"]
iy = 2001
ey = 2010
im = 1
em = 12
tstp = "day"
rmiss = -9999
lvar_2d = ["prectot", "ps", "qv10m", "slp", "t10m"]
lvar_3d = ["h", "omega"]
###############################################
def mk_dir(sdir):
  try:
    os.makedirs(sdir)
  except OSError:
    pass
#----------------------------------------------
def dumpheader(iname, nc, dims):
  ##########
  def a2s(a):
    s="\n".join(map(str, list(a))).strip()
    return s
  ##########
  def totext(filename, s):
    f = open(filename, "w")
    f.write(s)
    f.close()
  ##########
  os.system("ncdump -h %s > %s"%(iname, namedump))
  slat  = a2s( nc.variables["latitude"][:])
  slon  = a2s( nc.variables["longitude"][:])
  lenlat= len(nc.variables["latitude"][:])
  lenlon= len(nc.variables["longitude"][:])
  if dims == 3:
    slev  = a2s( nc.variables["levels"][:])
    lenlev = len(nc.variables["levels"][:])
  elif dims == 2:
    lenlev = 1

  sdims="lev %s\nlat %s\nlon %s"\
        %(lenlev, lenlat, lenlon)
  ###
  totext(namelat, slat)
  totext(namelon, slon)
  if dims == 3:
    totext(namelev, slev)
  totext(namedims, sdims)
  print namedump

###############################################
for var in lvar:
  #----------------------
  if var in lvar_2d:
    dims = 2
  elif var in lvar_3d:
    dims = 3
  else:
    sys.exit()
  #----------------------
  for y in range(iy, ey+1):
    #----------------
    # directories
    #----------------
    sidir = "/media/disk2/data/MERRA/nc/%s/%s"%(tstp, var)
    sncdir = "/media/disk2/data/MERRA/nc/%s/%s/%04d"%(tstp, var, y)
    sbndir = "/media/disk2/data/MERRA/bn/%s/%s/%04d"%(tstp, var, y)
    mk_dir(sncdir)
    mk_dir(sbndir)
    #--
    odir_dump = sbndir
    namedump  = odir_dump + "/ncdump.txt"
    namelon   = odir_dump + "/lon.txt"
    namelat   = odir_dump + "/lat.txt"
    namelev   = odir_dump + "/lev.txt"
    namedims  = odir_dump + "/dims.txt"
    #----------------
    for m in range(im, em+1):
      for d in range(1, calendar.monthrange(y,m)[1] +1):
      #for d in range(1, 1 +1):
        #-----------------------
        # move files to year directory
        #-----------------------
        sgzfile1 = sidir + "/*.%04d%02d%02d.SUB.nc.gz"%(y,m,d)
        sgzfile1 = glob(sgzfile1)
        if len(sgzfile1) == 1:
          sgzfile1 = sgzfile1[0]
          sgzfile2 = sncdir + "/" + sgzfile1.split("/")[-1]
          os.system("mv %s %s"%(sgzfile1,sgzfile2))
        #-----------------------
        # gunzip
        #-----------------------
        sgzfile2 = sncdir + "/*.%04d%02d%02d.SUB.nc.gz"%(y,m,d)
        sgzfile2 = glob(sgzfile2)
        if len(sgzfile2) == 1:
          sgzfile2 = sgzfile2[0]
          os.system("gunzip %s"%(sgzfile2))
        #-----------------------
        # rename NetCDF file
        #-----------------------
        sncfile0 = sncdir + "/*.%04d%02d%02d.SUB.nc"%(y,m,d)
        sncfile0 = glob(sncfile0)
        if len(sncfile0) == 1:
          sncfile0 = sncfile0[0]
          sncname  = sncfile0.split("/")[-1].split(".")[3]
          sncfile  = sncdir + "/MERRA.%s.%s.%s.%04d%02d%02d00.nc"%(sncname,tstp, var, y,m,d)
          if os.access(sncfile0, os.F_OK):
            os.rename(sncfile0, sncfile)
        #-----------------------
        # make ncdump_org
        #-----------------------
        sncfile  = sncdir + "/MERRA.*.%s.%s.%04d%02d%02d00.nc"%(tstp, var, y,m,d)
        sncfile  = glob(sncfile)
        #-----------
        # if sncfile does not exists, continue to next 
        #-----------
        if len(sncfile) == 0:
          print "nofile:" ,sncfile
          continue
        else:
          sncfile = sncfile[0]
        #-----------
        if ((m==1)&(d==1)):
          dumpname_org = sncdir + "/ncdump.org.txt"
          os.system("ncdump -h %s > %s"%(sncfile, dumpname_org))
          print dumpname_org
        #-----------------------
        # lats4d  # change resolution
        #-----------------------
        sncfile2 = sncfile[:-2] + "C.nc"
        if (var in lvarchange):
          if os.access(sncfile, os.F_OK):
            os.system("lats4d.sh  -i %s -merra1.25a -o %s > ./log.txt 2>&1"%(sncfile, sncfile2))
          print sncfile2
        #-----------------------
        # make binary file from NetCDF
        #-----------------------
        if ( var in lvarchange):
          snctemp = sncfile2
        else:
          snctemp = sncfile
        #----
        sbnname = "MERRA.%s.%s.%04d%02d%02d00.bn"%(tstp, var ,y,m,d)
        sbnfile = sbndir + "/%s"%(sbnname)
        if os.access(snctemp, os.F_OK):
          nc = Dataset(snctemp, "r", format="NETCDF")
          #---------------------
          # ncdump
          #---------------------
          if ((d == 1)&(m == 1)):
            dumpheader(snctemp, nc, dims)
          #---------------------
          ncdat = ma.filled(nc.variables[var][:], rmiss)
          ncdat.tofile(sbnfile)
          nc.close()
          print sbnfile
          #---------------------
          # remove --.C.nc
          #---------------------
          os.remove(snctemp)
