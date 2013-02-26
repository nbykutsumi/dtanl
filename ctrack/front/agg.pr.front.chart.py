from numpy import *
import calendar
import datetime
from ctrack_fsub import *
import gsmap_func
import ctrack_para
import ctrack_func
import ctrack_fig
import chart_para
import subprocess
#---------------------------------
iyear = 2000
eyear = 2010
lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
iday  = 1
lhour = [0,6,12,18]
region= "ASAS"
ny    = 180
nx    = 360
prtype = "GPCP1DD"
miss   = -9999.0
miss  = -9999.0
miss_gpcp = -99999.
lthdist   = [500]
locdir_root  = "/media/disk2/out/chart/%s/front"%(region)
dprdir_root  = {}
dprdir_root["GPCP1DD"] = "/media/disk2/data/GPCP1DD/v1.2/1dd"
dprdir_root["JRA25"]  = "/media/disk2/data/JRA25/sa.one/6hr/PR"
thorog       = 1500.0  # (m)
calcflag = True
#calcflag = False
meanflag = True

#----------------------------
a2one    = ones([ny,nx], float32)
#-- orog --------------------
orogname = "/media/disk2/data/JRA25/sa.one/const/topo/topo.sa.one"
a2orog   = fromfile(orogname, float32).reshape(ny,nx)
#-- domain ------------------
domname  = "/media/disk2/out/chart/%s/const/domainmask_saone.%s.2000-2006.bn"%(region,region)
a2domain = fromfile(domname , float32).reshape(ny,nx)
#-- shade  ------------------
a2shade  = ma.masked_where( a2domain==0.0, a2one).filled(miss)
a2shade  = ma.masked_where( a2orog > thorog, a2shade).filled(miss)

#----------------------------
odir_root  = "/media/disk2/out/chart/ASAS/front/agg"
#----------------------------
for thdist in lthdist:
  for year in range(iyear, eyear+1):
    #--------------------- 
    if calcflag == False:
      continue
    #--------------------- 
    for mon in lmon:
      itimes_mon = 0
      odir     = odir_root + "/%04d/%02d"%(year,mon)
      ctrack_func.mk_dir
      #-- dummy -------------------
      a2one    = ones([ny,nx], float32)
      a2pr_warm = zeros([ny,nx], float32) 
      a2pr_cold = zeros([ny,nx], float32) 
      a2pr_occ  = zeros([ny,nx], float32) 
      a2pr_stat = zeros([ny,nx], float32) 
      a2pr_all  = zeros([ny,nx], float32) 
      #----------------
      locdir  = locdir_root  + "/%04d%02d"%(year,mon)
      #----------------
      eday = calendar.monthrange(year, mon)[1]
      #eday = iday
      for day in range(iday, eday+1):
        print mon, day
        for hour in lhour:
          #---------------------
          if ((year==iyear)&(mon==1)&(day==1)):
            continue
          if ((year==eyear)&(mon==12)&(day==31)):
            continue 
          #-------------------
          itimes_mon = itimes_mon + 1
          #-------------------
          if prtype in ["GSMaP"]:
             lhour_inc  = [-9,-6,-3,0,3,6,9,12]
          elif prtype in ["JRA25"]:
             lhour_inc  = [-6,0,6,12]
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
              prname  = prdir  + "fcst_phy2m.PR.%04d%02d%02d%02d.sa.one"%(year_target, mon_target, day_target, hour_target)
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
  
          #---------------------
          # locator
          #---------------------
          locname    = locdir + "/front.%s.%04d.%02d.%02d.%02d.saone"%(region, year, mon, day, hour)
          a2loc      = fromfile(locname, float32).reshape(ny,nx)
          a2loc_warm = ma.masked_not_equal(a2loc, 1).filled(miss)
          a2loc_cold = ma.masked_not_equal(a2loc, 2).filled(miss)
          a2loc_occ  = ma.masked_not_equal(a2loc, 3).filled(miss)
          a2loc_stat = ma.masked_not_equal(a2loc, 4).filled(miss)
  
          #-----------------------------
          # territory
          #-----------------------------
          a2terr_warm = ctrack_fsub.mk_territory_saone( a2loc_warm.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T
          a2terr_cold = ctrack_fsub.mk_territory_saone( a2loc_cold.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T
          a2terr_occ  = ctrack_fsub.mk_territory_saone( a2loc_occ.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T
          a2terr_stat = ctrack_fsub.mk_territory_saone( a2loc_stat.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T
          a2terr_all  = ctrack_fsub.mk_territory_saone( a2loc.T,      thdist*1000.0, miss, -89.5, 1.0 ,1.0).T
          #-----------------------------
          a2num_warm =ma.masked_where(a2terr_warm==miss, a2one).filled(0.0)
          a2num_cold =ma.masked_where(a2terr_cold==miss, a2one).filled(0.0)
          a2num_occ  =ma.masked_where(a2terr_occ ==miss, a2one).filled(0.0)
          a2num_stat =ma.masked_where(a2terr_stat==miss, a2one).filled(0.0)
          a2num_all  =a2num_warm + a2num_cold + a2num_occ + a2num_stat 
          #-----------------------------
          a2pr_warm_temp = ma.masked_where(a2terr_warm ==miss, a2pr)
          a2pr_cold_temp = ma.masked_where(a2terr_cold ==miss, a2pr)
          a2pr_occ_temp  = ma.masked_where(a2terr_occ  ==miss, a2pr)
          a2pr_stat_temp = ma.masked_where(a2terr_stat ==miss, a2pr)
          a2pr_all_temp  = ma.masked_where(a2terr_all  ==miss, a2pr)
          #----- weighting -----
          a2pr_warm_temp = a2pr_warm_temp * a2num_warm /a2num_all
          a2pr_cold_temp = a2pr_cold_temp * a2num_cold /a2num_all
          a2pr_occ_temp  = a2pr_occ_temp  * a2num_occ  /a2num_all
          a2pr_stat_temp = a2pr_stat_temp * a2num_stat /a2num_all
          #---------------------
          a2pr_warm_temp = a2pr_warm_temp.filled(0.0)
          a2pr_cold_temp = a2pr_cold_temp.filled(0.0)
          a2pr_occ_temp  = a2pr_occ_temp.filled(0.0)
          a2pr_stat_temp = a2pr_stat_temp.filled(0.0)
          a2pr_all_temp  = a2pr_all_temp.filled(0.0)
          #--- add -------------
          a2pr_warm = a2pr_warm + a2pr_warm_temp 
          a2pr_cold = a2pr_cold + a2pr_cold_temp 
          a2pr_occ  = a2pr_occ  + a2pr_occ_temp 
          a2pr_stat = a2pr_stat + a2pr_stat_temp 
          a2pr_all  = a2pr_all  + a2pr_all_temp
  
      #--- precip rate ---------------------------------
      #-----------------
      if calcflag == False:
        continue
      #-----------------
      a2pr_warm  = a2pr_warm / itimes_mon
      a2pr_cold  = a2pr_cold / itimes_mon
      a2pr_occ   = a2pr_occ  / itimes_mon
      a2pr_stat  = a2pr_stat / itimes_mon
      a2pr_all   = a2pr_all  / itimes_mon
      #-----------------
      a2pr_warm  = ma.masked_where(a2domain==0.0, a2pr_warm).filled(miss)
      a2pr_cold  = ma.masked_where(a2domain==0.0, a2pr_cold).filled(miss)
      a2pr_occ   = ma.masked_where(a2domain==0.0, a2pr_occ ).filled(miss)
      a2pr_stat  = ma.masked_where(a2domain==0.0, a2pr_stat).filled(miss)
      a2pr_all   = ma.masked_where(a2domain==0.0, a2pr_all ).filled(miss)
      #-------------
      a2pr_warm  = ma.masked_where(a2orog>thorog, a2pr_warm).filled(miss)
      a2pr_cold  = ma.masked_where(a2orog>thorog, a2pr_cold).filled(miss)
      a2pr_occ   = ma.masked_where(a2orog>thorog, a2pr_occ).filled(miss)
      a2pr_stat  = ma.masked_where(a2orog>thorog, a2pr_stat).filled(miss)
      a2pr_all   = ma.masked_where(a2orog>thorog, a2pr_all).filled(miss)
      #-- ptot name --
      oname_warm  = odir + "/rad%04d.warm.saone"%(thdist)
      oname_cold  = odir + "/rad%04d.cold.saone"%(thdist)
      oname_occ   = odir + "/rad%04d.occ.saone"%(thdist)
      oname_stat  = odir + "/rad%04d.stat.saone"%(thdist)
      oname_all   = odir + "/rad%04d.all.saone"%(thdist)
      #--------------
      a2pr_warm.tofile(oname_warm)
      a2pr_cold.tofile(oname_cold)
      a2pr_occ.tofile(oname_occ)
      a2pr_stat.tofile(oname_stat)
      a2pr_all.tofile(oname_all)
  
  
