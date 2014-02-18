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
iyear = 2007
eyear = 2010
lseason = [1,2,3,4,5,6,7,8,9,10,11,12]
#lseason = [1]
#laxistype = ["theta_e","theta"]
laxistype = ["theta_e"]

#lvar     = ["theta_e","theta"]
#lvar     = ["theta_e"]
#lvar     = ["grad2.theta_e"]
#lvar     = ["SSI"]
#lvar     = ["VVEL"]
lvar     = ["RH"]

#lprtype  = ["GSMaP","GPCP1DD","JRA25"]
#lprtype  = ["GPCP1DD"]
#lprtype  = ["GSMaP","JRA","JRA25.C","JRA25.L"]
lprtype  = ["GSMaP"]
#lprtype  = ["GPCP1DD"]
#lseason = [1]
ldist_km = [-700,-600,-500,-400,-300,-200,-100,0,100,200,300,400,500,600,700] #(km)
plev_sfc = 850
#ldist_km = [-500,-400,-300,-200,-100,0,100,200,300,400,500] #(km)
lplev    = [925,850,700,600,500,300,250]
#lplev    = [plev_sfc]
#lftype = [1,2,3,4]
lftype = [2]
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
def load_a2var(year,mon,day,hour, plev, var):
  tdir_root     = "/media/disk2/data/JRA25/sa.one.anl_p/6hr/TMP"
  qdir_root     = "/media/disk2/data/JRA25/sa.one.anl_p/6hr/SPFH"
  wdir_root     = "//media/disk2/data/JRA25/sa.one.anl_chipsi/6hr/VVEL"

  tdir      = tdir_root     + "/%04d%02d"%(year,mon)
  qdir      = qdir_root     + "/%04d%02d"%(year,mon)
  wdir      = wdir_root     + "/%04d%02d"%(year,mon)

  tname     = tdir          + "/%s.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%("anl_p",plev,year,mon,day,hour)
  qname     = qdir          + "/%s.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%("anl_p",plev,year,mon,day,hour)
  wname     = wdir          + "/%s.VVEL.%04dhPa.%04d%02d%02d%02d.sa.one"%("anl_chipsi",plev,year,mon,day,hour)

  tname_sfc = tdir          + "/%s.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%("anl_p",plev_sfc,year,mon,day,hour)
  qname_sfc = qdir          + "/%s.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%("anl_p",plev_sfc,year,mon,day,hour)


  #-------------
  if var == "theta_e":
    a2t       = fromfile( tname, float32).reshape(ny,nx)   
    a2q       = fromfile( qname, float32).reshape(ny,nx)   
    a2var     = dtanl_fsub.mk_a2theta_e(plev*100.0, a2t.T, a2q.T).T

  elif var == "theta":
    a2t       = fromfile( tname, float32).reshape(ny,nx)   
    a2var     = dtanl_fsub.mk_a2theta(plev*100.0, a2t.T).T

  elif var == "grad2.theta_e":
    a2t       = fromfile( tname, float32).reshape(ny,nx)   
    a2q       = fromfile( qname, float32).reshape(ny,nx)   
    a2value   = dtanl_fsub.mk_a2theta_e(plev*100.0, a2t.T, a2q.T).T
    a2gradvalue = dtanl_fsub.mk_a2grad_abs_saone(a2value.T).T
    a2var       = dtanl_fsub.mk_a2grad_abs_saone(a2gradvalue.T).T
  elif var == "SSI":
    a2t       = fromfile( tname, float32).reshape(ny,nx)   
    a2q       = fromfile( qname, float32).reshape(ny,nx)   

    a2t_sfc   = fromfile( tname_sfc, float32).reshape(ny,nx)
    a2q_sfc   = fromfile( qname_sfc, float32).reshape(ny,nx)

    a2tt      = dtanl_fsub.a2t1_to_a2t2(plev_sfc*100.0, plev*100.0, a2t_sfc.T, a2q_sfc.T, miss).T
    a2var     = ma.masked_equal(a2t, miss) - ma.masked_equal(a2tt, miss)
    a2var     = a2var.filled(miss)
  elif var == "VVEL":
    a2var     = fromfile(wname, float32).reshape(ny,nx)
  elif var == "RH":
    a2t       = fromfile( tname, float32).reshape(ny,nx)   
    a2q       = fromfile( qname, float32).reshape(ny,nx)   

    a2var     = dtanl_fsub.mk_a2rh(a2t.T, a2q.T, plev).T

  #--------------
  return a2var


#-------------------------------------------

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
  for axistype in laxistype:
    a2one   = ones([ny,nx],float32)
    a2zero  = zeros([ny,nx],float32)
    a2miss  = ones([ny,nx],float32) * miss
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
            for side in ["w","c"]:
              for dist_km in ldist_km:
                da2pr [ftype, side, dist_km]    = a2zero.copy()
                da2num[ftype, side, dist_km]   = a2zero.copy()
          #-- init 3D-vars --------
          da2var  = {}
          da2nvar = {}
          for var in lvar:
            for ftype in lftype:
              for side in ["w","c"]:
                for plev in lplev:
                  for dist_km in ldist_km:
                    da2var [var, ftype, side, plev, dist_km] = a2zero.copy()
                    da2nvar[var, ftype, side, plev, dist_km] = a2zero.copy()

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
    
              #-- load theta at low level ------
              a2thermo_tmp= load_a2var(year,mon,day,hour,plev_sfc, axistype)
              #--- grad ----------------------
              a2gradthermo_tmp  = dtanl_fsub.mk_a2grad_abs_saone(a2thermo_tmp.T).T
    
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


              #------------------
              a2chart_screen = a2chart
 
              #***********************************
              for ftype in lftype:
                a2chart_seg        = ma.masked_not_equal(a2chart_screen, ftype).filled(miss)
                #** Precipitation ***********
                # Caution!
                # the warmer side is the lower side of the grad-theta
                #--------------------
                #-- for calc ------    
                da2pr_tmp = {}
                for dist_km in ldist_km:
                  da2pr_tmp[dist_km]  = a2zero.copy()
                #------------------

                for dist_km in ldist_km:
    
                  #a2pr_hs           = ctrack_fsub.find_highsidevalue_saone(a2thermo_tmp.T, a2chart_seg.T, a2pr.T, dist_km*1000.0, miss).T
                  da2pr_tmp[dist_km]    = ctrack_fsub.find_highsidevalue_saone(a2thermo_tmp.T, a2chart_seg.T, a2pr.T, dist_km*1000.0, miss).T
                
                #*********************
                # check high precip side
                #---------------------    
                a2pr_coldside  = a2zero.copy()
                a2pr_warmside  = a2zero.copy()
                a2num_coldside = a2zero.copy()
                a2num_warmside = a2zero.copy()

                #---------------------    
                # cold side 
                #------------
                for dist_km in ldist_km[:(len(ldist_km)-1)/2]:
                  a2num_coldside = a2num_coldside + ma.masked_where(da2pr_tmp[dist_km]==miss, a2one).filled(0.0)
                  a2pr_coldside  = a2pr_coldside  + ma.masked_equal(da2pr_tmp[dist_km], miss).filled(0.0)
                #--
                a2pr_coldside    = (ma.masked_where(a2num_coldside==0.0, a2pr_coldside) / a2num_coldside ).filled(0.0)

                #---------------------
                # warm side 
                #------------
                a2num_warmside = a2zero.copy()
                for dist_km in ldist_km[(len(ldist_km)-1)/2 +1:]:
                  a2num_warmside = a2num_warmside + ma.masked_where(da2pr_tmp[dist_km]==miss, a2one).filled(0.0)
                  a2pr_warmside  = a2pr_warmside  + ma.masked_equal(da2pr_tmp[dist_km], miss).filled(0.0)
                #--
                a2pr_warmside    = (ma.masked_where(a2num_warmside==0.0, a2pr_warmside) / a2num_warmside ).filled(0.0)

                #---------------------
                # warm and cold side mask
                #---------------------
                a2mask_warmside = ma.masked_where(a2pr_warmside <= a2pr_coldside, a2one).filled(miss)
                a2mask_coldside = ma.masked_where(a2pr_warmside >= a2pr_coldside, a2one).filled(miss)
                #---------------------
                for dist_km in ldist_km:
                  #--------------------
                  # SUM: warm side
                  #----------------
                  a2pr_tmp  = ma.masked_where(a2mask_warmside==miss, da2pr_tmp[dist_km]).filled(0.0)
                  a2pr_tmp  = ma.masked_equal(a2pr_tmp, miss).filled(0.0)

                  da2pr[ftype, "w", dist_km] = da2pr[ftype,"w", dist_km] + a2pr_tmp
                  #--
                  a2num_tmp = ma.masked_where(a2mask_coldside==miss, a2one).filled(0.0)

                  da2num[ftype,"w", dist_km] = da2num[ftype,"w", dist_km] + a2num_tmp

                  #--------------------
                  # SUM: cold side
                  #----------------
                  a2pr_tmp  = ma.masked_where(a2pr_warmside >= a2pr_coldside, da2pr_tmp[dist_km]).filled(0.0)
                  a2pr_tmp  = ma.masked_equal(a2pr_tmp, miss).filled(0.0)

                  da2pr[ftype, "c", dist_km] = da2pr[ftype,"c", dist_km] + a2pr_tmp
                  #--
                  a2num_tmp = ma.masked_where(a2pr_warmside <= a2pr_coldside, a2one).filled(0.0)

                  da2num[ftype,"c", dist_km] = da2num[ftype,"c", dist_km] + a2num_tmp


                #*******************************************
                #-- load var at each pressure level ------
                #-----------------
                for var in lvar:
                  for plev in lplev:
                    a2var_tmp  = load_a2var(year,mon,day,hour,plev,var)
                    for dist_km in ldist_km:
                      #******************
                      # Caution!
                      # the warmer side is the lower side of the grad-theta
                      a2var_hs   = ctrack_fsub.find_highsidevalue_saone(a2thermo_tmp.T, a2chart_seg.T, a2var_tmp.T, dist_km*1000.0, miss).T
                      #------------------
    
                      a2var_warmside = ma.masked_where(a2mask_warmside==miss, a2var_hs).filled(0.0)
                      a2var_coldside = ma.masked_where(a2mask_coldside==miss, a2var_hs).filled(0.0)
                      a2nvar_warmside= ma.masked_where(a2mask_warmside==miss, a2one).filled(0.0)
                      a2nvar_coldside= ma.masked_where(a2mask_coldside==miss, a2one).filled(0.0)

                      #---
                      da2var [var,ftype,"w",plev,dist_km]  = da2var [var,ftype,"w",plev,dist_km]  + a2var_warmside
                      da2var [var,ftype,"c",plev,dist_km]  = da2var [var,ftype,"c",plev,dist_km]  + a2var_coldside
                      da2nvar[var,ftype,"w",plev,dist_km]  = da2nvar[var,ftype,"w",plev,dist_km]  + a2nvar_warmside
                      da2nvar[var,ftype,"c",plev,dist_km]  = da2nvar[var,ftype,"c",plev,dist_km]  + a2nvar_coldside
                #-----------------
          ##** output ****************************************
          for side in ["w","c"]:
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
                #***************************************
                # precipitation 
                #---------------------------------------
                odir   = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d/%s-dist.%s.%speak"%(year,mon,"pr",prtype,side)
                ctrack_func.mk_dir(odir)

                oname_pr   = odir + "/pr.ax-%s.%04dkm.%s.sa.one"%(axistype,dist_km, sftype)
                oname_num  = odir + "/num.ax-%s.%04dkm.%s.sa.one"%(axistype,dist_km, sftype)

                #** write *******
                da2pr [ftype, side, dist_km].tofile(oname_pr)
                da2num[ftype, side, dist_km].tofile(oname_num)
                print oname_pr
                #*************************************** 
                # variables
                #--------------------------------------- 
                for var in lvar:
                  odir   = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d/%s-dist.%s.%speak"%(year,mon,var,prtype,side)
                  ctrack_func.mk_dir(odir)
                  for plev in lplev:
                    oname_var  = odir + "/var.ax-%s.%04dkm.%s.%04dhPa.sa.one"%(axistype, dist_km, sftype, plev)
                    oname_num  = odir + "/num.ax-%s.%04dkm.%s.%04dhPa.sa.one"%(axistype, dist_km, sftype, plev)

                    da2var [var,ftype,side,plev,dist_km].tofile(oname_var)
                    da2nvar[var,ftype,side,plev,dist_km].tofile(oname_num)
