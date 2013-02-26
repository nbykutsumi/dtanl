import subprocess
import calendar
import os,sys
idir_root  = "/home/utsumi/temp"
objdir_root= "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/06h"
lseason = ["ALL","DJF","MAM","JJA","SON"]
thdist  = 500
thbc    = 0.7 /1000/100.0
#thbc    = 0.5 /1000/100.0
odir  = "/home/utsumi/oekaki/pict"
llthfmask = [(0.4, 2.0), (0.5, 2.0)]
#llthfmask = [(0.5,2.0)]
#----------------------------------
for lthfmask in llthfmask:
  thfmask1, thfmask2 = lthfmask
  for season in lseason:
    siname1  = "/media/disk2/out/chart/ASAS/front/agg/2000-2010/%s/pict/frac.rad0500.all.png"%(season)
    siname2  = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/front/agg/2000-2004/%s/pict/frac.front.s%s.rad%04d.M1_%03.1f_M2_%03.1f.png"%(season,season,thdist, thfmask1, thfmask2)
    siname3  = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/front/agg/2000-2004/%s/pict/frac.bcf.s%s.rad%04d.M1_%03.1f_M2_%03.1f.thbc_%04.2f.png"%(season,season,thdist, thfmask1, thfmask2, thbc*1000*100)
    siname4  = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/front/agg/2000-2004/%s/pict/frac.nobc.s%s.rad%04d.M1_%03.1f_M2_%03.1f.thbc_%04.2f.png"%(season,season,thdist, thfmask1, thfmask2, thbc*1000*100)
    soname  = odir + "/comp.frac.M1_%04.2f.M2_%04.2f.thbc_%04.2f.%s.png"%(thfmask1, thfmask2, thbc*1000*100, season)
    #*********************************************
    #*********************************************
    for sname in [siname1, siname2, siname3, siname4]:
      if not os.access(sname, os.F_OK):
        print "no file:",sname
        sys.exit()
    #---------------------------------------------
    scmd    = "montage -tile 2x2 -geometry +0+0 %s %s %s %s %s"%(siname1, siname2, siname3, siname4, soname)
    subprocess.call(scmd, shell=True)
    print scmd 
    #--- cbar ---------
    cbarname_in  = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/front/agg/2000-2004/%s/pict/frac.front.cbar.png"%(season)
    cbarname_out = "/home/utsumi/oekaki/pict/frac.front.cbar.png"
    scmd2   = "cp %s %s"%(cbarname_in, cbarname_out)
    subprocess.call(scmd2, shell=True)    
