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
eyear = 2005
#lseason=["JJA"]
#lseason=["ALL","JJA","DJF"]
lseason = [1,2,3,4,5,6,7,8,9,10,11]
iday  = 1
lhour = [12]
region= "ASAS"
ny    = 180
nx    = 360
prtype = "GPCP1DD"
miss   = -9999.0
miss  = -9999.0
miss_gpcp = -99999.
lthdist   = [250,500,1000,1500]
locdir_root  = "/media/disk2/out/chart/%s/front"%(region)
dprdir_root  = {}
dprdir_root["GPCP1DD"] = "/media/disk2/data/GPCP1DD/v1.2/1dd"
dprdir_root["JRA25"]  = "/media/disk2/data/JRA25/sa.one/6hr/PR"

#calcflag = True
calcflag = False
meanflag = True
#-- orog --------------------
orogname = "/media/disk2/data/JRA25/sa.one/const/topo/topo.sa.one"
domname  = "/media/disk2/out/chart/%s/const/domainmask_saone.%s.2000.01.bn"%(region,region)
a2orog   = fromfile(orogname, float32).reshape(ny,nx)
a2domain = fromfile(domname , float32).reshape(ny,nx)
#-- dummy -------------------
a2one    = ones([ny,nx], float32)
da2pr_warm = {}
da2pr_cold = {}
da2pr_occ  = {}
da2pr_stat = {}
da2pr_all  = {}
for thdist in lthdist:
  da2pr_warm[thdist] = zeros([ny,nx], float32) 
  da2pr_cold[thdist] = zeros([ny,nx], float32) 
  da2pr_occ[thdist]  = zeros([ny,nx], float32) 
  da2pr_stat[thdist] = zeros([ny,nx], float32) 
  da2pr_all[thdist]  = zeros([ny,nx], float32) 

#----------------------------
for season in lseason:
  #-- out dir -----------------
  odir_root  = "/media/disk2/out/chart/%s/front/agg/%04d-%04d/%s"%(region, iyear, eyear, season)

  ptotdir     = odir_root + "/ptot"
  ctrack_func.mk_dir(ptotdir)

  figdir      = ptotdir
  #----------------------------
  itimes  = 0
  for year in range(iyear, eyear+1):
    #--------------------- 
    if calcflag == False:
      continue
    #--------------------- 
    lmon  = ctrack_para.ret_lmon(season)
    for mon in lmon:
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
          itimes = itimes + 1
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
            da2pr_warm[thdist] = da2pr_warm[thdist] + a2pr_warm_temp 
            da2pr_cold[thdist] = da2pr_cold[thdist] + a2pr_cold_temp 
            da2pr_occ[thdist]  = da2pr_occ[thdist]  + a2pr_occ_temp 
            da2pr_stat[thdist] = da2pr_stat[thdist] + a2pr_stat_temp 
            da2pr_all[thdist]  = da2pr_all[thdist]  + a2pr_all_temp
          #----------------------- 
  
  #---------------------------------------------------------
  for thdist in lthdist:
    #-----------------
    if calcflag == False:
      continue
    #-----------------
    da2pr_warm[thdist]  = da2pr_warm[thdist] / itimes
    da2pr_cold[thdist]  = da2pr_cold[thdist] / itimes
    da2pr_occ[thdist]   = da2pr_occ[thdist]  / itimes
    da2pr_stat[thdist]  = da2pr_stat[thdist] / itimes
    da2pr_all[thdist]   = da2pr_all[thdist]  / itimes
    #-----------------
    da2pr_warm[thdist]  = ma.masked_where(a2domain==0.0, da2pr_warm[thdist]).filled(miss)
    da2pr_cold[thdist]  = ma.masked_where(a2domain==0.0, da2pr_cold[thdist]).filled(miss)
    da2pr_occ[thdist]   = ma.masked_where(a2domain==0.0, da2pr_occ[thdist]).filled(miss)
    da2pr_stat[thdist]  = ma.masked_where(a2domain==0.0, da2pr_stat[thdist]).filled(miss)
    da2pr_all[thdist]   = ma.masked_where(a2domain==0.0, da2pr_all[thdist]).filled(miss)
    #-------------
    da2pr_warm[thdist]  = ma.masked_where(a2orog>1500.0, da2pr_warm[thdist]).filled(miss)
    da2pr_cold[thdist]  = ma.masked_where(a2orog>1500.0, da2pr_cold[thdist]).filled(miss)
    da2pr_occ[thdist]   = ma.masked_where(a2orog>1500.0, da2pr_occ[thdist]).filled(miss)
    da2pr_stat[thdist]  = ma.masked_where(a2orog>1500.0, da2pr_stat[thdist]).filled(miss)
    da2pr_all[thdist]   = ma.masked_where(a2orog>1500.0, da2pr_all[thdist]).filled(miss)
    #-- ptot name --
    oname_warm  = ptotdir + "/rad%04d.warm.saone"%(thdist)
    oname_cold  = ptotdir + "/rad%04d.cold.saone"%(thdist)
    oname_occ   = ptotdir + "/rad%04d.occ.saone"%(thdist)
    oname_stat  = ptotdir + "/rad%04d.stat.saone"%(thdist)
    oname_all   = ptotdir + "/rad%04d.all.saone"%(thdist)
    #--------------
    da2pr_warm[thdist].tofile(oname_warm)
    da2pr_cold[thdist].tofile(oname_cold)
    da2pr_occ[thdist].tofile(oname_occ)
    da2pr_stat[thdist].tofile(oname_stat)
    da2pr_all[thdist].tofile(oname_all)

  #**********************************************
  # annual mean precipitation
  if prtype in ["GPCP1DD"]:
    if meanflag ==True:
      sprog = "/home/utsumi/bin/dtanl/mk.mean.GPCP1DD.py" 
      scmd  = "python %s %s %s %s"%(sprog, iyear, eyear, season) 
      print scmd
      subprocess.call(scmd, shell=True)
    #--
    ptotplainname = "/media/disk2/data/GPCP1DD/v1.2/1dd/mean/gpcp_1dd_v1.2_p1d.%04d-%04d.%s.bn"%(iyear, eyear, season)
    a2ptotplain   = flipud(fromfile(ptotplainname, float32).reshape(ny,nx))
    a2ptotplain   = a2ptotplain / (60*60*24.0)  # mm/s
  #**********************************************
  # fraction
  #----------------------------------------------
  for thdist in lthdist:
    #-- ptot name --
    ptotname_warm  = ptotdir + "/rad%04d.warm.saone"%(thdist)
    ptotname_cold  = ptotdir + "/rad%04d.cold.saone"%(thdist)
    ptotname_occ   = ptotdir + "/rad%04d.occ.saone"%(thdist)
    ptotname_stat  = ptotdir + "/rad%04d.stat.saone"%(thdist)
    ptotname_all   = ptotdir + "/rad%04d.all.saone"%(thdist)

    #-- fig: frac name ---
    figdir         = ptotdir + "/pict"
    ctrack_func.mk_dir(figdir)
    fracname_warm   = figdir + "/frac.rad%04d.warm.png"%(thdist)
    fracname_cold   = figdir + "/frac.rad%04d.cold.png"%(thdist)
    fracname_occ    = figdir + "/frac.rad%04d.occ.png"%(thdist)
    fracname_stat   = figdir + "/frac.rad%04d.stat.png"%(thdist)
    fracname_all    = figdir + "/frac.rad%04d.all.png"%(thdist)
    #-- fig: load ptot ---
    a2ptot_warm     = fromfile(ptotname_warm, float32).reshape(ny,nx)
    a2ptot_cold     = fromfile(ptotname_cold, float32).reshape(ny,nx)
    a2ptot_occ      = fromfile(ptotname_occ, float32).reshape(ny,nx)
    a2ptot_stat     = fromfile(ptotname_stat, float32).reshape(ny,nx)
    a2ptot_all      = fromfile(ptotname_all, float32).reshape(ny,nx)
    #-- fig: mask 1st -
    a2ptot_warm     = ma.masked_equal(a2ptot_warm, miss) 
    a2ptot_cold     = ma.masked_equal(a2ptot_cold, miss) 
    a2ptot_occ      = ma.masked_equal(a2ptot_occ, miss) 
    a2ptot_stat     = ma.masked_equal(a2ptot_stat, miss) 
    a2ptot_all      = ma.masked_equal(a2ptot_all, miss) 
    #-- fig: mask 2nd -
    a2ptot_warm     = ma.masked_where(a2ptotplain==0.0, a2ptot_warm) 
    a2ptot_cold     = ma.masked_where(a2ptotplain==0.0, a2ptot_cold) 
    a2ptot_occ      = ma.masked_where(a2ptotplain==0.0, a2ptot_occ) 
    a2ptot_stat     = ma.masked_where(a2ptotplain==0.0, a2ptot_stat) 
    a2ptot_all      = ma.masked_where(a2ptotplain==0.0, a2ptot_all) 
    #-- fig: make frac data -
    a2frac_warm     = (a2ptot_warm / a2ptotplain).filled(0.0)
    a2frac_cold     = (a2ptot_cold / a2ptotplain).filled(0.0)
    a2frac_occ      = (a2ptot_occ / a2ptotplain).filled(0.0)
    a2frac_stat     = (a2ptot_stat / a2ptotplain).filled(0.0)
    a2frac_all      = (a2ptot_all / a2ptotplain).filled(0.0)

    #-- name: fractin data
    fracdatname_warm   = ptotdir + "/frac.rad%04d.warm.saone"%(thdist)
    fracdatname_cold   = ptotdir + "/frac.rad%04d.cold.saone"%(thdist)
    fracdatname_occ    = ptotdir + "/frac.rad%04d.occ.saone"%(thdist)
    fracdatname_stat   = ptotdir + "/frac.rad%04d.stat.saone"%(thdist)
    fracdatname_all    = ptotdir + "/frac.rad%04d.all.saone"%(thdist)

    #-- write data ----
    a2frac_warm.tofile(fracdatname_warm)
    a2frac_cold.tofile(fracdatname_cold)
    a2frac_occ.tofile(fracdatname_occ)
    a2frac_stat.tofile(fracdatname_stat)
    a2frac_all.tofile(fracdatname_all)

    #-- fig: frac prep -
    bnd      = range(6, 60+1, 6)
    bnd_all  = [1.0,10,20,30,40,50,60,70,80,90]
    cbarname = figdir + "/frac.cbar.png" 
    cbarname_all = figdir + "/frac.cbar.all.png" 
    a2shade  = ma.masked_equal(a2domain, 0.0).filled(miss)
    a2shade  = ma.masked_where(a2orog >1500.0, a2shade).filled(miss)
    coef     = 100.0
    stitle   = "proportion (%%), %s "%(season)
    mycm     = "Spectral"
    lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect(region)

    #-- fig: frac draw -
    ctrack_fig.mk_pict_saone_reg(a2frac_warm, bnd, mycm, fracname_warm, stitle+"warm", cbarname, miss, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, a2shade=a2shade, coef=coef)

    ctrack_fig.mk_pict_saone_reg(a2frac_cold, bnd, mycm, fracname_cold, stitle+"cold", cbarname, miss, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, a2shade=a2shade, coef=coef)

    ctrack_fig.mk_pict_saone_reg(a2frac_occ, bnd, mycm, fracname_occ, stitle+"occ", cbarname, miss, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, a2shade=a2shade, coef=coef)

    ctrack_fig.mk_pict_saone_reg(a2frac_stat, bnd, mycm, fracname_stat, stitle+"stat", cbarname, miss, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, a2shade=a2shade, coef=coef)

    ctrack_fig.mk_pict_saone_reg(a2frac_all, bnd_all, mycm, fracname_all, stitle+"all", cbarname_all, miss, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, a2shade=a2shade, coef=coef)






