import subprocess
import calendar
import os, sys
idir_root  = "/home/utsumi/temp"
objdir_root= "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/06h"
lseason = ["ALL","DJF","MAM","JJA","SON"]
percent = 99
thbc    = 0.7 /1000/100.0
#thbc    = 0.5 /1000/100.0
odir  = "/home/utsumi/oekaki/pict"
llthfmask = [(0.4, 2.0), (0.5, 2.0)]
#----------------------------------
for lthfmask in llthfmask:
  thfmask1, thfmask2 = lthfmask
  for season in lseason:
    siname1  = "/media/disk2/out/chart/ASAS/front/agg/2000-2010/%s/pict/rfreq.rad0500.p%05.2f.%s.png"%(season, percent, season)
    siname2  = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/front/agg/2000-2004/%s/pict/rfreq.rad0500.p%05.2f.M1_%04.2f.M2_%04.2f.%s.front.png"%(season, percent, thfmask1, thfmask2, season)
    siname3  = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/front/agg/2000-2004/%s/pict/rfreq.rad0500.p%05.2f.M1_%04.2f.M2_%04.2f.thbc_%04.2f.%s.bcf.png"%(season, percent, thfmask1, thfmask2, thbc*1000*100, season)
    siname4  = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/front/agg/2000-2004/%s/pict/rfreq.rad0500.p%05.2f.M1_%04.2f.M2_%04.2f.thbc_%04.2f.%s.nobc.png"%(season, percent, thfmask1, thfmask2, thbc*1000*100, season)
    soname  = odir + "/comp.rfreq.%05.2f.M1_%04.2f.M2_%04.2f.thbc_%04.2f.%s.png"%(percent, thfmask1, thfmask2, thbc*1000*100, season)
    #*********************************************
    for sname in [siname1, siname2, siname3, siname4]:
      if not os.access(sname, os.F_OK):
        print "no file:",sname
        sys.exit()
    #---------------------------------------------
    scmd    = "montage -tile 2x2 -geometry +0+0 %s %s %s %s %s"%(siname1, siname2, siname3, siname4, soname)
    subprocess.call(scmd, shell=True)
    print scmd 
    #---- cbar ---------------
    cbarname_in  =  "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/front/agg/2000-2004/%s/pict/rfreq.cbar.png"%(season)
    cbarname_out =  "/home/utsumi/oekaki/pict/rfreq.cbar.png"
    scmd2        = "cp %s %s"%(cbarname_in, cbarname_out)
    subprocess.call(scmd2, shell=True)
