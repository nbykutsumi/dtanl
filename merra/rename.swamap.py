#import os
#import calendar
##----------------------------------
#idir_root="/media/disk2/out/MERRA/day/scales/validate/swa.map"
#
#iyear = 2000
#eyear = 2010
#imon = 1
#emon = 12
#
#for year in range(iyear, eyear+1):
#  idir = idir_root + "/%04d"%(year)
#  for mon in range(imon, emon+1):
#    print year, mon
#    for day in range(1, calendar.monthrange(year, mon)[1]+1):
#      ifile = idir + "/corr.prec.swa.%04d.%02d.%02d.00.bn"%(year, mon, day)
#      ofile = idir + "/MERRA.day.swa.%04d.%02d.%02d.00.bn"%(year, mon, day)
#      if os.access(ifile, os.F_OK):
#        os.rename(ifile, ofile)
