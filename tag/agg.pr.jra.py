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
calcflag   = True
#calcflag   = True
lbstflag    = [True]
#lbstflag   = [False]

sresol  = "anl_p"
iyear   = 1997
eyear   = 2012
#lseason = ["DJF", "JJA","ALL"]
#lseason = ["NDJFMA","JJASON"]
#lseason = ["NDJFMA","JJASON","DJF","JJA","ALL"]
lseason = range(1,12+1)
#lseason = [1]
iday    = 1
#--------------------------------
#lprtype  = ["JRA","GPCP1DD"]
#lprtype  = ["GSMaP"]
lprtype   = ["GPCP1DD"]
#--------------------------------

dist_tc = 1000 #[km]
dist_c  = 1000 #[km]
dist_f  = 500 #[km]

## 80% area
#dist_tc    = 894 # [km]
#dist_c     = 894 # [km]
#dist_f     = 400 # [km]

## 120% area
#dist_tc    = 894 # [km]
#dist_c     = 894 # [km]
#dist_f     = 400 # [km]


nx,ny   =[360,180]

thdura_c    = 48
thdura_tc   = thdura_c

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
    #--- tag dir_root -------------------
    tagdir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/tag/c%02dh.tc%02dh"%(sresol, thdura_c, thdura_tc)
    #--- precipitation directory & timestep-----
    if prtype == "GSMaP":
      # unit (mm/s)
      prdir_root  = "/media/disk2/data/GSMaP/sa.one/3hr/ptot"
      timestep    = "3hr"
    
    elif prtype == "JRA":
      # unit (mm/s)
      prdir_root  = "/media/disk2/data/JRA25/sa.one.anl_p/6hr/PR"
      timestep    = "6hr"
    
    elif prtype == "GPCP1DD":
      # unit (mm/day)
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
      if calcflag == True:
        #-----------------
        lmon = ctrack_para.ret_lmon(season)
        #--------------------------------
        a2one    = ones([ny,nx],float32)
        a2zero   = zeros([ny,nx],float32)
        #--------------------------------
        for year in range(iyear, eyear+1):
          #-----------------
          for mon in lmon:
            print year,mon
            ##
            a2pr_all = a2zero
            a2pr_tc  = a2zero
            a2pr_c   = a2zero
            a2pr_fbc = a2zero
            a2pr_ot  = a2zero
            # wn:
            a2prwn_all = a2zero
            a2prwn_tc  = a2zero
            a2prwn_c   = a2zero
            a2prwn_fbc = a2zero
            a2prwn_nbc = a2zero
            a2prwn_ot  = a2zero


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
            ##-- leap year -------
            #if (mon==2)&(eday==29):
            #  eday = 28
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
                a2tagtmp_tc    = a2zero
                a2tagtmp_c     = a2zero
                a2tagtmp_fbc   = a2zero
                a2tagtmp_nbc   = a2zero
                a2tagtmp_ot    = a2zero
                a2tagtmpwn_ot  = a2zero
                #------------------ 

                #****************************
                # weighting considering occurence frequency
                #------------------
                #for htag_inc in lhtag_inc:
                #  dhour       = datetime.timedelta(hours = htag_inc)
                #  target      = now + dhour
                #  year_target = target.year
                #  mon_target  = target.month
                #  day_target  = target.day
                #  hour_target = target.hour
                #  #-- tag name ---
                #  tagdir   = tagdir_root + "/%04d%02d"%(year_target, mon_target)
                #  tagname  = tagdir + "/tag.%stc%04d.c%04d.f%04d.%04d.%02d.%02d.%02d.sa.one"%(tctype, dist_tc, dist_c, dist_f, year_target,mon_target,day_target,hour_target)
        
                #  if not os.access(tagname, os.F_OK):
                #    print "AAAA"
                #    print "nofile", tagname
                #    if (year==iyear)&(mon==1)&(day==1):
                #      continue
                #    elif (year==eyear)&(mon==12)&(day==eday):
                #      continue
                #  #-- load -------
                #  a2tag         = fromfile(tagname, int32).reshape(180,360)
                #  lout          = tag_fsub.solve_tag_4type(a2tag.T)
                #  a2tagtmp_tc   = a2tagtmp_tc   + array(lout[0].T, float32)
                #  a2tagtmp_c    = a2tagtmp_c    + array(lout[1].T, float32)
                #  a2tagtmp_fbc  = a2tagtmp_fbc  + array(lout[2].T, float32)
                #  a2tagtmp_nbc  = a2tagtmp_nbc  + array(lout[3].T, float32)
                #  a2tagtmp_ot   = a2tagtmp_ot   + ma.masked_where((a2tagtmp_tc + a2tagtmp_c + a2tagtmp_fbc) !=0, a2one).filled(0.0)
                #  # wn: with no n-baroclinic
                #  a2tagtmpwn_ot = a2tagtmpwn_ot + ma.masked_where(a2tag !=0, a2one).filled(0.0)

                ###
                #a2tagtmp_tc    = a2tagtmp_tc   / len(lhtag_inc)
                #a2tagtmp_c     = a2tagtmp_c    / len(lhtag_inc)
                #a2tagtmp_fbc   = a2tagtmp_fbc  / len(lhtag_inc)
                #a2tagtmp_nbc   = a2tagtmp_nbc  / len(lhtag_inc)
                #a2tagtmp_ot    = a2tagtmp_ot   / len(lhtag_inc)
                #a2tagtmpwn_ot  = a2tagtmpwn_ot / len(lhtag_inc)
                ###
                #a2tag_all   = a2tagtmp_tc + a2tagtmp_c + a2tagtmp_fbc + a2tagtmp_ot
                #a2tagwn_all = a2tagtmp_tc + a2tagtmp_c + a2tagtmp_fbc + a2tagtmp_nbc + a2tagtmpwn_ot
                ###
                #a2tag_tc    = a2tagtmp_tc  / a2tag_all
                #a2tag_c     = a2tagtmp_c   / a2tag_all
                #a2tag_fbc   = a2tagtmp_fbc / a2tag_all
                #a2tag_ot    = a2tagtmp_ot  / a2tag_all
                ## wn: with non-baroclinic
                #a2tagwn_tc  = a2tagtmp_tc    / a2tagwn_all
                #a2tagwn_c   = a2tagtmp_c     / a2tagwn_all
                #a2tagwn_fbc = a2tagtmp_fbc   / a2tagwn_all
                #a2tagwn_nbc = a2tagtmp_nbc   / a2tagwn_all
                #a2tagwn_ot  = a2tagtmpwn_ot  / a2tagwn_all


                #****************************
                # simple share
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
                  tagname  = tagdir + "/tag.%stc%04d.c%04d.f%04d.%04d.%02d.%02d.%02d.sa.one"%(tctype, dist_tc, dist_c, dist_f, year_target,mon_target,day_target,hour_target)

                  if not os.access(tagname, os.F_OK):
                    print "AAAA"
                    print "nofile", tagname
                    if (year==iyear)&(mon==1)&(day==1):
                      continue
                    elif (year==eyear)&(mon==12)&(day==eday):
                      continue
                  #-- load -------
                  a2tag         = fromfile(tagname, int32).reshape(180,360)
                  lout          = tag_fsub.solve_tag_4type(a2tag.T)
                  a2tagtmp_tc   = a2tagtmp_tc   + array(lout[0].T, float32)
                  a2tagtmp_c    = a2tagtmp_c    + array(lout[1].T, float32)
                  a2tagtmp_fbc  = a2tagtmp_fbc  + array(lout[2].T, float32)
                  a2tagtmp_nbc  = a2tagtmp_nbc  + array(lout[3].T, float32)
                  # wn: with non-baroclinic

                ##
                a2tagtmp_tc    = ma.masked_greater(a2tagtmp_tc,  0.0).filled(1.0)
                a2tagtmp_c     = ma.masked_greater(a2tagtmp_c,   0.0).filled(1.0)
                a2tagtmp_fbc   = ma.masked_greater(a2tagtmp_fbc, 0.0).filled(1.0)
                a2tagtmp_nbc   = ma.masked_greater(a2tagtmp_nbc, 0.0).filled(1.0)
                a2tagtmp_ot    = ma.masked_greater( (a2tagtmp_tc + a2tagtmp_c + a2tagtmp_fbc)==0.0, a2zero).filled(1.0)
                a2tagtmpwn_ot  = ma.masked_greater( (a2tagtmp_tc + a2tagtmp_c + a2tagtmp_fbc + a2tagtmp_nbc)==0.0, a2zero).filled(1.0)
                ##
                a2tag_all   = a2tagtmp_tc + a2tagtmp_c + a2tagtmp_fbc + a2tagtmp_ot
                a2tagwn_all = a2tagtmp_tc + a2tagtmp_c + a2tagtmp_fbc + a2tagtmp_nbc + a2tagtmpwn_ot
                ##
                a2tag_tc    = a2tagtmp_tc  / a2tag_all
                a2tag_c     = a2tagtmp_c   / a2tag_all
                a2tag_fbc   = a2tagtmp_fbc / a2tag_all
                a2tag_ot    = a2tagtmp_ot
                # wn: with non-baroclinic
                a2tagwn_tc  = a2tagtmp_tc    / a2tagwn_all
                a2tagwn_c   = a2tagtmp_c     / a2tagwn_all
                a2tagwn_fbc = a2tagtmp_fbc   / a2tagwn_all
                a2tagwn_nbc = a2tagtmp_nbc   / a2tagwn_all
                a2tagwn_ot  = a2tagtmpwn_ot


                ##*****************************
                # weight precipitation
                #-----------------------------
                a2prtmp_tc   = ma.masked_less(a2pr,0.0).filled(0.0) * a2tag_tc
                a2prtmp_c    = ma.masked_less(a2pr,0.0).filled(0.0) * a2tag_c
                a2prtmp_fbc  = ma.masked_less(a2pr,0.0).filled(0.0) * a2tag_fbc
                a2prtmp_ot   = ma.masked_less(a2pr,0.0).filled(0.0) * a2tag_ot

                # wn:
                a2prwntmp_tc   = ma.masked_less(a2pr,0.0).filled(0.0) * a2tagwn_tc
                a2prwntmp_c    = ma.masked_less(a2pr,0.0).filled(0.0) * a2tagwn_c
                a2prwntmp_fbc  = ma.masked_less(a2pr,0.0).filled(0.0) * a2tagwn_fbc
                a2prwntmp_nbc  = ma.masked_less(a2pr,0.0).filled(0.0) * a2tagwn_nbc
                a2prwntmp_ot   = ma.masked_less(a2pr,0.0).filled(0.0) * a2tagwn_ot



                #*****************************
                # sum precipitation
                #-----------------------------
                a2pr_all     = a2pr_all + a2pr
                a2pr_tc      = a2pr_tc  + a2prtmp_tc
                a2pr_c       = a2pr_c   + a2prtmp_c
                a2pr_fbc     = a2pr_fbc + a2prtmp_fbc
                a2pr_ot      = a2pr_ot  + a2prtmp_ot

                # wn:
                a2prwn_all     = a2prwn_all + a2pr
                a2prwn_tc      = a2prwn_tc  + a2prwntmp_tc
                a2prwn_c       = a2prwn_c   + a2prwntmp_c
                a2prwn_fbc     = a2prwn_fbc + a2prwntmp_fbc
                a2prwn_nbc     = a2prwn_nbc + a2prwntmp_nbc
                a2prwn_ot      = a2prwn_ot  + a2prwntmp_ot



            #*****************************
            # convert unit to mm/s
            #---------------------
            if prtype in ["GPCP1DD"]:
              coef       = 1.0/(60*60*24.0)
            else:
              coef       = 1.0
            #--                         
            totaltimes   = ctrack_para.ret_totaldays(year,year,mon)*len(lhour)
            #
            a2pr_all    = a2pr_all   *coef/ totaltimes 
            a2pr_tc     = a2pr_tc    *coef/ totaltimes 
            a2pr_c      = a2pr_c     *coef/ totaltimes 
            a2pr_fbc    = a2pr_fbc   *coef/ totaltimes 
            a2pr_ot     = a2pr_ot    *coef/ totaltimes 
            # wn:
            a2prwn_all  = a2prwn_all *coef/ totaltimes 
            a2prwn_tc   = a2prwn_tc  *coef/ totaltimes 
            a2prwn_c    = a2prwn_c   *coef/ totaltimes 
            a2prwn_fbc  = a2prwn_fbc *coef/ totaltimes 
            a2prwn_nbc  = a2prwn_nbc *coef/ totaltimes 
            a2prwn_ot   = a2prwn_ot  *coef/ totaltimes 


            #print "all",mon, a2pr_all.sum()
            #print "tc", mon, a2pr_tc.sum()
            #print "c",  mon, a2pr_c.sum()
            #print "fbc",mon, a2pr_fbc.sum()              
            #print "nbc",mon, a2pr_nbc.sum()
            #print "ot", mon, a2pr_ot.sum()
            #*****************************
            #-- save monthly data ---
            #-----------------------------
            sodir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/tagpr/c%02dh.tc%02dh"%(sresol, thdura_c, thdura_tc)
            sodirwn_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/tagpr/wn.c%02dh.tc%02dh"%(sresol, thdura_c, thdura_tc)
            #
            sodir      = sodir_root   + "/%04d%02d"%(year, mon)
            sodirwn    = sodirwn_root + "/%04d%02d"%(year, mon)
            ctrack_func.mk_dir(sodir)
            ctrack_func.mk_dir(sodirwn)
            #
            sname_all  =  sodir  + "/pr.plain.%stc%04d.c%04d.f%04d.%04d.%02d.%s.sa.one" %(tctype, dist_tc, dist_c, dist_f, year, mon, prtype)
            sname_tc   =  sodir  + "/pr.tc.%stc%04d.c%04d.f%04d.%04d.%04d.%s.sa.one" %(tctype, dist_tc, dist_c, dist_f, year, mon, prtype)
            sname_c    =  sodir  + "/pr.c.%stc%04d.c%04d.f%04d.%04d.%02d.%s.sa.one"  %(tctype, dist_tc, dist_c, dist_f, year, mon, prtype)
            sname_fbc  =  sodir  + "/pr.fbc.%stc%04d.c%04d.f%04d.%04d.%02d.%s.sa.one"%(tctype, dist_tc, dist_c, dist_f, year, mon, prtype)
            sname_ot   =  sodir  + "/pr.ot.%stc%04d.c%04d.f%04d.%04d.%02d.%s.sa.one" %(tctype, dist_tc, dist_c, dist_f, year, mon, prtype)

            # wn:
            snamewn_all  =  sodirwn  + "/pr.wn.plain.%stc%04d.c%04d.f%04d.%04d.%02d.%s.sa.one" %(tctype, dist_tc, dist_c, dist_f, year, mon, prtype)
            snamewn_tc   =  sodirwn  + "/pr.wn.tc.%stc%04d.c%04d.f%04d.%04d.%04d.%s.sa.one" %(tctype, dist_tc, dist_c, dist_f, year, mon, prtype)
            snamewn_c    =  sodirwn  + "/pr.wn.c.%stc%04d.c%04d.f%04d.%04d.%02d.%s.sa.one"  %(tctype, dist_tc, dist_c, dist_f, year, mon, prtype)
            snamewn_fbc  =  sodirwn  + "/pr.wn.fbc.%stc%04d.c%04d.f%04d.%04d.%02d.%s.sa.one"%(tctype, dist_tc, dist_c, dist_f, year, mon, prtype)
            snamewn_nbc  =  sodirwn  + "/pr.wn.nbc.%stc%04d.c%04d.f%04d.%04d.%02d.%s.sa.one"%(tctype, dist_tc, dist_c, dist_f, year, mon, prtype)
            snamewn_ot   =  sodirwn  + "/pr.wn.ot.%stc%04d.c%04d.f%04d.%04d.%02d.%s.sa.one" %(tctype, dist_tc, dist_c, dist_f, year, mon, prtype)


            #-----------------------------
            a2pr_all.tofile(sname_all)
            a2pr_tc.tofile(sname_tc)
            a2pr_c.tofile(sname_c)
            a2pr_fbc.tofile(sname_fbc)
            a2pr_ot.tofile(sname_ot)
            print sname_c

            # wn:
            a2prwn_all.tofile(snamewn_all)
            a2prwn_tc.tofile(snamewn_tc)
            a2prwn_c.tofile(snamewn_c)
            a2prwn_fbc.tofile(snamewn_fbc)
            a2prwn_nbc.tofile(snamewn_nbc)
            a2prwn_ot.tofile(snamewn_ot)
            print snamewn_c



