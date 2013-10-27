from numpy import *
import ctrack_func, cmip_func
import ctrack_para, cmip_para, tc_para, chart_para
import ctrack_fig
#**********************************************
calcflag= True
#calcflag= False
#lmodel  = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel  = ["GFDL-CM3"]
exprhis = "historical"
exprfut = "rcp85"
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
#dyrange = {"historical":[1980,1981], "rcp85":[2080,2081]}
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
#region    = "JPN"
lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region)
#**********************************************
llkey = [[season,model] for season in lseason for model in lmodel]

if calcflag == False:
  print "********************"
  print "Calcflag = False"
  print "********************"
if calcflag == True:
  for season, model in llkey:
  
    da2num  = {}
    da2pint = {}
    da2pr   = {}
  
    for expr in [exprhis, exprfut]:
      #------
      ens   = cmip_para.ret_ens(model, expr, "psl")
      sunit, scalendar = cmip_para.ret_unit_calendar(model,expr)
      iyear,eyear  = dyrange[expr]
      lyear        = range(iyear,eyear+1)
      lmon         = ctrack_para.ret_lmon(season)
    
      #-- init ---
      a2zero   = zeros([ny,nx],float32)
      a2pr_c   = zeros([ny,nx],float32)
      a2pr_tc  = zeros([ny,nx],float32)
      a2pr_f   = zeros([ny,nx],float32)
      a2pr_ot  = zeros([ny,nx],float32)
    
      a2num_c   = zeros([ny,nx],float32)
      a2num_tc  = zeros([ny,nx],float32)
      a2num_f   = zeros([ny,nx],float32)
      a2num_ot  = zeros([ny,nx],float32)
    
      #-----------
      for year in lyear:
        for mon in lmon:
          print season,model,expr,year,mon
          idir_root  = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/tagpr/c%02dh.tc%02dh"%(model,expr,thdura_c,thdura_tc)
          idir       = idir_root + "/%04d%02d"%(year,mon)
          #*** load *********
          iprname_c   = idir + "/pr.c.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, year, mon)
          iprname_tc  = idir + "/pr.tc.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, year, mon)
          iprname_f   = idir + "/pr.fbc.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, year, mon)
          iprname_ot  = idir + "/pr.ot.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, year, mon)
    
          inumname_c  = idir + "/num.c.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, year, mon)
          inumname_tc = idir + "/num.tc.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, year, mon)
          inumname_f  = idir + "/num.fbc.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, year, mon)
          inumname_ot = idir + "/num.ot.%s.%s.%s.tc%04d.c%04d.f%04d.%04d.%02d.sa.one"%(model,expr,ens,dist_tc, dist_c, dist_f, year, mon)
    
          a2tmppr_c   = fromfile(iprname_c,   float32).reshape(ny,nx)
          a2tmppr_tc  = fromfile(iprname_tc,  float32).reshape(ny,nx)
          a2tmppr_f   = fromfile(iprname_f,   float32).reshape(ny,nx)
          a2tmppr_ot  = fromfile(iprname_ot,  float32).reshape(ny,nx)
    
          a2tmpnum_c  = fromfile(inumname_c,   float32).reshape(ny,nx)
          a2tmpnum_tc = fromfile(inumname_tc,  float32).reshape(ny,nx)
          a2tmpnum_f  = fromfile(inumname_f,   float32).reshape(ny,nx)
          a2tmpnum_ot = fromfile(inumname_ot,  float32).reshape(ny,nx)
    
          a2pr_c      = a2pr_c  + a2tmppr_c 
          a2pr_tc     = a2pr_tc + a2tmppr_tc 
          a2pr_f      = a2pr_f  + a2tmppr_f
          a2pr_ot     = a2pr_ot + a2tmppr_ot
    
          a2num_c     = a2num_c  + a2tmpnum_c 
          a2num_tc    = a2num_tc + a2tmpnum_tc 
          a2num_f     = a2num_f  + a2tmpnum_f
          a2num_ot    = a2num_ot + a2tmpnum_ot
  
      #**********************
      # make output data
      #----------------------
      totaltimes = cmip_para.ret_totaldays_cmip(iyear,eyear,season,sunit,scalendar) 
      mons       = len(lyear)*len(lmon)
      #** pr (mm/s) ***
      a2pr_c     =  a2pr_c   /mons
      a2pr_tc    =  a2pr_tc  /mons 
      a2pr_f     =  a2pr_f   /mons 
      a2pr_ot    =  a2pr_ot  /mons 
    
      #** pint (mm/s) = (mm/s) / (day/season) * (day/season)  ***
      a2pint_c     =  ( ma.masked_where( a2num_c  ==0.0, a2pr_c  )  / a2num_c  ).filled(0.0) *totaltimes
      a2pint_tc    =  ( ma.masked_where( a2num_tc ==0.0, a2pr_tc )  / a2num_tc ).filled(0.0) *totaltimes
      a2pint_f     =  ( ma.masked_where( a2num_f  ==0.0, a2pr_f  )  / a2num_f  ).filled(0.0) *totaltimes
      a2pint_ot    =  ( ma.masked_where( a2num_ot ==0.0, a2pr_ot )  / a2num_ot ).filled(0.0) *totaltimes

      #** ExC + Front ****
      a2num_cf     = a2num_c + a2num_f
      a2pr_cf      = a2pr_c  + a2pr_f    # no need to be devided by "mons" here
      a2pint_cf    =  ( ma.masked_where( a2num_cf ==0.0, a2pr_cf )  / a2num_cf ).filled(0.0) *totaltimes
    
      #** dictionary ********
      print "AA",expr
      da2num[expr,"c"  ]  = a2num_c
      da2num[expr,"tc" ]  = a2num_tc
      da2num[expr,"fbc"]  = a2num_f
      da2num[expr,"ot" ]  = a2num_ot
      da2num[expr,"cf" ]  = a2num_cf
 
       
      da2pint[expr,"c"  ]  = a2pint_c
      da2pint[expr,"tc" ]  = a2pint_tc
      da2pint[expr,"fbc"]  = a2pint_f
      da2pint[expr,"ot" ]  = a2pint_ot
      da2pint[expr,"cf" ]  = a2pint_cf
  
      da2pr[expr,"c"  ]  = a2pr_c
      da2pr[expr,"tc" ]  = a2pr_tc
      da2pr[expr,"fbc"]  = a2pr_f
      da2pr[expr,"ot" ]  = a2pr_ot
      da2pr[expr,"cf" ]  = a2pr_cf
   
    #************************
    # decomposite
    #------------------------
    for stype in lstype:
      a2num    = da2num [exprhis, stype]            # day/season
      a2pint   = da2pint[exprhis, stype]*60*60*24.0 # mm/day
  
      a2dnum   = da2num [exprfut, stype] - da2num [exprhis, stype]  # day/season
      a2dpint  = (da2pint[exprfut, stype] - da2pint[exprhis, stype])*60*60*24.0 # mm/day
  
      #- day/season * mm/day = mm/season
      a2NdI    = a2num  * a2dpint
      a2dNI    = a2dnum * a2pint
      a2dNdI   = a2dnum * a2dpint
  
      #- mm/season --> mm/sec
      a2NdI    = a2NdI  / totaltimes / (60*60*24.)
      a2dNI    = a2dNI  / totaltimes / (60*60*24.)
      a2dNdI   = a2dNdI / totaltimes / (60*60*24.)
      a2dpr1   = a2NdI + a2dNI + a2dNdI 
      a2dpr2   = da2pr[exprfut,stype] - da2pr[exprhis,stype]
  
      #*** names *************
      odir_root  = idir_root
      odir       = odir_root + "/%04d-%04d.%s.decomp"%(iyear,eyear,season)
      ctrack_func.mk_dir(odir)
    
      NdIname    = odir + "/dpr.%s.NdI.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(stype,model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)
      dNIname    = odir + "/dpr.%s.dNI.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(stype,model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)
      dNdIname   = odir + "/dpr.%s.dNdI.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(stype,model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)
      dprname1   = odir + "/dpr.%s.dtot.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(stype,model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)
      #dprname2   = odir + "/dpr2.%s.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(stype,model,expr,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)
  
      #*** write *************
      a2NdI   .tofile(NdIname )
      a2dNI   .tofile(dNIname )
      a2dNdI  .tofile(dNdIname)
      a2dpr1  .tofile(dprname1)
      #a2dpr2  .tofile(dprname2)
      print "WRITE"
      print NdIname


#***********************
# Figure
#-------------------
for season, model in llkey:
  ens   = cmip_para.ret_ens(model, exprfut, "psl")
  sunit, scalendar = cmip_para.ret_unit_calendar(model,exprfut)
  iyear,eyear  = dyrange[exprfut]
  lyear        = range(iyear,eyear+1)
  lmon         = ctrack_para.ret_lmon(season)

  totaltimes = cmip_para.ret_totaldays_cmip(iyear,eyear,season,sunit,scalendar) 
  mons       = len(lyear)*len(lmon)
  #--- shade   ------
  ens   = cmip_para.ret_ens(model, exprfut, "psl")
  thorog     = ctrack_para.ret_thorog()
  orogname   = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog/orog.%s.sa.one"%(model,"historical",model)
  a2orog     = fromfile(orogname, float32).reshape(ny,nx)
  a2one    = ones([ny,nx],float32)
  a2shade  = ma.masked_where( a2orog >=thorog, a2one).filled(miss)
  #******************
  # Figure NdI, dNI, dNdI
  #------------------
  for stype in lstype:
    for dectype in ["dtot","NdI","dNI","dNdI"]:
      #-----------
      #----------
      mycm     = "RdBu"
      datdir_root= "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/tagpr/c%02dh.tc%02dh"%(model,exprfut,thdura_c,thdura_tc)
      datdir     = datdir_root + "/%04d-%04d.%s.decomp"%(iyear,eyear,season)

      #----
      if region == "GLOB":
        bnd        = [-20,-15,-10,-5,5,10,15,20]
        figdir     = datdir
      if region == "JPN":
        bnd        = [-10,-7,-4,-1,1,4,7,10]
        figdir     = datdir_root + "/%04d-%04d.%s.decomp.%s"%(iyear,eyear,season,region)
      #----

      stitle   = "mm/month %s %s %s season:%s %s %s %04d-%04d"%(model,exprfut,ens,season,stype, dectype, iyear, eyear)
      datname    = datdir + "/dpr.%s.%s.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"%(stype, dectype, model,exprfut,ens,dist_tc, dist_c, dist_f, iyear, eyear, season)



      #cbarname   = datname[:-7] + ".cbar.png"
      cbarname   = figdir + "/dpr.cbar.png"

      a2figdat = fromfile(datname,float32).reshape(ny,nx) *60*60*24.*totaltimes /mons  # (mm/month)
      figname    = figdir + "/" + datname.split("/")[-1][:-7] + ".png"
      ctrack_func.mk_dir(figdir) 
      #-------------------------------
      ctrack_fig.mk_pict_saone_reg_symm(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
      print figname


