from tag_fsub import *
from numpy import *
import ctrack_para, ctrack_func, ctrack_fig, chart_para, cmip_para, cmip_func
import calendar
import datetime
import os
import netCDF4
#---------------------------
#singletime = True
singletime = False
calcflag   = True
#calcflag   = True
lbstflag    = [True]
#lbstflag   = [False]

lmodel  = ["MIROC5"]
#lexpr   = ["historical", "rcp85"]
lexpr   = ["rcp85"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}

lmon    = range(1,12+1)
stepday = 1.0
#--------------------------------

dist_tc = 1000 #[km]
dist_c  = 1000 #[km]
dist_f  = 500 #[km]

nx,ny   =[360,180]

thdura_c    = 48
thdura_tc   = thdura_c

miss      = -9999.0

#---------------------
region    = "GLOB"
lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region)
#---------------------
timestep    = "day"
#--- lhour -----------------------
if timestep == "day":
  lhour = [0]
elif timestep == "6hr":
  lhour = [0,6,12,18]
elif timestep == "3hr":
  lhour = [0,3,6,9,12,15,18,21]

#--- corresponding tag time ------
lhtag_inc = [0,6,12,18,24]

#***************************************
llkey = [[model,expr] for model in lmodel for expr in lexpr]
for model, expr in llkey:
  #------
  iyear,eyear  = dyrange[expr]
  ens   = cmip_para.ret_ens(model, expr, "psl")
  sunit, scalendar = cmip_para.ret_unit_calendar(model,expr)
  a1dtime,a1tnum   = cmip_func.ret_times(iyear,eyear,lmon,sunit,scalendar,stepday)
  #--------------------------------
  a2one    = ones([ny,nx],float32)
  a2zero   = zeros([ny,nx],float32)
  #--------------------------------
  for year in range(iyear, eyear+1):
    #-----------------
    for mon in lmon:
      eday = cmip_para.ret_totaldays_cmip(year,year,mon,sunit,scalendar)

      #** init precip ******
      a2pr_all = a2zero.copy()
      a2pr_tc  = a2zero.copy()
      a2pr_c   = a2zero.copy()
      a2pr_fbc = a2zero.copy()
      a2pr_ot  = a2zero.copy()
      #** init num   *******
      a2num_tc  = a2zero.copy()
      a2num_c   = a2zero.copy()
      a2num_fbc = a2zero.copy()
      a2num_ot  = a2zero.copy()
      #********************* 

      for dtime, tnum in map(None, a1dtime, a1tnum):
        yearloop, monloop, dayloop = dtime.year, dtime.month, dtime.day
        #--- check year and month ---
        if not (yearloop==year)&(monloop==mon):
          continue
        #----------------------------

        print "agg.tag.cmip", model, expr, yearloop,monloop,dayloop
   

        #-- load prec ---
        prdir    = "/media/disk2/data/CMIP5/sa.one.%s.%s/pr/%04d%02d"%(model,expr,yearloop,monloop)
        prname   = prdir + "/pr.%s.%04d%02d%02d.sa.one"%(ens,yearloop,monloop,dayloop)

        a2pr     = fromfile( prname, float32).reshape(ny,nx)
        a2pr     = ma.masked_equal(a2pr, miss).filled(0.0)  

        #*****************************
        # load corresponding tags 
        #-----------------------------
        now   = datetime.datetime(yearloop, monloop, dayloop)
        #------------------
        a2tagtmp_tc    = a2zero
        a2tagtmp_c     = a2zero
        a2tagtmp_fbc   = a2zero
        a2tagtmp_ot    = a2zero
  
        #------------------ 
        for htag_inc in lhtag_inc:
          tnum_tag    = tnum + htag_inc/24.0
          target      = netCDF4.num2date(tnum_tag, units=sunit, calendar=scalendar)
          year_tag = target.year
          mon_tag  = target.month
          day_tag  = target.day
          hour_tag = target.hour
          #-- tag name ---
          tagdir_root     = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/tag/c%02dh.tc%02dh.tc%04d.c%04d.f%04d"%(model, expr, thdura_c, thdura_tc, dist_tc, dist_c, dist_f)
        
          tagdir     = tagdir_root + "/%04d%02d"%(year_tag,mon_tag)
          ctrack_func.mk_dir(tagdir_root)
          ctrack_func.mk_dir(tagdir)
        
          tagname     = tagdir + "/tag.tc%04d.c%04d.f%04d.%04d.%02d.%02d.%02d.sa.one"%(dist_tc, dist_c, dist_f, year_tag, mon_tag, day_tag, hour_tag)
  
          if not os.access(tagname, os.F_OK):
            print "AAAA"
            print "nofile", tagname
            if (yearloop==iyear)&(monloop==1)&(dayloop==1):
              continue
            elif (yearloop==eyear)&(monloop==12)&(dayloop>=eday):
              continue
          #-- load -------
          a2tag         = fromfile(tagname, int32).reshape(ny,nx)
          lout          = tag_fsub.solve_tag_4type(a2tag.T)
          a2tagtmp_tc   = a2tagtmp_tc   + array(lout[0].T, float32)
          a2tagtmp_c    = a2tagtmp_c    + array(lout[1].T, float32)
          a2tagtmp_fbc  = a2tagtmp_fbc  + array(lout[2].T, float32)
  
        ##
        a2tagtmp_tc    = ma.masked_greater(a2tagtmp_tc,  0.0).filled(1.0)
        a2tagtmp_c     = ma.masked_greater(a2tagtmp_c ,  0.0).filled(1.0)   
        a2tagtmp_fbc   = ma.masked_greater(a2tagtmp_fbc, 0.0).filled(1.0)
        a2tagtmp_ot    = ma.masked_where(a2tagtmp_tc + a2tagtmp_c + a2tagtmp_ot ==0.0, a2zero).filled(1.0)
        ##
        a2tag_all   = a2tagtmp_tc + a2tagtmp_c + a2tagtmp_fbc + a2tagtmp_ot
        ##
        a2tag_tc    = a2tagtmp_tc  / a2tag_all
        a2tag_c     = a2tagtmp_c   / a2tag_all
        a2tag_fbc   = a2tagtmp_fbc / a2tag_all
        a2tag_ot    = a2tagtmp_ot

        #******************************
        # count
        #------------------------------
        a2num_tc  = a2num_tc + a2tag_tc 
        a2num_c   = a2num_c  + a2tag_c 
        a2num_fbc = a2num_fbc+ a2tag_fbc 
        a2num_ot  = a2num_ot + a2tag_ot
        
 
        ##*****************************
        # weight precipitation
        #-----------------------------
        a2prtmp_tc   = ma.masked_less(a2pr,0.0).filled(0.0) * a2tag_tc
        a2prtmp_c    = ma.masked_less(a2pr,0.0).filled(0.0) * a2tag_c
        a2prtmp_fbc  = ma.masked_less(a2pr,0.0).filled(0.0) * a2tag_fbc
        a2prtmp_ot   = ma.masked_less(a2pr,0.0).filled(0.0) * a2tag_ot
  
        #*****************************
        # sum precipitation
        #-----------------------------

        a2pr_all     = a2pr_all + a2pr
        a2pr_tc      = a2pr_tc  + a2prtmp_tc
        a2pr_c       = a2pr_c   + a2prtmp_c
        a2pr_fbc     = a2pr_fbc + a2prtmp_fbc
        a2pr_ot      = a2pr_ot  + a2prtmp_ot

 
      #*****************************
      # convert unit --> mm/s
      #-----------------------
      totaltimes   = ctrack_para.ret_totaldays(year,year,mon)
      #
      a2pr_all    = a2pr_all   / totaltimes 
      a2pr_tc     = a2pr_tc    / totaltimes 
      a2pr_c      = a2pr_c     / totaltimes 
      a2pr_fbc    = a2pr_fbc   / totaltimes 
      a2pr_ot     = a2pr_ot    / totaltimes 
 
      #*****************************
      #-- save monthly data ---
      #-----------------------------
      sodir_root = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/tagpr/c%02dh.tc%02dh"%(model, expr, thdura_c, thdura_tc)
      #
      sodir      = sodir_root   + "/%04d%02d"%(year, mon)
      ctrack_func.mk_dir(sodir)
      #
      sname_all  =  sodir  + "/pr.plain.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one" %(model, expr, ens, dist_tc, dist_c, dist_f, year, mon)
      sname_tc   =  sodir  + "/pr.tc.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one" %(model, expr, ens, dist_tc, dist_c, dist_f, year, mon)
      sname_c    =  sodir  + "/pr.c.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"  %(model, expr, ens, dist_tc, dist_c, dist_f, year, mon)
      sname_fbc  =  sodir  + "/pr.fbc.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"%(model, expr, ens, dist_tc, dist_c, dist_f, year, mon)
      sname_ot   =  sodir  + "/pr.ot.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one" %(model, expr, ens, dist_tc, dist_c, dist_f, year, mon)

      numname_tc   =  sodir  + "/num.tc.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one" %(model, expr, ens, dist_tc, dist_c, dist_f, year, mon)
      numname_c    =  sodir  + "/num.c.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"  %(model, expr, ens, dist_tc, dist_c, dist_f, year, mon)
      numname_fbc  =  sodir  + "/num.fbc.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"%(model, expr, ens, dist_tc, dist_c, dist_f, year, mon)
      numname_ot   =  sodir  + "/num.ot.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one" %(model, expr, ens, dist_tc, dist_c, dist_f, year, mon)
  
      #-----------------------------
      a2pr_all.tofile(sname_all)
      a2pr_tc.tofile(sname_tc)
      a2pr_c.tofile(sname_c)
      a2pr_fbc.tofile(sname_fbc)
      a2pr_ot.tofile(sname_ot)
      print sname_c
  
      a2num_tc.tofile(numname_tc)
      a2num_c.tofile(numname_c)
      a2num_fbc.tofile(numname_fbc)
      a2num_ot.tofile(numname_ot)
      print numname_c
  

