from numpy import *

iyear = 2000
eyear = 2004
lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
#lllat = 30.0
#lllon = 140.0
#urlat = 45.0
#urlon = 160.0
lllat = 25.0
lllon = 0.0
urlat = 60.0
urlon = 359.0


miss  = -9999.0
ny    = 180
nx    = 360
thdist     = 500 # (km)
llthfmask  = [(0.3,2.0),(0.5,2.0)]
#
xdom_saone_first = int((lllon - 0.5 + 0.5)/1.0)
xdom_saone_last  = int((urlon - 0.5 + 0.5)/1.0)
ydom_saone_first = int((lllat -(-89.5) + 0.5)/1.0)
ydom_saone_last  = int((urlat -(-89.5) + 0.5)/1.0)
#
dir_obj_root  = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/front/agg"
#-- objective fronts -----------------
dpr_obj   = {}
#-- init --
for tkey in llthfmask:
  dpr_obj[tkey] = []
#----------
for year in range(iyear, eyear+1):
  for mon in lmon:
    for tkey in llthfmask:
      thfmask1,thfmask2 = tkey
      #-- name for  ----
      dir_obj    = dir_obj_root + "/%04d/%02d"%(year, mon)
      siname_obj = dir_obj      + "/rad%04d.M1_%s_M2_%s.saone"%(thdist, thfmask1, thfmask2)
      a2in_obj   = fromfile(siname_obj, float32).reshape(ny,nx)
      #-- dmain ---
      a2in_obj_dom = ma.masked_equal(a2in_obj[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1], miss)
      dpr_obj[thfmask1,thfmask2].append(mean(a2in_obj_dom))


#-- objective fronts -----------------
dir_jma_root  = "/media/disk2/out/chart/ASAS/front/agg"
lpr_jma       = []
for year in range(iyear, eyear+1):
  for mon in lmon:
    #-- name for  ----
    dir_jma    = dir_jma_root + "/%04d/%02d"%(year, mon)
    siname_jma = dir_jma      + "/rad%04d.saone"%(thdist)
    a2in_jma   = fromfile(siname_jma, float32).reshape(ny,nx)
    #-- dmain ---
    a2in_jma_dom = ma.masked_equal(a2in_jma[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1], miss)
    lpr_jma.append(mean(a2in_jma_dom))
    #--

#-- time-label -------
ltime = []
for year in range(iyear, eyear+1):
  for mon in lmon:
    ltime.append("%04d.%02d"%(year,mon))

#-- plot ------------- 
coef     = 60*60*24.0
figplot  = plt.figure()
axplot   = figplot.add_axes([0.1,0.2,0.8,0.7])
#
axplot.plot(array(lpr_jma)*coef)
#
for tkey in llthfmask:
  axplot.plot(array(dpr_obj[tkey])*coef)
#- xtics --
xticks(range(len(ltime))[::3],ltime[::3], rotation=90)
leg = axplot.legend(("JMA","M1:0.3 M2:2.0","M1:0.5 M2:2.0"))






