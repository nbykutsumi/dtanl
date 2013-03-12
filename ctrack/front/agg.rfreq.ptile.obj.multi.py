from numpy import *
import sys
import calendar
import datetime
from ctrack_fsub import *
from dtanl_fsub import *
import gsmap_func
import ctrack_para
import ctrack_func
import chart_para
import subprocess
#---------------------------------
#singleday= True
singleday= False
calcflag = True
#calcflag = False

#iyear = 2004
iyear = 2000
eyear = 2004
#eyear = 1997

iyear_ptile = 2000
eyear_ptile = 2010

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
thdist   = 500  # [km]
dprdir_root  = {}
dprdir_root["GPCP1DD"] = "/media/disk2/data/GPCP1DD/v1.2/1dd"
dprdir_root["JRA25"]  = "/media/disk2/data/JRA25/sa.one/6hr/PR"
#-- para for percentile ---
percent  = 99 # (%)

#-- para for objective locator -------------
plev     = 850*100.0 # (Pa)
#thfmasks = (0.4,2.0)
#thfmasks = (0.5,2.0)
thfmasks = (0.6,2.0)

thorog  = ctrack_para.ret_thorog()
thgradorog=ctrack_para.ret_thgradorog()

#-- para for baroclinic --------------------
#thbc     = 0.7 /1000.0/100.0  # (K/100km)
thbc     = 0.9 /1000.0/100.0  # (K/100km)

#-------------------------------------------
#----------------------------
#-- orog --------------------
orogname = "/media/disk2/data/JRA25/sa.one/const/topo/topo.sa.one"
a2orog   = fromfile(orogname, float32).reshape(ny,nx)
gradorogadjname= "/media/disk2/data/JRA25/sa.one/const/topo/grad.topo.adj.twogrids.sa.one"
a2gradorogmask = fromfile(gradorogadjname, float32).reshape(ny,nx)

#-- ptile  ------------------
if percent >0.0:
  if prtype == "GPCP1DD":
    ptiledir = "/media/disk2/data/GPCP1DD/v1.2/1dd/ptile/%04d-%04d"%(iyear_ptile, eyear_ptile)
    ptilename= ptiledir + "/pr.gpcp.p%05.2f.ALL.bn"%(percent)
    a2ptile  = fromfile(ptilename, float32).reshape(ny,nx)
    a2ptile  = flipud(a2ptile)
    a2ptile  = a2ptile / (60.0*60.0*24.0)   # mm/day --> mm/s
elif percent == 0.0:
  a2ptile = zeros([ny,nx],float32)
#----------------------------
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

#******************************
#-- dummy front ---------------
a2one    = ones([ny,nx], float32)
da2terr_front_all = {}
da2pr_front_all  = {}
#---------
#******************************
thfmask1, thfmask2 = thfmasks
#----------------------------
for year in range(iyear, eyear+1):
  #--------------------- 
  if calcflag == False:
    continue
  #--------------------- 
  for mon in lmon:
    #-- out dir -----------------
    odir        = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/front/agg/%04d/%02d/rfreq"%(year, mon)
    ctrack_func.mk_dir(odir)
    
    #************************
    #-- init for front ------
    a2numfront  = zeros([ny,nx],float32)
    a2numbcf    = zeros([ny,nx],float32)        
    a2numnobc   = zeros([ny,nx],float32)
    a2numplain  = zeros([ny,nx],float32)

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
        qname = "/media/disk2/data/JRA25/sa.one/6hr/SPFH/%04d%02d/anal_p25.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
        a2q   = fromfile(qname, float32).reshape(ny,nx)
        #-- t: mixing ratio --------------------------
        tname = "/media/disk2/data/JRA25/sa.one/6hr/TMP/%04d%02d/anal_p25.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
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
        # objective front territory: front
        #-----------------------------
        #---------------------------------------------
        a2loc_front    =  locbase2locfront(a2loc_base, a2fmask1, a2fmask2, thfmask1, thfmask2)

        a2loc_front    =  ctrack_fsub.find_highsidevalue_saone(a2gradthermo.T, a2loc_front.T, a2gradtv.T, distwarmside, miss).T

        a2terr_front   = ctrack_fsub.mk_territory_saone( a2loc_front.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T

        #-----------------------------
        # objective front territory: baroclinic
        #-----------------------------
        a2loc_front_bcf   = ma.masked_less( a2loc_front, thbc).filled(miss)
        a2terr_front_bcf  = ctrack_fsub.mk_territory_saone( a2loc_front_bcf.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T

        #-----------------------------
        # objective front territory: non-baroclinic
        #-----------------------------
        a2loc_front_nobc   = ma.masked_greater_equal( a2loc_front, thbc).filled(miss)
        a2terr_front_nobc  = ctrack_fsub.mk_territory_saone( a2loc_front_nobc.T, thdist*1000.0, miss, -89.5, 1.0 ,1.0).T

        #***********************************************
        # aggregate num : front
        #-----------------------------------
        a2numfront_temp   = ma.masked_where(a2terr_front  ==miss, a2one)
        a2numfront_temp   = ma.masked_where(a2pr <= a2ptile, a2numfront_temp)
        #------------------
        a2numfront_temp   = a2numfront_temp.filled(0.0)
        #--- add ----------
        a2numfront        = a2numfront  + a2numfront_temp

        #***********************************************
        # aggregate num : baroclinic front
        #-----------------------------------
        a2numbcf_temp     = ma.masked_where(a2terr_front_bcf ==miss, a2one)
        a2numbcf_temp     = ma.masked_where(a2pr <= a2ptile, a2numbcf_temp)
        #--------------------
        a2numbcf_temp     = a2numbcf_temp.filled(0.0)
        #--- add ------------
        a2numbcf          = a2numbcf + a2numbcf_temp

        #***********************************************
        # aggregate num : non-baroclinic front
        #-----------------------------------
        a2numnobc_temp   = ma.masked_where(a2terr_front_nobc ==miss, a2one)
        a2numnobc_temp   = ma.masked_where(a2pr <= a2ptile, a2numnobc_temp)
        #------------------
        a2numnobc_temp   = a2numnobc_temp.filled(0.0)
        #--- add ----------
        a2numnobc        = a2numnobc  + a2numnobc_temp

        #***********************************************
        # aggregate num : plain precip
        #-----------------------------------
        a2numplain_temp   = ma.masked_where(a2pr <= a2ptile, a2one)
        #------------------
        a2numplain_temp   = a2numplain_temp.filled(0.0)
        #--- add ----------
        a2numplain        = a2numplain  + a2numplain_temp

    #********************************
    a2numfront      = ma.masked_where(a2orog >thorog, a2numfront).filled(miss)
    a2numbcf        = ma.masked_where(a2orog >thorog, a2numbcf).filled(miss)
    a2numnobc       = ma.masked_where(a2orog >thorog, a2numnobc).filled(miss)
    a2numplain      = ma.masked_where(a2orog >thorog, a2numplain).filled(miss)

    #-- for monthly data front ------
    oname_numfront  = odir + "/num.rad%04d.p%05.2f.M1_%3.2f.M2_%3.2f.front.saone"%(thdist, percent, thfmask1, thfmask2 )
    oname_numbcf    = odir + "/num.rad%04d.p%05.2f.M1_%3.2f.M2_%3.2f.thbc_%03.2f.bcf.saone"%(thdist, percent, thfmask1, thfmask2 ,thbc*1000*100)
    oname_numnobc   = odir + "/num.rad%04d.p%05.2f.M1_%3.2f.M2_%3.2f.thbc_%03.2f.nobc.saone"%(thdist, percent, thfmask1, thfmask2 ,thbc*1000*100)
    oname_numplain  = odir + "/num.p%05.2f.plain.saone"%(percent)
    #--------------------------------
    a2numfront.tofile(oname_numfront)
    a2numbcf.tofile(oname_numbcf)
    a2numnobc.tofile(oname_numnobc)
    a2numplain.tofile(oname_numplain)
    print oname_numbcf
