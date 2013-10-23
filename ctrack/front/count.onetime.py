from dtanl_fsub import *
from chart_fsub import *
from numpy import *
import calendar
import ctrack_para, ctrack_func
#-----------------------------------------
#singletime = True
singletime = False
iyear = 2000
eyear = 2010
#lyear = range(iyear,eyear+1)
lyear = [2010]
#lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
lmon   = [1,7]
iday    = 1
lhour   = [0,6,12,18]
#lhour   = [0]
lftype  = [1]
ny,nx   = 180,360
miss    = -9999.0
idir_root = "/media/disk2/out/chart/ASAS/front"
#------------------------------------------

dnum = {}
for year in lyear:
  for mon in lmon:
    print year,mon
    #--- init ----------
    for ftype in lftype:
      dnum[ftype,year,mon] = 0
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
        #-------
        for ftype in lftype:
          a2in_seg = ma.masked_not_equal(a2in, ftype).filled(miss)
          #a2in_seg = dtanl_fsub.fill_front_gap(a2in_seg.T, miss).T
          a2in_seg = chart_fsub.fill_front_gap_for_countfronts(a2in_seg.T, miss,ftype).T

          num_tmp        = dtanl_fsub.count_fronts(a2in_seg.T, miss)
          print ",".join(map(str,[ftype,year,mon,day,hour,num_tmp]))
          dnum[ftype,year,mon]    = dnum[ftype,year,mon] + num_tmp
##****************************
## write to csv
##----------------------------
#for ftype in lftype:
#  sout = "," + ",".join( map(str, lmon)) + "\n"
#  for year in lyear:
#    line = [ dnum[ftype,year,mon] for mon in lmon]
#    sout = sout + "%d,"%(year) + ",".join( map(str, line) ) + "\n"
#  sout = sout.strip()
#  #------
#  sodir  = "/media/disk2/out/chart/ASAS/count"
#  ctrack_func.mk_dir(sodir)
#  soname = sodir + "/count.front.chart.%04d-%04d.f%d.csv"%(iyear,eyear,ftype)
#  f=open(soname,"w"); f.write(sout); f.close()
#  print soname
