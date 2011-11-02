import os
######################################
#iyear = 1990
#eyear = 1999
iyear = 2086
eyear = 2095
imon  = 1
emon  = 12
nx    = 144
ny    = 96
percent = 99.0
##
freq = "day"
model= "NorESM1-M"
#run  = "historical"
run  = "rcp85"
ens  = "r1i1p1"
######################################
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
