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
lmon   = [7]
iday   = 16
sresol = "anl_p"
#ldday  = [-10,-9,-8,-7,-6,-5,-4,-3,-2,1,0,1,2,3,4,5,6,7,8,9,10]
#ldday  = [-6,-5,-4,-3,-2,1,0,1,2,3,4,5,6]
#ldday  = [-5,-4,-3,-2,1,0,1,2,3,4,5]
#ldday  = [-4,-3,-2,1,0,1,2,3,4]
ldday  = [-3,-2,1,0,1,2,3]
#ldday  = [-2,1,0,1,2]
#ldday  = [1,0,1]
#ldday  = [0]
ny,nx  = 180,360
miss   = -9999.0
#*************************************
# shresholds  ----
thgradtheta  = 1.0 * 1.e-5  # (K/m)
thgradq      = 0.5 * 1.e-8  # (Kg/Kg/m)
thsta        = 0.01         # (K/hPa)
thdsta       =-1.0 *1.e-2   # (K/ha/day)

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
      #---- instant value -------
      tname  = "/media/disk2/data/JRA25/sa.one.%s/day/TMP/%04d%02d/%s.TMP.0850hPa.%04d%02d%02d.sa.one"%(sresol, year,mon,sresol,year,mon,day)
      qname  = "/media/disk2/data/JRA25/sa.one.%s/day/SPFH/%04d%02d/%s.SPFH.0850hPa.%04d%02d%02d.sa.one"%(sresol, year,mon, sresol, year,mon,day)
      uname  = "/media/disk2/data/JRA25/sa.one.%s/day/UGRD/%04d%02d/%s.UGRD.0850hPa.%04d%02d%02d.sa.one"%(sresol, year,mon, sresol, year,mon,day)
      vname  = "/media/disk2/data/JRA25/sa.one.%s/day/VGRD/%04d%02d/%s.VGRD.0850hPa.%04d%02d%02d.sa.one"%(sresol, year,mon, sresol, year,mon,day)
      thetaename = "/media/disk2/out/JRA25/sa.one.%s/day/theta_e/%04d%02d/anl_p.thetae.0850hPa.%04d%02d%02d.sa.one"%(sresol,year,mon,year,mon,day)
      #
      a2t      = fromfile(tname, float32).reshape(180,360)
      #a2t      = dtanl_fsub.mk_a2theta(850.0*100, a2t.T).T
      a2q      = fromfile(qname, float32).reshape(180,360)
      a2thetae = fromfile(thetaename, float32).reshape(180,360)
      a2gradt  = dtanl_fsub.mk_a2grad_abs_saone(a2t.T).T
      a2gradq  = dtanl_fsub.mk_a2grad_abs_saone(a2q.T).T
      a2gradthetae = dtanl_fsub.mk_a2grad_abs_saone(a2thetae.T).T

      #--- instant 6-hourly data ---
      tname6h  = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP/%04d%02d/%s.TMP.0850hPa.%04d%02d%02d00.sa.one"%(sresol, year,mon,sresol,year,mon,day)
      qname6h  = "/media/disk2/data/JRA25/sa.one.%s/6hr/SPFH/%04d%02d/%s.SPFH.0850hPa.%04d%02d%02d00.sa.one"%(sresol, year,mon, sresol, year,mon,day)
      #
      a2t6h    = fromfile(tname6h, float32).reshape(ny,nx)
      a2q6h    = fromfile(qname6h, float32).reshape(ny,nx)
      a2thetae6h = dtanl_fsub.mk_a2theta_e(850.0*100., a2t6h.T, a2q6h.T).T
      a2gradt6h       = dtanl_fsub.mk_a2grad_abs_saone(a2t6h.T).T
      a2gradq6h       = dtanl_fsub.mk_a2grad_abs_saone(a2q6h.T).T
      a2gradthetae6h  = dtanl_fsub.mk_a2grad_abs_saone(a2thetae6h.T).T
 
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
      # mean q and t
      a2qmean         = zeros([ny,nx],float32)
      a2tmean         = zeros([ny,nx],float32)
      # vorticity ---
      a2svort850      = zeros([ny,nx],float32)
      a2svort500      = zeros([ny,nx],float32)
      a2svort2_850    = zeros([ny,nx],float32)
      a2svort2_500    = zeros([ny,nx],float32)

      #---------------------
      now    = datetime.datetime(year,mon,day)
      for dday in ldday:
        dtime  = datetime.timedelta(days=dday)
        ttime  = now + dtime
        tyear  = ttime.year
        tmon   = ttime.month
        tday   = ttime.day
        #
        uname_t850      = "/media/disk2/data/JRA25/sa.one.%s/day/UGRD/%04d%02d/%s.UGRD.0850hPa.%04d%02d%02d.sa.one"%(sresol,tyear,tmon,sresol,tyear,tmon,tday)
        vname_t850      = "/media/disk2/data/JRA25/sa.one.%s/day/VGRD/%04d%02d/%s.VGRD.0850hPa.%04d%02d%02d.sa.one"%(sresol,tyear,tmon,sresol,tyear,tmon,tday)
        thetaename_t850 = "/media/disk2/out/JRA25/sa.one.%s/day/theta_e/%04d%02d/%s.thetae.0850hPa.%04d%02d%02d.sa.one"%(sresol,tyear,tmon,sresol,tyear,tmon,tday)
        #
        uname_t500      = "/media/disk2/data/JRA25/sa.one.%s/day/UGRD/%04d%02d/%s.UGRD.0500hPa.%04d%02d%02d.sa.one"%(sresol,tyear,tmon,sresol,tyear,tmon,tday)
        vname_t500      = "/media/disk2/data/JRA25/sa.one.%s/day/VGRD/%04d%02d/%s.VGRD.0500hPa.%04d%02d%02d.sa.one"%(sresol,tyear,tmon,sresol,tyear,tmon,tday)
        thetaename_t500 = "/media/disk2/out/JRA25/sa.one.%s/day/theta_e/%04d%02d/%s.thetae.0500hPa.%04d%02d%02d.sa.one"%(sresol,tyear,tmon,sresol,tyear,tmon,tday)

        #
        thetaename_t250 = "/media/disk2/out/JRA25/sa.one.%s/day/theta_e/%04d%02d/%s.thetae.0250hPa.%04d%02d%02d.sa.one"%(sresol,tyear,tmon,sresol,tyear,tmon,tday)
        thetaename_t700 = "/media/disk2/out/JRA25/sa.one.%s/day/theta_e/%04d%02d/%s.thetae.0700hPa.%04d%02d%02d.sa.one"%(sresol,tyear,tmon,sresol,tyear,tmon,tday)
        thetaename_t925 = "/media/disk2/out/JRA25/sa.one.%s/day/theta_e/%04d%02d/%s.thetae.0925hPa.%04d%02d%02d.sa.one"%(sresol,tyear,tmon,sresol,tyear,tmon,tday)

        #
        wname_t500      = "/media/disk2/data/JRA25/sa.one.anl_chipsi/day/VVEL/%04d%02d/anl_chipsi.VVEL.0500hPa.%04d%02d%02d.sa.one"%(tyear,tmon,tyear,tmon,tday)
        wname_t850      = "/media/disk2/data/JRA25/sa.one.anl_chipsi/day/VVEL/%04d%02d/anl_chipsi.VVEL.0500hPa.%04d%02d%02d.sa.one"%(tyear,tmon,tyear,tmon,tday)

        # mean q and t
        qname_t         = "/media/disk2/data/JRA25/sa.one.%s/day/SPFH/%04d%02d/%s.SPFH.0850hPa.%04d%02d%02d.sa.one"%(sresol,tyear,tmon,sresol,tyear,tmon,tday)
        tname_t         = "/media/disk2/data/JRA25/sa.one.%s/day/TMP/%04d%02d/%s.TMP.0850hPa.%04d%02d%02d.sa.one"%(sresol,tyear,tmon,sresol,tyear,tmon,tday)

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
        a2q_t          = fromfile(qname_t, float32).reshape(ny,nx)
        a2t_t          = fromfile(tname_t, float32).reshape(ny,nx)
        a2t_t          = dtanl_fsub.mk_a2theta(850.0*100, a2t_t.T).T
        ##
        #a2omega_t850   = fromfile(wname_t850, float32).reshape(ny,nx)
        #a2omega_t500   = fromfile(wname_t500, float32).reshape(ny,nx)
        #
        a2vort_t850    = dtanl_fsub.mk_a2relative_vorticity(a2u_t850.T, a2v_t850.T).T
        a2vort_t500    = dtanl_fsub.mk_a2relative_vorticity(a2u_t500.T, a2v_t500.T).T


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
        ##
        #a2omegamean850   = a2omegamean850  + a2omega_t850
        #a2omegamean500   = a2omegamean500  + a2omega_t500
        #
        a2qmean          = a2qmean         + a2q_t
        a2tmean          = a2tmean         + a2t_t
        #
        a2svort850       = a2svort850      + a2vort_t850
        a2svort500       = a2svort500      + a2vort_t500
        a2svort2_850     = a2svort2_850    + square(a2vort_t850)
        a2svort2_500     = a2svort2_500    + square(a2vort_t500)

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
      a2omegamean850    = a2omegamean850  / len(ldday)
      a2omegamean500    = a2omegamean500  / len(ldday)
      #
      a2qmean           = a2qmean         / len(ldday)
      a2tmean           = a2tmean         / len(ldday)

      #-- s.d.vort ----------------------------------
      a2vortmean850     = a2svort850      / len(ldday)
      a2vortmean500     = a2svort500      / len(ldday)
      a2sd_vort850      = sqrt( (a2svort2_850 - 2.0*a2vortmean850*a2svort850 + len(ldday)*square(a2vortmean850) )/len(ldday) ) *1.e+6   # (1.0e-6 /sec)
      a2sd_vort500      = sqrt( (a2svort2_500 - 2.0*a2vortmean500*a2svort500 + len(ldday)*square(a2vortmean500) )/len(ldday) ) *1.e+6   # (1.0e-6 /sec)


      #-- grad qmean and tmean ----------------------
      a2gradqmean       = dtanl_fsub.mk_a2grad_abs_saone(a2qmean.T).T
      a2gradtmean       = dtanl_fsub.mk_a2grad_abs_saone(a2tmean.T).T

      #-- d( differential advection)/dp : lateral ---
      a2dsta_adv_lateral = mk_a2dsta_adv_lateral(a2thetaemean850, a2thetaemean500, a2umean850, a2umean500, a2vmean850, a2vmean500, 850., 500.) * 3600*24.
      #--
      a2sta              = -(a2thetaemean850 - a2thetaemean500)/(850.-500.)
      ##-- d(vertical advection) / dp -----
      #a2dsta_adv_vertical= mk_a2dsta_adv_vertical(a2thetaemean925, a2thetaemean700, a2thetaemean250, a2omegamean850, a2omegamean500, 925., 850., 700., 500., 250.) * 3600 *24.

      ##-- d( differential advection) /dp ---
      #a2dsta_adv  = a2dsta_adv_lateral + a2dsta_adv_vertical

      #--
      a2gradthetae850x, a2gradthetae850y  = dtanl_fsub.mk_a2grad_saone(a2thetaemean850.T)
      a2gradthetae850x = a2gradthetae850x.T
      a2gradthetae850y = a2gradthetae850y.T
      #
      a2thetaeadv850   = (a2umean850 * a2gradthetae850x + a2vmean850 * a2gradthetae850y)*3600*24.

      #--
      a2gradthetae500x, a2gradthetae500y  = dtanl_fsub.mk_a2grad_saone(a2thetaemean500.T)
      a2gradthetae500x = a2gradthetae500x.T
      a2gradthetae500y = a2gradthetae500y.T
      #
      a2thetaeadv500   = (a2umean500 * a2gradthetae500x + a2vmean500 * a2gradthetae500y)*3600*24.

      #--- mask layers -----------
      a2mask    = ones([ny,nx],float32)
      #a2mask    = ma.masked_where(a2gradtmean > thgradtheta, a2mask)
      #a2mask    = ma.masked_where(a2gradqmean < thgradq, a2mask)
      #a2mask    = ma.masked_where( ma.masked_outside(a2sta, -thsta, thsta).mask, a2mask)
      a2mask    = ma.masked_where( a2dsta_adv_lateral > thdsta, a2mask)
      a2mask    = a2mask.filled(miss)

      #--- figure baiu ----------
      bnd = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
      #bnd = False
      ctrack_fig.mk_pict_saone_reg(a2gradqmean*1.e+8, a2shade=a2mask, soname="./baiu.gradq.png", bnd=bnd, mycm="jet",cbarname="./baiu.gradq.cbar.png")

      ##---- figure s.d.vort -------
      #bnd = [0,10,20,30,40,50]
      #ctrack_fig.mk_pict_saone_reg(a2sd_vort850, soname="./s.d.vort850.png", bnd=bnd, mycm="jet",cbarname="./s.d.vort.cbar.png")
      #ctrack_fig.mk_pict_saone_reg(a2sd_vort500, soname="./s.d.vort500.png", bnd=bnd, mycm="jet",cbarname="./s.d.vort.cbar.png")

      #--- figure gradq 6h -------
      bnd = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
      #bnd = False
      ctrack_fig.mk_pict_saone_reg(a2gradq6h*1.e+8, soname="./grad.q.6h.png", bnd=bnd, mycm="jet",cbarname="./grad.q.cbar.png")

      #--- figure gradq ----------
      bnd = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
      #bnd = False
      ctrack_fig.mk_pict_saone_reg(a2gradq*1.e+8, soname="./grad.q.day.png", bnd=bnd, mycm="jet",cbarname="./grad.q.cbar.png")

      #--- figure gradt 6h -------
      #bnd = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
      bnd = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
      ctrack_fig.mk_pict_saone_reg(a2gradt6h*1.e+5, soname="./grad.t.6h.png", bnd=bnd, mycm="jet",cbarname="./grad.t.cbar.png")

      #--- figure gradt ----------
      #bnd = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
      bnd = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
      ctrack_fig.mk_pict_saone_reg(a2gradt*1.e+5, soname="./grad.t.day.png", bnd=bnd, mycm="jet",cbarname="./grad.t.cbar.png")

      #--- figure gradthetae 6h ----------
      #bnd = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
      bnd = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
      ctrack_fig.mk_pict_saone_reg(a2gradthetae6h*1.e+5, soname="./grad.thetae.6h.png", bnd=bnd, mycm="jet",cbarname="./grad.t.cbar.png")

      #--- figure gradthetae 6h ----------
      #bnd = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
      bnd = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
      ctrack_fig.mk_pict_saone_reg(a2gradthetae*1.e+5, soname="./grad.thetae.day.png", bnd=bnd, mycm="jet",cbarname="./grad.t.cbar.png")

      ##--- figure gradqmean ------
      #bnd = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
      ##bnd = False
      #ctrack_fig.mk_pict_saone_reg(a2gradqmean*1.e+8, soname="./grad.qmean.png", bnd=bnd, mycm="jet",cbarname="./grad.q.cbar.png")

      ##--- figure gradtmean ------
      ##bnd = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
      #bnd = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
      #ctrack_fig.mk_pict_saone_reg(a2gradtmean*1.e+5, soname="./grad.tmean.png", bnd=bnd, mycm="jet",cbarname="./grad.t.cbar.png")

      #--- figure dsta lateral----
      bnd  = [-0.05, -0.03, -0.01, 0.01, 0.03, 0.05]
      if len(ldday)==1:
        print "AAAA"
        bnd  = [-0.09,-0.07,-0.05, -0.03, -0.01, 0.01, 0.03, 0.05, 0.07,0.09]
      ctrack_fig.mk_pict_saone_reg_symm(a2dsta_adv_lateral, soname="./dsta.late.png", bnd=bnd, mycm="RdBu",cbarname="./dstat.late.cbar.png")

      #--- figure sta ----
      bnd  = [-0.025, -0.015, -0.005, 0.005, 0.015, 0.025]
      #bnd  = [-0.05,-0.03,-0.01,0.0, 0.01, 0.03, 0.05]
      ctrack_fig.mk_pict_saone_reg_symm(a2sta, soname="./sta.png", bnd=bnd, mycm="RdBu",cbarname="./sta.cbar.png")

      ##--- figure dsta vertical ----
      #bnd  = [-0.05, -0.03, -0.01, 0.01, 0.03, 0.05]
      #ctrack_fig.mk_pict_saone_reg_symm(a2dsta_adv_vertical, soname="./dsta.vert.png", bnd=bnd, mycm="RdBu",cbarname="./dstat.vert.cbar.png")
      ##--- figure dsta  ----
      #bnd  = [-0.05, -0.03, -0.01, 0.01, 0.03, 0.05]
      #ctrack_fig.mk_pict_saone_reg_symm(a2dsta_adv, soname="./dsta.png", bnd=bnd, mycm="RdBu",cbarname="./dstat.cbar.png")

      #--- figure adv850 ----
      bnd   = [-20,-15,-10,-5,0,5,10,15,20]
      ctrack_fig.mk_pict_saone_reg_symm(a2thetaeadv850, soname="./adv850.png", bnd=bnd, mycm="RdBu",cbarname="./adv.cbar.png")

      #--- figure adv500 ----
      bnd   = [-20,-15,-10,-5,0,5,10,15,20]
      ctrack_fig.mk_pict_saone_reg_symm(a2thetaeadv500, soname="./adv500.png", bnd=bnd, mycm="RdBu",cbarname="./adv.cbar.png")

