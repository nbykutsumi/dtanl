from numpy import *
from dtanl_fsub import *
import calendar
import ctrack_func
import ctrack_para
import ctrack_fig
import chart_para
import cf.util
#------------------------------------------------------
iyear  = 2000
eyear  = 2010
lseason = ["ALL","DJF","MAM","JJA","SON"]
ny     = 180
nx     = 360
miss   = -9999.0
region = "ASAS"

region_draw = "JPN"
#---------------------
#lllat  = 0.0
#lllon  = 60.0
#urlat  = 80.0
#urlon  = 210.0
lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region_draw)
thorog = 1500.0 # (m)
#------------------------------------------------------
idir_root  = "/media/disk2/out/chart/ASAS/front/agg"
odir_root  = idir_root 

#--- domain mask ------
domdir   = "/media/disk2/out/chart/ASAS/const"
domname  = domdir + "/domainmask_saone.ASAS.2000-2006.bn"
a2dom    = fromfile(domname, float32).reshape(180,360)
#--- orog mask   ------
orogname = "/media/disk2/data/JRA25/sa.one/const/topo/topo.sa.one"
a2orog   = fromfile(orogname, float32).reshape(ny,nx)
#--- shade       ------
a2shade  = ma.masked_equal(a2dom, 0.0).filled(miss)
a2shade  = ma.masked_where( a2orog >=thorog, a2shade).filled(miss)
#----------------------

for season in lseason:
  #----------------------------
  odir         = odir_root + "/%04d-%04d/%s"%(iyear, eyear, season)
  figdir       = odir + "/pict"
  ctrack_func.mk_dir(odir)
  ctrack_func.mk_dir(figdir)
  #
  soname_warm  = odir      + "/freq.warm.saone"
  soname_cold  = odir      + "/freq.cold.saone"
  soname_occ   = odir      + "/freq.occ.saone"
  soname_stat  = odir      + "/freq.stat.saone"
  soname_all   = odir      + "/freq.all.saone"
  #
  figname_warm = figdir    + "/freq.warm.%s.png"%(season)
  figname_cold = figdir    + "/freq.cold.%s.png"%(season)
  figname_occ  = figdir    + "/freq.occ.%s.png"%(season)
  figname_stat = figdir    + "/freq.stat.%s.png"%(season)
  figname_all  = figdir    + "/freq.all.%s.png"%(season)
  #--- init -------------------
  a2warm     = zeros([ny,nx], float32)
  a2cold     = zeros([ny,nx], float32)
  a2occ      = zeros([ny,nx], float32)
  a2stat     = zeros([ny,nx], float32)
  a2all      = zeros([ny,nx], float32)

  #----------------------------
  totaltimes = ctrack_para.ret_totaldays(iyear, eyear, season)*4.0
  print totaltimes
  lmon = ctrack_para.ret_lmon(season)
  for year in range(iyear, eyear+1):
    for mon in lmon:
      #--------------------
      idir         = idir_root + "/%04d/%02d"%(year,mon)
      siname_warm  = idir      + "/count.warm.saone"
      siname_cold  = idir      + "/count.cold.saone"
      siname_occ   = idir      + "/count.occ.saone"
      siname_stat  = idir      + "/count.stat.saone"
      #--------------------
      a2warm_temp       = fromfile(siname_warm, float32).reshape(ny,nx)
      a2cold_temp       = fromfile(siname_cold, float32).reshape(ny,nx)
      a2occ_temp        = fromfile(siname_occ,  float32).reshape(ny,nx)
      a2stat_temp       = fromfile(siname_stat, float32).reshape(ny,nx)
      #
      a2warm  = a2warm + ma.masked_equal(a2warm_temp, miss).filled(0.0)
      a2cold  = a2cold + ma.masked_equal(a2cold_temp, miss).filled(0.0)
      a2occ   = a2occ  + ma.masked_equal(a2occ_temp , miss).filled(0.0)
      a2stat  = a2stat + ma.masked_equal(a2stat_temp, miss).filled(0.0)
      a2all   = a2warm + a2cold + a2occ + a2stat
  #-----------------------------
  a2freq_warm  = (ma.masked_equal(a2warm, miss) / totaltimes).filled(miss)
  a2freq_cold  = (ma.masked_equal(a2cold, miss) / totaltimes).filled(miss)
  a2freq_occ   = (ma.masked_equal(a2occ , miss) / totaltimes).filled(miss)
  a2freq_stat  = (ma.masked_equal(a2stat, miss) / totaltimes).filled(miss)
  a2freq_all   = (ma.masked_equal(a2all , miss) / totaltimes).filled(miss)
  #-----------------------------
  a2freq_warm.tofile(soname_warm)
  a2freq_cold.tofile(soname_cold)
  a2freq_occ.tofile(soname_occ)
  a2freq_stat.tofile(soname_stat)
  a2freq_all.tofile(soname_all)
  #***************************
  #  figure warm 
  #---------------------------
  #bnd        = [2,3,4,5,6,7,8,9,10]
  bnd        = [4,8,12,16,20,24,28,32,36]
  cbarname = figdir + "/freq.cbar.png"
  stitle   = "freq. warm: season:%s %04d-%04d"%(season,iyear, eyear)
  mycm     = "Spectral"
  datname  = soname_warm
  figname  = figname_warm
  a2figdat = fromfile(datname, float32).reshape(ny,nx)
  #-- sum 9grids ---
  a2figdat = dtanl_fsub.sum_9grids_saone(a2figdat.T, miss).T
  
  #-------------------------------
  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
  print figname
  #***************************
  #  figure cold 
  #---------------------------
  #bnd        = [2,3,4,5,6,7,8,9,10]
  bnd        = [4,8,12,16,20,24,28,32,36]
  cbarname = figdir + "/freq.cbar.png"
  stitle   = "freq. cold: season:%s %04d-%04d"%(season,iyear, eyear)
  mycm     = "Spectral"
  datname  = soname_cold
  figname  = figname_cold
  a2figdat = fromfile(datname, float32).reshape(ny,nx)
  #-- sum 9grids ---
  a2figdat = dtanl_fsub.sum_9grids_saone(a2figdat.T, miss).T
  
  #-------------------------------
  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
  print figname
  #***************************
  #  figure occ 
  #---------------------------
  #bnd        = [2,3,4,5,6,7,8,9,10]
  bnd        = [4,8,12,16,20,24,28,32,36]
  cbarname = figdir + "/freq.cbar.png"
  stitle   = "freq. occ: season:%s %04d-%04d"%(season,iyear, eyear)
  mycm     = "Spectral"
  datname  = soname_occ
  figname  = figname_occ
  a2figdat = fromfile(datname, float32).reshape(ny,nx)
  #-- sum 9grids ---
  a2figdat = dtanl_fsub.sum_9grids_saone(a2figdat.T, miss).T
  
  #-------------------------------
  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
  print figname
  #***************************
  #  figure stat 
  #---------------------------
  #bnd        = [2,3,4,5,6,7,8,9,10]
  #bnd        = [4,8,12,16,20,24,28,32,36]
  #bnd        = [4,10,16,22,28,34,40,46,52,58,64,70,76,82,88,94]
  bnd        = [4,10,16,22,28,34,40,46,52,58,64]
  cbarname = figdir + "/freq.cbar.stat.png"
  stitle   = "freq. stat: season:%s %04d-%04d"%(season,iyear, eyear)
  mycm     = "Spectral"
  datname  = soname_stat
  figname  = figname_stat
  a2figdat = fromfile(datname, float32).reshape(ny,nx)
  #-- sum 9grids ---
  a2figdat = dtanl_fsub.sum_9grids_saone(a2figdat.T, miss).T
  
  #-------------------------------
  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
  print figname
  #***************************
  #  figure all 
  #---------------------------
  #bnd        = [2,3,4,5,6,7,8,9,10]
  bnd        = [10,20,30,40,50,60,70,80]
  cbarname = figdir + "/freq.cbar.all.png"
  stitle   = "freq. all: season:%s %04d-%04d"%(season,iyear, eyear)
  mycm     = "Spectral"
  datname  = soname_all
  figname  = figname_all
  a2figdat = fromfile(datname, float32).reshape(ny,nx)
  #-- sum 9grids ---
  a2figdat = dtanl_fsub.sum_9grids_saone(a2figdat.T, miss).T
  
  #-------------------------------
  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
  print figname

