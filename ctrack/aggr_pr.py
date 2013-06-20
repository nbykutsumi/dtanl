from ctrack import *
from numpy import *
import calendar
import datetime
import os, sys


#####################################################
# functions
#####################################################
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
    print "AAAAA"
    a2regionmask[ymin:ymax+1, nx + xmin: nx] = 1.0
    a2regionmask[ymin:ymax+1, 0:xmax+1] = 1.0
  else:  
    a2regionmask[ymin:ymax+1, nx + xmin: nx + xmax +1] = 1.0

  print "xmin, xmax",xmin, xmax
  return a2regionmask
#####################################################
def delmiss_int(a):
  return a != -9999
#####################################################
def xy2fortpos(ix, iy, nx):
  number = iy* nx + ix +1
  return number
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
#def solvelife(number):
#  #pmin = int(number / 10000)
#  #dura = number - pmin *10000
#  dura = int(number / 1000000)
#  pgmax = number - dura*1000000
#  return (pgmax, dura)
#**************************************************
# make area [km2] map
#----------------------
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
def main(\
  model       = "NorESM1-M"\
  ,expr        = "historical"\
  ,ens         = "r1i1p1"\
  ,tstp        = "6hr"\
  ,hinc        = 6\
  ,iyear       = 1990\
  ,eyear       = 1990\
  ,season      = "DJF"\
  ,nx          = 144\
  ,ny          = 96\
  ,miss_dbl    = -9999.0\
  ,miss_int    = -9999\
  ,crad        = 2000.0*1000.0\
  ,thdura      = 24\
  ,thorog      = 1500.0\
  ,dpgradrange = {0:[0.0, 10.0e+10],1:[0.0,250.0],2:[250.0,500.0],3:[500.0,750.0],4:[750.0, 1000.0], 5:[1000.0, 1250.0], 6:[1250.0, 1500.0], 7:[2500.0, 10.0e+10]}
  ,daggname    = {}\
  ,dpgrad_mean_name ={}\
  ,dcountname  = {}
  ):

  ##***************************
  #model          = sys.argv[1]
  #expr           = sys.argv[2]
  #ens            = sys.argv[3]
  #tstp           = sys.argv[4]
  #hinc           = int(sys.argv[5])
  #iyear          = int(sys.argv[6])
  #eyear          = int(sys.argv[7])
  #season         = sys.argv[8]
  #nx             = int(sys.argv[9])
  #ny             = int(sys.argv[10])
  #miss_dbl       = float(sys.argv[11])
  #miss_int       = int(sys.argv[12])
  #crad           = float(sys.argv[13])
  #thdura         = float(sys.argv[14])
  #thorog         = float(sys.argv[15]) 
  
  
 
  #dpgradrange = {1:[0.0,1000.0],2:[1000.0,2000.0],3:[2000.0,3000.0],4:[3000.0, 4000.0], 5:[4000.0, 9999999.0]}
  
  lclass      = dpgradrange.keys()
  #**********************
  dendh = {"6hr":18}
  endh  = dendh[tstp]
  #**********************
  #  names for OUTPUT
  #----------------------
  outdir     = "/media/disk2/out/CMIP5/6hr/%s/%s/%s/tracks/aggr.pr"%(model, expr, ens)
  #-----------
  # precip aggr
  #-----------
  if (daggname =={}):
    daggname  = {}
    for i in range(len(lclass)):
      iclass = lclass[i]
      daggname[iclass] = outdir + "/aggr.pr.c%02d.r%04d_%s_%s_%s_%s_%s.bn"%(iclass, crad*0.001, season, tstp, model, expr, ens)
  #-----------
  # count  # counts the center of cyclone
  #-----------
  if dcountname == {}:
    dcountname = {}
    for i in range(len(lclass)):
      iclass = lclass[i]
      dcountname[iclass] = outdir + "/count.cyclone.c%02d.r%04d_%s_%s_%s_%s_%s.bn"%(iclass, crad*0.001, season, tstp, model, expr, ens)
  #-----------
  # pgrad_mean
  #-----------
  if dpgrad_mean_name == {}:
    dpgrad_mean_name = {}
    for i in range(len(lclass)):
      iclass = lclass[i]
      dpgrad_mean_name[iclass] = outdir + "/pgrad_mean.c%02d.r%04d_%s_%s_%s_%s_%s.bn"%(iclass, crad*0.001, season, tstp, model, expr, ens)
  #**********************
  #  read orography
  #----------------------
  orogdir_root = "/media/disk2/data/CMIP5/bn/orog/fx/%s/%s/r0i0p0"%(model, expr)
  orogname     = orogdir_root + "/orog_fx_%s_%s_r0i0p0.bn"%(model, expr)
  a2orog         = fromfile(orogname, float32).reshape(ny,nx)
  
  #**********************
  # make lmon
  #**********************
  dlmon = {}
  dlmon["DJF"] = [12, 1, 2]
  dlmon["JJA"] = [6, 7, 8]
  dlmon["ALL"] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
  lmon = dlmon[season]
  #****************************************************
  # dir_root
  #---------------
  #psldir_root     = "/media/disk2/data/CMIP5/bn/psl/%s"%(tstp)
  #pmeandir_root   = "/media/disk2/out/CMIP5/%s"%(tstp)
  #winddir_root    = "/media/disk2/out/CMIP5/day"
  axisdir_root    = "/media/disk2/data/CMIP5/bn/psl/%s"%(tstp)
  #
  #lastposdir_root = "/media/disk2/out/CMIP5/%s"%(tstp)
  #pmindir_root    = "/media/disk2/out/CMIP5/%s"%(tstp)
  #pgmaxdir_root   = "/media/disk2/out/CMIP5/%s"%(tstp)
  #iposdir_root    = "/media/disk2/out/CMIP5/%s"%(tstp)
  #idatedir_root   = "/media/disk2/out/CMIP5/%s"%(tstp)
  #timedir_root    = "/media/disk2/out/CMIP5/%s"%(tstp)
  lifedir_root    = "/media/disk2/out/CMIP5/%s"%(tstp)
  pgraddir_root   = "/media/disk2/out/CMIP5/%s"%(tstp)
  prdir_root      = "/media/disk2/data/CMIP5/bn/pr/%s"%(tstp)
  #nextposdir_root = "/media/disk2/out/CMIP5/%s"%(tstp)
  #**************************************************
  # read lat, lon data
  #----------------------
  axisdir    = axisdir_root  + "/%s/%s/%s"%(model, expr, ens)
  latname    = axisdir  + "/lat.txt"
  lonname    = axisdir  + "/lon.txt"
  a1lat      = read_txtlist(latname)
  a1lon      = read_txtlist(lonname) 
  dlat       = a1lat[1] - a1lat[0]
  dlon       = a1lon[1] - a1lon[0]
  
  lat_first  = a1lat[0]
  #-------         
  a2area = array(zeros(ny*nx), float32).reshape(96,144)
  #---
  for iy in [0, ny-1]:
    lat           = a1lat[iy]
    lat1          = abs(lat) - dlat*0.5
    lat2          = lat
    area          = cal_area(lat1, lat2, dlon) * 2.0
    a2area[iy,:] = area
  #---
  for iy in range(1,ny-1):
    lat           = a1lat[iy]
    lat1          = a1lat[iy] - dlat*0.5
    lat2          = a1lat[iy] + dlat*0.5
    area          = cal_area(lat1, lat2, dlon)
    a2area[iy,:] = area
  #**************************************************
  counter = 0
  #**************************************************
  #**************
  # dummy for da2agg
  #--------------
  da2agg = {}
  for iclass in lclass:
    da2agg[iclass] = zeros( nx*ny).reshape(ny,nx)
  #**************
  # dummy for da2count
  #--------------
  da2count = {}
  for iclass in lclass:
    da2count[iclass] = zeros( nx*ny).reshape(ny, nx)
  #**************
  # dummy for da2pgrad_mean
  #--------------
  da2pgrad_mean = {}
  for iclass in lclass:
    da2pgrad_mean[iclass] = zeros( nx*ny).reshape(ny, nx)
  #**************
  # make a2ones 
  #--------------
  a2ones = ones(nx*ny).reshape(ny, nx)
  #--------------
  for year in range(iyear, eyear+1):
    #---------
    # dirs
    #---------
    for mon in lmon:
      print year, mon
      ##############
      # no leap
      ##############
      if (mon==2)&(calendar.isleap(year)):
        ed = calendar.monthrange(year,mon)[1] -1
      else:
        ed = calendar.monthrange(year,mon)[1]
      ##############
      for day in range(1, ed+1):
      #for day in range(1, 1+1):
        for hour in range(0, endh+1, hinc):
          counter = counter + 1
          ##---------
          stimeh  = "%04d%02d%02d%02d"%(year,mon,day,hour)
          ##------
          ##***************************************
          ##    DIRS
          ##***********
          #psldir     = psldir_root      + "/%s/%s/%s/%04d"%(model,expr,ens, year)
          #pmeandir   = pmeandir_root    + "/%s/%s/%s/pmean/%04d"%(model, expr, ens, year)
          ##
          #iposdir    = iposdir_root     + "/%s/%s/%s/ipos/%04d"%(model, expr, ens, year)
          #idatedir   = idatedir_root    + "/%s/%s/%s/idate/%04d"%(model, expr, ens, year)
          lifedir    = lifedir_root     + "/%s/%s/%s/life/%04d"%(model, expr, ens, year)
          pgraddir   = pgraddir_root    + "/%s/%s/%s/pgrad/%04d"%(model, expr, ens, year)
          prdir      = prdir_root       + "/%s/%s/%s/%04d"%(model, expr, ens, year)
  
          ##----------
          ##   names
          ##**********
          #pslname   = psldir           + "/psl_%sPlev_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
          #pmeanname = pmeandir         + "/pmean_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
          ##
          #iposname    = iposdir        + "/ipos_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
          #idatename   = idatedir       + "/idate_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
          lifename     = lifedir        + "/life_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
          pgradname    = pgraddir        + "/pgrad_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
          prname       = prdir        + "/pr_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
          ##***************************************
          ##   read
          ##---------------------------------------
          a2life   = fromfile(lifename, int32).reshape(ny, nx)
          a2pgrad  = fromfile(pgradname, float32).reshape(ny, nx)
          a2pr     = fromfile(prname, float32).reshape(ny, nx)
          #****************************************
          # make a2territory
          #----------------------------------------
          tout  = ctrack.aggr_pr(a2life.T, a2pgrad.T, crad, thdura\
                                 , miss_int, miss_dbl, lat_first\
                                 , dlat, dlon)
          #--
          a2territory = tout[0].T
          #****************************************
          # aggregate precipitation
          #----------------------------------------
          # mask high elevation area
          #-------------
          a2territory = ma.masked_where( a2orog >= thorog, a2territory)
          a2pgrad     = ma.masked_where( a2orog >= thorog, a2pgrad)
          a2ones      = ma.masked_where( a2orog >= thorog, a2ones)
          #-------------
          # mask miss data ( for a2pgrad)
          #-------------
          a2pgrad     = ma.masked_equal(a2pgrad, miss_dbl)
          #-------------
          for iclass in lclass:
            pgradrange = dpgradrange[iclass]
            pgrad_min  = pgradrange[0]
            pgrad_max  = pgradrange[1]
            #-----------
            # mask outside of the class
            #-----------
            a2mask      = ma.masked_outside(a2territory, pgrad_min, pgrad_max)
            #-----
            # agg
            #-----
            a2agg_tmp   = ma.masked_where( a2mask.mask, a2pr ).filled(0.0)
            da2agg[iclass] = da2agg[iclass] + a2agg_tmp
            #-----
            # pgrad_mean
            #-----
            a2pgrad_tmp = ma.masked_where( a2mask.mask, a2pgrad).filled(0.0)
            da2pgrad_mean[iclass] = da2pgrad_mean[iclass] + a2pgrad_tmp
            #-----
            # count
            #-----
            da2count[iclass] = da2count[iclass] + ma.masked_where( a2mask.mask, a2ones).filled(0.0)
            #-----
            # reset
  #-----------------
  # average of agg
  #-----------------
  for iclass in lclass:
    da2agg[iclass] = da2agg[iclass] / ma.masked_equal(da2count[iclass], 0.0)
    da2agg[iclass] = da2agg[iclass].filled(miss_dbl)
    da2agg[iclass] = array(da2agg[iclass], float32)
  #-----------------
  # average of pgrad_mean
  #-----------------
  for iclass in lclass:
    da2pgrad_mean[iclass] = da2pgrad_mean[iclass] / ma.masked_equal(da2count[iclass], 0.0)
    da2pgrad_mean[iclass] = da2pgrad_mean[iclass].filled(miss_dbl)
    da2pgrad_mean[iclass] = array(da2pgrad_mean[iclass], float32)
  #-----------------
  # fill da2count with miss
  #-----------------
  for iclass in lclass:
    da2count[iclass] = ma.masked_equal(da2count[iclass], 0.0).filled(miss_dbl)
    da2count[iclass] = array(da2count[iclass], float32)
  #-----------------
  # convert to float32
  #-----------------
  #****************************
  # write map to files
  #----------------------------
  mk_dir(outdir)
  for iclass in lclass:
    da2agg[iclass].tofile(daggname[iclass])
    da2pgrad_mean[iclass].tofile(dpgrad_mean_name[iclass])
    da2count[iclass].tofile(dcountname[iclass])
    print daggname[iclass]
  
#$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
if __name__ == '__main__': main()
