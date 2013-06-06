from numpy import *
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
eyear = 2000
#iyear = 1997
#eyear = 2004
#lseason=["ALL"]
#lseason=[1,2,3,4,5,6,7,8,9,10,11,12]
#lseason=[10,11,12]
#lseason=["JJA"]
lseason = [1]
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
lthdist   = [500]
dprdir_root  = {}
dprdir_root["GPCP1DD"] = "/media/disk2/data/GPCP1DD/v1.2/1dd"
dprdir_root["JRA25"]  = "/media/disk2/data/JRA25/sa.one/6hr/PR"

#-- para for objective locator -------------
plev     = 850*100.0 # (Pa)
llthfmask = [[0.4,2.0]]
#llthfmask = [[0.2,2.0],[0.3,2.0],[0.5,2.0]]
#llthfmask = [[0.2,2.0],[0.3,2.0]]

thorog  = ctrack_para.ret_thorog()
thgradorog=ctrack_para.ret_thgradorog()
#-------------------------------------------
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
def package_mk_front_loc(a2t, a2q, thfmask1, thfmask2):
  #-- theta_e -----------------------------------
  a2thermo = dtanl_fsub.mk_a2theta_e(plev, a2t.T, a2q.T).T
  #-- grad.theta_e ------------------------------------
  a2gradthermo    = dtanl_fsub.mk_a2grad_abs_saone(a2thermo.T).T
  a2gradthermo    = a2gradthermo * 1000.0*100.0 # [K (100km)-1]
  #-------------
  (a2grad2x, a2grad2y) = dtanl_fsub.mk_a2grad_saone(a2gradthermo.T)
  a2grad2x = a2grad2x.T
  a2grad2y = a2grad2y.T

  a2loc    = dtanl_fsub.mk_a2axisgrad(a2grad2x.T, a2grad2y.T).T
  a2loc    = dtanl_fsub.mk_a2contour(a2loc.T, 0.0, 0.0, miss).T

  a2fmask1 = dtanl_fsub.mk_a2frontmask1(a2thermo.T).T
  a2fmask2 = dtanl_fsub.mk_a2frontmask2(a2thermo.T).T
  a2fmask1 = a2fmask1 *(1000.0*100.0)**2.0  #[(100km)-2]
  a2fmask2 = a2fmask2 *(1000.0*100.0)       #[(100km)-1]
  #-------------
  a2loc    = ma.masked_where(a2fmask1 < thfmask1, a2loc)
  a2loc    = ma.masked_where(a2fmask2 < thfmask2, a2loc)

  a2loc    = ma.masked_where(a2orog > thorog, a2loc)
  a2loc    = ma.masked_where(a2gradorogmask > thgradorog, a2loc)
  a2loc    = a2loc.filled(miss)
  a2loc    = dtanl_fsub.del_front_2grids(a2loc.T, miss).T
  return   a2loc

#***************************************
#--------------------
for season in lseason:
  lmon  = ctrack_para.ret_lmon(season)
  #-- dummy -------------------
  a2one    = ones([ny,nx], float32)
  da2pr_all  = {}
  da2pr_obj_all  = {}
  da2existrat = {}
  #---------
  for lthfmask in llthfmask:
    thfmask1, thfmask2 = lthfmask
    #--------
    for thdist in lthdist:
      #----
      tkey  = (thfmask1, thfmask2, thdist)
      #----
      da2pr_all[tkey]      = zeros([ny,nx], float32) 
      da2pr_obj_all[tkey]  = zeros([ny,nx], float32) 
      da2existrat[thfmask1,thfmask2]    = zeros([ny,nx], float32) 
  #-- out dir -----------------
  odir_root  = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/front/agg/%04d-%04d/%s"%(iyear, eyear, season)

  ptotdir     = odir_root 
  #ptotdir     = "/home/utsumi/temp"
  ctrack_func.mk_dir(ptotdir)

  figdir      = ptotdir
  #----------------------------
  itimes  = 0
  idays   = 0
  for year in range(iyear, eyear+1):
    #--------------------- 
    if calcflag == False:
      continue
    #--------------------- 
    for mon in lmon:
      itimes_mon  = 0
      #-- init --------
      da2pr_mon    = {}
      da2count_mon = {}
      for lthfmask in llthfmask:
        thfmask1, thfmask2 = lthfmask
        #--------
        for thdist in lthdist:
          #----
          tkey  = (thfmask1, thfmask2, thdist)
          #----
          da2pr_mon[tkey]                 = zeros([ny,nx],float32)
          da2count_mon[thfmask1,thfmask2] = zeros([ny,nx],float32)
      #----------------
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
        idays  = idays + 1
        print year, mon, day, "single=",singleday
        #---------------------
        for hour in lhour:
          #-------------------
          itimes = itimes + 1
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
          # objective front locator
          #----------------------------- 
          #-- q: mixing ratio --------------------------
          qname = "/media/disk2/data/JRA25/sa.one/6hr/SPFH/%04d%02d/anal_p25.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
          a2q   = fromfile(qname, float32).reshape(ny,nx)
          #-- t: mixing ratio --------------------------
          tname = "/media/disk2/data/JRA25/sa.one/6hr/TMP/%04d%02d/anal_p25.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
          a2t   = fromfile(tname, float32).reshape(ny,nx)  


          for lthfmask in llthfmask:
            thfmask1, thfmask2 = lthfmask 
            #---------------------------------------------
            a2loc_obj = package_mk_front_loc(a2t, a2q, thfmask1, thfmask2)

            #-- count front loc --
            da2count_mon[thfmask1,thfmask2]= da2count_mon[thfmask1,thfmask2] + ma.masked_where(a2loc_obj == miss,a2one).filled(0.0)
            da2existrat[thfmask1,thfmask2] = da2existrat[thfmask1,thfmask2]  + ma.masked_where(a2loc_obj == miss, a2one).filled(0.0)
            #-----------------------------
            # objective front territory
            #-----------------------------
            for thdist in lthdist:
              #---
              tkey  = (thfmask1, thfmask2, thdist)
              #---
              a2terr_all  = ctrack_fsub.mk_territory_saone( a2loc_obj.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T
              #-----------------------------
              a2num_all   = ma.masked_where(a2terr_all==miss, a2one).filled(0.0)
              #-----------------------------
              a2pr_all_temp  = ma.masked_where(a2terr_all  ==miss, a2pr)
              #---------------------
              a2pr_all_temp  = a2pr_all_temp.filled(0.0)
              #--- add -------------
              da2pr_mon[tkey]      = da2pr_mon[tkey]       + a2pr_all_temp
              da2pr_obj_all[tkey]  = da2pr_obj_all[tkey]  + a2pr_all_temp
      #-- for monthly data ------
      #dir_ptot_mon   = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/front/agg/%04d/%02d"%(year,mon)
      dir_ptot_mon   = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/front/agg/temp/%04d/%02d"%(year,mon)
      ctrack_func.mk_dir(dir_ptot_mon)
      #--
      for lthfmask in llthfmask:
        thfmask1, thfmask2 = lthfmask
        #-- count -
        name_count_mon = dir_ptot_mon + "/count.M1_%s_M2_%s.saone"%(thfmask1, thfmask2)
        da2count_mon[thfmask1,thfmask2] = ma.masked_where(a2orog>1500.0, da2count_mon[thfmask1,thfmask2]).filled(miss)
        da2count_mon[thfmask1,thfmask2].tofile(name_count_mon)

        for thdist in lthdist:
          tkey  = (thfmask1, thfmask2, thdist)
          #----
          print itimes_mon
          da2pr_mon[tkey]   = da2pr_mon[tkey] / itimes_mon  #[mm/s]
          da2pr_mon[tkey]   = ma.masked_where(a2orog>1500, da2pr_mon[tkey]).filled(miss)
          name_ptot_mon  = dir_ptot_mon + "/rad%04d.M1_%s_M2_%s.saone"%(thdist,thfmask1, thfmask2)
          da2pr_mon[tkey].tofile(name_ptot_mon) 
  #---------------------------------------------------------

  for lthfmask in llthfmask:
    thfmask1, thfmask2 = lthfmask 
    #--------------
    da2existrat[thfmask1,thfmask2]  = da2existrat[thfmask1,thfmask2] / itimes
    existrat_name      = ptotdir + "/existrat.M1_%s_M2_%s.saone"%(thfmask1, thfmask2)

    da2existrat[thfmask1,thfmask2].tofile(existrat_name)
    #--------------
    for thdist in lthdist:
      #-----------------
      if calcflag == False:
        continue
      #-----------------
      tkey  = (thfmask1, thfmask2, thdist)
      #********************************************
      # objective front
      #-----------------
      da2pr_obj_all[tkey]   = da2pr_obj_all[tkey]  / itimes    # mm/s
      da2pr_obj_all[tkey]   = da2pr_obj_all[tkey]  * idays *60*60*24.0 /(eyear-iyear+1)    # mm/season
      #-----------------
      #-------------
      da2pr_obj_all[tkey]   = ma.masked_where(a2orog>1500.0, da2pr_obj_all[tkey]).filled(miss)
      #-- ptot name --
      oname_obj_all   = ptotdir + "/rad%04d.M1_%s_M2_%s.saone"%(thdist,thfmask1, thfmask2)
      #--------------
      da2pr_obj_all[tkey].tofile(oname_obj_all)
      print oname_obj_all 
 
  #**********************************************
  #    figure  precipitation 
  #**********************************************
  # figure preparation
  if singleday==True:
    bnd = [0,5,10,15,20,25,30]
  elif len(lmon)==1:
    bnd = [5,10,20,30,60,90,150,210,300]
  elif len(lmon)==3:
    bnd = [10,2000+1,200] 
  elif len(lmon)==12:
    bnd = [100,3000+1, 500]
  #----------------------------
  # figure : objective
  #----------------------------
  
  for lthfmask in llthfmask:
    thfmask1, thfmask2 = lthfmask 
    #------
    for thdist in lthdist:
      #----
      tkey  = (thfmask1, thfmask2, thdist)
      #-- load data ---
      datname = ptotdir + "/rad%04d.M1_%s_M2_%s.saone"%(thdist,thfmask1, thfmask2)
      a2in    = fromfile(datname, float32).reshape(ny,nx)
      #-- fig: name ---
      figdir         = ptotdir
      ctrack_func.mk_dir(figdir)
      figname_all    = figdir + "/front.s%s.M1_%s_M2_%s.png"%(season, thfmask1, thfmask2)
      #-- fig: prep -
      #bnd      = range(6, 60+1, 6)
      cbarname = figdir + "/front.cbar.png" 
      a2shade  = ma.masked_where(a2orog >thorog, a2orog).filled(miss)
      #a2shade  = ma.masked_where(a2gradorogmask >thgradorog, a2shade).filled(miss)
      stitle   = "season:%s M1:%s  M2:%s"%(season,thfmask1, thfmask2)
      mycm     = "jet_r"
      a2in     = ma.masked_equal(a2in, miss).filled(0.0)
      #-- fig: draw -
      ctrack_fig.mk_pict_saone_reg(a2in, bnd=bnd, soname=figname_all, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)

  #**********************************************
  #    figure: rate of existence
  #**********************************************
  # figure preparation
  bnd = [1, 3 ,5, 7, 9, 11, 13, 15, 17]

  #----------------------------
  for lthfmask in llthfmask:
    thfmask1, thfmask2 = lthfmask 

    #-- load data ---

    datname = ptotdir + "/existrat.M1_%s_M2_%s.saone"%(thfmask1, thfmask2)
    a2in    = fromfile(datname, float32).reshape(ny,nx) * 100.0

    #-- fig: name ---
    figdir         = ptotdir
    ctrack_func.mk_dir(figdir)
    figname_all    = figdir + "/existrat.s%s.M1_%s_M2_%s.png"%(season, thfmask1, thfmask2)
    #-- fig: prep -
    #bnd      = range(6, 60+1, 6)
    cbarname = figdir + "/existrat.cbar.png" 
    a2shade  = ma.masked_where(a2orog >thorog, a2orog).filled(miss)
    a2shade  = ma.masked_where(a2gradorogmask >thgradorog, a2shade).filled(miss)
    stitle   = "frequency season:%s M1:%s  M2:%s"%(season,thfmask1, thfmask2)
    mycm     = "jet_r"
    a2in     = ma.masked_equal(a2in, miss).filled(0.0)
    #-- fig: draw -
    ctrack_fig.mk_pict_saone_reg(a2in, bnd=bnd, soname=figname_all, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
 

