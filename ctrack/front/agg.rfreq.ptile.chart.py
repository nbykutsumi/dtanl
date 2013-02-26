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
#lhour = [0]
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
percent      = 0.0  # (%)

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
#-- ptile  ------------------
if percent >0.0:
  if prtype == "GPCP1DD":
    ptiledir = "/media/disk2/data/GPCP1DD/v1.2/1dd/ptile/%04d-%04d"%(iyear, eyear)
    ptilename= ptiledir + "/pr.gpcp.p%05.2f.ALL.bn"%(percent)
    a2ptile  = fromfile(ptilename, float32).reshape(ny,nx)
    a2ptile  = flipud(a2ptile)
    a2ptile  = a2ptile / (60.0*60.0*24.0)   # mm/day --> mm/s
elif percent == 0.0:
  a2ptile = zeros([ny,nx],float32)
#----------------------------
#----------------------------
for year in range(iyear, eyear+1):
  #--------------------- 
  if calcflag == False:
    continue
  #--------------------- 
  for mon in lmon:

    #-- dummy -------------------
    da2num_warm = {}
    da2num_cold = {}
    da2num_occ  = {}
    da2num_stat = {}
    da2num_all  = {}
    for thdist in lthdist:
      da2num_warm[thdist] = zeros([ny,nx], float32) 
      da2num_cold[thdist] = zeros([ny,nx], float32) 
      da2num_occ[thdist]  = zeros([ny,nx], float32) 
      da2num_stat[thdist] = zeros([ny,nx], float32) 
      da2num_all[thdist]  = zeros([ny,nx], float32) 
    #---
    a2num_plain = zeros([ny,nx], float32) 
    #----------------------------
    odir_root  = "/media/disk2/out/chart/%s/front/agg/%04d/%02d"%(region, year, mon)
    #-- out dir -----------------
    rfreqdir     = odir_root + "/rfreq"
    ctrack_func.mk_dir(rfreqdir)
    
    figdir      = rfreqdir

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
        for thdist in lthdist:
          a2terr_warm = ctrack_fsub.mk_territory_saone( a2loc_warm.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T
          a2terr_cold = ctrack_fsub.mk_territory_saone( a2loc_cold.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T
          a2terr_occ  = ctrack_fsub.mk_territory_saone( a2loc_occ.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T
          a2terr_stat = ctrack_fsub.mk_territory_saone( a2loc_stat.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T
          a2terr_all  = ctrack_fsub.mk_territory_saone( a2loc.T,      thdist*1000.0, miss, -89.5, 1.0 ,1.0).T
          #-----------------------------
          a2exist_warm =ma.masked_where(a2terr_warm==miss, a2one).filled(0.0)
          a2exist_cold =ma.masked_where(a2terr_cold==miss, a2one).filled(0.0)
          a2exist_occ  =ma.masked_where(a2terr_occ ==miss, a2one).filled(0.0)
          a2exist_stat =ma.masked_where(a2terr_stat==miss, a2one).filled(0.0)
          a2exist_all  =a2exist_warm + a2exist_cold + a2exist_occ + a2exist_stat 
          #-----------------------------
          a2pr_warm_temp = ma.masked_where(a2terr_warm ==miss, a2pr)
          a2pr_cold_temp = ma.masked_where(a2terr_cold ==miss, a2pr)
          a2pr_occ_temp  = ma.masked_where(a2terr_occ  ==miss, a2pr)
          a2pr_stat_temp = ma.masked_where(a2terr_stat ==miss, a2pr)
          a2pr_all_temp  = ma.masked_where(a2terr_all  ==miss, a2pr)
          #-----------------------------
          a2num_warm_temp= ma.masked_where(a2pr_warm_temp <= a2ptile, a2one)
          a2num_cold_temp= ma.masked_where(a2pr_cold_temp <= a2ptile, a2one)
          a2num_occ_temp = ma.masked_where(a2pr_occ_temp  <= a2ptile, a2one)
          a2num_stat_temp= ma.masked_where(a2pr_stat_temp <= a2ptile, a2one)
          a2num_all_temp = ma.masked_where(a2pr_all_temp  <= a2ptile, a2one)
          a2num_plain_temp=ma.masked_where(a2pr           <= a2ptile, a2one)
          #----- weight ----------------
          a2num_warm_temp= a2num_warm_temp * a2exist_warm / a2exist_all
          a2num_cold_temp= a2num_cold_temp * a2exist_cold / a2exist_all
          a2num_occ_temp = a2num_occ_temp  * a2exist_occ  / a2exist_all
          a2num_stat_temp= a2num_stat_temp * a2exist_stat / a2exist_all
          #-----------------------------
          a2num_warm_temp = a2num_warm_temp.filled(0.0)
          a2num_cold_temp = a2num_cold_temp.filled(0.0)
          a2num_occ_temp  = a2num_occ_temp.filled(0.0)
          a2num_stat_temp = a2num_stat_temp.filled(0.0)
          a2num_all_temp  = a2num_all_temp.filled(0.0)
          a2num_plain_temp= a2num_plain_temp.filled(0.0)
          #--- add -------------
          da2num_warm[thdist] = da2num_warm[thdist] + a2num_warm_temp 
          da2num_cold[thdist] = da2num_cold[thdist] + a2num_cold_temp 
          da2num_occ[thdist]  = da2num_occ[thdist]  + a2num_occ_temp 
          da2num_stat[thdist] = da2num_stat[thdist] + a2num_stat_temp 
          da2num_all[thdist]  = da2num_all[thdist]  + a2num_all_temp
          a2num_plain         = a2num_plain         + a2num_plain_temp
    #-- num --
    for thdist in lthdist:
      soname_num_warm = rfreqdir + "/num.rad%04d.p%05.2f.warm.saone"%(thdist,percent)
      soname_num_cold = rfreqdir + "/num.rad%04d.p%05.2f.cold.saone"%(thdist,percent)
      soname_num_occ  = rfreqdir + "/num.rad%04d.p%05.2f.occ.saone"%(thdist,percent)
      soname_num_stat = rfreqdir + "/num.rad%04d.p%05.2f.stat.saone"%(thdist,percent)
      soname_num_all  = rfreqdir + "/num.rad%04d.p%05.2f.all.saone"%(thdist,percent)
      soname_num_plain= rfreqdir + "/num.p%05.2f.saone"%(percent)
      #
      da2num_warm[thdist].tofile(soname_num_warm) 
      da2num_cold[thdist].tofile(soname_num_cold) 
      da2num_occ[thdist ].tofile(soname_num_occ ) 
      da2num_stat[thdist].tofile(soname_num_stat) 
      da2num_all[thdist ].tofile(soname_num_all ) 
      a2num_plain.tofile(soname_num_plain) 
      print soname_num_all
