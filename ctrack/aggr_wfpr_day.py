from ctrack import *
import ctrack_para
from numpy import *
import calendar
import datetime
import os, sys


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
  iz500    = int(sys.argv[17])
  xth      = float(sys.argv[18])
  #---
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
  nz          = 8
  miss_dbl    = -9999.0
  miss_int    = -9999
  crad        = 1000.0*1000.0
  thdura      = 24
  thorog      = 1500.0
  iz500       = 3
  xth         = 90.0
dnumname = {}
dspname = {}
dsp2name = {}
dswname = {}
dsw2name = {}
dmpgradname = {}
 
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
outdir     = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d"%(model, expr, ens, thdura, im, em, nclass, cmin)
#
mk_dir(outdir)
#-----------
# number of events
#-----------
outdir_num = outdir + "/num"
mk_dir(outdir_num)
if (dnumname =={}):
  dnumname  = {}
  for iclass in [-1] +lclass:
    dnumname[iclass ] = outdir_num + "/num.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad*0.001, nwbin, season, "day", model, expr, ens)
#-----------
# number of events , annual data
#-----------
for year in range(iy, ey+1):
  outdir_num_ann = outdir + "/num/%04d"%(year)
  mk_dir(outdir_num_ann)
  for iclass in [-1] +lclass:
    dnumname[year, iclass ] = outdir_num_ann + "/num.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad*0.001, nwbin, season, "day", model, expr, ens)
#-----------
# sum of precip
#-----------
outdir_sp = outdir + "/sp"
mk_dir(outdir_sp)
if (dspname =={}):
  dspname  = {}
  for iclass in [-1] +lclass:
    dspname[iclass ] = outdir_sp + "/sp.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad*0.001, nwbin, season, "day", model, expr, ens)
#-----------
# sum of precip, annual data
#-----------
for year in range(iy, ey +1):
  outdir_sp_ann = outdir + "/sp/%04d"%(year)
  mk_dir(outdir_sp_ann)
  for iclass in [-1] +lclass:
    dspname[year, iclass ] = outdir_sp_ann + "/sp.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad*0.001, nwbin, season, "day", model, expr, ens)

#-----------
# sum of precip**2
#-----------
outdir_sp2 = outdir + "/sp2"
mk_dir(outdir_sp2)
if (dsp2name =={}):
  dsp2name  = {}
  for iclass in [-1] +lclass:
    dsp2name[iclass ] = outdir_sp2 + "/sp2.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad*0.001, nwbin, season, "day", model, expr, ens)
#-----------
# sum of w
#-----------
outdir_sw = outdir + "/sw"
mk_dir(outdir_sw)
if (dswname =={}):
  dswname  = {}
  for iclass in [-1] +lclass:
    dswname[iclass ] = outdir_sw + "/sw.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad*0.001, nwbin, season, "day", model, expr, ens)
#-----------
# sum of w2
#-----------
outdir_sw2 = outdir + "/sw2"
mk_dir(outdir_sw2)
if (dsw2name =={}):
  dsw2name  = {}
  for iclass in [-1] +lclass:
    dsw2name[iclass ] = outdir_sw2 + "/sw2.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad*0.001, nwbin, season, "day", model, expr, ens)
#----------------------
# mean of pgrad
#-----------
outdir_mpgrad = outdir + "/mpgrad"
mk_dir(outdir_mpgrad)
if (dmpgradname =={}):
  dmpgradname  = {}
  for iclass in [-1] +lclass:
    dmpgradname[iclass ] = outdir_mpgrad + "/mpgrad.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, cmin, iclass, nclass, crad*0.001, nwbin, season, "day", model, expr, ens)


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
wapdir_root     = "/media/disk2/data/CMIP5/bn/wap/%s"%("day")
wapupdir_root   = "/media/disk2/data/CMIP5/bn/wapup/%s"%("day")
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
# dummy for da2num
#--------------
da2num = {}
for iw in dlwbin.keys():
  #for iclass in lclass:
  for iclass in [-1]+lclass:
    da2num[iclass, iw] = zeros( nx*ny).reshape(ny,nx)
#**************
# dummy for da2sp
#--------------
da2sp = {}
for iw in dlwbin.keys():
  #for iclass in lclass:
  for iclass in [-1]+lclass:
    da2sp[iclass, iw] = zeros( nx*ny).reshape(ny,nx)
#**************
# dummy for da2sp2
#--------------
da2sp2 = {}
for iw in dlwbin.keys():
  #for iclass in lclass:
  for iclass in [-1]+lclass:
    da2sp2[iclass, iw] = zeros( nx*ny).reshape(ny,nx)
#**************
# dummy for da2sw
#--------------
da2sw = {}
for iw in dlwbin.keys():
  #for iclass in lclass:
  for iclass in [-1]+lclass:
    da2sw[iclass, iw] = zeros( nx*ny).reshape(ny,nx)
#**************
# dummy for da2sw2
#--------------
da2sw2 = {}
for iw in dlwbin.keys():
  #for iclass in lclass:
  for iclass in [-1]+lclass:
    da2sw2[iclass, iw] = zeros( nx*ny).reshape(ny,nx)
#**************
# dummy for da2mpgrad
#--------------
da2mpgrad = {}
for iw in dlwbin.keys():
  #for iclass in lclass:
  for iclass in [-1]+lclass:
    da2mpgrad[iclass, iw] = zeros( nx*ny).reshape(ny,nx)
#**************
# make a2ones 
#--------------
a2ones = ones(nx*ny).reshape(ny, nx)
#--------------
for year in range(iyear, eyear+1):
  #--------------
  # dummy for da2num, annual data
  #--------------
  da2num_ann = {}
  for iw in dlwbin.keys():
    #for iclass in lclass:
    for iclass in [-1]+lclass:
      da2num_ann[iclass, iw] = zeros( nx*ny).reshape(ny,nx)
  #**************
  # dummy for da2sp, annual data
  #--------------
  da2sp_ann = {}
  for iw in dlwbin.keys():
    #for iclass in lclass:
    for iclass in [-1]+lclass:
      da2sp_ann[iclass, iw] = zeros( nx*ny).reshape(ny,nx)
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
      a2territory_day = zeros(nx*ny).reshape(ny, nx)
      a2pgrad_day     = zeros(nx*ny).reshape(ny, nx)
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
      ##------------------------------------------
      ## read daily omega data
      ##---------------------------
      wapdir   = wapdir_root   + "/%s/%s/%s/%04d"%(model, expr, ens, year)
      wapname  = wapdir        + "/wap_%s_%s_%s_%s_%s.bn"%("day", model, expr, ens, stimed)
      a2wap    = fromfile(wapname, float32).reshape(nz, ny, nx)[iz500]
      ##------------------------------------------
      ## read daily precip data
      ##---------------------------
      prdir   = prdir_root   + "/%s/%s/%s/%04d"%(model, expr, ens, year)
      prname  = prdir        + "/pr_%s_%s_%s_%s_%s.bn"%("day", model, expr, ens, stimed)
      a2pr    = fromfile(prname, float32).reshape(ny, nx)
      #---------------------------
      da2mask ={}
      for iclass in lclass:
      #for iclass in [0]:
        pgradrange = dpgradrange[iclass]
        pgrad_min  = pgradrange[0]
        pgrad_max  = pgradrange[1]
        #************************************
        # start wbin loop
        #------------------------------------
        for iw in dlwbin.keys():
        #for iw in [0]:
          wrange =  - array(dlwbin[iw])
          wmin   = wrange.min()
          wmax   = wrange.max()
          #-----------
          # mask outside of the cyclone class
          #-----------
          #a2mask  = ma.masked_outside(a2territory_day, pgrad_min, pgrad_max)
          a2mask  = ma.masked_less(a2territory_day, pgrad_min)
          a2mask  = ma.masked_greater_equal(a2mask, pgrad_max)
          da2mask[iclass, iw] = a2mask
          #-----------
          # mask outside of the wbin range
          #-----------
          a2mask  = ma.masked_where(a2wap< wmin,  a2mask)
          a2mask  = ma.masked_where(wmax <= a2wap, a2mask)
          da2mask[iclass, iw] = a2mask

          #-----------
          # mask grids with pr < xth
          #-----------
          if xth > 0.0:
            a2mask  = ma.masked_where(a2pr < a2prxth, a2mask)
            da2mask[iclass, iw] = a2mask
          #-----
          # num
          #-----
          a2num_tmp   = ma.masked_where( a2mask.mask, a2ones ).filled(0.0)
          da2num[iclass, iw] = da2num[iclass, iw] + a2num_tmp
          da2num_ann[iclass, iw] = da2num_ann[iclass, iw] + a2num_tmp

          #-----
          # sp
          #-----
          a2sp_tmp    = ma.masked_where( a2mask.mask, a2pr).filled(0.0)
          da2sp[iclass, iw]  = da2sp[iclass, iw] + a2sp_tmp
          da2sp_ann[iclass, iw] = da2sp_ann[iclass, iw] + a2sp_tmp

          #-----
          # sp2
          #-----
          a2sp2_tmp   = ma.masked_where( a2mask.mask, a2pr).filled(0.0)
          da2sp2[iclass, iw]  = da2sp2[iclass, iw] + a2sp2_tmp * a2sp2_tmp
          #-----
          # sw
          #-----
          a2sw_tmp    = ma.masked_where( a2mask.mask, a2wap).filled(0.0)
          da2sw[iclass, iw]  = da2sw[iclass, iw] + a2sw_tmp
          #-----
          # sw2
          #-----
          a2sw2_tmp    = ma.masked_where( a2mask.mask, a2wap).filled(0.0)
          da2sw2[iclass, iw]  = da2sw2[iclass, iw] + a2sw2_tmp * a2sw2_tmp
          #-----
          # mpgrad
          #-----
          a2mpgrad_tmp = ma.masked_where( a2mask.mask, a2territory_day).filled(0.0)
          da2mpgrad[iclass, iw]  = da2mpgrad[iclass, iw] + a2mpgrad_tmp


      #***************************************
      # plain sp and num # without consideration of cyclone
      #---------------------------------------
      iclass = -1
      #------------------------------------
      # start wbin loop
      #------------------------------------
      for iw in dlwbin.keys():
        wrange =  - array(dlwbin[iw])
        wmin   = wrange.min()
        wmax   = wrange.max()
        #-----------
        # mask outside of the wbin range
        #-----------
        a2mask  = ma.masked_where(a2wap< wmin,  a2pr)
        a2mask  = ma.masked_where(wmax < a2wap, a2mask)
        da2mask[iclass, iw] = a2mask

        #-----------
        # mask grids with pr <= xth
        #-----------
        if xth > 0.0:
          a2mask  = ma.masked_where(a2pr < a2prxth, a2mask)
          da2mask[iclass, iw] = a2mask
        #-----
        # num
        #-----
        a2num_tmp   = ma.masked_where( a2mask.mask, a2ones ).filled(0.0)
        da2num[iclass, iw] = da2num[iclass, iw] + a2num_tmp
        da2num_ann[iclass, iw] = da2num_ann[iclass, iw] + a2num_tmp
        #-----
        # sp
        #-----
        a2sp_tmp    = ma.masked_where( a2mask.mask, a2pr).filled(0.0)
        da2sp[iclass, iw]  = da2sp[iclass, iw] + a2sp_tmp
        da2sp_ann[iclass, iw] = da2sp_ann[iclass, iw] + a2sp_tmp

        #-----
        # sp2
        #-----
        a2sp2_tmp   = ma.masked_where( a2mask.mask, a2pr).filled(0.0)
        da2sp2[iclass, iw]  = da2sp2[iclass, iw] + a2sp2_tmp * a2sp2_tmp
        #-----
        # sw
        #-----
        a2sw_tmp    = ma.masked_where( a2mask.mask, a2wap).filled(0.0)
        da2sw[iclass, iw]  = da2sw[iclass, iw] + a2sw_tmp
        #-----
        # sw2
        #-----
        a2sw2_tmp    = ma.masked_where( a2mask.mask, a2wap).filled(0.0)
        da2sw2[iclass, iw]  = da2sw2[iclass, iw] + a2sw2_tmp * a2sw2_tmp
        #-----
        # mpgrad
        #-----
        a2mpgrad_tmp    = ma.masked_where( a2mask.mask, a2territory_day).filled(0.0)
        da2mpgrad[iclass, iw]  = da2mpgrad[iclass, iw] + a2mpgrad_tmp

  #****************************
  # combine all wbins to one array, annual data
  #----------------------------
  # num_ann
  #---------
  da2num_ann_comb ={}
  #for iclass in lclass:
  for iclass in [-1] + lclass:
    da2num_ann_comb[iclass] = []
    for iw in dlwbin.keys():
      da2num_ann_comb[iclass] = da2num_ann_comb[iclass] + da2num_ann[iclass, iw].flatten().tolist()
    #-
    da2num_ann_comb[iclass] = array(da2num_ann_comb[iclass], float32).reshape(nwbin, ny, nx)
  #---------
  # sp_ann
  #---------
  da2sp_ann_comb ={}
  #for iclass in lclass:
  for iclass in [-1] + lclass:
    da2sp_ann_comb[iclass] = []
    for iw in dlwbin.keys():
      da2sp_ann_comb[iclass] = da2sp_ann_comb[iclass] + da2sp_ann[iclass, iw].flatten().tolist()
    #-
    da2sp_ann_comb[iclass] = array(da2sp_ann_comb[iclass], float32).reshape(nwbin, ny, nx)
  ##****************************
  ## write annual map to files
  ##----------------------------
  for iclass in [-1]+lclass:
    da2num_ann_comb[iclass].tofile(dnumname[year, iclass])
    da2sp_ann_comb[iclass].tofile(dspname[year, iclass])
  #
  print dspname[year, iclass] 
#****************************
# combine all wbins to one array
#----------------------------
# num
#---------
da2num_comb ={}
#for iclass in lclass:
for iclass in [-1] + lclass:
  da2num_comb[iclass] = []
  for iw in dlwbin.keys():
    da2num_comb[iclass] = da2num_comb[iclass] + da2num[iclass, iw].flatten().tolist()
  #-
  da2num_comb[iclass] = array(da2num_comb[iclass], float32).reshape(nwbin, ny, nx)
#---------
# sp
#---------
da2sp_comb ={}
#for iclass in lclass:
for iclass in [-1] + lclass:
  da2sp_comb[iclass] = []
  for iw in dlwbin.keys():
    da2sp_comb[iclass] = da2sp_comb[iclass] + da2sp[iclass, iw].flatten().tolist()
  #-
  da2sp_comb[iclass] = array(da2sp_comb[iclass], float32).reshape(nwbin, ny, nx)
#---------
# sp2
#---------
da2sp2_comb ={}
#for iclass in lclass:
for iclass in [-1] + lclass:
  da2sp2_comb[iclass] = []
  for iw in dlwbin.keys():
    da2sp2_comb[iclass] = da2sp2_comb[iclass] + da2sp2[iclass, iw].flatten().tolist()
  #-
  da2sp2_comb[iclass] = array(da2sp2_comb[iclass], float32).reshape(nwbin, ny, nx)
#---------
# sw
#---------
da2sw_comb ={}
#for iclass in lclass:
for iclass in [-1] + lclass:
  da2sw_comb[iclass] = []
  for iw in dlwbin.keys():
    da2sw_comb[iclass] = da2sw_comb[iclass] + da2sw[iclass, iw].flatten().tolist()
  #-
  da2sw_comb[iclass] = array(da2sw_comb[iclass], float32).reshape(nwbin, ny, nx)
#---------
# sw2
#---------
da2sw2_comb ={}
#for iclass in lclass:
for iclass in [-1] + lclass:
  da2sw2_comb[iclass] = []
  for iw in dlwbin.keys():
    da2sw2_comb[iclass] = da2sw2_comb[iclass] + da2sw2[iclass, iw].flatten().tolist()
  #-
  da2sw2_comb[iclass] = array(da2sw2_comb[iclass], float32).reshape(nwbin, ny, nx)
#---------
# mpgrad
#---------
da2mpgrad_comb ={}
#for iclass in lclass:
for iclass in [-1] + lclass:
  da2mpgrad_comb[iclass] = []
  for iw in dlwbin.keys():
    da2mpgrad_comb[iclass] = da2mpgrad_comb[iclass] + da2mpgrad[iclass, iw].flatten().tolist()
  #-
  da2mpgrad_comb[iclass] = array(da2mpgrad_comb[iclass], float32).reshape(nwbin, ny, nx)
  da2mpgrad_comb[iclass] = ma.masked_where( da2num_comb[iclass]==0.0, da2mpgrad_comb[iclass]) / da2num_comb[iclass]
  da2mpgrad_comb[iclass] = da2mpgrad_comb[iclass].filled(0.0)
#
##****************************
## write map to files
##----------------------------

#for iclass in lclass:
for iclass in [-1]+lclass:
  da2num_comb[iclass].tofile(dnumname[iclass])
  da2sp_comb[iclass].tofile(dspname[iclass])
  da2sp2_comb[iclass].tofile(dsp2name[iclass])
  da2sw_comb[iclass].tofile(dswname[iclass])
  da2sw2_comb[iclass].tofile(dsw2name[iclass])
  da2mpgrad_comb[iclass].tofile(dmpgradname[iclass])
 
  print dnumname[iclass]

