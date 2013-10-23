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
iyear = 2007
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
lhinc    = [6,12,18,24]
thorog       = 1500.0  # (m)
calcflag = True
#calcflag = False
meanflag = True

#----------------------------
a2one    = ones([ny,nx], float32)
a2miss   = ones([ny,nx], float32)*miss
#-- orog --------------------
orogname = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
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
      #----------------
      eday = calendar.monthrange(year, mon)[1]
      #eday = iday
      for day in range(iday, eday+1):
        #---------------------
        if ((year==iyear)&(mon==1)&(day==1)):
          continue
        if ((year==eyear)&(mon==12)&(day==31)):
          continue 
        #---------------------
        print year,mon, day
        #-------------------
        itimes_mon = itimes_mon + 1
        #-------------------
        #*** load precipitation ********
        prdir   = dprdir_root[prtype] + "/%04d"%(year)
        prname  = prdir + "/gpcp_1dd_v1.2_p1d.%04d%02d%02d.bn"%(year, mon, day)  
        a2pr  = flipud(fromfile(prname, float32).reshape(ny,nx))
        a2pr  = ma.masked_equal(a2pr, miss_gpcp).filled(0.0)
        a2pr  = a2pr / (60*60*24.0)  # mm/day->mm/s

        #*** init territory ************
        a2terr_warm  = zeros([ny,nx],float32)
        a2terr_cold  = zeros([ny,nx],float32)
        a2terr_occ   = zeros([ny,nx],float32)
        a2terr_stat  = zeros([ny,nx],float32)

        #******************************* 
        now   = datetime.datetime(year,mon,day,0)
        for hinc in lhinc:
          tagtime = now + datetime.timedelta(hours=hinc)
          year_tag = tagtime.year
          mon_tag  = tagtime.month
          day_tag  = tagtime.day
          hour_tag = tagtime.hour


          #---------------------
          # locator
          #---------------------
          locdir  = locdir_root  + "/%04d%02d"%(year_tag,mon_tag)
          locname    = locdir + "/front.%s.%04d.%02d.%02d.%02d.sa.one"%(region, year_tag, mon_tag, day_tag, hour_tag)

          a2loc      = fromfile(locname, float32).reshape(ny,nx)
          a2loc_warm = ma.masked_not_equal(a2loc, 1).filled(miss)
          a2loc_cold = ma.masked_not_equal(a2loc, 2).filled(miss)
          a2loc_occ  = ma.masked_not_equal(a2loc, 3).filled(miss)
          a2loc_stat = ma.masked_not_equal(a2loc, 4).filled(miss)
  
          #-----------------------------
          # territory
          #-----------------------------
          a2terr_temp_warm = ctrack_fsub.mk_territory_saone( a2loc_warm.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T
          a2terr_temp_cold = ctrack_fsub.mk_territory_saone( a2loc_cold.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T
          a2terr_temp_occ  = ctrack_fsub.mk_territory_saone( a2loc_occ.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T
          a2terr_temp_stat = ctrack_fsub.mk_territory_saone( a2loc_stat.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T
          a2terr_temp_all  = ctrack_fsub.mk_territory_saone( a2loc.T,      thdist*1000.0, miss, -89.5, 1.0 ,1.0).T

          a2terr_warm      = a2terr_warm + ma.masked_equal(a2terr_temp_warm, miss).filled(0.0)
          a2terr_cold      = a2terr_cold + ma.masked_equal(a2terr_temp_cold, miss).filled(0.0)
          a2terr_occ       = a2terr_occ  + ma.masked_equal(a2terr_temp_occ,  miss).filled(0.0)
          a2terr_stat      = a2terr_stat + ma.masked_equal(a2terr_temp_stat, miss).filled(0.0)

        #-----------------------------
        a2terr_warm    = ma.masked_greater(a2terr_warm ,0.0).filled(1.0)
        a2terr_cold    = ma.masked_greater(a2terr_cold ,0.0).filled(1.0)
        a2terr_occ     = ma.masked_greater(a2terr_occ  ,0.0).filled(1.0)
        a2terr_stat    = ma.masked_greater(a2terr_stat ,0.0).filled(1.0)

        a2num_all      = a2terr_warm + a2terr_cold + a2terr_occ + a2terr_stat
        #-----------------------------
        a2pr_warm_temp = ma.masked_where(a2terr_warm ==0.0, a2pr)
        a2pr_cold_temp = ma.masked_where(a2terr_cold ==0.0, a2pr)
        a2pr_occ_temp  = ma.masked_where(a2terr_occ  ==0.0, a2pr)
        a2pr_stat_temp = ma.masked_where(a2terr_stat ==0.0, a2pr)
        a2pr_all_temp  = ma.masked_where(a2num_all   ==0.0, a2pr)

        #-- weighting --------
        a2pr_warm_temp = ma.masked_where(a2num_all==0.0, a2pr_warm_temp)/a2num_all
        a2pr_cold_temp = ma.masked_where(a2num_all==0.0, a2pr_cold_temp)/a2num_all
        a2pr_occ_temp  = ma.masked_where(a2num_all==0.0, a2pr_occ_temp)/a2num_all
        a2pr_stat_temp = ma.masked_where(a2num_all==0.0, a2pr_stat_temp)/a2num_all

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
      print year,mon,ma.masked_equal(a2pr_all,miss).mean(), ma.masked_equal(a2pr_warm,miss).mean()
      #-- ptot name --
      oname_warm  = odir + "/rad%04d.warm.sa.one"%(thdist)
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
  
  
