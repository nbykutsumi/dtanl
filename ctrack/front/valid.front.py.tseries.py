import ctrack_func
from numpy import *
#---------------------------------------
iyear   = 2000
eyear   = 2000
lmon    = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon    = [1,2]
#----
sresol  = "anl_p"
lthfmask1  = [0.1,0.3,0.5,0.7,0.9,1.1]
lthfmask2  = [1.0,2.0,3.0,4.0,5.0,6.0]
nx,ny      = 360,180
lat_first  = -89.5
lon_first  = 0.5
dlat,dlon  = 1.0, 1.0

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
#-- init ----
dhit       = {}
dmiss      = {}
dos        = {}
dnumchart  = {}
drmse     = {}
da2numchart = {}
da2numobj   = {}
for mon in lmon:
  #---
  dnumchart[mon]   = 0.0
  da2numchart[mon] = zeros([ny,nx],float32)
  #---
  for thfmask1 in lthfmask1:
    for thfmask2 in lthfmask2:
      key  = thfmask1, thfmask2
      dhit[key, mon]      = 0.0
      dmiss[key, mon]     = 0.0
      dos[key, mon]       = 0.0
      drmse[key,mon]      = 0.0
      da2numobj[key,mon]  = zeros([ny,nx],float32)
#*************************
for mon in lmon:
  print mon
  for year in range(iyear,eyear+1):
    sidir            = sidir_root  + "/%04d%02d"%(year,mon)
    #--
    namenumchart     = sidir + "/num.chart.sa.one"
    a2numchart_tmp   = fromfile(namenumchart, float32).reshape(ny,nx)
    a2numchart_tmp   = ma.masked_where(a2regionmask==0.0,  a2numchart_tmp)
    da2numchart[mon] = da2numchart[mon] + a2numchart_tmp
    dnumchart[mon]   = dnumchart[mon]   + a2numchart_tmp.sum()  

    #--
    for thfmask1 in lthfmask1:
      for thfmask2 in lthfmask2:
        key  = (thfmask1, thfmask2)
        #----
        namehit    = sidir + "/num.hit.M1-%04.2f.M2-%04.2f.sa.one"%(thfmask1,thfmask2)
        namemiss   = sidir + "/num.miss.M1-%04.2f.M2-%04.2f.sa.one"%(thfmask1,thfmask2)
        nameos     = sidir + "/num.os.M1-%04.2f.M2-%04.2f.sa.one"%(thfmask1,thfmask2)
        namenumobj = sidir + "/num.obj.M1-%04.2f.M2-%04.2f.sa.one"%(thfmask1,thfmask2)
        #----
        a2hit      = fromfile(namehit,    float32).reshape(ny,nx)
        a2miss     = fromfile(namemiss,   float32).reshape(ny,nx)
        a2os       = fromfile(nameos,     float32).reshape(ny,nx)
        a2numobj   = fromfile(namenumobj, float32).reshape(ny,nx)
        #----
        a2hit      = ma.masked_where(a2regionmask==0.0, a2hit)
        a2miss     = ma.masked_where(a2regionmask==0.0, a2miss)
        a2os       = ma.masked_where(a2regionmask==0.0, a2os)
        a2numobj   = ma.masked_where(a2regionmask==0.0, a2numobj)
        #---- 
        dhit[key,mon]   = dhit[key,mon]  + a2hit.sum()
        dmiss[key,mon]  = dmiss[key,mon] + a2miss.sum()
        dos[key,mon]    = dos[key,mon]   + a2os.sum()
        da2numobj[key,mon] = da2numobj[key,mon]  + a2numobj
  #--------------------
  for thfmask1 in lthfmask1:
    for thfmask2 in lthfmask2:
      #---
      key             = thfmask1, thfmask2
      #---
      dhit[key,mon]   = dhit[key,mon]  / dnumchart[mon]
      dmiss[key,mon]  = dmiss[key,mon] / dnumchart[mon]
      dos[key,mon]    = dos[key,mon]   / dnumchart[mon]
      a2rmse          = ((da2numobj[key,mon] - da2numchart[mon])/(eyear-iyear+1))**2.0
      drmse[key,mon]  = (a2rmse.mean())**0.5
#***********************************
#--- time series -----------
shit    = ""
smiss   = ""
sos     = ""
srmse  = ""
#-- label ----
for mon in lmon:
  shit   = shit   + ",%d"%(mon) 
  smiss  = smiss  + ",%d"%(mon) 
  sos    = sos    + ",%d"%(mon) 
  srmse = srmse + ",%d"%(mon) 
shit    = shit  + "\n"
smiss   = smiss + "\n"
sos     = sos   + "\n"
srmse  = srmse+ "\n"
#-- data -----
for thfmask1 in lthfmask1:
  for thfmask2 in lthfmask2:
    shit   = shit  + "M1-%04.2f.M2-%04.2f"%(thfmask1,thfmask2)
    smiss  = smiss + "M1-%04.2f.M2-%04.2f"%(thfmask1,thfmask2)
    sos    = sos   + "M1-%04.2f.M2-%04.2f"%(thfmask1,thfmask2)
    srmse = srmse+ "M1-%04.2f.M2-%04.2f"%(thfmask1,thfmask2)
    for mon in lmon:
      #-----
      key    = thfmask1, thfmask2
      #-----
      shit   = shit  + ",%6.4f"%(dhit[key,mon]) 
      smiss  = smiss + ",%6.4f"%(dmiss[key,mon]) 
      sos    = sos   + ",%6.4f"%(dos[key,mon]) 
      srmse = srmse+ ",%6.4f"%(drmse[key,mon]) 
      #-----
    shit   = shit   + "\n"
    smiss  = smiss  + "\n"
    sos    = sos    + "\n"
    srmse = srmse + "\n"
#-- save -----
sodir    = sidir_root + "/%04d-%04d"%(iyear,eyear)
ctrack_func.mk_dir(sodir)
#-
csvhit   = sodir  + "/hit.%04d-%04d.csv"%(iyear,eyear)
csvmiss  = sodir  + "/miss.%04d-%04d.csv"%(iyear,eyear)
csvos    = sodir  + "/os.%04d-%04d.csv"%(iyear,eyear)
csvrmse = sodir  + "/rmse.%04d-%04d.csv"%(iyear,eyear)
#
f = open(csvhit,"w")  ; f.write(shit)    ;  f.close()
f = open(csvmiss,"w") ; f.write(smiss)   ;  f.close()
f = open(csvos,"w")   ; f.write(sos)     ;  f.close()
f = open(csvrmse,"w"); f.write(srmse)  ;  f.close()
print csvhit





