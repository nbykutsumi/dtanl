import subprocess
import ctrack_func
#------------------------
year = 2004
lmon = [1,3,5,7,9,11]
lhour = [0,12]
for mon in lmon:
  idir = "/media/disk2/data/JMAChart/ASAS/%04d%02d"%(year,mon)
  odir = "/media/disk2/temp/chart/%04d%02d"%(year,mon)
  ctrack_func.mk_dir(odir)
  for hour in lhour:
    scmd = "cp %s/*%02d.PDF %s/"%(idir, hour, odir)
    subprocess.call(scmd, shell=True)
    print scmd 
    scmd = "cp %s/*%02d.pdf %s/"%(idir, hour, odir)
    subprocess.call(scmd, shell=True)
    print scmd 
