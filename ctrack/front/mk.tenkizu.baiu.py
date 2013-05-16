from numpy import *
from dtanl_fsub import *
import ctrack_func
import calendar
import datetime
import ctrack_fig
#------------------------------------
singleday = True
iyear  = 2004
eyear  = 2004
lmon   = [6]
iday   = 26
sresol = "anl_p"
#ldday  = [-5,-4,-3,-2,1,0,1,2,3,4,5]
ldday  = [-4,-3,-2,1,0,1,2,3,4]
#ldday  = [-3,-2,1,0,1,2,3]
#ldday  = [-2,1,0,1,2]
#ldday  = [1,0,1]
ny,nx  = 180,360
#*************************************
def mk_a2dsta_adv_lateral(a2thetaelow,a2thetaeup,a2ulow,a2uup,a2vlow,a2vup,plevlow,plevup):
  adv_thetae_low = dtanl_fsub.mk_a2thermoadv(a2thetaelow.T, a2ulow.T, a2vlow.T).T
  adv_thetae_up  = dtanl_fsub.mk_a2thermoadv(a2thetaeup.T,  a2uup.T,  a2vup.T ).T
  return  (adv_thetae_low - adv_thetae_up) / (plevlow - plevup)

#-------------------------------------
def mk_a2dsta_adv_vertical(a2thetae1, a2thetae3, a2thetae5, a2omega2, a2omega4, plev1, plev2, plev3, plev4, plev5):
  # from lower to higher 1,2,3,4,5
  da2thetae_low    = (a2thetae1 - a2thetae3)/(plev1 - plev3)
  da2thetae_up     = (a2thetae3 - a2thetae5)/(plev3 - plev5)
  #
  return (a2omega2*0.01*da2thetae_low - a2omega4*0.01*da2thetae_up)/(plev2-plev4)

#*************************************
#-------------------------------------
for year in range(iyear,eyear+1):
  for mon in lmon:
    eday  = calendar.monthrange(year,mon)[1]
    #---------------
    if singleday == True:
      eday = iday
    #---------------
    for day in range(iday,eday+1):
      #-------------
      tname  = "/media/disk2/data/JRA25/sa.one.anl_p/day/TMP/%04d%02d/anl_p.TMP.0850hPa.%04d%02d%02d.sa.one"%(year,mon,year,mon,day)
      qname  = "/media/disk2/data/JRA25/sa.one.anl_p/day/SPFH/%04d%02d/anl_p.SPFH.0850hPa.%04d%02d%02d.sa.one"%(year,mon,year,mon,day)
      uname  = "/media/disk2/data/JRA25/sa.one.anl_p/day/UGRD/%04d%02d/anl_p.UGRD.0850hPa.%04d%02d%02d.sa.one"%(year,mon,year,mon,day)
      vname  = "/media/disk2/data/JRA25/sa.one.anl_p/day/VGRD/%04d%02d/anl_p.VGRD.0850hPa.%04d%02d%02d.sa.one"%(year,mon,year,mon,day)
      thetaename = "/media/disk2/out/JRA25/sa.one.anl_p/day/theta_e"
      #--- time mean -------
      a2thetaemean850 = zeros([ny,nx],float32)
      a2umean850      = zeros([ny,nx],float32)
      a2vmean850      = zeros([ny,nx],float32)
      a2thetaemean500 = zeros([ny,nx],float32)
      a2umean500      = zeros([ny,nx],float32)
      a2vmean500      = zeros([ny,nx],float32)
      #

      a2thetaemean250 = zeros([ny,nx],float32)
      a2thetaemean700 = zeros([ny,nx],float32)
      a2thetaemean925 = zeros([ny,nx],float32)
      #
      a2omegamean850      = zeros([ny,nx],float32)
      a2omegamean500      = zeros([ny,nx],float32)

      #---------------------
      now    = datetime.datetime(year,mon,day)
      for dday in ldday:
        dtime  = datetime.timedelta(days=dday)
        ttime  = now + dtime
        tyear  = ttime.year
        tmon   = ttime.month
        tday   = ttime.day
        #
        uname_t850      = "/media/disk2/data/JRA25/sa.one.anl_p/day/UGRD/%04d%02d/anl_p.UGRD.0850hPa.%04d%02d%02d.sa.one"%(tyear,tmon,tyear,tmon,tday)
        vname_t850      = "/media/disk2/data/JRA25/sa.one.anl_p/day/VGRD/%04d%02d/anl_p.VGRD.0850hPa.%04d%02d%02d.sa.one"%(tyear,tmon,tyear,tmon,tday)
        thetaename_t850 = "/media/disk2/out/JRA25/sa.one.anl_p/day/theta_e/%04d%02d/anl_p.thetae.0850hPa.%04d%02d%02d.sa.one"%(tyear,tmon,tyear,tmon,tday)
        #
        uname_t500      = "/media/disk2/data/JRA25/sa.one.anl_p/day/UGRD/%04d%02d/anl_p.UGRD.0500hPa.%04d%02d%02d.sa.one"%(tyear,tmon,tyear,tmon,tday)
        vname_t500      = "/media/disk2/data/JRA25/sa.one.anl_p/day/VGRD/%04d%02d/anl_p.VGRD.0500hPa.%04d%02d%02d.sa.one"%(tyear,tmon,tyear,tmon,tday)
        thetaename_t500 = "/media/disk2/out/JRA25/sa.one.anl_p/day/theta_e/%04d%02d/anl_p.thetae.0500hPa.%04d%02d%02d.sa.one"%(tyear,tmon,tyear,tmon,tday)

        #
        thetaename_t250 = "/media/disk2/out/JRA25/sa.one.anl_p/day/theta_e/%04d%02d/anl_p.thetae.0250hPa.%04d%02d%02d.sa.one"%(tyear,tmon,tyear,tmon,tday)
        thetaename_t700 = "/media/disk2/out/JRA25/sa.one.anl_p/day/theta_e/%04d%02d/anl_p.thetae.0700hPa.%04d%02d%02d.sa.one"%(tyear,tmon,tyear,tmon,tday)
        thetaename_t925 = "/media/disk2/out/JRA25/sa.one.anl_p/day/theta_e/%04d%02d/anl_p.thetae.0925hPa.%04d%02d%02d.sa.one"%(tyear,tmon,tyear,tmon,tday)

        #
        wname_t500      = "/media/disk2/data/JRA25/sa.one.anl_chipsi/day/VVEL/%04d%02d/anl_chipsi.VVEL.0500hPa.%04d%02d%02d.sa.one"%(tyear,tmon,tyear,tmon,tday)
        wname_t850      = "/media/disk2/data/JRA25/sa.one.anl_chipsi/day/VVEL/%04d%02d/anl_chipsi.VVEL.0500hPa.%04d%02d%02d.sa.one"%(tyear,tmon,tyear,tmon,tday)

        #
        a2thetae_t850  = fromfile(thetaename_t850, float32).reshape(ny,nx)
        a2u_t850       = fromfile(uname_t850, float32).reshape(ny,nx)
        a2v_t850       = fromfile(vname_t850, float32).reshape(ny,nx)
        #
        a2thetae_t500  = fromfile(thetaename_t500, float32).reshape(ny,nx)
        a2u_t500       = fromfile(uname_t500, float32).reshape(ny,nx)
        a2v_t500       = fromfile(vname_t500, float32).reshape(ny,nx)
        #
        a2thetae_t250  = fromfile(thetaename_t250, float32).reshape(ny,nx)
        a2thetae_t700  = fromfile(thetaename_t700, float32).reshape(ny,nx)
        a2thetae_t925  = fromfile(thetaename_t925, float32).reshape(ny,nx)
        #
        a2omega_t850   = fromfile(wname_t850, float32).reshape(ny,nx)
        a2omega_t500   = fromfile(wname_t500, float32).reshape(ny,nx)
        #
        a2thetaemean850  = a2thetaemean850 + a2thetae_t850
        a2umean850       = a2umean850      + a2u_t850
        a2vmean850       = a2vmean850      + a2v_t850
        #
        a2thetaemean500  = a2thetaemean500 + a2thetae_t500
        a2umean500       = a2umean500      + a2u_t500
        a2vmean500       = a2vmean500      + a2v_t500
        #
        a2thetaemean250  = a2thetaemean250 + a2thetae_t250
        a2thetaemean700  = a2thetaemean700 + a2thetae_t700
        a2thetaemean925  = a2thetaemean925 + a2thetae_t925
        #
        a2omegamean850       = a2omegamean850      + a2omega_t850
        a2omegamean500       = a2omegamean500      + a2omega_t500

      #----
      a2thetaemean850   = a2thetaemean850 / len(ldday)
      a2umean850        = a2umean850      / len(ldday)
      a2vmean850        = a2umean850      / len(ldday)
      #----
      a2thetaemean500   = a2thetaemean500 / len(ldday)
      a2umean500        = a2umean500      / len(ldday)
      a2vmean500        = a2umean500      / len(ldday)
      #--
      a2thetaemean250   = a2thetaemean250 / len(ldday)
      a2thetaemean700   = a2thetaemean700 / len(ldday)
      a2thetaemean925   = a2thetaemean925 / len(ldday)
      #--
      a2omegamean850        = a2omegamean850      / len(ldday)
      a2omegamean500        = a2omegamean500      / len(ldday)

      #--
      a2dsta_adv_lateral = mk_a2dsta_adv_lateral(a2thetaemean850, a2thetaemean500, a2umean850, a2umean500, a2vmean850, a2vmean500, 850., 500.)
      #--
      a2sta              = -(a2thetaemean850 - a2thetaemean500)/(850.-500.)
      #-- d(vertical advection) / dp -----
      a2dsta_adv_vertical= mk_a2dsta_adv_vertical(a2thetaemean925, a2thetaemean700, a2thetaemean250, a2omegamean850, a2omegamean500, 925., 850., 700., 500., 250.)

      #-- d( differential advection) /dp ---
      a2dsta_adv  = a2dsta_adv_lateral + a2dsta_adv_vertical

      #--
      a2gradthetae850x, a2gradthetae850y  = dtanl_fsub.mk_a2grad_saone(a2thetaemean850.T)
      a2gradthetae850x = a2gradthetae850x.T
      a2gradthetae850y = a2gradthetae850y.T
      #
      a2thetaeadv850   = a2umean850 * a2gradthetae850x + a2vmean850 * a2gradthetae850y

      #--
      a2gradthetae500x, a2gradthetae500y  = dtanl_fsub.mk_a2grad_saone(a2thetaemean500.T)
      a2gradthetae500x = a2gradthetae500x.T
      a2gradthetae500y = a2gradthetae500y.T
      #
      a2thetaeadv500   = a2umean500 * a2gradthetae500x + a2vmean500 * a2gradthetae500y


      #--- figure dsta lateral----
      bnd  = [-5,-3,-1,1,3,5]
      ctrack_fig.mk_pict_saone_reg_symm(a2dsta_adv_lateral*1.e+7, soname="./dsta.late.png", bnd=bnd, mycm="RdBu",cbarname="./dstat.late.cbar.png")

      #--- figure sta ----
      bnd  = [-0.025, -0.015, -0.005, 0.005, 0.015, 0.025]
      #bnd  = [-0.05,-0.03,-0.01,0.0, 0.01, 0.03, 0.05]
      ctrack_fig.mk_pict_saone_reg_symm(a2sta, soname="./sta.png", bnd=bnd, mycm="RdBu",cbarname="./sta.cbar.png")

      #--- figure dsta vertical ----
      bnd  = [-5,-3,-1,1,3,5]
      ctrack_fig.mk_pict_saone_reg_symm(a2dsta_adv_vertical*1.e+7, soname="./dsta.vert.png", bnd=bnd, mycm="RdBu",cbarname="./dstat.vert.cbar.png")
      #--- figure dsta  ----
      bnd  = [-5,-3,-1,1,3,5]
      ctrack_fig.mk_pict_saone_reg_symm(a2dsta_adv*1.e+7, soname="./dsta.png", bnd=bnd, mycm="RdBu",cbarname="./dstat.cbar.png")



      #--- figure adv850 ----
      bnd   = [-200,-150,-100,-50,0,50,100,150,200]
      ctrack_fig.mk_pict_saone_reg_symm(a2thetaeadv850*1.e+6, soname="./adv850.png", bnd=bnd, mycm="RdBu",cbarname="./adv.cbar.png")

      #--- figure adv500 ----
      bnd   = [-200,-150,-100,-50,0,50,100,150,200]
      ctrack_fig.mk_pict_saone_reg_symm(a2thetaeadv500*1.e+6, soname="./adv500.png", bnd=bnd, mycm="RdBu",cbarname="./adv.cbar.png")


