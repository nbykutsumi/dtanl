import subprocess
import os
import calendar
import matplotlib.image as mpimg
from numpy import *
#----------------------------------
iyear = 2006
eyear = 2006
#eyear = 2003

jpgdir  = "/home/utsumi/bin/dtanl/ctrack/chart/test"
for year in range(iyear, eyear+1):
  for mon in range(1,12+1):
    eday = calendar.monthrange(year, mon)[1]
    for day in [1, eday]:
      pdfdir = "/media/disk2/data/JMAChart/ASAS/%04d%02d"%(year, mon)
      pdfname1 = pdfdir + "/AS_%04d%02d%02d12.pdf"%(year, mon, day)
      pdfname2 = pdfdir + "/AS_%04d%02d%02d12.PDF"%(year, mon, day)
      pdfname3 = pdfdir + "/As_%04d%02d%02d12.pdf"%(year, mon, day)
      pdfname4 = pdfdir + "/As_%04d%02d%02d12.PDF"%(year, mon, day)
      if os.access(pdfname1, os.F_OK):
        pdfname = pdfname1
      if os.access(pdfname2, os.F_OK):
        pdfname = pdfname2
      if os.access(pdfname3, os.F_OK):
        pdfname = pdfname3
      if os.access(pdfname4, os.F_OK):
        pdfname = pdfname4
      #----- resize --------------------- 
      #print pdfname
      jpgname  = jpgdir + "/As_%04d.%02d.%02d.jpg"%(year, mon, day)
      scmd = "convert -resize 1300x900 %s %s"%(pdfname, jpgname)
      #subprocess.call(scmd, shell=True)
      #----- original size --------------
      #print pdfname
      jpgorgname  = jpgdir + "/org.As_%04d.%02d.%02d.jpg"%(year, mon, day)
      scmd = "convert %s %s"%(pdfname, jpgorgname)
      #subprocess.call(scmd, shell=True)
      #-------------------------------------
      #print jpgname
      #a2jpg = mpimg.imread(jpgname)
      #print year, mon, day, shape(a2jpg)
      a2jpgorg = mpimg.imread(jpgorgname)
      print year, mon, day, shape(a2jpgorg)
      #print year,mon,day



