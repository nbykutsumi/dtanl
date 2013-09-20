from numpy import *
from ctrack_fsub import *
import calendar
import ctrack_func
import tc_func
import front_func
import ctrack_para
import front_para
import tc_para
#-------------------------
#singletime = True
singletime = False
#
sresol = "anl_p"
#
#bstflag_tc = "bst"   # "bst" or ""
#bstflag_tc = ""      # "bst" or ""
#lbstflag_tc = ["","bst"]
lbstflag_tc = ["bst"]
#
#bstflag_f  = "bst.high" # "bst.high" or "bst.type" or "" 
#bstflag_f  = "bst.type" # "bst.high" or "bst.type" or ""
#lbstflag_f = ["bst.high", "bst.type"]
#lbstflag_f = ["","bst"]
lbstflag_f = [""]
#
#iyear  = 2001
#eyear  = 2001
#iyear  = 1997
#eyear  = 2012
iyear  = 2004
eyear  = 2004
lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon   = [1]
iday   = 1
lhour  = [0,6,12,18]
#lhour  = [0]
thdura = 48
#thdura = 72
thdura_tc = thdura
#- dist ----
lldist   = array([[1000,1000,500],[500,500,250],[750,750,375],[1250,1250,625],[1500,1500,750]])*1000.0

#dist_tc    = 1000.0 *1000.0 # [m]
#dist_c     = 1000.0*1000.0 # [m]
#dist_f     = 500.0*1000.0  # [m]

## 80% area
#dist_tc    = 894.0 *1000.0 # [m]
#dist_c     = 894.0*1000.0 # [m]
#dist_f     = 400.0*1000.0  # [m]

## 120% area
#dist_tc    = 1095 *1000.0 # [m]
#dist_c     = 1095 *1000.0 # [m]
#dist_f     = 600.0*1000.0  # [m]

#-----------
pgradmin = ctrack_para.ret_dpgradrange()[2][0]  # Pa/1000km
#----------- 
#--tc ------
#thwcore = 0.5
#thsst   = 273.15 + 25.0
#thwind  = 0.0
#thrvort = 7.0e-5

thsst    = tc_para.ret_thsst()
thwind   = tc_para.ret_thwind()
thwcore  = tc_para.ret_thwcore()
thrvort  = tc_para.ret_thrvort()
#-----------
nx, ny     = (360,180)
miss       = -9999.0
miss_int   = -9999
lat_first  = -89.5
dlat       = 1.0
dlon       = 1.0

#--front ---
thorog     = ctrack_para.ret_thorog()
thgradorog = ctrack_para.ret_thgradorog()
thgrids    = front_para.ret_thgrids()
thfmask1t, thfmask2t, thfmask1q, thfmask2q   = front_para.ret_thfmasktq(sresol)
orogname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
gradname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/maxgrad.0200km.sa.one"
a2orog     = fromfile(orogname, float32).reshape(ny,nx)
a2gradorog = fromfile(gradname, float32).reshape(ny,nx)


#-----------
pgraddir_root   = "/media/disk2/out/JRA25/sa.one.%s/6hr/pgrad"%(sresol)
lifedir_root    = "/media/disk2/out/JRA25/sa.one.%s/6hr/life"%(sresol)
tcdir_root      = "/media/disk2/out/JRA25/sa.one.%s/6hr/tc/%02dh"%(sresol, thdura_tc)
frontdir_t_root   = "/media/disk2/out/JRA25/sa.one.%s/6hr/front.t"%(sresol)
frontdir_q_root   = "/media/disk2/out/JRA25/sa.one.%s/6hr/front.q"%(sresol)

#
#------------
a2one      = ones([ny,nx],float32)
a2oneint   = ones([ny,nx],int32)
#------------

#------------
for ldist in lldist:
  dist_tc, dist_c, dist_f = ldist
  for bstflag_tc in lbstflag_tc:
    for bstflag_f in lbstflag_f:
      #******************
      # tagdir_root
      #------------------
      tagdir_root     = "/media/disk2/out/JRA25/sa.one.%s/6hr/tag/c%02dh.tc%02dh.%stc%04d.c%04d.%sf%04d"%(sresol, thdura, thdura_tc, bstflag_tc, dist_tc/1000.0, dist_c/1000.0, bstflag_f, dist_f/1000.0)
    
      ctrack_func.mk_dir(tagdir_root)
      #------------------
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
          readmename = tagdir + "/readme.tc%04d.c%04d.f%04d.txt"%(dist_tc/1000, dist_c/1000, dist_f/1000)
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
              frontdir_t  = frontdir_t_root   + "/%04d%02d"%(year, mon)
              frontdir_q  = frontdir_q_root   + "/%04d%02d"%(year, mon)
              #---- name -----------------
              pgradname   = pgraddir   + "/pgrad.%s.sa.one"%(stime)
              lifename    = lifedir    + "/life.%s.sa.one"%(stime)
              tcname      = tcdir      + "/tc.wc%4.2f.sst%02d.wind%02d.vor%.1e.%s.sa.one"%(thwcore, thsst-273.15, thwind, thrvort, stime)
              # Front
              fronttname1 = frontdir_t + "/front.t.M1.%04d.%02d.%02d.%02d.sa.one"%(year, mon, day, hour)
              fronttname2 = frontdir_t + "/front.t.M2.%04d.%02d.%02d.%02d.sa.one"%(year, mon, day, hour)
              frontqname1 = frontdir_q + "/front.q.M1.%04d.%02d.%02d.%02d.sa.one"%(year, mon, day, hour)
              frontqname2 = frontdir_q + "/front.q.M2.%04d.%02d.%02d.%02d.sa.one"%(year, mon, day, hour)
              ##########################
              #--- load for c ----------
              a2pgrad     = fromfile(pgradname, float32).reshape(ny,nx)
              a2life      = fromfile(lifename,  int32  ).reshape(ny,nx)
      
              ##########################
              #--- load front -----------
              if bstflag_f =="bst.high":
                a2f         = front_func.mk_a2chart_gradtv_highside_saone(sresol, year, mon,day, hour)
                a2fbc       = ma.masked_less(a2f, thbc).filled(miss)
                a2nbc       = ma.masked_greater_equal(a2f, thbc).filled(miss)
      
              elif bstflag_f == "bst.type":
                frontname = "/media/disk2/out/chart/ASAS/front/%04d%02d/front.ASAS.%04d.%02d.%02d.%02d.saone"%(year,mon,year,mon,day,hour)
                a2f         = fromfile(frontname, float32).reshape(ny,nx)
                a2f         = ma.masked_equal(a2f, miss)
                a2fbc       = ma.masked_equal(a2f, 4.0).filled(miss)
                a2nbc       = ma.masked_not_equal(a2f, 4.0).filled(miss)
       
              elif bstflag_f == "":
                #-- front.t ---
                a2fbc1      = fromfile(fronttname1, float32).reshape(ny,nx)
                a2fbc2      = fromfile(fronttname2, float32).reshape(ny,nx)
                a2fbc       = front_func.complete_front_t_saone(a2fbc1, a2fbc2, thfmask1t, thfmask2t, a2orog, a2gradorog, thorog, thgradorog, thgrids, miss )
  
                #-- front.q ---
                a2nbc1      = fromfile(frontqname1, float32).reshape(ny,nx)
                a2nbc2      = fromfile(frontqname2, float32).reshape(ny,nx)
                a2nbc       = front_func.complete_front_q_saone(a2fbc, a2nbc1, a2nbc2, thfmask1q, thfmask2q, a2orog, a2gradorog, thorog, thgradorog, thgrids, miss)
              ##########################
              #--- load  TC -----------------
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
              a2c         = ma.masked_less(a2c, pgradmin)
              #-- close to TC --
              a2tcsurr    = ctrack_fsub.mk_8gridsmask_saone(a2tc.T, miss).T
              a2c         = ma.masked_where( a2tcsurr != miss, a2c)
              #----------------- 
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
              #tagname     = tagdir + "/tag.%stc%02d.c%02d.%sf%02d.%04d.%02d.%02d.%02d.sa.one"%(bstflag_tc, dist_tc/100/1000, dist_c/100/1000, bstflag_f, dist_f/100/1000, year, mon, day, hour)
              tagname     = tagdir + "/tag.%stc%04d.c%04d.%sf%04d.%04d.%02d.%02d.%02d.sa.one"%(bstflag_tc, dist_tc/1000, dist_c/1000, bstflag_f, dist_f/1000, year, mon, day, hour)
              a2tag.tofile(tagname)
              #
              print tagname
          
