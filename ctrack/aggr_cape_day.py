from mpl_toolkits.basemap import Basemap
import matplotlib
import matplotlib.pyplot as plt
from ctrack import *
import ctrack_para
from numpy import *
import calendar
import datetime
import os, sys
from cf.plot import *

#####################################################
# functions
#####################################################
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
#**************************************************
if (len(sys.argv) >1):
  model    = sys.argv[1]
  expr     = sys.argv[2]
  ens      = sys.argv[3]
  tstp     = sys.argv[4]
  hinc     = int(sys.argv[5])
  iyear    = int(sys.argv[6])
  eyear    = int(sys.argv[7])
  season   = sys.argv[8]
  nx       = int(sys.argv[9])
  ny       = int(sys.argv[10])
  nz       = int(sys.argv[11])
  miss_dbl = float(sys.argv[12])
  miss_int = int(sys.argv[13])
  crad     = float(sys.argv[14])
  thdura   = int(sys.argv[15])
  thorog   = float(sys.argv[16])
  xth      = float(sys.argv[17])
  #---
else:
  model       = "NorESM1-M"
  #expr        = "historical"
  expr        = "rcp85"
  ens         = "r1i1p1"
  tstp        = "6hr"
  hinc        = 6
  #iyear       = 1990
  #eyear       = 1999
  iyear       = 2086
  eyear       = 2095
  season      = "DJF"
  nx          = 144
  ny          = 96
  nz          = 8
  miss_dbl    = -9999.0
  miss_int    = -9999
  crad        = 1000.0*1000.0
  thdura      = 24
  thorog      = 1500.0
  xth         = 00.0
dnumname = {}
dspname = {}
dsp2name = {}
dswname = {}
dsw2name = {}
dmpgradname = {}
 

lvar        = ["pap", "capep"]
mnum_min    = 1.0
#----------------------
lats        = linspace(-90.0, 90.0, ny)
lons        = linspace(0.0, 360.0 - 360.0/nx, nx)
lllat       = -90.0
lllon       = 0.0
urlat       = 90.0
urlon       = 360.0
#
dlon        = lons[1] - lons[0]
dlat        = lats[1] - lats[0]
nnx         = int( (urlon - lllon)/dlon )
nny         = int( (urlat - lllat)/dlat )
#----------------------
[iy, ey]    = ctrack_para.ret_iy_ey(expr)
[im, em]    = ctrack_para.ret_im_em(season)
dpgradrange = ctrack_para.ret_dpgradrange()
cmin        = dpgradrange[0][0]

#**********************
# omega bin
#----------------------
dlwbin  = ctrack_para.ret_dlwbin()
nwbin    = len(dlwbin.keys())
for i in dlwbin.keys():
  abin = array(dlwbin[i])*100.0/60.0/60.0/24.0
  dlwbin[i] = abin
#----------------------
lclass      = dpgradrange.keys()
nclass      = len(lclass) -1
#**********************
dendh = {"6hr":18}
endh  = dendh[tstp]
#***************************************
#  names for OUTPUT
#---------------------------------------
outdir_root     = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d"%(model, expr, ens, thdura, im, em, nclass, cmin)
#
mk_dir(outdir_root)

dodir    = {}
doname   = {}
daccname = {}
#-----------
for var in lvar:
  dodir[var]  = outdir_root + "/%s"%(var)
  mk_dir(dodir[var])
  for iclass in [-1] +lclass:
    doname[var, iclass ] = dodir[var] + "/%s.p%05.2f.cmin%04d.c%02d.%02d.r%04d.%s_%s_%s_%s_%s.bn"%(var, xth, cmin, iclass, nclass, crad*0.001, season, "day", model, expr, ens)
    daccname[var, iclass ] = dodir[var] + "/acc.%s.p%05.2f.cmin%04d.c%02d.%02d.r%04d.%s_%s_%s_%s_%s.bn"%(var, xth, cmin, iclass, nclass, crad*0.001, season, "day", model, expr, ens)
#**********************
#  read orography
#----------------------
orogdir_root = "/media/disk2/data/CMIP5/bn/orog/fx/%s/%s/r0i0p0"%(model, expr)
orogname     = orogdir_root + "/orog_fx_%s_%s_r0i0p0.bn"%(model, expr)
a2orog         = fromfile(orogname, float32).reshape(ny,nx)
#**********************
# read pxth data
#----------------------
if xth != 0.0:
  prxthdir = "/media/disk2/out/CMIP5/day/%s/%s/%s/prxth/%04d-%04d/%02d-%02d"%(model, expr, ens, iy, ey, im, em)
  prxthname = prxthdir + "/prxth_day_%s_%s_%s_%06.2f.bn"%(model, expr, ens, xth)
  a2prxth     = fromfile(prxthname, float32).reshape(ny, nx)
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
axisdir_root    = "/media/disk2/data/CMIP5/bn/psl/%s"%(tstp)
#
lifedir_root    = "/media/disk2/out/CMIP5/%s"%(tstp)
pgraddir_root   = "/media/disk2/out/CMIP5/%s"%(tstp)
prdir_root      = "/media/disk2/data/CMIP5/bn/pr/%s"%("day")
didir_root        =  {}
for var in lvar:
  didir_root[var] = "/media/disk2/data/CMIP5/bn/%s/%s"%(var,"day")
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
# dummy , out
#--------------
da2out = {}
for var in ["pap", "capep"]:
  for iclass in [-1]+lclass:
    da2out[var, iclass] = zeros( nx*ny, float32).reshape(ny,nx)
#--------------
# dummy , acc out
#--------------
da2acc = {}
for var in ["pap", "capep"]:
  for iclass in [-1]+lclass:
    da2acc[var, iclass] = zeros( nx*ny, float32).reshape(ny,nx)
#--------------
# dummy , num
#--------------
da2num = {}
for iclass in [-1]+lclass:
  da2num[iclass] = zeros( nx*ny, float32).reshape(ny,nx)
#--------------
# dummy , acc num
#--------------
da2accnum = {}
for iclass in [-1]+lclass:
  da2accnum[iclass] = zeros( nx*ny, float32).reshape(ny,nx)

#**************
# make a2ones 
#--------------
a2ones = ones(nx*ny, float32).reshape(ny, nx)
#--------------
for year in range(iyear, eyear+1):
  #---------
  # dirs
  #---------
  dsp_test   = {}
  dspc_test  = {}
  dporg_test  = {}
  dporgc_test = {}
  dmask_test   = {}
  dmaskc_test  = {}
  drat_test    = {}
  dsum_test    = {}
  dsumc_test   = {}
  dmask1  = {}
  dmask2  = {}
  dmaskc1 = {}
  dmaskc2 = {}

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

      #----------------------------------
      # make dummy for daily data
      #----------------------------------
      a2territory_day = zeros(nx*ny, float32).reshape(ny, nx)
      a2pgrad_day     = zeros(nx*ny, float32).reshape(ny, nx)
      #----------------------------------
      for hour in range(0, endh+1, hinc):
        counter = counter + 1
        ##---------
        stimeh  = "%04d%02d%02d%02d"%(year,mon,day,hour)
        ##------
        ##***************************************
        ##    DIRS
        ##***********
        lifedir    = lifedir_root     + "/%s/%s/%s/life/%04d"%(model, expr, ens, year)
        pgraddir   = pgraddir_root    + "/%s/%s/%s/pgrad/%04d"%(model, expr, ens, year)

        ##----------
        ##   names
        ##**********
        lifename     = lifedir        + "/life_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
        pgradname    = pgraddir        + "/pgrad_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
        ##***************************************
        ##   read
        ##---------------------------------------
        a2life      = fromfile(lifename, int32).reshape(ny, nx)
        a2pgrad_6h  = fromfile(pgradname, float32).reshape(ny, nx)
        #****************************************
        # make a2territory
        #----------------------------------------
        tout  = ctrack.aggr_pr(a2life.T, a2pgrad_6h.T, crad, thdura\
                               , miss_int, miss_dbl, lat_first\
                               , dlat, dlon)
        #--
        a2territory_6h = tout[0].T
        #****************************************
        # aggregate precipitation
        #----------------------------------------
        # mask high elevation area
        #-------------
        a2territory_6h = ma.masked_where( a2orog >= thorog, a2territory_6h)
        a2pgrad_6h     = ma.masked_where( a2orog >= thorog, a2pgrad_6h)
        a2ones         = ma.masked_where( a2orog >= thorog, a2ones)
        #-------------
        # mask miss data ( for a2pgrad_6h)
        #-------------
        a2pgrad_6h      = ma.masked_equal(a2pgrad_6h, miss_dbl)
        a2territory_6h  = ma.masked_equal(a2territory_6h, miss_dbl)
        #----------------
        a2pgrad_day = a2pgrad_day + a2pgrad_6h.filled(0.0)
        a2territory_day = a2territory_day + a2territory_6h.filled(0.0)
      #------------------------------------------  
      a2pgrad_day     = a2pgrad_day /4.0
      a2pgrad_day     = ma.masked_equal( a2pgrad_day, miss_dbl)
      #
      a2territory_day = a2territory_day / 4.0
      a2territory_day = ma.masked_equal(a2territory_day, miss_dbl)
      #*******************************************************
      #
      # aggregate daily data
      #
      #------------------------------------------
      stimed  = "%04d%02d%02d00"%(year,mon,day)

      didir   = {}
      diname  = {}
      da2in   = {}
      #---------------------------
      # read daily input data, pap
      #---------------------------
      didir["pap"]   = didir_root["pap"] + "/%s/%s/%s/%04d"%(model, expr, ens, year)
      diname["pap"]  = didir["pap"] + "/%s_%s_%s_%s_%s_%s.bn"%("pap","day", model, expr, ens, stimed)
      da2in["pap"]   = fromfile(diname["pap"], float32).reshape(ny, nx)
      #---------------------------
      # read daily input data, capep
      #---------------------------
      didir["capep"]   = didir_root["capep"] + "/%s/%s/%s/%04d"%(model, expr, ens, year)
      diname["capep"]  = didir["capep"] + "/%s_%s_%s_%s_%s_%s.bn"%("capep","day", model, expr, ens, stimed)
      da2in["capep"]   = fromfile(diname["capep"], float32).reshape(ny, nx)

      #---------------------------
      da2mask ={}
      for iclass in lclass:
        pgradrange = dpgradrange[iclass]
        pgrad_min  = pgradrange[0]
        pgrad_max  = pgradrange[1]
        #-----------
        # mask outside of the cyclone class
        #-----------
        a2mask  = ma.masked_less(a2territory_day, pgrad_min)
        a2mask  = ma.masked_greater_equal(a2mask, pgrad_max)
        da2mask[iclass] = a2mask
        #-----------
        # mask grids with pr < xth
        #-----------
        if xth > 0.0:
          a2mask  = ma.masked_where(a2pr < a2prxth, a2mask)
          da2mask[iclass] = a2mask

        #-----
        # calc, out
        #-----
        for var in lvar:
          a2out_tmp    = ma.masked_where( a2mask.mask, da2in[var]).filled(0.0)
          da2out[var, iclass]  = da2out[var, iclass] + a2out_tmp
        #-----
        # calc, num
        #-----
        a2num_tmp    = ma.masked_where( a2mask.mask, a2ones).filled(0.0)
        da2num[iclass]  = da2num[iclass] + a2num_tmp

      #***************************************
      # plain sp and num # without consideration of cyclone
      #---------------------------------------
      iclass = -1
      #------------------------------------
      # mask grids with pr <= xth
      #-----------
      if xth > 0.0:
        a2mask  = ma.masked_where(a2pr < a2prxth, a2ones)
        da2mask[iclass] = a2mask

      #-----
      # calc, out
      #-----
      for var in lvar:
        a2out_tmp    = ma.masked_where( a2mask.mask, da2in[var]).filled(0.0)
        da2out[var, iclass]  = da2out[var, iclass] + a2out_tmp
      #-----
      # calc, num
      #-----
      a2num_tmp    = ma.masked_where( a2mask.mask, a2ones).filled(0.0)
      da2num[iclass]  = da2num[iclass] + a2num_tmp
#*****************************
# make acc
#----------------
for var in lvar:
  for iclass in lclass[2:]:
    for iclass_temp in lclass[iclass:]:
      da2acc[var, iclass]  = da2acc[var, iclass] + da2out[var, iclass_temp]

# make acc num
for iclass in lclass[2:]:
  for iclass_temp in lclass[iclass:]:
    da2accnum[iclass]    = da2accnum[iclass]   + da2num[iclass_temp]
#*****************************
# sum --> average
#----------------
for var in lvar:
  for iclass in lclass:
    da2out[var, iclass]  =  ma.masked_where(da2num[iclass] ==0.0, da2out[var,iclass]) / da2num[iclass]
    #
    da2out[var, iclass] = da2out[var, iclass].filled(0.0)
#-----
for var in lvar:
  for iclass in lclass[2:]:
    da2acc[var, iclass]  = ma.masked_where(da2accnum[iclass]==0.0, da2acc[var,iclass]) / da2accnum[iclass]
    #
    da2acc[var, iclass] = da2acc[var, iclass].filled(0.0)
##****************************
## write map to files
##----------------------------
for var in lvar:
  for iclass in [-1]+lclass:
    da2out[var, iclass].tofile(doname[var, iclass])
    print doname[var, iclass]

for var in lvar:
  for iclass in lclass[2:]:
    da2acc[var, iclass].tofile(daccname[var, iclass])
    print daccname[var, iclass]

#*****************************
# figure
#-----------------------------
# read mnum
#-----------------------------
dmnum    = {}
daccmnum = {}
mnumdir = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d/mnum"%(model, expr, ens, thdura, im, em, nclass, cmin)

for iclass in lclass:
  mnumname       = mnumdir + "/mnum.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad*0.001, nwbin, season, model, expr, ens)
  dmnum[iclass]   = fromfile(mnumname, float32).reshape(nwbin, ny, nx)[0]

for iclass in lclass[2:]:
  accmnumname     = mnumdir + "/acc.mnum.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad*0.001, nwbin, season, model, expr, ens)  
  daccmnum[iclass]= fromfile(accmnumname, float32).reshape(nwbin, ny, nx)[0]

#-- each class -------
for acckey in ["T", "F"]:
  for var in ["pap","capep"]:
    for iclass in lclass:
      if (acckey == "T")&(iclass in lclass[:2]):
        continue
      #-- prep for map --------
      if acckey == "T":
        figname  = daccname[var, iclass][:-3] + ".png"
      elif acckey == "F":
        figname  = doname[var, iclass][:-3] + ".png"
      #----
      figmap   = plt.figure()
      axmap    = figmap.add_axes([0, 0, 1.0, 1.0])
    
      adat     = fromfile(doname[var, iclass], float32).reshape(ny, nx)
      adat     = ma.masked_where( a2orog > thorog, adat)
      adat     = ma.masked_equal(adat, 0.0)
  
      #-- prep for cbar -------
      cbarname = figname[:-4] + "cbar.png"
      figcbar  = plt.figure(figsize=(1,5))
      axcbar   = figcbar.add_axes([0, 0.1, 0.3, 0.9])
  
      #-- Basemap  ------------
      M        = Basemap(resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
  
      #-- transform --
      adat_trans    = M.transform_scalar(adat, lons, lats, nnx, nny)
      a2mask_trans  = M.transform_scalar(dmnum[iclass], lons, lats, nnx, nny)
  
      #---------------
      if var == "pap":
        bnd      = [0, 50, 100, 150, 200, 500, 1000, 2000]
      elif var == "capep":
        bnd      = [-2000, -1000, -500, -200, -150, -100, -50, 0, 50, 100, 150, 200, 500, 1000, 2000]
      #-----
      if var == "pap":
        bnd_cbar = bnd + [1.0e+40]
      elif var == "capep":
        bnd_cbar = [-1.0e+40] + bnd + [1.0e+40]
      #--
      im       = M.imshow(adat_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap="jet", interpolation="nearest")
      figcbar.colorbar(im, boundaries = bnd_cbar, extend="max", cax=axcbar)
  
      #-- superimpose shade ---
      cmshade  = matplotlib.colors.ListedColormap([ (0.8, 0.8, 0.8), (0.8, 0.8, 0.8) ])
      ashade   = ma.masked_where(a2mask_trans > mnum_min, a2mask_trans)
      im       = M.imshow(ashade, origin="lower", cmap=cmshade, interpolation="nearest")
  
      #---------------
      if acckey  == "T":
        stitle   = "acc.%s [J/kg] %s %s c%02d"%(var, expr, season, iclass)
      elif acckey == "F":
        stitle   = "%s [J/kg] %s %s c%02d"%(var, expr, season, iclass)
      #--
      axmap.set_title(stitle)
  
      #---------------
      M.drawcoastlines()
      figmap.savefig(figname)
      figmap.clf()
      print figname
  
      #---------------
      figcbar.savefig(cbarname)
      figcbar.clf()
#--------------------------------------------------
# dif
#--------------------------------------------------


  
  
  
      
  
  
