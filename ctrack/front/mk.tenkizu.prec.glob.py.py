import subprocess
import calendar

#--------------------------
iyear  = 2004
eyear  = 2004
lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
iday   = 1
lhour  = [0]
lllat  = -79.5
urlat  = 79.5
lllon  = 0.0
urlon  = 359.5

plev   = 850.*100.
thdura = 6
sresol = "anl_p"

#-----
for year in range(iyear,eyear+1):
  for mon in lmon:
    eday  = calendar.monthrange(year,mon)[1]
    for day in range(iday,eday+1):
      #------------
      if day == iday:
        cbarflag = True
      else:
        cbarflag = False
      #------------
      for hour in lhour:
        scmd = "python ./mk.tenkizu.prec.glob.py %s %s %s %s %s %s %s %s %s %s %s %s"\
              %(year,mon,day,hour,lllat,urlat,lllon,urlon,plev,cbarflag,thdura,sresol)
        subprocess.call(scmd, shell=True)

