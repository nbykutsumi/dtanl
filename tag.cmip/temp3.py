from numpy import *

ny,nx  = 180,360


a2pr    = zeros([ny,nx],float32)

for day in range(1,31+1):
  iname = "/media/disk2/data/CMIP5/sa.one.MIROC5.historical/pr/198001/pr.r1i1p1.198001%02d.sa.one"%(day)
  print iname
  a2pr_tmp = fromfile(iname, float32).reshape(ny,nx)

  a2pr  = a2pr + a2pr_tmp
#---
a2pr  = a2pr / 31.0
print a2pr.sum()
