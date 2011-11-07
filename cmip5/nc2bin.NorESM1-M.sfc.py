from netCDF4 import *
from numpy import *
import os
import calendar
#####################################################
incdir = "/media/disk2/data/CMIP5/nc/day/NorESM1-M"
odir_root ="/media/disk2/data/CMIP5/bn"
#####################################################
#lvar = ["pr","psl","tas","rhs","huss"] #pr, psl, tas, rhs, huss
lvar = ["pr"]
tstp = "day"
model = "NorESM1-M"
#expr = "historical" #historical, rcp85
expr = "rcp85" #historical, rcp85
lexpr =["historical","rcp85"]
ens  = "r1i1p1"
#lyrange= [ [1950,1999] ]
#lyrange= [ [2056,2100] ]
dlyrange = {"historical":[[1950,1999]], "rcp85":[[2056,2100]]}
for expr in lexpr:
  lyrange = dlyrange[expr]
  print expr, lyrange
  for var in lvar:
    #####################################################
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
    #####################################################
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
