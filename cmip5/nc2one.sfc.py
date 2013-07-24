from netCDF4 import *
from numpy import *
import os
import calendar, datetime
import cf
import cmip_func
#####################################################
#####################################################
if len(sys.argv) > 1:
  var     = sys.argv[1]
  model   = sys.argv[2]
  expr    = sys.argv[3]
  ens     = sys.argv[4]
  year    = int(sys.argv[5])
  mon     = int(sys.argv[6])
  dattype = sys.argv[7]
else:
  print "*******************"
  print "BBBBBBBBBBBB"
  print "*******************"
  var   = "pr"
  model = "MIROC5"
  expr  = "historical"
  ens   = "r1i1p1"
  year  = 1996
  mon   = 2
  dattype = "3hr"

#--------------
noleapflag = True
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
#****************************
if dattype == "3hr":
  tinc = 3
elif dattype == "6hrPlev":
  tinc = 6
else:
  print "check dattype and tinc"
  sys.exit()
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

  #--
  lenlev = 1
  #--
  sdims="lev %s\nlat %s\nlon %s"\
        %(lenlev, lenlat, lenlon)
  ###
  totext(namelat, slat)
  totext(namelon, slon)
  totext(namedims, sdims)
  print namedump
#####################################################
odir_root ="/media/disk2/data/CMIP5/sa.one.%s.%s/%s"%(model, expr, var)
odir_dump = odir_root
#---------

#####################################################
# set dlyrange
#####################################################
llfileinfo = cmip_func.ret_filedate(var,dattype,model,expr,ens,year,mon,iday,0,0,year,mon,eday,23,59,noleapflag)

print llfileinfo
for lfileinfo in llfileinfo:
  fyear0,fmon0,fday0,fhour0,fmin0,fcmiptime0,fyear1,fmon1,fday1,fhour1,fmin1,fcmiptime1,ncname\
   = lfileinfo 
  print lfileinfo
  #------
  time0 = datetime.datetime(fyear0,fmon0,fday0,fhour0,fmin0)
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
  print os.access(iname, os.F_OK)
  print "iname=", iname
  nc = Dataset(iname, "r", format="NETCDF")
  #*********
  # ntime
  #---------
  ntime  = shape(nc.variables["time"])[0]

  #####
  dumpdata(iname, nc)
  ny    = len(nc.variables["lat"][:])
  nx    = len(nc.variables["lon"][:])
  #--
  #####
  istep = -1
  istep_withleap = -1
  #--------------------
  while istep <= ntime:
    istep_withleap = istep_withleap + 1
    time = time0 + datetime.timedelta(hours=istep_withleap *tinc)
    year_tmp = time.year
    mon_tmp  = time.month
    day_tmp  = time.day
    hour_tmp = time.hour
    min_tmp  = time.minute
  
    ##############
    # no leap
    ##############
    if (calendar.isleap(year_tmp))& (mon_tmp == 2)&(day_tmp==29):
      continue
    ##############
    istep = istep + 1
    #############
    if ((year_tmp not in lyear) or (mon_tmp not in lmon)):
      continue
    ##############
    # check cmiptime & file name time
    #-------------
    cmiptime_tmp  = nc.variables["time"][istep]

    year_cmip, mon_cmip, day_cmip, hour_cmip, min_cmip\
       = cmip_func.cmiptime2date(cmiptime_tmp, noleapflag=True)

    if not (year_cmip, mon_cmip, day_cmip, hour_cmip, min_cmip\
       == year_tmp, mon_tmp, day_tmp, hour_tmp, min_tmp):
      print "not much in time"
      print "time_cmip",year_cmip, mon_cmip, day_cmip, hour_cmip, min_cmip
      print "time_tmp ",year_tmp, mon_tmp, day_tmp, hour_tmp, min_tmp 
      sys.exit()
    #############
    odir = odir_root + "/%04d%02d"%(year_tmp,mon_tmp)
    print odir
    try:
      os.makedirs(odir)
    except OSError:
      pass
    #############
    stime = "%04d%02d%02d%02d%02d"%(year_tmp,mon_tmp,day_tmp,hour_tmp, min_tmp)
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
    oname = odir + "/%s.%s.%s.%s.%s.sa.one"%(var, model, expr, ens, stime)
    ########
    f = open(oname, "wb")
    f.write(data_one)
    f.close()
    print oname

