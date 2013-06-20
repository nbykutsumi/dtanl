import ctrack
import ctrack_para
import ctrack_func as func
from numpy import *
import calendar
import datetime
import os, sys
##***************************
##--------------------------------------------------
if (len(sys.argv) > 1):
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
  thpgmax        = int(sys.argv[15])
  thorog         = float(sys.argv[16])
else:
  model       = "NorESM1-M"
  expr        = "historical"
  ens         = "r1i1p1"
  tstp        = "6hr"
  hinc        = 6
  iyear       = 1990
  eyear       = 1990
  season      = "DJF"
  nx          = 144
  ny          = 96
  miss_dbl    = -9999.0
  miss_int    = -9999
  endh        = 18
  thdura      = 24
  thpgmax     = 20*100
  thorog      = 1500.0    #[m]


#----------
# classes
#----------
dpgradrange  = ctrack_para.ret_dpgradrange()
lclass       = dpgradrange.keys()
nclass       = len(lclass) -1
#**********************
#  names for each class
#----------------------
outdir_root     = "/media/disk2/out/CMIP5/6hr/%s/%s/%s/tracks/map"%(model, expr, ens)

ddens_area_name  = {}
dtrack_name      = {}
doutdir          = {}
for year in range(iyear, eyear+1) + [0]: 
  #---------------------------
  doutdir[year]  = outdir_root + "/%04d"%(year)
  func.mk_dir(doutdir[year])

  #---------------------------
  for iclass in lclass:
    ddens_area_name[year, iclass]  = doutdir[year]  + "/dens.area.dura%02d.nc%02d.c%02d_%s_%s_%s_%s_%s.bn"%(thdura, nclass, iclass, season, tstp, model, expr, ens)
    dtrack_name[year, iclass]      = doutdir[year]  + "/track.grid.dura%02d.nc%02d.c%02d_%s_%s_%s_%s_%s.bn"%(thdura, nclass, iclass, season, tstp, model, expr, ens)
#**********************
#  names for each upper side of the class
#----------------------
outdir     = "/media/disk2/out/CMIP5/6hr/%s/%s/%s/tracks/map"%(model, expr, ens)

ddens_area_u_name  = {}
dtrack_u_name      = {}
doutdir            = {}
for year in range(iyear, eyear+1) + [0]:
  #---------------------------
  doutdir[year]    = outdir_root + "/%04d"%(year)
  func.mk_dir(doutdir[year])

  #---------------------------
  for iclass in lclass[1:]:
    ddens_area_u_name[year, iclass]  = doutdir[year]  + "/u.dens.area.dura%02d.nc%02d.c%02d_%s_%s_%s_%s_%s.bn"%(thdura, nclass, iclass, season, tstp, model, expr, ens)
    dtrack_u_name[year, iclass]      = doutdir[year]  + "/u.track.grid.dura%02d.nc%02d.c%02d_%s_%s_%s_%s_%s.bn"%(thdura, nclass, iclass, season, tstp, model, expr, ens)
  func.mk_dir(outdir)
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
def check_file(sname):
  if not os.access(sname, os.F_OK):
    print "no file:",sname
    sys.exit()
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
pgraddir_root   = "/media/disk2/out/CMIP5/%s"%(tstp)
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
#*****************************************************
#  read orography
#----------------------
orogdir_root = "/media/disk2/data/CMIP5/bn/orog/fx/%s/%s/r0i0p0"%(model, expr)
orogname     = orogdir_root + "/orog_fx_%s_%s_r0i0p0.bn"%(model, expr)
a2orog         = fromfile(orogname, float32).reshape(ny,nx)
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
# for all year
#---------
da2dens = {}
for iclass in lclass:
  da2dens[iclass] = array(zeros(ny*nx).reshape(ny, nx), float32)
#--------------
for year in range(iyear, eyear+1):
#for year in range(1990, 1990+1):
  #-----------------------------------
  # dummy for annual data
  #---------
  da2dens_y  = {}
  for iclass in lclass:
    da2dens_y[iclass]  = array(zeros(ny*nx).reshape(ny, nx), float32)
  #-----------------------------------
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
        pgraddir   = pgraddir_root    + "/%s/%s/%s/pgrad/%04d"%(model,expr,ens, year)
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
        pgradname = pgraddir         + "/pgrad_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
        #
        iposname    = iposdir        + "/ipos_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
        idatename   = idatedir       + "/idate_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
        lifename    = lifedir        + "/life_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
        #***************************************
        #   read
        #*******************
        a2psl        = fromfile(pslname,   float32).reshape(ny, nx)
        a2pgrad      = fromfile(pgradname, float32).reshape(ny, nx)
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
        a2center   = array(ones(ny*nx).reshape(ny, nx), float32)
        a2center   = ma.masked_where(a2dura < thdura, a2center)
        #-------------------
        # filter with maximum gprad in it's lifetime
        #*******************
        a2center   = ma.masked_where(a2pgmax < thpgmax, a2center)
        #-------------------
        # filter with cyclone class   # 
        #*******************
        for iclass in lclass:
          pgradrange        =  dpgradrange[iclass]
          pglw              =  pgradrange[0]
          pgup              =  pgradrange[1]
          a2center_tmp      =  ma.masked_where( a2pgrad > pgup, a2center)
          a2center_tmp      =  ma.masked_where( a2pgrad < pglw, a2center_tmp)
          #*******************
          a2center_tmp      =  a2center_tmp.filled(0)
          #********************************
          da2dens_y[iclass] =  da2dens_y[iclass] + a2center_tmp
          da2dens[iclass]   =  da2dens[iclass]   + a2center_tmp
  #***********************************************
  # write annual data
  #-----------------------------------------------
  # for each class
  #----------------------
  da2dens_area_y        = {}
  for iclass in lclass:
    da2dens_y[iclass]      = ma.masked_where( a2orog >= thorog, da2dens_y[iclass]).filled(NaN)
    da2dens_area_y[iclass] = array(da2dens_y[iclass] *10000.0 / a2area ,float32)  #[times/100x100m2/season] 
    #
    da2dens_area_y[iclass].tofile( ddens_area_name[year, iclass])
  #----------------------
  # for upper side
  #----------------------
  da2dens_area_uy       = {}
  for iclass in lclass[1:]:
    #----------
    # dummy
    #----------
    da2dens_area_uy[iclass] = zeros(ny*nx).reshape(ny, nx)
    #----------
    # sum up
    #----------
    for iiclass in lclass[iclass:]:
      da2dens_area_uy[iclass] = da2dens_area_uy[iclass] + da2dens_area_y[iiclass] 
    #----------
    # fill and write
    #----------
    da2dens_area_uy[iclass]   = ma.masked_where( a2orog >= thorog, da2dens_area_uy[iclass]).filled(NaN)
    da2dens_area_uy[iclass]   = array( da2dens_area_uy[iclass] , float32)
    da2dens_area_uy[iclass].tofile( ddens_area_u_name[year, iclass] )
  #***********************************************
#*****************
# dummy
#-----------------
da2dens_area = {}
da2track     = {}
#*****************
# dens_area
#-----------------
for iclass in lclass:
  da2dens_area[iclass] = array(da2dens[iclass] * 10000.0 / a2area / (eyear-iyear+1), float32)  # [times/100x100km2/season]

#*****************
# track
#-----------------
for iclass in lclass:
  da2track[iclass]     = array(ma.masked_greater(da2dens[iclass], 0.0).filled(1.0), float32)
#-----------
# mask high altitude area
#-----------
for iclass in lclass:
  da2dens_area[iclass]  = ma.masked_where( a2orog >= thorog, da2dens_area[iclass]).filled(NaN)
  da2track[iclass]      = ma.masked_where( a2orog >= thorog, da2track[iclass]).filled(NaN)

#-----------
# write to file
#-----------
for iclass in lclass:
  da2dens_area[iclass].tofile(ddens_area_name[0, iclass])
  da2track[iclass].tofile(dtrack_name[0, iclass])

#-----------
print ddens_area_name[0, 0]
print dtrack_name[0, 0]
#********************************************************
# upper side of the class
#--------------------------------------------------------
# dummy
#-----------------
da2dens_area_u = {}
da2track_u     = {}
for iclass in lclass[1:]:
  da2dens_area_u[iclass] = zeros(ny*nx).reshape(ny, nx)
  da2track_u[iclass]     = zeros(ny*nx).reshape(ny, nx)
#-----------------
# dens_area
#-----------------
for iclass in lclass[1:]:
  for iiclass in lclass[iclass:]:
    da2dens_area_u[iclass] = da2dens_area_u[iclass] + da2dens_area[iiclass]
#-----------------
# track
#-----------------
for iclass in lclass[1:]:
  da2track_u[iclass]       = array(ma.masked_greater(da2dens_area_u[iclass], 0.0).filled(1.0), float32)
#-----------
# mask high altitude area
#-----------
for iclass in lclass[1:]:
  da2dens_area_u[iclass]  = ma.masked_where( a2orog >= thorog, da2dens_area_u[iclass]).filled(NaN)
  da2track_u[iclass]      = ma.masked_where( a2orog >= thorog, da2track_u[iclass]).filled(NaN)
#----------
# convert to float32
#----------
for iclass in lclass[1:]:
  da2dens_area_u[iclass]  = array( da2dens_area_u[iclass] ,float32)
  da2track_u[iclass]      = array( da2track_u[iclass]     ,float32)
#----------
# write to file
#-----------
for iclass in lclass[1:]:
  da2dens_area_u[iclass].tofile(ddens_area_u_name[0, iclass])
  da2track_u[iclass].tofile(dtrack_u_name[0, iclass])
#-----------
print ddens_area_name[0, 0]
print dtrack_name[0, 0]








