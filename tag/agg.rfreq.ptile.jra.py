from tag_fsub import *
from numpy import *
import ctrack_para, ctrack_func, ctrack_fig, chart_para
import gsmap_func
import calendar
import gsmap_func
import datetime
import os
#---------------------------
#singletime = True
singletime = False
calcflag   = True
#calcflag   = False
#lbstflag    = [True,False]
lbstflag   = [False]
iyear   = 2001
eyear   = 2004
#lseason = [1]
#lseason = ["NDJFMA","JJASON"]
#lseason = ["NDJFMA","JJASON","DJF","JJA","ALL"]
lseason = ["ALL"]
iday    = 1
ptile   = 99 # (%)
ltag    = ["tc","c","fbc","nbc","ot","o.tc","o.fbc","o.nbc","TCF","TCFC","TCB","TCBC"]
#ltag    = ["o.tc"]

iyear_dat= 2001
eyear_dat= 2004
#--------------------------------
#prtype   = "GPCP1DD"
#prtype    = "JRA"
#lprtype  = ["JRA"]
#lprtype  = ["GPCP1DD"]
lprtype  = ["GSMaP.03hr"]
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
  #-- load ptile -------
  if prtype == "JRA":
    ptiledir_root = "/media/disk2/data/JRA25/sa.one/6hr/PR/ptile" 
    ptiledir      = ptiledir_root + "/%04d-%04d"%(2001,2004)
    ptilename     = ptiledir + "/fcst_phy2m.PR.p%05.2f.%s.sa.one"%(ptile,"ALL")
    #ptiledir      = ptiledir_root + "/%04d-%04d"%(iyear,eyear)
    #ptilename     = ptiledir + "/fcst_phy2m.PR.p%05.2f.%s.sa.one"%(ptile,season)
    a2ptile       = fromfile(ptilename, float32).reshape(ny,nx)
  if prtype == "GPCP1DD":
    ptiledir_root = "/media/disk2/data/GPCP1DD/v1.2/1dd/ptile" 
    ptiledir      = ptiledir_root + "/%04d-%04d"%(2000,2010)
    ptilename     = ptiledir + "/pr.gpcp.p%05.2f.%s.bn"%(ptile,"ALL")
    #ptiledir      = ptiledir_root + "/%04d-%04d"%(iyear,eyear)
    #ptilename     = ptiledir + "/pr.gpcp.p%05.2f.%s.bn"%(ptile,season)
    a2ptile       = fromfile(ptilename, float32).reshape(ny,nx)

  if prtype == "GSMaP.03hr":
    ptiledir_root = "/media/disk2/data/GSMaP/sa.one/3hr/ptot/ptile" 
    ptiledir      = ptiledir_root + "/%04d-%04d"%(2001, 2004)
    ptilename     = ptiledir + "/gsmap_mvk.3rh.v5.222.1.p%05.2f.%s.sa.one"%(ptile,"ALL")
    a2ptile       = fromfile(ptilename, float32).reshape(120,360)
    a2ptile       = gsmap_func.gsmap2global_one(a2ptile, miss_out)

  #-----------------------
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
    if prtype   == "GSMaP.03hr":
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

    elif timestep == "12hr":
      hlen  = 12
      lhour = [0,12]
    elif timestep == "6hr":
      hlen  = 6
      lhour = [0,6,12,18]
    elif timestep == "3hr":
      hlen  = 3
      lhour = [0,3,6,9,12,15,18,21]
    elif timestep == "1hr":
      hlen  = 1
      lhour = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
    
    #--- corresponding tag time ------
    def ret_lhtag_inc(timestep, hour):
      if timestep == "day":
        lhtag_inc = [0,-6,-12,-18]

      elif timestep == "6hr":
        lhtag_inc = [0, -6]

      elif timestep == "3hr":
        if hour in  [0,6,12,18]:
          lhtag_inc = [0]
        elif hour in [3,9,15,21]:
          lhtag_inc = [-3]

      elif timestep == "1hr":
        if hour in [0,6,12,18]:
          lhtag_inc = [0]
        elif hour in [1,7,13,19]:
          lhtag_inc = [-1]
        elif hour in [2,8,14,20]:
          lhtag_inc = [-2]
        elif hour in [3,9,15,21]:
          lhtag_inc = [-3]
        elif hour in [4,10,16,22]:
          lhtag_inc = [+2]
        elif hour in [5,11,17,23]:
          lhtag_inc = [+1]
      #
      return lhtag_inc

    #-- orog ------------------------
    orogname = "/media/disk2/data/JRA25/sa.one/const/topo/topo.sa.one"
    a2orog   = fromfile(orogname, float32).reshape(ny,nx)
    
    a2shade  = ma.masked_where(a2orog >thorog, a2orog).filled(miss)
    #***************************************
    
    
    for season in lseason:
      #-----------------
      if calcflag == True:
        #-----------------
        lmon = ctrack_para.ret_lmon(season)
        #--------------------------------
        a2one       = ones([ny,nx],float32)
        a2zero      = zeros([ny,nx],float32)
        a2num_all   = a2zero.copy()
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
              print prtype, season, year, mon, day
              #*** 
              for hour in lhour:
                #-- prec name ----
                if prtype == "GSMaP.03hr":
                  prname    = prdir    + "/gsmap_mvk.3rh.%04d%02d%02d.%02d00.v5.222.1.sa.one"%(year, mon, day, hour)
                elif prtype == "JRA":
                  prname    = prdir    + "/fcst_phy2m.PR.%04d%02d%02d%02d.sa.one"%(year, mon, day, hour)
                elif prtype == "GPCP1DD":
                  prname    = prdir    + "/gpcp_1dd_v1.2_p1d.%04d%02d%02d.bn"%(year, mon, day)
        
                #-- load prec ----
                if prtype   in ["GSMaP.03hr","GSMaP.01hr"]:
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
                a2tag_tc    = a2zero.copy()
                a2tag_c     = a2zero.copy()
                a2tag_fbc   = a2zero.copy()
                a2tag_nbc   = a2zero.copy()
                a2tag_ot    = a2zero.copy()
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

                #****************
                a2num_all   = a2num_all + ma.masked_where(a2pr < a2ptile, a2one).filled(0.0)
                a2num_tc    = a2num_tc  + a2tag_tc
                a2num_c     = a2num_c   + a2tag_c
                a2num_fbc   = a2num_fbc + a2tag_fbc
                a2num_nbc   = a2num_nbc + a2tag_nbc
                a2num_ot    = a2num_ot  + a2tag_ot
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
        #-------------------------------------
        da2rfreq         = {}
        da2rfreq["tc"]   = (ma.masked_where(a2num_all==0.0, a2num_tc ) / a2num_all).filled(0.0)
        da2rfreq["c"]    = (ma.masked_where(a2num_all==0.0, a2num_c  ) / a2num_all).filled(0.0)
        da2rfreq["fbc"]  = (ma.masked_where(a2num_all==0.0, a2num_fbc) / a2num_all).filled(0.0)
        da2rfreq["nbc"]  = (ma.masked_where(a2num_all==0.0, a2num_nbc) / a2num_all).filled(0.0)
        da2rfreq["ot"]   = (ma.masked_where(a2num_all==0.0, a2num_ot ) / a2num_all).filled(0.0)
        ##
        da2rfreq["o.tc"]   = (ma.masked_where(a2num_all==0.0, a2num_o_tc ) / a2num_all).filled(0.0)
        da2rfreq["o.c"]    = (ma.masked_where(a2num_all==0.0, a2num_o_c  ) / a2num_all).filled(0.0)
        da2rfreq["o.fbc"]  = (ma.masked_where(a2num_all==0.0, a2num_o_fbc) / a2num_all).filled(0.0)
        da2rfreq["o.nbc"]  = (ma.masked_where(a2num_all==0.0, a2num_o_nbc) / a2num_all).filled(0.0)
        ##
        da2rfreq["TCF"]    = (ma.masked_where(a2num_all==0.0, a2num_TCF  ) / a2num_all).filled(0.0)
        da2rfreq["TCFC"]   = (ma.masked_where(a2num_all==0.0, a2num_TCFC ) / a2num_all).filled(0.0)
        da2rfreq["TCB"]    = (ma.masked_where(a2num_all==0.0, a2num_TCB  ) / a2num_all).filled(0.0)
        da2rfreq["TCBC"]   = (ma.masked_where(a2num_all==0.0, a2num_TCBC ) / a2num_all).filled(0.0)
        ##
      
        #****************************************
        # write to file
        #----------------------------------------
        sodir_root = "/media/disk2/out/JRA25/sa.one/6hr/tagpr"
        sodir      = sodir_root + "/%04d-%04d/%s"%(iyear, eyear, season)
        ctrack_func.mk_dir(sodir)
        dsname    = {}
        for stag in ltag:
          dsname[stag]    =  sodir  + "/rfreq.%stc%02d.c%02d.f%02d.%04d-%04d.%s.%04.1f.%s.%s.sa.one" %(tctype, dist_tc/100, dist_c/100, dist_f/100, iyear, eyear, season, ptile, prtype, stag)
          da2rfreq[stag].tofile(dsname[stag])
          print dsname[stag] 
    
      ##****************************************
      ## draw figure
      ##----------------------------------------
      sodir_root = "/media/disk2/out/JRA25/sa.one/6hr/tagpr"
      sodir      = sodir_root + "/%04d-%04d/%s"%(iyear, eyear, season)
      figdir     = sodir + "/pict"
      ctrack_func.mk_dir(figdir)
      dsname     = {}
      dfigname   = {}
      da2frac    = {}
      for stag in ltag:
        #-- name --
        dsname[stag]    =  sodir  + "/rfreq.%stc%02d.c%02d.f%02d.%04d-%04d.%s.%04.1f.%s.%s.sa.one" %(tctype, dist_tc/100, dist_c/100, dist_f/100, iyear, eyear, season, ptile, prtype, stag)
        dfigname[stag]   =  figdir + "/rfreq.%stc%02d.c%02d.f%02d.%04d-%04d.%s.%04.1f.%s.%s.png" %(tctype, dist_tc/100, dist_c/100, dist_f/100, iyear, eyear, season, ptile, prtype, stag)


    
        #-- settings --
        bnd    = [5,10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]
        cbarname = figdir + "/rfreq.cbar.png"
        #
        stitle   = "rfreq %04.1f %s: season:%s %s %04d-%04d %stc%02d c%02d f%02d"%(ptile, stag, season, prtype, iyear, eyear, tctype, dist_tc/100, dist_c/100, dist_f/100)
        mycm     = "Spectral_r"
        datname  = dsname[stag]
        figname  = dfigname[stag]
    
        #-- loaad -----
        a2figdat = fromfile(datname, float32).reshape(ny,nx)
        a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
    
        #-- draw ------
        ctrack_fig.mk_pict_saone_reg(a2figdat, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon)
        print figname
   



