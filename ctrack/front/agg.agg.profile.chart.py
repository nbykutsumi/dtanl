import ctrack_para
import ctrack_func
import matplotlib
import matplotlib.pyplot as plt
import subprocess
from numpy import *
#-----------------------------
#lseason = ["ALL","JJA","DJF"]
lseason = [1]
#lftype  = ["warm","cold","stat"]
lftype  = ["cold"]
#lplev     = [925., 850.,700., 600., 500., 300., 250.]
lplev     = [925., 850.,700., 600., 500., 300.]
ldist_km = [-700,-600,-500,-400,-300,-200,-100,0,100,200,300,400,500,600,700]
region  = "ASAS"
dist_mask= 0. # (km)
#dist_mask= 700. # (km)
#dist_mask= 1400. # (km)
#dist_mask= 2500. # (km)
iyear   = 2001
eyear   = 2010
#eyear   = 2001
nx,ny   = (360,180)
#**** mask *************
lllon     = 100.
lllat     = 0.
urlon     = 210.
urlat     = 41.
dlon,dlat = (1.,1.)
lat_first = -89.5
lon_first = 0.5
a2region  = ctrack_func.mk_region_mask(lllat, urlat, lllon, urlon, nx, ny, lat_first, lon_first, dlat, dlon)
#***********************
for season in lseason:
  lmon  = ctrack_para.ret_lmon(season)
  #-- make theta_e climatology ----
  for mon in lmon:
    scmd  = "python ./mk.mean.theta.py.py %s %s %s %s"%(iyear,eyear,mon,925)
    subprocess.call(scmd, shell=True) 
  #--------------------------------
  dpint       = {}
  dtheta      = {}
  dgradtheta  = {}
  dgrad2theta = {}
  #--------------
  for ftype in lftype: 
    #-----
    dpint[ftype]        = []
    dgradtheta[ftype]   = []
    dgrad2theta[ftype]  = []
    for plev in lplev:
      dtheta[ftype, plev]      = []
    #-----
    for dist_km in ldist_km:
      #** initialize precip *******
      a2num = zeros([ny,nx],float32)
      a2pr  = zeros([ny,nx],float32)

      #** initialize theta  *******
      da2num_theta = {}
      da2theta = {}
      for plev in lplev:
        da2num_theta[plev] = zeros([ny,nx],float32)
        da2theta[plev]     = zeros([ny,nx],float32)

      #** initialize grad theta  *******
      a2num_gradtheta  = zeros([ny,nx],float32)
      a2gradtheta      = zeros([ny,nx],float32)

      #** initialize grad2 theta  *******
      a2num_grad2theta = zeros([ny,nx],float32)
      a2grad2theta     = zeros([ny,nx],float32)

      #--------------------------
      for year in range(iyear, eyear+1):
        for mon in lmon:
          #----------
          if ((year==2010)&(mon==12)):
            continue
          #----------
          print season, ftype, dist_km, year,mon
          #***** precipitation ****************
          idir       = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d/prof"%(year,mon)
          iname_pr   =  idir + "/pr.maskrad.%04dkm.%04dkm.%s.sa.one"%(dist_mask, dist_km, ftype)
          iname_num  =  idir + "/num.maskrad.%04dkm.%04dkm.%s.sa.one"%(dist_mask, dist_km, ftype)
          #--
          a2pr_tmp   =  fromfile(iname_pr,  float32).reshape(ny,nx)
          a2num_tmp  =  fromfile(iname_num, float32).reshape(ny,nx)
          #--
          a2pr       =  a2pr  + a2pr_tmp
          a2num      =  a2num + a2num_tmp

          #***** theta *************************
          idir            = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d/prof"%(year,mon)
          for plev in lplev:
            #--- mean theta ----------
            climdir         = "/media/disk2/out/chart/ASAS/front/agg/%04d-%04d/%s"%(iyear,eyear,mon)
            #climname        = climdir  + "/mean.theta_e.%04dhPa.sa.one"%(plev) 
            climname        = climdir  + "/mean.theta_e.%04dhPa.sa.one"%(925) 
            a2clim          = fromfile(climname, float32).reshape(ny,nx)
            #-------------------------
            iname_theta         =  idir + "/theta.maskrad.%04dkm.%04dkm.%s.%04dhPa.sa.one"%(dist_mask, dist_km, ftype, plev)
            iname_num_theta     =  idir + "/num_theta.maskrad.%04dkm.%04dkm.%s.%04dhPa.sa.one"%(dist_mask, dist_km, ftype, plev)
            #--
            a2theta_tmp         =  fromfile(iname_theta,  float32).reshape(ny,nx)
            a2num_theta_tmp     =  fromfile(iname_num_theta, float32).reshape(ny,nx)
            #--- anomaly -------------
            a2theta_tmp         = a2theta_tmp - a2clim * a2num_theta_tmp
            #-------------------------
            da2theta[plev]      =  da2theta[plev]     + a2theta_tmp
            da2num_theta[plev]  =  da2num_theta[plev] + a2num_theta_tmp

          #***** grad.theta *************************
          idir            = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d/prof"%(year,mon)
          iname_gradtheta         =  idir + "/grad.theta.maskrad.%04dkm.%04dkm.%s.sa.one"%(dist_mask, dist_km, ftype)
          iname_num_gradtheta     =  idir + "/num_grad.theta.maskrad.%04dkm.%04dkm.%s.sa.one"%(dist_mask, dist_km, ftype)
          #--
          a2gradtheta_tmp         =  fromfile(iname_gradtheta,  float32).reshape(ny,nx)
          a2num_gradtheta_tmp     =  fromfile(iname_num_gradtheta, float32).reshape(ny,nx)
          #--
          a2gradtheta             =  a2gradtheta     + a2gradtheta_tmp
          a2num_gradtheta         =  a2num_gradtheta + a2num_gradtheta_tmp

          #***** grad2.theta *************************
          idir            = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d/prof"%(year,mon)
          iname_grad2theta         =  idir + "/grad2.theta.maskrad.%04dkm.%04dkm.%s.sa.one"%(dist_mask, dist_km, ftype)
          iname_num_grad2theta     =  idir + "/num_grad2.theta.maskrad.%04dkm.%04dkm.%s.sa.one"%(dist_mask, dist_km, ftype)
          #--
          a2grad2theta_tmp         =  fromfile(iname_grad2theta,  float32).reshape(ny,nx)
          a2num_grad2theta_tmp     =  fromfile(iname_num_grad2theta, float32).reshape(ny,nx)
          #--
          a2grad2theta      =  a2grad2theta     + a2grad2theta_tmp
          a2num_grad2theta  =  a2num_grad2theta + a2num_grad2theta_tmp

      #** calc precip *******
      pint     = ma.masked_where(a2num==0.0, a2pr).sum() / a2num.sum() * 60.*60.  # (mm/hour)
      dpint[ftype].append(pint)

      #** calc theta ********
      for plev in lplev:
        theta    = ma.masked_where(da2num_theta[plev]==0.0, da2theta[plev]).sum() / da2num_theta[plev].sum() # (K)
        dtheta[ftype,plev].append(theta)

      #** calc gradtheta ********
      gradtheta    = ma.masked_where(a2num_gradtheta==0.0, a2gradtheta).sum() / a2num_gradtheta.sum() # (K)
      dgradtheta[ftype].append(gradtheta)

      #** calc grad2theta ********
      grad2theta    = ma.masked_where(a2num_grad2theta==0.0, a2grad2theta).sum() / a2num_grad2theta.sum() # (K)
      dgrad2theta[ftype].append(grad2theta)


  #***********************************************
  #** figure precip *******
  figplot   = plt.figure()
  axplot    = figplot.add_axes([0.2, 0.2, 0.7, 0.7])
  #-- linestyle -------
  dstyle    = {"warm":"-", "cold": "--", "stat": "-."}  

  #--------------------
  for ftype in lftype:
    ly      = dpint[ftype]
    lx      = ldist_km
    axplot.plot(lx,ly, color="k", linewidth=2, linestyle=dstyle[ftype])
  #-- set axis limit ---
  axplot.set_ylim( (0.0, 0.6) )
  #-- legend -----------
  axplot.legend(lftype)
  #-- axis label -------
  axplot.set_ylabel("Precipitation intensity (mm/hour)", fontsize=18)
  axplot.set_xlabel("Distance from front (km)",fontsize=18)

  #-- title ------------
  axplot.set_title( "%s season:%s maskrad:%04dkm %04d-%04d"%(ftype, season, dist_mask, iyear, eyear))
  #-- save -------------
  pictdir   = "/media/disk2/out/chart/ASAS/front/agg/%04d-%04d/%s/pict"%(iyear,eyear,season)
  ctrack_func.mk_dir(pictdir)
  figname   = pictdir + "/plt.dist.pint.maskrad.%04dkm.%04d-%04d.%s.%s.png"%(dist_mask, iyear,eyear,season,region)
  figplot.savefig(figname)
  print figname

  #***********************************************
  #** contour theta *******
  for ftype in lftype:
    plt.clf()
    figcont   = plt.figure()
    axcont    = figcont.add_axes([0.2, 0.2, 0.7, 0.7])
    #---------------------
    lx      = ldist_km
    ly      = lplev

    #-- for contour ------
    a2x, a2y  = meshgrid(lx, ly)
    #
    a2v       = zeros([len(ly),len(lx)],float32)
    for i in arange(len(ly)):
      plev    = ly[i]
      a2v[i]  = dtheta[ftype, plev]
    #--- draw contour ----
    #levels    = arange(250,380,2.0)
    levels    = arange(-40,40,2.0)
    matplotlib.rcParams["contour.negative_linestyle"] = "solid"
    CS        = axcont.contour(a2x, a2y, a2v, levels=levels, colors="k") 
    #--- inversed axis ----
    axcont.invert_yaxis()

    #--- label ------------
    plt.clabel(CS, levels[::2], inline=1, fontsize=18, fmt="%d")
    #plt.clabel(CS, inline=1, fontsize=18, fmt="%03d")

    #-- axis ticks -------
    #plt.rc("xtick", labelsize=18)
    #plt.rc("ytick", labelsize=18)

    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)

    ##-- title ------------
    #axcont.set_title( "%s season:%s maskrad:%04dkm %04d-%04d"%(ftype, season, dist_mask, iyear, eyear))
    #-- save -------------
    pictdir   = "/media/disk2/out/chart/ASAS/front/agg/%04d-%04d/%s/pict"%(iyear,eyear,season)
    ctrack_func.mk_dir(pictdir)
    figname   = pictdir + "/cont.dist.theta.maskrad.%04dkm.%04d-%04d.%s.%s.%s.png"%(dist_mask, iyear,eyear,season,region,ftype)
    figcont.savefig(figname)
    print figname

  #***********************************************
  #** figure gradtheta *******
  plt.clf()
  figplot   = plt.figure()
  axplot    = figplot.add_axes([0.2, 0.2, 0.7, 0.7])

  #-- linestyle -------
  dstyle    = {"warm":"-", "cold": "--", "stat": "-."}  
  
  #--------------------
  for ftype in lftype:
    ly      = array(dgradtheta[ftype]) * 1000.0*100.0
    lx      = ldist_km
    axplot.plot(lx,ly, color="k", linewidth=2, linestyle=dstyle[ftype])
  #-- set axis limit ---
  #axplot.set_ylim( (0.0, 0.6) )
  #-- legend -----------
  axplot.legend(lftype)
  #-- axis label -------
  axplot.set_ylabel("(K/100km)", fontsize=18)
  axplot.set_xlabel("Distance from front (km)",fontsize=18)

  #-- title ------------
  axplot.set_title( "%s season:%s maskrad:%04dkm %04d-%04d"%(ftype, season, dist_mask, iyear, eyear))
  #-- save -------------
  pictdir   = "/media/disk2/out/chart/ASAS/front/agg/%04d-%04d/%s/pict"%(iyear,eyear,season)
  ctrack_func.mk_dir(pictdir)
  figname   = pictdir + "/plt.dist.grad.theta.maskrad.%04dkm.%04d-%04d.%s.%s.png"%(dist_mask, iyear,eyear,season,region)
  figplot.savefig(figname)
  print figname

  #***********************************************
  #** figure grad2theta *******
  plt.clf()
  figplot   = plt.figure()
  axplot    = figplot.add_axes([0.2, 0.2, 0.7, 0.7])
  #-- linestyle -------
  dstyle    = {"warm":"-", "cold": "--", "stat": "-."}  
  
  #--------------------
  for ftype in lftype:
    ly      = array(dgrad2theta[ftype]) * 1000. * 100. * 1000. *100.
    lx      = ldist_km
    axplot.plot(lx,ly, color="k", linewidth=2, linestyle=dstyle[ftype])
  #-- set axis limit ---
  #axplot.set_ylim( (0.0, 0.6) )
  #-- legend -----------
  axplot.legend(lftype)
  #-- axis label -------
  axplot.set_ylabel("(K / 100km /100km)", fontsize=18)
  axplot.set_xlabel("Distance from front (km)",fontsize=18)

  #-- title ------------
  axplot.set_title( "%s season:%s maskrad:%04dkm %04d-%04d"%(ftype, season, dist_mask, iyear, eyear))
  #-- save -------------
  pictdir   = "/media/disk2/out/chart/ASAS/front/agg/%04d-%04d/%s/pict"%(iyear,eyear,season)
  ctrack_func.mk_dir(pictdir)
  figname   = pictdir + "/plt.dist.grad2theta.maskrad.%04dkm.%04d-%04d.%s.%s.png"%(dist_mask, iyear,eyear,season,region)
  figplot.savefig(figname)
  print figname


