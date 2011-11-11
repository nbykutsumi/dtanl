from netCDF4 import *
from numpy import *
import os
import calendar
#####################################################
incdir = "/media/disk2/data/CMIP5/nc/day/NorESM1-M"
odir_root ="/media/disk2/data/CMIP5/bn"
#####################################################
lvar = ["sftlf"]
#var = "orog" # orog
tstp = "fx"
model = "NorESM1-M"
lexpr = ["historical","rcp85"]
#expr = "rcp85" #historical, rcp85
ens  = "r0i0p0"

for var in lvar:
  for expr in lexpr:
    ihead = var + "_" + tstp + "_" +model + "_" + expr +"_"\
           +ens
    ohead = ihead
    odir_tail = var + "/" + tstp + "/" +model + "/" + expr +"/"\
           +ens
    #####################################################
    odir_dump = odir_root + "/" +odir_tail
    try:
      os.makedirs(odir_dump)
    except OSError:
      pass
    namedump = odir_dump +"/ncdump.txt"
    namelon  = odir_dump +"/lon.txt"
    namelat  = odir_dump +"/lat.txt"
    namedims  = odir_dump +"/dims.txt"
    #####################################################
    # Function
    #####################################################
    def dumpdata(iname, nc):
      #if not os.access( namedump, os.F_OK):
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
      slat  = a2s( nc.variables["lat"][:])
      slon  = a2s( nc.variables["lon"][:])
      lenlat= len(nc.variables["lat"][:])
      lenlon= len(nc.variables["lon"][:])
      sdims="lev 1\nlat %s\nlon %s"\
            %(lenlat, lenlon)
      ###
      totext(namelat, slat)
      totext(namelon, slon)
      totext(namedims, sdims)
      print namedump
    #####################################################
    iname = "%s/%s.nc"%(incdir, ihead)
    print os.access(iname, os.F_OK)
    print iname
    nc = Dataset(iname, "r", format="NETCDF")
    #####
    dumpdata(iname, nc)
    #####
    odir = odir_root + "/%s"%(odir_tail)
    print odir
    try:
      os.makedirs(odir)
    except OSError:
      pass
    ########
    data = nc.variables["%s"%(var)][:]
    ########
    oname = odir + "/%s.bn"%(ohead)
    print oname
    ########
    f = open(oname, "wb")
    f.write(data)
    f.close()
