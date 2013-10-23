from numpy import *
import calendar
import datetime
from ctrack_fsub import *
import gsmap_func
import ctrack_para
import ctrack_func
import ctrack_fig
import chart_para
import subprocess
#---------------------------------
iyear = 2007
eyear = 2010
lseason=["ALL"]
#lseason=["ALL","DJF","MAM","JJA","SON"]
#lseason = [1,2,3,4,5,6,7,8,9,10,11,12]
iday  = 1
lhour = [0,6,12,18]
region= "ASAS"
region_draw = "JPN"
ny    = 180
nx    = 360
prtype = "GPCP1DD"
miss   = -9999.0
miss  = -9999.0
miss_gpcp = -99999.
lonlatfontsize = 30
lonrotation    = 0.0
lthdist   = [500]
locdir_root  = "/media/disk2/out/chart/%s/front"%(region)
dprdir_root  = {}
dprdir_root["GPCP1DD"] = "/media/disk2/data/GPCP1DD/v1.2/1dd"
dprdir_root["JRA25"]  = "/media/disk2/data/JRA25/sa.one/6hr/PR"
thorog       = 1500.0  # (m)
#calcflag = True
calcflag = False
#meanflag = True
meanflag = False
#----------------------------
a2one    = ones([ny,nx], float32)
#-- orog --------------------
orogname = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
a2orog   = fromfile(orogname, float32).reshape(ny,nx)
#-- domain ------------------
domname  = "/media/disk2/out/chart/%s/const/domainmask_saone.%s.2000-2006.bn"%(region,region)
a2domain = fromfile(domname , float32).reshape(ny,nx)
#-- shade  ------------------
a2shade  = ma.masked_where( a2domain==0.0, a2one).filled(miss)
a2shade  = ma.masked_where( a2orog > thorog, a2shade).filled(miss)

#----------------------------
idir_root   = "/media/disk2/out/chart/ASAS/front/agg"
for thdist in lthdist:
  for season in lseason:
    #**********************************************
    # annual mean precipitation
    if prtype in ["GPCP1DD"]:
      if meanflag ==True:
        sprog = "/home/utsumi/bin/dtanl/mk.mean.GPCP1DD.py" 
        scmd  = "python %s %s %s %s"%(sprog, iyear, eyear, season) 
        print scmd
        subprocess.call(scmd, shell=True)
      #--
      ptotplainname = "/media/disk2/data/GPCP1DD/v1.2/1dd/mean/gpcp_1dd_v1.2_p1d.%04d-%04d.%s.bn"%(iyear, eyear, season)
      a2ptotplain   = flipud(fromfile(ptotplainname, float32).reshape(ny,nx))
      a2ptotplain   = a2ptotplain / (60*60*24.0)  # mm/s

    #****************************
    #-- dummy -------------------
    a2ptot_warm = zeros([ny,nx], float32) 
    a2ptot_cold = zeros([ny,nx], float32) 
    a2ptot_occ  = zeros([ny,nx], float32) 
    a2ptot_stat = zeros([ny,nx], float32) 
    a2ptot_all  = zeros([ny,nx], float32) 

    #**********************************************
    # fraction
    #----------------------------------------------
    for year in range(iyear, eyear+1):
      lmon   = ctrack_para.ret_lmon(season)
      for mon in lmon:
        idir   = idir_root + "/%04d/%02d"%(year, mon)

        itimes_mon     = ctrack_para.ret_totaldays(year,year, mon) * 4.0
        #-- ptot name --
        ptotname_warm  = idir + "/rad%04d.warm.sa.one"%(thdist)
        ptotname_cold  = idir + "/rad%04d.cold.sa.one"%(thdist)
        ptotname_occ   = idir + "/rad%04d.occ.sa.one"%(thdist)
        ptotname_stat  = idir + "/rad%04d.stat.sa.one"%(thdist)
        ptotname_all   = idir + "/rad%04d.all.sa.one"%(thdist)

        #-- fig: load ptot ---
        a2ptot_warm_temp     = fromfile(ptotname_warm, float32).reshape(ny,nx)
        a2ptot_cold_temp     = fromfile(ptotname_cold, float32).reshape(ny,nx)
        a2ptot_occ_temp      = fromfile(ptotname_occ, float32).reshape(ny,nx)
        a2ptot_stat_temp     = fromfile(ptotname_stat, float32).reshape(ny,nx)
        a2ptot_all_temp      = fromfile(ptotname_all, float32).reshape(ny,nx)
        #-- fig: mask -
        a2ptot_warm_temp     = ma.masked_equal(a2ptot_warm_temp, miss).filled(0.0)
        a2ptot_cold_temp     = ma.masked_equal(a2ptot_cold_temp, miss).filled(0.0) 
        a2ptot_occ_temp      = ma.masked_equal(a2ptot_occ_temp, miss).filled(0.0) 
        a2ptot_stat_temp     = ma.masked_equal(a2ptot_stat_temp, miss).filled(0.0) 
        a2ptot_all_temp      = ma.masked_equal(a2ptot_all_temp, miss).filled(0.0) 
        # 
        a2ptot_warm          = a2ptot_warm + a2ptot_warm_temp * itimes_mon
        a2ptot_cold          = a2ptot_cold + a2ptot_cold_temp * itimes_mon
        a2ptot_occ           = a2ptot_occ  + a2ptot_occ_temp  * itimes_mon
        a2ptot_stat          = a2ptot_stat + a2ptot_stat_temp * itimes_mon
        a2ptot_all           = a2ptot_all  + a2ptot_all_temp  * itimes_mon
    #---------------------------------------------
    itimes  = ctrack_para.ret_totaldays(iyear, eyear, season) * 4.0
    a2ptot_warm  = a2ptot_warm / itimes
    a2ptot_cold  = a2ptot_cold / itimes
    a2ptot_occ   = a2ptot_occ  / itimes
    a2ptot_stat  = a2ptot_stat / itimes  
    a2ptot_all   = a2ptot_all  / itimes 

    #-- dirs -------------
    odir            = idir_root + "/%04d-%04d/%s"%(iyear,eyear,season)
    ctrack_func.mk_dir(odir)
    figdir          = odir + "/pict"
    ctrack_func.mk_dir(figdir)
    #-- fig: frac name ---
    fracname_warm   = figdir + "/frac.rad%04d.warm.%s.png"%(thdist,season)
    fracname_cold   = figdir + "/frac.rad%04d.cold.%s.png"%(thdist,season)
    fracname_occ    = figdir + "/frac.rad%04d.occ.%s.png"%(thdist,season)
    fracname_stat   = figdir + "/frac.rad%04d.stat.%s.png"%(thdist,season)
    fracname_all    = figdir + "/frac.rad%04d.all.%s.png"%(thdist,season)

    fracname_cwo    = figdir + "/frac.rad%04d.cwo.%s.png"%(thdist,season)

    #-- fig: mask 2nd -
    a2ptot_warm     = ma.masked_where(a2ptotplain==0.0, a2ptot_warm) 
    a2ptot_cold     = ma.masked_where(a2ptotplain==0.0, a2ptot_cold) 
    a2ptot_occ      = ma.masked_where(a2ptotplain==0.0, a2ptot_occ) 
    a2ptot_stat     = ma.masked_where(a2ptotplain==0.0, a2ptot_stat) 
    a2ptot_all      = ma.masked_where(a2ptotplain==0.0, a2ptot_all) 

    a2ptot_cwo      = a2ptot_cold + a2ptot_warm + a2ptot_occ

    #-- fig: make frac data -
    a2frac_warm     = (a2ptot_warm / a2ptotplain).filled(0.0)
    a2frac_cold     = (a2ptot_cold / a2ptotplain).filled(0.0)
    a2frac_occ      = (a2ptot_occ / a2ptotplain).filled(0.0)
    a2frac_stat     = (a2ptot_stat / a2ptotplain).filled(0.0)
    a2frac_all      = (a2ptot_all / a2ptotplain).filled(0.0)

    a2frac_cwo      = (a2ptot_cwo / a2ptotplain).filled(0.0)
    
    #-- name: fractin data
    fracdatname_warm   = odir + "/frac.rad%04d.warm.%s.sa.one"%(thdist,season)
    fracdatname_cold   = odir + "/frac.rad%04d.cold.%s.sa.one"%(thdist,season)
    fracdatname_occ    = odir + "/frac.rad%04d.occ.%s.sa.one"%(thdist,season)
    fracdatname_stat   = odir + "/frac.rad%04d.stat.%s.sa.one"%(thdist,season)
    fracdatname_all    = odir + "/frac.rad%04d.all.%s.sa.one"%(thdist,season)

    fracdatname_cwo    = odir + "/frac.rad%04d.cwo.%s.sa.one"%(thdist,season)
    
    #-- write data ----
    a2frac_warm.tofile(fracdatname_warm)
    a2frac_cold.tofile(fracdatname_cold)
    a2frac_occ.tofile(fracdatname_occ)
    a2frac_stat.tofile(fracdatname_stat)
    a2frac_all.tofile(fracdatname_all)
    
    a2frac_cwo.tofile(fracdatname_cwo)

    #-- fig: frac prep -
    bnd      = range(6, 70+1, 8)
    #bnd      = [10,20,30,40,50,60,70,80,90]
    bnd_all  = [10,20,30,40,50,60,70,80,90]
    cbarname = figdir + "/frac.cbar.png" 
    cbarname_all = figdir + "/frac.cbar.all.png" 
    a2shade  = ma.masked_equal(a2domain, 0.0).filled(miss)
    a2shade  = ma.masked_where(a2orog >1500.0, a2shade).filled(miss)
    coef     = 100.0
    stitle   = "proportion (%%), %s "%(season)
    mycm     = "Spectral"
    lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region_draw)
    
    #-- fig: frac draw -
    ctrack_fig.mk_pict_saone_reg(a2frac_warm, bnd, mycm, fracname_warm, stitle+"warm", cbarname, miss, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, a2shade=a2shade, coef=coef, lonlatfontsize=lonlatfontsize, lonrotation=lonrotation)
    
    ctrack_fig.mk_pict_saone_reg(a2frac_cold, bnd, mycm, fracname_cold, stitle+"cold", cbarname, miss, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, a2shade=a2shade, coef=coef, lonlatfontsize=lonlatfontsize, lonrotation=lonrotation)
    
    ctrack_fig.mk_pict_saone_reg(a2frac_occ, bnd, mycm, fracname_occ, stitle+"occ", cbarname, miss, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, a2shade=a2shade, coef=coef, lonlatfontsize=lonlatfontsize, lonrotation=lonrotation)
    
    ctrack_fig.mk_pict_saone_reg(a2frac_stat, bnd, mycm, fracname_stat, stitle+"stat", cbarname, miss, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, a2shade=a2shade, coef=coef, lonlatfontsize=lonlatfontsize, lonrotation=lonrotation)
    
    ctrack_fig.mk_pict_saone_reg(a2frac_all, bnd_all, mycm, fracname_all, stitle+"all", cbarname_all, miss, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, a2shade=a2shade, coef=coef, lonlatfontsize=lonlatfontsize, lonrotation=lonrotation)


    ctrack_fig.mk_pict_saone_reg(a2frac_cwo, bnd, mycm, fracname_cwo, stitle+"cwo", cbarname, miss, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, a2shade=a2shade, coef=coef, lonlatfontsize=lonlatfontsize, lonrotation=lonrotation)
      
    print fracname_all




