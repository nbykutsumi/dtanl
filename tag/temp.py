from gsmap_fsub import *
from numpy import *
import gsmap_func, calendar

ptile = 99.9
thmissrat = 0.8
iyear = 2002
eyear = 2002
#lmon  = range(1,12+1)
lmon  =[1]
lhour = arange(0,24)
nhour = 24
miss  = -9999.0
ny,nx = 120,360
a2one = ones([ny,nx],float32)
#
ptiledir = "/media/disk2/data/GSMaP/sa.one/1hr/ptot/ptile/2001-2009"
ptilename = ptiledir + "/gsmap_mvk.v5.222.1.movw%02dhr.%3.1f.p%05.2f.ALL.sa.one"%(nhour, thmissrat, ptile)
a2ptile = ma.masked_equal(fromfile(ptilename,float32).reshape(120,360),miss)

a2countsum = zeros([ny,nx],float32)
for year in range(iyear,eyear+1):
  for mon in lmon:
    eday = calendar.monthrange(year,mon)[1]
    for day in range(1,eday+1):
      for hour in lhour:
        a = ma.masked_equal(gsmap_func.timeave_gsmap_backward_saone(year,mon,day,hour,nhour),miss)
        d = a2ptile - a
        a2count = ma.masked_where(a < a2ptile, a2one)
        count = a2count.sum()
        print count /(ny*nx)
        a2countsum = a2countsum + a2count.filled(0.0)

oname = "./count.plain.sa.one"
a2countsum.tofile(oname)
