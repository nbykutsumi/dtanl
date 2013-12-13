from ctrack_fsub import *
from numpy import *
import matplotlib.pyplot as plt
import calendar
import ctrack_para, ctrack_func, ctrack_fig
import tc_para, tc_func
import sys, os
#--------------------------------------
#sresol = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lsresol = ["org"]
calcflag   = False
#calcflag   = True
bstflag_tc = "bst"
#iyear   = 1997
#eyear   = 1997
iyear   = 1980
eyear   = 1999
#lseason = ["ALL","DJF","JJA"]
lseason = range(1,12+1)
iday    = 1
ny      = 180
nx      = 360

miss_int= -9999
miss    = -9999.0
# local region ------
#
# corner points should be
# at the center of original grid box
#lllat   = 25.
#urlat   = 50.
#lllon   = 130.
#urlon   = 155.

lllat   = -89.5
urlat   = 89.5
lllon   = 0.5
urlon   = 359.5

thdura_c  = 48
thdura_tc = thdura_c
thorog  = ctrack_para.ret_thorog()
#--------------
a2one   = ones([ny,nx],float32)
#--------------
for season in lseason:
  #----------------------------
  lmon = ctrack_para.ret_lmon(season)
  #lmon = [1]
  #----------------------------
  dlat    = 1.0
  dlon    = 1.0
  a1lat   = arange(-89.5, 89.5 +dlat*0.5,  dlat)
  a1lon   = arange(0.5,   359.5 +dlon*0.5, dlon)
  #----------------------------
  dpgradrange  = ctrack_para.ret_dpgradrange()
  thpgrad = dpgradrange[0][0]
  pgradmin = ctrack_para.ret_dpgradrange()[2][0]  # Pa/1000km
  #-- orog ------------------------
  orogname = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
  a2orog   = fromfile(orogname, float32).reshape(ny,nx)

  a2shade  = ma.masked_where(a2orog >thorog, a2orog).filled(miss)


  #----------------------------
  for sresol in lsresol:
    if bstflag_tc == "bst":
      odir     = "/media/disk2/out/JRA25/sa.one.%s/6hr/exc/c%02dh.bsttc/%04d-%04d.%s"%(sresol,thdura_c,iyear,eyear,season)

    oname    = odir + "/freq.exc.3deg.%stc.%04d-%04d.%s.sa.one"%(bstflag_tc,iyear,eyear,season)
    #*******************
    # tc params
    #-------------------
    thsst    = tc_para.ret_thsst()
    thwind   = tc_para.ret_thwind()
    thrvort  = tc_para.ret_thrvort(sresol)
    thwcore  = tc_para.ret_thwcore(sresol)
    #-------------------
    psldir_root     = "/media/disk2/data/JRA25/sa.one.%s/6hr/PRMSL"%(sresol)
    pgraddir_root   = "/media/disk2/out/JRA25/sa.one.%s/6hr/pgrad"%(sresol)
    lifedir_root    = "/media/disk2/out/JRA25/sa.one.%s/6hr/life"%(sresol)
    #************************************
    # init
    #--------------------
    a2count = zeros([ny,nx],float32)

    #------------------------------------
    if calcflag ==True: 
      for year in range(iyear, eyear+1):
        # TC ----
        dbstxy   = tc_func.ret_ibtracs_dpyxy_saone(year)
        #--------
        for mon in lmon:
          ##############
          eday = calendar.monthrange(year,mon)[1]
          for day in range(iday, eday+1):
            print "freq",sresol,year, mon, day
            for hour in [0, 6, 12, 18]:
      
              stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)
      
              psldir          = psldir_root     + "/%04d%02d"%(year, mon)
              pgraddir        = pgraddir_root   + "/%04d%02d"%(year, mon)
              lifedir         = lifedir_root    + "/%04d%02d"%(year, mon)
              
              pslname         = psldir     + "/anl_p.PRMSL.%s.sa.one"%(stime)
              pgradname       = pgraddir   + "/pgrad.%s.sa.one"%(stime)
              lifename        = lifedir    + "/life.%s.sa.one"%(stime)
              
              a2psl           = fromfile(pslname,   float32).reshape(ny, nx)
              a2pgrad         = fromfile(pgradname, float32).reshape(ny, nx)
              a2life          = fromfile(lifename,  int32).reshape(ny, nx)
              #************************
              # load TCs
              #------------------------
  
              lbstxy  = dbstxy[year,mon,day,hour]
              a2tc      = tc_func.lpyxy2map_saone(lpyxy=lbstxy, vfill=1.0, miss=miss)
              a2tcsurr    = ctrack_fsub.mk_8gridsmask_saone(a2tc.T, miss).T
              #************************
              # screen ExC
              #------------------------
              a2dura      = ctrack_fsub.solvelife(a2life.T, miss_int)[0].T
              a2c         = ma.masked_where(a2dura<thdura_c, a2pgrad)
              a2c         = ma.masked_less(a2c, pgradmin).filled(miss)
              a2c         = ctrack_fsub.mk_8gridsmask_saone(a2c.T, miss).T
                
              #------------------------
              a2count_tmp = ma.masked_where(a2c==miss, a2one).filled(0.0)
              a2count     = a2count + a2count_tmp
              #------------------------

      #-----------
      numtot = ctrack_para.ret_totaldays(iyear,eyear,season)*4
      a2freq = a2count / numtot
      #--- write -----
      ctrack_func.mk_dir(odir)
      a2freq.tofile(oname)
      print oname

    #***************
    # figure
    #---------------
    #  figure all
    #---------------------------
    bnd        = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0]
    #bnd        = [5,10,15,20,25,30,35,40,45]
    #bnd        = [10,20,30,40,50,60,70,80]
    #----------
    figdir   = odir + "/pict"
    ctrack_func.mk_dir(figdir)
    figname  = figdir + "/freq.exc.%stc.%04d-%04d.%s.png"%(bstflag_tc,iyear,eyear,season)
    cbarname = figdir + "/freq.exc.%stc.cbar.%s.png"%(bstflag_tc,season)
    #----------
    stitle   = "freq. exc: w/%s tc season:%s %04d-%04d"%(bstflag_tc, season,iyear, eyear)
    mycm     = "Spectral"
    datname  = oname
    a2figdat = fromfile(datname, float32).reshape(ny,nx)
    #-------------------------------
    a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
    ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
    print figname  
   





