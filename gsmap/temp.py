from numpy import *
import gsmap_func
year = 2001
mon   = 1
day   = 31
nhour = 3
lhour = [23]
miss  = -9999.0
for hour in lhour:
  a     = ma.masked_equal(gsmap_func.timeave_gsmap_backward_org(year,mon,day,hour, nhour)[:123], miss)
  print a.mean()
