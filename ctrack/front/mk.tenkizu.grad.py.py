import calendar
import subprocess
import os
iyear = 2004
eyear = 2004
#lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon  = [1,2,3,4]
#lmon  = [6,8,10,12]
#lmon  = [6,7,9,10, 1,2,3,4,5,8,11,12]
#lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon  = [1,2,6,7]
#lmon  = [5,7,9,11]
iday  = 1
#singleday = True
singleday = False
lhour  = [0]
thdura = 6
#-- local region ---
#lllat   = 20.
#urlat   = 60.
#lllon   = 110.
#urlon   = 160.
lllat   = 0.
urlat   = 80.
lllon   = 60.
urlon   = 190.



#plev    = 925*100.0
plev    = 850*100.0

for year in range(iyear, eyear+1):
  for mon in lmon: 
    eday = calendar.monthrange(year, mon)[1]
    if singleday == True:
      eday = iday
    for day in range(iday, eday+1):
      #-----------
      if ((year ==iyear)&(mon==lmon[0])&(day==iday)):
        cbarflag = "True"
      #-----------
      for hour in lhour:
        ##------
        #scmd = "python mk.tenkizu.frontogen.py %s %s %s %s %s %s %s %s %s %s %s"\
        #           %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev, cbarflag, thdura)
        #subprocess.call(scmd, shell=True)
        #------
        scmd = "python mk.tenkizu.others.py %s %s %s %s %s %s %s %s %s %s %s"\
                   %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev, cbarflag, thdura)
        subprocess.call(scmd, shell=True)
        #
        ##------
        #scmd = "python mk.tenkizu.wind.py %s %s %s %s %s %s %s %s %s %s %s"\
        #           %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev, cbarflag, thdura)
        #subprocess.call(scmd, shell=True)

        ##------
        scmd = "python mk.tenkizu.grad.py %s %s %s %s %s %s %s %s %s %s %s"\
                   %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev, cbarflag, thdura)
        subprocess.call(scmd, shell=True)
        ###------
        #scmd = "python mk.tenkizu.q.front.py %s %s %s %s %s %s %s %s %s %s %s"\
        #           %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev, cbarflag, thdura)
        #subprocess.call(scmd, shell=True)
        ###------
        #scmd = "python mk.tenkizu.t.front.py %s %s %s %s %s %s %s %s %s %s %s"\
        #           %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev, cbarflag, thdura)
        #subprocess.call(scmd, shell=True)

