from numpy import *
from ctrack_fsub import *
import calendar
import ctrack_func
import tc_func
import front_func
#-------------------------
#singletime = True
singletime = False
#
#bstflag_tc = "bst"   # "bst" or ""
#bstflag_tc = ""      # "bst" or ""
lbstflag_tc = ["bst"]
#
#bstflag_f  = "bst.high" # "bst.high" or "bst.type" or "" 
#bstflag_f  = "bst.type" # "bst.high" or "bst.type" or ""
lbstflag_f = ["bst.high", "bst.type"]
#lbstflag_f = ["bst.high"]
#
iyear  = 2001
eyear  = 2004
lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
iday   = 1
#lhour  = [0,6,12,18]
lhour  = [0]
thdura = 36
#-----------
pgradmin = 500.0  # Pa/1000km
thbc     = 0.7  /1000/100 # (K/m)
#--tc ------
thwcore = 0.5
thsst   = 273.15 + 25.0
thwind  = 0.0
thrvort = 7.0e-5
#--front ---
thfmask1 = 0.6
thfmask2 = 2.0
#- dist ----
dist_tc    = 500.0 *1000.0 # [m]
dist_c     = 1000.0*1000.0 # [m]
dist_f     = 500.0*1000.0  # [m]
#-----------
nx, ny     = (360,180)
miss       = -9999.0
miss_int   = -9999
lat_first  = -89.5
dlat       = 1.0
dlon       = 1.0
#-----------
pgraddir_root   = "/media/disk2/out/JRA25/sa.one/6hr/pgrad"
lifedir_root    = "/media/disk2/out/JRA25/sa.one/6hr/life"
tcdir_root      = "/media/disk2/out/JRA25/sa.one/6hr/tc/%02dh"%(thdura)
frontdir_root   = "/media/disk2/out/JRA25/sa.one/6hr/front"

#
tagdir_root     = "/media/disk2/out/JRA25/sa.one/6hr/tag"
ctrack_func.mk_dir(tagdir_root)
#------------
a2one      = ones([ny,nx],float32)
a2oneint   = ones([ny,nx],int32)
#------------

#------------
for bstflag_tc in lbstflag_tc:
  for bstflag_f in lbstflag_f:
    for year in range(iyear,eyear+1):
      #- TC BestTrack -
      if bstflag_tc == "bst":
        dbstxy   = tc_func.ret_ibtracs_dpyxy_saone(year)
      #----------------
      for mon in lmon:
        #------------
        eday = calendar.monthrange(year,mon)[1]
    
        #-- readme ----
        tagdir      = tagdir_root + "/%04d%02d"%(year,mon)
        ctrack_func.mk_dir(tagdir)
        readmename = tagdir + "/readme.tc%02d.c%02d.f%02d.txt"%(dist_tc/100/1000, dist_c/100/1000, dist_f/100/1000)
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
        #------------
        if singletime == True:
          print "singletime!!"
          eday = iday
          lhour = [0]
        #------------
        for day in range(iday, eday+1):
          for hour in lhour:
    
            stime       = "%04d%02d%02d%02d"%(year, mon, day, hour)
            print year, mon, day, hour
            #---- dir ------------------
            pgraddir    = pgraddir_root   + "/%04d%02d"%(year, mon)
            lifedir     = lifedir_root    + "/%04d%02d"%(year, mon)
            tcdir       = tcdir_root      + "/%04d/%02d"%(year,mon)
            frontdir    = frontdir_root   + "/%04d%02d"%(year, mon)
            #---- name -----------------
            pgradname   = pgraddir   + "/pgrad.%s.sa.one"%(stime)
            lifename    = lifedir    + "/life.%s.sa.one"%(stime)
            tcname      = tcdir      + "/tc.wc%3.1f.sst%02d.wind%02d.vor%.1e.%s.sa.one"%(thwcore, thsst-273.15, thwind, thrvort, stime)
            frontname   = frontdir   + "/front.M1_%03.1f.M2_%03.1f.%04d.%02d.%02d.%02d.sa.one"%(thfmask1, thfmask2, year, mon, day, hour)
            ##########################
            #--- load for c ----------
            a2pgrad     = fromfile(pgradname, float32).reshape(ny,nx)
            a2life      = fromfile(lifename,  int32  ).reshape(ny,nx)
    
            ##########################
            #--- load front -----------
            if bstflag_f =="bst.high":
              a2f         = front_func.mk_a2chart_gradtv_highside_saone(year, mon,day, hour)
              a2fbc       = ma.masked_less(a2f, thbc).filled(miss)
              a2nbc       = ma.masked_greater_equal(a2f, thbc).filled(miss)
    
            elif bstflag_f == "bst.type":
              frontname = "/media/disk2/out/chart/ASAS/front/%04d%02d/front.ASAS.%04d.%02d.%02d.%02d.saone"%(year,mon,year,mon,day,hour)
              a2f         = fromfile(frontname, float32).reshape(ny,nx)
              a2f         = ma.masked_equal(a2f, miss)
              a2fbc       = ma.masked_equal(a2f, 4.0).filled(miss)
              a2nbc       = ma.masked_not_equal(a2f, 4.0).filled(miss)
     
            elif bstflag_f == "":
              a2f         = fromfile(frontname, float32).reshape(ny,nx)
              a2fbc       = ma.masked_less(a2f, thbc).filled(miss)
              a2nbc       = ma.masked_greater_equal(a2f, thbc).filled(miss)
            #-- front baroclinic & non-baroclinic
    
    
            ##########################
            #--- load  TC -----------------
            a2pgrad     = fromfile(pgradname, float32).reshape(ny,nx)
            ## BEST TC  ###
            if bstflag_tc == "bst":
              lbstxy  = dbstxy[year,mon,day,hour]
              a2tc      = tc_func.lpyxy2map_saone(lpyxy=lbstxy, vfill=1.0, miss=miss)
            ## DETECT TC ##
            else: 
              a2tc        = fromfile(tcname,    float32).reshape(ny,nx)
            ##########################
            #-- make exC ---------------
            a2dura      = ctrack_fsub.solvelife(a2life.T, miss_int)[0].T
            a2c         = ma.masked_where(a2dura<thdura, a2pgrad)
            a2c         = ma.masked_where(a2tc != miss,   a2c)
            a2c         = ma.masked_less(a2c, pgradmin)  
            a2c         = a2c.filled(miss)
            #-- territory---------------
            a2trr_tc    = ctrack_fsub.mk_territory_saone(a2tc.T, dist_tc, miss, lat_first, dlat, dlon).T
            a2trr_c     = ctrack_fsub.mk_territory_saone(a2c.T,  dist_c,  miss, lat_first, dlat, dlon).T
            a2trr_fbc   = ctrack_fsub.mk_territory_saone(a2fbc.T,  dist_f,  miss, lat_first, dlat, dlon).T
            a2trr_nbc   = ctrack_fsub.mk_territory_saone(a2nbc.T,  dist_f,  miss, lat_first, dlat, dlon).T
            # 
            #-- tag   ------------------
            a2tag       = zeros([ny,nx],int32)
            a2tag       = a2tag + ma.masked_where(a2trr_tc  ==miss, a2oneint).filled(0)
            a2tag       = a2tag + ma.masked_where(a2trr_c   ==miss, a2oneint).filled(0)*10
            a2tag       = a2tag + ma.masked_where(a2trr_fbc ==miss, a2oneint).filled(0)*100
            a2tag       = a2tag + ma.masked_where(a2trr_nbc ==miss, a2oneint).filled(0)*1000
            #--
            tagname     = tagdir + "/tag.%stc%02d.c%02d.%sf%02d.%04d.%02d.%02d.%02d.sa.one"%(bstflag_tc, dist_tc/100/1000, dist_c/100/1000, bstflag_f, dist_f/100/1000, year, mon, day, hour)
            a2tag.tofile(tagname)
            #
            print tagname
        
