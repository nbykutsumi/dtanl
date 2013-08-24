from tag_fsub import *
from gsmap_fsub import *
from numpy import *
import ctrack_para, ctrack_func, ctrack_fig, chart_para
import calendar
import gsmap_func
import datetime
import os, sys
#---------------------------
#singletime = True
singletime = False
calcflag   = True
#calcflag   = False
lbstflag_tc   = ["bst"]
#lbstflag_tc   = ["bst"]
#lbstflag_f    = ["bst.high","bst.type"]
lbstflag_f = [""]
#lprtype  = ["GSMaP"]
lprtype  = ["GSMaP.dec"]


sresol  = "anl_p"
iyear   = 2003
eyear   = 2009
#iyear    = 2001
#eyear    = 2009
#lseason = ["NDJFMA","JJASON"]
#lseason = ["ALL","NDJFMA","JJASON"]
#lseason = ["NDJFMA","JJASON","DJF","JJA"]
#lseason = ["DJF"]
lseason = ["ALL"]
#lseason = [10,11,12]

iday    = 1
ptile   = 99.9 # (%)
lfbctype= ["nn","wn"]
lnhour  = [1,6,24]
#lnhour  = [1,3,6,12,24]
#lnhour  = [24]
#ltag    = ["nbcot","nbcot","tc","c","fbc","nbc","ot","o.tc","o.c","o.fbc","o.nbc","TCF","TCFC","TCB","TCBC"]
ltag    = ["tc","c","fbc","nbc","ot"]
#ltag    = ["nbcot"]
thdura_c  = 48
thdura_tc = thdura_c

iyear_dat= 2001
eyear_dat= 2009
itime_dat = datetime.datetime(iyear_dat,1,1,0)
#--------------------------------
# 100% area
dist_tc = 1000 #[km]
dist_c  = 1000 #[km]
dist_f  = 500 #[km]

## 80% area
#dist_tc    = 894 # [km]
#dist_c     = 894 # [km]
#dist_f     = 400 # [km]

## 120% area
#dist_tc    = 1095 # [km]
#dist_c     = 1095 # [km]
#dist_f     = 600  # [km]

nx,ny     = [360,180]

thorog    = 1500   # [m]
miss      = -9999.0
miss_out  = -9999.0
miss_gpcp = -99999.

#---------------------
region    = "GLOB"
lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region)

#--------------
#calcoef  = 60*60*24.0
calcoef = 1.0e+9   # for floating number calculation reason.
#calcoef = 1.0   # for floating number calculation reason.
#**********************************
for prtype in lprtype:
  da2zero  = {}
  da2one   = {}
  dext     = {}
  if prtype in ["GSMaP"]:
    da2zero[prtype] = zeros([120,360],float32)
    da2one[prtype]  = ones([120,360],float32)
    dext[prtype]    = "sa.one"
  elif prtype in ["GSMaP.dec"]: 
    da2zero[prtype] = zeros([1200,3600],float32)
    da2one[prtype]  = ones([1200,3600],float32)
    dext[prtype]    = "sa.dec"
#
a2one_saone = ones([ny,nx],float32)
#**********************************
# FUNCTIONS
#----------------------------------
def mk_initial_a2accpr( tctype, ftype, dist_tc, dist_c, dist_f, year,mon,day,hour):
  #-----------------------------
  now            = datetime.datetime(year,mon,day,hour)
  da2accpr       = {}
  da2accpr_plain = {}
  #***** init ******
  for fbctype,tag,nhour in ret_lkeys(fbctypeflag=True,tagflag=True,nhourflag=True):
    da2accpr[fbctype,tag,nhour] = da2zero[prtype].copy()
  for nhour in lnhour:
    da2accpr_plain[nhour]       = da2zero[prtype].copy()      
  #*****************
  for nhour in lnhour:
    for inc_hour in range(1,nhour+1):
      timetarget = now + datetime.timedelta(hours= -inc_hour)
      yeart      = timetarget.year
      mont       = timetarget.month
      dayt       = timetarget.day
      hourt      = timetarget.hour
      #** check time ***
      if timetarget < itime_dat: 
        continue
      #-----------------
      #a2pr   = ma.masked_equal(ret_pr(prtype, yeart, mont, dayt, hourt),miss).filled(0.0) 
      a2pr   = ret_pr(prtype, yeart, mont, dayt, hourt).filled(0.0) 
      #*****************************
      # load corresponding tags 
      #-----------------------------
      da2tag = load_tag(tctype, ftype, dist_tc, dist_c, dist_f, yeart, mont, dayt, hourt)   # load 180x360 sa.one shape
      for fbctype,tag in ret_lkeys(fbctypeflag=True,tagflag=True,nhourflag=False):
        da2tag[fbctype,tag] = fitshape(da2tag[fbctype,tag], prtype)

      #*****************************
      # Partial precip for each system
      #-----------------------------
      lkeys  = ret_lkeys(fbctypeflag=True,tagflag=True,nhourflag=False)
      for fbctype,tag in lkeys:
        da2accpr[fbctype,tag,nhour] = da2accpr[fbctype,tag,nhour] \
                                  + a2pr * da2tag[fbctype, tag]

      #---
      da2accpr_plain[nhour]  = da2accpr_plain[nhour]\
                             + a2pr 

  #-----
  return da2accpr_plain, da2accpr
 
#---------------------------
def fitshape(a2saone, prtype):
  if prtype in ["GSMaP"]:
    a2out = a2saone[30:150]
  elif prtype in ["GSMaP.dec"]:
    a2in  = a2saone[30:150]
    a2out = gsmap_fsub.saone_gsmap2dec_gsmap(a2in.T).T
  #-----
  return a2out

#---------------------------
def ret_da2pr_kick(now, prtype, tctype, ftype, dist_tc, dist_c, dist_f):
  #----
  da2prplain_kick  = {}
  da2pr_kick       = {}
  #----
  for nhour in lnhour:
    timekick     = now + datetime.timedelta(hours = -nhour)
    year_kick    = timekick.year
    mon_kick     = timekick.month
    day_kick     = timekick.day
    hour_kick    = timekick.hour
    #
    #-- in nofiles ---
    if timekick < itime_dat:
      da2prplain_kick[nhour] = da2zero[prtype]
      for fbctype, tag in ret_lkeys(fbctypeflag=True, tagflag=True, nhourflag=False):
        da2pr_kick[fbctype,tag,nhour] = da2zero[prtype]
    #-----------------
    else: 
      #da2prplain_kick[nhour] = ma.masked_equal(ret_pr(prtype,year_kick,mon_kick,day_kick,hour_kick), miss).filled(0.0)
      da2prplain_kick[nhour] = ret_pr(prtype,year_kick,mon_kick,day_kick,hour_kick).filled(0.0)
      #
      da2tag_kick  = load_tag(tctype, ftype, dist_tc,dist_c,dist_f, year_kick,mon_kick,day_kick,hour_kick)
      #
      for fbctype, tag in ret_lkeys(fbctypeflag=True, tagflag=True, nhourflag=False):
        a2tag_kick_tmp  = fitshape(da2tag_kick[fbctype,tag], prtype)
        da2pr_kick[fbctype,tag,nhour] = a2tag_kick_tmp * da2prplain_kick[nhour]

    #
  return da2prplain_kick, da2pr_kick
#---------------------------
def ret_pr(prtype,yeart,mont,dayt,hourt):
  #---
  if prtype =="GSMaP": 
    a2pr  = gsmap_func.timeave_gsmap_backward_saone(yeart,mont,dayt,hourt,1)

    #-- test --
    #a2pr  = ones([120,360],float32) 

  if prtype =="GSMaP.dec": 
    a2pr  = gsmap_func.timeave_gsmap_backward_org(yeart,mont,dayt,hourt,1)
  #---
  return ma.masked_equal(a2pr, miss) * calcoef

#---------------------------
def load_tag(tctype,ftype, dist_tc,dist_c,dist_f,year,mon,day,hour):
  #--
  htag_inc    = ret_htag_inc(hour)
  timetarget  = datetime.datetime(year,mon,day,hour) + datetime.timedelta(hours=htag_inc)
  yeart       = timetarget.year
  mont        = timetarget.month
  dayt        = timetarget.day
  hourt       = timetarget.hour
  #
  tagdir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/tag/c%02dh.tc%02dh"%(sresol, thdura_c, thdura_tc)
  tagdir   = tagdir_root + "/%04d%02d"%(yeart, mont)
  tagname  = tagdir + "/tag.%stc%04d.c%04d.%sf%04d.%04d.%02d.%02d.%02d.sa.one"%(tctype, dist_tc, dist_c, ftype, dist_f, yeart,mont,dayt,hourt)
  #-- load -------
  a2tag     = fromfile(tagname, int32).reshape(180,360)
  lout      = tag_fsub.solve_tag_4type(a2tag.T)
  
  a2tag_tmp_tc  = array(lout[0].T, float32)
  a2tag_tmp_c   = array(lout[1].T, float32)
  a2tag_tmp_fbc = array(lout[2].T, float32)
  a2tag_tmp_nbc = array(lout[3].T, float32)
  a2tag_tmp_ot  = ma.masked_where(a2tag !=0, a2one_saone).filled(0.0)
  
  a2tag_sum     = a2tag_tmp_tc + a2tag_tmp_c + a2tag_tmp_fbc

  #---------------
  da2tag           = {}
  da2tag["nn","tc" ] = (ma.masked_where(a2tag_sum ==0.0, a2tag_tmp_tc ) / a2tag_sum).filled(0.0)
  da2tag["nn","c"  ] = (ma.masked_where(a2tag_sum ==0.0, a2tag_tmp_c  ) / a2tag_sum).filled(0.0)
  da2tag["nn","fbc"] = (ma.masked_where(a2tag_sum ==0.0, a2tag_tmp_fbc) / a2tag_sum).filled(0.0)
  da2tag["nn","ot" ] =  ma.masked_where(a2tag_sum !=0.0, a2one_saone).filled(0.0)
  
  # wn: with non-baroclinic    
  a2tagwn_sum     = a2tag_tmp_tc + a2tag_tmp_c + a2tag_tmp_fbc + a2tag_tmp_nbc
  da2tag["wn","tc" ]  = (ma.masked_where(a2tagwn_sum ==0.0, a2tag_tmp_tc ) / a2tagwn_sum).filled(0.0)
  da2tag["wn","c"  ]  = (ma.masked_where(a2tagwn_sum ==0.0, a2tag_tmp_c  ) / a2tagwn_sum).filled(0.0)
  da2tag["wn","fbc"]  = (ma.masked_where(a2tagwn_sum ==0.0, a2tag_tmp_fbc) / a2tagwn_sum).filled(0.0)
  da2tag["wn","nbc"]  = (ma.masked_where(a2tagwn_sum ==0.0, a2tag_tmp_nbc) / a2tagwn_sum).filled(0.0) 
  da2tag["wn","ot" ]  =  ma.masked_where(a2tagwn_sum !=0.0, a2one_saone).filled(0.0)
  #
  return da2tag   

#---------------------------
def ret_lkeys(fbctypeflag, tagflag, nhourflag):
  if (fbctypeflag, tagflag, nhourflag) == (True,True,True):
    lkeys = [ [fbctype,tag,nhour] for fbctype in lfbctype\
                                for tag   in ltag\
                                for nhour in lnhour]
    if (("nn" in lfbctype)&("nbc" in ltag)):
      for nhour in lnhour:
        lkeys.remove(["nn","nbc",nhour])
  #----
  if (fbctypeflag, tagflag, nhourflag) == (True,True,False):
    lkeys = [ [fbctype,tag] for fbctype in lfbctype\
                                for tag   in ltag]
    if (("nn" in lfbctype)&("nbc" in ltag)):
      lkeys.remove(["nn","nbc"])
  #----
  return lkeys

#----------------------------------- 
def ret_htag_inc(hour):
  #--------------------------
  # for backward precipitation
  #--------------------------
  if hour in [0,6,12,18]:
    htag_inc = 0
  elif hour in [1,7,13,19]:
    htag_inc = -1
  elif hour in [2,8,14,20]:
    htag_inc = -2
  elif hour in [3,9,15,21]:
    htag_inc = -3
  elif hour in [4,10,16,22]:
    htag_inc = +2
  elif hour in [5,11,17,23]:
    htag_inc = +1
  #
  return htag_inc
#----------------------------------- 
#**************************************************
#  START 
#---------------------
for season, prtype in [[season,prtype]\
                    for season in lseason\
                    for prtype in lprtype]:
  #-- load ptile -------
  da2ptile  = {}
  for nhour in lnhour:
    #if prtype == "JRA":
    #  ptiledir_root   = "/media/disk2/data/JRA25/sa.one/6hr/PR/ptile" 
    #  ptiledir        = ptiledir_root + "/%04d-%04d"%(2001,2004)
    #  ptilename       = ptiledir + "/fcst_phy2m.PR.p%05.2f.%s.sa.one"%(ptile,"ALL")
    #  #ptiledir        = ptiledir_root + "/%04d-%04d"%(iyear,eyear)
    #  da2ptile[nhour] = fromfile(ptilename, float32).reshape(ny,nx)
    #if prtype == "GPCP1DD":
    #  ptiledir_root   = "/media/disk2/data/GPCP1DD/v1.2/1dd/ptile" 
    #  ptiledir        = ptiledir_root + "/%04d-%04d"%(2000,2010)
    #  ptilename       = ptiledir + "/pr.gpcp.p%05.2f.%s.bn"%(ptile,"ALL")
    #  #ptiledir        = ptiledir_root + "/%04d-%04d"%(iyear,eyear)
    #  da2ptile[nhour] = fromfile(ptilename, float32).reshape(ny,nx)

    if prtype == "GSMaP":
      thmissrat = 0.8
      ptiledir_root   = "/media/disk2/data/GSMaP/sa.one/1hr/ptot/ptile" 
      ptiledir        = ptiledir_root + "/%04d-%04d"%(2001, 2009)
      ptilename       = ptiledir  + "/gsmap_mvk.v5.222.1.movw%02dhr.%3.1f.p%05.2f.ALL.sa.one"%(nhour, thmissrat, ptile)
      da2ptile[nhour] = fromfile(ptilename, float32).reshape(120,360)

      #- test --
      #da2ptile[nhour] = ones([120,360],float32)*0.5
 
    if prtype == "GSMaP.dec":
      thmissrat = 0.8
      ptiledir_root   = "/home/utsumi/mnt/iis.data1/utsumi/GSMaP/ptile.dec" 
      ptiledir        = ptiledir_root + "/%04d-%04d"%(2001, 2009)
      ptilename       = ptiledir  + "/gsmap_mvk.v5.222.1.movw%02dhr.%3.1f.p%05.2f.ALL.sa.dec"%(nhour, thmissrat, ptile)
      da2ptile[nhour] = fromfile(ptilename, float32).reshape(1200,3600)
    print ptilename
  #-- mask a2ptile ---
  for nhour in lnhour:
    da2ptile[nhour] = ma.masked_equal(da2ptile[nhour], miss) * calcoef

  #-----------------------
  for bstflag_tc, bstflag_f in [[bstflag_tc, bstflag_f]\
                                 for bstflag_tc in lbstflag_tc\
                                 for bstflag_f  in lbstflag_f]:
    #-- TC type ----------
    if bstflag_tc =="bst":
      tctype = "bst"
    else:
      tctype = "obj"
    #-- front type  ------
    if bstflag_f   == "bst.high":
      ftype  = "bst.high"
    elif bstflag_f == "bst.type":
      ftype  = "bst.type"
    elif bstflag_f == "":
      ftype  = ""
    #---------------------
    if prtype in ["GPCP1DD"]:
      coef       = 1.0/(60*60*24.0)
    else:
      coef       = 1.0
    #--- tag dir_root -------------------
    tagdir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/tag/c%02dh.tc%02dh"%(sresol, thdura_c, thdura_tc)
    #--- lhour -----------------------
    lhour = range(24) 
    #--- corresponding tag time ------

    #-- orog ------------------------
    orogname = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
    a2orog   = fromfile(orogname, float32).reshape(ny,nx)
    
    a2shade  = ma.masked_where(a2orog >thorog, a2orog).filled(miss)
    #***************************************
    if calcflag == True:
      #-----------------
      lmon = ctrack_para.ret_lmon(season)
      #--------------------------------
      for year in range(iyear, eyear+1):
        #-----------------
        for mon in lmon:
          #**** init da2accpr *********
          da2accpr_plain , da2accpr = mk_initial_a2accpr(tctype, ftype, dist_tc, dist_c, dist_f, year, mon, iday, 0)

          da2accpr_plain_init , da2accpr_init = mk_initial_a2accpr(tctype, ftype, dist_tc, dist_c, dist_f, year, mon, iday, 0)

          #**** init da2num ***********
          lkeys = ret_lkeys(fbctypeflag=True,tagflag=True,nhourflag=True)
          da2num          = {}
          for fbctype, tag, nhour in lkeys:
            da2num[fbctype,tag,nhour]   = da2zero[prtype].copy()

          da2num_plain    = {}
          for nhour in lnhour:
            da2num_plain[nhour]         = da2zero[prtype].copy()
          #**** init others ***********
          a2totalcount    = da2zero[prtype].copy()
 
          #-- prdir ---
          if prtype in ["GSMaP.03hr", "JRA"]:
            prdir    = prdir_root + "/%04d%02d"%(year, mon)
          elif prtype in ["GPCP1DD"]:
            prdir    = prdir_root + "/%04d"%(year)
          #--------------------
          eday  = calendar.monthrange(year,mon)[1]
          #--------------------
          if singletime ==True:
            eday = iday
            lhour = [0]
          ##-- leap year -------
          #if (mon==2)&(eday==29):
          #  eday = 28
          #--------------------
          for day in range(iday, eday+1):
            ##***
            #if (year==iyear_dat)&(mon==1)&(day==1):
            #  continue
            #elif (year==eyear_dat)&(mon==12)&(day==eday):
            #  continue
            #*** 
            for hour in lhour:
              now = datetime.datetime(year,mon,day,hour)
              print year,mon,day,hour
              #*****************************
              #-- load prec ----
              # prtype == GSMaP: 120x360
              # prtype == GSMaP.dec: 1200x3600
              #-----------------------------
              a2pr         = ret_pr(prtype, year, mon, day, hour)

              a2totalcount = a2totalcount + ma.masked_where(a2pr.mask, da2one[prtype]).filled(0.0)
              a2pr         = a2pr.filled(0.0)

              #a2totalcount = a2totalcount + ma.masked_where(a2pr==miss, da2one[prtype]).filled(0.0)

              #a2pr         = ma.masked_equal(a2pr, miss).filled(0.0)

              #*****************************
              # load corresponding tags 
              #-----------------------------
              da2tag = load_tag(tctype, ftype, dist_tc, dist_c, dist_f, year, mon, day, hour)   # load 180x360 sa.one shape
              for fbctype,tag in ret_lkeys(fbctypeflag=True,tagflag=True,nhourflag=False):
                da2tag[fbctype,tag] = fitshape(da2tag[fbctype,tag], prtype)

              #*****************************
              # update da2pr_kick
              #-----------------------------
              da2prplain_kick, da2pr_kick\
                 = ret_da2pr_kick(now, prtype, tctype, ftype, dist_tc, dist_c, dist_f)

              #*****************************
              # Partial precip for each system
              #-----------------------------
              lkeys  = ret_lkeys(fbctypeflag=True,tagflag=True,nhourflag=True)

              for [fbctype,tag,nhour] in lkeys:
                da2accpr[fbctype,tag,nhour] = da2accpr[fbctype,tag,nhour] \
                                          - da2pr_kick[fbctype,tag, nhour]\
                                          + a2pr * da2tag[fbctype, tag]


              #---
              for nhour in lnhour:

                da2accpr_plain[nhour]  = da2accpr_plain[nhour]\
                                       - da2prplain_kick[nhour]\
                                       + a2pr 



                 
              
              #*****************************
              # check Pex
              #-----------------------------
              # plain
              #-----------
              for nhour in lnhour:
                da2num_plain[nhour]\
                  = da2num_plain[nhour]\
                  + ma.masked_where(da2accpr_plain[nhour] < da2ptile[nhour] * nhour, da2one[prtype]).filled(0.0)
              #-----------
              # each tag
              #-----------
              lkeys     = ret_lkeys(fbctypeflag=True,tagflag=True,nhourflag=True)
              for [fbctype,tag,nhour] in lkeys:
                a2numtmp = ma.masked_where(da2accpr_plain[nhour] < da2ptile[nhour] * nhour, da2accpr[fbctype,tag,nhour])

                a2numtmp =(ma.masked_where(da2accpr_plain[nhour] < 0.0, a2numtmp) / da2accpr_plain[nhour]).filled(0.0)


                da2num[fbctype,tag,nhour] = da2num[fbctype,tag,nhour]\
                                          + a2numtmp

          #*************************************
          # mask where da2ptile is Masked
          #----------
          lkeys     = ret_lkeys(fbctypeflag=True,tagflag=True,nhourflag=True)
          for [fbctype,tag,nhour] in lkeys:
            da2num[fbctype,tag,nhour] = ma.masked_where(da2ptile[nhour].mask, da2num[fbctype,tag,nhour]).filled(miss)

          #----------
          for nhour in lnhour:
            da2num_plain[nhour]       = ma.masked_where(da2ptile[nhour].mask, da2num_plain[nhour]).filled(miss)

          #*************************************
          #----- write to file ---
          #--------------------------
          odir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/tagexpr/%s.c%02dh.tc%02dh"%(sresol, fbctype, thdura_c, thdura_tc)
          odir      = odir_root + "/%s.%04d-%04d.%s.%04d.%02d"%(prtype, iyear_dat, eyear_dat, season, year,mon)
          ctrack_func.mk_dir(odir)

          #-- num -----
          dnumname  = {}
          lkeys     = ret_lkeys(fbctypeflag=True,tagflag=True,nhourflag=True)
          for [fbctype,tag,nhour] in lkeys:
            numname\
            = odir + "/num.%s.%s.mov%02dhr.%05.2f.%stc%04d.c%04d.%sf%04d.%s.%s" %(fbctype, prtype, nhour, ptile, tctype, dist_tc, dist_c, ftype, dist_f, tag, dext[prtype])
            #
            da2num[fbctype,tag,nhour].tofile(numname)
            print numname
          
          a = ma.masked_equal(da2num["nn","c",24],-9999.0)
          b = ma.masked_equal(da2num["nn","tc",24],-9999.0)
          c = ma.masked_equal(da2num["nn","fbc",24],-9999.0)
          d = ma.masked_equal(da2num["nn","ot",24],-9999.0)
          s = a+b+c+d 
          #-- num_plain ----
          dnumname_plain = {}
          for nhour in lnhour:
            numname_plain\
            = odir + "/num.%s.mov%02dhr.plain.%s" %(prtype, nhour, dext[prtype])
          #--
          da2num_plain[nhour].tofile(numname_plain)
          print numname_plain
          p = ma.masked_equal(da2num_plain[24], -9999.0)
          #-- totalcount ----
          totalcountname\
            = odir + "/totalcount.%s.%s"%(prtype,dext[prtype])
          a2totalcount.tofile(totalcountname)
          print totalcountname
          #**************************************
