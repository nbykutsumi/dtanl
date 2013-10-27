from numpy import *
import ctrack_func, cmip_func
import ctrack_para, cmip_para, chart_para
import calendar
import datetime, os, netCDF4
#***************************************
#lmodel=["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel=["GFDL-CM3"]
lexpr   = ["historical", "rcp85"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
#dyrange = {"historical":[1980,1981], "rcp85":[2080,2081]}

lmon    = range(1,12+1)
stepday = 1.0
miss      = -9999.0
ny,nx   = 180,360
#---------------------
region    = "GLOB"
lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region)
#---------------------

#***************************************
llkey = [[model,expr] for model in lmodel for expr in lexpr]
for model, expr in llkey:
  #------
  iyear,eyear  = dyrange[expr]
  ens   = cmip_para.ret_ens(model, expr, "psl")
  sunit, scalendar = cmip_para.ret_unit_calendar(model,expr)
  a1dtime,a1tnum   = cmip_func.ret_times(iyear,eyear,lmon,sunit,scalendar,stepday,model=model)
  #--------------------------------
  a2one    = ones([ny,nx],float32)
  a2zero   = zeros([ny,nx],float32)
  #--------------------------------
  for year in range(iyear, eyear+1):
    #-----------------
    for mon in lmon:
      eday = cmip_para.ret_totaldays_cmip(year,year,mon,sunit,scalendar)
      #** init precip ******
      a2pr = a2zero.copy()

      #*********************
      for dtime, tnum in map(None, a1dtime, a1tnum):
        yearloop, monloop, dayloop = dtime.year, dtime.month, dtime.day
        #--- check year and month ---
        if not (yearloop==year)&(monloop==mon):
          continue
        #----------------------------

        print "agg.pr.plain.cmip", model, expr, yearloop,monloop,dayloop


        #-- load prec ---
        prdir    = "/media/disk2/data/CMIP5/sa.one.%s.%s/pr/%04d%02d"%(model,expr,yearloop,monloop)
        prname   = prdir + "/pr.%s.%04d%02d%02d.sa.one"%(ens,yearloop,monloop,dayloop)

        a2pr_tmp = fromfile( prname, float32).reshape(ny,nx)
        a2pr_tmp = ma.masked_equal(a2pr_tmp, miss).filled(0.0)
        a2pr     = a2pr + a2pr_tmp
      #*********************
      totaltimes = cmip_para.ret_totaldays_cmip(year,year,mon,sunit,scalendar)
      print "totaltimes",totaltimes
      a2pr       = a2pr / totaltimes

      #*********************
      #  write
      sodir      = prdir
      ctrack_func.mk_dir(sodir)
      #
      soname     = sodir  + "/pr.%s.%04d%02d.sa.one"%(ens,year,mon)
      a2pr.tofile(soname)
      print soname


