import ctrack
from numpy import *
import calendar
import datetime
import os, sys
##***************************
#--------------------------------------------------
model          = sys.argv[1]
expr           = sys.argv[2]
ens            = sys.argv[3]
tstp           = sys.argv[4]
hinc           = int(sys.argv[5])
iyear          = int(sys.argv[6])
eyear          = int(sys.argv[7])
season         = sys.argv[8]
nx             = int(sys.argv[9])
ny             = int(sys.argv[10])
miss_dbl       = float(sys.argv[11])
miss_int       = int(sys.argv[12])
endh           = int(sys.argv[13])
thdura         = float(sys.argv[14])
thpgmax         = int(sys.argv[15])
dens_area_name = sys.argv[16]
track_name     = sys.argv[17]

#
#model       = "NorESM1-M"
#expr        = "historical"
#ens         = "r1i1p1"
#tstp        = "6hr"
#hinc        = 6
#iyear       = 1990
#eyear       = 1995
#season      = "DJF"
#nx          = 144
#ny          = 96
#miss_dbl    = -9999.0
#miss_int    = -9999
#endh        = 18
#thdura      = 24
#thpgmax     = 20*100
#----------
#  names
#----------
outdir     = "/media/disk2/out/CMIP5/6hr/NorESM1-M/historical/r1i1p1/tracks/map"
outdir     = "/media/disk2/out/CMIP5/6hr/%s/%s/%s/tracks/map"%(model, expr, ens)
dens_area_name  = outdir + "/dens.area_%s_%s_%s_%s_%s.bn"%(season, tstp, model, expr, ens)
track_name       = outdir + "/track.grid_%s_%s_%s_%s_%s.bn"%(season, tstp, model, expr, ens)


#**********************
# make lmon
#**********************
dlmon = {}
dlmon["DJF"] = [12, 1, 2]
dlmon["JJA"] = [6, 7, 8]
dlmon["ALL"] = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
lmon = dlmon[season]
#####################################################
# functions
#####################################################
def delmiss_int(a):
  return a != -9999
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
#def solvelife(number):
#  #pmin = int(number / 10000)
#  #dura = number - pmin *10000
#  dura = int(number / 1000000)
#  pgmax = number - dura*1000000
#  return (pgmax, dura)
#****************************************************
# dir_root
#---------------
psldir_root     = "/media/disk2/data/CMIP5/bn/psl/%s"%(tstp)
pmeandir_root   = "/media/disk2/out/CMIP5/%s"%(tstp)
winddir_root    = "/media/disk2/out/CMIP5/day"
axisdir_root    = psldir_root
#
lastposdir_root = "/media/disk2/out/CMIP5/%s"%(tstp)
#pmindir_root    = "/media/disk2/out/CMIP5/%s"%(tstp)
pgmaxdir_root   = "/media/disk2/out/CMIP5/%s"%(tstp)
iposdir_root    = "/media/disk2/out/CMIP5/%s"%(tstp)
idatedir_root   = "/media/disk2/out/CMIP5/%s"%(tstp)
timedir_root    = "/media/disk2/out/CMIP5/%s"%(tstp)
lifedir_root    = "/media/disk2/out/CMIP5/%s"%(tstp)
nextposdir_root = "/media/disk2/out/CMIP5/%s"%(tstp)
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
# dummy
#**************
a2dens = array(zeros(ny*nx).reshape(ny, nx), int32)
#--------------
for year in range(iyear, eyear+1):
#for year in range(1990, 1990+1):
  #---------
  # dirs
  #---------
  for mon in lmon:
    print "cdens.py",year, mon
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
        #---------
        stimeh  = "%04d%02d%02d%02d"%(year,mon,day,hour)
        #------
        #***************************************
        #    DIRS
        #***********
        psldir     = psldir_root      + "/%s/%s/%s/%04d"%(model,expr,ens, year)
        pmeandir   = pmeandir_root    + "/%s/%s/%s/pmean/%04d"%(model, expr, ens, year)
        #
        iposdir    = iposdir_root     + "/%s/%s/%s/ipos/%04d"%(model, expr, ens, year)
        idatedir   = idatedir_root    + "/%s/%s/%s/idate/%04d"%(model, expr, ens, year)
        lifedir    = lifedir_root     + "/%s/%s/%s/life/%04d"%(model, expr, ens, year)
        #----------
        #   names
        #**********
        pslname   = psldir           + "/psl_%sPlev_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
        pmeanname = pmeandir         + "/pmean_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
        #
        iposname    = iposdir        + "/ipos_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
        idatename   = idatedir       + "/idate_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
        lifename    = lifedir        + "/life_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
        #***************************************
        #   read
        #*******************
        a2psl        = fromfile(pslname,   float32).reshape(ny, nx)
        a2pmean      = fromfile(pmeanname, float32).reshape(ny, nx)
        a2iposname   = fromfile(iposname,  int32).reshape(ny, nx)
        a2idate      = fromfile(idatename, int32).reshape(ny, nx)
        a2life       = fromfile(lifename,  int32).reshape(ny, nx)
        #---------------------------------------
        # make pmin, dura
        #*******************
        tsolvelife = ctrack.ctrack.solvelife(a2life.T, miss_int)
        #a2pmin     = tsolvelife[0].T
        a2dura     = tsolvelife[0].T
        a2pgmax    = tsolvelife[1].T
        #---------------------------------------
        # filter
        #*******************
        a2center   = array(ones(ny*nx).reshape(ny, nx), int32)
        a2center   = ma.masked_where(a2dura < thdura, a2center)
        a2center   = ma.masked_where(a2pgmax < thpgmax, a2center)
        a2center   = a2center.filled(0)
        #-------------------
        a2dens     = a2dens + a2center
#----------
a2dens_area = array(a2dens / a2area * 1000.0 / (eyear-iyear+1), float32)  # [times/1000km/season]
a2track     = array(ma.masked_greater(a2dens, 0.0).filled(1.0), float32)
#-----------
# write to file
#-----------
a2dens_area.tofile(dens_area_name)
a2track.tofile(track_name)
#-----------
print dens_area_name
print track_name
#-----------








