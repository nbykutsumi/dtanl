from numpy import *
import datetime
import sys
import subprocess
#**********************************************
def gsmap2global_one(a2org_one, miss):
  a2glob = ones([180,360], float32)*miss
  a2glob[30:149+1,:] = a2org_one
  return a2glob
#**********************************************
def timeave_gsmap_backward_org(year,mon,day,hour, hlen):
  lhlen = [1,2,3,6,12,24]
  if not hlen in lhlen:
    print "'hlen' should be" ,lhlen
    sys.exit()
  #-------------
  lh_inc     = range(hlen)
  now       = datetime.datetime(year,mon,day,hour)

  a2ave     = zeros([1200*3600],float32)  
  for h_inc in lh_inc:
    dhour   = datetime.timedelta(hours = -h_inc)
    target  = now + dhour
    year_t  = target.year
    mon_t   = target.month
    day_t   = target.day
    hour_t  = target.hour
    idir_root = "/home/utsumi/mnt/iis.data2/GSMaP/standard/v5/hourly"
    idir      = idir_root + "/%04d/%02d/%02d"%(year_t,mon_t,day_t)
    ##--- for compressed files ------
    #iname     = idir + "/gsmap_mvk.%04d%02d%02d.%02d00.v5.222.1.dat.gz"%(year_t,mon_t,day_t,hour_t)
    #dat_org   = subprocess.Popen(["gzip", "-dc", iname, " >", "/dev/stdout"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]

    #a2in      = fromstring(dat_org, float32)
    #---- for decompressed files ---
    iname     = idir + "/gsmap_mvk.%04d%02d%02d.%02d00.v5.222.1.dat"%(year_t,mon_t,day_t,hour_t)
    a2in      = fromfile(iname,float32)



    a2ave     = a2ave + ma.masked_less(a2in, 0.0)

  #---
  #a2ave       = (a2ave /(len(lhlen)* 60.0*60.0)).filled(-9999.0)  # original data is in [mm/hour]
  a2ave       = (a2ave /(hlen* 60.0*60.0)).filled(-9999.0)  # original data is in [mm/hour]
  a2ave       = flipud(a2ave.reshape(1200,3600))
  return a2ave

#**********************************************
def timeave_gsmap_backward_saone(year,mon,day,hour, hlen):
  lhlen = [1,2,3,6,12,24]
  if not hlen in lhlen:
    print "'hlen' should be" ,lhlen
    sys.exit()
  #-------------
  lh_inc     = range(hlen)
  now       = datetime.datetime(year,mon,day,hour)

  a2ave     = zeros([120,360],float32)  
  for h_inc in lh_inc:
    dhour   = datetime.timedelta(hours = -h_inc)
    target  = now + dhour
    year_t  = target.year
    mon_t   = target.month
    day_t   = target.day
    hour_t  = target.hour
    idir_root = "/media/disk2/data/GSMaP/sa.one/1hr/ptot"
    idir      = idir_root + "/%04d%02d"%(year_t,mon_t)
    iname     = idir + "/gsmap_mvk.1rh.%04d%02d%02d.%02d00.v5.222.1.sa.one"%(year_t,mon_t,day_t,hour_t)
    a2in      = fromfile(iname, float32).reshape(120,360)
    a2ave     = a2ave + ma.masked_equal(a2in, -9999.0)
  #---
  a2ave       = a2ave / hlen
  a2ave       = a2ave.filled(-9999.0)
  return a2ave






