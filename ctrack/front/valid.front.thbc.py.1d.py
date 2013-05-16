import ctrack_func
import ctrack_para
from numpy import *
#---------------------------------------
iyear   = 2001
eyear   = 2003

#----
lseason = [6]
sresol  = "anl_p"
lthfmask1  = [0.7]
lthfmask2  = [3.0, 4.0]
lthbc      = array([0.1,0.3,0.5,0.7,0.9,1.1,1.3,1.5,1.7,1.9,2.1])/1000./100.  # (K/m)
nx,ny      = 360,180
lat_first  = -89.5
lon_first  = 0.5
dlat,dlon  = 1.0, 1.0

#** region mask **********
lllat = 0.0
lllon = 90.0
urlat = 80.0
urlon = 135.0

#--
a2regionmask  = ctrack_func.mk_region_mask(lllat,urlat,lllon,urlon,nx,ny,lat_first,lon_first,dlat,dlon)
#*************************
sidir_root  = "/media/disk2/out/JRA25/sa.one.%s/6hr/front/valid"%(sresol)

#*************************
for season in lseason:
  lmon  = ctrack_para.ret_lmon(season)
  #-- init ----
  a2numchart  = zeros([ny,nx], float32).reshape(ny,nx)
  #---
  da2numobj   = {}
  for thfmask1 in lthfmask1:
    for thfmask2 in lthfmask2:
      for thbc in lthbc:
        key  = thfmask1, thfmask2, thbc
        da2numobj[key]   = zeros([ny,nx], float32).reshape(ny,nx)
  #--
  #--
  for year in range(iyear,eyear+1):
    for mon in lmon:
      sidir             = sidir_root  + "/%04d%02d"%(year,mon)
      #*************************
      namenumchart      = sidir + "/num.stat.chart.sa.one"
      a2numchart_tmp    = fromfile(namenumchart, float32).reshape(ny,nx)
      a2numchart_tmp    = ma.masked_where(a2regionmask==0.0,  a2numchart_tmp)
      a2numchart        = a2numchart  + a2numchart_tmp
      #-------------------------
      for thfmask1 in lthfmask1:
        for thfmask2 in lthfmask2:
          for thbc in lthbc:
            season, year,mon, thfmask1, thfmask2, thbc*1000.*100.
            key  = (thfmask1, thfmask2, thbc)
            #----
            namenumobj     = sidir + "/num.nbc.obj.M1-%04.2f.M2-%04.2f.thbc-%3.1f.sa.one"%(thfmask1,thfmask2,thbc*1000.*100.)
            #----
            a2numobj_tmp   = fromfile(namenumobj, float32).reshape(ny,nx)
            #----
            a2numobj_tmp   = ma.masked_where(a2regionmask==0.0, a2numobj_tmp)
            #---- 
            da2numobj[key] = da2numobj[key]  + a2numobj_tmp 
  #--------------------
  drmse  = {}
  ntimes = ctrack_para.ret_totaldays(iyear,eyear,season)*4.0
  for thfmask1 in lthfmask1:
    for thfmask2 in lthfmask2:
      for thbc in lthbc:
        #---
        key        = thfmask1, thfmask2, thbc
        #---
        drmse[key] = ((a2numchart - da2numobj[key])**2.0)/ntimes
        drmse[key] = (drmse[key].mean())**0.5
  #*******************************
  #-----  save ----------
  sodir  = sidir_root + "/%04d-%04d"%(iyear,eyear)
  ctrack_func.mk_dir(sodir)
  #
  #--
  for thfmask1 in lthfmask1:
    for thfmask2 in lthfmask2:
      soname = sodir      + "/rmse.nbc.1d.%04d-%04d.%s.csv"%(iyear,eyear,season)
      srmse  = ""
      #--
      for thbc in lthbc:
        key    = thfmask1, thfmask2, thbc
        srmse  = srmse + "%3.1f,%06.4f\n"%(thbc*1000.*100., drmse[key])
      #--
      f = open(soname, "w")  ;   f.write(srmse);    f.close()
      print soname
#***********************************

