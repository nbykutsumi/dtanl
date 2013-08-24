from numpy import *
import calendar
import ctrack_para
import ctrack_func
import sys, os
import gsmap_func
import datetime
import front_para
from dtanl_fsub import *
from ctrack_fsub import *
#-----------------------
lyear  = range(1996,2012+1)
#lyear  = [1997] 
lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon   = [4]
iday   = 1
lhour  = [0,6,12,18]
#local region ------
plev     = 850 *100.0   #(Pa)
cbarflag = "True"
sresol   = "anl_p"
#-------------------

miss_out  = -9999.0
ny  = 180
nx  = 360

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
def mk_front_loc_contour(a2thermo, a2gradthermo):
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

  a2loc    = ma.masked_where(a2fmask1 < 0.0, a2loc)
  a2loc    = ma.masked_where(a2fmask2 < 0.0, a2loc)
  a2loc1   = ma.masked_where(a2loc.mask, a2fmask1).filled(miss_out)
  a2loc2   = ma.masked_where(a2loc.mask, a2fmask2).filled(miss_out)
  return a2loc1, a2loc2

##---------------
## front locator :contour: Old
##---------------
#def mk_front_loc_contour(a2thermo, a2gradthermo, thfmask1, thfmask2):
#  a2fmask1 = dtanl_fsub.mk_a2frontmask1(a2thermo.T).T
#  a2fmask2 = dtanl_fsub.mk_a2frontmask2(a2thermo.T).T
#  a2fmask1 = a2fmask1 * (1000.0*100.0)**2.0  #[(100km)-2]
#  a2fmask2 = a2fmask2 * (1000.0*100.0)       #[(100km)-1]
# 
#  (a2grad2x, a2grad2y) = dtanl_fsub.mk_a2grad_saone(a2gradthermo.T)
#  a2grad2x = a2grad2x.T
#  a2grad2y = a2grad2y.T
#  a2loc    = dtanl_fsub.mk_a2axisgrad(a2grad2x.T, a2grad2y.T).T
#  a2loc    = dtanl_fsub.mk_a2contour(a2loc.T, 0.0, 0.0, miss_out).T
#  a2loc    = ma.masked_equal(a2loc, miss_out)  
#  a2loc    = ma.masked_where(a2fmask1 < thfmask1, a2loc)
#  a2loc    = ma.masked_where(a2fmask2 < thfmask2, a2loc)
#  return a2loc

##---------------
## locator
##---------------
#def mk_front_loc(a2thermo, a2gradthermo, thfmask1, thfmask2):
#  a2fmask1 = dtanl_fsub.mk_a2frontmask1(a2thermo.T).T
#  a2fmask2 = dtanl_fsub.mk_a2frontmask2(a2thermo.T).T
#  a2fmask1 = a2fmask1 *(1000.0*100.0)**2.0  #[(100km)-2]
#  a2fmask2 = a2fmask2 *(1000.0*100.0)       #[(100km)-1]
#
#  a2loc    = a2gradthermo  
#  a2loc    = ma.masked_where(a2fmask1 < thfmask1, a2loc)
#  a2loc    = ma.masked_where(a2fmask2 < thfmask2, a2loc)
#  return a2loc

#******************************************************
#-- orog & grad orog ----
orogname     = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
gradorogname = "/media/disk2/data/JRA25/sa.one.125/const/topo/maxgrad.0200km.sa.one"
a2orog     = fromfile(orogname, float32).reshape(ny,nx)
a2gradorog = fromfile(gradorogname, float32).reshape(ny,nx)

#******************************************************
for year in lyear:
  for mon in lmon:
    #-----------
    sodir_t_root    = "/media/disk2/out/JRA25/sa.one.%s/6hr/front.t"%(sresol)
    sodir_t         = sodir_t_root + "/%04d%02d"%(year, mon)

    sodir_q_root    = "/media/disk2/out/JRA25/sa.one.%s/6hr/front.q"%(sresol)
    sodir_q         = sodir_q_root + "/%04d%02d"%(year, mon)

    ctrack_func.mk_dir(sodir_t)
    ctrack_func.mk_dir(sodir_q)
    #-----------
    eday  = calendar.monthrange(year,mon)[1]
    #-----------
    for day in range(iday, eday+1):
      for hour in lhour:
        stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)
        #******************************************************
        #-- q: mixing ratio --------------------------
        qname    = "/media/disk2/data/JRA25/sa.one.%s/6hr/SPFH/%04d%02d/anl_p.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,year, mon, plev*0.01, year, mon, day, hour)
        a2q      = fromfile(qname, float32).reshape(ny,nx)
        a2gradq  = dtanl_fsub.mk_a2grad_abs_saone(a2q.T).T
        a2gradq  = a2gradq *1000.0*100.0   # [kg/kg (100km)-1]
        
        #-- t: ---------------------------------------
        tname    = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP/%04d%02d/anl_p.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,year, mon, plev*0.01, year, mon, day, hour)
        a2t      = fromfile(tname, float32).reshape(ny,nx)
        a2gradt  = dtanl_fsub.mk_a2grad_abs_saone(a2t.T).T
        a2gradt  = a2gradt *1000.0*100.0   # [K (100km)-1]
        
        ##**********************************************
        # front locator: t
        a2thermo             = a2t # K
        a2gradthermo         = a2gradt  # K/100km
        
        sonamet1    = sodir_t + "/front.t.M1.%04d.%02d.%02d.%02d.sa.one"%(year, mon, day, hour)
        sonamet2    = sodir_t + "/front.t.M2.%04d.%02d.%02d.%02d.sa.one"%(year, mon, day, hour)
       
        a2loc1,a2loc2  = mk_front_loc_contour(a2thermo, a2gradthermo)
        #------
        a2loc1.tofile(sonamet1)
        a2loc2.tofile(sonamet2)
        print sonamet1
        print sonamet2
        a2loct1 = a2loc1
        a2loct2 = a2loc2
        #------
        ##**********************************************
        # front locator: q
        a2thermo             = a2q # K
        a2gradthermo         = a2gradq  # K/100km
        sonameq1    = sodir_q + "/front.q.M1.%04d.%02d.%02d.%02d.sa.one"%(year, mon, day, hour)
        sonameq2    = sodir_q + "/front.q.M2.%04d.%02d.%02d.%02d.sa.one"%(year, mon, day, hour)
       
        a2loc1,a2loc2   = mk_front_loc_contour(a2thermo, a2gradthermo)
        #------
        a2loc1.tofile(sonameq1)
        a2loc2.tofile(sonameq2)
        print sonameq1
        print sonameq2
        a2locq1 = a2loc1
        a2locq2 = a2loc2
        #------





