from numpy import *
import calendar
#################################################
def ret_ibtracs_dlonlat(year_org):
  idir ="/media/disk2/data/ibtracs/v03r04"
  csvname = idir + "/Year.%04d.ibtracs_all.v03r04.csv"%(year_org) 
  lhour  = [0,6,12,18]
  #-- open ----
  f = open(csvname, "r")
  lines = f.readlines()
  f.close()
  #--- init dict ---
  dout   = {}
  for mon in range(1,12+1):
    eday = calendar.monthrange(year_org,mon)[1]
    for day in range(1,eday+1):
      for hour in lhour:
        print year_org,mon,day,hour
        dout[year_org,mon,day,hour] = []
  #-----------------
  for line in lines[3:]:
    line     = line.split(",")
    isotime  = line[6].split(" ")
    date     = map(int, isotime[0].split("-"))
    year     = date[0]
    mon      = date[1]
    day      = date[2]
    hour     = int(isotime[1].split(":")[0])
    #--- check year --
    if year != year_org:
      continue
    #--- check hour --
    if hour not in lhour:
      continue
    #--- check nature --
    nature   = line[7].strip()
    if nature not in ["TS"]:
      continue
    #-----------------
    tcname   = line[5].strip()
    tcid     = line[0]
    lat      = float(line[16])
    lon      = float(line[17])
    if (lon < 0.0):
      lon = 360.0 + lon
    #-----------------
    dout[year,mon,day,hour].append((lon,lat))
  #---
  return dout

#################################################
def ret_ibtracs_dpyxy_saone(year_org):
  idir ="/media/disk2/data/ibtracs/v03r04"
  csvname = idir + "/Year.%04d.ibtracs_all.v03r04.csv"%(year_org) 
  lat_first  = -89.5
  lon_first  = 0.5
  dlon       = 1.0
  dlat       = 1.0
  lhour  = [0,6,12,18]
  #-- open ----
  f = open(csvname, "r")
  lines = f.readlines()
  f.close()
  #--- init dict ---
  dout   = {}
  for mon in range(1,12+1):
    eday = calendar.monthrange(year_org,mon)[1]
    for day in range(1,eday+1):
      for hour in lhour:
        print year_org,mon,day,hour
        dout[year_org,mon,day,hour] = []
  #-----------------
  for line in lines[3:]:
    line     = line.split(",")
    isotime  = line[6].split(" ")
    date     = map(int, isotime[0].split("-"))
    year     = date[0]
    mon      = date[1]
    day      = date[2]
    hour     = int(isotime[1].split(":")[0])
    #--- check year --
    if year != year_org:
      continue
    #--- check hour --
    if hour not in lhour:
      continue
    #--- check nature --
    nature   = line[7].strip()
    if nature not in ["TS"]:
      continue
    #-----------------
    tcname   = line[5].strip()
    tcid     = line[0]
    lat      = float(line[16])
    lon      = float(line[17])
    if (lon < 0.0):
      lon = 360.0 + lon
    #-----------------
    x        = int( (lon - lon_first + dlon*0.5)/dlon)
    y        = int( (lat - lat_first + dlat*0.5)/dlat)
    #-----------------
    dout[year,mon,day,hour].append((x,y))
  #---
  return dout
################################################# 
def lpyxy2map_saone(lpyxy, vfill, miss):
  a2out = ones([180,360],float32)*miss
  #------
  for xy in lpyxy:
    ix, iy = xy
    a2out[iy,ix] = vfill
  #------
  return a2out
################################################# 




