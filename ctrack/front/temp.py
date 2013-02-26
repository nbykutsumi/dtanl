from numpy import *
from ctrack_fsub import *
#------------------------------
idir_root = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/front/agg"
for year in [2000,2001,2002,2003,2004]:
  for mon in [1,2,3,4,5,6,7,8,9,10,11,12]:
    idir  = idir_root + "/%04d/%02d"%(year,mon)
    aname = idir + "/pr.front.rad0500.M1_0.5_M2_2.0.saone"
    bname = idir + "/pr.bcf.rad0500.M1_0.5_M2_2.0.thbc_0.70.saone"
    cname = idir + "/pr.nobc.rad0500.M1_0.5_M2_2.0.thbc_0.70.saone"
    #
    a     = fromfile(aname, float32).reshape(180,360)
    b     = fromfile(bname, float32).reshape(180,360)
    c     = fromfile(cname, float32).reshape(180,360)
    #
    print ma.masked_equal(a, -9999.0).sum(), ma.masked_equal(b,-9999.0).sum(), ma.masked_equal(c,-9999.0).sum()
