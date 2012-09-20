from numpy import *
import calendar
import ctrack_para
import sys, os
#--------------------------------------
iyear   = 1981
eyear   = 1999
#iyear   = 1999
#eyear   = 1999


season  = "DJF"
lmon    =ctrack_para.ret_lmon(season)

prmin   = 0.0
#---- global domain ----------
#latmin_g   = -90.0
#lonmin_g   = 0.0
#dlat_g        = 1.8947368
#dlon_g        = 2.5
#nx_g          = 144
#ny_g          = 96

latmin_g   = -89.375
lonmin_g   = -179.375

latmax_g   = 89.375
lonmax_g   = 179.375
 
dlat_g        = 1.25
dlon_g        = 1.25
nx_g          = 288
ny_g          = 144


#---- small domain -----------
latmin_s       = 24.0  + 0.025
lonmin_s       = 123.0 + 0.025
latmax_s       = 46.0  - 0.025
lonmax_s       = 146   - 0.025

dlat_s         = 0.05
dlon_s         = 0.05

nx_s           = 460
ny_s           = 440

#---- large domain -----------
latmin_l       = 15.0
latmax_l       = 75.0
lonmin_l       = 105.0
lonmax_l       = 160.0

#latmin_l       = 0.0
#latmax_l       = 80.0
#lonmin_l       = 50.0
#lonmax_l       = 250.0


#latmin_l       = 15.0
#latmax_l       = 15.0
#lonmin_l       = 105.0
#lonmax_l       = 106.0


#-----------------------------
ymin_l         = int((latmin_l + dlat_g*0.5 - latmin_g)/dlat_g)
ymax_l         = int((latmax_l + dlat_g*0.5 - latmin_g)/dlat_g)
xmin_l         = int((lonmin_l + dlon_g*0.5 - lonmin_g)/dlon_g)
xmax_l         = int((lonmax_l + dlon_g*0.5 - lonmin_g)/dlon_g)
print ymin_l, ymax_l
print xmin_l, xmax_l

ny_l           = ymax_l - ymin_l +1
nx_l           = xmax_l - xmin_l +1
#--------------------------------------
#--------------------------------------
didir_root         = {}
didir_root["pr"]   = "/media/disk2/data/aphro/DPREC"
didir_root["psl"]  = "/media/disk2/data/MERRA/bn/day/slp"

#--------------------------------------
didir      = {}
didir["pr"]= didir_root["pr"]
iname_pr   = didir["pr"]  + "/AphroJP_V1207_DPREC.%04d"%(1990)

a1pr       = ma.masked_less(fromfile(iname_pr, float32).reshape(365, -1)[0], 0.0).compressed()
ngrids_s   = len(a1pr)

#-- matching latlon, n_orgiginal, n_compressed ----
a2pr_temp  = fromfile(iname_pr, float32).reshape(365, ny_s, nx_s)[0]
dnorg_ncomp = {}
norg_s  = -1
ncomp_s = -1
for iy in range(ny_s):
  for ix in range(nx_s):
    norg_s  = norg_s + 1
    if a2pr_temp[iy, ix] >=0.0:
      ncomp_s = ncomp_s + 1 
      dnorg_ncomp[norg_s] = ncomp_s

def latlon2yx_l(lat, lon):
  print lat, lon
  x_l = int((lon - lonmin_l)/ dlon_g)
  y_l = int((lat - latmin_l)/ dlat_g)
  return (y_l, x_l) 

def latlon2ncomp_s(lat, lon):
  x_s = int((lon - lonmin_s)/ dlon_s)
  y_s = int((lat - latmin_s)/ dlat_s)

  norg_s  = y_s* nx_s + x_s
  #return y_s, x_s
  ncomp_s = dnorg_ncomp[norg_s]
  return ncomp_s

#-------------------------------------
# dummy
#---------
#ngrids_s   = 1

a1one       = ones([ngrids_s], float64)
a1snum       = zeros([ngrids_s], float64)
a3sxy       = zeros([ngrids_s, ny_l, nx_l], float64)
a1sxx       = zeros([ngrids_s], float64)
a1sx        = zeros([ngrids_s], float64)
a3syy       = zeros([ngrids_s, ny_l, nx_l], float64)
a3sy        = zeros([ngrids_s, ny_l, nx_l], float64)
a3my        = zeros([ngrids_s, ny_l, nx_l], float64)
#-------------------------------------
didir   = {}
nday    = 0

lpr     = []
lpsl    = []
for year in range(iyear, eyear+1):
  iiday  = 0
  didir["pr"]      = didir_root["pr"]
  didir["psl"]     = didir_root["psl"] + "/%04d"%(year)
  #------------
  iname_pr   = didir["pr"]  + "/AphroJP_V1207_DPREC.%04d"%(year)
  if calendar.isleap(year):
    a3pr       = fromfile(iname_pr, float32).reshape(366, ny_s, nx_s)  
    a3pr       = r_[a3pr[:31+28], a3pr[31+28+1:]]
  else:
    a3pr       = fromfile(iname_pr, float32).reshape(365, ny_s, nx_s)  
  #--------------
  for mon in lmon:
  #for mon in [1]:
    #--- skip leap --
    if (mon == 2)&(calendar.isleap(year)):
      eday = calendar.monthrange(year, mon)[1]-1
    else:
      eday = calendar.monthrange(year, mon)[1]

    #----------------
    for day in range(1, eday+1):
    #for day in [1,2,3]:
      print year, mon, day
      #--- pr   -----
      a1pr  = a3pr[iiday]
      a1pr  = array(a1pr, float64)
      a1pr  = ma.masked_less(a1pr, 0.0).compressed()
      a1pr  = a1pr[:ngrids_s]
      #--------------
      iiday  = iiday+ 1

      #-- load psl data ----------------
      iname_psl  = didir["psl"] + "/MERRA.day.slp.1999122800.bn"
      iname_psl  = didir["psl"] + "/MERRA.day.slp.%04d%02d%02d00.bn"%(year, mon, day)
      #
      a2psl      = fromfile(iname_psl, float32).reshape(ny_g, nx_g)*0.01
      a2psl      = array(a2psl, float64)
      a2psl      = a2psl[ymin_l:ymax_l+1, xmin_l:xmax_l+1]

      #--- mask -----
      a1mask = ma.masked_where(a1pr <= prmin, a1pr)

      #--- num  -----
      a1num   = ma.masked_where(a1mask.mask, a1one).filled(0.0)
      a1snum  = a1snum + a1num

      #--- a1xx -----
      a1pr   = ma.masked_where(a1mask.mask, a1pr).filled(0.0)
      a1sxx  = a1sxx + a1pr*a1pr

      #--- a1x  -----
      a1sx   = a1sx  + a1pr

      #--- a2yy -----
      for igrid_s in range(ngrids_s):
        if a1num[igrid_s] ==0.0:
          a3syy[igrid_s]  = a3syy[igrid_s]
        else:
          a3syy[igrid_s]  = a3syy[igrid_s] + a2psl * a2psl

      #--- a2y ------
      for igrid_s in range(ngrids_s):
        if a1num[igrid_s] == 0.0:
          a3sy[igrid_s]   = a3sy[igrid_s]
        else:
          a3sy[igrid_s]   = a3sy[igrid_s]  + a2psl

      #--- a3xy -----
      for igrid_s in range(ngrids_s):
        if a1num[igrid_s] == 0.0:
          a3sxy[igrid_s] = a3sxy[igrid_s]
        else:
          a3sxy[igrid_s] = a3sxy[igrid_s] + a2psl * a1pr[igrid_s]

      if a1num[igrid_s] != 0.0:
        lpr.append(a1pr[0])
        lpsl.append(a2psl[0,0])

#-------------------------------------
a1mx   = a1sx / a1snum
for igrid_s in range(ngrids_s):
  a3my[igrid_s]   = a3sy[igrid_s] / a1snum[igrid_s]

#-------------------------------------
#
a3corr = zeros([ngrids_s, ny_l, nx_l], float64)
#
for igrid_s in arange(ngrids_s):
  a2bunshi  = a3sxy[igrid_s] - a3my[igrid_s]*a1sx[igrid_s] - a1mx[igrid_s]*a3sy[igrid_s] + a1snum[igrid_s]*a1mx[igrid_s]*a3my[igrid_s]

  vbunbo1   = (a1sxx[igrid_s] - 2*a1mx[igrid_s]*a1sx[igrid_s] + a1snum[igrid_s]*a1mx[igrid_s]*a1mx[igrid_s])**0.5

  a2bunbo2  = (a3syy[igrid_s] - 2*a3my[igrid_s]*a3sy[igrid_s] + a1snum[igrid_s]*a3my[igrid_s]*a3my[igrid_s])**0.5

  a3corr[igrid_s]  = a2bunshi / (vbunbo1 * a2bunbo2)

#----------------------------------
a3corr = array(a3corr, float32)
sodir  = "/media/disk2/out/MERRA/day/ctrack/corr"
soname = sodir + "/MERRA.corr.pr.psl.%s.%s.bn"%(season, ncomp_s+1)
a3corr.tofile(soname)
print soname


#from mpl_toolkits.basemap import Basemap
#import matplotlib.pyplot as plt
#
#lat = 33.0
#lon = 131.0
#(y_l, x_l)   = latlon2yx_l(lat, lon)
#ncomp_s      = latlon2ncomp_s( lat, lon)
#a2in         = a3corr[ncomp_s]
#
#lats         = linspace(latmin_g, latmax_g, ny_g)
#lons         = linspace(lonmin_g, lonmax_g - lonmax_g/nx_g, nx_g)
#
##---------------
## -- basemap
##---------------
#figmap  = plt.figure()
#axmap   = figmap.add_axes([0, 0.1, 1.0, 0.8])
#M    = Basemap(resolution="l", llcrnrlat=latmin_l, llcrnrlon=lonmin_l, urcrnrlat=latmax_l, urcrnrlon=lonmax_l, ax=axmap)
#
#im           = M.imshow(a2in, origin="lower")
#
#M.scatter(lon, lat, color="r", marker="o")
#
#M.drawcoastlines()
#plt.savefig("temp.png")
#plt.clf()
#
