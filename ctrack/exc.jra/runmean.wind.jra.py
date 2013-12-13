from numpy import *
import os, sys
import calendar
import datetime
#******************************************************
#******************************************************
#var    = "UGRD"    # UGRD or VGRD
#var    = "VGRD"    # UGRD or VGRD
lvar   = ["UGRD","VGRD"]
plev  = 500
tstp   = "6hr"
idir_root = "/media/disk2/data/JRA25/sa.one.anl_p/%s"%(tstp)
#******************************************************
# set dlyrange
#******************************************************
dnx    = {}
dny    = {}
#****************************************************
#lyear  = [1996,1997,1998,1999,2000,2001,2002,2003,2005,2006,2007,2008,2009,2010,2011,2012]
lyear  = range(1980,1995+1)
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

for var in lvar:
  #------
  odir_root = "/media/disk2/out/JRA25/sa.one.anl_p/run.mean/%s"%(var)
  #------------------------------
  # make heads and tails
  #------------------------------
  for year in lyear:
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
        oname  = odir + "/run.mean.%s.%04dhPa.%s.sa.one"%(var, plev, stime)
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
            iname  = idir + "/anl_p.%s.%04dhPa.%s.sa.one"%(var, plev, stimeh)
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
  


