from numpy import *
from dtanl_fsub import *
from ctrack_fsub import *
from myfunc_fsub import *
import calendar
import ctrack_func
import ctrack_para
import ctrack_fig
import chart_para
import cf.util

#------------------------------------------------------
#filterflag = True
filterflag = False

iyear  = 2007
eyear  = 2010
#lseason = ["ALL","DJF","MAM","JJA","SON"]
lseason = ["DJF","MAM","JJA","SON"]
ny     = 180
nx     = 360
miss   = -9999.0
region = "ASAS"

region_draw = "JPN"
#rad    = 200.0  # (km)
rad    = 1.0  # (km)
#rad    = ""  # (km)
lonlatfontsize = 35.0
lonrotation    = 0.0
#---------------------
#lllat  = 0.0
#lllon  = 60.0
#urlat  = 80.0
#urlon  = 210.0
lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region_draw)
thorog = 1500.0 # (m)
#bnd_normal  = [1,3,5,7,9,11,13]
#bnd_normal    = [2,5,10,15,20,30,40,50,60]
bnd_normal   = [0.2,0.5,1,2,3,4,5,6]
bnd_stat     = bnd_normal
bnd_all      = bnd_normal
#bnd_stat    = [1,4,7,10,13,16,19,22,25,28]
#bnd_stat    = [1,5,10,15,20,25,30,35,40,45,50,55]
#bnd_all     = [1,5,10,15,20,25,30,35,40,45,50,55]

#--------------
#a2filter = array(\
#           [[1,2,1]\
#           ,[2,4,2]\
#           ,[1,2,1]], float32)
a2filter = array(\
           [[1,1,1]\
           ,[1,1,1]\
           ,[1,1,1]], float32)


#------------------------------------------------------
idir_root  = "/media/disk2/out/chart/ASAS/front/agg"
odir_root  = idir_root 

#--- domain mask ------
domdir   = "/media/disk2/out/chart/ASAS/const"
domname  = domdir + "/domainmask_saone.ASAS.2000-2006.bn"
a2dom    = fromfile(domname, float32).reshape(180,360)
#--- orog mask   ------
orogname = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
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
  if rad != "":
    soname_warm  = odir      + "/freq.rad%04dkm.warm.sa.one"%(rad)
    soname_cold  = odir      + "/freq.rad%04dkm.cold.sa.one"%(rad)
    soname_occ   = odir      + "/freq.rad%04dkm.occ.sa.one"%(rad)
    soname_stat  = odir      + "/freq.rad%04dkm.stat.sa.one"%(rad)
    soname_all   = odir      + "/freq.rad%04dkm.all.sa.one"%(rad)
    #
    figname_warm = figdir    + "/freq.rad%04dkm.warm.%s.png"%(rad,season)
    figname_cold = figdir    + "/freq.rad%04dkm.cold.%s.png"%(rad,season)
    figname_occ  = figdir    + "/freq.rad%04dkm.occ.%s.png"%(rad,season)
    figname_stat = figdir    + "/freq.rad%04dkm.stat.%s.png"%(rad,season)
    figname_all  = figdir    + "/freq.rad%04dkm.all.%s.png"%(rad,season)
  else:
    soname_warm  = odir      + "/freq.warm.sa.one"
    soname_cold  = odir      + "/freq.cold.sa.one"
    soname_occ   = odir      + "/freq.occ.sa.one"
    soname_stat  = odir      + "/freq.stat.sa.one"
    soname_all   = odir      + "/freq.all.sa.one"
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
      if rad != "":
        siname_warm  = idir      + "/count.rad%04dkm.warm.sa.one"%(rad)
        siname_cold  = idir      + "/count.rad%04dkm.cold.sa.one"%(rad)
        siname_occ   = idir      + "/count.rad%04dkm.occ.sa.one"%(rad)
        siname_stat  = idir      + "/count.rad%04dkm.stat.sa.one"%(rad)
      else:
        siname_warm  = idir      + "/count.warm.sa.one"
        siname_cold  = idir      + "/count.cold.sa.one"
        siname_occ   = idir      + "/count.occ.sa.one"
        siname_stat  = idir      + "/count.stat.sa.one"
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
  bnd        = bnd_normal
  #-------
  if rad == "":
    cbarname = figdir + "/freq.cbar.png"
  else:
    cbarname = figdir + "/freq.rad%04dkm.cbar.png"%(rad)
  #-------
  stitle   = "freq. warm: season:%s %04d-%04d"%(season,iyear, eyear)
  mycm     = "Spectral"
  datname  = soname_warm
  figname  = figname_warm
  a2figdat = fromfile(datname, float32).reshape(ny,nx)
  #-- sum 9grids ---
  #a2figdat = dtanl_fsub.sum_9grids_saone(a2figdat.T, miss).T
  
  #-------------------------------
  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0

  #-- filter --------------
  if filterflag == True:
    a2figdat = myfunc_fsub.mk_a2convolution(a2figdat.T, a2filter.T, miss).T
    a2figdat = a2figdat * a2filter.size
  elif filterflag ==False:
    pass
  else:
    print "check filterflag",filterflag
    sys.exit()
  #------------------------

  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname, lonlatfontsize=lonlatfontsize, lonrotation=lonrotation)
  print "fontsize",lonlatfontsize
  print figname
  #***************************
  #  figure cold 
  #---------------------------
  bnd  = bnd_normal
  #-------
  if rad == "":
    cbarname = figdir + "/freq.cbar.png"
  else:
    cbarname = figdir + "/freq.rad%04dkm.cbar.png"%(rad)
  #-------
  stitle   = "freq. cold: season:%s %04d-%04d"%(season,iyear, eyear)
  mycm     = "Spectral"
  datname  = soname_cold
  figname  = figname_cold
  a2figdat = fromfile(datname, float32).reshape(ny,nx)
  #-- sum 9grids ---
  #a2figdat = dtanl_fsub.sum_9grids_saone(a2figdat.T, miss).T
  
  #-------------------------------
  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0

  #-- filter --------------
  if filterflag == True:
    a2figdat = myfunc_fsub.mk_a2convolution(a2figdat.T, a2filter.T, miss).T
    a2figdat = a2figdat * a2filter.size
  elif filterflag ==False:
    pass
  else:
    print "check filterflag",filterflag
    sys.exit()
  #------------------------

  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname, lonlatfontsize=lonlatfontsize, lonrotation=lonrotation)
  print figname
  #***************************
  #  figure occ 
  #---------------------------
  bnd  = bnd_normal
  #-------
  if rad == "":
    cbarname = figdir + "/freq.cbar.png"
  else:
    cbarname = figdir + "/freq.rad%04dkm.cbar.png"%(rad)
  #-------
  stitle   = "freq. occ: season:%s %04d-%04d"%(season,iyear, eyear)
  mycm     = "Spectral"
  datname  = soname_occ
  figname  = figname_occ
  a2figdat = fromfile(datname, float32).reshape(ny,nx)
  #-- sum 9grids ---
  #a2figdat = dtanl_fsub.sum_9grids_saone(a2figdat.T, miss).T
  
  #-------------------------------
  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0

  #-- filter --------------
  if filterflag == True:
    a2figdat = myfunc_fsub.mk_a2convolution(a2figdat.T, a2filter.T, miss).T
    a2figdat = a2figdat * a2filter.size
  elif filterflag ==False:
    pass
  else:
    print "check filterflag",filterflag
    sys.exit()
  #------------------------

  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname, lonlatfontsize=lonlatfontsize, lonrotation=lonrotation)
  print figname
  #***************************
  #  figure stat 
  #---------------------------
  bnd        = bnd_stat
  #-----------
  if rad == "":
    cbarname = figdir + "/freq.cbar.stat.png"
  else:
    cbarname = figdir + "/freq.rad%04dkm.cbar.stat.png"%(rad)
  #-----------
  stitle   = "freq. stat: season:%s %04d-%04d"%(season,iyear, eyear)
  mycm     = "Spectral"
  datname  = soname_stat
  figname  = figname_stat
  a2figdat = fromfile(datname, float32).reshape(ny,nx)
  #-- sum 9grids ---
  #a2figdat = dtanl_fsub.sum_9grids_saone(a2figdat.T, miss).T
  
  #-------------------------------
  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0

  #-- filter --------------
  if filterflag == True:
    a2figdat = myfunc_fsub.mk_a2convolution(a2figdat.T, a2filter.T, miss).T
    a2figdat = a2figdat * a2filter.size
  elif filterflag ==False:
    pass
  else:
    print "check filterflag",filterflag
    sys.exit()
  #------------------------

  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname, lonlatfontsize=lonlatfontsize, lonrotation=lonrotation)
  print figname
  #***************************
  #  figure all 
  #---------------------------
  bnd        = bnd_all
  #----------
  if rad == "":
    cbarname = figdir + "/freq.cbar.all.png"
  else:
    cbarname = figdir + "/freq.rad%04dkm.cbar.all.png"%(rad)
  #----------
  stitle   = "freq. all: season:%s %04d-%04d"%(season,iyear, eyear)
  mycm     = "Spectral"
  datname  = soname_all
  figname  = figname_all
  a2figdat = fromfile(datname, float32).reshape(ny,nx)
  #-- sum 9grids ---
  #a2figdat = dtanl_fsub.sum_9grids_saone(a2figdat.T, miss).T
  
  #-------------------------------
  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0

  #-- filter --------------
  if filterflag == True:
    a2figdat = myfunc_fsub.mk_a2convolution(a2figdat.T, a2filter.T, miss).T
    a2figdat = a2figdat * a2filter.size
  elif filterflag ==False:
    pass
  else:
    print "check filterflag",filterflag
    sys.exit()
  #------------------------

  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname, lonlatfontsize=lonlatfontsize, lonrotation=lonrotation)
  print figname

