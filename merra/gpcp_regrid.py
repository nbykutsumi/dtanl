from numpy import *
import calendar
import os
#***************************************************
iyear = 2001
eyear = 2001
imon  = 1
emon  = 12
#***************************************************
def mk_dir(sdir):
  if not os.access(sdir, os.F_OK):
    os.mkdir(sdir)
#***************************************************
def mk_dummy(sctlname, sdummyname):
  adummy = zeros(144*288, float32)
  adummy.tofile(sdummyname)
  #
  sout = ""
  sout = sout + "DSET %s\n"%(sdummyname)
  sout = sout + "title Template GrADS for regridding\n"
  sout = sout + "options yrev\n"
  sout = sout + "undef -9999.0\n"
  sout = sout + "xdef 288 linear -179.375 1.25\n"
  sout = sout + "ydef 144 linear 89.375 1.25\n"
  sout = sout + "zdef   1 levels  1000\n"
  sout = sout + "tdef 1 linear 0Z1jan1900 1dy\n"
  sout = sout + "vars 1\n"
  sout = sout + "var       0 0        generic sfc variable\n"
  sout = sout + "endvars\n"
  #
  f = open(sctlname, "w")
  f.write(sout)
  f.close()
#***************************************************
def mk_gsfile(sctlin, sctlout, soname):
  s=""
  s = s + "'open %s'\n" %(sctlin)
  s = s + "'open %s'\n" %(sctlout)
  s = s + "'set dfile 2'\n"
  s = s + "'set x 1 288'\n"
  s = s + "'set y 1 144'\n"
  s = s + "'set t 1'\n"
  s = s + "'var = lterp(var.1, var.2)'\n"
  s = s + "'set fwrite -le %s'\n" %(soname)
  s = s + "'set gxout fwrite'\n"
  s = s + "'d var'\n"
  s = s + "'disable fwrite'\n"
  s = s + "'quit'\n"
  #-----
  f = open("./gpcp_regrid.gs", "w")
  f.write(s)
  f.close()
#***************************************************
def mk_readme(sodir):
  s=""
  s= s + "lon = from -179.375 to 179.375, elon = 1.25deg\n"
  s= s + "lat = from -89.375 to 89.375,  dlat = 1.25deg\n"
  s= s + "!! unit is converted from original GPCP1DD"
  s= s + "Unit: mm/s"
  sfile = sodir + "/README.txt"
  f = open(sfile, "w")
  f.write(s)
  f.close()
#***************************************************
sidir_root = "/media/disk2/data/GPCP1DD/data/1dd"
sodir_root = "/media/disk2/data/GPCP1DD/data/merra1.25"
#***************************************************
# make out dir
#----------------
#***************************************************
# start loop
#***************************************************
for year in range(iyear, eyear+1):
  sodir = sodir_root + "/%04d"%(year)
  mk_dir(sodir)
  #*******************************
  # README file
  #-------------------------------
  mk_readme(sodir)
  #*******************************
  # ctl & dummy file
  #-------------------------------
  sctl_out   = sodir + "/merra.2D.Cx_slide.ctl"
  sdummy     = sodir + "/merra.2D.Cx_slide.bn"
  mk_dummy(sctl_out, sdummy)
  #*******************************
  for mon in range(imon, emon +1):
    for day in range(1, calendar.monthrange(year, mon)[1] +1):
      sidir = sidir_root + "/%04d"%(year)
      #****************************
      # ctl_input
      #----------------------------
      sctl_in = sidir + "/gpcp_1dd_v1.1_p1d.%04d%02d%02d.ctl"\
                       %(year, mon, day)
      #****************************
      # check input file
      #----------------------------
      if not os.access(sctl_in, os.F_OK):
        continue
      #****************************
      # output file
      #----------------------------
      soname = sodir + "/gpcp_1dd_v1.1_p1d.Cx.%04d%02d%02d.bn"\
                       %(year, mon, day)
      #****************************
      # Regrid with lterp
      #****************************
      ## ## Problem for lterp 
      ## The output of lterp have missing value (-9.99e+8)
      ##    on the first line. It should be replaced with zero
      #****************************
      # 1. use lterp
      #----------------------------
      mk_gsfile(sctl_in, sctl_out, soname)
      os.system("grads -blc ./gpcp_regrid.gs")
      #****************************
      # 2. fill lterp's default missing value with zero
      #----------------------------
      atemp = fromfile(soname, float32).reshape(144,288)
      atemp = ma.masked_equal(atemp, -9.99e+8)
      atemp = ma.filled(atemp, 0.0) /(60.0 * 60.0 * 24.0)
      #****************************
      # write final product
      #****************************
      atemp.tofile(soname)
      print soname
  #********************************
  # remove ctl
  #--------------------------------
  os.remove(sctl_out)
  os.remove(sdummy)
