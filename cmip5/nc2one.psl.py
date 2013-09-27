from netCDF4 import *
from numpy import *
import os,sys
import calendar, datetime
import cf
import cmip_func
#####################################################
#####################################################
if len(sys.argv) > 1:
  var     = "psl"
  model   = sys.argv[1]
  expr    = sys.argv[2]
  ens     = sys.argv[3]
  year    = int(sys.argv[4])
  mon     = int(sys.argv[5])
  dattype = "6hrPlev"
  tinc    = 6
else:
  print "*******************"
  print "BBBBBBBBBBBB"
  print "*******************"
  var   = "psl"
  model = "MIROC5"
  expr  = "historical"
  ens   = "r1i1p1"
  year  = 1995
  mon   = 1
  dattype = "6hrPlev"
  tinc  = 6
#--------------
iday  = 1
eday  = calendar.monthrange(year,mon)[1]
lyear = [year]
lmon  = [mon]

miss    = -9999.0
ny_one  = 180
nx_one  = 360
#####################################################
dlat_one = 1.0
dlon_one = 1.0
a1lat_one   = arange(-89.5, 89.5+dlat_one*0.1, dlat_one)
a1lon_one   = arange(0.5,  359.5+dlon_one*0.1, dlat_one)

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
  #slat  = a2s( nc.variables["lat"][:])
  #slon  = a2s( nc.variables["lon"][:])
  #lenlat= len(nc.variables["lat"][:])
  #lenlon= len(nc.variables["lon"][:])
  slat  = a2s( a1lat_one)
  slon  = a2s( a1lon_one)
  lenlat= len( a1lat_one)
  lenlon= len( a1lon_one)

  ##--
  #if dattype not in ["6hrLev"]:
  #  plev   = nc.variables["plev"][diz[lev]]
  #  #slev   = a2s( nc.variables["plev"][:])
  #  #lenlev = len(nc.variables["plev"][:])
  #  slev   = str(plev)
  #  lenlev = 1
  #else:
  #  lenlev = len(nc.variables["lev"][:])
  ##--
  sdims="lev 1\nlat %s\nlon %s"\
        %(lenlat, lenlon)
  ###
  totext(namelat, slat)
  totext(namelon, slon)
  print namedump
#####################################################
odir_root ="/media/disk2/data/CMIP5/sa.one.%s.%s/%s"%(model, expr, var)
odir_dump = odir_root
#---------

#####################################################
# set dlyrange
#####################################################
llfileinfo = cmip_func.ret_filedate(var,dattype,model,expr,ens,year,mon,iday,0,0,year,mon,eday,23,59)

print llfileinfo
for lfileinfo in llfileinfo:
  fyear0,fmon0,fday0,fhour0,fmin0,ftime0,fyear1,fmon1,fday1,fhour1,fmin1,ftime1,sunit,scalendar,ncname\
   = lfileinfo 
  print lfileinfo
  #------
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
  namedims = odir_dump +"/dims.txt"
  
  #------------------------------
  ######
  iname = incdir + "/" + ncname
  #####
  if not os.access(iname, os.F_OK):
    print "NoFile", iname
    sys.exit()
  else:
    print iname
  nc = Dataset(iname, "r", format="NETCDF")
  #*********
  # a1tnum
  #---------
  nctime    = nc.variables["time"]
  a1tnum    = nc.variables["time"][:]
  sunit     = nc.variables["time"].units
  scalendar = nc.variables["time"].calendar
  #####
  dumpdata(iname, nc)
  ny    = len(nc.variables["lat"][:])
  nx    = len(nc.variables["lon"][:])
  #--
  ################
  for tnum in a1tnum:
    time     = num2date(tnum, units=sunit, calendar=scalendar)
    year_tmp = time.year
    mon_tmp  = time.month
    day_tmp  = time.day
    hour_tmp = time.hour
    min_tmp = time.minute
    #############
    if ((year_tmp not in lyear) or (mon_tmp not in lmon)):
      continue
    ##############
    istep         = date2index(time, nctime, calendar=nctime.calendar)
 
    #############
    odir = odir_root + "/%04d%02d"%(year_tmp,mon_tmp)
    print odir
    try:
      os.makedirs(odir)
    except OSError:
      pass
    #############
    stime = "%04d%02d%02d%02d%02d"%(year_tmp,mon_tmp,day_tmp,hour_tmp,min_tmp)
    ########
    data      = nc.variables["%s"%(var)][istep]
    if type(data) == numpy.ma.core.MaskedArray:
      data = data.filled(miss)
  
    #- Interpolation --
    a1lat_org = nc.variables["lat"][:]
    a1lon_org = nc.variables["lon"][:]
    data_one  = cf.biIntp(a1lat_org, a1lon_org, data, a1lat_one, a1lon_one, miss=miss)[0]
    data_one  = array(data_one, float32)
   
    ########
    oname = odir + "/%s.%s.%s.sa.one"%(var, ens, stime)
    ########
    f = open(oname, "wb")
    f.write(data_one)
    f.close()
    print oname
    #-------------

