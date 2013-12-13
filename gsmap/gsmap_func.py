from numpy import *
import datetime
import sys
import subprocess
#**********************************************
def global2gsmap_one(a2glob_one):
  a2gsmap_one  = a2glob_one[30:149+1,:]
  return a2gsmap_one

#**********************************************
def gsmap2global_one(a2org_one, miss):
  a2glob = ones([180,360], float32)*miss
  a2glob[30:149+1,:] = a2org_one
  return a2glob

#**********************************************
def gsmap2global_dec(a2org_dec, miss):
  a2glob = ones([1800,3600], float32)*miss
  a2glob[300:1499+1,:] = a2org_dec
  return a2glob

#**********************************************
def gsmap2global(a2org, miss):
  if shape(a2org) == (120,360):
    a2glob = gsmap2global_one(a2org, miss)
  elif shape(a2org) == (1200,3600):
    a2glob = gsmap2global_dec(a2org, miss)
  #
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
  a2ave       = (a2ave /(hlen* 60.0*60.0)).filled(-9999.0)  # original data is in [mm/hour]
  a2ave       = flipud(a2ave.reshape(1200,3600))
  return a2ave

#**********************************************
def timeave_gsmap_backward_nmiss_saone(year,mon,day,hour, hlen, relaxflag=False):
  lhlen = [1,2,3,6,12,24]
  if not hlen in lhlen:
    print "'hlen' should be" ,lhlen
    sys.exit()
  #-------------
  lh_inc     = range(hlen)
  now       = datetime.datetime(year,mon,day,hour)

  a2ave     = zeros([120,360],float32)  
  a2nmiss   = zeros([120,360],float32)
  a2zero    = zeros([120,360],float32)
  #---------------
  if   relaxflag == False:
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
      a2ave     = a2ave   + ma.masked_equal(a2in, -9999.0)
      a2nmiss   = a2nmiss + ma.masked_where(a2in==-9999.0, a2zero).filled(1.0)
  elif relaxflag == True:
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
      a2ave     = a2ave + ma.masked_equal(a2in, -9999.0).filled(0.0)
      a2nmiss   = a2nmiss + ma.masked_where(a2in==-9999.0, a2zero).filled(1.0)
  #---------------
  a2ave       = a2ave / hlen
  if relaxflag == False:
    a2ave       = a2ave.filled(-9999.0)
  elif relaxflag == True:
    a2ave       = ma.masked_where(a2nmiss==float(hlen), a2ave).filled(-9999.)
  #---------------
  return a2ave, a2nmiss

#**********************************************
def timeave_gsmap_backward_saone(year,mon,day,hour, hlen, relaxflag=False):
  lhlen = [1,2,3,6,12,24]
  if not hlen in lhlen:
    print "'hlen' should be" ,lhlen
    sys.exit()
  #-------------
  lh_inc     = range(hlen)
  now       = datetime.datetime(year,mon,day,hour)

  a2ave     = zeros([120,360],float32)  
  #---------------
  if   relaxflag == False:
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
  elif relaxflag == True:
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
      a2ave     = a2ave + ma.masked_equal(a2in, -9999.0).filled(0.0)
  #---------------
  a2ave       = a2ave / hlen
  if relaxflag == False:
    a2ave       = a2ave.filled(-9999.0)
  #---------------
  return a2ave


#*************************
def mk_metadata_one(odir, dattype):
  sunit  = "(mm s-1)"

  if dattype in ["sa.one"]:
    ny_one   = 120
    nx_one   = 360
    newShape = array([ny_one, nx_one], int)
    lat_one_first  = -59.5
    lat_one_last   = 59.5
    lon_one_first  = 0.5
    lon_one_last   = 359.5
    dlat_one       = 1.0
    dlon_one       = 1.0
    a1lat_one  = arange(lat_one_first, lat_one_last + dlat_one*0.5, dlat_one)
    a1lon_one  = arange(lon_one_first, lon_one_last + dlon_one*0.5, dlon_one)

  #---- for latlon ------------
  def mk_latlontxt(odir):
    sout     = "\n".join(map( str, a1lat_one))
    f        = open( odir + "/lat.txt", "w")
    f.write(sout)
    f.close()
    #
    sout     = "\n".join(map( str, a1lon_one))
    f        = open( odir + "/lon.txt", "w")
    f.write(sout)
    f.close()
  #---- for dimtxt ------------
  def mk_dimtxt(odir):
    sout   = "lev %d\nlat %d\nlon %d"%(1, ny_one, nx_one)
    f      = open( odir + "/dims.txt", "w")
    f.write(sout)
    f.close()
  #--- for unit file -----------
  def mk_unittxt(odir):
    sout   = "unit: %s"%(sunit)
    f      = open( odir + "/unit.txt","w")
    f.write(sout)
    f.close()
  #-- readme -------------------
  def mk_readme(odir):
    sout   = "mean precipitation rate (%s)\n"%(sunit)
    sout   = sout + "daily mean"
    f      = open( odir + "/readme.txt","w")
    f.write(sout)
    f.close()
  #-----------------------------
  mk_latlontxt(odir)
  mk_dimtxt(odir)
  mk_unittxt(odir)
  mk_readme(odir)

