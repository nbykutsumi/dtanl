from numpy import *
from dtanl_fsub import *
import calendar
import ctrack_fig
import ctrack_para
import ctrack_func
import gsmap_func
from ctrack_fsub import *
#----------------------------------------------------
#singleday =True
singleday = False
iyear = 2006
eyear = 2010
lseason = [1,2,3,4,5,6,7,8,9,10,11,12]
#lseason = [1]
window = "no"
#window = "out"
#window = "in"
ldist_km = [-700,-600,-500,-400,-300,-200,-100,0,100,200,300,400,500,600,700] #(km)
#ldist_km = [300.0]  #(km)
#dist_mask = 500.  # (km)
#dist_mask = 1400.  # (km)
#dist_mask = 1800.  # (km)
#dist_mask = 2500.  # (km)
dist_mask = 0.  # (km)
lplev    = [925.,850.,700., 600., 500.,300.,250.,]
plev_sfc = 925
lftype = [1,2,4]
#lftype = [2]
sresol  = "anl_p25"
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
chartdir_root = "/media/disk2/out/chart/ASAS/front"
tdir_root     = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP"%(sresol)
qdir_root     = "/media/disk2/data/JRA25/sa.one.%s/6hr/SPFH"%(sresol)
#------------------------
#************************
lat_first     = -89.5
dlat          = 1.0
dlon          = 1.0
#------------------------
a2one   = ones([ny,nx],float32)
a2zero  = zeros([ny,nx],float32)
for season in lseason:
  lmon     = ctrack_para.ret_lmon(season)
  #------------------------
  for year in range(iyear, eyear+1):
    for mon in lmon:
      print season, year, mon
      #-- init precip ---------
      da2pr   = {}
      da2num  = {}
      for ftype in lftype:
        for dist_km in ldist_km:
          da2pr[ftype, dist_km]    = a2zero.copy()
          da2num[ftype, dist_km]   = a2zero.copy()

      #-- init theta ----------
      da2theta      = {}
      da2num_theta  = {}
      for ftype in lftype:
        for dist_km in ldist_km:
          for plev in lplev:
            da2theta[ftype, dist_km, plev]       = a2zero.copy()
            da2num_theta[ftype, dist_km, plev]   = a2zero.copy()

      #-- init grad theta ----------
      da2gradtheta      = {}
      da2num_gradtheta  = {}
      for ftype in lftype:
        for dist_km in ldist_km:
          da2gradtheta[ftype, dist_km]       = a2zero.copy()
          da2num_gradtheta[ftype, dist_km]   = a2zero.copy()

      #-- init grad2 theta ----------
      da2grad2theta      = {}
      da2num_grad2theta  = {}
      for ftype in lftype:
        for dist_km in ldist_km:
          da2grad2theta[ftype, dist_km]       = a2zero.copy()
          da2num_grad2theta[ftype, dist_km]   = a2zero.copy()


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
          chartname = chartdir      + "/front.ASAS.%04d.%02d.%02d.%02d.saone"%(year,mon,day,hour)
          a2chart   = fromfile(chartname, float32).reshape(ny,nx)

          #-- load theta at each pressure level ------
          da2theta_tmp  = {}
          #-----------------
          for plev in lplev:
            tname     = tdir          + "/%s.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,plev,year,mon,day,hour)
            qname     = qdir          + "/%s.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,plev,year,mon,day,hour)
            a2t                = fromfile(tname,     float32).reshape(ny,nx)
            a2q                = fromfile(qname,     float32).reshape(ny,nx)
            da2theta_tmp[plev] = dtanl_fsub.mk_a2theta_e(plev*100., a2t.T, a2q.T).T

          #--- gradtheta ----------------------
          a2gradtheta_tmp  = dtanl_fsub.mk_a2grad_abs_saone(da2theta_tmp[plev_sfc].T).T

          #--- grad2theta ----------------------
          a2grad2theta_tmp = dtanl_fsub.mk_a2grad_abs_saone(a2gradtheta_tmp.T).T

          #-- load precipitation ----------
          a2pr      = gsmap_func.timeave_gsmap_backward_saone(year,mon,day,hour+1, 2)
          a2pr      = gsmap_func.gsmap2global_one(a2pr, miss) 

          #***********************************
          for ftype in lftype:
            a2chart_seg        = ma.masked_not_equal(a2chart, ftype).filled(miss)
            #-- maskout fronts close to other front type ----
            a2chart_others     = ma.masked_equal(a2chart, ftype).filled(miss)
            a2terr_others      = ctrack_fsub.mk_territory_saone(a2chart_others.T, dist_mask*1000., miss, lat_first, dlat, dlon).T
            #-- make chart_seg ------------------------------
            if window =="no":
              pass
            elif window == "out":
              a2chart_seg        = ma.masked_where(a2terr_others !=miss, a2chart_seg).filled(miss)
            elif window == "in":
              a2chart_seg        = ma.masked_where(a2terr_others ==miss, a2chart_seg).filled(miss)
            #--------------------
            for dist_km in ldist_km:
              #** Precipitation ***********
              # Caution!
              # the warmer side is the lower side of the grad-theta

              a2pr_hs           = ctrack_fsub.find_highsidevalue_saone(da2theta_tmp[plev_sfc].T, a2chart_seg.T, a2pr.T, dist_km*1000.0, miss).T

              # SUM ---
              da2pr[ftype, dist_km] = da2pr[ftype, dist_km] + ma.masked_equal(a2pr_hs,miss).filled(0.0)
              da2num[ftype,dist_km] = da2num[ftype,dist_km] + ma.masked_where(a2pr_hs==miss, a2one).filled(0.0)

              #** theta_e *****************
              # Caution!
              # the warmer side is the lower side of the grad-theta
              for plev in lplev:
                a2theta_hs            = ctrack_fsub.find_highsidevalue_saone(da2theta_tmp[plev_sfc].T, a2chart_seg.T, da2theta_tmp[plev].T, dist_km*1000.0, miss).T
  
                # SUM ---
                da2theta[ftype, dist_km, plev] = da2theta[ftype, dist_km, plev] + ma.masked_equal(a2theta_hs,miss).filled(0.0)
                da2num_theta[ftype,dist_km, plev] = da2num_theta[ftype,dist_km,plev] + ma.masked_where(a2theta_hs==miss, a2one).filled(0.0)

              #** grad theta_e *****************
              # Caution!
              # the warmer side is the lower side of the grad-theta
              a2gradtheta_hs   = ctrack_fsub.find_highsidevalue_saone(da2theta_tmp[plev_sfc].T, a2chart_seg.T, a2gradtheta_tmp.T, dist_km*1000.0, miss).T
  
              # SUM ---
              da2gradtheta[ftype, dist_km]    = da2gradtheta[ftype, dist_km]     + ma.masked_equal(a2gradtheta_hs,miss).filled(0.0)
              da2num_gradtheta[ftype,dist_km] = da2num_gradtheta[ftype, dist_km] + ma.masked_where(a2gradtheta_hs==miss, a2one).filled(0.0)

              #** grad2 theta_e *****************
              # Caution!
              # the warmer side is the lower side of the grad-theta
              a2grad2theta_hs  = ctrack_fsub.find_highsidevalue_saone(da2theta_tmp[plev_sfc].T, a2chart_seg.T, a2grad2theta_tmp.T, dist_km*1000.0, miss).T

              # SUM ---
              da2grad2theta[ftype, dist_km] = da2grad2theta[ftype, dist_km] + ma.masked_equal(a2grad2theta_hs,miss).filled(0.0)
              da2num_grad2theta[ftype,dist_km] = da2num_grad2theta[ftype,dist_km] + ma.masked_where(a2grad2theta_hs==miss, a2one).filled(0.0)


              #------------------
      #** output ****************************************
      odir   = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d/prof"%(year,mon)
      ctrack_func.mk_dir(odir)
      #***
      for ftype in lftype:
        if ftype == 1:
          sftype = "warm"
        elif ftype == 2:
          sftype = "cold"
        elif ftype == 4:
          sftype = "stat"
        #---- 
        for dist_km in ldist_km:
          #** precipitation *************************
          #** names *******
          if window == "no":
            oname_pr   = odir + "/pr.maskrad.%04dkm.%s.sa.one"%(dist_km, sftype)
            oname_num  = odir + "/num.maskrad.%04dkm.%s.sa.one"%(dist_km, sftype)
          elif window in ["in","out"]:
            oname_pr   = odir + "/pr.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(window,dist_mask, dist_km, sftype)
            oname_num  = odir + "/num.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(window,dist_mask, dist_km, sftype)
          #** write *******
          da2pr[ftype, dist_km].tofile(oname_pr)
          da2num[ftype,dist_km].tofile(oname_num)
          print oname_pr

          #** theta *********************************
          for plev in lplev:
            #** names *******
            if window == "no":
              oname_theta      = odir + "/theta.maskrad.%04dkm.%s.%04dhPa.sa.one"%(dist_km, sftype, plev)
              oname_num_theta  = odir + "/num_theta.maskrad.%04dkm.%s.%04dhPa.sa.one"%(dist_km, sftype, plev)
            elif window in ["in","out"]: 
              oname_theta      = odir + "/theta.maskrad.%s.%04dkm.%04dkm.%s.%04dhPa.sa.one"%(window,dist_mask, dist_km, sftype, plev)
              oname_num_theta  = odir + "/num_theta.maskrad.%s.%04dkm.%04dkm.%s.%04dhPa.sa.one"%(window,dist_mask, dist_km, sftype, plev)
            #** write *******
            da2theta[ftype, dist_km, plev].tofile(oname_theta)
            da2num_theta[ftype, dist_km, plev].tofile(oname_num_theta)
            print oname_theta

          #** gradtheta *********************************
          #** names *******
          if window == "no":
            oname_gradtheta      = odir + "/grad.theta.maskrad.%04dkm.%s.sa.one"%(dist_km, sftype)
            oname_num_gradtheta  = odir + "/num_grad.theta.maskrad.%04dkm.%s.sa.one"%(dist_km, sftype)
          elif window in ["in","out"]:
            oname_gradtheta      = odir + "/grad.theta.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(window,dist_mask, dist_km, sftype)
            oname_num_gradtheta  = odir + "/num_grad.theta.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(window,dist_mask, dist_km, sftype)
          #** write *******
          da2gradtheta[ftype, dist_km].tofile(oname_gradtheta)
          da2num_gradtheta[ftype, dist_km].tofile(oname_num_gradtheta)
          print oname_gradtheta

          #** grad2theta *********************************
          #** names *******
          if window == "no":
            oname_grad2theta      = odir + "/grad2.theta.maskrad.%04dkm.%s.sa.one"%(dist_km, sftype)
            oname_num_grad2theta  = odir + "/num_grad2.theta.maskrad.%04dkm.%s.sa.one"%(dist_km, sftype)
          elif window in ["in","out"]:
            oname_grad2theta      = odir + "/grad2.theta.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(window,dist_mask, dist_km, sftype)
            oname_num_grad2theta  = odir + "/num_grad2.theta.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(window,dist_mask, dist_km, sftype)
          #** write *******
          da2grad2theta[ftype, dist_km].tofile(oname_grad2theta)
          da2num_grad2theta[ftype, dist_km].tofile(oname_num_grad2theta)
          print oname_grad2theta


