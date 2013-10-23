from dtanl_fsub import *
from chart_fsub import *
from numpy import *
import datetime
import calendar
import ctrack_para, ctrack_func, chart_para
#-----------------------------------------
#singletime = True
singletime = False
iyear = 2000
eyear = 2010
#eyear = 2000
lyear = range(iyear,eyear+1)
lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon  = [1]
iday    = 1
lhour   = [0,6,12,18]
#lhour   = [0]
lftype  = [1,2,3,4]
ny,nx   = 180,360
miss    = -9999.0
idir_root = "/media/disk2/out/chart/ASAS/front"

#-----------------
lat_first = -89.5
lon_first = 0.5
dlat, dlon = 1.0, 1.0

#region= "JPN"
region = "ASAS"
lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region)
a2regionmask = ctrack_func.mk_region_mask(lllat,urlat,lllon,urlon, nx,ny, lat_first, lon_first, dlat, dlon)

#------------------------------------------

#--- init ----------
dnum = {}
for year in lyear:
  for mon in lmon:
    for ftype in lftype:
      dnum[ftype,year,mon] = 0
#-------------------
for year in lyear:
  for mon in lmon:
    print year,mon
    #-------------------
    if singletime ==True:  
      eday = 1
    elif singletime == False:
      eday = calendar.monthrange(year,mon)[1]
    #--------------------
    for day in range(iday,eday+1):
      for hour in lhour:
        idir  = idir_root + "/%04d%02d"%(year,mon) 
        iname = idir + "/front.ASAS.%04d.%02d.%02d.%02d.sa.one"%(year,mon,day,hour)
        a2in  = fromfile(iname, float32).reshape(ny,nx)
        if region != "ASAS":
          a2in  = ma.masked_where(a2regionmask==0.0, a2in).filled(miss)
        #-------
        for ftype in lftype:
          vfill = float(ftype)
          a2in_seg = ma.masked_not_equal(a2in, ftype).filled(miss)
          a2in_seg = chart_fsub.fill_front_gap_for_countfronts(a2in_seg.T, miss, vfill).T
          #a2in_seg = dtanl_fsub.fill_front_gap(a2in_seg.T, miss).T

          num_tmp        = dtanl_fsub.count_fronts(a2in_seg.T, miss)
          dnum[ftype,year,mon]    = dnum[ftype,year,mon] + num_tmp
#****************************
# write to table csv
#----------------------------
for ftype in lftype:
  sout = "," + ",".join( map(str, lmon)) + "\n"
  for year in lyear:
    line = [ dnum[ftype,year,mon] for mon in lmon]
    sout = sout + "%d,"%(year) + ",".join( map(str, line) ) + "\n"
  sout = sout.strip()
  #------
  sodir  = "/media/disk2/out/chart/ASAS/count"
  ctrack_func.mk_dir(sodir)
  soname = sodir + "/count.front.chart.%04d-%04d.%s.f%d.csv"%(iyear,eyear,region,ftype)
  f=open(soname,"w"); f.write(sout); f.close()
  print soname

#*****************************
# time series
#-----------------------------
sout   = ",warm,cold,occ,stat\n"
for year in lyear:
  for mon in lmon:
    sdate  = "%04d-%02d"%(year,mon)
    count1 = dnum[1,year,mon]
    count2 = dnum[2,year,mon]
    count3 = dnum[3,year,mon]
    count4 = dnum[4,year,mon]
    sout = sout + "%s,%s,%s,%s,%s\n"%(sdate,count1,count2,count3,count4)

soname = sodir + "/tseries.count.front.chart.%04d-%04d.%s.csv"%(iyear,eyear,region)
f=open(soname,"w"); f.write(sout); f.close()

#*****************************
# time series 3months
#-----------------------------

lcount1 = []
lcount2 = []
lcount3 = []
lcount4 = []
for year in lyear:
  for mon in lmon:
    sdate  = "%04d-%02d"%(year,mon)
    lcount1.append(dnum[1,year,mon])
    lcount2.append(dnum[2,year,mon])
    lcount3.append(dnum[3,year,mon])
    lcount4.append(dnum[4,year,mon])

sout = ",warm,cold,occ,stat\n"
for i in range(int(len(lyear)*len(lmon)/3.0)):
  #count1  = sum(lcount1[2+3*i:2+3*i+3])/3.0
  #count2  = sum(lcount2[2+3*i:2+3*i+3])/3.0
  #count3  = sum(lcount3[2+3*i:2+3*i+3])/3.0
  #count4  = sum(lcount4[2+3*i:2+3*i+3])/3.0

  count1  = sum(lcount1[2+3*i:2+3*i+3])
  count2  = sum(lcount2[2+3*i:2+3*i+3])
  count3  = sum(lcount3[2+3*i:2+3*i+3])
  count4  = sum(lcount4[2+3*i:2+3*i+3])

  if i%4 ==0: season="MAM"
  if i%4 ==1: season="JJA"
  if i%4 ==2: season="SON"
  if i%4 ==3: season="DJF"
  print season,count1,count2,count3,count4
  sout  = sout + "%s,%s,%s,%s,%s\n"%(season,count1,count2,count3,count4)

soname = sodir + "/tseries.count.front.chart.3season.%04d-%04d.%s.csv"%(iyear,eyear,region)
f=open(soname,"w"); f.write(sout); f.close()



