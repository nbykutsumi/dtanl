from tag_fsub import *
from gsmap_fsub import *
from numpy import *
import ctrack_para, ctrack_func, ctrack_fig, chart_para
import calendar
import gsmap_func
import datetime
import os, sys
#---------------------------
lbstflag_tc   = ["bst"]
#lbstflag_tc   = ["bst"]
#lbstflag_f    = ["bst.high","bst.type"]
lbstflag_f = [""]
#lprtype  = ["GSMaP"]
lprtype  = ["GSMaP.dec"]

dext    = {"GSMaP":"sa.one", "GSMaP.dec":"sa.dec"}

sresol  = "anl_p"
iyear   = 2001
eyear   = 2001
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
#lfbctype= ["nn","wn"]
lfbctype= ["nn"]
#lnhour  = [1,6,24]
lnhour  = [24]
#lnhour  = [1,3,6,12,24]
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
  sext  = dext[prtype]
  #------------------
  for fbctype, tag, nhour in ret_lkeys(fbctypeflag=True, tagflag=True, nhourflag=True):
    #--- init  ------
    if prtype in ["GSMaP"]:
      ny,nx     = [120,360]
    elif prtype in ["GSMaP.dec"]:
      ny,nx     = [1200,3600]
    #----
    a2tagnum    = zeros([ny,nx],float32)
    a2plainnum  = zeros([ny,nx],float32)
    a2totnum    = zeros([ny,nx],float32)
    #----------------
    lyear = range(iyear, eyear+1)
    lmon  = ctrack_para.ret_lmon(season)
    for year, mon in [[year,mon] for year in lyear for mon in lmon]:
      #-- idir ------
      idir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/tagexpr/%s.c%02dh.tc%02dh"%(sresol, fbctype, thdura_c, thdura_tc)
      idir      = idir_root + "/%s.%04d-%04d.%s.%04d.%02d"%(prtype, iyear_dat, eyear_dat, season, year,mon)
  
      # plain ---
      name_plainnum = idir + "/num.%s.mov%02dhr.plain.%s"%(prtype,nhour,sext)
      a2plainnum_tmp  = fromfile(name_plainnum,float32).reshape(ny,nx)
      a2plainnum_tmp  = ma.masked_equal(a2plainnum_tmp, miss).filled(0.0)
      a2plainnum      = a2plainnum + a2plainnum_tmp
  
      # tagnum --
      name_tagnum  = idir + "/num.%s.%s.mov%02dhr.%05.2f.bsttc%04d.c%04d.f%04d.%s.%s"%(fbctype,prtype, nhour,ptile,dist_tc,dist_c,dist_f,tag,sext)
      a2tagnum_tmp = fromfile(name_tagnum,float32).reshape(ny,nx)
      a2tagnum_tmp = ma.masked_equal(a2tagnum_tmp, miss).filled(0.0)
      a2tagnum     = a2tagnum + a2tagnum_tmp 
 
      # totnum -
      name_totnum  = idir + "/totalcount.%s.%s"%(prtype,sext)
      a2totnum_tmp = fromfile(name_totnum,float32).reshape(ny,nx)
      a2totnum     = a2totnum + a2totnum_tmp
    #-------------------
    # rfreq
    #-------------------
    a2tagnum  = ma.masked_equal(a2tagnum, miss)
    a2rfreq   = (ma.masked_where(a2plainnum <=0.0, a2tagnum)/a2plainnum).filled(miss)
    #--------------------
    # check obs times
    #--------------------
    a2rfreq = ma.masked_where(a2totnum < thnumrat*totalnum, a2rfreq)

    #--------------------
    # write to files
    #--------------------
    odir_root = idir_root
    odir      = odir_root + "/%s.%04d-%04d.%s"%(prtype, iyear_dat, eyear_dat, season)
    ctrack_func.mk_dir(odir)
  
    rfreqname = odir + "/rfreq.%s.%s.mov%02dhr.%05.2f.%stc%04d.c%04d.%sf%04d.%s.%s.%s"%(fbctype, prtype, nhour, ptile, bstflag_tc, dist_tc, dist_c, bstflag_f, dist_f,prtype,tag,sext)
    #--
    a2rfreq.tofile(rfreqname)
    print ""
    print rfreqname  

    #****************************************
    # draw figure
    #----------------------------------------
    figdir     = odir + "/pict"
    ctrack_func.mk_dir(figdir)
    figname    = figdir + "/rfreq.%s.%s.mov%02dhr.%05.2f.%stc%04d.c%04d.%sf%04d.GSMaP.%s.png"%(fbctype, prtype, nhour, ptile, bstflag_tc, dist_tc, dist_c, bstflag_f, dist_f,tag)
    #-- settings --
    bnd    = [5,10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]
    cbarname = figdir + "/rfreq.cbar.png"
    #
    stitle   = "rfreq %04.1f %s %s: season:%s %s %04d-%04d %stc%04d c%04d %sf%04d"%(ptile, fbctype, tag, season, prtype, iyear, eyear, bstflag_tc, dist_tc, dist_c, bstflag_f, dist_f)
    mycm     = "Spectral_r"

    #-- load -----
    totalnum = ctrack_para.ret_totaldays(iyear,eyear,season) * 24
    a2figdat = a2rfreq
    a2figdat = ma.masked_equal(a2figdat, miss) * 100.0
    a2figdat = ma.masked_equal(a2figdat, miss).filled(miss)
    if prtype in ["GSMaP", "GSMaP.dec"]:
      a2figdat = gsmap_func.gsmap2global(a2figdat, miss)
    #-- shade -----
    orogname = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
    a2orog   = fromfile(orogname, float32).reshape(180,360)
    #----
    if prtype == "GSMaP.dec":
      a2orog = gsmap_fsub.saone2dec(a2orog.T).T
    #----
    a2shade  = ma.masked_where(a2orog >thorog, a2orog).filled(miss)

    a2shade  = ma.masked_where(a2figdat==miss, a2shade).filled(miss)
    #-- draw ------
    ctrack_fig.mk_pict_saone_reg(a2figdat, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon)
    print figname






