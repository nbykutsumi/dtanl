from numpy import *
import ctrack_func
import ctrack_para
import matplotlib.pyplot as plt
#-------------------------------------------
iyear = 1980
eyear = 1999
#lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
season="ALL"
lmon  =ctrack_para.ret_lmon(season) 
thdura= 36
lthwcore = [thwcore]
lthsst   = [thsst]
lthwind  = [thwind]
lthrvort = [thrvort]

ny    = 180
nx    = 360

lat_first = -89.5
lon_first = 0.5
dlat      = 1.0
dlon      = 1.0
#------------------------

a2freq_bst  = zeros([ny,nx],float32)
a2freq_obj  = zeros([ny,nx],float32)
#--- region -----
lregion    = ["PNW", "PNE","INN","INS", "PSW","ATN"]
da2regmask = {}
for region in lregion:
  lllat, lllon, urlat, urlon = ctrack_para.ret_tcregionlatlon(region) 
  da2regmask[region]  = ctrack_func.mk_region_mask(lllat, urlat, lllon, urlon, nx, ny, lat_first, lon_first, dlat, dlon) 
#----------------
dmfreq_bst  = {}
dmfreq_obj  = {}
#----------------
for year in range(iyear, eyear+1):
  for mon in lmon:
    totalnum_mon   = ctrack_para.ret_totaldays(year,year,mon)*4.0
    idir_bst   = "/media/disk2/out/ibtracs/sa.one/%04d/%02d"%(year, mon)
    idir_obj   = "/media/disk2/out/JRA25/sa.one/6hr/tc/%02dh/%04d/%02d"%(thdura, year, mon)
    iname_bst  = idir_bst + "/freq.ibtracs_all.v03r04.sa.one"
    iname_obj  = idir_obj + "/freq.tc.%02dh.w%.1f.sst%02d.wind%d.vor%.1e.sa.one"%(thdura, thwcore, thsst-273.15, thwind, thrvort)
    a2freq_bst_mon  = fromfile(iname_bst, float32).reshape(ny,nx) 
    a2freq_obj_mon  = fromfile(iname_obj, float32).reshape(ny,nx)
    #
    a2freq_bst      = a2freq_bst + a2freq_bst_mon * totalnum_mon
    a2freq_obj      = a2freq_obj + a2freq_obj_mon * totalnum_mon
 
    #-------
    for region in lregion:
      a2freq_bst_temp = ma.masked_where(da2regmask[region] !=1.0, a2freq_bst_mon)
      a2freq_obj_temp = ma.masked_where(da2regmask[region] !=1.0, a2freq_obj_mon)
      dmfreq_bst[region, year,mon] = a2freq_bst_temp.mean()
      dmfreq_obj[region, year,mon] = a2freq_obj_temp.mean()
#---------
totalnum  = ctrack_para.ret_totaldays(iyear,eyear,season)*4.0
a2freq_bst = a2freq_bst / totalnum
a2freq_obj = a2freq_obj / totalnum

#---- montly graph -----------
for region in lregion:
  lv_bst = []
  lv_obj = []
  ltime  = []
  for year in range(iyear, eyear+1):
    for mon in lmon:
      ltime.append("%04d.%02d"%(year,mon))
      lv_bst.append(dmfreq_bst[region, year, mon])
      lv_obj.append(dmfreq_obj[region, year, mon])
  #
  plt.clf()
  figplot  = plt.figure()
  axplot   = figplot.add_axes([0.1,0.2,0.8,0.6])
  axplot.plot( array(lv_bst) )  
  axplot.plot( array(lv_obj) )
  #- xticks --
  plt.xticks( range(len(ltime))[::3],ltime[::3], rotation=90)
  leg      = axplot.legend( ["bst","obj"])

  #- axis limit ---
  axplot.set_ylim((0, 0.0006))

  #-- title --
  stitle   = "%s wcore:%3.1f"%(region, thwcore)
  axplot.set_title(stitle)
  #-- save ---
  odir_root = "/media/disk2/out/JRA25/sa.one/6hr/tc"
  odir      = odir_root + "/%02dh/%04d-%04d/%s/pict"%(thdura, iyear, eyear, season)
  ctrack_func.mk_dir(odir)
  soname    = odir + "/plot.freq.%02dh.w%3.1f.sst%02d.wind%d.vor%.1e.%04d-%04d.%s.%s.png"%(thdura, thwcore, thsst-273.15, thwind, thrvort, iyear,eyear,season, region)
  figplot.savefig(soname)
  print soname


