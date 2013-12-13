import calendar
from numpy import *
#----------------------------------------------------------
def ret_thdura():
  return 48
#----------------------------------------------------------
def ret_tagregionlatlon(region):
  if region=="MA":
    lllat = -15.0
    lllon = 60.0
    urlat = 55.0
    urlon = 150.0
  if region=="S.ASIA":
    lllat = 0.0
    lllon = 60.0
    urlat = 25.0
    urlon = 110.0
  if region=="E.ASIA":
    lllat = 30.0
    lllon = 115.0
    urlat = 50.0
    urlon = 150.0
  #------------
  return lllat, lllon, urlat, urlon

#----------------------------------------------------------
def ret_excregionlatlon(region):
  if region=="GLB":
    lllat = -90.0
    lllon = 0.0
    urlat = 90.0
    urlon = 360.0
  if region=="NH":
    lllat = 25.0
    lllon = 0.0
    urlat = 80.0
    urlon = 360.0
  if region=="SH":
    lllat = -80.0
    lllon = 0.0
    urlat = -25.0
    urlon = 360.0
  if region=="NPA":
    lllat = 25.0
    lllon = 100.0
    urlat = 80.0
    urlon = 230.0
  if region=="NAT":
    lllat = 25.0
    lllon = 230.0
    urlat = 80.0
    urlon = 360.0
  if region=="EUR":
    lllat = 25.0
    lllon = 0.0
    urlat = 80.0
    urlon = 100.0
  if region=="SIP":
    lllat = -80.0
    lllon = 30.0
    urlat = -25.0
    urlon = 280.0
  if region=="SAT":
    lllat = -80.0
    lllon = 290.0
    urlat = -25.0
    urlon = 360.0
  #------------
  return lllat, lllon, urlat, urlon
#----------------------------------------------------------
def ret_tcregionlatlon(region):
  if region=="GLB":
    lllat = -90.0
    lllon = 0.0
    urlat = 90.0
    urlon = 360.0
  if region=="PNW":
    lllat = 0.0
    lllon = 100.0
    urlat = 50.0
    urlon = 180.0
  if region=="PNE":
    lllat = 0.0
    lllon = 180.0
    urlon = 270.0
    urlat = 40.0
  if region=="INN":
    lllat = 0.0
    lllon = 45.0
    urlat = 30.0
    urlon = 100.0
  if region=="INS":
    lllat = -45.0
    lllon = 30.0
    urlat = 0.0
    urlon = 140.0
  if region=="PSW":
    lllat = -45.0
    lllon = 140.0
    urlat = 0.0
    urlon = 240.0
  if region=="ATN":
    lllat = 0.0
    lllon = 270.0
    urlat = 50.0
    urlon = 360.0
  #------------
  return lllat, lllon, urlat, urlon
#------------------------------------
def ret_thdp():
  return -9999.0  # (Pa) for connectc
#------------------------------------
def ret_highsidedist():
  highsidedist = 100*1000.0 #(m)
  return highsidedist
#-----------------------------------
def ret_thorog():
  thorog = 1500 # m
  return thorog
#-----------------------------------
def ret_thgradorog():
  #thgradorog = 5.0 # m/km
  thgradorog = 3.0*1.e-3 # m/m
  return thgradorog
#-----------------------------------
def ret_totaldays(iyear, eyear, season):
  lmon  = ret_lmon(season)
  days  = 0
  for year in range(iyear, eyear+1):
    for mon in lmon:
      days = days + calendar.monthrange(year,mon)[1]
  #--
  return days
#-----------------------------------
def ret_days(season):
  if season == "ALL":
    days = 365
  elif season == "MAM":
    days = 92  # 31 + 30 + 31
  elif season == "DFJ":
    days = 90  # 31 + 31 + 28
  elif season == "JJA":
    days = 92  # 30 + 31 + 31
  elif season == "SON":
    days = 91  # 30 + 31 + 30
  return days
#--------------
def ret_lcrad():
  #lcrad =  [500.0*1000.0, 1000.0*1000.0, 1500.0*1000.0, 2000.0*1000.0]
  #lcrad =  [1000.0*1000.0, 1500.0*1000.0]
  #lcrad =  [2000.0*1000.0]
  lcrad =  [1000.0*1000.0]
  return lcrad
#-----------------------------------
def ret_dpgradrange_8gridgrad():
  #------------------
  # unit: Pa/1000km, not hPa/1000km or hPa/100km
  #------------------
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
def ret_dpgradrange(model="org"):
  #------------------
  # unit: Pa/1000km, not hPa/1000km or hPa/100km
  #------------------
  #pgradmin : hPa/100km
  #------------------
  if model in ["org","anl_p","MRI-CGCM3"]:
      pgradmin = 0.342
  if model=="HadGEM2-ES":
      pgradmin = 0.343
  if model=="IPSL-CM5A-MR":
      pgradmin = 0.309
  if model=="CNRM-CM5":
      pgradmin = 0.351
  if model=="MIROC5":
      pgradmin = 0.351
  if model=="inmcm4":
      pgradmin = 0.323
  if model=="MPI-ESM-MR":
      pgradmin = 0.320
  if model=="CSIRO-Mk3-6-0":
      pgradmin = 0.320
  if model=="NorESM1-M":
      pgradmin = 0.285
  if model=="IPSL-CM5B-LR":
      pgradmin = 0.212
  if model=="GFDL-CM3":
      pgradmin = 0.261
  if model=="test.1.5deg":
      pgradmin = 0.333
  if model=="test.10deg":
      pgradmin = -0.019
  if model=="test.5deg":
      pgradmin = 0.017
  if model=="test.3deg":
      pgradmin = 0.154
 
  dpgradrange = {0:[0.0, 10.0e+10],1:[0.0,pgradmin*1000.],2:[pgradmin*1000., 500.0],3:[500.0, 1000.0],4:[1000.0, 10.0e+10]}
  #---------------------
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
  elif season == "MAM":
    lmon  = [3,4,5]
  elif season == "JJA":
    lmon  = [6,7,8]
  elif season == "SON":
    lmon  = [9,10,11]
  elif season == "ALL":
    lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
  elif type(season) == int:
    lmon  = [season]
  elif season == "NDJFMA":
    lmon  = [11,12,1,2,3,4]
  elif season == "MJJASO":
    lmon  = [5,6,7,8,9,10]
  elif season == "JJASON":
    lmon  = [6,7,8,9,10,11]
  elif season == "JJAS":
    lmon  = [6,7,8,9]
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

  reg      = "se.asia"
  lat_min  = 0.0
  lat_max  = 80.0
  lon_min  = 60.0
  lon_max  = 190.0
  dbound[reg] = [lat_min, lat_max, lon_min, lon_max]
  
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

