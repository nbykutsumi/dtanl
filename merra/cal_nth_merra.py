import os
######################################
iyear = 2001
eyear = 2002
imon  = 1
emon  = 12
nx    = 288
ny    = 144
percent = 99.0
##
freq = "day"
######################################
sidir_root = "/media/disk2/data/MERRA/bn/%s/prectot"%(freq)
siname_head = "MERRA.%s.prectot"%(freq)
sodir_root  = "/media/disk2/out/MERRA/%s/prxth"%(freq)
sodir = sodir_root +"/%04d-%04d/%02d-%02d"%(iyear, eyear, imon, emon)
soname_head = "prxth.MERRA.%s"%(freq)
######################################
# make directory
######################################
try:
  os.makedirs(sodir)
except OSError:
  pass
######################################
cmd = "/home/utsumi/bin/dtanl/merra/cal_nth_merra"
######################################
os.system("%s %s %s %s %s %s %s %s %s %s %s %s" %(cmd, iyear, eyear, imon, emon, sidir_root, siname_head, sodir, soname_head, nx, ny, percent))
#print "%s %s %s %s %s %s %s %s %s %s %s %s" s(cmd, iyear, eyear, imon, emon, sidir_root, siname_head, sodir, soname_head, nx, ny, percent)
