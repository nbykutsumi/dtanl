from numpy import *
import ctrack_func
import calendar
#--------------------------------
iyear  = 2003
eyear  = 2005
lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon   = [6,7]
iday   = 1
lhour  = [0,6,12,18]
#lvar   = ["UGRD", "VGRD"]
#lvar   = ["SPFH","TMP"]
lvar   = ["VVEL"]
lplev  = array([850,500])*100.
#lplev  = array([250])*100.
#lplev  = array([925,850,700,500,300])*100.
#sresol = "anl_p"
sresol = "anl_chipsi"
ny,nx  = 180,360
idir_root = "/media/disk2/data/JRA25/sa.one.%s/6hr"%(sresol)
odir_root = "/media/disk2/data/JRA25/sa.one.%s/day"%(sresol)
#---------------------------------
for year in range(iyear,eyear+1):
  for mon in lmon:
    eday  = calendar.monthrange(year,mon)[1]
    for var in lvar:
      #--- readme.txt ------------
      ctrack_func.mk_dir("/%s/%s"%(odir_root,var))
      f   = open(odir_root + "/%s/readme.txt"%(var), "w")
      stxt= "data in this directory was created from 6hourly data using mk.daily.py"
      f.write(stxt);  f.close()
      #---------------------------
      for plev in lplev:
        #---------------------
        a2day     = zeros([ny,nx],float32)
        for day in range(iday,eday+1):
          print year,mon,day,plev
          for hour in lhour:
            idir  = idir_root + "/%s/%04d%02d"%(var,year,mon)
            iname = idir + "/%s.%s.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,var,plev*0.01,year,mon,day,hour)
            a2in  = fromfile(iname, float32).reshape(ny,nx)
            a2day = a2day + a2in
          #-------
          a2day = a2day / len(lhour)
          #--- save ---
          odir  = odir_root + "/%s/%04d%02d"%(var,year,mon)
          ctrack_func.mk_dir(odir)
          oname = odir      + "/%s.%s.%04dhPa.%04d%02d%02d.sa.one"%(sresol,var,plev*0.01,year,mon,day)
          a2day.tofile(oname)
          print oname 
