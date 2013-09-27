from netCDF4 import *
from numpy import *
import os,sys
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
  tinc    = int(sys.argv[8])
  lev     = int(sys.argv[9])
else:
  print "*******************"
  print "BBBBBBBBBBBB"
  print "*******************"
  var   = "ua"
  model = "HadGEM2-ES"
  expr  = "historical"
  #ens   = "r1i1p1"
  ens   = "r2i1p1"
  year  = 1980
  mon   = 1
  dattype = "6hrPlev"
  tinc  = 6
  lev   =  850

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
  if dattype not in ["6hrLev"]:
    plev   = nc.variables["plev"][diz[lev]]
    #slev   = a2s( nc.variables["plev"][:])
    #lenlev = len(nc.variables["plev"][:])
    slev   = str(plev)
    lenlev = 1
  else:
    lenlev = len(nc.variables["lev"][:])
  #--
  sdims="lev %s\nlat %s\nlon %s"\
        %(lenlev, lenlat, lenlon)
  ###
  totext(namelat, slat)
  totext(namelon, slon)
  if dattype not in["6hrLev"]:
    totext(namelev, slev)
  totext(namedims, sdims)
  print namedump
#####################################################
# diz
#------------------------------
diz = {}
diz[850]  = 0
diz[500]  = 1
diz[250]  = 2

#####################################################
odir_root ="/media/disk2/data/CMIP5/sa.one.%s.%s/%s"%(model, expr, var)
odir_dump = odir_root
#---------

#####################################################
# set dlyrange
#####################################################
llfileinfo = cmip_func.ret_filedate(var,dattype,model,expr,ens,year,mon,iday,0,0,year,mon,eday,23,59)

print "nc2one.atm.1lev.py",llfileinfo
for lfileinfo in llfileinfo:
  fyear0,fmon0,fday0,fhour0,fmin0,ftime0,fyear1,fmon1,fday1,fhour1,fmin1,ftime1,sunit,scalendar,ncname\
   = lfileinfo 
  print "nc2oane.atm.1lev.py", "BBB",lfileinfo
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
  if not os.access(iname, os.F_OK):
    print "No File", iname
    sys.exit()
  else:
    print iname
  #----
  nc = Dataset(iname, "r", format="NETCDF")
  #*********
  # a1tnum
  #---------
  #ntime     = shape(nc.variables["time"])[0]
  nctime    = nc.variables["time"]
  a1tnum    = nc.variables["time"][:]
  sunit     = nc.variables["time"].units
  scalendar = nc.variables["time"].calendar
  #####
  dumpdata(iname, nc)
  ny    = len(nc.variables["lat"][:])
  nx    = len(nc.variables["lon"][:])
  #--
  if dattype in ["6hrLev"]:
    nz  = len(nc.variables["lev"][:])
  else:
    nz  = len(nc.variables["plev"][:])
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
    data      = nc.variables["%s"%(var)][istep][diz[lev]]
    if type(data) == numpy.ma.core.MaskedArray:
      data = data.filled(miss)
  
    #- Interpolation --
    a1lat_org = nc.variables["lat"][:]
    a1lon_org = nc.variables["lon"][:]
    data_one  = cf.biIntp(a1lat_org, a1lon_org, data, a1lat_one, a1lon_one, miss=miss)[0]
    data_one  = array(data_one, float32)
   
    ########
    oname = odir + "/%s.%04dhPa.%s.%s.sa.one"%(var, lev, ens, stime)
    ########
    f = open(oname, "wb")
    f.write(data_one)
    f.close()
    print oname
    #-------------
    ##----------------
    ## make pa for 6hrLev
    ##----------------
    #if dattype in ["6hrLev"]:
    #  a1a    = nc.variables["a"][:]
    #  a1b    = nc.variables["b"][:]
    #  p0     = nc.variables["p0"][:]
    #  a2ps   = nc.variables["ps"][istep]
    #  ##
    #  a3a    = a1z_to_a3zyx(a1a, ny, nx)
    #  a3b    = a1z_to_a3zyx(a1b, ny, nx)
    #  a3p0   = ones([nz, ny, nx], float32) * p0
    #  a3ps   = mul_a2( a2ps, nz)
    #  ##
    #  a3pa   = a3a * a3p0 + a3b * a3ps
    #  a3pa   = array(a3pa, float32)
    #  #-- name -----------------
    #  odir_tail_pa = "pa" + "/" + dattype + "/"\
    #                 +model + "/" + expr +"/" +ens
    #  odir_pa      = odir_root + "/%s/%04d"%(odir_tail_pa, y)
  
    #  ihead_pa     = "pa" + "_" + dattype + "_" +model\
    #                 + "_" + expr +"_"+ens
    #  ohead_pa     = ihead_pa
    #  oname_pa  = odir_pa  + "/%s_%s.bn"%(ohead_pa, stime)
    #  try:
    #    os.makedirs(odir_pa)
    #  except OSError:
    #    pass 
    #  #-------------------------
    #  f = open(oname_pa, "wb")
    #  f.write(a3pa)
    #  f.close()
    #  print oname_pa 
