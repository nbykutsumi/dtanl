from numpy import *
import ctrack_func, cmip_func
import ctrack_para, cmip_para, tc_para, chart_para
import ctrack_fig

#lmodel=["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel  = ["MIROC5"]
exprhis = "historical"
lexprfut = ["rcp85"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
#dyrange = {"historical":[1980,1981], "rcp85":[2080,2081]}
lseason = ["ALL"]

ny,nx   = 180,360
miss    = -9999.
#---------------------
#region    = "GLOB"
region    = "JPN"
lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region)
#**********************************************
llkey = [[season,exprfut,model] for season in lseason for exprfut in lexprfut for model in lmodel]

for season, exprfut, model in llkey:
  #------
  ens   = cmip_para.ret_ens(model, exprfut, "psl")
  sunit, scalendar = cmip_para.ret_unit_calendar(model,exprfut)
  iyear_fut,eyear_fut  = dyrange[exprfut]
  iyear_his,eyear_his  = dyrange[exprhis]

  lyear        = range(iyear_fut,eyear_fut+1)
  lmon         = ctrack_para.ret_lmon(season)
  #------
  futdir   = "/media/disk2/data/CMIP5/sa.one.%s.%s/pr/%04d-%04d.%s"%(model,exprfut,iyear_fut,eyear_fut,season)
  hisdir   = "/media/disk2/data/CMIP5/sa.one.%s.%s/pr/%04d-%04d.%s"%(model,exprhis,iyear_his,eyear_his,season)

  futname  = futdir + "/pr.%s.%s.%s.%04d-%04d.%s.sa.one"%(model,exprfut,ens,iyear_fut,eyear_fut,season)
  hisname  = hisdir + "/pr.%s.%s.%s.%04d-%04d.%s.sa.one"%(model,exprhis,ens,iyear_his,eyear_his,season)
  
  a2fut    = fromfile(futname, float32).reshape(ny,nx)
  a2his    = fromfile(hisname, float32).reshape(ny,nx)

  a2dif    = a2fut - a2his

  odir     = futdir
  difname  = odir   + "/dif.pr.%s.%s.%s.%04d-%04d.%s.sa.one"%(model,exprfut,ens,iyear_fut,eyear_fut,season)
  a2dif.tofile(difname)
  #*******************************
  # Figure
  #-----------
  #--- shade   ------
  ens   = cmip_para.ret_ens(model, exprfut, "psl")
  thorog     = ctrack_para.ret_thorog()
  orogname   = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog/orog.%s.sa.one"%(model,"historical",model)
  a2orog     = fromfile(orogname, float32).reshape(ny,nx)
  a2one    = ones([ny,nx],float32)
  a2shade  = ma.masked_where( a2orog >=thorog, a2one).filled(miss)
  #----------
  bnd        = [-20,-15,-10,-5,5,10,15,20]
  #----------
  stitle   = "dif. mm/month %s %s %s season:%s %04d-%04d"%(model,exprfut,ens,season,iyear_fut, eyear_fut)
  mycm     = "RdBu"

  datdir_root= "/".join(futdir.split("/")[:-1])
  datdir     = datdir_root + "/%04d-%04d.%s"%(iyear_fut, eyear_fut, season)
  datname    = datdir    + "/dif.pr.%s.%s.%s.%04d-%04d.%s.sa.one"%(model,exprfut,ens,iyear_fut,eyear_fut,season)
  #----
  if region == "GLOB":
    bnd        = [-40,-20,-10,-5,5,10,20,40]
    figdir     = datdir
  if region == "JPN":
    bnd        = [-40,-20,-10,-5,5,10,20,40]
    figdir     = datdir_root + "/%04d-%04d.%s.%s"%(iyear_fut,eyear_fut,season,region)
  #----
  totaltimes   = cmip_para.ret_totaldays_cmip(iyear_fut,eyear_fut,season,sunit,scalendar)
  mons         = len(lyear)*len(lmon)

  a2figdat = fromfile(datname,float32).reshape(ny,nx) *60*60*24.*totaltimes /mons  # (mm/month)
  cbarname   = figdir + "/dif.pr.cbar.png"
  figname    = figdir + "/" + datname.split("/")[-1][:-7] + ".png"
  ctrack_func.mk_dir(figdir)
  #-------------------------------
  ctrack_fig.mk_pict_saone_reg_symm(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
  print figname
  
  
