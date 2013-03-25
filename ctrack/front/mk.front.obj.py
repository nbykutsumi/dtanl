from numpy import *
import calendar
import ctrack_para
import ctrack_func
import sys, os
import gsmap_func
import datetime
from dtanl_fsub import *
from ctrack_fsub import *
#-----------------------

iyear  = 2000
eyear  = 2004
lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon   = [1]
iday   = 1
lhour  = [0,6,12,18]
#local region ------
plev     = 850 *100.0   #(Pa)
cbarflag = "True"
thfmasktheta1 = 0.6
thfmasktheta2 = 2.0

#-----------------------------
miss_out  = -9999.0
ny  = 180
nx  = 360
highsidedist  = ctrack_para.ret_highsidedist()


dlat    = 1.0
dlon    = 1.0

meridians = 10.0
parallels = 10.0

thorog  = ctrack_para.ret_thorog()
thgradorog=ctrack_para.ret_thgradorog()
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
for year in range(iyear, eyear+1):
  for mon in lmon:
    #-----------
    sodir_root    = "/media/disk2/out/JRA25/sa.one/6hr/front"
    sodir         = sodir_root + "/%04d%02d"%(year, mon)
    ctrack_func.mk_dir(sodir)
    #-----------
    eday  = calendar.monthrange(year,mon)[1]
    #-----------
    for day in range(iday, eday+1):
      for hour in lhour:
        stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)
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
        
        #bnd        = [0.0, 0.000005,  0.000007, 0.000009, 0.000011]
        soname     = sodir + "/front.M1_%03.1f.M2_%03.1f.%04d.%02d.%02d.%02d.sa.one"%(thfmask1, thfmask2, year, mon, day, hour)
        
        #******************************************************
        #-- orog & grad orog ----
        orogname   = "/media/disk2/data/JRA25/sa.one/const/topo/topo.sa.one"
        gradorogadjname= "/media/disk2/data/JRA25/sa.one/const/topo/grad.topo.adj.twogrids.sa.one"
        a2orog     = fromfile(orogname, float32).reshape(ny,nx)
        a2gradorogmask = fromfile(gradorogadjname, float32).reshape(ny,nx)
        
        #------
        a2loc    = mk_front_loc_contour(a2thermo, a2gradthermo, thfmask1, thfmask2)
        a2loc    = ma.masked_where(a2orog > thorog, a2loc).filled(miss_out)
        a2loc    = ma.masked_where(a2gradorogmask > thgradorog, a2loc).filled(miss_out)
        a2loc    = dtanl_fsub.del_front_2grids(a2loc.T, miss_out).T
        a2loc    = ctrack_fsub.find_highsidevalue_saone(a2gradtheta_e.T, a2loc.T, a2gradtv.T, highsidedist, miss_out).T
        #------
        a2loc.tofile(soname)
        print soname
        #------



