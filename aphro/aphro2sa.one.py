from numpy import *
import calendar
import os, subprocess, cf.util
import ctrack_func
#--------------------------------------
iyear    = 2001
eyear    = 2007
imon     = 1
emon     = 12
miss_in  = -99.9
miss_out = -9999.0
#sunit    = "(mm day-1)"
sunit    = "(mm s-1)"
dattype  = "MA"
#---------------------
if dattype == "MA":
  ny_fin   = 280
  nx_fin   = 360
  
  ny_one   = 70
  nx_one   = 90
  newShape = array([ny_one, nx_one], int)
  lon_one_first  = 60.5
  lon_one_last   = 149.5
  lat_one_first  = -14.5
  lat_one_last   = 54.5
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
for year in range(iyear, eyear+1):
  #------------
  icount = -1
  #------------
  if dattype in ["MA"]:
    idir   = "/home/utsumi/mnt/mizu.tank/utsumi/data/APHRO/%s.org.V1101R2"%(dattype)
    iname  = idir + "/APHRO_%s_025deg_V1101R2.%04d.gz"%(dattype,year)
  
    #idir   = "/media/disk2/data/aphro/%s/org"%(dattype)
    #iname  = idir + "/APHRO_%s_025deg_V1101.%04d.gz"%(dattype,year)
    #
    odir   = "/media/disk2/data/aphro/%s.V1101R2.sa.one/%04d"%(dattype, year)
  ctrack_func.mk_dir(odir) 

  #-- latlon files ---
  mk_latlontxt(odir)
  mk_dimtxt(odir)
  mk_unittxt(odir)
  mk_readme(odir)

  #--- load data --
  dat_org   = subprocess.Popen(["gzip", "-dc", iname, " >", "/dev/stdout"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
  a3dat_org = fromstring( dat_org, float32).reshape(-1, ny_fin, nx_fin)
  #----------------
  for mon in range(imon, emon+1):
    print year, mon
    #----------
    eday = calendar.monthrange(year, mon)[1]
    #----------
    for day in range(1, eday+1):
      icount = icount + 1
      #--------
      #a2dat_org    = a3dat_org[icount*2]
      a2dat_org    = a3dat_org[icount*3]  # for V1101R2
      #-- upscale ------
      a2dat_one  = cf.util.upscale(a2dat_org, newShape, mode="m", missing=miss_in)
      #-----------------
      if dattype == "MA":
        #soname     = odir + "/APHRO_%s_025deg_V1101.%04d.%02d.%02d.sa.one"%(dattype, year,mon,day)
        soname     = odir + "/APHRO_%s_025deg_V1101R2.%04d.%02d.%02d.sa.one"%(dattype, year,mon,day)

      a2dat_one  = ma.masked_equal(a2dat_one, miss_in) / (60.*60.*24.)
      a2dat_one  = a2dat_one.filled(miss_out)
      a2dat_one  = array(a2dat_one, float32)
      a2dat_one.tofile(soname)
      print soname
      #-----------------



