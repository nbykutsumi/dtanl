from numpy import *
import calendar
import ctrack_para
import sys, os
#--------------------------------------
iyear   = 1998
eyear   = 1999
season  = "DJF"
lmon    =ctrack_para.ret_lmon(season)
model   = "NorESM1-M"
expr    = "historical"
ens     = "r1i1p1"


prmin   = 0.0
#---- global domain ----------
lat_first_g   = -90.0
lon_first_g   = 0.0
dlat_g        = 1.8947368
dlon_g        = 2.5
nx_g          = 144
ny_g          = 96

#---- small domain -----------
latmin_s       = 24.0  + 0.025
lonmin_s       = 123.0 + 0.025
latmax_s       = 46.0  - 0.025
lonmax_s       = 146   - 0.025
nx_s           = 440
ny_s           = 460

#---- large domain -----------
#latmin_l       = 15.0
#latmax_l       = 75.0
#lonmin_l       = 105.0
#lonmax_l       = 180.0

#latmin_l       = 0.0
#latmax_l       = 80.0
#lonmin_l       = 50.0
#lonmax_l       = 250.0


latmin_l       = 15.0
latmax_l       = 15.0
lonmin_l       = 105.0
lonmax_l       = 106.0


#-----------------------------
ymin_l         = int((latmin_l + dlat_g*0.5 - lat_first_g)/dlat_g)
ymax_l         = int((latmax_l + dlat_g*0.5 - lat_first_g)/dlat_g)
xmin_l         = int((lonmin_l + dlon_g*0.5 - lon_first_g)/dlon_g)
xmax_l         = int((lonmax_l + dlon_g*0.5 - lon_first_g)/dlon_g)
print ymin_l, ymax_l
print xmin_l, xmax_l

ny_l           = ymax_l - ymin_l +1
nx_l           = xmax_l - xmin_l +1
#--------------------------------------
#--------------------------------------
didir_root         = {}
didir_root["pr"]   = "/media/disk2/data/aphro/DPREC"
didir_root["psl"]  = "/media/disk2/data/CMIP5/bn/psl/day/%s/%s/%s"%(model, expr, ens)

#--------------------------------------
didir      = {}
didir["pr"]= didir_root["pr"]
iname_pr   = didir["pr"]  + "/AphroJP_V1207_DPREC.%04d"%(1990)
a1pr       = ma.masked_less(fromfile(iname_pr, float32).reshape(365, -1)[0], 0.0).compressed()
ngrids_s   = len(a1pr)
#-------------------------------------
# dummy
#---------
ngrids_s   = 1

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
    #for day in [1,2]:
      #print year, mon, day
      #--- pr   -----
      a1pr  = a3pr[iiday]
      a1pr  = array(a1pr, float64)
      a1pr  = ma.masked_less(a1pr, 0.0).compressed()
      a1pr  = a1pr[:ngrids_s]
      #--------------
      iiday  = iiday+ 1

      #-- load psl data ----------------
      iname_psl  = didir["psl"] + "/%s_day_%s_%s_%s_%04d%02d%02d00.bn"%("psl",model, expr, ens, year, mon, day)
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

  vbunbo1  = (a1sxx[igrid_s] - 2*a1mx[igrid_s]*a1sx[igrid_s] + a1snum[igrid_s]*a1mx[igrid_s]*a1mx[igrid_s])**0.5

  a2bunbo2  = (a3syy[igrid_s] - 2*a3my[igrid_s]*a3sy[igrid_s] + a1snum[igrid_s]*a3my[igrid_s]*a3my[igrid_s])**0.5

  a3corr[igrid_s]  = a2bunshi / (vbunbo1 * a2bunbo2)

#----------------------------------
