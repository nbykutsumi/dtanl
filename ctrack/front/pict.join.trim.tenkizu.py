import subprocess
import calendar
import os, sys


iyear   =2004
eyear   =2004
imon    =1
emon    =12
iday    =1
lhour   =[0]
odir_root   = "/home/utsumi/oekaki/pict"
prdir_root  = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/06h"
tvdir_root  = "/home/utsumi/temp"
#----------------------------------
for year in range(iyear, eyear+1):
  for mon in range(imon, emon+1):
    eday = calendar.monthrange(year,mon)[1]
    prdir   = prdir_root + "/%04d%02d"%(year, mon)
    tvdir   = tvdir_root + "/%04d.%02d"%(year, mon)
    for day in range(iday, eday+1):
      locdir  = prdir_root + "/%04d%02d/front/%02d"%(year, mon,day)
      for hour in lhour:
        siname1 = prdir + "/tenkizu.%04d.%02d.%02d.%02d.JRA.png"%(year, mon, day, hour)
        siname2 = tvdir + "/highside.highside.300.gradtv.%04d.%02d.%02d.%02d.png"%(year, mon, day, hour)
        siname3 = locdir + "/front.loc.theta_e.%04d.%02d.%02d.%02d.M1-0.50.M2-2.00.png"%(year,mon,day,hour)   
        siname4 = locdir + "/front.loc.theta_e.%04d.%02d.%02d.%02d.M1-0.60.M2-2.00.png"%(year,mon,day,hour)   
        siname5 = locdir + "/tenkizu.thetae.%04d.%02d.%02d.%02d.0850hPa.png"%(year,mon,day,hour)   
        #*********************************************
        for sname in [siname1, siname2, siname3, siname4, siname5]:
          if not os.access(sname, os.F_OK):
            print "no file:",sname
            sys.exit()
        #---------------------------------------------
        soname  = tvdir + "/front.grad.%04d.%02d.%02d.%02d.png"%(year, mon, day, hour)
        scmd    = "montage -tile 2x3 -geometry +0+0 %s %s %s %s %s %s"%(siname1, siname2, siname3, siname4, siname5, soname)
        subprocess.call(scmd, shell=True)
        print scmd 
    
