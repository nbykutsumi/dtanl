from numpy import *
import ctrack_func, cmip_func
import ctrack_para, cmip_para, tc_para, chart_para
import ctrack_fig
#**********************************************
#calcflag= True
calcflag= False
#lmodel  = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel  = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
#lmodel  = ["GFDL-CM3"]
exprhis = "historical"
exprfut = "rcp85"
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
#dyrange = {"historical":[1980,1981], "rcp85":[2080,2081]}
lseason = ["ALL"]

nx,ny   =[360,180]

miss      = -9999.0

#---------------------
#region    = "GLOB"
region    = "JPN"
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
      a2pr     = zeros([ny,nx],float32)
      a2one    = ones ([ny,nx],float32)
      #-----------
      for year in lyear:
        for mon in lmon:
          print season,model,expr,year,mon
          prdir    = "/media/disk2/data/CMIP5/sa.one.%s.%s/pr/%04d%02d"%(model,expr,year,mon)
          iprname  = prdir + "/pr.%s.%04d%02d.sa.one"%(ens,year,mon)

          #*** load *********
          a2tmppr  = fromfile(iprname,   float32).reshape(ny,nx)
          a2pr     = a2pr  + a2tmppr 
  
      #**********************
      # make output data
      #----------------------
      mons       = len(lyear)*len(lmon)
      #** pr (mm/s) ***
      a2pr       =  a2pr   /mons
    
      #** dictionary ********
      print "AA",expr
  
      da2pr[expr  ] = a2pr
   
    #************************
    # decomposite
    #------------------------
    #- mm/season --> mm/sec
    a2dpr    = da2pr[exprfut]  - da2pr[exprhis]
  
    #*** names *************
    odir_root  = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/dpr.plain"%(model,exprfut)
    odir       = odir_root + "/%04d-%04d.%s.decomp"%(iyear,eyear,season)
    ctrack_func.mk_dir(odir)
    
    dprname    = odir + "/dpr.plain.dtot.%s.%s.%s.%04d-%04d.%s.sa.one"%(model,expr,ens,iyear, eyear, season)
  
    #*** write *************
    #a2NdI   .tofile(NdIname )
    #a2dNI   .tofile(dNIname )
    #a2dNdI  .tofile(dNdIname)
    a2dpr   .tofile(dprname)
    print "WRITE"
    print NdIname


#***********************
# Figure
#-------------------
llkey = [[season,model] for season in lseason for model in lmodel]
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
  for dectype in ["dtot"]:
    #-----------
    #----------
    mycm        = "RdBu"
    datdir_root = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/dpr.plain"%(model,exprfut)
    datdir      = datdir_root + "/%04d-%04d.%s.decomp"%(iyear,eyear,season)

    #----
    if region == "GLOB":
      bnd        = [-20,-15,-10,-5,5,10,15,20]
      figdir     = datdir
    if region == "JPN":
      bnd        = [-10,-7,-4,-1,1,4,7,10]
      figdir     = datdir_root + "/%04d-%04d.%s.decomp.%s"%(iyear,eyear,season,region)
    #----

    stitle   = "mm/month %s %s %s season:%s %s %04d-%04d"%(model,exprfut,ens,season,dectype, iyear, eyear)
    datname    = datdir + "/dpr.plain.%s.%s.%s.%s.%04d-%04d.%s.sa.one"%(dectype, model,exprfut,ens,iyear, eyear, season)



    #cbarname   = datname[:-7] + ".cbar.png"
    cbarname   = figdir + "/dpr.cbar.png"

    a2figdat = fromfile(datname,float32).reshape(ny,nx) *60*60*24.*totaltimes /mons  # (mm/month)
    figname    = figdir + "/" + datname.split("/")[-1][:-7] + ".png"
    ctrack_func.mk_dir(figdir) 
    #-------------------------------
    ctrack_fig.mk_pict_saone_reg_symm(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
    print figname


