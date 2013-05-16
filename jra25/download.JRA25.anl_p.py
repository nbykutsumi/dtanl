import subprocess 
import calendar
import ctrack_func
#----------------------------------
dattype   = "anl_p"
hostname  = "ds.data.jma.go.jp"
sidir_root = "/data01/Grib/anl_p"
sodir_root = "/media/disk2/temp"
iyear     = 2001
eyear     = 2001
lmon      = [1]
iday      = 1
lhour     = [0,6,12,18]
myid      = "jra02177"
mypass    = "suimongaku"
#----------------------------------
for year in range(iyear, eyear+1):
  for mon in lmon:
    #--- directory -----------
    sidir = sidir_root + "/%04d%02d"%(year, mon)
    sodir = sodir_root + "/%s/%04d%02d"%(dattype, year, mon) 
    ctrack_func.mk_dir(sodir)
    #--- ctl file ------------
    ctlname = sidir + "/anl_p.ctl"
    idxname = sidir + "/anl_p.idx"

    scmd  = "wget ftp://%s:%s@%s%s -P %s"%(myid, mypass, hostname, ctlname, sodir)
    subprocess.call(scmd, shell=True)

    scmd  = "wget ftp://%s:%s@%s%s -P %s"%(myid, mypass, hostname, idxname, sodir)
    subprocess.call(scmd, shell=True)

    -------------------------
    eday = calendar.monthrange(year, mon)[1]
    for day in range(iday, eday+1):
      for hour in lhour:
        #siname  = sidir + "/anl_p.2001010112"
        siname  = sidir + "/anl_p.%04d%02d%02d%02d"%(year,mon,day,hour)
        print year, mon, day, hour
        scmd  = "wget ftp://%s:%s@%s%s -P %s"%(myid, mypass, hostname, siname,sodir)
        print scmd
        subprocess.call(scmd, shell=True)
