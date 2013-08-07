import ctrack_func
import ctrack_para
from numpy import *
#---------------------------------------
iyear   = 2001
eyear   = 2004

#----
#lseason = ["ALL","DJF","JJA"]
lseason = ["ALL"]
lbaiumon= [6,7]
sresol  = "anl_p"
ftype   = "t"
if ftype == "t":
  #lthfmask1  = [0.25,0.26,0.27,0.28,0.29,0.30,0.31]
  #lthfmask2  = [0.2,0.4,0.6,0.8,1.0,1.2]
  lthfmask1  = [0.18,0.22,0.25,0.26,0.27,0.28,0.29,0.30,0.31]
  lthfmask2  = [0.2,0.4,0.6,0.8,1.0,1.2]
elif ftype == "q":
  lthfmask1  = array([2.0,2.2,2.4,2.6,2.8,3.0,3.2]) #*1.0e-4
  lthfmask2  = array([2.2,2.4,2.6,2.8,3.0,3.2])     #*1.0e-3

thgrids    = 7
#----
nx,ny      = 360,180
lat_first  = -89.5
lon_first  = 0.5
dlat,dlon  = 1.0, 1.0
lbaiumon   = [5,6,7]

##** baiu region **********
lllat    = 25.
lllon    = 125
urlat    = 45.
urlon    = 145.
#--
a2baiu_region  = ctrack_func.mk_region_mask(lllat,urlat,lllon,urlon,nx,ny,lat_first,lon_first,dlat,dlon)


#** region mask **********
lllat    = 25.
lllon    = 125.
urlat    = 50.
urlon    = 155.
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
      key  = thfmask1, thfmask2
      da2numobj[key]   = zeros([ny,nx], float32).reshape(ny,nx)
  #--
  #--
  for year in range(iyear,eyear+1):
    for mon in lmon:
      #------
      if (ftype in ["q"])&(mon not in lbaiumon):
        continue
      #------
      print season,year,mon
      sidir             = sidir_root  + "/%04d%02d"%(year,mon)
      #*************************
      namenumchart      = sidir + "/num.chart.sa.one"
      a2numchart_tmp    = fromfile(namenumchart, float32).reshape(ny,nx)
      a2numchart_tmp    = ma.masked_where(a2regionmask==0.0,  a2numchart_tmp)
      #-- screen out baiu  ---
      if (ftype=="t")&(mon in lbaiumon):
        a2numchart_tmp  = ma.masked_where(a2baiu_region ==1.0, a2numchart_tmp)

      #-- pick up baiu  ---
      if (ftype=="q")&(mon in lbaiumon):
        a2numchart_tmp  = ma.masked_where(a2baiu_region ==0.0, a2numchart_tmp)
        
      #------------------
      a2numchart        = a2numchart  + a2numchart_tmp
      #-------------------------
      for thfmask1 in lthfmask1:
        for thfmask2 in lthfmask2:
          key  = (thfmask1, thfmask2)
          #----
          namenumobj     = sidir + "/num.%s.obj.M1-%04.2f.M2-%04.2f.gt%02d.sa.one"%(ftype, thfmask1,thfmask2,thgrids)
          #----
          a2numobj_tmp   = fromfile(namenumobj, float32).reshape(ny,nx)
          #----
          a2numobj_tmp   = ma.masked_where(a2regionmask==0.0, a2numobj_tmp)
          print namenumobj
          print "mean",mean(a2numobj_tmp)
          #---- 
          da2numobj[key] = da2numobj[key]  + a2numobj_tmp 
  #--------------------
  drmse  = {}
  ntimes = ctrack_para.ret_totaldays(iyear,eyear,season)*4.0
  for thfmask1 in lthfmask1:
    for thfmask2 in lthfmask2:
      #---
      key        = thfmask1, thfmask2
      #---
      drmse[key] = ((a2numchart - da2numobj[key])**2.0)/ntimes
      drmse[key] = (drmse[key].mean())**0.5
  #*******************************
  #-----  save ----------
  sodir  = sidir_root + "/%04d-%04d"%(iyear,eyear)
  ctrack_func.mk_dir(sodir)
  soname = sodir      + "/rmse.2d.%s.%04d-%04d.%s.gt%02d.csv"%(ftype,iyear,eyear,season,thgrids)
  #
  srmse  = ""
  #--
  for thfmask2 in lthfmask2:
    srmse = srmse + ",M2-%04.2f"%(thfmask2)
  srmse = srmse + "\n"
  #--
  for thfmask1 in lthfmask1:
    srmse  = srmse + "M1-%04.2f"%(thfmask1)
    for thfmask2 in lthfmask2:
      srmse  = srmse + ",%06.4f"%(drmse[thfmask1,thfmask2])
    srmse  = srmse + "\n"  
  #--
  f = open(soname, "w")  ;   f.write(srmse);    f.close()
  print soname

#***********************************

