import subprocess 
import calendar
import ctrack_func
#----------------------------------
dattype   = "anl_chipsi"
hostname  = "ds.data.jma.go.jp"
sidir_root = "/data01/Grib/anl_chipsi"
sodir_root = "/media/disk2/data/JRA25/grib.anl_chipsi/6hr"
iyear     = 2003
eyear     = 2003
lmon      = [12]
iday      = 1
lhour     = [0,6,12,18]
myid      = "jra02177"
mypass    = "suimongaku"
#----------------------------------
for year in range(iyear, eyear+1):
  for mon in lmon:
    #--- directory -----------
    sidir = sidir_root + "/%04d%02d"%(year, mon)
    sodir = sodir_root + "/%04d%02d"%(year, mon) 
    ctrack_func.mk_dir(sodir)
    #--- ctl file ------------
    ctlname = sidir + "/anl_chipsi.ctl"
    idxname = sidir + "/anl_chipsi.idx"

    scmd  = "wget ftp://%s:%s@%s%s -P %s"%(myid, mypass, hostname, ctlname, sodir)
    subprocess.call(scmd, shell=True)

    scmd  = "wget ftp://%s:%s@%s%s -P %s"%(myid, mypass, hostname, idxname, sodir)
    subprocess.call(scmd, shell=True)

    #-------------------------
    eday = calendar.monthrange(year, mon)[1]
    for day in range(iday, eday+1):
      for hour in lhour:
        siname  = sidir + "/anl_chipsi.%04d%02d%02d%02d"%(year,mon,day,hour)
        print year, mon, day, hour
        scmd  = "wget ftp://%s:%s@%s%s -P %s"%(myid, mypass, hostname, siname,sodir)
        print scmd
        subprocess.call(scmd, shell=True)
