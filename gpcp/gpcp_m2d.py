from numpy import *
import calendar
import os, sys
#********************************************
iyear = 1997
eyear = 2010
imon  = 1
emon  = 12
#********************************************
def readheader(siname):
  f = open(siname)
  s = f.read()
  f.close()
  sheader = s[:1440]
  return sheader
#********************************************
def writestring(sout, sofile):
  f = open(sofile, "w")
  f.write(sheader)
  f.close()
#********************************************
def mk_dir(sdir):
  if not os.access(sdir , os.F_OK):
    os.mkdir(sdir)
#********************************************
def mk_ctl(sfile, year):
  #----
  if calendar.isleap(year):
    nday = 366
  else:
    nday = 365
  #----
  sout = ""
  sout = sout + "DSET gpcp_1dd_v1.2_p1d.%y4%m2%d2.bn\n"
  sout = sout + "title Template GrADS for regridding\n"
  sout = sout + "options template yrev\n"
  sout = sout + "undef -99999.\n"
  sout = sout + "xdef 360 linear 0.5  1.0\n"
  sout = sout + "ydef 180 linear 89.5 1.0\n"
  sout = sout + "zdef   1 levels  1000\n"
  sout = sout + "tdef %s linear 1jan%04d 1dy\n"%(nday, year)
  sout = sout + "vars 1\n"
  sout = sout + "var       0 0        generic sfc variable\n"
  sout = sout + "endvars\n"
  f = open(sfile, "w")
  f.write(sout)
  f.close()
#********************************************
def mk_ctl_daily(sfile_daily, soname):
  sout = ""
  sout = sout + "DSET %s\n"%(soname)
  sout = sout + "title Template GrADS for regridding\n"
  sout = sout + "options yrev\n"
  sout = sout + "undef -99999.\n"
  sout = sout + "xdef 360 linear 0.5  1.0\n"
  sout = sout + "ydef 180 linear 89.5 1.0\n"
  sout = sout + "zdef   1 levels  1000\n"
  sout = sout + "tdef 1 linear 0Z1jan1900 1dy\n"
  sout = sout + "vars 1\n"
  sout = sout + "var       0 0        generic sfc variable\n"
  sout = sout + "endvars\n"
  f = open(sfile_daily, "w")
  f.write(sout)
  f.close()
#********************************************
for year in range(iyear, eyear +1):
  #-----
  #sidir = "/media/disk2/data/GPCP1DD/data/org"
  sidir = "/home/utsumi/mnt/export/nas02/data/GPCP1DD/v1.2/data"
  sodir = "/media/disk2/data/GPCP1DD/v1.2/1dd/%04d"%(year)
  mk_dir(sodir)
  #**************
  # make annal ctl file
  #--------------
  sctlfile = sodir + "/gpcp_1dd_v1.2_p1d.%04d.ctl"%(year)
  mk_ctl(sctlfile, year)
  #**************
  for mon in range(imon, emon+1):
    #*****************
    # open input monthly file
    #*****************
    siname  = sidir + "/gpcp_1dd_v1.2_p1d.%04d%02d"%(year, mon)
    if not os.access(siname, os.F_OK):
      continue
    #************
    # read & write header
    #************
    sheader = readheader(siname)
    sheadfile = sodir + "/head.gpcp_1dd_v1.2_p1d.%04d%02d"%(year, mon)
    writestring( sheader.strip(), sheadfile)
    #************
    amondat_org = fromfile(siname, float32)
    amondat = amondat_org[1440/4.0 : ]
    #******************
    for day in range(1, calendar.monthrange(year, mon)[1]+1):
      #************
      # soname
      #------------
      soname = sodir + "/gpcp_1dd_v1.2_p1d.%04d%02d%02d.bn"%(year, mon, day)
      #************
      # make daily ctl file
      #------------
      sctlfile_daily = sodir + "/gpcp_1dd_v1.2_p1d.%04d%02d%02d.ctl"%(year, mon, day)
      mk_ctl_daily(sctlfile_daily, soname)
      #************
      adaydat = amondat[360*180*(day-1) : 360*180*day].byteswap()
      adaydat.tofile(soname)
      print soname
    #******************
    #******************
