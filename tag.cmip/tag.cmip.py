from numpy import *
from ctrack_fsub import *
import calendar
import ctrack_func, front_func, cmip_func, tc_func
import ctrack_para, front_para, cmip_para, tc_para
#-------------------------
#singletime = True
singletime = False
#
#lmodel    = ["MRI-CGCM3","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
#lmodel = ["CNRM-CM5","inmcm4","MPI-ESM-MR","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel = ["GFDL-CM3"]
lexpr  = ["historical","rcp85"]
#lexpr  = ["rcp85"]

dyrange= {"historical":[1980,1999], "rcp85":[2080,2099]}

#
lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
iday   = 1
lhour  = [0,6,12,18]
stepday= 0.25

thdura = 48
thdura_tc = thdura
#- dist ----
#dist_tc, dist_c, dist_f
lldist   = array([[1000,1000,500]])*1000.0
#-----------
nx, ny     = (360,180)
miss       = -9999.0
miss_int   = -9999
lat_first  = -89.5
dlat       = 1.0
dlon       = 1.0

#------------
a2one      = ones([ny,nx],float32)
a2oneint   = ones([ny,nx],int32)

#------------
llkey = [[model,expr] for model in lmodel for expr in lexpr]
for model, expr in llkey:
  #------
  iyear,eyear  = dyrange[expr]
  ens   = cmip_para.ret_ens(model, expr, "psl")
  sunit, scalendar = cmip_para.ret_unit_calendar(model,expr)
  #-----------
  pgradmin = ctrack_para.ret_dpgradrange()[2][0]  # Pa/1000km
  #********************
  # Parameters
  #********************
  #--tc ------
  thsst    = tc_para.ret_thsst()
  thwind   = tc_para.ret_thwind()
  thwcore  = tc_para.ret_thwcore(model)
  thrvort  = tc_para.ret_thrvort(model)

  #--front ---
  thorog     = ctrack_para.ret_thorog()
  thgradorog = ctrack_para.ret_thgradorog()
  thgrids    = front_para.ret_thgrids()
  thfmask1t, thfmask2t, thfmask1q, thfmask2q   = front_para.ret_thfmasktq(model)
  
  #-----------
  orogname   = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog/orog.%s.sa.one"%(model,expr,model)
  gradname   = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog/maxgrad.0200km.sa.one"%(model,expr)
  
  a2orog     = fromfile(orogname, float32).reshape(ny,nx)
  a2gradorog = fromfile(gradname, float32).reshape(ny,nx)
  #-----------
  cmiproot        = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr"%(model,expr)
  pgraddir_root   = cmiproot + "/pgrad"
  lifedir_root    = cmiproot + "/life"
  tcdir_root      = cmiproot + "/tc/%02dh"%(thdura_tc)
  frontdir_t_root = cmiproot + "/front.t"
  #******************
  # Time Loop
  #------------------
  a1dtime,a1tnum  = cmip_func.ret_times(iyear,eyear,lmon,sunit,scalendar,stepday,model=model)
  for dtime, tnum in map(None, a1dtime, a1tnum):

    year,mon,day,hour = dtime.year, dtime.month, dtime.day, dtime.hour 
    stime             = "%04d%02d%02d%02d00"%(year, mon, day, hour)
    print year, mon, day, hour

    #****************
    #-- readme
    if ((year == iyear)&(mon==lmon[0])&(day==1)&(hour==0)):
      readmedir  = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/tag"%(model,expr)
      ctrack_func.mk_dir(readmedir)
      readmename = readmedir + "/readme.tag.txt"
      sreadme    =""" 
          #-- tag   ------------------
          a2tag       = zeros([ny,nx],int32)
          a2tag       = a2tag + ma.masked_where(a2trr_tc  ==miss, a2oneint).filled(0)
          a2tag       = a2tag + ma.masked_where(a2trr_c   ==miss, a2oneint).filled(0)*10
          a2tag       = a2tag + ma.masked_where(a2trr_fbc ==miss, a2oneint).filled(0)*100
          a2tag       = a2tag + ma.masked_where(a2trr_nbc ==miss, a2oneint).filled(0)*1000
          """
      f = open(readmename, "w")
      f.write(sreadme)
      f.close()
    #****************
    #---- dir ------------------
    pgraddir    = pgraddir_root   + "/%04d%02d"%(year, mon)
    lifedir     = lifedir_root    + "/%04d%02d"%(year, mon)
    tcdir       = tcdir_root      + "/%04d/%02d"%(year,mon)
    frontdir_t  = frontdir_t_root   + "/%04d%02d"%(year, mon)
    #---- name -----------------
    pgradname   = pgraddir   + "/pgrad.%s.%s.sa.one"%(ens, stime)
    lifename    = lifedir    + "/life.%s.%s.sa.one"%(ens, stime)
    tcname      = tcdir      + "/tc.wc%4.2f.sst%02d.wind%02d.vor%.1e.%s.sa.one"%(thwcore, thsst-273.15, thwind, thrvort, stime)
    # Front
    fronttname1 = frontdir_t + "/front.t.M1.%04d.%02d.%02d.%02d.sa.one"%(year, mon, day, hour)
    fronttname2 = frontdir_t + "/front.t.M2.%04d.%02d.%02d.%02d.sa.one"%(year, mon, day, hour)
    ##########################
    #--- load for c ----------
    a2pgrad     = fromfile(pgradname, float32).reshape(ny,nx)
    a2life      = fromfile(lifename,  int32  ).reshape(ny,nx)
  
    ##########################
    #--- load front.t -----------
    a2fbc1      = fromfile(fronttname1, float32).reshape(ny,nx)
    a2fbc2      = fromfile(fronttname2, float32).reshape(ny,nx)
    a2fbc       = front_func.complete_front_t_saone(a2fbc1, a2fbc2, thfmask1t, thfmask2t, a2orog, a2gradorog, thorog, thgradorog, thgrids, miss )
  
    ##########################
    #--- load  TC -----------------
    a2tc        = fromfile(tcname,    float32).reshape(ny,nx)

    ##########################
    #-- make exC ---------------
    a2dura      = ctrack_fsub.solvelife(a2life.T, miss_int)[0].T
    a2c         = ma.masked_where(a2dura<thdura, a2pgrad)
    a2c         = ma.masked_less(a2c, pgradmin)
    #-- close to TC --
    a2tcsurr    = ctrack_fsub.mk_8gridsmask_saone(a2tc.T, miss).T
    a2c         = ma.masked_where( a2tcsurr != miss, a2c)
    #----------------- 
    a2c         = a2c.filled(miss)
    ###############################
    #-- territory---------------
    for dist_tc, dist_c, dist_f in lldist:

      a2trr_tc    = ctrack_fsub.mk_territory_saone(a2tc.T, dist_tc, miss, lat_first, dlat, dlon).T
      a2trr_c     = ctrack_fsub.mk_territory_saone(a2c.T,  dist_c,  miss, lat_first, dlat, dlon).T
      a2trr_fbc   = ctrack_fsub.mk_territory_saone(a2fbc.T,  dist_f,  miss, lat_first, dlat, dlon).T
      a2trr_nbc   = a2one*miss
      # 
      #-- tag   ------------------
      a2tag       = zeros([ny,nx],int32)
      a2tag       = a2tag + ma.masked_where(a2trr_tc  ==miss, a2oneint).filled(0)
      a2tag       = a2tag + ma.masked_where(a2trr_c   ==miss, a2oneint).filled(0)*10
      a2tag       = a2tag + ma.masked_where(a2trr_fbc ==miss, a2oneint).filled(0)*100
      a2tag       = a2tag + ma.masked_where(a2trr_nbc ==miss, a2oneint).filled(0)*1000
      #--
      tagdir_root     = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/tag/c%02dh.tc%02dh.tc%04d.c%04d.f%04d"%(model, expr, thdura, thdura_tc, dist_tc/1000.0, dist_c/1000.0, dist_f/1000.0)
  
      tagdir     = tagdir_root + "/%04d%02d"%(year,mon)
      ctrack_func.mk_dir(tagdir_root)
      ctrack_func.mk_dir(tagdir)

      tagname     = tagdir + "/tag.tc%04d.c%04d.f%04d.%04d.%02d.%02d.%02d.sa.one"%(dist_tc/1000, dist_c/1000, dist_f/1000, year, mon, day, hour)
      a2tag.tofile(tagname)
      #
      print tagname
          
