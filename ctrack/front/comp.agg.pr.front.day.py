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
singleday= True
iyear = 2004
eyear = 2004
#lseason=["JJA"]
lseason = [7]
iday  = 14
#lhour = [12]
lhour = [0]
region= "ASAS"
ny    = 180
nx    = 360
#prtype = "GPCP1DD"
prtype = "JRA25"
miss   = -9999.0
miss  = -9999.0
miss_gpcp = -99999.
#lthdist   = [250,500,1000,1500]
lthdist   = [500]
locdir_root  = "/media/disk2/out/chart/%s/front"%(region)
dprdir_root  = {}
dprdir_root["GPCP1DD"] = "/media/disk2/data/GPCP1DD/v1.2/1dd"
dprdir_root["JRA25"]  = "/media/disk2/data/JRA25/sa.one/6hr/PR"

#-- para for objective locator -------------
plev     = 850*100.0 # (Pa)
#llthfmask = [[0.3,2.0]]
llthfmask = [[0.5,2.0],[0.8,2.0],[1.0,2.0],[0.5,2.5],[0.5,3.0]]

#-------------------------------------------
#----------------------------
calcflag = True
#calcflag = False
meanflag = True
#-- orog --------------------
orogname = "/media/disk2/data/JRA25/sa.one/const/topo/topo.sa.one"
domname  = "/media/disk2/out/chart/%s/const/domainmask_saone.%s.2000.01.bn"%(region,region)
a2orog   = fromfile(orogname, float32).reshape(ny,nx)
a2domain = fromfile(domname , float32).reshape(ny,nx)
a2chartshade = ma.masked_where(a2orog>1500.0, a2orog).filled(miss)
a2chartshade = ma.masked_where(a2domain==0.0, a2chartshade).filled(miss)
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
  a2loc    = dtanl_fsub.mk_a2contour(a2loc.T, 0.0, 0.0, miss_out).T


  a2fmask1 = dtanl_fsub.mk_a2frontmask1(a2thermo.T).T
  a2fmask2 = dtanl_fsub.mk_a2frontmask2(a2thermo.T).T
  a2fmask1 = a2fmask1 *(1000.0*100.0)**2.0  #[(100km)-2]
  a2fmask2 = a2fmask2 *(1000.0*100.0)       #[(100km)-1]
  #-------------
  a2loc    = ma.masked_where(a2fmask1 < thfmask1, a2loc)
  a2loc    = ma.masked_where(a2fmask2 < thfmask2, a2loc)
  return   a2loc

#***************************************
#----------------------------
for lthfmask in llthfmask:
  thfmask1, thfmask2 = lthfmask
  #--------------------
  for season in lseason:
    #-- dummy -------------------
    a2one    = ones([ny,nx], float32)
    da2pr_all  = {}
    da2pr_obj_all  = {}
    for thdist in lthdist:
      da2pr_all[thdist]      = zeros([ny,nx], float32) 
      da2pr_obj_all[thdist]  = zeros([ny,nx], float32) 
    #-- out dir -----------------
    odir_root  = "/media/disk2/out/chart/%s/front/agg/%04d-%04d/%s"%(region, iyear, eyear, season)
  
    #ptotdir     = odir_root + "/ptot"
    ptotdir     = "/home/utsumi/temp"
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
        if singleday==True:
          eday = iday
        #----------------
        for day in range(iday, eday+1):
          print mon, day
          for hour in lhour:
            #---------------------
            if ((year==iyear)&(mon==1)&(day==1)):
              continue
            if ((year==eyear)&(mon==12)&(day==31)):
              continue 
            #---------------------
            if singleday == True:
              if (day !=iday):
                continue
            #-------------------
            itimes = itimes + 1
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
            # chart locator
            #-----------------------------
            locname    = locdir + "/front.%s.%04d.%02d.%02d.%02d.saone"%(region, year, mon, day, hour)
            a2loc      = fromfile(locname, float32).reshape(ny,nx)

            #--- domain & orog mask --------------------
            a2loc = ma.masked_where(a2chartshade==miss, a2loc).filled(miss)

            #-----------------------------
            # chart territory
            #-----------------------------
            for thdist in lthdist:
              a2terr_all  = ctrack_fsub.mk_territory_saone( a2loc.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T
              #-----------------------------
              a2num_all   = ma.masked_where(a2terr_all==miss, a2one).filled(0.0)
              #-----------------------------
              a2pr_all_temp  = ma.masked_where(a2terr_all  ==miss, a2pr)
              #---------------------
              a2pr_all_temp  = a2pr_all_temp.filled(0.0)
              #--- add -------------
              da2pr_all[thdist]  = da2pr_all[thdist]  + a2pr_all_temp
  
            #*********************************************
            # objective front locator
            #----------------------------- 
            #-- q: mixing ratio --------------------------
            qname = "/media/disk2/data/JRA25/sa.one/6hr/SPFH/%04d%02d/anal_p25.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
            a2q   = fromfile(qname, float32).reshape(ny,nx)
            #-- t: mixing ratio --------------------------
            tname = "/media/disk2/data/JRA25/sa.one/6hr/TMP/%04d%02d/anal_p25.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
            a2t   = fromfile(tname, float32).reshape(ny,nx)  
            #---------------------------------------------
            a2loc_obj = package_mk_front_loc(a2t, a2q, thfmask1, thfmask2)

            #--- domain & orog mask --------------------
            a2loc_obj = ma.masked_where(a2chartshade==miss, a2loc_obj).filled(miss)
            #-----------------------------
            # objective front territory
            #-----------------------------
            for thdist in lthdist:
              a2terr_all  = ctrack_fsub.mk_territory_saone( a2loc_obj.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T
              #-----------------------------
              a2num_all   = ma.masked_where(a2terr_all==miss, a2one).filled(0.0)
              #-----------------------------
              a2pr_all_temp  = ma.masked_where(a2terr_all  ==miss, a2pr)
              #---------------------
              a2pr_all_temp  = a2pr_all_temp.filled(0.0)
              #--- add -------------
              da2pr_obj_all[thdist]  = da2pr_obj_all[thdist]  + a2pr_all_temp


    #---------------------------------------------------------
    for thdist in lthdist:
      #-----------------
      if calcflag == False:
        continue
      #********************************************
      # chart front
      #-----------------
      da2pr_all[thdist]   = da2pr_all[thdist]  / itimes
      #-----------------
      da2pr_all[thdist]   = ma.masked_where(a2domain==0.0, da2pr_all[thdist]).filled(miss)
      #-------------
      da2pr_all[thdist]   = ma.masked_where(a2orog>1500.0, da2pr_all[thdist]).filled(miss)
      #-- ptot name --
      oname_all   = ptotdir + "/rad%04d.all.saone"%(thdist)
      #--------------
      #da2pr_all[thdist].tofile(oname_all)

      #********************************************
      # objective front
      #-----------------
      da2pr_obj_all[thdist]   = da2pr_obj_all[thdist]  / itimes
      #-----------------
      da2pr_obj_all[thdist]   = ma.masked_where(a2domain==0.0, da2pr_obj_all[thdist]).filled(miss)
      #-------------
      da2pr_obj_all[thdist]   = ma.masked_where(a2orog>1500.0, da2pr_obj_all[thdist]).filled(miss)
      #-- ptot name --
      oname_obj_all   = ptotdir + "/rad%04d.all.saone"%(thdist)
      #--------------
      #da2pr_obj_all[thdist].tofile(oname_obj_all)
  

    #**********************************************
    # figure preparation
    bnd = [0,5,10,15,20,25,30]
    #**********************************************
    # figure : chart
    #----------------------------------------------
    for thdist in lthdist:
      #-- fig: name ---
      figdir         = ptotdir
      ctrack_func.mk_dir(figdir)
      figname_all    = figdir + "/front.%04d.%02d.%02d.%02d.rad%04d.%s.png"%(year, mon, day, hour, thdist, region)
      #-- fig: prep -
      #bnd      = range(6, 60+1, 6)
      cbarname = figdir + "/front.cbar.png" 
      a2shade  = ma.masked_equal(a2domain, 0.0).filled(miss)
      a2shade  = ma.masked_where(a2orog >1500.0, a2shade).filled(miss)
      stitle   = "%04d.%02d.%02d.%02d"%(year,mon,day,hour)
      mycm     = "jet_r"
      lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect(region)
 
      a2in     = ma.masked_equal(da2pr_all[thdist], miss).filled(0.0) *60*60*24.0
      #-- fig: draw -
      ctrack_fig.mk_pict_saone_reg(a2in, bnd=bnd, soname=figname_all, stitle=stitle, miss=miss, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, a2shade=a2shade, cbarname=cbarname)
  
    #**********************************************
    # figure : objective
    #----------------------------------------------
    for thdist in lthdist:
      #-- fig: name ---
      figdir         = ptotdir
      ctrack_func.mk_dir(figdir)
      figname_all    = figdir + "/front.%04d.%02d.%02d.%02d.rad%04d.%s.M1_%s_M2_%s.png"%(year, mon, day, hour, thdist, region, thfmask1, thfmask2)
      #-- fig: prep -
      #bnd      = range(6, 60+1, 6)
      cbarname = figdir + "/front.cbar.png" 
      a2shade  = ma.masked_equal(a2domain, 0.0).filled(miss)
      a2shade  = ma.masked_where(a2orog >1500.0, a2shade).filled(miss)
      stitle   = "M1:%s  M2:%s %04d.%02d.%02d.%02d"%(thfmask1, thfmask2, year,mon,day,hour)
      mycm     = "jet_r"
      lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect(region)
 
      a2in     = ma.masked_equal(da2pr_obj_all[thdist], miss).filled(0.0) *60*60*24.0
      #-- fig: draw -
      ctrack_fig.mk_pict_saone_reg(a2in, bnd=bnd, soname=figname_all, stitle=stitle, miss=miss, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, a2shade=a2shade, cbarname=cbarname)
  






