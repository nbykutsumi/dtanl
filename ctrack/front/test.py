from numpy import *
lyear = [2000,2001,2002,2003,2004]
lmon  = [7]
iday  = 1
eday  = 31

tdir1 = "/media/disk2/data/JRA25/sa.one/6hr/TMP/200407"
tdir2 = "/media/disk2/data/JRA25/sa.one/6hr/temp/TMP/200407"
tdir_root1 = "/media/disk2/data/JRA25/sa.one/6hr/TMP"
tdir_root2 = "/media/disk2/data/JRA25/sa.one/6hr/temp/TMP"

udir1 = "/media/disk2/data/JRA25/sa.one/6hr/UGRD/200407"
udir2 = "/media/disk2/data/JRA25/sa.one/6hr/temp/UGRD/200407"
udir_root1 = "/media/disk2/data/JRA25/sa.one/6hr/UGRD"
udir_root2 = "/media/disk2/data/JRA25/sa.one/6hr/temp/UGRD"

for year in lyear:
  for mon in lmon:
    for day in range(iday,eday+1):
      #tdir1  = tdir_root1 + "/%04d%02d"%(year,mon)
      #tdir2  = tdir_root2 + "/%04d%02d"%(year,mon)
      ##
      #tname1 =  tdir1 + "/anal_p25.TMP.0850hPa.%04d%02d%02d00.sa.one"%(year,mon,day)
      #tname2 =  tdir2 + "/anal_p25.TMP.0850hPa.%04d%02d%02d00.sa.one"%(year,mon,day)
      #a2t1   = fromfile(tname1, float32).reshape(180,360)
      #a2t2   = fromfile(tname2, float32).reshape(180,360)
      #print year,mon, day, a2t1.mean(), a2t2.mean()

      udir1  = udir_root1 + "/%04d%02d"%(year,mon)
      udir2  = udir_root2 + "/%04d%02d"%(year,mon)
      uname1 =  udir1 + "/anal_p25.UGRD.0850hPa.%04d%02d%02d00.sa.one"%(year,mon,day)
      uname2 =  udir2 + "/anal_p25.UGRD.0850hPa.%04d%02d%02d00.sa.one"%(year,mon,day)
      a2u1   = fromfile(uname1, float32).reshape(180,360)
      a2u2   = fromfile(uname2, float32).reshape(180,360)
      print year,mon, day, a2u1.mean(), a2u2.mean()


