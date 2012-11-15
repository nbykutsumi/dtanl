from numpy import *
import os, sys
import calendar
import datetime
#******************************************************
#******************************************************
#var    = "UGRD"    # UGRD or VGRD
var    = "VGRD"    # UGRD or VGRD
tstp   = "6hr"
idir_root = "/media/disk2/data/JRA25/sa.one/%s"%(tstp)
#******************************************************
# set dlyrange
#******************************************************
dnx    = {}
dny    = {}
#****************************************************
iyear  = 2000
eyear  = 2004
imon   = 1
emon   = 12
nx     = 360
ny     = 180

dw         = 7
ldaydelta  = range(-dw, dw+1)
#####################################################
# Function
#####################################################
def check_file(sname):
  if not os.access(sname, os.F_OK):
    print "no file:",sname
    sys.exit()
#####################################################
def mk_dir(sdir):
  try:
    os.makedirs(sdir)
  except:
    pass
#******************************************************
def date_slide(year,mon,day, daydelta):
  today       = datetime.date(year, mon, day)
  target      = today + datetime.timedelta(daydelta)
  targetyear  = target.year
  #***********
  if ( calendar.isleap(targetyear) ):
    leapdate   = datetime.date(targetyear, 2, 29)
    #---------
    if (target <= leapdate) & (leapdate < today):
      target = target + datetime.timedelta(-1)
    elif (target >= leapdate ) & (leapdate > today):
      target = target + datetime.timedelta(1)
  #-----------
  return target
  
#******************************************************
odir_root = "/media/disk2/out/JRA25/sa.one/run.mean/%s"%(var)
#------------------------------
# make heads and tails
#------------------------------
for year in range(iyear, eyear+1):
#for year in range(1981, 1981+1):
  for  mon in range(imon, emon + 1):
    #*************
    odir       = odir_root + "/%04d%02d"%(year, mon)
    mk_dir(odir)
    ##*************
    ## no leap
    ##*************
    #if (mon==2)&(calendar.isleap(year)):
    #  ed = calendar.monthrange(year,mon)[1] -1
    #else:
    #  ed = calendar.monthrange(year,mon)[1]

    ed = calendar.monthrange(year,mon)[1]
    #*************
    for day in range(1, ed + 1):
      stime  = "%04d%02d%02d%02d"%(year,mon,day, 0)
      #***********
      oname  = odir + "/run.mean.%s.%s.sa.one"%(var, stime)
      #*********************
      # start running mean
      #*********************
      # dummy
      #********
      aout  = zeros(ny*nx)
      aout  = array( aout , float32)
      ntimes = 0
      #********
      for daydelta in ldaydelta:
        target     = date_slide( year, mon, day, daydelta)
        targetyear = target.year
        targetmon  = target.month
        targetday  = target.day
        #-------------------
        idir       = idir_root + "/%s/%04d%02d"%(var, targetyear,  targetmon)
        for targethour in [0, 6, 12, 18]:
          ntimes = ntimes + 1
          stimeh     = "%04d%02d%02d%02d"%(targetyear, targetmon, targetday, targethour)
          iname  = idir + "/anal_p25.%s.%s.sa.one"%(var, stimeh)
          if not os.access(iname, os.F_OK):
            print "no file", iname
            ntimes = ntimes - 1
            continue
          #--------------------
          # add 
          #--------------------
          ain   = fromfile(iname, float32)
          aout  = aout + ain
      #*****************
      aout    = aout / ntimes
      #*****************
      print oname
      aout.tofile(oname)



