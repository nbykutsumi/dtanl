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
lbstflag_tc   = ["bst"]
#lbstflag_tc   = ["bst"]
#lbstflag_f    = ["bst.high","bst.type"]
lbstflag_f = [""]

sresol  = "anl_p"
iyear   = 2001
eyear   = 2009
#iyear    = 2001
#eyear    = 2001
#lseason = ["NDJFMA","JJASON"]
lseason = ["ALL","NDJFMA","JJASON"]
#lseason = ["NDJFMA","JJASON","DJF","JJA"]
#lseason = ["DJF"]
#lseason = ["ALL"]
#lseason = [1]

iday    = 1
ptile   = 99.9 # (%)
#lnhour  = [1,3,6,12]
#lnhour  = [1,3,6,12,24]
lnhour  = [1,3,6,12,24]
#lnhour  = [24]
#ltag    = ["nbcot","nbcot","tc","c","fbc","nbc","ot","o.tc","o.c","o.fbc","o.nbc","TCF","TCFC","TCB","TCBC"]
#ltag    = ["tc","c","fbc","nbc","ot"]
ltag    = ["nbcot"]
thdura_c  = 48
thdura_tc = thdura_c

iyear_dat= 2001
eyear_dat= 2009
#--------------------------------
lprtype  = ["GSMaP"]
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

nx,ny   =[360,180]

thorog    = 1500   # [m]
miss      = -9999.0
miss_out  = -9999.0
miss_gpcp = -99999.

#---------------------
region    = "GLOB"
lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region)

#---------------------
for season in lseason:
  for nhour in lnhour:
    for prtype in lprtype:
      #-- load ptile -------
      if prtype == "JRA":
        ptiledir_root = "/media/disk2/data/JRA25/sa.one/6hr/PR/ptile" 
        ptiledir      = ptiledir_root + "/%04d-%04d"%(2001,2004)
        ptilename     = ptiledir + "/fcst_phy2m.PR.p%05.2f.%s.sa.one"%(ptile,"ALL")
        #ptiledir      = ptiledir_root + "/%04d-%04d"%(iyear,eyear)
        a2ptile       = fromfile(ptilename, float32).reshape(ny,nx)
      if prtype == "GPCP1DD":
        ptiledir_root = "/media/disk2/data/GPCP1DD/v1.2/1dd/ptile" 
        ptiledir      = ptiledir_root + "/%04d-%04d"%(2000,2010)
        ptilename     = ptiledir + "/pr.gpcp.p%05.2f.%s.bn"%(ptile,"ALL")
        #ptiledir      = ptiledir_root + "/%04d-%04d"%(iyear,eyear)
        a2ptile       = fromfile(ptilename, float32).reshape(ny,nx)
    
      if prtype == "GSMaP":
        thmissrat = 0.8
        #ptiledir_root = "/media/disk2/data/GSMaP/sa.one/1hr/ptot/ptile" 
        #ptiledir      = ptiledir_root + "/%04d-%04d"%(iyear, eyear)
        #ptilename     = ptiledir + "/gsmap_mvk.v5.222.1.mov%02dhr.p%05.2f.%s.sa.one"%(nhour, ptile,"ALL")
        ptiledir_root = "/media/disk2/data/GSMaP/sa.one/1hr/ptot/ptile" 
        #ptiledir      = ptiledir_root + "/%04d-%04d"%(iyear, eyear)
        ptiledir      = ptiledir_root + "/%04d-%04d"%(2001, 2009)
        #ptilename     = ptiledir  + "/gsmap_mvk.v5.222.1.movw06hr.p99.90.ALL.sa.one"
        ptilename     = ptiledir  + "/gsmap_mvk.v5.222.1.movw%02dhr.%3.1f.p%05.2f.ALL.sa.one"%(nhour, thmissrat, ptile)
        a2ptile       = fromfile(ptilename, float32).reshape(120,360)
        a2ptile       = gsmap_func.gsmap2global_one(a2ptile, miss_out)
  
        a2ptile       = (ma.masked_equal(a2ptile,miss)).filled(miss)
  
        print ptilename
    
      #-----------------------
      for bstflag_tc in lbstflag_tc:
        for bstflag_f in lbstflag_f:
          #-- TC type ----------
          if bstflag_tc =="bst":
            tctype = "bst"
          else:
            tctype = ""
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
          def ret_lhtag_inc(nhour, hour):
            if nhour == 24:
              if hour in [0,6,12,18]:
                lhtag_inc = [-24,-18,-12,-6,0]
                lwght     = array([3,6,6,6,3])/24.0
              elif hour in [1,7,13,19]:
                lhtag_inc = [-25,-19,-13,-7,-1]
                lwght     = array([2,6,6,6,4])/24.0
              elif hour in [2,8,14,20]:
                lhtag_inc = [-26,-20,-14,-8,-2]
                lwght     = array([1,6,6,6,5])/24.0
              elif hour in [3,9,15,21]:
                lhtag_inc = [-21,-15,-9,-3]
                lwght     = array([6,6,6,6])/24.0
              elif hour in [4,10,16,22]:
                lhtag_inc = [-22,-16,-10,-4,+2]
                lwght     = array([5,6,6,6,1])/24.0
              elif hour in [5,11,17,23]:
                lhtag_inc = [-23,-17,-11,-5,+1]
                lwght     = array([4,6,6,6,2])/24.0
      
            elif nhour == 12:
              if hour in [0,6,12,18]:
                lhtag_inc = [-12,-6,0]
                lwght     = array([3,6,3])/12.0
              elif hour in [1,7,13,19]:
                lhtag_inc = [-13,-7,-1]
                lwght     = array([2,6,4])/12.0
              elif hour in [2,8,14,20]:
                lhtag_inc = [-14,-8,-2]
                lwght     = array([1,6,5])/12.0
              elif hour in [3,9,15,21]:
                lhtag_inc = [-9,-3]
                lwght     = array([6,6])/12.0
              elif hour in [4,10,16,22]:
                lhtag_inc = [-10,-4,+2]
                lwght     = array([5,6,1])/12.0
              elif hour in [5,11,17,23]:
                lhtag_inc = [-11,-5,+1]
                lwght     = array([4,6,2])/12.0
      
            elif nhour == 6:
              if hour in [0,6,12,18]:
                lhtag_inc = [-6,0]
                lwght     = array([3,3])/6.0
              elif hour in [1,7,13,19]:
                lhtag_inc = [-7,-1]
                lwght     = array([2,4])/6.0
              elif hour in [2,8,14,20]:
                lhtag_inc = [-8,-2]
                lwght     = array([1,5])/6.0
              elif hour in [3,9,15,21]:
                lhtag_inc = [-3]
                lwght     = array([1.0])
              elif hour in [4,10,16,22]:
                lhtag_inc = [-4,+2]
                lwght     = array([5,1])/6.0
              elif hour in [5,11,17,23]:
                lhtag_inc = [-5,+1]
                lwght     = array([4,2])/6.0
      
            elif nhour == 3:
              if hour in  [0,6,12,18]:
                lhtag_inc = [0]
                lwght     = array([1.0])
              elif hour in [1,7,13,19]:
                lhtag_inc = [-1]
                lwght     = array([1.0])
              elif hour in [2,8,14,20]:
                lhtag_inc = [-2]
                lwght     = array([1.0])
              elif hour in [3,9,15,21]:
                lhtag_inc = [-3]
                lwght     = array([1.0])
              elif hour in [4,10,16,22]:
                lhtag_inc = [-4,+2]
                lwght     = array([2,1])/3.0
              elif hour in [5,11,17,23]:
                lhtag_inc = [-5,+1]
                lwght     = array([1,2])/3.0
      
            elif nhour == 1:
              if hour in [0,6,12,18]:
                lhtag_inc = [0]
                lwght     = array([1.0])
              elif hour in [1,7,13,19]:
                lhtag_inc = [-1]
                lwght     = array([1.0])
              elif hour in [2,8,14,20]:
                lhtag_inc = [-2]
                lwght     = array([1.0])
              elif hour in [3,9,15,21]:
                lhtag_inc = [-3]
                lwght     = array([1.0])
              elif hour in [4,10,16,22]:
                lhtag_inc = [+2]
                lwght     = array([1.0])
              elif hour in [5,11,17,23]:
                lhtag_inc = [+1]
                lwght     = array([1.0])
            #
            return lhtag_inc, lwght
      
          #-- orog ------------------------
          orogname = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
          a2orog   = fromfile(orogname, float32).reshape(ny,nx)
          
          a2shade  = ma.masked_where(a2orog >thorog, a2orog).filled(miss)
          #***************************************
          
          #-----------------
          if calcflag == True:
            #-----------------
            lmon = ctrack_para.ret_lmon(season)
            #--------------------------------
            a2one       = ones([ny,nx],float32)
            a2zero      = zeros([ny,nx],float32)
            a2num_pln   = a2zero.copy()
            a2num_tc    = a2zero.copy()
            a2num_c     = a2zero.copy()
            a2num_fbc   = a2zero.copy()
            a2num_nbc   = a2zero.copy()
            a2num_ot    = a2zero.copy()
            ##
            a2num_o_tc  = a2zero.copy()
            a2num_o_c   = a2zero.copy()
            a2num_o_fbc = a2zero.copy()
            a2num_o_nbc = a2zero.copy()
            a2num_o_ot  = a2zero.copy()
            ##
            a2num_TCF   = a2zero.copy()
            a2num_TCFC  = a2zero.copy()
            a2num_TCB   = a2zero.copy()
            a2num_TCBC  = a2zero.copy()
       
    
            a2rfreq_sum = zeros([ny,nx],float32)
            #--------------------------------
            for year in range(iyear, eyear+1):
              #-----------------
              for mon in lmon:
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
                #-- leap year -------
                if (mon==2)&(eday==29):
                  eday = 28
                #--------------------
                for day in range(iday, eday+1):
                  #***
                  if (year==iyear_dat)&(mon==1)&(day==1):
                    continue
                  elif (year==eyear_dat)&(mon==12)&(day==eday):
                    continue
                  #*** 
                  print "nhour=",nhour,prtype, season, year, mon, day
                  for hour in lhour:
                    #-- load prec ----
                    if prtype   in ["GSMaP"]:
                      a2pr  = gsmap_func.timeave_gsmap_backward_saone(year,mon,day,hour, nhour)
                      a2pr  = gsmap_func.gsmap2global_one(a2pr, miss_out)
      
                    #*****************************
                    # load corresponding tags 
                    #-----------------------------
                    (lhtag_inc, lwght)   = ret_lhtag_inc(nhour, hour)
                    now   = datetime.datetime(year, mon, day, hour)
                    #------------------
                    a2tag_tc    = a2zero.copy()
                    a2tag_c     = a2zero.copy()
                    a2tag_fbc   = a2zero.copy()
                    a2tag_nbc   = a2zero.copy()
                    a2tag_ot    = a2zero.copy()
                    #------------------ 
                    for iinc in arange(len(lhtag_inc)):
                      htag_inc  = lhtag_inc[iinc]
                      wght      = lwght[iinc]
      
                      dhour       = datetime.timedelta(hours = htag_inc)
                      target      = now + dhour
                      year_target = target.year
                      mon_target  = target.month
                      day_target  = target.day
                      hour_target = target.hour
                      #-- tag name ---
                      tagdir   = tagdir_root + "/%04d%02d"%(year_target, mon_target)
                      tagname  = tagdir + "/tag.%stc%04d.c%04d.%sf%04d.%04d.%02d.%02d.%02d.sa.one"%(tctype, dist_tc, dist_c, ftype, dist_f, year_target,mon_target,day_target,hour_target)
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
    
                      a2tag_tmp_tc  = array(lout[0].T, float32)
                      a2tag_tmp_c   = array(lout[1].T, float32)
                      a2tag_tmp_fbc = array(lout[2].T, float32)
                      a2tag_tmp_nbc = array(lout[3].T, float32)
                      a2tag_tmp_ot  = ma.masked_where(a2tag !=0, a2one).filled(0.0)
    
                      a2tag_sum     = a2tag_tmp_tc + a2tag_tmp_c + a2tag_tmp_fbc + a2tag_tmp_nbc
                      a2olwgt_tc      = (ma.masked_where(a2tag_sum==0.0, a2tag_tmp_tc ) / a2tag_sum).filled(0.0)
                      a2olwgt_c       = (ma.masked_where(a2tag_sum==0.0, a2tag_tmp_c  ) / a2tag_sum).filled(0.0)
                      a2olwgt_fbc     = (ma.masked_where(a2tag_sum==0.0, a2tag_tmp_fbc) / a2tag_sum).filled(0.0)
                      a2olwgt_nbc     = (ma.masked_where(a2tag_sum==0.0, a2tag_tmp_nbc) / a2tag_sum).filled(0.0) 
    
                      a2tag_tc  = a2tag_tc  + a2tag_tmp_tc  * wght *a2olwgt_tc 
                      a2tag_c   = a2tag_c   + a2tag_tmp_c   * wght *a2olwgt_c
                      a2tag_fbc = a2tag_fbc + a2tag_tmp_fbc * wght *a2olwgt_fbc 
                      a2tag_nbc = a2tag_nbc + a2tag_tmp_nbc * wght *a2olwgt_nbc 
                      a2tag_ot  = a2tag_ot  + a2tag_tmp_ot  * wght
    
                    ##
                    a2tag_all = a2tag_tc + a2tag_c + a2tag_fbc + a2tag_nbc + a2tag_ot
                    #************************************
                    # make tag with only one type
                    #------------------------------------
                    a2tag_o_tc     = ma.masked_where(a2tag_all !=a2tag_tc, a2tag_tc).filled(0.0)
                    a2tag_o_c      = ma.masked_where(a2tag_all !=a2tag_c,  a2tag_c).filled(0.0)
                    a2tag_o_fbc    = ma.masked_where(a2tag_all !=a2tag_fbc, a2tag_fbc).filled(0.0)
                    a2tag_o_nbc    = ma.masked_where(a2tag_all !=a2tag_nbc, a2tag_nbc).filled(0.0)
                    a2tag_o_ot     = a2tag_ot
      
                    #****************
                    # tag for overlap
                    #----------------
                    a2tag_TCF      = ma.masked_where(a2tag_tc  ==0.0,  (a2tag_tc + a2tag_fbc + a2tag_nbc)/3.0 ).filled(0.0)
                    a2tag_TCF      = ma.masked_where((a2tag_fbc==0.0)&(a2tag_nbc==0.0), a2tag_TCF).filled(0.0)
                    a2tag_TCF      = ma.masked_where((a2tag_c  !=0.0), a2tag_TCF).filled(0.0)
                    ##
                    a2tag_TCFC     = ma.masked_where(a2tag_tc  ==0.0, (a2tag_tc + a2tag_fbc + a2tag_nbc + a2tag_c)/4.0 ).filled(0.0)
                    a2tag_TCFC     = ma.masked_where((a2tag_fbc==0.0)&(a2tag_nbc==0.0)&(a2tag_c==0.0), a2tag_TCFC).filled(0.0)
                    ##
                    a2tag_TCB      = ma.masked_where(a2tag_tc  ==0.0, (a2tag_tc + a2tag_fbc)/2.0).filled(0.0)
                    a2tag_TCB      = ma.masked_where(a2tag_fbc ==0.0, a2tag_TCB).filled(0.0)
                    a2tag_TCB      = ma.masked_where(a2tag_nbc !=0.0, a2tag_TCB).filled(0.0)
                    a2tag_TCB      = ma.masked_where(a2tag_c   !=0.0, a2tag_TCB).filled(0.0)
                    ##
                    a2tag_TCBC     = ma.masked_where(a2tag_tc  ==0.0, (a2tag_tc + a2tag_fbc + a2tag_c)/3.0).filled(0.0)
                    a2tag_TCBC     = ma.masked_where((a2tag_fbc==0.0)&(a2tag_c==0.0), a2tag_TCBC).filled(0.0)
                    a2tag_TCBC     = ma.masked_where(a2tag_nbc !=0.0, a2tag_TCBC).filled(0.0)
      
                    #*****************************
                    # check Pex
                    #-----------------------------
                    a2tag_tc    = ma.masked_where(a2pr < a2ptile, a2tag_tc ).filled(0.0)
                    a2tag_c     = ma.masked_where(a2pr < a2ptile, a2tag_c  ).filled(0.0)
                    a2tag_fbc   = ma.masked_where(a2pr < a2ptile, a2tag_fbc).filled(0.0)
                    a2tag_nbc   = ma.masked_where(a2pr < a2ptile, a2tag_nbc).filled(0.0)
                    a2tag_ot    = ma.masked_where(a2pr < a2ptile, a2tag_ot ).filled(0.0)
    
                    ##
      
                    a2tag_o_tc  = ma.masked_where(a2pr < a2ptile, a2tag_o_tc ).filled(0.0)
                    a2tag_o_c   = ma.masked_where(a2pr < a2ptile, a2tag_o_c  ).filled(0.0)
                    a2tag_o_fbc = ma.masked_where(a2pr < a2ptile, a2tag_o_fbc).filled(0.0)
                    a2tag_o_nbc = ma.masked_where(a2pr < a2ptile, a2tag_o_nbc).filled(0.0)
                    a2tag_o_ot  = ma.masked_where(a2pr < a2ptile, a2tag_o_ot ).filled(0.0)
                    ##
                    a2tag_TCF   = ma.masked_where(a2pr < a2ptile, a2tag_TCF).filled(0.0)
                    a2tag_TCFC  = ma.masked_where(a2pr < a2ptile, a2tag_TCFC).filled(0.0)
                    a2tag_TCB   = ma.masked_where(a2pr < a2ptile, a2tag_TCB).filled(0.0)
                    a2tag_TCBC  = ma.masked_where(a2pr < a2ptile, a2tag_TCBC).filled(0.0)
      
                    #** weighting ***
                    #****************
                    a2num_pln   = a2num_pln + ma.masked_where(a2pr < a2ptile, a2one).filled(0.0)
                    a2num_tc    = a2num_tc    + a2tag_tc  
                    a2num_c     = a2num_c     + a2tag_c  
                    a2num_fbc   = a2num_fbc   + a2tag_fbc
                    a2num_nbc   = a2num_nbc   + a2tag_nbc
                    a2num_ot    = a2num_ot    + a2tag_ot
                    ##
                    a2num_o_tc  = a2num_o_tc  + a2tag_o_tc
                    a2num_o_c   = a2num_o_c   + a2tag_o_c
                    a2num_o_fbc = a2num_o_fbc + a2tag_o_fbc
                    a2num_o_nbc = a2num_o_nbc + a2tag_o_nbc
                    ##
                    a2num_TCF   = a2num_TCF   + a2tag_TCF
                    a2num_TCFC  = a2num_TCFC  + a2tag_TCFC
                    a2num_TCB   = a2num_TCB   + a2tag_TCB
                    a2num_TCBC  = a2num_TCBC  + a2tag_TCBC
                    ##
            #------------------------------------
            da2rfreq         = {}
            da2rfreq["tc"]   = (ma.masked_where(a2num_pln==0.0, a2num_tc ) / a2num_pln).filled(0.0)
            da2rfreq["c"]    = (ma.masked_where(a2num_pln==0.0, a2num_c  ) / a2num_pln).filled(0.0)
            da2rfreq["fbc"]  = (ma.masked_where(a2num_pln==0.0, a2num_fbc) / a2num_pln).filled(0.0)
            da2rfreq["nbc"]  = (ma.masked_where(a2num_pln==0.0, a2num_nbc) / a2num_pln).filled(0.0)
            da2rfreq["ot"]   = (ma.masked_where(a2num_pln==0.0, a2num_ot ) / a2num_pln).filled(0.0)
            ##
            da2rfreq["o.tc"]   = (ma.masked_where(a2num_pln==0.0, a2num_o_tc ) / a2num_pln).filled(0.0)
            da2rfreq["o.c"]    = (ma.masked_where(a2num_pln==0.0, a2num_o_c  ) / a2num_pln).filled(0.0)
            da2rfreq["o.fbc"]  = (ma.masked_where(a2num_pln==0.0, a2num_o_fbc) / a2num_pln).filled(0.0)
            da2rfreq["o.nbc"]  = (ma.masked_where(a2num_pln==0.0, a2num_o_nbc) / a2num_pln).filled(0.0)
            ##
            da2rfreq["TCF"]    = (ma.masked_where(a2num_pln==0.0, a2num_TCF  ) / a2num_pln).filled(0.0)
            da2rfreq["TCFC"]   = (ma.masked_where(a2num_pln==0.0, a2num_TCFC ) / a2num_pln).filled(0.0)
            da2rfreq["TCB"]    = (ma.masked_where(a2num_pln==0.0, a2num_TCB  ) / a2num_pln).filled(0.0)
            da2rfreq["TCBC"]   = (ma.masked_where(a2num_pln==0.0, a2num_TCBC ) / a2num_pln).filled(0.0)
            ##
            #****************************************
            # mask where a2ptile ==miss
            #----------------------------------------
            for stag in ltag:
              da2rfreq[stag]   = ma.masked_where(a2ptile==miss, da2rfreq[stag]).filled(miss)
            #****************************************
            # write to file
            #----------------------------------------
            sodir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/tagpr/c%02dh.tc%02dh"%(sresol, thdura_c, thdura_tc)
            sodir      = sodir_root + "/%04d-%04d/%s"%(iyear, eyear, season)
            ctrack_func.mk_dir(sodir)
            dsname    = {}
            for stag in ltag:
              #dsname[stag]    =  sodir  + "/rfreq.%stc%02d.c%02d.%sf%02d.%04d-%04d.%s.mov%02dhr.%05.2f.%s.%s.sa.one" %(tctype, dist_tc/100, dist_c/100, ftype, dist_f/100, iyear, eyear, season, nhour, ptile, prtype, stag)
              dsname[stag]    =  sodir  + "/rfreq.%stc%04d.c%04d.%sf%04d.%04d-%04d.%s.mov%02dhr.%05.2f.%s.%s.sa.one" %(tctype, dist_tc, dist_c, ftype, dist_f, iyear, eyear, season, nhour, ptile, prtype, stag)
              da2rfreq[stag].tofile(dsname[stag])
              print dsname[stag] 
    
            ##*** test *******
            #for stag in ["tc","c","fbc","nbc","ot"]:
            #  print stag, ma.masked_equal(da2rfreq[stag],miss).sum()
            #  a2rfreq_sum = a2rfreq_sum + ma.masked_equal(da2rfreq[stag],-9999.0).filled(0.0)
    
          #****************************************
          # draw figure
          #----------------------------------------
          sodir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/tagpr/c%02dh.tc%02dh"%(sresol, thdura_c, thdura_tc)
          sodir      = sodir_root + "/%04d-%04d/%s"%(iyear, eyear, season)
          figdir     = sodir + "/pict"
          ctrack_func.mk_dir(figdir)
          dsname     = {}
          dfigname   = {}
          da2frac    = {}
          for stag in ltag:
            #-- name --
            if stag == "nbcot":
              dsname["ot"]    =  sodir  + "/rfreq.%stc%04d.c%04d.%sf%04d.%04d-%04d.%s.mov%02dhr.%05.2f.%s.%s.sa.one" %(tctype, dist_tc, dist_c, ftype, dist_f, iyear, eyear, season, nhour, ptile, prtype, "ot")
              dsname["nbc"]    =  sodir  + "/rfreq.%stc%04d.c%04d.%sf%04d.%04d-%04d.%s.mov%02dhr.%05.2f.%s.%s.sa.one" %(tctype, dist_tc, dist_c, ftype, dist_f, iyear, eyear, season, nhour, ptile, prtype, "nbc")
            else:
              dsname[stag]    =  sodir  + "/rfreq.%stc%04d.c%04d.%sf%04d.%04d-%04d.%s.mov%02dhr.%05.2f.%s.%s.sa.one" %(tctype, dist_tc, dist_c, ftype, dist_f, iyear, eyear, season, nhour, ptile, prtype, stag)
            #--
            dfigname[stag]  =  figdir + "/rfreq.%stc%04d.c%04d.%sf%04d.%04d-%04d.%s.mov%02dhr.%05.2f.%s.%s.png" %(tctype, dist_tc, dist_c, ftype, dist_f, iyear, eyear, season, nhour, ptile, prtype, stag)
      
      
          
            #-- settings --
            bnd    = [5,10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]
            cbarname = figdir + "/rfreq.cbar.png"
            #
            stitle   = "rfreq %04.1f %s: season:%s %s %04d-%04d %stc%04d c%04d %sf%04d"%(ptile, stag, season, prtype, iyear, eyear, tctype, dist_tc, dist_c, ftype, dist_f)
            mycm     = "Spectral_r"
            figname  = dfigname[stag]
          
            #-- load -----
            if stag == "nbcot":
              a2figdat_ot  = fromfile(dsname["ot"],  float32).reshape(ny,nx)
              a2figdat_nbc = fromfile(dsname["nbc"], float32).reshape(ny,nx)
              a2figdat     = ma.masked_equal(a2figdat_ot,miss) + ma.masked_equal(a2figdat_ot, miss)
            else:
              datname  = dsname[stag]
              a2figdat = fromfile(datname, float32).reshape(ny,nx)
            #--
            a2figdat = ma.masked_equal(a2figdat, miss) * 100.0
            a2figdat = ma.masked_equal(a2figdat, miss).filled(miss)



            #-- shade -----
            a2shade  = ma.masked_where(a2figdat==miss, a2shade).filled(miss)  
            #-- draw ------
            ctrack_fig.mk_pict_saone_reg(a2figdat, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon)
            print figname
     



