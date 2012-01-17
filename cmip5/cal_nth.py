import os
######################################
lmodel = ["NorESM1-M", "MIROC5", "CanESM2"]
#lmodel = ["MIROC5", "CanESM2"]
lrun   = ["historical","rcp85"]
###################
# set dlyrange
#-----------------
dlyrange     = {"historical":[1990,1999], "rcp85":[2086,2095]}
###################
imon  = 1
emon  = 12
###################
# set dnz, dny, dnx
###################
dnx    = {}
dny    = {}
dnz    = {}
#
dnz["NorESM1-M"] = 8
dny["NorESM1-M"] = 96
dnx["NorESM1-M"] = 144
#
dnz["MIROC5"] = 8
dny["MIROC5"] = 128
dnx["MIROC5"] = 256
#
dnz["CanESM2"] = 8
dny["CanESM2"] = 64
dnx["CanESM2"] = 128
###################
#percent = 99.0
percent = 50.0
##
freq = "day"
ens  = "r1i1p1"
######################################
for model in lmodel:
  #---------------
  nz = dnz[model]
  ny = dny[model]
  nx = dnx[model]
  #---------------
  for run in lrun:
    lyrange = dlyrange[run]
    iyear = lyrange[0]
    eyear = lyrange[1]
    print "run=",run
    print "iyear, eyear =", iyear, eyear
    #---------------
    sidir_root1 = "/media/disk2/data/CMIP5/bn"
    #sidir_root2 = "/pr/day/NorESM1-M/historical/r1i1p1"
    sidir_root2 = "/pr/%s/%s/%s/%s"%(freq, model, run, ens)
    sidir_root  = sidir_root1 + sidir_root2
    #siname_head = "pr_day_NorESM1-M_historical_r1i1p1_"
    siname_head = "pr_%s_%s_%s_%s"%(freq, model, run, ens)
    #sodir_root  = "/media/disk2/out/CMIP5/day/NorESM1-M/historical/r1i1p1/prxth"
    sodir_root  = "/media/disk2/out/CMIP5/%s/%s/%s/%s/prxth"%(freq, model, run, ens)
    sodir = sodir_root +"/%04d-%04d/%02d-%02d"%(iyear, eyear, imon, emon)
    #soname_head = "prxth_day_NorESM1-M_historical_r1i1p1"
    soname_head = "prxth_%s_%s_%s_%s"\
                  %(freq, model, run, ens)
    ######################################
    # make directory
    ######################################
    try:
      os.makedirs(sodir)
    except OSError:
      pass
    ######################################
    cmd = "/home/utsumi/bin/dtanl/cmip5/cal_nth"
    ######################################
    os.system("%s %s %s %s %s %s %s %s %s %s %s %s" %(cmd, iyear, eyear, imon, emon, sidir_root, siname_head, sodir, soname_head, nx, ny, percent))
    #print "%s %s %s %s %s %s %s %s %s %s %s %s" %(cmd, iyear, eyear, imon, emon, sidir_root, siname_head, sodir, soname_head, nx, ny, percent)
