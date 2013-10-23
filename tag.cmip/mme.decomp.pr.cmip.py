from numpy import *
import ctrack_func, cmip_func
import ctrack_para, cmip_para, chart_para
import ctrack_fig
import math

#lmodel=["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel = ["MIROC5","MIROC5","MIROC5","MIROC5"]
nmodel = len(lmodel)
lexprfut= ["rcp85"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
#dyrange = {"historical":[1980,1981], "rcp85":[2080,2081]}
lseason = ["ALL"]

dist_tc = 1000 #[km]
dist_c  = 1000 #[km]
dist_f  = 500 #[km]

nx,ny   =[360,180]

thdura_c    = 48
thdura_tc   = thdura_c
miss        = -9999.0
thres       = 4

#lstype   = ["cf","c","tc","fbc","ot"]
#ldectype = ["dNI","NdI","dtot"]

lstype   = ["cf"]
ldectype = ["dNI"]

#---------------------
#region    = "GLOB"
region    = "JPN"
lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region)
#**********************************************
#**********************************************
llkey = [[exprfut,season] for exprfut in lexprfut for season in lseason]
for exprfut, season in llkey:
  for stype, dectype in [[stype,dectype] for stype in lstype for dectype in ldectype]:

    #** init ******
    a2one    = ones ([ny,nx],float32)
    a2mdpr   = zeros([ny,nx],float32)
    a2nposi  = zeros([ny,nx],float32)
    a2nnega  = zeros([ny,nx],float32)
    totaltimes = 0.0
    #--------------
    for model in lmodel:
      #------
      ens   = cmip_para.ret_ens(model, exprfut, "psl")
      sunit, scalendar = cmip_para.ret_unit_calendar(model,exprfut)
      iyear,eyear  = dyrange[exprfut]

      totaltimes_model = cmip_para.ret_totaldays_cmip(iyear,eyear,season,sunit,scalendar)
      totaltimes       = totaltimes_model

      #------
      #idir  = "/media/disk2/out/CMIP5/sa.one.MIROC5.rcp85/6hr/tagpr/c48h.tc48h/2080-2099.ALL.decomp"\
      idir  = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/tagpr/c%02dh.tc%02dh/%04d-%04d.%s.decomp"\
           %(model,exprfut,thdura_c,thdura_tc,iyear,eyear,season)
   
      #iname = idir + "/dpr.c.dNI.MIROC5.rcp85.r1i1p1.tc1000.c1000.f0500.2080-2099.ALL.sa.one"
      iname = idir + "/dpr.%s.%s.%s.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"\
                     %(stype,dectype,model,exprfut,ens,dist_tc,dist_c,dist_f,iyear,eyear,season)
  
      a2dpr   = fromfile(iname, float32).reshape(ny,nx)
      a2mdpr  = a2mdpr + a2dpr

      a2nposi = a2nposi + ma.masked_where( a2dpr >0.0, a2one).filled(0.0)
      a2nnega = a2nnega + ma.masked_where( a2dpr <=0.0, a2one).filled(0.0)
    #--------------
    totaltimes= totaltimes / len(lmodel)
    a2mdpr    = a2mdpr / len(lmodel)

    a2nsame   = ma.maximum(a2nposi, a2nnega)     
    a2shade   = ma.masked_where(a2nsame< thres, ones([ny,nx],float32)).filled(miss)    
    #--------------
    odir      = "/media/disk2/out/CMIP5/sa.one.MME.%s/6hr/tagpr/c%02dh.tc%02dh/%04d-%04d.%s.decomp"\
                %(exprfut,thdura_c,thdura_tc,iyear,eyear,season)
    ctrack_func.mk_dir(odir)
    oname     = odir + "/dpr.%s.%s.MME.%s.%s.tc%04d.c%04d.f%04d.%04d-%04d.%s.sa.one"\
                     %(stype,dectype,exprfut,ens,dist_tc,dist_c,dist_f,iyear,eyear,season)
    
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
    stitle   = "dif mm/month MME %s %s season:%s %04d-%04d %s %s"%(exprfut,ens,season,iyear, eyear,stype,dectype)
    stitle   = stitle + "\n" + "%d out of %d models"%(nmodel, thres)
    mycm     = "RdBu"

    datdir     = odir
    datname    = oname

    if region == "GLOB":
      bnd        = [-40,-20,-10,-5,-2,2,5,10,20,40]
      figdir     = datdir
    if region == "JPN":
      bnd        = [-40,-20,-10,-5,-2,2,5,10,20,40]
      figdir     = datdir + ".JPN"
      ctrack_func.mk_dir(figdir)
    #----

    figname    = figdir + "/" + datname.split("/")[-1][:-7] + ".png"
    cbarname   = figdir + "/dpr.dec.cbar.png"

    mons     = len(ctrack_para.ret_lmon(season))
    a2figdat = fromfile(datname,float32).reshape(ny,nx) *60*60*24.*totaltimes /mons  # (mm/month)

    ##-------------------------------
    ##--- test ---
    #a2shade = ones([ny,nx],float32)
    ##------------
    
    ctrack_fig.mk_pict_saone_reg_symm(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
    print figname


