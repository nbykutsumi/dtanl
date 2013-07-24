from numpy import *
import calendar
import datetime
from ctrack_fsub import *
from dtanl_fsub import *
import gsmap_func
import ctrack_para
import ctrack_func
import ctrack_fig
import chart_para
import front_para
import subprocess
import calendar
#---------------------------------
#singleday= True
singleday= False
sresol = "anl_p"
iyear = 1997
eyear = 2012
#lseason=["ALL", "DJF","MAM","JJA","SON"]
#lseason=[1,2,3,4,5,6,7,8,9,10,11,12,"ALL","DJF","JJA"]
lseason=["DJF","JJA","ALL",1,2,3,4,5,6,7,8,9,10,11,12]
#lseason=[1,2,3,4,5,6,7,8,9,10,11,12]
#lseason=["DJF"]
#lseason=["JJA"]
#lseason=[1]
iday  = 1
#lhour = [12]
#region= "ASAS"
region= "GLOB"
#region= "JPN"
ny    = 180
nx    = 360
prtype = "GPCP1DD"
#prtype = "JRA25"
miss  = -9999.0
miss_gpcp = -99999.
thdist    = front_para.ret_thdistkm()  # (km)
countrad  = 300  # (km) for count
#-----------------------------------------
lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region)
#-- para for objective locator -------------
plev     = 850*100.0 # (Pa)
thfmask1, thfmask2 = front_para.ret_thfmask(sresol)

thorog  = ctrack_para.ret_thorog()
thgradorog=ctrack_para.ret_thgradorog()
#--- para for baroclinicity --------------
#thbc       = 0.7/1000/100.0
#thbc       = 0.9/1000/100.0
thbc       = front_para.ret_thbc(sresol)
#----------------------------
#-- orog --------------------
orogname = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
a2orog   = fromfile(orogname, float32).reshape(ny,nx)
gradorogadjname= "/media/disk2/data/JRA25/sa.one.125/const/topo/grad.topo.adj.twogrids.sa.one"
a2gradorogmask = fromfile(gradorogadjname, float32).reshape(ny,nx)

a2shade  = ma.masked_where(a2orog >thorog, a2orog).filled(miss)
a2shade  = ma.masked_where(a2gradorogmask >thgradorog, a2shade).filled(miss)
#***************************************
odir_root  = "/media/disk2/out/JRA25/sa.one.%s/6hr/tenkizu/front/agg"%(sresol)

##*********************************************************
##      fraction
##------------------------------------------------
#bnd        = [10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]
#for season in lseason:
#  lmon  = ctrack_para.ret_lmon(season)
#  #**********************************************
#  odir       = odir_root + "/%04d-%04d/%s"%(iyear, eyear,season)
#  ctrack_func.mk_dir(odir)
#  figdir     = odir + "/pict"
#  ctrack_func.mk_dir(figdir)
#  #-------
#  print "param:", thfmask1,thfmask2
#  #----
#  #-- oname  ----
#  sfracname_front = odir + "/frac.front.rad%04d.M1_%s_M2_%s.sa.one"%(thdist,thfmask1, thfmask2)
#  sfracname_bcf   = odir + "/frac.bcf.rad%04d.M1_%s_M2_%s.thbc_%04.2f.sa.one"%(thdist,thfmask1, thfmask2, thbc*1000*100)
#  sfracname_nobc  = odir + "/frac.nobc.rad%04d.M1_%s_M2_%s.thbc_%04.2f.sa.one"%(thdist,thfmask1, thfmask2, thbc*1000*100)
#  sfracname_olap  = odir + "/frac.olap.rad%04d.M1_%s_M2_%s.sa.one"%(thdist,thfmask1, thfmask2)
#
#  #-- init -------
#  a2frac_front  = zeros([ny,nx], float32)
#  a2frac_bcf    = zeros([ny,nx], float32)
#  a2frac_nobc   = zeros([ny,nx], float32)
#  a2frac_olap   = zeros([ny,nx], float32)
#  a2pr_plain    = zeros([ny,nx], float32)
#  #---------------
#  dsname = {}
#  da2in  = {}
#  for year in range(iyear, eyear+1):
#    for mon in lmon:
#      days         =  calendar.monthrange(year, mon)[1]
#      datdir_root  = "/media/disk2/out/JRA25/sa.one.%s/6hr/tenkizu/front/agg/%04d/%02d"%(sresol, year, mon)
#
#      #-- load data: front ---
#      datname     = datdir_root + "/pr.front.rad%04d.M1_%s_M2_%s.sa.one"%(thdist,thfmask1, thfmask2)
#      a2in        = fromfile(datname, float32).reshape(ny,nx)
#      a2frac_front = a2frac_front + ma.masked_where(a2shade==miss, a2in)*60*60*24*days
#
#      #-- load data: bcf   ---
#      datname     = datdir_root + "/pr.bcf.rad%04d.M1_%s_M2_%s.thbc_%04.2f.sa.one"%(thdist, thfmask1, thfmask2, thbc*1000*100)
#      a2in        = fromfile(datname, float32).reshape(ny,nx)
#      a2frac_bcf  = a2frac_bcf  + ma.masked_where(a2shade==miss, a2in)*60*60*24*days
#
#       #-- load data: nobc ---
#      datname     = datdir_root + "/pr.nobc.rad%04d.M1_%s_M2_%s.thbc_%04.2f.sa.one"%(thdist,thfmask1, thfmask2, thbc*1000*100)
#      a2in        = fromfile(datname, float32).reshape(ny,nx)
#      a2frac_nobc = a2frac_nobc + ma.masked_where(a2shade==miss, a2in)*60*60*24*days
#
#      #-- load data: olap ---
#      datname     = datdir_root + "/pr.olap.rad%04d.M1_%s_M2_%s.sa.one"%(thdist,thfmask1, thfmask2)
#      a2in        = fromfile(datname, float32).reshape(ny,nx)
#      a2frac_olap = a2frac_olap  + ma.masked_where(a2shade==miss, a2in)*60*60*24*days
#
#      # plain precip --
#      if prtype == "GPCP1DD":
#        plaindir  = "/media/disk2/data/GPCP1DD/v1.2/1dd/mean"
#        plainname = plaindir + "/gpcp_1dd_v1.2_p1d.%04d-%04d.%s.bn"%(iyear,eyear,mon)
#        a2in    = fromfile(plainname, float32).reshape(ny,nx)
#        a2in    = flipud(a2in)
#        a2in    = a2in * calendar.monthrange(1999, mon)[1]  #mm/day ->mm/mon
#      #-----
#      a2pr_plain = a2pr_plain + a2in
#
#  #----------------
#  a2frac_front = ma.masked_where(a2pr_plain<1.0, a2frac_front) / a2pr_plain
#  a2frac_bcf   = ma.masked_where(a2pr_plain<1.0, a2frac_bcf  ) / a2pr_plain
#  a2frac_nobc  = ma.masked_where(a2pr_plain<1.0, a2frac_nobc ) / a2pr_plain
#  a2frac_olap  = ma.masked_where(a2pr_plain<1.0, a2frac_olap ) / a2pr_plain
#
#  #-- save --------
#  a2frac_front = ma.masked_where(a2shade==miss, a2frac_front).filled(miss)
#  a2frac_bcf   = ma.masked_where(a2shade==miss, a2frac_bcf  ).filled(miss)
#  a2frac_nobc  = ma.masked_where(a2shade==miss, a2frac_nobc ).filled(miss)
#  a2frac_olap  = ma.masked_where(a2shade==miss, a2frac_olap ).filled(miss)
#  #-
#  a2frac_front.tofile(sfracname_front)
#  a2frac_bcf.tofile(sfracname_bcf)
#  a2frac_nobc.tofile(sfracname_nobc)
#  a2frac_olap.tofile(sfracname_olap)
#
#  #-- fig: name ---
#  figname_front  = figdir + "/frac.front.s%s.rad%04d.M1_%s_M2_%s.png"%(season,thdist, thfmask1, thfmask2)
#  figname_bcf    = figdir + "/frac.bcf.s%s.rad%04d.M1_%s_M2_%s.thbc_%04.2f.png"%(season,thdist, thfmask1, thfmask2, thbc*1000*100)
#  figname_nobc   = figdir + "/frac.nobc.s%s.rad%04d.M1_%s_M2_%s.thbc_%04.2f.png"%(season,thdist, thfmask1, thfmask2, thbc*1000*100)
#  figname_olap   = figdir + "/frac.olap.s%s.rad%04d.M1_%s_M2_%s.png"%(season,thdist, thfmask1, thfmask2)
#
#  #-- fig: front -
#  cbarname = figdir + "/frac.front.cbar.png" 
#  stitle   = "frac front: season:%s %04d-%04d M1:%s  M2:%s "%(season,iyear, eyear, thfmask1, thfmask2)
#  mycm     = "Spectral"
#  datname  = sfracname_front
#  figname  = figname_front
#  a2figdat = fromfile(datname, float32).reshape(ny,nx)
#  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
#  ctrack_fig.mk_pict_saone_reg(a2figdat, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon)
#  print figname
#
#  #-- fig: bcf  -
#  cbarname = figdir + "/frac.bcf.cbar.png" 
#  stitle   = "frac bcf: season:%s %04d-%04d M1:%s  M2:%s thbc:%04.2f"%(season,iyear, eyear, thfmask1, thfmask2, thbc*1000*100)
#  mycm     = "Spectral"
#  datname  = sfracname_bcf
#  figname  = figname_bcf
#  a2figdat = fromfile(datname, float32).reshape(ny,nx)
#  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
#  ctrack_fig.mk_pict_saone_reg(a2figdat, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon)
#  print figname
#
#  #-- fig: nobc  -
#  cbarname = figdir + "/frac.nobc.cbar.png" 
#  stitle   = "frac nobc: season:%s %04d-%04d M1:%s  M2:%s thbc:%04.2f"%(season,iyear, eyear, thfmask1, thfmask2, thbc*1000*100)
#  mycm     = "Spectral"
#  datname  = sfracname_nobc
#  figname  = figname_nobc
#  a2figdat = fromfile(datname, float32).reshape(ny,nx)
#  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
#  ctrack_fig.mk_pict_saone_reg(a2figdat, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon)
#  print figname
#
#  #-- fig: olap -
#  stitle   = "frac olap: season:%s %04d-%04d M1:%s  M2:%s "%(season,iyear, eyear, thfmask1, thfmask2)
#  mycm     = "Spectral"
#  datname  = sfracname_olap
#  figname  = figname_olap
#  a2figdat = fromfile(datname, float32).reshape(ny,nx)
#  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
#  ctrack_fig.mk_pict_saone_reg(a2figdat, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon)
#

#**********************************************

#*********************************************************
#      existence proportion
#------------------------------------------------
#bnd        = [1.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]
bnd        = [1,5,9,13,17,21,25,29]
nd        = [10,20,30,40,50,60,70,80]

for season in lseason:
  lmon  = ctrack_para.ret_lmon(season)
  #**********************************************
  odir       = odir_root + "/%04d-%04d/%s"%(iyear, eyear,season)
  ctrack_func.mk_dir(odir)
  figdir     = odir + "/pict"
  ctrack_func.mk_dir(figdir)
  #-------
  #----
  tkey  = (thfmask1, thfmask2)
  #-- oname  ----
  soname_front = odir + "/freq.front.M1_%s_M2_%s.sa.one"%(thfmask1, thfmask2)
  soname_olap  = odir + "/freq.olap.M1_%s_M2_%s.sa.one"%(thfmask1, thfmask2)
  #
  soname_bc_front   = odir + "/freq.bcf.front.M1_%s_M2_%s.sa.one"%(thfmask1, thfmask2)
  soname_nbc_front  = odir + "/freq.nobc.front.M1_%s_M2_%s.sa.one"%(thfmask1, thfmask2)

  #-- init -------
  a2out_front  = zeros([ny,nx], float32)
  #
  a2out_bc_front= zeros([ny,nx],float32)
  a2out_nbc_front= zeros([ny,nx],float32)
  #---------------
  dsname = {}
  da2in  = {}
  days             = 0.0 
  for year in range(iyear, eyear+1):
    for mon in lmon:
      days         =  days + calendar.monthrange(year, mon)[1]
      datdir_root  = "/media/disk2/out/JRA25/sa.one.%s/6hr/tenkizu/front/agg/%04d/%02d"%(sresol, year, mon)

      #-- load data: front ---
      datname     = datdir_root + "/count.front.rad%04dkm.M1_%s_M2_%s.sa.one"%(countrad, thfmask1,thfmask2)
      a2in        = fromfile(datname, float32).reshape(ny,nx)
      a2out_front = a2out_front + ma.masked_where(a2shade==miss, a2in)

      #-- load data: baroclinic front ---
      datname     = datdir_root + "/count.bcf.rad%04dkm.M1_%s_M2_%s.thbc_%04.2f.sa.one"%(countrad, thfmask1,thfmask2, thbc*1000*100)
      a2in        = fromfile(datname, float32).reshape(ny,nx)
      a2out_bc_front = a2out_bc_front  + ma.masked_where(a2shade==miss, a2in)

      #-- load data: non-baroclinic front ---
      datname     = datdir_root + "/count.nobc.rad%04dkm.M1_%s_M2_%s.thbc_%04.2f.sa.one"%(countrad, thfmask1,thfmask2, thbc*1000*100)
      a2in        = fromfile(datname, float32).reshape(ny,nx)
      a2out_nbc_front = a2out_nbc_front  + ma.masked_where(a2shade==miss, a2in)
  #----------------
  a2out_front = a2out_front / (days*4.0)
  #
  a2out_bc_front = a2out_bc_front / (days*4.0)
  a2out_nbc_front = a2out_nbc_front / (days*4.0)

  #-- fill --------
  a2out_front = ma.masked_where(a2shade==miss, a2out_front).filled(miss)
  #
  a2out_bc_front  = ma.masked_where(a2shade==miss, a2out_bc_front).filled(miss)
  a2out_nbc_front = ma.masked_where(a2shade==miss, a2out_nbc_front).filled(miss)

  #-- save --------

  a2out_front.tofile(soname_front)
  #
  a2out_bc_front.tofile(soname_bc_front) 
  a2out_nbc_front.tofile(soname_nbc_front) 

  #-- fig: name ---
  figname_front  = figdir + "/freq.front.s%s.M1_%s_M2_%s.thbc_%04.2f.png"%(season, thfmask1, thfmask2, thbc*1000*100)
  figname_bc_front   = figdir + "/freq.bcf.front.s%s.M1_%s_M2_%s.thbc_%04.2f.png"%(season, thfmask1, thfmask2, thbc*1000*100)
  figname_nbc_front  = figdir + "/freq.nobc.front.s%s.M1_%s_M2_%s.thbc_%04.2f.png"%(season, thfmask1, thfmask2, thbc*1000*100)
  #
  #--------------------------------
  #-- fig: front -
  cbarname = figdir + "/freq.front.cbar.png" 
  stitle   = "freq. front: season:%s %04d-%04d M1:%s  M2:%s "%(season,iyear, eyear, thfmask1, thfmask2)
  mycm     = "Spectral"
  datname  = soname_front
  figname  = figname_front
  a2figdat = fromfile(datname, float32).reshape(ny,nx)
  #-- sum 9grids ---
  #a2figdat = dtanl_fsub.sum_9grids_saone(a2figdat.T, miss).T

  #-------------------------------
  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
  ctrack_fig.mk_pict_saone_reg(a2figdat, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon)
  print figname

  #--------------------------------
  #-- fig: baroclinic front -
  cbarname = figdir + "/freq.bcf.front.cbar.png" 
  stitle   = "freq. bcf front: season:%s %04d-%04d M1:%s  M2:%s "%(season,iyear, eyear, thfmask1, thfmask2)
  mycm     = "Spectral"
  datname  = soname_bc_front
  figname  = figname_bc_front
  a2figdat = fromfile(datname, float32).reshape(ny,nx)
  #-- sum 9grids ---
  #a2figdat = dtanl_fsub.sum_9grids_saone(a2figdat.T, miss).T

  #-------------------------------
  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
  ctrack_fig.mk_pict_saone_reg(a2figdat, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon)
  print figname

  #--------------------------------
  #-- fig: non-baroclinic front -
  stitle   = "freq. non-bc front: season:%s %04d-%04d M1:%s  M2:%s "%(season,iyear, eyear, thfmask1, thfmask2)
  mycm     = "Spectral"
  datname  = soname_nbc_front
  figname  = figname_nbc_front
  a2figdat = fromfile(datname, float32).reshape(ny,nx)
  #-- sum 9grids ---
  #a2figdat = dtanl_fsub.sum_9grids_saone(a2figdat.T, miss).T

  #-------------------------------
  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
  ctrack_fig.mk_pict_saone_reg(a2figdat, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon)
  print figname

#**********************************************


