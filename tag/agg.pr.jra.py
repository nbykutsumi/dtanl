from tag_fsub import *
from numpy import *
import ctrack_para, ctrack_func, ctrack_fig, chart_para
import calendar
import gsmap_func
import datetime
import os
#---------------------------
#singletime = True
singletime = False
#calcflag   = True
calcflag   = False
lbstflag    = [True,False]
#lbstflag   = [False]
iyear   = 2001
eyear   = 2004
#lseason = ["DJF", "JJA","ALL"]
#lseason = ["NDJFMA","JJASON"]
lseason = ["NDJFMA","JJASON","DJF","JJA","ALL"]
#lseason = [1]
iday    = 1
#--------------------------------
#lprtype  = ["JRA","GPCP1DD"]
lprtype  = ["GSMaP"]
#lprtype   = ["JRA"]
#--------------------------------

dist_tc = 500 #[km]
dist_c  = 1000 #[km]
dist_f  = 500 #[km]
nx,ny   =[360,180]

thorog    = 1500   # [m]
miss      = -9999.0
miss_out  = -9999.0
miss_gpcp = -99999.

#---------------------
region    = "GLOB"
lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region)
#---------------------
for prtype in lprtype:
  for bstflag in lbstflag:
    #-- TC type ----------
    if bstflag ==True:
      tctype = "bst"
    else:
      tctype = ""
    #---------------------
    if prtype in ["GPCP1DD"]:
      coef       = 1.0/(60*60*24.0)
    else:
      coef       = 1.0
    #--- tag dir_root -------------------
    tagdir_root = "/media/disk2/out/JRA25/sa.one/6hr/tag"
    #--- precipitation directory & timestep-----
    if prtype == "GSMaP":
      prdir_root  = "/media/disk2/data/GSMaP/sa.one/3hr/ptot"
      timestep    = "3hr"
    
    elif prtype == "JRA":
      prdir_root  = "/media/disk2/data/JRA25/sa.one/6hr/PR"
      timestep    = "6hr"
    
    elif prtype == "GPCP1DD":
      prdir_root  = "/media/disk2/data/GPCP1DD/v1.2/1dd"
      timestep    = "day"
    
    elif prtype == "APHRO_MA":
      prdir_root  = "/media/disk2/data/aphro/MA/sa.one"
      timestep    = "day"
    #--- lhour -----------------------
    if timestep == "day":
      lhour = [0]
    elif timestep == "6hr":
      lhour = [0,6,12,18]
    elif timestep == "3hr":
      lhour = [0,3,6,9,12,15,18,21]
    
    #--- corresponding tag time ------
    def ret_lhtag_inc(timestep, hour):
      if timestep == "day":
        lhtag_inc = [0,6,12,18]
      elif timestep == "6hr":
        lhtag_inc = [0, -6]
      elif timestep == "3hr":
        if hour in  [0,6,12,18]:
          lhtag_inc = [0]
        elif hour in [3,9,15,21]:
          lhtag_inc = [-3]
      #
      return lhtag_inc
    
    #-- orog ------------------------
    orogname = "/media/disk2/data/JRA25/sa.one/const/topo/topo.sa.one"
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
      if calcflag == True:
        #-----------------
        lmon = ctrack_para.ret_lmon(season)
        #--------------------------------
        a2one    = ones([ny,nx],float32)
        a2zero   = zeros([ny,nx],float32)
        ##
        a2pr_all = a2zero
        a2pr_tc  = a2zero
        a2pr_c   = a2zero
        a2pr_fbc = a2zero
        a2pr_nbc = a2zero
        a2pr_ot  = a2zero
        #--------------------------------
        for year in range(iyear, eyear+1):
          #-----------------
          for mon in lmon:
            #-- prdir ---
            if prtype in ["GSMaP", "JRA"]:
              prdir    = prdir_root + "/%04d%02d"%(year, mon)
            elif prtype in ["GPCP1DD"]:
              prdir    = prdir_root + "/%04d"%(year)
            #--------------------
            eday  = calendar.monthrange(year,mon)[1]
            #--------------------
            if singletime ==True:
              eday = iday
              lhour = [0]
            #-- leap year -------
            if (mon==2)&(eday==29):
              eday = 28
            #--------------------
            for day in range(iday, eday+1):
              print prtype, season, year, mon, day
              for hour in lhour:
                #-- prec name ----
                if prtype == "GSMaP":
                  prname    = prdir    + "/gsmap_mvk.3rh.%04d%02d%02d.%02d00.v5.222.1.sa.one"%(year, mon, day, hour)
                elif prtype == "JRA":
                  prname    = prdir    + "/fcst_phy2m.PR.%04d%02d%02d%02d.sa.one"%(year, mon, day, hour)
                elif prtype == "GPCP1DD":
                  prname    = prdir    + "/gpcp_1dd_v1.2_p1d.%04d%02d%02d.bn"%(year, mon, day)
        
                #-- load prec ----
                if prtype   == "GSMaP":
                  a2pr      = fromfile(prname,  float32).reshape(120, 360)
                  a2pr      = gsmap_func.gsmap2global_one(a2pr, miss_out)
                elif prtype == "JRA":
                  a2pr      = fromfile(prname,  float32).reshape(ny, nx)
                elif prtype == "GPCP1DD":
                  a2pr      = flipud(fromfile(prname,  float32).reshape(ny, nx))
                  a2pr      = ma.masked_equal(a2pr, miss_gpcp).filled(0.0)
        
                #*****************************
                # load corresponding tags 
                #-----------------------------
                lhtag_inc   = ret_lhtag_inc(timestep, hour)
                now   = datetime.datetime(year, mon, day, hour)
                #------------------
                a2tag_tc    = a2zero
                a2tag_c     = a2zero
                a2tag_fbc   = a2zero
                a2tag_nbc   = a2zero
                a2tag_ot    = a2zero
                #------------------ 
                for htag_inc in lhtag_inc:
                  dhour       = datetime.timedelta(hours = htag_inc)
                  target      = now + dhour
                  year_target = target.year
                  mon_target  = target.month
                  day_target  = target.day
                  hour_target = target.hour
                  #-- tag name ---
                  tagdir   = tagdir_root + "/%04d%02d"%(year_target, mon_target)
                  tagname  = tagdir + "/tag.%stc%02d.c%02d.f%02d.%04d.%02d.%02d.%02d.sa.one"%(tctype, dist_tc/100, dist_c/100, dist_f/100, year_target,mon_target,day_target,hour_target)
        
                  if not os.access(tagname, os.F_OK):
                    print "AAAA"
                    print "nofile", tagname
                    if (year==iyear)&(mon==1)&(day==1):
                      continue
                    elif (year==eyear)&(mon==12)&(day==eday):
                      continue
                  #-- load -------
                  a2tag     = fromfile(tagname, int32).reshape(180,360)
                  lout      = tag_fsub.solve_tag_4type(a2tag.T)
                  a2tag_tc  = a2tag_tc  + array(lout[0].T, float32)
                  a2tag_c   = a2tag_c   + array(lout[1].T, float32)
                  a2tag_fbc = a2tag_fbc + array(lout[2].T, float32)
                  a2tag_nbc = a2tag_nbc + array(lout[3].T, float32)
                  a2tag_ot  = a2tag_ot  + ma.masked_where(a2tag !=0, a2one).filled(0.0)
                ##
                a2tag_tc  = a2tag_tc  / len(lhtag_inc)
                a2tag_c   = a2tag_c   / len(lhtag_inc)
                a2tag_fbc = a2tag_fbc / len(lhtag_inc)
                a2tag_nbc = a2tag_nbc / len(lhtag_inc)
                a2tag_ot  = a2tag_ot  / len(lhtag_inc)
                ##
                a2tag_all = a2tag_tc + a2tag_c + a2tag_fbc + a2tag_nbc + a2tag_ot
                ##
                a2tag_tc  = a2tag_tc  / a2tag_all
                a2tag_c   = a2tag_c   / a2tag_all
                a2tag_fbc = a2tag_fbc / a2tag_all
                a2tag_nbc = a2tag_nbc / a2tag_all
                a2tag_ot  = a2tag_ot  / a2tag_all
                ##*****************************
                # weight precipitation
                #-----------------------------
                a2prtmp_tc   = ma.masked_less(a2pr,0.0).filled(0.0) * a2tag_tc
                a2prtmp_c    = ma.masked_less(a2pr,0.0).filled(0.0) * a2tag_c
                a2prtmp_fbc  = ma.masked_less(a2pr,0.0).filled(0.0) * a2tag_fbc
                a2prtmp_nbc  = ma.masked_less(a2pr,0.0).filled(0.0) * a2tag_nbc
                a2prtmp_ot   = ma.masked_less(a2pr,0.0).filled(0.0) * a2tag_ot
                #*****************************
                # sum precipitation
                #-----------------------------
                a2pr_all     = a2pr_all + a2pr
                a2pr_tc      = a2pr_tc  + a2prtmp_tc
                a2pr_c       = a2pr_c   + a2prtmp_c
                a2pr_fbc     = a2pr_fbc + a2prtmp_fbc
                a2pr_nbc     = a2pr_nbc + a2prtmp_nbc
                a2pr_ot      = a2pr_ot  + a2prtmp_ot
        #-------------------------------------
        a2frac_tc  = (ma.masked_where(a2pr_all==0.0, a2pr_tc ) / a2pr_all).filled(0.0)
        a2frac_c   = (ma.masked_where(a2pr_all==0.0, a2pr_c  ) / a2pr_all).filled(0.0)
        a2frac_fbc = (ma.masked_where(a2pr_all==0.0, a2pr_fbc) / a2pr_all).filled(0.0)
        a2frac_nbc = (ma.masked_where(a2pr_all==0.0, a2pr_nbc) / a2pr_all).filled(0.0)
        a2frac_ot  = (ma.masked_where(a2pr_all==0.0, a2pr_ot ) / a2pr_all).filled(0.0)

        #*** mask for GSMaP *********************
        if prtype == "GSMaP":
          a2frac_tc  = ma.masked_where(a2shade_gsmap==miss, a2frac_tc ).filled(miss)
          a2frac_c   = ma.masked_where(a2shade_gsmap==miss, a2frac_c  ).filled(miss)
          a2frac_fbc = ma.masked_where(a2shade_gsmap==miss, a2frac_fbc).filled(miss)
          a2frac_nbc = ma.masked_where(a2shade_gsmap==miss, a2frac_nbc).filled(miss)
          a2frac_ot  = ma.masked_where(a2shade_gsmap==miss, a2frac_ot ).filled(miss)
      
        #****************************************
        # write to file
        #----------------------------------------
        sodir_root = "/media/disk2/out/JRA25/sa.one/6hr/tagpr"
        sodir      = sodir_root + "/%04d-%04d/%s"%(iyear, eyear, season)
        ctrack_func.mk_dir(sodir)
        sname_tc   =  sodir  + "/frac.%stc%02d.c%02d.f%02d.%04d-%04d.%s.%s.tc.sa.one" %(tctype, dist_tc/100, dist_c/100, dist_f/100, iyear, eyear, season, prtype)
        sname_c    =  sodir  + "/frac.%stc%02d.c%02d.f%02d.%04d-%04d.%s.%s.c.sa.one"  %(tctype, dist_tc/100, dist_c/100, dist_f/100, iyear, eyear, season, prtype)
        sname_fbc  =  sodir  + "/frac.%stc%02d.c%02d.f%02d.%04d-%04d.%s.%s.fbc.sa.one"%(tctype, dist_tc/100, dist_c/100, dist_f/100, iyear, eyear, season, prtype)
        sname_nbc  =  sodir  + "/frac.%stc%02d.c%02d.f%02d.%04d-%04d.%s.%s.nbc.sa.one"%(tctype, dist_tc/100, dist_c/100, dist_f/100, iyear, eyear, season, prtype)
        sname_ot   =  sodir  + "/frac.%stc%02d.c%02d.f%02d.%04d-%04d.%s.%s.ot.sa.one" %(tctype, dist_tc/100, dist_c/100, dist_f/100, iyear, eyear, season, prtype)
        ##
        a2frac_tc.tofile(sname_tc)
        a2frac_c.tofile(sname_c)
        a2frac_fbc.tofile(sname_fbc)
        a2frac_nbc.tofile(sname_nbc)
        a2frac_ot.tofile(sname_ot)
    
    
      #****************************************
      # draw figure
      #----------------------------------------
      ltag       = ["tc","c","fbc","nbc","ot"]
      sodir_root = "/media/disk2/out/JRA25/sa.one/6hr/tagpr"
      sodir      = sodir_root + "/%04d-%04d/%s"%(iyear, eyear, season)
      figdir     = sodir + "/pict"
      ctrack_func.mk_dir(figdir)
      dsname     = {}
      dfigname   = {}
      da2frac    = {}
      for tag in ltag:
        #-- name --
        dsname[tag]   =  sodir  + "/frac.%stc%02d.c%02d.f%02d.%04d-%04d.%s.%s.%s.sa.one"%(tctype, dist_tc/100, dist_c/100, dist_f/100, iyear, eyear, season, prtype, tag)
        dfigname[tag] =  figdir + "/frac.%stc%02d.c%02d.f%02d.%04d-%04d.%s.%s.%s.png"%(tctype, dist_tc/100, dist_c/100, dist_f/100, iyear, eyear, season, prtype, tag)
    
        #-- settings --
        if tag in ["tc"]:
          bnd    = [5,10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]
          cbarname = figdir + "/frac.cbar.tc.png"
        else:
          bnd    = [5,10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]
          cbarname = figdir + "/frac.cbar.png"
        #
        if tag =="tc":
          stitle   = "frac %s%s: season:%s %s %04d-%04d %stc%02d c%02d f%02d"%(tctype, tag, season, prtype, iyear, eyear, tctype, dist_tc/100, dist_c/100, dist_f/100)
        else:
          stitle   = "frac %s: season:%s %s %04d-%04d %stc%02d c%02d f%02d"%(tag, season, prtype, iyear, eyear, tctype, dist_tc/100, dist_c/100, dist_f/100)
        mycm     = "Spectral_r"
        datname  = dsname[tag]
        figname  = dfigname[tag]
    
        #-- loaad -----
        a2figdat = fromfile(datname, float32).reshape(ny,nx)
        a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
    
        #-- draw ------
        ctrack_fig.mk_pict_saone_reg(a2figdat, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon)
        print figname
   



