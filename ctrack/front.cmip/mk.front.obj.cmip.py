from numpy import *
import calendar
import ctrack_para, cmip_para
import ctrack_func, cmip_func
import sys, os
import gsmap_func
import datetime
import front_para
from dtanl_fsub import *
from ctrack_fsub import *
#-----------------------
#lmodel=["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel=["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","inmcm4","MPI-ESM-MR","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lexpr = ["historical","rcp85"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}

#------
stepday  = 0.25
#local region ------
plev     = 850 *100.0   #(Pa)
cbarflag = "True"
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
  
#**************************************************
llkey = [[model,expr] for model in lmodel for expr in lexpr]
for model,expr in llkey:
  #-------------------------
  iyear,eyear = dyrange[expr]
  lyear  = range(iyear,eyear+1)
  lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
  ens   = cmip_para.ret_ens(model, expr, "psl")
  sunit, scalendar = cmip_para.ret_unit_calendar(model,expr)
  #******************************************************
  #-- orog & grad orog ----
  orogname     = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog/orog.%s.sa.one"%(model,expr,model)
  gradorogname = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog/maxgrad.0200km.sa.one"%(model,expr)
  
  a2orog     = fromfile(orogname, float32).reshape(ny,nx)
  a2gradorog = fromfile(gradorogname, float32).reshape(ny,nx)
  
  #******************************************************
  # Time Loop
  #*******************************
  a1dtime,a1tnum  = cmip_func.ret_times(iyear,eyear,lmon,sunit,scalendar,stepday,model=model)
  
  for dtime, tnum in map(None, a1dtime, a1tnum):
    year,mon,day,hour = dtime.year, dtime.month, dtime.day, dtime.hour
    #-----------
    sodir_t_root    = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/front.t"%(model,expr)
    sodir_t         = sodir_t_root + "/%04d%02d"%(year, mon)
  
    #sodir_q_root    = "/media/disk2/out/JRA25/sa.one.%s/6hr/front.q"%(sresol)
    #sodir_q         = sodir_q_root + "/%04d%02d"%(year, mon)
  
    ctrack_func.mk_dir(sodir_t)
    #ctrack_func.mk_dir(sodir_q)
    #-----------
    eday  = calendar.monthrange(year,mon)[1]
    #-----------
    stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)
    ##******************************************************
    ##-- q: mixing ratio --------------------------
    #qname    = "/media/disk2/data/JRA25/sa.one.%s/6hr/SPFH/%04d%02d/anl_p.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,year, mon, plev*0.01, year, mon, day, hour)
    #a2q      = fromfile(qname, float32).reshape(ny,nx)
    #a2gradq  = dtanl_fsub.mk_a2grad_abs_saone(a2q.T).T
    #a2gradq  = a2gradq *1000.0*100.0   # [kg/kg (100km)-1]
    
    #-- t: ---------------------------------------
    #tname    = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP/%04d%02d/anl_p.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,year, mon, plev*0.01, year, mon, day, hour)
    tname    = "/media/disk2/data/CMIP5/sa.one.%s.%s/ta/%04d%02d/ta.%04dhPa.%s.%04d%02d%02d%02d00.sa.one"%(model, expr ,year, mon, plev*0.01, ens, year, mon, day, hour)
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
    ###**********************************************
    ## front locator: q
    #a2thermo             = a2q # K
    #a2gradthermo         = a2gradq  # K/100km
    #sonameq1    = sodir_q + "/front.q.M1.%04d.%02d.%02d.%02d.sa.one"%(year, mon, day, hour)
    #sonameq2    = sodir_q + "/front.q.M2.%04d.%02d.%02d.%02d.sa.one"%(year, mon, day, hour)
    
    #a2loc1,a2loc2   = mk_front_loc_contour(a2thermo, a2gradthermo)
    ##------
    #a2loc1.tofile(sonameq1)
    #a2loc2.tofile(sonameq2)
    #print sonameq1
    #print sonameq2
    #a2locq1 = a2loc1
    #a2locq2 = a2loc2
    ##------





