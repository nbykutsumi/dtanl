import subprocess
import calendar
lbstflag = ["bst","obj"]  # "bst" or ""
lyear  = [2008,2009,2010]
lmon   = [6,7,8,9]
dday  = 7
thdura = 24
region = "INDIA"
for  bstflag in lbstflag:
  for year in lyear:
    for mon in lmon:
      #for iday in range(1,31,dday):
      #  eday = iday + dday-1
      #--
      iday = 1
      eday = calendar.monthrange(year,mon)[1]
      #--- obj ------
      if bstflag == "obj":
        prog = "/home/utsumi/bin/dtanl/ctrack/jra/mk.exc.trackline.region.py"
      elif bstflag == "bst":
        prog = "/home/utsumi/bin/dtanl/ctrack/jra/mk.exc.trackline.bsttc.region.py"
      #
      scmd = "python %s %s %s %s %s %s %s"%(prog, year, mon, iday, eday, thdura, region)
      print scmd
      subprocess.call(scmd, shell=True)
      
      ##--- chart ------
      #prog = "/home/utsumi/bin/dtanl/ctrack/chartc/mk.trackline.chartc.py"
      #scmd = "python %s %s %s %s %s"%(prog, year, mon, iday, eday)
      #subprocess.call(scmd, shell=True)
        
      
