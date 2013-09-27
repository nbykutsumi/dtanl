import ctrack_para
import ctrack_func
import matplotlib
import matplotlib.pyplot as plt
import subprocess
from numpy import *
#-----------------------------
iyear   = 2001
eyear   = 2009
#lseason = ["ALL","JJA","DJF"]
#lseason = ["ALL"]
lseason = [1]
lprtype = ["GSMaP"] 
#lprtype = ["GPCP1DD"] 
#lprtype = ["GSMaP","JRA25.C","JRA25.L","JRA25"] 
lvtype  = ["theta_e"]
lftype  = ["warm","cold","occ","stat"]
#lftype  = ["warm","cold","stat"]
ldist_km = [-700,-600,-500,-400,-300,-200,-100,0,100,200,300,400,500,600,700]
region  = "ASAS"
window  = "no"
#window  = "out"
#window  = "in"
#-------
if window == "no":
  dist_mask= 0. # (km)
else:
  dist_mask= 500. # (km)
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
  for vtype in lvtype:
    for season in lseason:
      lmon  = ctrack_para.ret_lmon(season)
      print "aaa",lmon
      #-- make theta_e climatology ----
      #for mon in lmon:
      #  scmd  = "python ./mk.mean.theta.py.py %s %s %s %s %s"%(iyear,eyear,mon,plev_sfc,vtype)
      #  print scmd
      #  subprocess.call(scmd, shell=True) 
      #--------------------------------
      dpint       = {}
      dthermo      = {}
      dgradthermo  = {}
      dgrad2thermo = {}
      #--------------
      for ftype in lftype: 
        #-----
        dpint[ftype]        = []
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
              idir       = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d/pr-dist.%s"%(year,mon,prtype)
              if window == "no":
                iname_pr   =  idir + "/pr.%s.%s.maskrad.%04dkm.%s.sa.one"%(prtype,vtype,dist_km, ftype)
                iname_num  =  idir + "/num.%s.%s.maskrad.%04dkm.%s.sa.one"%(prtype,vtype,dist_km, ftype)
              elif window in ["in","out"]:
                iname_pr   =  idir + "/pr.%s.%s.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(prtype,vtype,window, dist_mask, dist_km, ftype)
                iname_num  =  idir + "/num.%s.%s.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(prtype,vtype,window, dist_mask, dist_km, ftype)
              #--
              a2pr_tmp   =  fromfile(iname_pr,  float32).reshape(ny,nx)
              a2num_tmp  =  fromfile(iname_num, float32).reshape(ny,nx)
              #--
              a2pr       =  a2pr  + a2pr_tmp
              a2num      =  a2num + a2num_tmp
   
          #** calc precip *******
          pint     = ma.masked_where(a2num==0.0, a2pr).sum() / a2num.sum() * 60.*60.  # (mm/hour)
          dpint[ftype].append(pint)
    
      #***********************************************
      #** figure precip *******
      figplot   = plt.figure()
      axplot    = figplot.add_axes([0.2, 0.2, 0.7, 0.7])
      #-- linestyle -------
      dstyle    = {"warm":"-", "cold": "--", "occ": ":", "stat": "-."}  
    
      #--------------------
      for ftype in lftype:
        ly      = dpint[ftype]
        lx      = ldist_km
        axplot.plot(lx,ly, color="k", linewidth=2, linestyle=dstyle[ftype])
      #-- set axis limit ---
      #axplot.set_ylim( (0.0, 0.6) )
      axplot.set_ylim( (0.0, 3.0) )
      #-- legend -----------
      axplot.legend(lftype)
      #-- axis label -------
      axplot.set_ylabel("Precipitation intensity (mm/hour)", fontsize=18)
      axplot.set_xlabel("Distance from front (km)",fontsize=18)
    
      #-- title ------------
      axplot.set_title( "%s %s season:%s maskrad:%04dkm %04d-%04d"%(prtype, ftype, season, dist_mask, iyear, eyear))
      #-- save -------------
      pictdir   = "/media/disk2/out/chart/ASAS/front/agg/%04d-%04d/%s/pict"%(iyear,eyear,season)
      ctrack_func.mk_dir(pictdir)
      if window == "no":
        figname   = pictdir + "/plt.dist.pint.%s.%s.maskrad.%04d-%04d.%s.%s.png"%(prtype,vtype,iyear,eyear,season,region)
      elif window in ["in","out"]:
        figname   = pictdir + "/plt.dist.pint.%s.%s.maskrad.%s.%04dkm.%04d-%04d.%s.%s.png"%(prtype,vtype,window,dist_mask, iyear,eyear,season,region)
      figplot.savefig(figname)
      print figname
  
 
