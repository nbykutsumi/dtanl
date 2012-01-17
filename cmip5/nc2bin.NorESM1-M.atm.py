from netCDF4 import *
from numpy import *
import os
import calendar
#####################################################
odir_root ="/media/disk2/data/CMIP5/bn"
#####################################################
#var = "wap" #wap, zg, hur, hus
#lvar = ["wap", "zg"]
lvar = ["hur","ta"]
tstp = "day"
lmodel = ["NorESM1-M", "MIROC5", "CanESM2"]
#lmodel = ["MIROC5", "CanESM2"]
#expr = "historical" #historical, rcp85
#expr = "rcp85"
lexpr = ["historical", "rcp85"]
ens  = "r1i1p1"
#lyrange= [ [1990,1999] ]
#####################################################
# set dlyrange
#####################################################
dlyrange     = {}
#
dlyrange["NorESM1-M", "historical"]  = [[1990,1999]]
dlyrange["NorESM1-M", "rcp85"]       = [[2086,2095]]
#
dlyrange["MIROC5", "historical"]  = [[1990,1999]]
dlyrange["MIROC5", "rcp85"]       = [[2080,2089], [2090,2099]]
#
dlyrange["CanESM2", "historical"]  = [[1979,2005]]
dlyrange["CanESM2", "rcp85"]       = [[2081,2090], [2091,2100]]

#####################################################
#####################################################
# Function
#####################################################
def dumpdata(iname, nc):
  print namedump
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
  slev = a2s( nc.variables["plev"][:])
  lenlev=len(nc.variables["plev"][:])
  lenlat= len(nc.variables["lat"][:])
  lenlon= len(nc.variables["lon"][:])
  sdims="lev %s\nlat %s\nlon %s"\
        %(lenlev, lenlat, lenlon)
  ###
  totext(namelat, slat)
  totext(namelon, slon)
  totext(namelev, slev)
  totext(namedims, sdims)
  print namedump
#####################################################
#####################################################
for model in lmodel:
  for expr in lexpr:
    for var in lvar:
      #------------------------------
      # make heads and tails
      #------------------------------
      ihead = var + "_" + tstp + "_" +model + "_" + expr +"_"\
             +ens
      ohead = ihead
      odir_tail = var + "/" + tstp + "/" +model + "/" + expr +"/"\
             +ens
      odir_dump = odir_root + "/" +odir_tail
      #------------------------------
      # set dir for nc input
      #------------------------------
      #incdir = "/media/disk2/data/CMIP5/nc/day/NorESM1-M"
      incdir = "/media/disk2/data/CMIP5/nc/%s/%s"%(tstp, model)
      #------------------------------
      # make dump
      #------------------------------
      try:
        os.makedirs(odir_dump)
      except OSError:
        pass
      namedump = odir_dump +"/ncdump.txt"
      namelon  = odir_dump +"/lon.txt"
      namelat  = odir_dump +"/lat.txt"
      namelev = odir_dump +"/lev.txt"
      namedims  = odir_dump +"/dims.txt"
  
      #------------------------------
      lyrange = dlyrange[model, expr]
      for yrange in lyrange:
        y0 = yrange[0]
        y1 = yrange[1]
        ######
        itimerange="%04d0101-%04d1231"%(y0,y1)
        iname = "%s/%s_%s.nc"%(incdir, ihead, itimerange)
        #####
        print os.access(iname, os.F_OK)
        print iname
        nc = Dataset(iname, "r", format="NETCDF")
        #####
        dumpdata(iname, nc)
        #####
        istep = -1
        for y in range(y0, y1+1):
          print y
          #############
          odir = odir_root + "/%s/%04d"%(odir_tail, y)
          print odir
          try:
            os.makedirs(odir)
          except OSError:
            pass
          #############
          print odir
          for m in range(1,12+1):
            ##############
            # no leap
            ##############
            if (m==2)&(calendar.isleap(y)):
              ed = calendar.monthrange(y,m)[1] -1
            else:
              ed = calendar.monthrange(y,m)[1]
            ##############
            for d in range(1, ed + 1):
              istep = istep +1
              stime = "%04d%02d%02d%02d"%(y,m,d,0)
              ########
              data = nc.variables["%s"%(var)][istep]
              ########
              oname = odir + "/%s_%s.bn"%(ohead, stime)
              ########
              f = open(oname, "wb")
              f.write(data)
              f.close()
