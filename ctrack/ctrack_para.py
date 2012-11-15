import calendar
from numpy import *
#----------------------------------------------------------
#--------------
# 
#--------------
def ret_lcrad():
  #lcrad =  [500.0*1000.0, 1000.0*1000.0, 1500.0*1000.0, 2000.0*1000.0]
  #lcrad =  [1000.0*1000.0, 1500.0*1000.0]
  #lcrad =  [2000.0*1000.0]
  lcrad =  [1000.0*1000.0]
  return lcrad
#-----------------------------------
def ret_dpgradrange():
  ##dpgradrange = {0:[1.0, 10.0e+10],1:[1.0,250.0],2:[250.0,500.0],3:[500.0,750.0],4:[750.0, 1000.0], 5:[1000.0, 1250.0], 6:[1250.0, 1500.0], 7:[2500.0, 3000.0], 8:[3000.0, 10.0e+10]}
  #dpgradrange = {0:[1.0, 10.0e+10],1:[1.0,250.0],2:[250.0,500.0],3:[500.0,750.0],4:[750.0, 1000.0], 5:[1000.0, 1250.0], 6:[1250.0, 1500.0], 7:[1500, 1750], 8:[1750, 10.0e+10]}
  #dpgradrange = {0:[1.0, 10.0e+10],1:[1.0,500.0],2:[500.0, 1000.0],3:[1000.0, 1500.0],4:[1500.0, 10.0e+10]}
  #dpgradrange = {0:[100.0, 10.0e+10],1:[100.0,500.0],2:[500.0, 1000.0],3:[1000.0, 1500.0],4:[1500.0, 10.0e+10]}
  dpgradrange = {0:[30.0, 10.0e+10],1:[30.0,500.0],2:[500.0, 1000.0],3:[1000.0, 1500.0],4:[1500.0, 10.0e+10]}
  #dpgradrange = {0:[500.0, 10.0e+10], 1:[500.0, 10.0e+10]}
  #---------------------
  #dpgradrange  = {0:[1.0, 10.0e+10], 1:[1.0, 100.0]}
  #for i in arange(2, 15+1):
  #  dpgradrange[i] = [i*100.0 - 100.0, i*100.0]
  #dpgradrange[16] = [1500.0, 10.0e+10]
  ##---------------------
  return dpgradrange
#-----------------------------------
def ret_lseason():
  lseason = ["DJF"]
  return lseason
#-----------------------------------
def ret_iy_ey(expr):
  if expr == "historical":
    #[iy, ey] = [1990, 1999]
    #[iy, ey] = [1980, 1989]
    #[iy, ey] = [1980, 1999]
    [iy, ey] = [1980, 2005]
  elif expr == "rcp85":
    #[iy, ey] = [2086, 2095]
    #[iy, ey] = [2076, 2085]
    [iy, ey] = [2076, 2095]
  #-----
  return [iy, ey]
#-----------------------------------
def ret_im_em(season):
  if season == "DJF":
    im_em = [12, 2]
  return im_em
#-----------------------------------
def ret_lmon(season):
  if season == "DJF":
    lmon  = [1,2, 12]
  elif season == "ALL":
    lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
  return lmon
#-----------------------------------
def ret_mons(season):
  (im, em) = ret_im_em(season)
  if im <= em:
    mons = em - im + 1
  else:
    mons = (12 - im + 1) + em
  return mons
#-----------------------------------
def ret_lxth():
  #lxth = [0.0]
  lxth = [0.0, 90.0]
  #lxth  = [90.0, 99.0]
  #lxth = [0.0, 50.0, 60.0, 70.0, 80.0, 90.0, 99.0]
  #lxth = [50.0, 60, 70.0, 80, 90.0, 99.0]
  #lxth = [60.0, 80.0]
  return lxth
#-----------------------------------
def ret_dlwbin():
  #wmin   = -600.0  #[hPa/day]
  #wmax   = 100.0   #[hPa/day]
  wmin   = -100.0  #[hPa/day]
  wmax   = 600.0   #[hPa/day]

  dw     = 50.0    #[hPa/day]
  l  = arange( wmin, wmax+1, dw)
  n  = len(l)
  dlwbin  = {}
  dlwbin[0] = [-10.0e+10, 10.0e+10]
  i = 1
  #-----
  for w in l:
    i = i+1
    dlwbin[i] = [w, (w+dw)]
  #-----
  dlwbin[1] = [-10.0e+10, wmin]
  dlwbin[n+1] = [wmax, 10.0e+10]
  #-----
  return dlwbin
#-----------------------------------
def ret_dbound():
  dbound   = {}
  
  #reg      = "alljapan"
  #lat_min  = 22.0
  #lat_max  = 46.0
  #lon_min  = 122.0
  #lon_max  = 150.0
  #dbound[reg] = [lat_min, lat_max, lon_min, lon_max]
  #
  #
  reg      = "scjapan"
  lat_min  = 22.0
  lat_max  = 41.0
  lon_min  = 122.0
  lon_max  = 150.0
  dbound[reg] = [lat_min, lat_max, lon_min, lon_max]
  
  reg      = "njapan"
  lat_min  = 41.0
  lat_max  = 46.0
  lon_min  = 125.0
  lon_max  = 150.0
  dbound[reg] = [lat_min, lat_max, lon_min, lon_max]

  #reg      = "scjapan"
  #lat_min  = 5.0
  #lat_max  = 10.0
  #lon_min  = 75.0
  #lon_max  = 88.0
  #dbound[reg] = [lat_min, lat_max, lon_min, lon_max]

  return dbound
#-----------------------------------
def ret_lonlatinfo(model):
  if model == "NorESM1-M":
    lon_first   = 0.0
    lat_first   = -90.0
    dlon        = 2.5
    dlat        = 1.8947368
    lonlatinfo = [lon_first, lat_first, dlon, dlat]
    return lonlatinfo
