import ctrack_para
import ctrack_func
import matplotlib
import matplotlib.pyplot as plt
import subprocess
from numpy import *
#-----------------------------
#revflag  = True
revflag  = False
#lseason = ["ALL","JJA","DJF"]
lseason = ["ALL"]
#lseason = [1]
#lvtype  = ["theta_e","theta"]
#lvtype  = ["theta_e"]
lvtype  = ["theta"]
lftype  = ["warm","cold","occ","stat"]
#lftype  = ["warm"]
lplev     = [925., 850.,700., 600., 500., 300., 250.]
#lplev     = [850.,700., 600., 500., 300., 250.]
ldist_km = [-700,-600,-500,-400,-300,-200,-100,0,100,200,300,400,500,600,700]
region  = "ASAS"
window  = "no"
#window  = "out"
#window  = "in"

dist_mask= 0. # (km)
#dist_mask= 300. # (km)
#dist_mask= 500. # (km)
#dist_mask= 1000. # (km)

iyear   = 2007
eyear   = 2010
#eyear   = 2001
nx,ny   = (360,180)
plev_sfc  = 850.0
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
for vtype in lvtype:
  for season in lseason:
    lmon  = ctrack_para.ret_lmon(season)
    print "aaa",lmon
    #-- make theta_e climatology ----
    for mon in lmon:
      scmd  = "python ./mk.mean.theta.py.py %s %s %s %s %s"%(iyear,eyear,mon,plev_sfc,vtype)
      print scmd
      subprocess.call(scmd, shell=True) 
    #--------------------------------
    dpint       = {}
    dthermo      = {}
    dgradthermo  = {}
    dgrad2thermo = {}
    #--------------
    for ftype in lftype: 
      #-----
      dpint[ftype]        = []
      dgradthermo[ftype]   = []
      dgrad2thermo[ftype]  = []
      for plev in lplev:
        dthermo[ftype, plev]      = []
      #-----
      for dist_km in ldist_km:
        ##** initialize precip *******
        #a2num = zeros([ny,nx],float32)
        #a2pr  = zeros([ny,nx],float32)
  
        #** initialize thermo  *******
        da2num_thermo = {}
        da2thermo = {}
        for plev in lplev:
          da2num_thermo[plev] = zeros([ny,nx],float32)
          da2thermo[plev]     = zeros([ny,nx],float32)
  
        #** initialize grad thermo  *******
        a2num_gradthermo  = zeros([ny,nx],float32)
        a2gradthermo      = zeros([ny,nx],float32)
  
        #** initialize grad2 thermo  *******
        a2num_grad2thermo = zeros([ny,nx],float32)
        a2grad2thermo     = zeros([ny,nx],float32)
  
        #--------------------------
        for year in range(iyear, eyear+1):
          for mon in lmon:
            #----------
            if ((year==2010)&(mon==12)):
              continue
            #----------
            print season, ftype, dist_km, year,mon
            ##***** precipitation ****************
            #idir       = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d/prof"%(year,mon)
            #if window == "no":
            #  #iname_pr   =  idir + "/pr.%s.%s.maskrad.%04dkm.%s.sa.one"%(prtype,vtype,dist_km, ftype)
            #  iname_num  =  idir + "/num.%s.%s.maskrad.%04dkm.%s.sa.one"%(prtype,vtype,dist_km, ftype)
            #elif window in ["in","out"]:
            #  #iname_pr   =  idir + "/pr.%s.%s.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(prtype,vtype,window, dist_mask, dist_km, ftype)
            #  iname_num  =  idir + "/num.%s.%s.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(prtype,vtype,window, dist_mask, dist_km, ftype)
            ##--
            ##a2pr_tmp   =  fromfile(iname_pr,  float32).reshape(ny,nx)
            #a2num_tmp  =  fromfile(iname_num, float32).reshape(ny,nx)
            ##--
            ##a2pr       =  a2pr  + a2pr_tmp
            #a2num      =  a2num + a2num_tmp
  
            #***** theta *************************
            idir            = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d/prof"%(year,mon)
            for plev in lplev:
              #--- mean theta ----------
              climdir         = "/media/disk2/out/chart/ASAS/front/agg/%04d-%04d/%s"%(iyear,eyear,mon)
              climname        = climdir  + "/mean.%s.%04dhPa.sa.one"%(vtype,plev_sfc) 
              a2clim          = fromfile(climname, float32).reshape(ny,nx)
              #-------------------------
              if window == "no":
                iname_thermo         =  idir + "/%s.maskrad.%04dkm.%s.%04dhPa.sa.one"%(vtype, dist_km, ftype, plev)
                iname_num_thermo     =  idir + "/num_%s.maskrad.%04dkm.%s.%04dhPa.sa.one"%(vtype, dist_km, ftype, plev)
              elif window in ["in","out"]:
                iname_thermo         =  idir + "/%s.maskrad.%s.%04dkm.%04dkm.%s.%04dhPa.sa.one"%(vtype, window, dist_mask, dist_km, ftype, plev)
                iname_num_thermo     =  idir + "/num_%s.maskrad.%s.%04dkm.%04dkm.%s.%04dhPa.sa.one"%(vtype, window, dist_mask, dist_km, ftype, plev)
              #--
              a2thermo_tmp         =  fromfile(iname_thermo,  float32).reshape(ny,nx)
              a2num_thermo_tmp     =  fromfile(iname_num_thermo, float32).reshape(ny,nx)
              #--- anomaly -------------
              a2thermo_tmp         = a2thermo_tmp - a2clim * a2num_thermo_tmp
              #-------------------------
              da2thermo[plev]      =  da2thermo[plev]     + a2thermo_tmp
              da2num_thermo[plev]  =  da2num_thermo[plev] + a2num_thermo_tmp
  
            #***** grad.theta *************************
            idir            = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d/prof"%(year,mon)
            if window == "no":
              iname_gradthermo         =  idir + "/grad.%s.maskrad.%04dkm.%s.sa.one"%(vtype, dist_km, ftype)
              iname_num_gradthermo     =  idir + "/num_grad.%s.maskrad.%04dkm.%s.sa.one"%(vtype, dist_km, ftype)
            elif window in ["in","out"]:
              iname_gradthermo         =  idir + "/grad.%s.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(vtype, window, dist_mask, dist_km, ftype)
              iname_num_gradthermo     =  idir + "/num_grad.%s.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(vtype, window, dist_mask, dist_km, ftype)
            #--
            a2gradthermo_tmp         =  fromfile(iname_gradthermo,  float32).reshape(ny,nx)
            a2num_gradthermo_tmp     =  fromfile(iname_num_gradthermo, float32).reshape(ny,nx)
            #--
            a2gradthermo             =  a2gradthermo     + a2gradthermo_tmp
            a2num_gradthermo         =  a2num_gradthermo + a2num_gradthermo_tmp
  
            #***** grad2.theta *************************
            idir            = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d/prof"%(year,mon)
            if window == "no":
              iname_grad2thermo         =  idir + "/grad2.%s.maskrad.%04dkm.%s.sa.one"%(vtype, dist_km, ftype)
              iname_num_grad2thermo     =  idir + "/num_grad2.%s.maskrad.%04dkm.%s.sa.one"%(vtype, dist_km, ftype)
            elif window in ["in","out"]:
              iname_grad2thermo         =  idir + "/grad2.%s.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(vtype, window,dist_mask, dist_km, ftype)
              iname_num_grad2thermo     =  idir + "/num_grad2.%s.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(vtype, window,dist_mask, dist_km, ftype)
            #--
            a2grad2thermo_tmp         =  fromfile(iname_grad2thermo,  float32).reshape(ny,nx)
            a2num_grad2thermo_tmp     =  fromfile(iname_num_grad2thermo, float32).reshape(ny,nx)
            #--
            a2grad2thermo      =  a2grad2thermo     + a2grad2thermo_tmp
            a2num_grad2thermo  =  a2num_grad2thermo + a2num_grad2thermo_tmp
  
        ##** calc precip *******
        #pint     = ma.masked_where(a2num==0.0, a2pr).sum() / a2num.sum() * 60.*60.  # (mm/hour)
        #dpint[ftype].append(pint)
  
        #** calc theta ********
        for plev in lplev:
          thermo    = ma.masked_where(da2num_thermo[plev]==0.0, da2thermo[plev]).sum() / da2num_thermo[plev].sum() # (K)
          dthermo[ftype,plev].append(thermo)
  
        #** calc gradthermo ********
        gradthermo    = ma.masked_where(a2num_gradthermo==0.0, a2gradthermo).sum() / a2num_gradthermo.sum() # (K)
        dgradthermo[ftype].append(gradthermo)
  
        #** calc grad2thermo ********
        grad2thermo    = ma.masked_where(a2num_grad2thermo==0.0, a2grad2thermo).sum() / a2num_grad2thermo.sum() # (K)
        dgrad2thermo[ftype].append(grad2thermo)
  
  
 
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
        a2v[i]  = dthermo[ftype, plev]
      #--- WARM front reverse --
      if (ftype == "warm")&(revflag==True):
        a2v = a2v[:,::-1]

      #--- draw contour ----
      #levels    = arange(250,380,2.0)
      levels    = arange(-60,60,2.0)
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
  
      #-- title ------------
      axcont.set_title( "%s season:%s maskrad:%04dkm %04d-%04d"%(ftype, season, dist_mask, iyear, eyear))
      #-- save -------------
      pictdir   = "/media/disk2/out/chart/ASAS/front/agg/%04d-%04d/%s/pict"%(iyear,eyear,season)
      ctrack_func.mk_dir(pictdir)
      if window == "no":
        figname   = pictdir + "/cont.dist.%s.maskrad.%04d-%04d.%s.%s.%s.png"%(vtype, iyear,eyear,season,region,ftype)
      elif window in ["in","out"]:
        figname   = pictdir + "/cont.dist.%s.maskrad.%s.%04dkm.%04d-%04d.%s.%s.%s.png"%(vtype, window, dist_mask, iyear,eyear,season,region,ftype)

      if (ftype == "warm")&(revflag==True):
        figname = figname.split(".png")[0] + ".REV.png"

      figcont.savefig(figname)
      print figname
  
    #***********************************************
    #** figure grad *******
    plt.clf()
    figplot   = plt.figure()
    axplot    = figplot.add_axes([0.2, 0.2, 0.7, 0.7])
  
    #-- linestyle -------
    dstyle    = {"warm":"-", "cold": "--", "occ": ":", "stat": "-."}  
    
    #--------------------
    for ftype in lftype:
      ly      = array(dgradthermo[ftype]) * 1000.0*100.0
      lx      = ldist_km
      axplot.plot(lx,ly, color="k", linewidth=2, linestyle=dstyle[ftype])
    #-- set axis limit ---
    #axplot.set_ylim( (0.0, 0.6) )
    #-- legend -----------
    legend  = axplot.legend(lftype)
    for label in legend.get_texts():
      label.set_fontsize(20)
    for line in legend.get_lines():
      line.set_linewidth(3.0)

    #-- axis label -------
    axplot.set_ylabel("(K/100km)", fontsize=20)
    axplot.set_xlabel("Distance from front (km)",fontsize=20)

    #-- ticks ------------
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
 
    #-- title ------------
    axplot.set_title( "%s %s season:%s maskrad:%04dkm %04d-%04d"%(vtype, ftype, season, dist_mask, iyear, eyear))
    #-- save -------------
    pictdir   = "/media/disk2/out/chart/ASAS/front/agg/%04d-%04d/%s/pict"%(iyear,eyear,season)
    ctrack_func.mk_dir(pictdir)
    if window == "no":
      figname   = pictdir + "/plt.dist.grad.%s.maskrad.%04d-%04d.%s.%s.png"%(vtype, iyear,eyear,season,region)
    elif window in ["in","out"]:
      figname   = pictdir + "/plt.dist.grad.%s.maskrad.%s.%04dkm.%04d-%04d.%s.%s.png"%(vtype, window, dist_mask, iyear,eyear,season,region)
    figplot.savefig(figname)
    print figname
  
    #***********************************************
    #** figure grad2thermo *******
    plt.clf()
    figplot   = plt.figure()
    axplot    = figplot.add_axes([0.2, 0.2, 0.7, 0.7])
    #-- linestyle -------
    dstyle    = {"warm":"-", "cold": "--", "occ": ":", "stat": "-."}  
    
    #--------------------
    for ftype in lftype:
      ly      = array(dgrad2thermo[ftype]) * 1000. * 100. * 1000. *100.
      lx      = ldist_km
      axplot.plot(lx,ly, color="k", linewidth=2, linestyle=dstyle[ftype])
    #-- set axis limit ---
    #axplot.set_ylim( (0.0, 0.6) )
    #-- legend -----------
    legend  =  axplot.legend(lftype)
    for label in legend.get_texts():
      label.set_fontsize(20)

    for line in legend.get_lines():
      line.set_linewidth(3.0)

    #-- axis label -------
    axplot.set_ylabel("(K / 100km /100km)", fontsize=20)
    axplot.set_xlabel("Distance from front (km)",fontsize=20)

    #-- ticks ------------
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
  
    #-- title ------------
    axplot.set_title( "%s %s season:%s maskrad:%04dkm %04d-%04d"%(vtype, ftype, season, dist_mask, iyear, eyear))
    #-- save -------------
    pictdir   = "/media/disk2/out/chart/ASAS/front/agg/%04d-%04d/%s/pict"%(iyear,eyear,season)
    ctrack_func.mk_dir(pictdir)
    if window == "no":
      figname   = pictdir + "/plt.dist.grad2%s.maskrad.%04d-%04d.%s.%s.png"%(vtype, iyear,eyear,season,region)
    elif window in ["in","out"]:
      figname   = pictdir + "/plt.dist.grad2%s.maskrad.%s.%04dkm.%04d-%04d.%s.%s.png"%(vtype, window, dist_mask, iyear,eyear,season,region)
    figplot.savefig(figname)
    print figname
  
  
