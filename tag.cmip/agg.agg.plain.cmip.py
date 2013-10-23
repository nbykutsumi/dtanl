from numpy import *
import ctrack_func, cmip_func
import ctrack_para, cmip_para, tc_para, chart_para
import ctrack_fig
#*******************************************
#lmodel=["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel=["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lexpr   = ["historical", "rcp85"]
#lexpr   = ["rcp85"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
#dyrange = {"historical":[1980,1980], "rcp85":[2080,2080]}
lseason = ["ALL"]
miss    = -9999.0
ny,nx   = 180,360
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
  a2pr      = zeros([ny,nx],float32)
  #*******************************
  idir_root = "/media/disk2/data/CMIP5/sa.one.%s.%s/pr"%(model,expr)

  for year in lyear:
    for mon in lmon:
      print year,mon
      idir    = idir_root + "/%04d%02d"%(year,mon)
      iname   = idir      + "/pr.%s.%04d%02d.sa.one"%(ens,year,mon)
      a2pr_tmp = fromfile(iname, float32).reshape(ny,nx)  
      a2pr     = a2pr + a2pr_tmp
  #*******************************
  a2pr = a2pr / len(lyear) / len(lmon) 
  odir_root = idir_root
  odir      = odir_root + "/%04d-%04d.%s"%(iyear,eyear,season)
  ctrack_func.mk_dir(odir)
  oname     = odir  + "/pr.%s.%s.%s.%04d-%04d.%s.sa.one"%(model,expr,ens,iyear,eyear,season)
  a2pr.tofile(oname)


  #*******************************
  # Figure
  #------
  #--- shade       ------
  thorog     = ctrack_para.ret_thorog()
  orogname   = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog/orog.%s.sa.one"%(model,expr,model)
  a2orog     = fromfile(orogname, float32).reshape(ny,nx)
  a2one    = ones([ny,nx],float32)
  a2shade  = ma.masked_where( a2orog >=thorog, a2one).filled(miss)
  #----------

  ens   = cmip_para.ret_ens(model, expr, "psl")
  sunit, scalendar = cmip_para.ret_unit_calendar(model,expr)
  iyear,eyear  = dyrange[expr]
  lyear        = range(iyear,eyear+1)
  lmon         = ctrack_para.ret_lmon(season)
  totaltimes   = cmip_para.ret_totaldays_cmip(iyear,eyear,season,sunit,scalendar)
  mons         = len(lyear)*len(lmon)
  #*******************************
  # Prec
  #-----------
  bnd        = [10,20,40,80,160]
  #bnd        = [10,30,50,70,90]
  #----------
  stitle   = "mm/month %s %s %s season:%s %04d-%04d"%(model,expr,ens,season,iyear, eyear)
  mycm     = "Spectral"

  datdir_root= "/media/disk2/data/CMIP5/sa.one.%s.%s/pr"%(model,expr)
  datdir     = idir_root + "/%04d-%04d.%s"%(iyear,eyear,season)
  datname    = datdir    + "/pr.%s.%s.%s.%04d-%04d.%s.sa.one"%(model,expr,ens,iyear,eyear,season)
  figname    = datname[:-7] + ".png"
  cbarname   = datname[:-7] + ".cbar.png"


  a2figdat = fromfile(datname,float32).reshape(ny,nx) *60*60*24.*totaltimes /mons  # (mm/month)

  #-------------------------------
  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
  print figname



