from tag_fsub import *
from numpy import *
import ctrack_para, ctrack_func, ctrack_fig, chart_para
import calendar
import gsmap_func
import datetime
import os
#---------------------------
figflag   = True
#figflag   = False
#singletime = True
singletime = False
lbstflag_tc = ["bst"]
#lbstflag_tc = [""]
bstflag_f = ""

sresol  = "anl_p"
#iyear   = 1997
#eyear   = 2012
#iyear,eyear = 2001,2004
iyear,eyear = 1997,2011
#lseason = ["ALL",1,2,3,4,5,6,7,8,9,10,11,12]
#lseason = ["DJF", "JJA","ALL",1,2,3,4,5,6,7,8,9,10,11,12]
#lseason = ["NDJFMA","JJASON"]
#lseason = ["NDJFMA","JJASON","DJF","JJA","ALL"]
lseason = ["ALL"]
iday    = 1
#--------------------------------
#lprtype  = ["JRA","GPCP1DD"]
#lprtype  = ["GSMaP"]
lprtype   = ["GPCP1DD"]
#--------------------------------
#- dist ----
lldist1   = array([[500,1000,500],[750,1000,500],[1000,1000,500],[1250,1000,500],[1500,1000,500]])*1000.0
lldist2   = array([[1000,500,500],[1000,750,500],[1000,1250,500],[1000,1500,500]])*1000.0
lldist3   = array([[1000,1000,250],[1000,1000,375],[1000,1000,625],[1000,1000,750]])*1000.0
#lldist    = vstack( [lldist1, lldist2, lldist3] )

lldist    = array([[1000,1000,500]])*1000.0
#-----------
nx,ny   =[360,180]

thorog    = 1500   # [m]
miss      = -9999.0
miss_out  = -9999.0
miss_gpcp = -99999.

thdura_c  = 48
thdura_tc = thdura_c
#thdura_c  = 72
#thdura_tc = thdura_c

#---------------------
region    = "GLOB"
lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region)
#---------------------
for prtype in lprtype:
  for bstflag_tc in lbstflag_tc:
    for ldist in lldist:
      dist_tc, dist_c, dist_f = ldist
      #---------------------
      if prtype in ["GPCP1DD"]:
        coef       = 1.0/(60*60*24.0)
      else:
        coef       = 1.0
      #--- precipitation directory & timestep-----
      if prtype == "GSMaP":
        prdir_root  = "/media/disk2/data/GSMaP/sa.one/3hr/ptot"
        timestep    = "3hr"
      
      elif prtype == "JRA":
        prdir_root  = "/media/disk2/data/JRA25/sa.one.anl_p/6hr/PR"
        timestep    = "6hr"
      
      elif prtype == "GPCP1DD":
        prdir_root  = "/media/disk2/data/GPCP1DD/v1.2/1dd"
        timestep    = "day"
      
      elif prtype == "APHRO_MA":
        prdir_root  = "/media/disk2/data/aphro/MA/sa.one"
        timestep    = "day"
      
      #-- orog ------------------------
      orogname = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
      a2orog   = fromfile(orogname, float32).reshape(ny,nx)
      
      a2shade  = ma.masked_where(a2orog >thorog, a2orog).filled(miss)
      #-- for GSMaP ----
      if prtype =="GSMaP":
        a2shade[:30,:]  = miss
        a2shade[150:,:] = miss
        #----
        a2shade_gsmap         = zeros([ny,nx],float32)
        a2shade_gsmap[:30,:]  = miss
        a2shade_gsmap[150:,:] = miss 
      #***************************************
      for season in lseason:
        #-----------------
        lmon = ctrack_para.ret_lmon(season)
        #--------------------------------
        a2one    = ones([ny,nx],float32)
        a2zero   = zeros([ny,nx],float32)
        #--------------------------------
        a2pr_all   = a2zero.copy()
        a2pr_tc    = a2zero.copy()
        a2pr_c     = a2zero.copy()
        a2pr_fbc   = a2zero.copy()
        a2pr_nbc   = a2zero.copy()
        a2pr_ot    = a2zero.copy()
        #
        a2pr_te    = a2zero.copy()
        a2pr_tf    = a2zero.copy()
        a2pr_ef    = a2zero.copy()
        a2pr_tef   = a2zero.copy()
        #
        a2prwn_all = a2zero.copy()
        a2prwn_tc  = a2zero.copy()
        a2prwn_c   = a2zero.copy()
        a2prwn_fbc = a2zero.copy()
        a2prwn_nbc = a2zero.copy()
        a2prwn_ot  = a2zero.copy()
  
        #-----------------
        nmon = 0
        for year in range(iyear, eyear+1):
          #-----------------
          for mon in lmon:
            nmon = nmon + 1
            print year,mon
            #-----------------------------
            sidir_root   = "/media/disk2/out/JRA25/sa.one.%s/6hr/tagpr/c%02dh.tc%02dh.%stc%04d.c%04d.%sf%04d"%(sresol, thdura_c, thdura_tc, bstflag_tc, dist_tc/1000.0, dist_c/1000.0, bstflag_f, dist_f/1000.0)
            sidirwn_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/tagpr/wn.c%02dh.tc%02dh.%stc%04d.c%04d.%sf%04d"%(sresol, thdura_c, thdura_tc, bstflag_tc, dist_tc/1000.0, dist_c/1000.0, bstflag_f, dist_f/1000.0)


            sidir        = sidir_root   + "/%04d%02d"%(year, mon)
            sidirwn      = sidirwn_root + "/%04d%02d"%(year, mon)
            ctrack_func.mk_dir(sidir)
            ctrack_func.mk_dir(sidirwn)
  
            sname_all  =  sidir  + "/pr.plain.%04d.%02d.%s.sa.one" %(year, mon, prtype)
            sname_tc   =  sidir  + "/pr.tc.%04d.%02d.%s.sa.one" %(year, mon, prtype)
            sname_c    =  sidir  + "/pr.c.%04d.%02d.%s.sa.one"  %(year, mon, prtype)
            sname_fbc  =  sidir  + "/pr.fbc.%04d.%02d.%s.sa.one"%(year, mon, prtype)
            sname_ot   =  sidir  + "/pr.ot.%04d.%02d.%s.sa.one" %(year, mon, prtype)
 
  
            # wn:
            snamewn_all  =  sidirwn  + "/pr.wn.plain.%04d.%02d.%s.sa.one" %(year, mon, prtype)
            snamewn_tc   =  sidirwn  + "/pr.wn.tc.%04d.%02d.%s.sa.one" %(year, mon, prtype)
            snamewn_c    =  sidirwn  + "/pr.wn.c.%04d.%02d.%s.sa.one"  %(year, mon, prtype)
            snamewn_fbc  =  sidirwn  + "/pr.wn.fbc.%04d.%02d.%s.sa.one"%(year, mon, prtype)
            snamewn_nbc  =  sidirwn  + "/pr.wn.nbc.%04d.%02d.%s.sa.one"%(year, mon, prtype)
            snamewn_ot   =  sidirwn  + "/pr.wn.ot.%04d.%02d.%s.sa.one" %(year, mon, prtype)
 
            # overlap: baroclinic
            sname_te  =  sidir  + "/pr.te.%04d.%02d.%s.sa.one" %(year, mon, prtype)
            sname_tf  =  sidir  + "/pr.tf.%04d.%02d.%s.sa.one" %(year, mon, prtype)
            sname_ef    =  sidir  + "/pr.ef.%04d.%02d.%s.sa.one"  %(year, mon, prtype)
            sname_tef   =  sidir  + "/pr.tef.%04d.%02d.%s.sa.one"%(year, mon, prtype)
 
  
            #--- load --------------------
            a2prtmp_all    = fromfile(sname_all, float32).reshape(ny,nx)
            a2prtmp_tc     = fromfile(sname_tc , float32).reshape(ny,nx)
            a2prtmp_c      = fromfile(sname_c  , float32).reshape(ny,nx)
            a2prtmp_fbc    = fromfile(sname_fbc, float32).reshape(ny,nx)
            a2prtmp_ot     = fromfile(sname_ot , float32).reshape(ny,nx)
  
            # wn:
            a2prwntmp_all  = fromfile(snamewn_all, float32).reshape(ny,nx)
            a2prwntmp_tc   = fromfile(snamewn_tc , float32).reshape(ny,nx)
            a2prwntmp_c    = fromfile(snamewn_c  , float32).reshape(ny,nx)
            a2prwntmp_fbc  = fromfile(snamewn_fbc, float32).reshape(ny,nx)
            a2prwntmp_nbc  = fromfile(snamewn_nbc, float32).reshape(ny,nx)
            a2prwntmp_ot   = fromfile(snamewn_ot , float32).reshape(ny,nx)

            # overlap: baroclinic
  
            a2prtmp_te   = fromfile(sname_te, float32).reshape(ny,nx)
            a2prtmp_tf   = fromfile(sname_tf, float32).reshape(ny,nx)
            a2prtmp_ef   = fromfile(sname_ef, float32).reshape(ny,nx)
            a2prtmp_tef  = fromfile(sname_tef,float32).reshape(ny,nx)
            #-----------------------------
            a2pr_all     = a2pr_all + a2prtmp_all
            a2pr_tc      = a2pr_tc  + a2prtmp_tc
            a2pr_c       = a2pr_c   + a2prtmp_c
            a2pr_fbc     = a2pr_fbc + a2prtmp_fbc
            a2pr_ot      = a2pr_ot  + a2prtmp_ot
            # wn:
            a2prwn_all   = a2prwn_all + a2prwntmp_all
            a2prwn_tc    = a2prwn_tc  + a2prwntmp_tc
            a2prwn_c     = a2prwn_c   + a2prwntmp_c
            a2prwn_fbc   = a2prwn_fbc + a2prwntmp_fbc
            a2prwn_nbc   = a2prwn_nbc + a2prwntmp_nbc
            a2prwn_ot    = a2prwn_ot  + a2prwntmp_ot
  
            # overlap: baroclinic
            a2pr_te      = a2pr_te    + a2prtmp_te     
            a2pr_tf      = a2pr_tf    + a2prtmp_tf  
            a2pr_ef      = a2pr_ef    + a2prtmp_ef     
            a2pr_tef     = a2pr_tef   + a2prtmp_tef 
  
        #------- calc fraction ------------
        a2frac_tc    = (ma.masked_where(a2pr_all==0.0, a2pr_tc ) / a2pr_all).filled(0.0)
        a2frac_c     = (ma.masked_where(a2pr_all==0.0, a2pr_c  ) / a2pr_all).filled(0.0)
        a2frac_fbc   = (ma.masked_where(a2pr_all==0.0, a2pr_fbc) / a2pr_all).filled(0.0)
        a2frac_ot    = (ma.masked_where(a2pr_all==0.0, a2pr_ot ) / a2pr_all).filled(0.0)
  
        # wn:
        a2fracwn_tc  = (ma.masked_where(a2prwn_all==0.0, a2prwn_tc ) / a2prwn_all).filled(0.0)
        a2fracwn_c   = (ma.masked_where(a2prwn_all==0.0, a2prwn_c  ) / a2prwn_all).filled(0.0)
        a2fracwn_fbc = (ma.masked_where(a2prwn_all==0.0, a2prwn_fbc) / a2prwn_all).filled(0.0)
        a2fracwn_nbc = (ma.masked_where(a2prwn_all==0.0, a2prwn_nbc) / a2prwn_all).filled(0.0)
        a2fracwn_ot  = (ma.masked_where(a2prwn_all==0.0, a2prwn_ot ) / a2prwn_all).filled(0.0)
 
        # overlap: baroclinic
        a2frac_te    = (ma.masked_where(a2pr_all==0.0, a2pr_te ) / a2pr_all).filled(0.0)
        a2frac_tf    = (ma.masked_where(a2pr_all==0.0, a2pr_tf ) / a2pr_all).filled(0.0)
        a2frac_ef    = (ma.masked_where(a2pr_all==0.0, a2pr_ef ) / a2pr_all).filled(0.0)
        a2frac_tef   = (ma.masked_where(a2pr_all==0.0, a2pr_tef )/ a2pr_all).filled(0.0)
 
        #------- calc mean precip ------------
        a2pr_tc_mean    = a2pr_tc    / nmon
        a2pr_c_mean     = a2pr_c     / nmon
        a2pr_fbc_mean   = a2pr_fbc   / nmon
        a2pr_ot_mean    = a2pr_ot    / nmon
        a2pr_cf_mean    = (a2pr_c + a2pr_fbc) /nmon
        #
        a2prwn_tc_mean  = a2prwn_tc  / nmon
        a2prwn_c_mean   = a2prwn_c   / nmon
        a2prwn_fbc_mean = a2prwn_fbc / nmon
        a2prwn_nbc_mean = a2prwn_nbc / nmon
        a2prwn_ot_mean  = a2prwn_ot  / nmon
        #  
        a2pr_te_mean    = a2pr_te    / nmon
        a2pr_tf_mean    = a2pr_tf    / nmon
        a2pr_ef_mean    = a2pr_ef    / nmon
        a2pr_tef_mean   = a2pr_tef   / nmon
  
  
        #*** mask for GSMaP *********************
        if prtype == "GSMaP":
          a2frac_tc  = ma.masked_where(a2shade_gsmap==miss, a2frac_tc ).filled(miss)
          a2frac_c   = ma.masked_where(a2shade_gsmap==miss, a2frac_c  ).filled(miss)
          a2frac_fbc = ma.masked_where(a2shade_gsmap==miss, a2frac_fbc).filled(miss)
          a2frac_ot  = ma.masked_where(a2shade_gsmap==miss, a2frac_ot ).filled(miss)
  
          # wn:
          a2fracwn_tc  = ma.masked_where(a2shade_gsmap==miss, a2fracwn_tc ).filled(miss)
          a2fracwn_c   = ma.masked_where(a2shade_gsmap==miss, a2fracwn_c  ).filled(miss)
          a2fracwn_fbc = ma.masked_where(a2shade_gsmap==miss, a2fracwn_fbc).filled(miss)
          a2fracwn_nbc = ma.masked_where(a2shade_gsmap==miss, a2fracwn_nbc).filled(miss)
          a2fracwn_ot  = ma.masked_where(a2shade_gsmap==miss, a2fracwn_ot ).filled(miss)

          # overlap: baroclinic
          a2frac_te  = ma.masked_where(a2shade_gsmap==miss, a2frac_te ).filled(miss)
          a2frac_tf  = ma.masked_where(a2shade_gsmap==miss, a2frac_tf ).filled(miss)
          a2frac_ef  = ma.masked_where(a2shade_gsmap==miss, a2frac_ef ).filled(miss)
          a2frac_tef = ma.masked_where(a2shade_gsmap==miss, a2frac_tef ).filled(miss)
  
          #        
          a2pr_tc_mean  = ma.masked_where(a2shade_gsmap==miss, a2pr_tc_mean ).filled(miss)
          a2pr_c_mean   = ma.masked_where(a2shade_gsmap==miss, a2pr_c_mean  ).filled(miss)
          a2pr_fbc_mean = ma.masked_where(a2shade_gsmap==miss, a2pr_fbc_mean).filled(miss)
          a2pr_ot_mean  = ma.masked_where(a2shade_gsmap==miss, a2pr_ot_mean ).filled(miss)
  
          # wn:
          a2prwn_tc_mean  = ma.masked_where(a2shade_gsmap==miss, a2prwn_tc_mean ).filled(miss)
          a2prwn_c_mean   = ma.masked_where(a2shade_gsmap==miss, a2prwn_c_mean  ).filled(miss)
          a2prwn_fbc_mean = ma.masked_where(a2shade_gsmap==miss, a2prwn_fbc_mean).filled(miss)
          a2prwn_nbc_mean = ma.masked_where(a2shade_gsmap==miss, a2prwn_nbc_mean).filled(miss)
          a2prwn_ot_mean  = ma.masked_where(a2shade_gsmap==miss, a2prwn_ot_mean ).filled(miss)

          # overlap: baroclinic
          a2pr_te_mean  = ma.masked_where(a2shade_gsmap==miss, a2pr_te_mean ).filled(miss)
          a2pr_tf_mean  = ma.masked_where(a2shade_gsmap==miss, a2pr_tf_mean ).filled(miss)
          a2pr_ef_mean  = ma.masked_where(a2shade_gsmap==miss, a2pr_ef_mean ).filled(miss)
          a2pr_tef_mean  = ma.masked_where(a2shade_gsmap==miss, a2pr_tef_mean ).filled(miss)
        
        #****************************************
        # write to file
        #----------------------------------------
        sodir_root = sidir_root
        sodir      = sodir_root + "/%04d-%04d.%s"%(iyear, eyear, season)
        ctrack_func.mk_dir(sodir)
        #--  
        sname_tc   =  sodir  + "/frac.%04d-%04d.%s.%s.tc.sa.one" %(iyear, eyear, season, prtype)
        sname_c    =  sodir  + "/frac.%04d-%04d.%s.%s.c.sa.one"  %(iyear, eyear, season, prtype)
        sname_fbc  =  sodir  + "/frac.%04d-%04d.%s.%s.fbc.sa.one"%(iyear, eyear, season, prtype)
        sname_ot   =  sodir  + "/frac.%04d-%04d.%s.%s.ot.sa.one" %(iyear, eyear, season, prtype)
        sname_cf   =  sodir  + "/frac.%04d-%04d.%s.%s.cf.sa.one" %(iyear, eyear, season, prtype)
        #--
        sname_te   =  sodir  + "/frac.%04d-%04d.%s.%s.te.sa.one" %(iyear, eyear, season, prtype)
        sname_tf   =  sodir  + "/frac.%04d-%04d.%s.%s.tf.sa.one" %(iyear, eyear, season, prtype)
        sname_ef   =  sodir  + "/frac.%04d-%04d.%s.%s.ef.sa.one" %(iyear, eyear, season, prtype)
        sname_tef   =  sodir  + "/frac.%04d-%04d.%s.%s.tef.sa.one" %(iyear, eyear, season, prtype)

        #
        spr_tc     =  sodir  + "/pr.tc.%04d-%04d.%s.%s.sa.one" %(iyear, eyear, season, prtype)
        spr_c      =  sodir  + "/pr.c.%04d-%04d.%s.%s.sa.one" %(iyear, eyear, season, prtype)
        spr_fbc    =  sodir  + "/pr.fbc.%04d-%04d.%s.%s.sa.one" %(iyear, eyear, season, prtype)
        spr_ot     =  sodir  + "/pr.ot.%04d-%04d.%s.%s.sa.one" %(iyear, eyear, season, prtype)
        spr_cf     =  sodir  + "/pr.cf.%04d-%04d.%s.%s.sa.one" %(iyear, eyear, season, prtype)

        #--
        spr_te     =  sodir  + "/pr.te.%04d-%04d.%s.%s.sa.one" %(iyear, eyear, season, prtype)
        spr_tf     =  sodir  + "/pr.tf.%04d-%04d.%s.%s.sa.one" %(iyear, eyear, season, prtype)
        spr_ef     =  sodir  + "/pr.ef.%04d-%04d.%s.%s.sa.one" %(iyear, eyear, season, prtype)
        spr_tef    =  sodir  + "/pr.tef.%04d-%04d.%s.%s.sa.one" %(iyear, eyear, season, prtype)
  
        # wn:
        sodirwn_root = sidirwn_root
        sodirwn      = sodirwn_root + "/%04d-%04d.%s"%(iyear, eyear, season)
        ctrack_func.mk_dir(sodirwn)
  
        snamewn_tc   =  sodirwn  + "/frac.wn.%04d-%04d.%s.%s.tc.sa.one" %(iyear, eyear, season, prtype)
        snamewn_c    =  sodirwn  + "/frac.wn.%04d-%04d.%s.%s.c.sa.one"  %(iyear, eyear, season, prtype)
        snamewn_fbc  =  sodirwn  + "/frac.wn.%04d-%04d.%s.%s.fbc.sa.one"%(iyear, eyear, season, prtype)
        snamewn_nbc  =  sodirwn  + "/frac.wn.%04d-%04d.%s.%s.nbc.sa.one"%(iyear, eyear, season, prtype)
        snamewn_ot   =  sodirwn  + "/frac.wn.%04d-%04d.%s.%s.ot.sa.one" %(iyear, eyear, season, prtype)
        #
        sprwn_tc     =  sodirwn  + "/pr.wn.tc.%04d-%04d.%s.%s.sa.one" %(iyear, eyear, season, prtype)
        sprwn_c      =  sodirwn  + "/pr.wn.c.%04d-%04d.%s.%s.sa.one" %(iyear, eyear, season, prtype)
        sprwn_fbc    =  sodirwn  + "/pr.wn.fbc.%04d-%04d.%s.%s.sa.one" %(iyear, eyear, season, prtype)
        sprwn_nbc    =  sodirwn  + "/pr.wn.nbc.%04d-%04d.%s.%s.sa.one" %(iyear, eyear, season, prtype)
        sprwn_ot     =  sodirwn  + "/pr.wn.ot.%04d-%04d.%s.%s.sa.one" %(iyear, eyear, season, prtype)
  
        ##
        a2frac_tc .tofile(sname_tc)
        a2frac_c  .tofile(sname_c)
        a2frac_fbc.tofile(sname_fbc)
        a2frac_ot .tofile(sname_ot)
        (a2frac_c + a2frac_fbc) .tofile(sname_cf)

        print sname_tc
        ##
        a2frac_te .tofile(sname_te)
        a2frac_tf .tofile(sname_tf)
        a2frac_ef .tofile(sname_ef)
        a2frac_tef.tofile(sname_tef)

        ##
        a2pr_tc_mean.tofile(spr_tc)
        a2pr_c_mean.tofile(spr_c)
        a2pr_fbc_mean.tofile(spr_fbc)
        a2pr_ot_mean.tofile(spr_ot)
        a2pr_cf_mean.tofile(spr_cf)
        ##
        a2pr_te_mean .tofile(spr_te)
        a2pr_tf_mean .tofile(spr_tf)
        a2pr_ef_mean .tofile(spr_ef)
        a2pr_tef_mean.tofile(spr_tef)
 
        ## wn:
        a2fracwn_tc.tofile(snamewn_tc)
        a2fracwn_c.tofile(snamewn_c)
        a2fracwn_fbc.tofile(snamewn_fbc)
        a2fracwn_nbc.tofile(snamewn_nbc)
        a2fracwn_ot.tofile(snamewn_ot)
        ##
        a2prwn_tc_mean.tofile(sprwn_tc)
        a2prwn_c_mean.tofile(sprwn_c)
        a2prwn_fbc_mean.tofile(sprwn_fbc)
        a2prwn_nbc_mean.tofile(sprwn_nbc)
        a2prwn_ot_mean.tofile(sprwn_ot)
  
        #******************************************
        # draw figures
        #****************************************** 
        if figflag ==False:
          continue
        #------------

        #lftype     = ["",".wn"]
        lftype     = [""]
  
        for ftype in lftype:
          #****************************************
          # draw figure : fraction
          #----------------------------------------
          if ftype == "":
            ltag       = ["tc","c","fbc","ot", "cf"] + ["te","tf","ef","tef"]
            sodir      = sodir_root + "/%04d-%04d.%s"%(iyear, eyear, season)
          elif ftype == ".wn":
            ltag       = ["tc","c","fbc","ot", "nbc", "nbcot"]
            sodir      = sodirwn_root + "/%04d-%04d.%s"%(iyear, eyear, season)
          #--
          figdir     = sodir + "/pict"
          ctrack_func.mk_dir(figdir)
          #----------------------------------------
          for tag in ltag:
  
            #-- name --
            if tag == "nbcot": 
              sname_ot =  sodir  + "/frac%s.%04d-%04d.%s.%s.%s.sa.one" %(ftype, iyear, eyear, season, prtype, "ot")
              sname_nbc=  sodir  + "/frac%s.%04d-%04d.%s.%s.%s.sa.one" %(ftype, iyear, eyear, season, prtype, "nbc")
            else:
              sname    =  sodir  + "/frac%s.%04d-%04d.%s.%s.%s.sa.one" %(ftype, iyear, eyear, season, prtype, tag)
            figname    =  figdir + "/frac%s.%04d-%04d.%s.%s.%s.png"%(ftype, iyear, eyear, season, prtype, tag)
        
            #-- settings --
            if tag in ["tc"]:
              bnd    = [5,10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]
              cbarname = figdir + "/frac.cbar.tc.png"
            else:
              bnd    = [5,10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]
              cbarname = figdir + "/frac.cbar.png"
            #
            if tag =="tc":
              stitle   = "frac %s %s%s: season:%s %s %04d-%04d %stc%04d c%04d f%04d"%(ftype, bstflag_tc, tag, season, prtype, iyear, eyear, bstflag_tc, dist_tc/1000., dist_c/1000., dist_f/1000.)
            else:
              stitle   = "frac %s %s: season:%s %s %04d-%04d %stc%04d c%04d f%04d"%(ftype, tag, season, prtype, iyear, eyear, bstflag_tc, dist_tc/1000., dist_c/1000., dist_f/1000.)
            mycm     = "Spectral_r"
        
            #-- load -----
            if tag == "nbcot":
              a2figdat_ot  = fromfile(sname_ot , float32).reshape(ny,nx)
              a2figdat_nbc = fromfile(sname_nbc, float32).reshape(ny,nx)
              a2figdat_ot  = ma.masked_equal(a2figdat_ot, miss).filled(0.0) * 100.0
              a2figdat_nbc = ma.masked_equal(a2figdat_nbc, miss).filled(0.0) * 100.0
              a2figdat     = a2figdat_ot + a2figdat_nbc
            else:
              a2figdat = fromfile(sname, float32).reshape(ny,nx)
              a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
        
            #-- draw ------
            ctrack_fig.mk_pict_saone_reg(a2figdat, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon)
            print figname
       
    
          #****************************************
          # draw figure : precip mean
          #----------------------------------------
          if ftype == "":
            ltag       = ["tc","c","fbc","ot","cf"] + ["te","tf","ef","tef"]
            sodir      = sodir_root + "/%04d-%04d.%s"%(iyear, eyear, season)
          elif ftype == ".wn":
            ltag       = ["tc","c","fbc","ot","nbc","nbcot"]
            sodir      = sodirwn_root + "/%04d-%04d.%s"%(iyear, eyear, season)
          #--
          figdir     = sodir + "/pict"
          ctrack_func.mk_dir(figdir)
  
          #----------------------------------------
          for tag in ltag:
            #-- name --
            sname   =  sodir  + "/pr%s.%s.%04d-%04d.%s.%s.sa.one" %(ftype, tag, iyear, eyear, season, prtype)
            figname    =  figdir + "/pr%s.%04d-%04d.%s.%s.%s.png"%(ftype, iyear, eyear, season, prtype, tag)
        
            #-- settings --
            #bnd    = [10,30,50,100,150,200]
            bnd    = [10,40,70,100,130,160,190]
            cbarname = figdir + "/pr.cbar.png"
            #
            if tag =="tc":
              stitle   = "mm/month %s %s%s: season:%s %s %04d-%04d %stc%02d c%02d f%02d"%(ftype, bstflag_tc, tag, season, prtype, iyear, eyear, bstflag_tc, dist_tc/1000., dist_c/1000., dist_f/1000.)
            else:
              stitle   = "mm/month %s %s: season:%s %s %04d-%04d %stc%02d c%02d f%02d"%(ftype, tag, season, prtype, iyear, eyear, bstflag_tc, dist_tc/1000., dist_c/1000., dist_f/1000.)
            mycm     = "jet_r"
        
            #-- load -----
            a2figdat = fromfile(sname, float32).reshape(ny,nx)
            a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0)
    
            #-- convert unit: mm/sec --> mm/season
            nsec  = ctrack_para.ret_totaldays(iyear, eyear, season) *24.*60.*60.
            a2figdat = a2figdat * nsec / nmon
    
            #-- draw ------
            ctrack_fig.mk_pict_saone_reg(a2figdat, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon)
            print figname
       
          #****************************************
          # draw figure : precip mean nbc + ot
          #----------------------------------------
          if ftype==".wn":
            tag        = "nbcot"
            sodir      = sodirwn_root + "/%04d-%04d.%s"%(iyear, eyear, season)
            figdir     = sodir + "/pict"
            ctrack_func.mk_dir(figdir)
            #-- name --
            sname_ot   =  sodir  + "/pr%s.ot.%stc%02d.c%02d.f%02d.%04d-%04d.%s.%s.sa.one" %(ftype, bstflag_tc, dist_tc, dist_c, dist_f, iyear, eyear, season, prtype)
            sname_nbc  =  sodir  + "/pr%s.nbc.%stc%02d.c%02d.f%02d.%04d-%04d.%s.%s.sa.one" %(ftype, bstflag_tc, dist_tc, dist_c, dist_f, iyear, eyear, season, prtype)
            figname    =  figdir + "/pr%s.%stc%02d.c%02d.f%02d.%04d-%04d.%s.%s.%s.png"%(ftype, bstflag_tc, dist_tc, dist_c, dist_f, iyear, eyear, season, prtype, tag)
          
            #-- settings --
            #bnd    = [10,30,50,100,150,200]
            bnd    = [10,40,70,100,130,160,190]
            cbarname = figdir + "/pr.cbar.png"
            #
            stitle   = "mm/month %s %s: season:%s %s %04d-%04d %stc%02d c%02d f%02d"%(ftype, tag, season, prtype, iyear, eyear, bstflag_tc, dist_tc, dist_c, dist_f)
            mycm     = "jet_r"
          
            #-- load -----
            a2figdat_ot = fromfile(sname_ot, float32).reshape(ny,nx)
            a2figdat_ot = ma.masked_equal(a2figdat_ot, miss).filled(0.0)
      
            a2figdat_nbc = fromfile(sname_nbc, float32).reshape(ny,nx)
            a2figdat_nbc = ma.masked_equal(a2figdat_nbc, miss).filled(0.0)
      
            a2figdat     = a2figdat_ot + a2figdat_nbc
            #-- convert unit: mm/sec --> mm/season
            nsec  = ctrack_para.ret_totaldays(iyear, eyear, season) *24.*60.*60.
            a2figdat = a2figdat * nsec / nmon
      
            #-- draw ------
            ctrack_fig.mk_pict_saone_reg(a2figdat, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon)
            print figname
       





