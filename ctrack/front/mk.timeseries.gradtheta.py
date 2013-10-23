from numpy import *
from dtanl_fsub import *
from ctrack_fsub import *
import ctrack_func
import chart_para, ctrack_para
import calendar, datetime

iyear = 2000
eyear = 2010
imon  = 1
emon  = 12
lyear = range(iyear,eyear+1)
lmon  = range(imon,emon+1)
iday  = 1
lhour = [0,6,12,18]
lftype= [1,2,3,4]
ny,nx  = 180,360
plev   = 850  # (hPa)
distkm = 200.0
#-----
miss  = -9999.0
chartdir_root = "/media/disk2/out/chart/ASAS/front"
tdir_root     = "/media/disk2/data/JRA25/sa.one.anl_p/6hr/TMP"
qdir_root     = "/media/disk2/data/JRA25/sa.one.anl_p/6hr/SPFH"
#-----
for year in lyear:
  for mon in lmon:
    #***************************************
    # mask
    #------------------------
    region        = "ASAS"
    nx_fig,ny_fig    = chart_para.ret_nxnyfig(region, year, mon)
    paradate      = datetime.date(year,mon,1)
    xydatadir   = "/media/disk2/out/chart/ASAS/const"
    if (paradate < datetime.date(2006,1,1)):
      name_x_corres = xydatadir + "/stereo.xfort.fig2saone.ASAS.2000.01.bn"
      name_y_corres = xydatadir + "/stereo.yfort.fig2saone.ASAS.2000.01.bn"
      name_domain_mask = xydatadir + "/domainmask_saone.%s.2000.01.bn"%(region)

    if ( datetime.date(2006,1,1)<=paradate<datetime.date(2006,3,1)):
      name_x_corres = xydatadir + "/stereo.xfort.fig2saone.ASAS.2006.01.bn"
      name_y_corres = xydatadir + "/stereo.yfort.fig2saone.ASAS.2006.01.bn"
      name_domain_mask = xydatadir + "/domainmask_saone.%s.2006.01.bn"%(region)

    if ( datetime.date(2006,3,1)<=paradate):
      name_x_corres = xydatadir + "/stereo.xfort.fig2saone.ASAS.2006.03.bn"
      name_y_corres = xydatadir + "/stereo.yfort.fig2saone.ASAS.2006.03.bn"
      name_domain_mask = xydatadir + "/domainmask_saone.%s.2006.03.bn"%(region)
    #----
    a2xfort_corres   = fromfile(name_x_corres, float32).reshape(ny_fig, nx_fig)
    a2yfort_corres   = fromfile(name_y_corres, float32).reshape(ny_fig, nx_fig)
    a2domain_mask    = fromfile(name_domain_mask,float32).reshape(180,360)
    #***************************************
    da2frontgrad  = {}
    da2frontgrade = {}
    da2num        = {}

    for ftype in lftype:
      da2frontgrad[ftype]    = zeros([ny,nx],float32)
      da2frontgrade[ftype]   = zeros([ny,nx],float32)
      da2num[ftype]          = zeros([ny,nx],float32)


    #
    a2gradtheta   = zeros([ny,nx],float32) 
    a2gradthetae  = zeros([ny,nx],float32)

    eday   = calendar.monthrange(year,mon)[1]
    for day in range(iday,eday+1):
      for hour in lhour:
        #*** load ************
        tdir      = tdir_root     + "/%04d%02d"%(year,mon)
        qdir      = qdir_root     + "/%04d%02d"%(year,mon)

        tname     = tdir + "/anl_p.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev,year,mon,day,hour)
        qname     = qdir + "/anl_p.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev,year,mon,day,hour)

        a2t       = fromfile( tname,     float32).reshape(ny,nx)
        a2q       = fromfile( qname,     float32).reshape(ny,nx)


        a2theta   = dtanl_fsub.mk_a2theta(plev*100.0, a2t.T).T
        a2thetae  = dtanl_fsub.mk_a2theta_e(plev*100.0, a2t.T, a2q.T).T          
        #*** grad *************
        a2gradtheta_tmp   = dtanl_fsub.mk_a2grad_abs_saone(a2theta.T).T
        a2gradthetae_tmp  = dtanl_fsub.mk_a2grad_abs_saone(a2thetae.T).T

        a2gradtheta       = a2gradtheta  + a2gradtheta_tmp
        a2gradthetae      = a2gradthetae + a2gradthetae_tmp

        #*** front grad ********
        frontdir        = chartdir_root + "/%04d%02d"%(year,mon)
        frontname       = frontdir      + "/front.ASAS.%04d.%02d.%02d.%02d.sa.one"%(year,mon,day,hour)
        a2front         = fromfile(frontname,float32).reshape(ny,nx)

        for ftype in lftype:
          #a2frontgrad_tmp   = ma.masked_where(a2front !=ftype, a2gradtheta_tmp).filled(0.0)
          #a2frontgrade_tmp  = ma.masked_where(a2front !=ftype, a2gradthetae_tmp).filled(0.0)

          #-- cold side ---
          a2front_seg       = ma.masked_not_equal(a2front, ftype).filled(miss)
          #a2front_seg  = a2front

          a2frontgrad_tmp   = ctrack_fsub.find_highsidevalue_saone(-a2theta.T, a2front_seg.T, a2gradtheta_tmp.T, distkm*1000.0, miss).T
          a2frontgrade_tmp  = ctrack_fsub.find_highsidevalue_saone(-a2thetae.T, a2front_seg.T, a2gradthetae_tmp.T, distkm*1000.0, miss).T



          a2frontgrad_tmp   = ma.masked_equal(a2frontgrad_tmp, miss).filled(0.0)
          a2frontgrade_tmp  = ma.masked_equal(a2frontgrade_tmp, miss).filled(0.0)


          a2num_tmp         = ma.masked_where(a2front !=ftype, ones([ny,nx],float32)).filled(0.0)

          da2frontgrad[ftype]   = da2frontgrad[ftype]  + a2frontgrad_tmp
          da2frontgrade[ftype]  = da2frontgrade[ftype] + a2frontgrade_tmp
          da2num[ftype]         = da2num[ftype]        + a2num_tmp
        #--------------

    #*** output data *********
    totaltimes   = ctrack_para.ret_totaldays(year,year,mon) *4.0
    a2gradtheta  = a2gradtheta  / totaltimes
    a2gradthetae = a2gradthetae / totaltimes


    for ftype in lftype:
      da2frontgrad[ftype]  = (ma.masked_where(da2num[ftype]==0.0, da2frontgrad[ftype]) / da2num[ftype] ).filled(miss)

      da2frontgrade[ftype] = (ma.masked_where(da2num[ftype]==0.0, da2frontgrade[ftype]) / da2num[ftype] ).filled(miss)
    #--------------------
    #*** write ****************

    odir       = "/media/disk2/out/obj.valid/gradtheta/%04d"%(year)
    ctrack_func.mk_dir(odir)
    thetaname  = odir + "/anl_p.plain.gradtheta.%04d.%02d.sa.one"%(year,mon)
    thetaename = odir + "/anl_p.plain.gradtheta_e.%04d.%02d.sa.one"%(year,mon)
   
    a2gradtheta .tofile(thetaname)
    a2gradthetae.tofile(thetaename)
    print thetaname

    for ftype in lftype:
      frontgrad  = odir + "/anl_p.front.gradtheta.%04dkm.%s.%04d.%02d.sa.one"%(distkm,ftype,year,mon)
      frontgrade = odir + "/anl_p.front.gradtheta_e.%04dkm.%s.%04d.%02d.sa.one"%(distkm,ftype,year,mon)

      da2frontgrad[ftype] .tofile(frontgrad) 
      da2frontgrade[ftype].tofile(frontgrade) 

    
