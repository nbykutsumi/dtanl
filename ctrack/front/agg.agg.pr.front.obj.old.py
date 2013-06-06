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
import subprocess
#---------------------------------
#singleday= True
singleday= False

iyear = 1997
eyear = 2004
#lseason=["ALL","DJF","JJA"]
#lseason=[1,2,3,4,5,6,7,8,9,10,11,12,"ALL","DJF","JJA"]
#lseason=[1,2,3,4,5,6,7,8,9,10,11,12]
lseason = [1]
#lseason=["DJF"]
#lseason=["JJA"]
#lseason=["ALL"]
iday  = 1
#lhour = [12]
region= "ASAS"
ny    = 180
nx    = 360
prtype = "GPCP1DD"
#prtype = "JRA25"
miss   = -9999.0
miss  = -9999.0
miss_gpcp = -99999.
#lthdist   = [250,500,1000,1500]
lthdist   = [500]
sreol     = "anl_p"
#-- para for objective locator -------------
plev     = 850*100.0 # (Pa)
#llthfmask = [[0.3,2.0]]
#llthfmask = [[0.5,2.0],[0.8,2.0],[1.0,2.0],[0.5,2.5],[0.5,3.0]]
#llthfmask = [[0.5,2.0]]
#llthfmask = [[0.2,2.0],[0.3,2.0]]
#llthfmask = [[0.4,2.0]]
llthfmask  = [[0.7,4.0]]

thorog  = ctrack_para.ret_thorog()
thgradorog=ctrack_para.ret_thgradorog()
#-------------------------------------------
#----------------------------
#-- orog --------------------
orogname = "/media/disk2/data/JRA25/sa.one/const/topo/topo.sa.one"
a2orog   = fromfile(orogname, float32).reshape(ny,nx)
gradorogadjname= "/media/disk2/data/JRA25/sa.one/const/topo/grad.topo.adj.twogrids.sa.one"
a2gradorogmask = fromfile(gradorogadjname, float32).reshape(ny,nx)

a2shade  = ma.masked_where(a2orog >thorog, a2orog).filled(miss)
a2shade  = ma.masked_where(a2gradorogmask >thgradorog, a2shade).filled(miss)
#***************************************
##***************************************
#for season in lseason:
#  lmon  = ctrack_para.ret_lmon(season)
#
#  #**********************************************
#  # figure :total preparation
#  if singleday==True:
#    bnd = [0,5,10,15,20,25,30]
#  elif len(lmon)==1:
#    bnd = [5,10,20,30,60,90,150,210,300]
#  elif len(lmon)==3:
#    #bnd = [20,50,100,150,200,300,400,500,600] 
#    bnd = [5,10,20,30,60,90,150,210,300]
#  elif len(lmon)==12:
#    bnd = [100,300,500,700,900,1100,1300,1500,1700,1900,2100]
#
#  #----------------------------------------------
#  odir_root  = "/media/disk2/out/JRA25/sa.one.%s/6hr/tenkizu/front/agg/%04d-%04d/%s"%(sresol,iyear, eyear, season)
#  odir       = odir_root
#  ctrack_func.mk_dir(odir)
#  #-------
#  for lthfmask in llthfmask:
#    thfmask1, thfmask2 = lthfmask 
#    #------
#    for thdist in lthdist:
#      #----
#      tkey  = (thfmask1, thfmask2, thdist)
#      #-- oname  ----
#      soname = odir + "/rad%04d.M1_%s_M2_%s.saone"%(thdist,thfmask1, thfmask2)
#      #-- init -------
#      a2out  = zeros([ny,nx], float32)
#      #---------------
#      dsname = {}
#      da2in  = {}
#      for mon in lmon:
#        #-- load data ---
#        datdir_root  = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/front/agg/%04d-%04d/%s"%(iyear, eyear, mon)
#        datdir       = datdir_root
#        datname = datdir + "/rad%04d.M1_%s_M2_%s.saone"%(thdist,thfmask1, thfmask2)
#        a2in    = fromfile(datname, float32).reshape(ny,nx)
#        a2out   = a2out + ma.masked_where(a2shade==miss, a2in)
#
#      #-- save --------
#      a2out     = ma.masked_where(a2shade==miss, a2out).filled(miss)
#      a2out.tofile(soname)
#
#      #-- fig: name ---
#      figdir         = odir
#      ctrack_func.mk_dir(figdir)
#      figname_all    = figdir + "/front.s%s.rad%04d.M1_%s_M2_%s.png"%(season,thdist, thfmask1, thfmask2)
#      #-- fig: prep -
#      cbarname = figdir + "/front.cbar.png" 
#      stitle   = "season:%s M1:%s  M2:%s"%(season,thfmask1, thfmask2)
#      mycm     = "Spectral"
#      a2figdat = fromfile(soname, float32).reshape(ny,nx)
#      a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0)
#      #-- fig: draw -
#      ctrack_fig.mk_pict_saone_reg(a2figdat, bnd=bnd, mycm=mycm, soname=figname_all, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
#  
#     
#**********************************************
# figure : fraction of frontal precipitation
#----------------------------------------------
bnd        = [1.0, 10.0, 20.0, 30.0, 40.0, 50.0, 60.0, 70.0, 80.0, 90.0]

for season in lseason:
  lmon  = ctrack_para.ret_lmon(season)
  odir_root  = "/media/disk2/out/JRA25/sa.one.%s/6hr/tenkizu/front/agg/%04d-%04d/%s"%(sresol,iyear, eyear, season)
  odir       = odir_root
  ctrack_func.mk_dir(odir)
  #-------
  for lthfmask in llthfmask:
    thfmask1, thfmask2 = lthfmask 
    #------
    for thdist in lthdist:
      #----
      tkey  = (thfmask1, thfmask2, thdist)
      #-- oname  ----
      soname = odir + "/frac.rad%04d.M1_%s_M2_%s.saone"%(thdist,thfmask1, thfmask2)
      #-- init -------
      a2spr_front= zeros([ny,nx], float32)
      a2spr_plain= zeros([ny,nx], float32)
      
      #---------------
      for mon in lmon:
        #-- load data ---
        # frontal precip --
        datdir_root  = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/front/agg/%04d-%04d/%s"%(iyear, eyear, mon)
        datdir       = datdir_root
        datname = datdir + "/rad%04d.M1_%s_M2_%s.saone"%(thdist,thfmask1, thfmask2)
        a2in    = fromfile(datname, float32).reshape(ny,nx)
        a2spr_front = a2spr_front + ma.masked_equal(a2in, miss).filled(0.0)
  
        # plain precip --
        if prtype == "GPCP1DD":
          plaindir  = "/media/disk2/data/GPCP1DD/v1.2/1dd/mean"
          plainname = plaindir + "/gpcp_1dd_v1.2_p1d.%04d-%04d.%s.bn"%(iyear,eyear,mon)
          a2in    = fromfile(plainname, float32).reshape(ny,nx)
          a2in    = flipud(a2in)
          a2in    = a2in * calendar.monthrange(1999, mon)[1]  #mm/day ->mm/mon
        #-----
        a2spr_plain = a2spr_plain + a2in
      #-- save --------
      a2frac    = ma.masked_where(a2spr_plain <1.0, a2spr_front)/a2spr_plain
      a2frac    = ma.masked_where(a2spr_front <1.0, a2frac)
      a2frac    = a2frac.filled(miss)
      a2frac.tofile(soname)
  
      #-- fig: name ---
      figdir         = odir
      ctrack_func.mk_dir(figdir)
      figname_all    = figdir + "/frac.pr.s%s.rad%04d.M1_%s_M2_%s.png"%(season,thdist, thfmask1, thfmask2)
      #-- fig: prep -
      cbarname = figdir + "/frac.pr.cbar.png" 
      stitle   = "precip fraction,  season:%s M1:%s  M2:%s"%(season,thfmask1, thfmask2)
      mycm     = "Spectral"
      a2figdat = fromfile( soname, float32).reshape(ny,nx)
      a2figdat = ma.masked_equal(a2figdat, miss) * 100.0
      a2figdat = a2figdat.filled(miss)
      #-- fig: draw -
      ctrack_fig.mk_pict_saone_reg(a2figdat, bnd=bnd, soname=figname_all, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname, mycm=mycm)
      print figname_all  
  

