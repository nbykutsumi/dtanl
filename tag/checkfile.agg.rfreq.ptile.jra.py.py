from numpy import *
import ctrack_para, ctrack_func, ctrack_fig, chart_para
import calendar
import datetime
import os, sys
#---------------------------
lbstflag_tc   = ["bst"]
#lbstflag_tc   = ["bst"]
#lbstflag_f    = ["bst.high","bst.type"]
lbstflag_f = [""]
#lprtype  = ["GSMaP"]
lprtype  = ["GSMaP.dec"]

#-------------------
dext = {"GSMaP.dec":"sa.dec", "GSMaP":"sa.one"}
#-------------------

sresol  = "anl_p"
iyear   = 2001
eyear   = 2009
#iyear    = 2001
#eyear    = 2009
#lseason = ["NDJFMA","JJASON"]
#lseason = ["ALL","NDJFMA","JJASON"]
#lseason = ["NDJFMA","JJASON","DJF","JJA"]
#lseason = ["DJF"]
#lseason = ["ALL"]
lseason = ["ALL"]

iday    = 1
ptile   = 99.9 # (%)
lfbctype= ["nn","wn"]
#lnhour  = [1,6,24]
#lnhour  = [1,3,6,12,24]
lnhour  = [1,3,6,12,24]
#lnhour  = [24]
#ltag    = ["nbcot","nbcot","tc","c","fbc","nbc","ot","o.tc","o.c","o.fbc","o.nbc","TCF","TCFC","TCB","TCBC"]
ltag    = ["tc","c","fbc","nbc","ot"]
#ltag    = ["nbcot"]
thdura_c  = 48
thdura_tc = thdura_c
thnumrat  = 0.95

iyear_dat= 2001
eyear_dat= 2009
itime_dat = datetime.datetime(iyear_dat,1,1,0)
miss     = -9999.0
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

#-----------------------
thorog    = 1500   # [m]
miss      = -9999.0
miss_out  = -9999.0
miss_gpcp = -99999.
#---------------------
#---------------------
region    = "GLOB"
lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region)

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
for prtype,bstflag_tc, bstflag_f,season in \
   [[prtype,bstflag_tc,bstflag_f,season] for prtype in lprtype\
                                         for bstflag_tc in lbstflag_tc\
                                         for bstflag_f in lbstflag_f\
                                         for season in lseason]:
  #------------------
  sext = dext[prtype]

  #------------------
  for fbctype, tag, nhour in ret_lkeys(fbctypeflag=True, tagflag=True, nhourflag=True):
    #--- init  ------
    if prtype in ["GSMaP"]:
      ny,nx     = [120,360]
    elif prtype in ["GSMaP.dec"]:
      ny,nx     = [1200,3600]
    #----
    #----------------
    lyear = range(iyear, eyear+1)
    lmon  = ctrack_para.ret_lmon(season)
    for year, mon in [[year,mon] for year in lyear for mon in lmon]:
      #-- idir ------
      idir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/tagexpr/%s.c%02dh.tc%02dh"%(sresol, fbctype, thdura_c, thdura_tc)
      idir      = idir_root + "/%s.%04d-%04d.%s.%04d.%02d"%(prtype, iyear_dat, eyear_dat, season, year,mon)
  
      # plain ---
      name_plainnum = idir + "/num.%s.mov%02dhr.plain.%s"%(prtype,nhour,sext)
  
      # tagnum --
      name_tagnum  = idir + "/num.%s.%s.mov%02dhr.%05.2f.bsttc%04d.c%04d.f%04d.%s.%s"%(fbctype,prtype, nhour,ptile,dist_tc,dist_c,dist_f,tag,sext)
      # totnum -
      name_totnum  = idir + "/totalcount.%s.%s"%(prtype,sext)
      #----------
      iname = name_plainnum
      if os.path.exists(iname)==False:
        print "nofile", iname

      iname = name_tagnum
      if os.path.exists(iname)==False:
        print "nofile", iname

      iname = name_totnum
      if os.path.exists(iname)==False:
        print "nofile", iname


