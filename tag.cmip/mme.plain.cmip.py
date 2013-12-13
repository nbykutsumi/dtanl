from numpy import *
import ctrack_func, cmip_func
import ctrack_para, cmip_para, chart_para
import ctrack_fig
import calendar
import datetime, os, netCDF4
#***************************************
#lmodel=["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel=["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","GFDL-CM3"]
#lmodel=["GFDL-CM3"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
#dyrange = {"historical":[1980,1981], "rcp85":[2080,2081]}
lseason  = ["ALL"]
lexprfut = ["rcp85"]
lmon    = range(1,12+1)
stepday = 1.0
miss      = -9999.0
ny,nx   = 180,360
thprob  = 0.05
#---------------------
#region    = "GLOB"
region    = "JPN"
lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region)
#---------------------
#**********************************************
# FUNCTIONS
#****************
def combi(n,r):
  return math.factorial(n) / ( math.factorial(r)* math.factorial(n-r) )

#****************
def pcombi(n,r):
  p = 0.0
  for i in range(r,n+1):
    p = p + combi(n,i)
  #----
  p = p / (2.0**n)
  return p
#*****************
def mk_a2prob(a2n, a2r):
  a1n  = a2n.flatten()
  a1r  = a2r.flatten()
  a2prob = array( map( pcombi, a1n, a1r), float32).reshape(ny,nx)
  return a2prob

#*****************
print pcombi(9,8)
print pcombi(9,7)
#***************************************
#**********************************************
llkey = [[exprfut,season] for exprfut in lexprfut for season in lseason]
for exprfut, season in llkey:
  #** init ******
  a2one    = ones ([ny,nx],float32)
  a2mdpr   = zeros([ny,nx],float32)
  a2nposi  = zeros([ny,nx],float32)
  a2nnega  = zeros([ny,nx],float32)

  iyear,eyear  = dyrange[exprfut]
  lyear        = range(iyear,eyear+1)
  totaldays    = 0.0

  #--------------
  for model in lmodel:
    ens   = cmip_para.ret_ens(model, exprfut, "psl")
    sunit, scalendar = cmip_para.ret_unit_calendar(model,exprfut)
    totaldays_model = cmip_para.ret_totaldays_cmip(iyear,eyear,season,sunit,scalendar)
    totaldays       = totaldays + totaldays_model

    idir     = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/dpr.plain/%04d-%04d.%s.decomp"%(model,exprfut,iyear,eyear,season)
    dprname  = idir  + "/dpr.plain.dtot.%s.%s.%s.%04d-%04d.%s.sa.one"%(model,exprfut,ens,iyear,eyear,season)

    a2dprtmp = fromfile( dprname, float32).reshape(ny,nx)
    a2mdpr   = a2mdpr   + a2dprtmp
    a2nposi  = a2nposi  + ma.masked_where( a2dprtmp <= 0.0, a2one ).filled(0.0)
    a2nnega  = a2nnega  + ma.masked_where( a2dprtmp >= 0.0, a2one ).filled(0.0)

  #--------------
  a2mdpr     = a2mdpr / len(lmodel)
  totaldays  = totaldays / len(lmodel)
  #-- probability ---
  a2nsame    = array( ma.maximum(a2nposi, a2nnega), int32)
  a2nmodel   = array( ones([ny,nx],float32) * len(lmodel), int32)
  a2prob     = mk_a2prob( a2nmodel, a2nsame)
  #------------------

  a2shade    = ma.masked_where( a2prob > thprob, ones([ny,nx],float32)).filled(miss)
  #------------------
  odir     = "/media/disk2/out/CMIP5/sa.one.MME.%s/6hr/dpr.plain/%04d-%04d.%s.decomp"%(exprfut,iyear,eyear,season)
  ctrack_func.mk_dir(odir)
  oname    = odir + "/dpr.plain.dtot.MME.%s.%s.%04d-%04d.%s.sa.one"%(exprfut,ens,iyear,eyear,season)
  a2mdpr.tofile(oname)
  print oname

  #--------------
  # readme.txt
  #--------------
  sout = " ".join(lmodel)
  f=open(odir+"/readme.txt","w"); f.write(sout); f.close()

  #**************
  # Figure
  #--------------
  stitle   = "dif.plain mm/month MME %s %s season:%s %04d-%04d"%(exprfut,ens,season,iyear, eyear)
  #stitle   = stitle + "\n" + "%d out of %d models"%(nmodel, thres)
  mycm     = "RdBu"

  datdir     = odir
  datname    = oname

  if region == "GLOB":
    bnd        = [-40,-20,-10,-5,-2,2,5,10,20,40]
    bnd        = [-40,-20,-10,-5,-2,2,5,10,20,40]
    figdir     = datdir
    dotstep    = 5
  if region == "JPN":
    bnd        = [-40,-20,-10,-5,-2,2,5,10,20,40]
    figdir     = datdir + ".JPN"
    dotstep    = 1
    ctrack_func.mk_dir(figdir)
  #----

  figname    = figdir + "/" + datname.split("/")[-1][:-7] + ".png"
  cbarname   = figdir + "/dpr.dec.cbar.png"

  mons     = len(lyear) * len(ctrack_para.ret_lmon(season))

  a2figdat = fromfile(datname,float32).reshape(ny,nx) *60*60*24.*totaldays /mons  # (mm/month)

  ##-------------------------------
  ##--- test ---
  #a2shade = ones([ny,nx],float32)
  ##------------
  ctrack_fig.mk_pict_saone_reg_symm_dotshade(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname, dotcolor="k",dotstep=dotstep )
  #ctrack_fig.mk_pict_saone_reg_symm(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)

  print figname






