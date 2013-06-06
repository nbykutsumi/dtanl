from numpy import *
import sys
import calendar
import datetime
from ctrack_fsub import *
from dtanl_fsub import *
import gsmap_func
import ctrack_para
import ctrack_func
import ctrack_fig
import chart_para
import subprocess
#---------------------------------
#singleday= True
singleday= False
calcflag = True
#calcflag = False

iyear = 2000
eyear = 2004
lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon  = [1]
iday  = 1
#lhour = [12]
lhour = [0,6,12,18]
region= "ASAS"
ny    = 180
nx    = 360
prtype = "GPCP1DD"
#prtype = "JRA25"
miss   = -9999.0
miss  = -9999.0
miss_gpcp = -99999.
#lthdist   = [250,500,1000,1500]
distwarmside = 300.0*1000.0 #[m]
thdist   = 500  # (km)
#
sresol   = "anl_p"
dprdir_root  = {}
dprdir_root["GPCP1DD"] = "/media/disk2/data/GPCP1DD/v1.2/1dd"
dprdir_root["JRA25"]  = "/media/disk2/data/JRA25/sa.one.%s/6hr/PR"%(sresol)
#-- para for objective locator -------------
plev     = 850*100.0 # (Pa)
#llthfmask = [(0.4,2.0)]
#llthfmask = [(0.5,2.0)]
#llthfmask = [(0.6,2.0)]
llthfmask = [(0.7,4.0)]

thorog  = ctrack_para.ret_thorog()
thgradorog=ctrack_para.ret_thgradorog()

#-- para for baroclinic --------------------
#thbc     = 0.7 /1000.0/100.0  # (K/m)
thbc     = 0.9 /1000.0/100.0  # (K/m)

#-------------------------------------------
a2one    = ones([ny,nx],float32)
#----------------------------
#-- orog --------------------
orogname = "/media/disk2/data/JRA25/sa.one/const/topo/topo.sa.one"
a2orog   = fromfile(orogname, float32).reshape(ny,nx)
gradorogadjname= "/media/disk2/data/JRA25/sa.one/const/topo/grad.topo.adj.twogrids.sa.one"
a2gradorogmask = fromfile(gradorogadjname, float32).reshape(ny,nx)


#***************************************
# function
#-----------------
# locatlor
#-----------------
def mk_loc_base(a2t, a2q, miss):
  #-- theta_e -----------------------------------
  a2thermo = dtanl_fsub.mk_a2theta_e(plev, a2t.T, a2q.T).T
  #-- grad.theta_e ------------------------------------
  a2gradthermo    = dtanl_fsub.mk_a2grad_abs_saone(a2thermo.T).T
  a2gradthermo    = a2gradthermo * 1000.0*100.0 # [K (100km)-1]
  #-------------
  a2fmask1 = dtanl_fsub.mk_a2frontmask1(a2thermo.T).T
  a2fmask2 = dtanl_fsub.mk_a2frontmask2(a2thermo.T).T
  a2fmask1 = a2fmask1 *(1000.0*100.0)**2.0  #[(100km)-2]
  a2fmask2 = a2fmask2 *(1000.0*100.0)       #[(100km)-1]
  #-------------
  (a2grad2x, a2grad2y) = dtanl_fsub.mk_a2grad_saone(a2gradthermo.T)
  a2grad2x = a2grad2x.T
  a2grad2y = a2grad2y.T
  a2loc_base    = dtanl_fsub.mk_a2axisgrad(a2grad2x.T, a2grad2y.T).T
  a2loc_base    = dtanl_fsub.mk_a2contour(a2loc_base.T, 0.0, 0.0, miss).T
  #-----------------------------------
  return   a2loc_base, a2fmask1, a2fmask2
#******************************************

#***************************************
def locbase2locfront(a2loc_base, a2fmask1, a2fmask2, thfmask1, thfmask2):
  #-------------
  a2loc    = a2loc_base
  a2loc    = ma.masked_where(a2fmask1 < thfmask1, a2loc)
  a2loc    = ma.masked_where(a2fmask2 < thfmask2, a2loc)

  a2loc    = ma.masked_where(a2orog > thorog, a2loc)
  a2loc    = ma.masked_where(a2gradorogmask > thgradorog, a2loc)
  a2loc    = a2loc.filled(miss)
  #a2loc    = dtanl_fsub.del_front_2grids(a2loc.T, miss).T
  a2loc    = dtanl_fsub.del_front_3grids(a2loc.T, miss).T
  return   a2loc

#***************************************
#******************************
#-- out dir -----------------
odir_root  = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/front/agg"

#----------------------------

for lthfmask in llthfmask:
  thfmask1, thfmask2 = lthfmask
  for year in range(iyear, eyear+1):
    #--------------------- 
    if calcflag == False:
      continue
    #--------------------- 
    for mon in lmon:
      itimes_mon  = 0
      #************************
      #-- init for front ------
      a2pr_front_mon           = zeros([ny,nx],float32)
      a2pr_bcf_mon             = zeros([ny,nx],float32)
      a2pr_nobc_mon            = zeros([ny,nx],float32)
      a2count_front_mon        = zeros([ny,nx],float32)
      a2count_bcf_front_mon    = zeros([ny,nx],float32)
      #************************
      #-- init for olap ------
      a2pr_olap_mon            = zeros([ny,nx],float32)
      a2count_olap_mon         = zeros([ny,nx],float32)
  
      #----------------
      eday = calendar.monthrange(year, mon)[1]
      if singleday==True:
        eday = iday
      #----------------
      for day in range(iday, eday+1):
        #---------------------
        if ((year==iyear)&(mon==1)&(day==1)):
          continue
        if ((year==eyear)&(mon==12)&(day==31)):
          continue 
        #---------------------
        if singleday == True:
          if (day !=iday):
            continue
        #---------------------
        print year, mon, day, "single=",singleday
        #---------------------
        for hour in lhour:
          #-------------------
          itimes_mon = itimes_mon + 1
          #-------------------
          if prtype in ["GSMaP"]:
             lhour_inc  = [-9,-6,-3,0,3,6,9,12]
          elif prtype in ["JRA25"]:
             #lhour_inc  = [-6,0,6,12]
             lhour_inc  = [0,6]
          elif prtype in ["GPCP1DD"]:
             lhour_inc  = [0]
          elif prtype in ["APHRO_MA"]:
             lhour_inc  = [0]
          #-------------------
          now   = datetime.datetime(year, mon, day, hour)
          a2pr  = zeros([ny, nx], float32)
          #-------------------
          for hour_inc in lhour_inc:
            dhour       = datetime.timedelta(hours = hour_inc)
            target      = now + dhour
            year_target = target.year
            mon_target  = target.month
            day_target  = target.day
            hour_target = target.hour
            didir       = {}
            diname      = {} 
            #-----------------------------
            if prtype in ["JRA25"]:
              prdir   = dprdir_root[prtype] + "/%04d%02d"%(year_target, mon_target)
              prname  = prdir  + "/fcst_phy2m.PR.%04d%02d%02d%02d.sa.one"%(year_target, mon_target, day_target, hour_target)
              a2pr_temp  = fromfile(prname, float32).reshape(ny,nx)
              a2pr_temp  = a2pr_temp   # mm/s
  
            elif prtype in ["GPCP1DD"]:
              prdir   = dprdir_root[prtype] + "/%04d"%(year_target)
              prname  = prdir + "/gpcp_1dd_v1.2_p1d.%04d%02d%02d.bn"%(year_target, mon_target, day_target)  
              a2pr_temp  = flipud(fromfile(prname, float32).reshape(ny,nx))
              a2pr_temp  = ma.masked_equal(a2pr_temp, miss_gpcp).filled(0.0)
              a2pr_temp  = a2pr_temp / (60*60*24.0)  # mm/day->mm/s
  
            elif prtype in ["GSMaP"]:
              prdir   = dprdir_root[prtype] + "/%04d%02d"%(year_target, mon_target)
              prname  = prdir + "/gsmap_mvk.3rh.%04d%02d%02d.%02d00.v5.222.1.sa.one"%(year_target, mon_target, day_target, hour_target)          
              a2pr_temp  = fromfile(prname, float32).reshape(120,360)
              a2pr_temp  = gsmap_func.gsmap2globl_one(a2pr_temp, miss)
              a2pr_temp  = ma.masked_equal(a2pr_temp, miss) # mm/s
            #----------------------------
            a2pr  = a2pr + a2pr_temp
          #-----------------------------
          a2pr  = a2pr / len(lhour_inc)
          if type(a2pr) == ma.core.MaskedArray:
            a2pr = a2pr.filled(miss)
  
          #*********************************************
          # for objective front locator
          #----------------------------- 
          #-- q: mixing ratio --------------------------
          qname = "/media/disk2/data/JRA25/sa.one.%s/6hr/SPFH/%04d%02d/%s.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,year, mon, plev*0.01, sresol, year, mon, day, hour)
          a2q   = fromfile(qname, float32).reshape(ny,nx)
          #-- t: mixing ratio --------------------------
          tname = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP/%04d%02d/%s.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,year, mon, plev*0.01, sresol,year, mon, day, hour)
          a2t   = fromfile(tname, float32).reshape(ny,nx)  
  
          #-- virtual temperature ----------------------
          a2tv  = a2t * (1.0 + 0.61*a2q)
          a2gradtv = dtanl_fsub.mk_a2grad_abs_saone(a2tv.T).T
  
          #-- thermo: theta_e --------------------------
          a2thermo = dtanl_fsub.mk_a2theta_e(plev, a2t.T, a2q.T).T  
          a2gradthermo = dtanl_fsub.mk_a2grad_abs_saone(a2thermo.T).T
  
          #******************************
          # loc_base
          #------------------------------
          a2loc_base, a2fmask1, a2fmask2 = mk_loc_base(a2t, a2q, miss)
  
          #-----------------------------
          # objective front territory
          #-----------------------------
          #---------------------------------------------
          a2loc_front    =  locbase2locfront(a2loc_base, a2fmask1, a2fmask2, thfmask1, thfmask2)
  
          a2loc_front    =  ctrack_fsub.find_highsidevalue_saone(a2gradthermo.T, a2loc_front.T, a2gradtv.T, distwarmside, miss).T
  
          #-- count front loc  --
          a2count_front_mon     = a2count_front_mon + ma.masked_where(a2loc_front == miss,a2one).filled(0.0)
          a2terr_front = ctrack_fsub.mk_territory_saone( a2loc_front.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T
  
          #-- count baloclinic front loc --
          a2temp         = ma.masked_where(a2loc_front ==-9999.0, a2one)
          a2temp         = ma.masked_where(a2loc_front < thbc,   a2temp)
          a2count_bcf_front_mon = a2count_bcf_front_mon + a2temp.filled(0.0)

          a2loc_temp     = ma.masked_less(a2loc_front, thbc).filled(miss)
          a2terr_bcf     = ctrack_fsub.mk_territory_saone( a2loc_temp.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T
  
          #-- count non-baloclinic front loc --
          a2temp         = ma.masked_where(a2loc_front ==-9999.0, a2one)
          a2temp         = ma.masked_where(a2loc_front >= thbc,   a2temp)
          a2count_nobc_front_mon= a2count_nobc_front_mon + a2temp.filled(0.0)

          a2loc_temp     = ma.masked_greater_equal(a2loc_front, thbc).filled(miss)
          a2terr_nobc    = ctrack_fsub.mk_territory_saone( a2loc_temp.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T

         
          #***********************************************
          # aggregate precip : front
          #-----------------------------------
          a2pr_front_temp  = ma.masked_where(a2terr_front ==miss, a2pr)
          #---------------------
          a2pr_front_temp  = a2pr_front_temp.filled(0.0)
          #--- add -------------
          a2pr_front_mon   = a2pr_front_mon + a2pr_front_temp
          #************************************************
          # aggregate precip : overlap
          #-------------------------
          a2pr_olap_temp = ma.masked_where(a2terr_front ==miss, a2pr)
          #a2pr_olap_temp = ma.masked_where(a2terr_baiu  ==miss, a2pr_olap_temp)
          a2pr_olap_temp = a2pr_olap_temp.filled(0.0)
          #--- add -----------
          a2pr_olap_mon  = a2pr_olap_mon + a2pr_olap_temp
          #************************************************
          # aggregate precip : baroclinic front
          #-------------------------
          a2pr_bcf_temp = ma.masked_where(a2terr_bcf ==miss, a2pr)
          a2pr_bcf_temp = a2pr_bcf_temp.filled(0.0)
          #--- add -----------
          a2pr_bcf_mon  = a2pr_bcf_mon + a2pr_bcf_temp
  
          #************************************************
          # aggregate precip : non-baroclinic front
          #-------------------------
          a2pr_nobc_temp = ma.masked_where(a2terr_nobc ==miss, a2pr)
          a2pr_nobc_temp = a2pr_nobc_temp.filled(0.0)
          #--- add -----------
          a2pr_nobc_mon  = a2pr_nobc_mon + a2pr_nobc_temp
  
      #********************************
      #-- for monthly data front ------
      dir_ptot_mon   = "/media/disk2/out/JRA25/sa.one.%s/6hr/tenkizu/front/agg/%04d/%02d"%(sresol,year,mon)
      ctrack_func.mk_dir(dir_ptot_mon)
      #--
      #-- count : front -
      name_count_front_mon = dir_ptot_mon + "/count.front.M1_%s_M2_%s.saone"%(thfmask1, thfmask2)
      a2count_front_mon = ma.masked_where(a2orog>thorog, a2count_front_mon).filled(miss)
      a2count_front_mon = ma.masked_where(a2gradorogmask>thgradorog, a2count_front_mon).filled(miss)
      a2count_front_mon.tofile(name_count_front_mon)
  
      #-- count : baroclinic front -
      name_temp = dir_ptot_mon + "/count.bcf.front.M1_%s_M2_%s.thbc_%04.2f.saone"%(thfmask1, thfmask2, thbc*1000*100)
      a2temp    = a2count_bcf_front_mon
      a2temp    = ma.masked_where(a2orog>thorog, a2temp).filled(miss)
      a2temp    = ma.masked_where(a2gradorogmask>thgradorog, a2temp).filled(miss)
      a2temp.tofile(name_temp)
  
      #-- count : non-baroclinic front -
      name_temp = dir_ptot_mon + "/count.nobc.front.M1_%s_M2_%s.thbc_%04.2f.saone"%(thfmask1, thfmask2, thbc*1000*100 )
      a2temp    = a2count_nobc_front_mon
      a2temp    = ma.masked_where(a2orog>thorog, a2temp).filled(miss)
      a2temp    = ma.masked_where(a2gradorogmask>thgradorog, a2temp).filled(miss)
      a2temp.tofile(name_temp)
  
      #-- count : only-baiu --
      name_temp = dir_ptot_mon + "/count.only.baiu.saone"
      a2temp    = a2count_onbaiu_mon
      a2temp    = ma.masked_where(a2orog>thorog, a2temp).filled(miss)
      a2temp    = ma.masked_where(a2gradorogmask > thgradorog, a2temp).filled(miss)
      a2temp.tofile(name_temp)
  
      #-- count : non-baroclinic only-baiu --
      name_temp = dir_ptot_mon + "/count.nobc.only.baiu.saone"
      a2temp    = a2count_nobc_onbaiu_mon
      a2temp    = ma.masked_where(a2orog>thorog, a2temp).filled(miss)
      a2temp    = ma.masked_where(a2gradorogmask > thgradorog, a2temp).filled(miss)
      a2temp.tofile(name_temp)
  
      #--- precip rate: front ----------------------
      a2pr_front_mon  = a2pr_front_mon / itimes_mon  #[mm/s]
      a2pr_front_mon  = ma.masked_where(a2orog>thorog, a2pr_front_mon).filled(miss)
      a2pr_front_mon  = ma.masked_where(a2gradorogmask > thgradorog, a2pr_front_mon).filled(miss)
      name_ptot_front_mon  = dir_ptot_mon + "/pr.front.rad%04d.M1_%s_M2_%s.saone"%(thdist,thfmask1, thfmask2)
      a2pr_front_mon.tofile(name_ptot_front_mon) 
      print name_ptot_front_mon
  
      #--- precip rate: baroclinic front ----------------------
      a2pr_bcf_mon    = a2pr_bcf_mon / itimes_mon  #[mm/s]
      a2pr_bcf_mon    = ma.masked_where(a2orog>thorog, a2pr_bcf_mon).filled(miss)
      a2pr_bcf_mon    = ma.masked_where(a2gradorogmask > thgradorog, a2pr_bcf_mon).filled(miss)
      tempname              = dir_ptot_mon + "/pr.bcf.rad%04d.M1_%s_M2_%s.thbc_%04.2f.saone"%(thdist,thfmask1, thfmask2, thbc*1000*100)
      a2pr_bcf_mon.tofile(tempname) 
      print tempname
  
      #--- precip rate: non-baroclinic front ----------------------
      a2pr_nobc_mon   = a2pr_nobc_mon / itimes_mon  #[mm/s]
      a2pr_nobc_mon   = ma.masked_where(a2orog>thorog, a2pr_nobc_mon).filled(miss)
      a2pr_nobc_mon   = ma.masked_where(a2gradorogmask > thgradorog, a2pr_nobc_mon).filled(miss)
      tempname              = dir_ptot_mon + "/pr.nobc.rad%04d.M1_%s_M2_%s.thbc_%04.2f.saone"%(thdist,thfmask1, thfmask2, thbc*1000*100)
      a2pr_nobc_mon.tofile(tempname) 
      print tempname
  
      #********************************
      #-- for monthly data baiu ------
      #-- count : baiu --
      name_count_baiu_mon = dir_ptot_mon + "/count.baiu.saone"
      a2count_baiu_mon    = ma.masked_where(a2orog>thorog, a2count_baiu_mon).filled(miss)
      da2count_baiu_mon   = ma.masked_where(a2gradorogmask > thgradorog, a2count_baiu_mon).filled(miss)
      a2count_baiu_mon.tofile(name_count_baiu_mon)
  
      #-- precip --------
      a2pr_baiu_mon       = a2pr_baiu_mon / itimes_mon
      a2pr_baiu_mon       = ma.masked_where(a2orog>thorog, a2pr_baiu_mon).filled(miss)
      a2pr_baiu_mon       = ma.masked_where(a2gradorogmask>thgradorog, a2pr_baiu_mon).filled(miss)
      name_ptot_baiu_mon  = dir_ptot_mon + "/pr.baiu.rad%04d.saone"%(thdist)
      a2pr_baiu_mon.tofile(name_ptot_baiu_mon) 
      #------------------- 
      #********************************
      #-- for monthly data olap ------
      a2pr_olap_mon   = a2pr_olap_mon / itimes_mon  #[mm/s]
      a2pr_olap_mon   = ma.masked_where(a2orog>thorog, a2pr_olap_mon).filled(miss)
      a2pr_olap_mon   = ma.masked_where(a2gradorogmask > thgradorog, a2pr_olap_mon).filled(miss)
      name_ptot_olap_mon  = dir_ptot_mon + "/pr.olap.rad%04d.M1_%s_M2_%s.saone"%(thdist,thfmask1, thfmask2)
      a2pr_olap_mon.tofile(name_ptot_olap_mon) 
  
