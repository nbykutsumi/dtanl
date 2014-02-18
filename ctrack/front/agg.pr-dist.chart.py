from numpy import *
from dtanl_fsub import *
import calendar
import ctrack_fig
import ctrack_para
import ctrack_func
import gsmap_func
from ctrack_fsub import *
import datetime
#----------------------------------------------------
#singleday =True
singleday = False
iyear = 2006
eyear = 2006
lseason = [1,2,3,4,5,6,7,8,9,10,11,12]
#lseason = [1]
#lvtype = ["theta_e","theta"]
lvtype = ["theta_e"]
#lprtype  = ["GSMaP","GPCP1DD","JRA25"]
#lprtype  = ["GPCP1DD"]
#lprtype  = ["GSMaP","JRA","JRA25.C","JRA25.L"]
lprtype  = ["GSMaP"]
#lprtype  = ["GPCP1DD"]
#lseason = [1]
window = "no"
#window = "out"
#window = "in"
#ldist_km = [-1000,-900,-800,-700,-600,-500,-400,-300,-200,-100,0,100,200,300,400,500,600,700,800,900,1000] #(km)
ldist_km = [-700,-600,-500,-400,-300,-200,-100,0,100,200,300,400,500,600,700] #(km)
#ldist_km = [0.0] #(km)
#ldist_km = [300.0]  #(km)
#dist_mask = 500.  # (km)
#dist_mask = 1400.  # (km)
#dist_mask = 1800.  # (km)
#dist_mask = 2500.  # (km)
dist_mask = 1000.  # (km)
lplev    = [850]
plev_sfc = 850
lftype = [1,2,3,4]
#lftype = [2]
sresol  = "anl_p"
iday  = 1
ny    = 180
nx    = 360
lhour = [0,6,12,18]
#lhour = [0]

lllat = 0.0
lllon = 90
urlat = 80
urlon = 210

#lllat = 0.0
#lllon = 90.0
#urlat = 90.0
#urlon = 140.0

#lllat = 0.0
#lllon = 140.0
#urlat = 80.0
#urlon = 210.0

#-----
miss  = -9999.0
miss_int = -9999
chartdir_root = "/media/disk2/out/chart/ASAS/front"
tdir_root     = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP"%(sresol)
qdir_root     = "/media/disk2/data/JRA25/sa.one.%s/6hr/SPFH"%(sresol)
#------------------------
# for cyclone center
#----------
pgraddir_root   = "/media/disk2/out/JRA25/sa.one.%s/6hr/pgrad"%(sresol)
lifedir_root    = "/media/disk2/out/JRA25/sa.one.%s/6hr/life"%(sresol)
thdura_c        = 48
pgradmin        = ctrack_para.ret_dpgradrange()[2][0]  # Pa/1000km
#************************
lat_first     = -89.5
dlat          = 1.0
dlon          = 1.0

#********************************************
# Function
#-----------
def screen_cyclonearea(year,mon,day,hour,a2chart,dist_c,window):
  #---------------------------
  stime       = "%04d%02d%02d%02d"%(year, mon, day, hour)
  #---- dir ------------------
  pgraddir    = pgraddir_root   + "/%04d%02d"%(year, mon)
  lifedir     = lifedir_root    + "/%04d%02d"%(year, mon)
  #---- name -----------------
  pgradname   = pgraddir   + "/pgrad.%s.sa.one"%(stime)
  lifename    = lifedir    + "/life.%s.sa.one"%(stime)

  #--- load c ----------
  a2pgrad     = fromfile(pgradname, float32).reshape(ny,nx)
  a2life      = fromfile(lifename,  int32  ).reshape(ny,nx)

  ##########################
  #-- make exC ---------------
  a2dura      = ctrack_fsub.solvelife(a2life.T, miss_int)[0].T
  a2c         = ma.masked_where(a2dura<thdura_c, a2pgrad)
  a2c         = ma.masked_less(a2c, pgradmin)
  #-----------------
  a2c         = a2c.filled(miss)
  #-- territory---------------
  a2terr_c     = ctrack_fsub.mk_territory_saone(a2c.T,  dist_c*1000.0,  miss, lat_first, dlat, dlon).T

  if window == "out":
    a2chart_screen  = ma.masked_where(a2terr_c !=miss, a2chart).filled(miss)
  elif window == "in":
    a2chart_screen  = ma.masked_where(a2terr_c ==miss, a2chart).filled(miss)
  #--------------------
  return a2chart_screen
#********************************************

#------------------------
for prtype in lprtype:
  for vtype in lvtype:
    a2one   = ones([ny,nx],float32)
    a2zero  = zeros([ny,nx],float32)
    for season in lseason:
      lmon     = ctrack_para.ret_lmon(season)
      #------------------------
      for year in range(iyear, eyear+1):
        #---------------------
        for mon in lmon:
          print season, year, mon
          #-- init precip ---------
          da2pr   = {}
          da2num  = {}
          for ftype in lftype:
            for dist_km in ldist_km:
              da2pr[ftype, dist_km]    = a2zero.copy()
              da2num[ftype, dist_km]   = a2zero.copy()
    
          #------------------------
          if singleday ==True:
            eday = iday
          else:
            eday = calendar.monthrange(year,mon)[1]
          #----------------
          for day in range(iday, eday+1):
            print year, mon, day
            for hour in lhour:
              chartdir  = chartdir_root + "/%04d%02d"%(year,mon)
              tdir      = tdir_root     + "/%04d%02d"%(year,mon)
              qdir      = qdir_root     + "/%04d%02d"%(year,mon)
              #
              chartname = chartdir      + "/front.ASAS.%04d.%02d.%02d.%02d.sa.one"%(year,mon,day,hour)
              a2chart   = fromfile(chartname, float32).reshape(ny,nx)
    
              #-- load theta at each pressure level ------
              da2thermo_tmp  = {}
              #-----------------
              for plev in lplev:
                tname     = tdir          + "/%s.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,plev,year,mon,day,hour)
                qname     = qdir          + "/%s.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,plev,year,mon,day,hour)
                if vtype =="theta":
                  a2t                = fromfile(tname,     float32).reshape(ny,nx)
                  da2thermo_tmp[plev] = dtanl_fsub.mk_a2theta(plev*100.0, a2t.T).T
                elif vtype == "theta_e":
                  a2t                = fromfile(tname,     float32).reshape(ny,nx)
                  a2q                = fromfile(qname,     float32).reshape(ny,nx)
                  da2thermo_tmp[plev] = dtanl_fsub.mk_a2theta_e(plev*100., a2t.T, a2q.T).T
                else:
                  print "check vtype", vtype
                  sys.exit()
              #--- grad ----------------------
              a2gradthermo_tmp  = dtanl_fsub.mk_a2grad_abs_saone(da2thermo_tmp[plev_sfc].T).T
    
              #--- grad2 ----------------------
              a2grad2thermo_tmp = dtanl_fsub.mk_a2grad_abs_saone(a2gradthermo_tmp.T).T
    
              #-- load precipitation ----------
              if prtype == "GSMaP":
                a2pr      = gsmap_func.timeave_gsmap_backward_saone(year,mon,day,hour+1, 2)
                a2pr      = gsmap_func.gsmap2global_one(a2pr, miss) 
              elif prtype == "GPCP1DD":
                gpcpdir   = "/media/disk2/data/GPCP1DD/v1.2/1dd/%04d"%(year)
                gpcpname  = gpcpdir + "/gpcp_1dd_v1.2_p1d.%04d%02d%02d.bn"%(year,mon,day)
                a2pr      = flipud(fromfile(gpcpname,float32).reshape(ny,nx))
                a2pr      = ma.masked_equal(a2pr, -99999.)/86400. # mm/day->mm/s
              elif prtype == "JRA25":
                timenow   = datetime.datetime(year,mon,day,hour)
                timenext  = timenow + datetime.timedelta(hours=6)
                year0,mon0,day0,hour0 = year,mon,day,hour
                year1,mon1,day1,hour1 = timenext.year, timenext.month, timenext.day, timenext.hour

                jradir0   = "/media/disk2/data/JRA25/sa.one.fcst_phy2m/6hr/PR/%04d%02d"%(year0,mon0)
                jradir1   = "/media/disk2/data/JRA25/sa.one.fcst_phy2m/6hr/PR/%04d%02d"%(year1,mon1)
                 

                jraname0  = jradir0 + "/fcst_phy2m.PR.%04d%02d%02d%02d.sa.one"%(year0,mon0,day0,hour0)
                jraname1  = jradir1 + "/fcst_phy2m.PR.%04d%02d%02d%02d.sa.one"%(year1,mon1,day1,hour1)
                a2pr0     = fromfile(jraname0,float32).reshape(ny,nx)
                a2pr1     = fromfile(jraname1,float32).reshape(ny,nx)
                a2pr      = (a2pr0 + a2pr1)/2.0

              elif prtype == "JRA25.C":
                timenow   = datetime.datetime(year,mon,day,hour)
                timenext  = timenow + datetime.timedelta(hours=6)
                year0,mon0,day0,hour0 = year,mon,day,hour
                year1,mon1,day1,hour1 = timenext.year, timenext.month, timenext.day, timenext.hour

                jradir0   = "/media/disk2/data/JRA25/sa.one.fcst_phy2m/6hr/ACPCP/%04d%02d"%(year0,mon0)
                jradir1   = "/media/disk2/data/JRA25/sa.one.fcst_phy2m/6hr/ACPCP/%04d%02d"%(year1,mon1)
                 

                jraname0  = jradir0 + "/fcst_phy2m.ACPCP.%04d%02d%02d%02d.sa.one"%(year0,mon0,day0,hour0)
                jraname1  = jradir1 + "/fcst_phy2m.ACPCP.%04d%02d%02d%02d.sa.one"%(year1,mon1,day1,hour1)
                a2pr0     = fromfile(jraname0,float32).reshape(ny,nx)
                a2pr1     = fromfile(jraname1,float32).reshape(ny,nx)
                a2pr      = (a2pr0 + a2pr1)/2.0

              elif prtype == "JRA25.L":
                timenow   = datetime.datetime(year,mon,day,hour)
                timenext  = timenow + datetime.timedelta(hours=6)
                year0,mon0,day0,hour0 = year,mon,day,hour
                year1,mon1,day1,hour1 = timenext.year, timenext.month, timenext.day, timenext.hour

                jradir0   = "/media/disk2/data/JRA25/sa.one.fcst_phy2m/6hr/NCPCP/%04d%02d"%(year0,mon0)
                jradir1   = "/media/disk2/data/JRA25/sa.one.fcst_phy2m/6hr/NCPCP/%04d%02d"%(year1,mon1)
                 

                jraname0  = jradir0 + "/fcst_phy2m.NCPCP.%04d%02d%02d%02d.sa.one"%(year0,mon0,day0,hour0)
                jraname1  = jradir1 + "/fcst_phy2m.NCPCP.%04d%02d%02d%02d.sa.one"%(year1,mon1,day1,hour1)
                a2pr0     = fromfile(jraname0,float32).reshape(ny,nx)
                a2pr1     = fromfile(jraname1,float32).reshape(ny,nx)
                a2pr      = (a2pr0 + a2pr1)/2.0


              #-- screen fronts inside/outside of cyclones ----
              if window =="no":
                a2chart_screen = a2chart
              else:
                a2chart_screen = screen_cyclonearea(year,mon,day,hour,a2chart,dist_mask,window)
 
              #***********************************
              for ftype in lftype:
                a2chart_seg        = ma.masked_not_equal(a2chart_screen, ftype).filled(miss)

                #--------------------
                for dist_km in ldist_km:
                  #** Precipitation ***********
                  # Caution!
                  # the warmer side is the lower side of the grad-theta
    
                  a2pr_hs           = ctrack_fsub.find_highsidevalue_saone(da2thermo_tmp[plev_sfc].T, a2chart_seg.T, a2pr.T, dist_km*1000.0, miss).T
    
                  # SUM ---
                  da2pr[ftype, dist_km] = da2pr[ftype, dist_km] + ma.masked_equal(a2pr_hs,miss).filled(0.0)
                  da2num[ftype,dist_km] = da2num[ftype,dist_km] + ma.masked_where(a2pr_hs==miss, a2one).filled(0.0)

          #** output ****************************************
          odir   = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d/pr-dist.%s"%(year,mon,prtype)
          ctrack_func.mk_dir(odir)
          #***
          for ftype in lftype:
            if ftype == 1:
              sftype = "warm"
            elif ftype == 2:
              sftype = "cold"
            elif ftype == 3:
              sftype = "occ"
            elif ftype == 4:
              sftype = "stat"
            #---- 
            for dist_km in ldist_km:
              #** precipitation *************************
              #** names *******
              if window == "no":
                oname_pr   = odir + "/pr.%s.%s.maskrad.%04dkm.%s.sa.one"%(prtype,vtype,dist_km, sftype)
                oname_num  = odir + "/num.%s.%s.maskrad.%04dkm.%s.sa.one"%(prtype,vtype,dist_km, sftype)
              elif window in ["in","out"]:
                oname_pr   = odir + "/pr.%s.%s.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(prtype,vtype,window,dist_mask, dist_km, sftype)
                oname_num  = odir + "/num.%s.%s.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(prtype,vtype,window,dist_mask, dist_km, sftype)
              #** write *******
              da2pr[ftype, dist_km].tofile(oname_pr)
              da2num[ftype,dist_km].tofile(oname_num)
              print oname_pr
    
   
