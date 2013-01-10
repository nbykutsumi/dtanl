import os, sys
from numpy import *

#####################################################
#####################################################
def xy2fortpos(ix, iy, nx):
  number = iy* nx + ix +1
  return number
#####################################################
def fortpos2xy(number, nx, miss_int):
  if (number == miss_int):
    iy0 = miss_int
    ix0 = miss_int
  else:
    iy0 = int(number/nx)         # iy0 = 0, 1, 2, ..
    ix0 = number - nx*iy0 -1     # ix0 = 0, 1, 2, ..
  #----
  return ix0, iy0
#####################################################
def check_file(sname):
  if not os.access(sname, os.F_OK):
    print "no file:",sname
    sys.exit()
#####################################################
def mk_dir(sdir):
  try:
    os.makedirs(sdir)
  except:
    pass
#################################################
def mk_dir_tail(var, tstp, model, expr, ens):
  odir_tail = var + "/" + tstp + "/" +model + "/" + expr +"/"\
       +ens
  return odir_tail
#####################################################
def mk_namehead(var, tstp, model, expr, ens):
  namehead = var + "_" + tstp + "_" +model + "_" + expr +"_"\
       +ens
  return namehead
#******************************************************
def date_slide(year,mon,day, daydelta):
  today       = datetime.date(year, mon, day)
  target      = today + datetime.timedelta(daydelta)
  targetyear  = target.year
  #***********
  if ( calendar.isleap(targetyear) ):
    leapdate   = datetime.date(targetyear, 2, 29)
    #---------
    if (target <= leapdate) & (leapdate < today):
      target = target + datetime.timedelta(-1)
    elif (target >= leapdate ) & (leapdate > today):
      target = target + datetime.timedelta(1)
  #-----------
  return target
#****************************************************
def read_txtlist(iname):
  f = open(iname, "r")
  lines = f.readlines()
  f.close()
  lines = map(float, lines)
  aout  = array(lines, float32)
  return aout
#****************************************************
def solvelife_point_py(number, miss_int):
  #pmin = int(number / 10000)
  #dura = number - pmin *10000
  if (number == miss_int):
    dura   = miss_int
    pgmax  = miss_int
  else:
    dura = int(number / 1000000)
    pgmax = number - dura*1000000
  #----
  return (pgmax, dura)
#**************************************************
# make area [km2] map
def cal_area(lat1, lat2, dlon):
  lat1  = pi * abs(lat1) / 180.   # [deg] -> [rad]
  lat2  = pi * abs(lat2) / 180.   # [deg] -> [rad]
  dlon  = pi * dlon / 180.        # [deg] -> [rad]
  r     = 6379.136  #[km]
  ecc2  = 0.00669447
  ecc   = sqrt(ecc2)
  f1 = 0.5 * sin(lat1) / (1 - ecc2 * sin(lat1) * sin(lat1))\
      + 0.25 /ecc * log( abs((1 + ecc* sin(lat1))/(1- ecc* sin(lat1))) )

  f2 = 0.5 * sin(lat2) / (1 - ecc2 * sin(lat2) * sin(lat2))\
      + 0.25 /ecc * log( abs((1 + ecc* sin(lat2))/(1- ecc* sin(lat2))) )
  #print "f1=", f1
  #print "f2=", f2
  #print "f2-f1=" , f2 - f1
  area = pi * r*r * (1 - ecc2) /180.0 * abs(f2 - f1)
  area = area * (dlon * 180. /pi)
  return area
#****************************************************
def del_miss(l, miss):
  #-----
  def f(x):
    if x != miss:
      return l
  #-----
  l = filter(f, l)
  return l
#****************************************************
def mk_region_mask(lat_min, lat_max, lon_min, lon_max, nx, ny, lat_first, lon_first, dlat, dlon):
  #--- xmin ----------
  if (lon_first <= lon_min):
    xmin = int( (lon_min - lon_first + dlon*0.5) /dlon)
  else:
    if ( (lon_min - lon_first + dlon*0.5)%dlon == 0.0):
      xmin = int((lon_min - lon_first + dlon *0.5)/dlon)
    else:
      xmin = int((lon_min - lon_first + dlon *0.5)/dlon) -1
  #--- xmax ----------
  if (lon_first <= lon_max):
    if ( (lon_max - lon_first + dlon*0.5)%dlon == 0.0):
      xmax = int( (lon_max - lon_first + dlon*0.5) /dlon) -1
    else:
      xmax = int( (lon_max - lon_first + dlon*0.5) /dlon)
  else:
    xmax = int((lon_max - lon_first + dlon *0.5)/dlon) -1
  #--- ymin ----------
  if (lat_first <= lat_min):
    ymin = int( (lat_min - lat_first + dlat*0.5) /dlat)
  else:
    if ( (lat_min - lat_first + dlat*0.5)%dlat == 0.0):
      ymin = int((lat_min - lat_first + dlat *0.5)/dlat)
    else:
      ymin = int((lat_min - lat_first + dlat *0.5)/dlat) -1
  #--- ymax ----------
  if (lat_first <= lat_max):
    if ( (lat_max - lat_first + dlat*0.5)%dlat == 0.0):
      ymax = int( (lat_max - lat_first + dlat*0.5) /dlat) -1
    else:
      ymax = int( (lat_max - lat_first + dlat*0.5) /dlat)
  else:
    ymax = int((lat_max - lat_first + dlat *0.5)/dlat) -1
  #-----------
  a2regionmask  = zeros(nx*ny).reshape(ny, nx)
  if ( ( xmin >= 0 ) and (xmax >= 0)):
    a2regionmask[ymin:ymax+1, xmin:xmax+1] = 1.0
  elif ( ( xmin < 0) and (xmax >= 0) ):
    a2regionmask[ymin:ymax+1, nx + xmin: nx] = 1.0
    a2regionmask[ymin:ymax+1, 0:xmax+1] = 1.0
  else:
    a2regionmask[ymin:ymax+1, nx + xmin: nx + xmax +1] = 1.0
  return a2regionmask
#####################################################
def ret_tv_difmean(l1, l2):
  n1   = len(l1)
  n2   = len(l2)
  m1   = mean(l1)
  m2   = mean(l2)
  ss1  = ret_ubvar(l1)
  ss2  = ret_ubvar(l2)
  #
  alpha = ((n1-1)*ss1 + (n2-1)*ss2 ) / (n1 + n2 -2)
  beta  = 1.0/n1 + 1.0/n2
  #
  t     = (m1 - m2) / ( sqrt(alpha) * sqrt(beta)  )
  return t
#****************************************************
def ret_ubvar(l):
  # unbiased variance
  n      = len(l)
  m      = mean(l)
  a      = array(l)
  ubvar  = sum( (a-m)*(a-m) )/ (n-1)
  return ubvar 
#****************************************************
def mul_a2(a2, n):
  (ny, nx) = shape(a2)
  #----
  l  = a2.flatten().tolist() * n
  a3 = array(l).reshape(n, ny, nx)
  return a3 




