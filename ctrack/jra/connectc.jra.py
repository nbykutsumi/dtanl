import ctrack
from numpy import *
import calendar
import datetime
import os, sys
##***************************
#--------------------------------------------------
tstp        = "6hr"
hinc        = 6
iyear       = 2000
eyear       = 2004
imon        = 1
emon        = 12
nx          = 360
ny          = 180
miss_dbl    = -9999.0
miss_int    = -9999
endh        = 18
thdp        = 30.0  #[Pa]
thdist      = 300.0*1000.0   #[m]
#
#####################################################
# functions
#####################################################
def xy2fortpos(ix, iy, nx):
  ix     = ix + 1  # ix = 1,2,.. nx
  iy     = iy + 1  # iy = 1,2,.. ny
  #number = iy* nx + ix +1
  number = (iy-1)* nx + ix
  return number
#####################################################
def fortpos2xy(number, nx, miss_int):
  if (number == miss_int):
    iy0 = miss_int
    ix0 = miss_int
  else:
    iy0 = int((number-1)/nx)  +1  # iy0 = 1, 2, ..
    ix0 = number - nx*(iy0-1)     # ix0 = 1, 2, ..

    iy0 = iy0 -1    # iy0 = 0, 1, .. ny-1
    ix0 = ix0 -1    # ix0 = 0, 1, .. nx-1
  #----
  return ix0, iy0
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
#####################################################
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
#****************************************************
def read_txtlist(iname):
  f = open(iname, "r")
  lines = f.readlines()
  f.close()
  lines = map(float, lines)
  aout  = array(lines, float32)
  return aout
#****************************************************
#****************************************************
# dir_root
#---------------
psldir_root     = "/media/disk2/data/JRA25/sa.one/%s/PRMSL"%(tstp)
winddir_root    = "/media/disk2/out/JRA25/sa.one/run.mean"
pmeandir_root   = "/media/disk2/out/JRA25/sa.one/%s/pmean"%(tstp)
pgraddir_root   = "/media/disk2/out/JRA25/sa.one/%s/pgrad"%(tstp)
orogdir_root    = "/media/disk2/data/JRA25/sa.one/const/topo"
axisdir_root    = psldir_root

#
lastposdir_root  = "/media/disk2/out/JRA25/sa.one/%s"%(tstp)
pgmaxdir_root    = "/media/disk2/out/JRA25/sa.one/%s"%(tstp)
iposdir_root     = "/media/disk2/out/JRA25/sa.one/%s"%(tstp)
idatedir_root    = "/media/disk2/out/JRA25/sa.one/%s"%(tstp)
timedir_root     = "/media/disk2/out/JRA25/sa.one/%s"%(tstp)
pgraddir_root    = "/media/disk2/out/JRA25/sa.one/%s"%(tstp)
lifedir_root     = "/media/disk2/out/JRA25/sa.one/%s"%(tstp)
nextposdir_root  = "/media/disk2/out/JRA25/sa.one/%s"%(tstp)
#****************************************************
# read lat, lon data
#----------------------
axisdir    = axisdir_root  + "/%04d%02d"%(iyear, imon)
latname    = axisdir  + "/lat.txt"
lonname    = axisdir  + "/lon.txt"
a1lat      = read_txtlist(latname)
a1lon      = read_txtlist(lonname)

#**************************************************
#**************************************************
#counter = 0
#for year in range(iyear, eyear+1):
##for year in range(1990, 1990+1):
#  print "connectc.py, up",year
#  #---------
#  # dirs
#  #---------
#  for mon in range(imon, emon+1):
#  #for mon in range(1, 1+1):
#    ##############
#    # no leap
#    ##############
#    if (mon==2)&(calendar.isleap(year)):
#      ed = calendar.monthrange(year,mon)[1] -1
#    else:
#      ed = calendar.monthrange(year,mon)[1]
#    ##############
#    for day in range(1, ed+1):
#    #for day in range(1, 1+1):
#      for hour in range(0, endh+1, hinc):
#        counter = counter + 1
#        #---------
#        year1 = year
#        mon1  = mon
#        day1  = day
#        hour1 = hour
#        #---------
#        hour0    = hour - hinc
#        if (hour0 < 0):
#          date0    = date_slide(year,mon,day, -1)
#          year0    = date0.year
#          mon0     = date0.month
#          day0     = date0.day
#          hour0    = 24 + hour0
#          stimeh0  = "%04d%02d%02d%02d"%(year0,mon0,day0,hour0)
#          stimed0  = "%04d%02d%02d%02d"%(year0,mon0,day0,0)
#
#        else:
#          year0    = year
#          mon0     = mon
#          day0     = day
#          hour0    = hour0
#          stimeh0  = "%04d%02d%02d%02d"%(year,mon,day,hour0)
#          stimed0  = "%04d%02d%02d%02d"%(year,mon,day,0)
#        #------
#        stimeh1  = "%04d%02d%02d%02d"%(year,mon,day,hour)
#        #------
#        #***************************************
#        #* names for 0
#        #---------------------------------------
#        #   DIRS 
#        #**********
#        psldir0     = psldir_root     + "/%04d%02d"%(year0, mon0)
#        pmeandir0   = pmeandir_root   + "/%04d%02d"%(year0, mon0)
#        uadir0      = winddir_root    + "/UGRD/%04d%02d"%(year0, mon0)
#        vadir0      = winddir_root    + "/VGRD/%04d%02d"%(year0, mon0)
#        #
#        lastposdir0 = lastposdir_root + "/lastpos/%04d%02d"%(year0, mon0)
#        pgmaxdir0   = pgmaxdir_root   + "/pgmax/%04d%02d"%(year0, mon0)
#        pdraddir0   = pgmaxdir_root   + "/pgmaxs/%04d%02d"%(year0, mon0)
#        iposdir0    = iposdir_root    + "/ipos/%04d%02d"%(year0, mon0)
#        idatedir0   = idatedir_root   + "/idate/%04d%02d"%(year0, mon0)
#        timedir0    = timedir_root    + "/time/%04d%02d"%(year0, mon0)
#
#        #----------
#        #   names
#        #**********
#        pslname0    = psldir0   + "/fcst_phy2m.PRMSL.%s.sa.one"%(stimeh0)
#        pmeanname0  = pmeandir0 + "/pmean.%s.sa.one"%(stimeh0)
#        uaname0     = uadir0    + "/run.mean.UGRD.%s.sa.one"%(stimed0)
#        vaname0     = vadir0    + "/run.mean.VGRD.%s.sa.one"%(stimed0)
#        #
#        lastposname0 = lastposdir0     + "/lastpos.%s.sa.one"%(stimeh0) 
#        pgmaxname0   = pgmaxdir0       + "/pgmax.%s.sa.one"%(stimeh0) 
#        iposname0    = iposdir0        + "/ipos.%s.sa.one"%(stimeh0)
#        idatename0   = idatedir0       + "/idate.%s.sa.one"%(stimeh0)
#        timename0    = timedir0        + "/time.%s.sa.one"%(stimeh0)
#        #
#        mk_dir(lastposdir0)
#        mk_dir(pgmaxdir0)
#        mk_dir(iposdir0)
#        mk_dir(iposdir0)
#        mk_dir(idatedir0)
#        mk_dir(timedir0)
#        #***************************************
#        #* names for 1
#        #---------------------------------------
#        #    DIRS
#        #***********
#        psldir1     = psldir_root      + "/%04d%02d"%(year, mon)
#        pmeandir1   = pmeandir_root    + "/%04d%02d"%(year, mon)
#        #
#        lastposdir1 = lastposdir_root  + "/lastpos/%04d%02d"%(year1, mon1)
#        pgmaxdir1   = pgmaxdir_root    + "/pgmax/%04d%02d"%(year1, mon1)
#        iposdir1    = iposdir_root     + "/ipos/%04d%02d"%(year1, mon1)
#        idatedir1   = idatedir_root    + "/idate/%04d%02d"%(year1, mon1)
#        timedir1    = timedir_root     + "/time/%04d%02d"%(year1, mon1)
#        pgraddir1   = pgraddir_root    + "/pgrad/%04d%02d"%(year1, mon1)
#        #------
#        mk_dir(lastposdir1)
#        mk_dir(pgmaxdir1)
#        mk_dir(iposdir1)
#        mk_dir(iposdir1)
#        mk_dir(idatedir1)
#        mk_dir(timedir1)
#        #----------
#        #   names
#        #**********
#        pslname1   = psldir1           + "/fcst_phy2m.PRMSL.%s.sa.one"%(stimeh1)
#        pmeanname1 = pmeandir1         + "/pmean.%s.sa.one"%(stimeh1)
#        #
#        lastposname1 = lastposdir1     + "/lastpos.%s.sa.one"%(stimeh1)
#        pgmaxname1    = pgmaxdir1      + "/pgmax.%s.sa.one"%(stimeh1)
#        iposname1    = iposdir1        + "/ipos.%s.sa.one"%(stimeh1)
#        idatename1   = idatedir1       + "/idate.%s.sa.one"%(stimeh1)
#        timename1    = timedir1        + "/time.%s.sa.one"%(stimeh1)
#        pgradname1   = pgraddir1       + "/pgrad.%s.sa.one"%(stimeh1)
#        #***************************************
#        # read data
#        #---------------------------------------
#        #   for 0
#        #************
#        if ( os.access(iposname0, os.F_OK) ):
#          a2pmean0   = fromfile(pmeanname0,   float32).reshape(ny, nx)
#          a2psl0     = fromfile(pslname0,     float32).reshape(ny, nx)
#          a2ua0      = fromfile(uaname0,      float32).reshape(ny, nx)
#          a2va0      = fromfile(vaname0,      float32).reshape(ny, nx)
#          #--
#          a2lastpos0 = fromfile(lastposname0, int32).reshape(ny, nx)
#          a2pgmax0   = fromfile(pgmaxname0,   float32).reshape(ny, nx)
#          a2ipos0    = fromfile(iposname0,    int32).reshape(ny, nx)
#          a2idate0   = fromfile(idatename0,   int32).reshape(ny, nx)
#          a2time0    = fromfile(timename0,    int32).reshape(ny, nx)
#        elif ( counter == 1):
#          a2pmean0   = array(ones(ny*nx).reshape(ny,nx)*miss_dbl, float32)
#          a2psl0     = array(ones(ny*nx).reshape(ny,nx)*miss_dbl, float32)
#          a2ua0      = array(zeros(ny*nx).reshape(ny,nx), float32)
#          a2va0      = array(zeros(ny*nx).reshape(ny,nx), float32)
#          #--
#          a2lastpos0 = array(ones(ny*nx).reshape(ny,nx)*miss_int, int32)
#          a2pgmax0   = array(ones(ny*nx).reshape(ny,nx)*miss_dbl, float32)
#          a2ipos0    = array(ones(ny*nx).reshape(ny,nx)*miss_int, int32)
#          a2idate0   = array(ones(ny*nx).reshape(ny,nx)*miss_int, int32)
#          a2time0    = array(ones(ny*nx).reshape(ny,nx)*miss_int, int32)
#        else:
#          print "nofiles: stimeh0 = ",stimeh0
#          print "iposname0 =", iposname0
#          sys.exit()
#        #------------
#        #   for 1
#        #************
#        a2pmean1     = fromfile(pmeanname1, float32).reshape(ny, nx)
#        a2psl1       = fromfile(pslname1,   float32).reshape(ny, nx)
#        a2pgrad1     = fromfile(pgradname1, float32).reshape(ny, nx)
#        #****************************************
#        # connectc
#        ##***************************************
#        ctrackout = ctrack.ctrack.connectc(\
#           a2pmean0.T, a2pmean1.T, a2psl0.T, a2psl1.T, a2ua0.T, a2va0.T\
#           , a2pgmax0.T, a2ipos0.T, a2idate0.T, a2time0.T\
#           , a2pgrad1.T\
#           , a1lon, a1lat, thdp, thdist, hinc, miss_dbl, miss_int\
#           , year1, mon1, day1, hour1\
#           )
#
#        a2lastpos1 = array(ctrackout[0].T, int32)
#        a2pgmax1   = array(ctrackout[1].T, float32)
#        a2ipos1    = array(ctrackout[2].T, int32)
#        a2idate1   = array(ctrackout[3].T, int32)
#        a2time1    = array(ctrackout[4].T, int32)
#        #****************************************
#        # write to file
#        #----------------------------------------
#        a2lastpos1.tofile(lastposname1)
#        a2pgmax1.tofile(pgmaxname1)
#        a2ipos1.tofile(iposname1)
#        a2idate1.tofile(idatename1)
#        a2time1.tofile(timename1)
#
#        #*****************************************
#
#        #for iy1 in range(0, ny):
#        #  for ix1 in range(0, nx):
#        #    psl1     = a2psl1[iy1, ix1]
#        #    pmin1    = a2pmin1[iy1, ix1]
#        #    ipos1    = a2ipos1[iy1, ix1]
#        #    idate1   = a2idate1[iy1, ix1]
#        #    time1    = a2time1[iy1, ix1]
#        #    lastpos1 = a2lastpos1[iy1, ix1]
#        #    (ix0, iy0) = fortpos2xy( lastpos1, nx, miss_int)
#        #    if (ix0 != miss_int):
#        #      psl0   = a2psl0[iy0, ix0]
#        #      pmin0  = a2pmin0[iy0, ix0]
#        #      time0  = a2time0[iy0, ix0]
#        #      ipos0  = a2ipos0[iy0, ix0]
#        #      idate0 = a2idate0[iy0, ix0]
#        #      if (  (ipos1 == 610) and (idate1 == 1990010100) ):
#        #        print timename1
#        #        print "0, ix0, iy0, ipos0, idate0, time0", ix0, iy0, ipos0, idate0, time0, "pmin0",pmin0, "psl0", psl0
#        #        print "1, ix1, iy1, ipos1, idate1, time1", ix1, iy1, ipos1, idate1, time1, "pmin1",pmin1, "psl1", psl1
#        #        print "pmin0 - pmin1=", pmin0 - pmin1
#        #        print "psl1 - pmin1=", psl1 - pmin1
###*************************************************
counter = 0
for year in range(eyear, iyear -1, -1):
  for mon in range(emon, imon -1, -1):
    print "connectc.py, down",year, mon
    ##############
    # no leap
    ##############
    if (mon==2)&(calendar.isleap(year)):
      ed = calendar.monthrange(year,mon)[1] -1
    else:
      ed = calendar.monthrange(year,mon)[1]
    ##############
    for day in range(ed, 1-1, -1):
      for hour in range(endh, 0-1, -hinc):
        counter = counter + 1
        #---------
        year1 = year
        mon1  = mon
        day1  = day
        hour1 = hour
        #---------
        hour0    = hour - hinc
        if (hour0 < 0):
          date0    = date_slide(year,mon,day, -1)
          year0    = date0.year
          mon0     = date0.month
          day0     = date0.day
          hour0    = 24 + hour0
          stimeh0  = "%04d%02d%02d%02d"%(year0,mon0,day0,hour0)
          stimed0  = "%04d%02d%02d%02d"%(year0,mon0,day0,0)

        else:
          year0    = year
          mon0     = mon
          day0     = day
          hour0    = hour0
          stimeh0  = "%04d%02d%02d%02d"%(year,mon,day,hour0)
          stimed0  = "%04d%02d%02d%02d"%(year,mon,day,0)
        #------
        stimeh1  = "%04d%02d%02d%02d"%(year,mon,day,hour)
        #------
        #print stimeh1
        #***************************************
        #* names for 1
        #---------------------------------------
        #    DIRS
        #***********
        lastposdir1 = lastposdir_root  + "/lastpos/%04d%02d"%(year1, mon1)
        pgmaxdir1   = pgmaxdir_root    + "/pgmax/%04d%02d"%(year1, mon1)
        iposdir1    = iposdir_root     + "/ipos/%04d%02d"%(year1, mon1)
        idatedir1   = idatedir_root    + "/idate/%04d%02d"%(year1, mon1)
        timedir1    = timedir_root     + "/time/%04d%02d"%(year1, mon1)
        #----------
        #   names
        #**********
        lastposname1 = lastposdir1     + "/lastpos.%s.sa.one"%(stimeh1) 
        pgmaxname1   = pgmaxdir1       + "/pgmax.%s.sa.one"%(stimeh1)
        iposname1    = iposdir1        + "/ipos.%s.sa.one"%(stimeh1)
        idatename1   = idatedir1       + "/idate.%s.sa.one"%(stimeh1)
        timename1    = timedir1        + "/time.%s.sa.one"%(stimeh1)
        #----------
        # read data
        #**********
        a2lastpos1   = fromfile(lastposname1, int32).reshape(ny,nx)
        a2pgmax1     = fromfile(pgmaxname1, float32).reshape(ny,nx)
        a2time1      = fromfile(timename1,    int32).reshape(ny,nx)

        #**************************************
        #   inverse trace
        #--------------------------------------
        if (counter == 1):
          a2lifenext   = array(ones(ny*nx).reshape(ny,nx) * miss_int, int32)
        #--------------------------
        # initialize a2life1 and a2life2_new
        #*****************
        a2life1        = array(ones(ny*nx).reshape(ny,nx) * miss_int, int32)
        a2lifenext_new = array(ones(ny*nx).reshape(ny,nx) * miss_int, int32)
        a2nextpos0     = array(ones(ny*nx).reshape(ny,nx) * miss_int, int32)
        #*****************
        for iy1 in range(0, ny):
          for ix1 in range(0, nx):
            if (a2time1[iy1, ix1] != miss_int):  # find cyclone
              #pmin1    = a2pmin1[iy1, ix1]
              pgmax1   = a2pgmax1[iy1, ix1]
              time1    = a2time1[iy1, ix1]
              lifenext = a2lifenext[iy1, ix1]
              (ix0,iy0) = fortpos2xy(a2lastpos1[iy1,ix1], nx, miss_int)
              #---- 
              if (lifenext == miss_int):
                #life1 = 10000 * int(pgmax1) + time1
                life1 = 1000000* time1 + int(pgmax1)
                #print "date=",stimeh1
                #print "time1=",time1
                #print "pmin1=",pmin1
              else:
                life1 = lifenext
              #----
              a2life1[iy1, ix1] = life1
              #-----------------------
              # fill a2life2_new
              #***************
              if (ix0 != miss_int):
                a2lifenext_new[iy0, ix0] = life1
              #-----------------------
              # make "a2nextpos0"
              #***************
              if (iy0 != miss_int):
                a2nextpos0[iy0, ix0] = xy2fortpos(ix1, iy1, nx)
        #-------------------
        # replace a2lifenext with new data
        #*******************
        a2lifenext = a2lifenext_new
        #**************************************
        # write to file
        #--------------------------------------
        # out dir
        #**********
        lifedir1      = lifedir_root     + "/life/%04d%02d"%(year1, mon1)
        nextposdir0   = nextposdir_root      + "/nextpos/%04d%02d"%(year0, mon0)
        mk_dir(lifedir1)
        mk_dir(nextposdir0)
        #----------
        # out name
        #**********
        lifename1     = lifedir1          + "/life.%s.sa.one"%(stimeh1)
        nextposname0  = nextposdir0       + "/nextpos.%s.sa.one"%(stimeh0)
        
        #----------
        # write to file
        #**********
        a2life1.tofile(lifename1)
        a2nextpos0.tofile(nextposname0) 
        #----------
        # "nextpos" for last time
        #**********
        if counter == 1:
          nextposdir1   = nextposdir_root + "/nextpos/%04d%02d"%(year1, mon1)
          nextposname1  = nextposdir1     + "/nextpos.%s.sa.one"%(stimeh1)
          a2nextpos1    = array(ones(ny*nx).reshape(ny,nx)*miss_int, int32)
          a2nextpos1.tofile(nextposname1)
        #----------






