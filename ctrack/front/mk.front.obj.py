from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib
from numpy import *
import calendar
import ctrack_para
import ctrack_func
import sys, os
import gsmap_func
from cf.plot import *
import datetime
from dtanl_fsub import *
from ctrack_fsub import *
#-----------------------
contflag = "True"
#contflag = "False"

if len(sys.argv) > 1:
  year  = int(sys.argv[1])
  mon   = int(sys.argv[2])
  day   = int(sys.argv[3])
  hour  = int(sys.argv[4])
  lllat = float(sys.argv[5])
  urlat = float(sys.argv[6])
  lllon = float(sys.argv[7])
  urlon = float(sys.argv[8])
  plev = float(sys.argv[9])
  cbarflag  = sys.argv[10]
  thdura    = float(sys.argv[11])
  thfmasktheta1 = float(sys.argv[12])
  thfmasktheta2 = float(sys.argv[13])

else:
  year  = 2004
  mon   = 1
  day   = 18
  hour  = 0
  #local region ------
  #corner points should be
  #at the center of original grid box
  #lllat   = 20.
  #urlat   = 60.
  #lllon   = 110.
  #urlon   = 160.

  lllat    = 0.0
  urlat    = 80.
  lllon    = 60.
  urlon    = 190.

  #lllat    = 20.0
  #urlat    = 60.0
  #lllon    = 110.
  #urlon    = 160.

  plev     = 850 *100.0   #(Pa)
  cbarflag = "True"
  thdura   = 6
  thfmasktheta1 = 0.5
  thfmasktheta2 = 2.0

#-----------------------------
#-----------------------------
miss_out  = -9999.0
ny  = 180
nx  = 360
highsidedist  = ctrack_para.ret_highsidedist()

stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)
sodir_root    = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/%02dh"%(thdura)
sodir         = sodir_root + "/%04d%02d/front/%02d"%(year, mon, day)
#sodir         = "/home/utsumi/temp"
cbardir       = sodir[:-3]
#sodir         = sodir_root + "/%04d%02d/baiu"%(year, mon)
#cbardir       = sodir

ctrack_func.mk_dir(sodir)

dlat    = 1.0
dlon    = 1.0
a1lat   = arange(-89.5, 89.5  + dlat*0.1, dlat)
a1lon   = arange(0.5,   359.5 + dlon*0.1, dlon)

meridians = 10.0
parallels = 10.0

thorog  = ctrack_para.ret_thorog()
thgradorog=ctrack_para.ret_thgradorog()
#************************
# for mapping
nnx        = int( (urlon - lllon)/dlon)
nny        = int( (urlat - lllat)/dlat)
a1lon_loc  = linspace(lllon, urlon, nnx)
a1lat_loc  = linspace(lllat, urlat, nny)
LONS, LATS = meshgrid( a1lon_loc, a1lat_loc)

xdom_saone_first = int((lllon - 0.5 + 0.5)/1.0)
xdom_saone_last  = int((urlon - 0.5 + 0.5)/1.0)
ydom_saone_first = int((lllat -(-89.5) + 0.5)/1.0)
ydom_saone_last  = int((urlat -(-89.5) + 0.5)/1.0)

#************************
# FUNCTIONS
#************************
# front locator :contour
#---------------
def mk_front_loc_contour(a2thermo, a2gradthermo, thfmask1, thfmask2):
  a2fmask1 = dtanl_fsub.mk_a2frontmask1(a2thermo.T).T
  a2fmask2 = dtanl_fsub.mk_a2frontmask2(a2thermo.T).T
  a2fmask1 = a2fmask1 * (1000.0*100.0)**2.0  #[(100km)-2]
  a2fmask2 = a2fmask2 * (1000.0*100.0)       #[(100km)-1]
 
  (a2grad2x, a2grad2y) = dtanl_fsub.mk_a2grad_saone(a2gradthermo.T)
  a2grad2x = a2grad2x.T
  a2grad2y = a2grad2y.T
  a2loc    = dtanl_fsub.mk_a2axisgrad(a2grad2x.T, a2grad2y.T).T
  a2loc    = dtanl_fsub.mk_a2contour(a2loc.T, 0.0, 0.0, miss_out).T
  a2loc    = ma.masked_equal(a2loc, miss_out)  
  a2loc    = ma.masked_where(a2fmask1 < thfmask1, a2loc)
  a2loc    = ma.masked_where(a2fmask2 < thfmask2, a2loc)
  return a2loc

#---------------
# locator
#---------------
def mk_front_loc(a2thermo, a2gradthermo, thfmask1, thfmask2):
  a2fmask1 = dtanl_fsub.mk_a2frontmask1(a2thermo.T).T
  a2fmask2 = dtanl_fsub.mk_a2frontmask2(a2thermo.T).T
  a2fmask1 = a2fmask1 *(1000.0*100.0)**2.0  #[(100km)-2]
  a2fmask2 = a2fmask2 *(1000.0*100.0)       #[(100km)-1]

  a2loc    = a2gradthermo  
  a2loc    = ma.masked_where(a2fmask1 < thfmask1, a2loc)
  a2loc    = ma.masked_where(a2fmask2 < thfmask2, a2loc)
  return a2loc

#******************************************************
#-- U wind at 850hPa ---------------------------
plev_temp  = 850*100.0
idir_root  = "/media/disk2/data/JRA25/sa.one/6hr"
idir       = idir_root + "/UGRD/%04d%02d"%(year, mon)
uname850   = idir + "/anal_p25.UGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_temp*0.01, year, mon, day, hour)
a2u850     = fromfile(uname850, float32).reshape(ny,nx)

#-- q: mixing ratio --------------------------
qname = "/media/disk2/data/JRA25/sa.one/6hr/SPFH/%04d%02d/anal_p25.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
a2q   = fromfile(qname, float32).reshape(ny,nx)

#-- t: ---------------------------------------
tname = "/media/disk2/data/JRA25/sa.one/6hr/TMP/%04d%02d/anal_p25.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
a2t   = fromfile(tname, float32).reshape(ny,nx)

#-- tv: --------------------------------------
a2tv  = a2t * (1.0+0.61*a2q)

#-- a2gradtv ---------------------------------
a2gradtv  = dtanl_fsub.mk_a2grad_abs_saone(a2tv.T).T

#-- theta_e -----------------------------------
a2theta_e = dtanl_fsub.mk_a2theta_e(plev, a2t.T, a2q.T).T
#-- grad.theta_e ------------------------------------
a2thermo         = a2theta_e
a2gradtheta_e    = dtanl_fsub.mk_a2grad_abs_saone(a2thermo.T).T

#**********************************************
# base: grad.theta_e
a2gradtheta_e  = a2gradtheta_e * 1000.0*100.0 # [K (100km)-1]

##**********************************************
# front locator: theta_e
a2thermo             = a2theta_e # K
a2gradthermo         = a2gradtheta_e   # K/100km
thfmask1 = thfmasktheta1
thfmask2 = thfmasktheta2

vtype  = "loc.theta_e"
#bnd        = [0.1, 0.4, 0.7, 1.0,1.3,1.6,1.9,2.2,2.5]
#bnd        = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
bnd        = [0.0, 0.000005,  0.000007, 0.000009, 0.000011]
scm        = "jet"
stitle     = "%s (K 100km-1)\n"%(vtype)
stitle     = stitle + "M1:%3.2f M2:%3.2f\n"%(thfmask1, thfmask2)
stitle     = stitle + "%04d-%02d-%02d  UTC %02d:00 (JST %02d:00)"%(year, mon, day, hour, hour+9)
soname     = sodir + "/front.%s.%04d.%02d.%02d.%02d.png"%(vtype, year, mon, day, hour)
cbarname   = cbardir + "/cbar.%s.png"%(vtype)

#******************************************************
#-- orog & grad orog ----
orogname   = "/media/disk2/data/JRA25/sa.one/const/topo/topo.sa.one"
gradorogadjname= "/media/disk2/data/JRA25/sa.one/const/topo/grad.topo.adj.twogrids.sa.one"
a2orog     = fromfile(orogname, float32).reshape(ny,nx)
a2gradorogmask = fromfile(gradorogadjname, float32).reshape(ny,nx)

#
#------
if contflag == "True":
  a2loc    = mk_front_loc_contour(a2thermo, a2gradthermo, thfmask1, thfmask2)
  a2loc    = ma.masked_where(a2orog > thorog, a2loc).filled(miss_out)
  a2loc    = ma.masked_where(a2gradorogmask > thgradorog, a2loc).filled(miss_out)
  a2loc    = dtanl_fsub.del_front_2grids(a2loc.T, miss_out).T
  a2loc    = ctrack_fsub.find_highsidevalue_saone(a2gradtheta_e.T, a2loc.T, a2gradtv.T, highsidedist, miss_out).T
  mk_regmap(a2loc, bnd, scm, stitle, soname, cbarname, miss_out)
else:
  a2loc    = mk_front_loc(a2thermo, a2gradthermo, thfmask1, thfmask2)
  a2loc    = ma.masked_where(a2orog > thorog, a2loc).filled(miss_out)
  a2loc    = ma.masked_where(a2gradorogmask > thgradorog, a2loc).filled(miss_out)
  a2loc    = dtanl_fsub.del_front_2grids(a2loc.T, miss_out).T
  a2loc    = ctrack_fsub.find_highsidevalue_saone(a2gradtheta_e.T, a2loc.T, a2gradtv.T, highsidedist, miss_out).T
  mk_regmap(a2loc, bnd, scm, stitle, soname, cbarname, miss_out)
#------



