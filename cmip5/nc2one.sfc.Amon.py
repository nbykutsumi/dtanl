from netCDF4 import *
from numpy import *
from myfunc_fsub import *
import os, sys
import calendar, datetime
import cf
import cmip_func, cmip_para
#####################################################
#####################################################
if len(sys.argv) > 1:
  var     = sys.argv[1]
  model   = sys.argv[2]
  expr    = sys.argv[3]
  ens     = sys.argv[4]
  iyear    = int(sys.argv[5])
  eyear    = int(sys.argv[6])
else:
  print "*******************"
  print "BBBBBBBBBBBB"
  print "*******************"
  var   = "ts"
  model = "MRI-CGCM3"
  expr  = "historical"
  ens   = "r1i1p1"
  iyear  = 1980
  eyear  = 1999

#--------------
dattype = "Amon"
#--------------
lyear = range(iyear,eyear+1)

miss    = -9999.0
ny_one  = 180
nx_one  = 360
#####################################################
dlat_one = 1.0
dlon_one = 1.0
a1lat_one   = arange(-89.5, 89.5+dlat_one*0.1, dlat_one)
a1lon_one   = arange(0.5,  359.5+dlon_one*0.1, dlat_one)
#****************************
#####################################################
# Function
#####################################################
def mul_a2(a2, n):
  (ny, nx) = shape(a2)
  #----
  l  = a2.flatten().tolist() * n
  a3 = array(l).reshape(n, ny, nx)
  return a3
#-----------------------
def a1z_to_a3zyx(a1, ny, nx):
  nz = len(a1)
  l  = a1.tolist() * nx*ny
  a3 = array(l).reshape(nx,ny,nz).T
  return a3
#-----------------------
def dumpdata(iname, nc):
  print "namedump",namedump
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

  #--
  lenlev = 1
  #--
  sdims="lev %s\nlat %s\nlon %s"\
        %(lenlev, lenlat, lenlon)
  ###
  totext(namelat, slat)
  totext(namelon, slon)
  totext(namedims, sdims)
  print "namedump",namedump
#####################################################
odir_root ="/media/disk2/data/CMIP5/sa.one.%s.%s/%s"%(model, expr, var)
odir_dump = odir_root
#---------
#####################################################
# set dlyrange
#####################################################
llfileinfo = cmip_func.ret_filedate(var,dattype,model,expr,ens,iyear,1,1,0,0,eyear,12,31,23,59)


print "fileinfo",llfileinfo
for lfileinfo in llfileinfo:
  #fyear0,fmon0,fday0,fhour0,fmin0,fcmiptime0,fyear1,fmon1,fday1,fhour1,fmin1,fcmiptime1,ncname\
  fyear0,fmon0,fday0,fhour0,fmin0,ftime0,fyear1,fmon1,fday1,fhour1,fmin1,ftime1,sunit,scalendar,ncname\
   = lfileinfo 
  print "fileinfo",lfileinfo
  #------
  #time0 = datetime.datetime(fyear0,fmon0,fday0,fhour0,fmin0)
  time0 = ftime0
  #------------------------------
  # make heads 
  #------------------------------
  ihead = var + "_" + dattype + "_" +model + "_" + expr +"_" +ens
    
  #------------------------------
  # set dir for nc input
  #------------------------------
  incdir = "/home/utsumi/mnt/iis.data2/CMIP5/cmip5.working/%s.%s"%(model,expr)
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
  namelev  = odir_dump +"/lev.txt"
  namedims = odir_dump +"/dims.txt"
  
  #------------------------------
  #itimerange="%04d%02d%02d%02d-%04d%02d%02d%02d"%(fyear0,fmon0,fday0,fhour0,fyear1,fmon1,fday1,fhour1)
  ######
  #iname = "%s/%s_%s.nc"%(incdir, ihead, itimerange)
  iname = incdir + "/" + ncname
  #####
  if os.access(iname, os.F_OK):
    print "fileinfo=", iname
  else:
    print "nofile",iname
    sys.exit()
  nc = Dataset(iname, "r", format="NETCDF")
  #*********
  # ntime
  #---------
  nctime = nc.variables["time"]
  sunit  = nctime.units
  scalendar = nctime.calendar
  a1tnum = nctime[:]

  #####
  dumpdata(iname, nc)
  ny    = len(nc.variables["lat"][:])
  nx    = len(nc.variables["lon"][:])
  #--
  #####
  istep = -1
  #--------------------
  for tnum in a1tnum:
    ##############
    # check cmiptime & file name time
    #-------------
    dtime    = num2date(tnum, units=sunit, calendar=scalendar)
    year_tmp = dtime.year
    mon_tmp  = dtime.month
    day_tmp  = dtime.day
    hour_tmp = dtime.hour  
    #############
    if (year_tmp not in lyear):
      continue

    #############
    odir = odir_root + "/%04d"%(year_tmp)
    print odir
    try:
      os.makedirs(odir)
    except OSError:
      pass
    #############
    stime = "%04d%02d%02d%02d%02d"%(year_tmp,mon_tmp,0,0,0)
    ########
    data      = nc.variables["%s"%(var)][istep]
    if type(data) == numpy.ma.core.MaskedArray:
      data = data.filled(miss)
  
    #- Interpolation --
    a1lat_org = nc.variables["lat"][:]
    a1lon_org = nc.variables["lon"][:]
    upflag  = cmip_para.ret_upflag(model)
    #-- upscale ------
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

    #-- downscale: Interpolation --
    elif upflag == False:
      data_one  = cf.biIntp(a1lat_org, a1lon_org, data, a1lat_one, a1lon_one, miss=miss)[0]
    #-------
    data_one  = array(data_one, float32)
   
    ########
    oname = odir + "/%s.%s.%s.sa.one"%(var, ens, stime)
    ########
    f = open(oname, "wb")
    f.write(data_one)
    f.close()
    print oname

