import sys
import ctrack_func
from numpy import *
iyear  = 1980
eyear  = 1980
lyear  = range(iyear,eyear+1)
#lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
lmon   = [1]
model  = "anl_p"

#--- init ----
dinisst   = {}
#-------------
for year, mon in [[year,mon] for year in lyear for mon in lmon]:
  #----------
  dinisst_pre          = dinisst
  dinisst              = {}
  dinisst[-9999,-9999] = -9999.0
  #----------
  sidir_root  = "/media/disk2/out/JRA25/sa.one.%s/6hr/clist"%(model)
  sidir       = sidir_root + "/%04d/%02d"%(year,mon)

  #-- input name ----------
  idatename   = sidir + "/idate.%04d.%02d.bn"%(year,mon)
  nowposname  = sidir + "/nowpos.%04d.%02d.bn"%(year,mon)
  iposname    = sidir + "/ipos.%04d.%02d.bn" %(year,mon)
  timename    = sidir + "/time.%04d.%02d.bn" %(year,mon)
  sstname     = sidir + "/sst.%04d.%02d.bn"  %(year,mon)
  initsstname = sidir + "/initsst.%04d.%02d.bn"  %(year,mon)
  duraname    = sidir + "/dura.%04d.%02d.bn"  %(year,mon)
  #-- load ----------------
  a1idate     = fromfile(idatename,   int32)
  a1nowpos    = fromfile(nowposname,    int32)
  a1ipos      = fromfile(iposname,    int32)
  a1time      = fromfile(timename,   int32)
  a1sst       = fromfile(sstname,    float32)
  a1initsst   = fromfile(initsstname, float32)
  a1dura      = fromfile(duraname,   int32)
  #------------------------
  n  = len(a1idate)
  ldat    = []
  for i in range(n):
    idate = a1idate[i]
    nowpos= a1nowpos [i]
    ipos  = a1ipos [i]
    time  = a1time [i]
    sst   = a1sst  [i]
    initsst= a1initsst[i]
    dura  = a1dura[i]
    #print idate, ipos, dura, initsst
    if (idate ==1980010906 )&(ipos==24489):
      print "AAAAA", idate, ipos, time, sst, initsst, dura
      #sys.exit()

