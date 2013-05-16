import subprocess

iyear = 2000
eyear = 2004
imon  = 1
emon  = 12
for year in range(iyear , eyear+1):
  for mon in range(imon, emon+1):
    prog = "/home/utsumi/bin/dtanl/mk.mean.GPCP1DD.py"
    scm  = "python %s %04d %04d %d"%(prog, year, year, mon)
    subprocess.call(scm, shell=True)
