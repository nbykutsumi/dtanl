import ctrack_para
import ctrack_func
import matplotlib
import matplotlib.pyplot as plt
import subprocess
from numpy import *
#-----------------------------
calcflag = True
iyear   = 2007
#iyear   = 2010
eyear   = 2010
#lseason = ["ALL","JJA","DJF"]
lseason = ["ALL"]
#lseason = [1]
lprtype = ["GSMaP"] 
#lprtype = ["GPCP1DD"] 
#lprtype = ["GSMaP","JRA25.C","JRA25.L","JRA25"] 
laxistype  = ["theta_e"]
#laxistype  = ["theta"]
#lftype  = ["warm","cold","occ","stat"]
lftype  = ["cold"]
ldist_km = [-700,-600,-500,-400,-300,-200,-100,0,100,200,300,400,500,600,700]
#ldist_km = [-500,-400,-300,-200,-100,0,100,200,300,400,500]
region  = "ASAS"
lside   = ["w","c"]
lside_name = ["warm-side","cold-side"]
#-------
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
for prtype in lprtype:
  for axistype in laxistype:
    for season in lseason:
      lmon  = ctrack_para.ret_lmon(season)
      for ftype in lftype:
        if calcflag == True:
          #--------------------------------
          dpint       = {}
          dthermo      = {}
          dgradthermo  = {}
          dgrad2thermo = {}
          #--------------
          for side in lside: 
            #-----
            dpint[side]        = []
            #-----
            for dist_km in ldist_km:
              ##** initialize precip *******
              a2num = zeros([ny,nx],float32)
              a2pr  = zeros([ny,nx],float32)
      
              #--------------------------
              for year in range(iyear, eyear+1):
                for mon in lmon:
                  #----------
                  if ((year==2010)&(mon==12)):
                    continue
                  #----------
                  print season, ftype, dist_km, year,mon
                  #***** precipitation ****************
                  idir       = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d/pr-dist.%s.%speak"%(year,mon,prtype,side)
                  iname_pr   =  idir + "/pr.ax-%s.%04dkm.%s.sa.one"%(axistype,dist_km, ftype)
                  iname_num  =  idir + "/num.ax-%s.%04dkm.%s.sa.one"%(axistype,dist_km, ftype)
                  #--
                  a2pr_tmp   =  fromfile(iname_pr,  float32).reshape(ny,nx)
                  a2num_tmp  =  fromfile(iname_num, float32).reshape(ny,nx)
                  #--
                  a2pr       =  a2pr  + a2pr_tmp
                  a2num      =  a2num + a2num_tmp
     
              #** calc precip *******
              pint     = ma.masked_where(a2num==0.0, a2pr).sum() / a2num.sum() * 60.*60.  # (mm/hour)
              dpint[side].append(pint)

          #***************************
          #  save data for figure
          #----------------------
          for side in lside:
            datdir  = "/home/utsumi/mnt/mizu.tank/utsumi/man.front/%04d-%04d/%s"%(iyear,eyear,season)
            datname = datdir + "/plt.dist.pint.%s.ax-%s.%04d-%04d.%s.%s.%s-side.bn"%(prtype,axistype,iyear,eyear,season,region, side)
            #
            array(dpint[side], float32).tofile( datname )
            print datname

          #-- unit data ----
          sunit    = "mm h-1"
          unitname = datdir + "/plt.dist.pint.unit.txt"
          f=open(unitname,"w"); f.write(sunit); f.close()

        #***********************************************
        #** figure precip *******
        figplot   = plt.figure()
        axplot    = figplot.add_axes([0.2, 0.2, 0.7, 0.7])
        #-- linestyle -------
        #dstyle    = {"warm":"-", "cold": "--", "occ": ":", "stat": "-."}  
        dstyle    = {"w":"-", "c": "--"}  
      
        #--------------------
        for side in lside:
          datdir  = "/home/utsumi/mnt/mizu.tank/utsumi/man.front/%04d-%04d/%s"%(iyear,eyear,season)
          datname = datdir + "/plt.dist.pint.%s.ax-%s.%04d-%04d.%s.%s.%s-side.bn"%(prtype,axistype,iyear,eyear,season,region, side)
          ly      = fromfile(datname ,float32)
          lx      = ldist_km
          axplot.plot(lx,ly, color="k", linewidth=2, linestyle=dstyle[side])
        #-- set axis limit ---
        #axplot.set_ylim( (0.0, 0.6) )
        axplot.set_ylim( (0.0, 3.0) )
        #-- legend -----------
        #legend = axplot.legend(lside)
        legend = axplot.legend(lside_name)
        for label in legend.get_texts():
          label.set_fontsize(20)
  
        for line in legend.get_lines():
          line.set_linewidth(3.0)
  
        #-- axis label -------
        axplot.set_ylabel("Precipitation intensity (mm/hour)", fontsize=20)
        axplot.set_xlabel("Distance from front (km)",fontsize=20)
  
        #-- ticks ------------
        plt.xticks(fontsize=18)
        plt.yticks(fontsize=18)
      
        #-- title ------------
        axplot.set_title( "%s ftype:%s season:%s %04d-%04d"%(prtype, ftype, season, iyear, eyear))
        #-- save -------------
        pictdir   = "/media/disk2/out/chart/ASAS/front/agg/%04d-%04d/%s/pict.twosides"%(iyear,eyear,season)
        ctrack_func.mk_dir(pictdir)
        figname   = pictdir + "/plt.dist.pint.%s.ax-%s.%04d-%04d.%s.%s.png"%(prtype,axistype,iyear,eyear,season,region)
        figplot.savefig(figname)
        print figname
  
 
