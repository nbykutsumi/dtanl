from numpy import *
import ctrack_func, cmip_func
import ctrack_para, cmip_para, tc_para, chart_para
import ctrack_fig
#**********************************************
#lmodel=["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
#lmodel=["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel  = ["GFDL-CM3"]
lexpr   = ["historical", "rcp85"]
#lexpr   = ["rcp85"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
#dyrange = {"historical":[1980,1980], "rcp85":[2080,2080]}
lseason = ["ALL"]

dist_tc = 1000 #[km]
dist_c  = 1000 #[km]
dist_f  = 500 #[km]

nx,ny   =[360,180]

thdura_c    = 48
thdura_tc   = thdura_c
miss      = -9999.0

lstype = ["cf","c","tc","fbc","ot"]
#lstype = ["c"]
#---------------------
region    = "GLOB"
lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region)
#**********************************************
llkey = [[season,model,expr] for season in lseason for model in lmodel for expr in lexpr]
for season, model, expr in llkey:
  #------
  ens   = cmip_para.ret_ens(model, expr, "psl")
  sunit, scalendar = cmip_para.ret_unit_calendar(model,expr)
  iyear,eyear  = dyrange[expr]
  lyear        = range(iyear,eyear+1)
  lmon         = ctrack_para.ret_lmon(season)

  #-- init ---
  a2zero    = zeros([ny,nx],float32)
  #a2pr_plain= zeros([ny,nx],float32)
  a2pr_c    = zeros([ny,nx],float32)
  a2pr_tc   = zeros([ny,nx],float32)
  a2pr_f    = zeros([ny,nx],float32)
  a2pr_ot   = zeros([ny,nx],float32)

  a2num_c    = zeros([ny,nx],float32)
  a2num_tc   = zeros([ny,nx],float32)
  a2num_f    = zeros([ny,nx],float32)
  a2num_ot   = zeros([ny,nx],float32)

  #-----------
  for year in lyear:
    for mon in lmon:
      print season,model,expr,year,mon
      idir_root  = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/tagpr/c%02dh.tc%02dh"%(model,expr,thdura_c,thdura_tc)
      idir       = idir_root + "/%04d%02d"%(year,mon)
      #*** load *********
      #iprname_plain= idir + "/pr.plain.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, year, mon)
      iprname_c    = idir + "/pr.c.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, year, mon)
      iprname_tc   = idir + "/pr.tc.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, year, mon)
      iprname_f    = idir + "/pr.fbc.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, year, mon)
      iprname_ot   = idir + "/pr.ot.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, year, mon)

      inumname_c   = idir + "/num.c.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, year, mon)
      inumname_tc  = idir + "/num.tc.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, year, mon)
      inumname_f   = idir + "/num.fbc.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, year, mon)
      inumname_ot  = idir + "/num.ot.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, year, mon)

      #a2tmppr_plain= fromfile(iprname_plain, float32).reshape(ny,nx)
      a2tmppr_c    = fromfile(iprname_c,     float32).reshape(ny,nx)
      a2tmppr_tc   = fromfile(iprname_tc,    float32).reshape(ny,nx)
      a2tmppr_f    = fromfile(iprname_f,     float32).reshape(ny,nx)
      a2tmppr_ot   = fromfile(iprname_ot,    float32).reshape(ny,nx)

      a2tmpnum_c   = fromfile(inumname_c,    float32).reshape(ny,nx)
      a2tmpnum_tc  = fromfile(inumname_tc,   float32).reshape(ny,nx)
      a2tmpnum_f   = fromfile(inumname_f,    float32).reshape(ny,nx)
      a2tmpnum_ot  = fromfile(inumname_ot,   float32).reshape(ny,nx)

      #a2pr_plain   = a2pr_plain + a2tmppr_plain
      a2pr_c       = a2pr_c     + a2tmppr_c 
      a2pr_tc      = a2pr_tc    + a2tmppr_tc 
      a2pr_f       = a2pr_f     + a2tmppr_f
      a2pr_ot      = a2pr_ot    + a2tmppr_ot

      a2num_c      = a2num_c  + a2tmpnum_c 
      a2num_tc     = a2num_tc + a2tmpnum_tc 
      a2num_f      = a2num_f  + a2tmpnum_f
      a2num_ot     = a2num_ot + a2tmpnum_ot

  #**********************
  # make output data
  #----------------------
  totaltimes = cmip_para.ret_totaldays_cmip(iyear,eyear,season,sunit,scalendar) 
  mons       = len(lyear)*len(lmon)
  #** pr (mm/s) ***
  #a2pr_plain =  a2pr_plain/mons
  a2pr_c     =  a2pr_c    /mons
  a2pr_tc    =  a2pr_tc   /mons 
  a2pr_f     =  a2pr_f    /mons 
  a2pr_ot    =  a2pr_ot   /mons 

  #** pint (mm/s) ***
  a2pint_c     =  ( ma.masked_where( a2num_c  ==0.0, a2pr_c  )  / a2num_c  ).filled(0.0) *totaltimes
  a2pint_tc    =  ( ma.masked_where( a2num_tc ==0.0, a2pr_tc )  / a2num_tc ).filled(0.0) *totaltimes
  a2pint_f     =  ( ma.masked_where( a2num_f  ==0.0, a2pr_f  )  / a2num_f  ).filled(0.0) *totaltimes
  a2pint_ot    =  ( ma.masked_where( a2num_ot ==0.0, a2pr_ot )  / a2num_ot ).filled(0.0) *totaltimes

  #** freq (unitless) ***
  a2freq_c     = a2num_c  / totaltimes
  a2freq_tc    = a2num_tc / totaltimes
  a2freq_f     = a2num_f  / totaltimes
  a2freq_ot    = a2num_ot / totaltimes

  #** ExC + Front *******
  a2num_cf     = a2num_c +  a2num_f
  a2pr_cf      = a2pr_c  +  a2pr_f
  a2pint_cf    =  ( ma.masked_where( a2num_cf ==0.0, a2pr_cf )  / a2num_cf ).filled(0.0) *totaltimes
  a2freq_cf    = a2num_cf / totaltimes
  #**********************
  odir_root  = idir_root
  odir       = odir_root + "/%04d-%04d.%s"%(iyear,eyear,season)
  ctrack_func.mk_dir(odir)
 
  oprname_plain= odir + "/pr.plain.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)
  oprname_c    = odir + "/pr.c.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)
  oprname_tc   = odir + "/pr.tc.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)
  oprname_f    = odir + "/pr.fbc.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)
  oprname_ot   = odir + "/pr.ot.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)
  oprname_cf   = odir + "/pr.cf.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)

  ofreqname_c   = odir + "/freq.c.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)
  ofreqname_tc  = odir + "/freq.tc.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)
  ofreqname_f   = odir + "/freq.fbc.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)
  ofreqname_ot  = odir + "/freq.ot.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)
  ofreqname_cf  = odir + "/freq.cf.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)

  opintname_c   = odir + "/pint.c.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)
  opintname_tc  = odir + "/pint.tc.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)
  opintname_f   = odir + "/pint.fbc.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)
  opintname_ot  = odir + "/pint.ot.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)
  opintname_cf  = odir + "/pint.cf.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)

  #***********************
  #a2pr_plain.tofile(oprname_plain)
  a2pr_c .tofile(oprname_c)
  a2pr_tc.tofile(oprname_tc)
  a2pr_f .tofile(oprname_f)
  a2pr_ot.tofile(oprname_ot)
  a2pr_cf.tofile(oprname_cf)

  a2freq_c .tofile(ofreqname_c)
  a2freq_tc.tofile(ofreqname_tc)
  a2freq_f .tofile(ofreqname_f)
  a2freq_ot.tofile(ofreqname_ot)
  a2freq_cf.tofile(ofreqname_cf)

  a2pint_c .tofile(opintname_c)
  a2pint_tc.tofile(opintname_tc)
  a2pint_f .tofile(opintname_f)
  a2pint_ot.tofile(opintname_ot)
  a2pint_cf.tofile(opintname_cf)

  print opintname_c

  #***********************
  # Figure
  #-------------------
  #--- shade       ------
  thorog     = ctrack_para.ret_thorog()
  orogname   = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog/orog.%s.sa.one"%(model,expr,model)
  a2orog     = fromfile(orogname, float32).reshape(ny,nx)
  a2one    = ones([ny,nx],float32)
  a2shade  = ma.masked_where( a2orog >=thorog, a2one).filled(miss)
  #----------

  for stype in lstype:
    totaltimes   = cmip_para.ret_totaldays_cmip(iyear,eyear,season,sunit,scalendar) 
    #*******************************
    # Prec
    #-----------
    bnd        = [10,20,40,80,160]
    #bnd        = [10,30,50,70,90]
    #----------
    stitle   = "mm/month %s %s %s season:%s %04d-%04d %s"%(model,expr,ens,season,iyear, eyear,stype)
    mycm     = "Spectral"

    datdir     = idir_root + "/%04d-%04d.%s"%(iyear,eyear,season)
    datname    = datdir + "/pr.%s.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(stype,model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)
    figname    = datname[:-7] + ".png"
    cbarname   = datname[:-7] + ".cbar.png"


    a2figdat = fromfile(datname,float32).reshape(ny,nx) *60*60*24.*totaltimes /mons  # (mm/month)
   
    #-------------------------------
    ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
    print figname



