from netCDF4 import *
from numpy import *
from myfunc_fsub import *
import os,sys
import cf
import calendar
import cmip_para
#####################################################
if len(sys.argv) >1:
  model = sys.argv[1]
  expr  = sys.argv[2]
  lmodel = [model]
  lexpr  = [expr]
else:
  #lmodel = ["NorESM1-M", "MIROC5", "CanESM2"]
  #lmodel = ["MIROC5","MRI-CGCM3","HadGEM2-ES"]
  lmodel = ["CCSM4"]
  #lexpr = ["historical","rcp85"]
  lexpr = ["historical"]
  #expr = "rcp85" #historical, rcp85
#--------------------
#lvar = ["sftlf"]
lvar = ["sftlf","orog"] # orog
tstp = "fx"
ny_one  = 180
nx_one  = 360
miss    = -9999.0
#####################################################
#####################################################
dlat_one = 1.0
dlon_one = 1.0
a1lat_one   = arange(-89.5, 89.5+dlat_one*0.1, dlat_one)
a1lon_one   = arange(0.5,  359.5+dlon_one*0.1, dlat_one)

#####################################################
for model in lmodel:
  for expr in lexpr:
    for var in lvar:
      #------------------
      odir_root ="/media/disk2/data/CMIP5/sa.one.%s.%s/%s"%(model, expr, var)
      odir_dump = odir_root
      #------------------
      ens = cmip_para.ret_ens(model, expr, var)
      #########################
      # set nc dir
      #########################
      #incdir = "/home/utsumi/mnt/export/nas_d/data/CMIP5/fx"
      incdir = "/home/utsumi/mnt/iis.data2/CMIP5/cmip5.working/%s.%s"%(model,expr)
      #########################
      ihead = var + "_" + tstp + "_" +model + "_" + expr +"_"\
             +ens
      ohead = "%s.%s"%(var,model)

      #####################################################
      odir_dump = odir_root
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
        #slat  = a2s( nc.variables["lat"][:])
        #slon  = a2s( nc.variables["lon"][:])
        #lenlat= len(nc.variables["lat"][:])
        #lenlon= len(nc.variables["lon"][:])
        slat  = a2s( a1lat_one)
        slon  = a2s( a1lon_one)
        lenlat= len( a1lat_one)
        lenlon= len( a1lon_one)

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
      odir = odir_root
      print odir
      try:
        os.makedirs(odir)
      except OSError:
        pass
      ########
      a1lat_org = nc.variables["lat"][:]
      a1lon_org = nc.variables["lon"][:]
      data = nc.variables["%s"%(var)][:]
      #*** Regrid ********
      upflag  = cmip_para.ret_upflag(model)
      if upflag == True:
        pergrid = 0 # per area (e.g. mm/m2), others (e.g, K, kg/kg, mm/s)
        #pergrid = 1 # per grid (e.g. km2/grid, population/grid)
        missflag  = 1
        ny_org    = len(a1lat_org)
        nx_org    = len(a1lon_org)
        data_one  = myfunc_fsub.upscale( data.T\
                        , a1lon_org, a1lat_org\
                        , a1lon_one, a1lat_one\
                        , pergrid, missflag, miss\
                        , nx_org, ny_org\
                        , nx_one, ny_one).T
      #-- downscale: Interpolation ----  
      elif upflag == False:
        data_one  = cf.biIntp(a1lat_org, a1lon_org, data, a1lat_one, a1lon_one)[0]
      #-------
      data_one  = array(data_one, float32)

      ########
      oname = odir + "/%s.sa.one"%(ohead)
      print oname
      ########
      f = open(oname, "wb")
      f.write(data_one)
      f.close()
