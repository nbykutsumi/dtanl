import ctrack
from numpy import *
from ctrack_func import fortpos2pyxy
import calendar
import datetime
import os, sys
##***************************
#--------------------------------------------------
thdp    = 30.0  # [Pa]
thdist  = 300.0*1000.0  # [m]
###################
# set dnz, dny, dnx
###################
dnx    = {}
dny    = {}
dnz    = {}
#
model = "NorESM1-M"
dnz.update({(model,"psl"):1, (model,"ua"):1, (model,"va"):1, (model,"hus"):8, (model,"ta"):8, (model,"wap"):8, (model,"zg"):8, (model,"huss"):1, (model,"psl"):1, (model,"tas"):1, (model,"prc"):1, (model,"pr"):1, (model,"rhs"):1})
dny[model] = 96
dnx[model] = 144
#
model = "MIROC5"
dnz.update({(model,"psl"):1, (model,"ua"):1, (model,"va"):1, (model,"hus"):8, (model,"ta"):8, (model,"wap"):8, (model,"zg"):8, (model,"huss"):1, (model,"psl"):1, (model,"tas"):1, (model,"prc"):1, (model,"pr"):1, (model,"rhs"):1})
dny[model] = 128
dnx[model] = 256
#
model = "CanESM2"
dnz.update({(model,"psl"):1, (model,"ua"):1, (model,"va"):1, (model,"hus"):8, (model,"ta"):8, (model,"wap"):8, (model,"zg"):8, (model,"huss"):1, (model,"psl"):1, (model,"tas"):1, (model,"prc"):1, (model,"pr"):1, (model,"rhs"):1})
dny[model] = 64
dnx[model] = 128
#####################################################
tstp  = "6hr"
dhinc = { "6hr":6 }
hinc  = dhinc[tstp]
dendh = { "6hr":18}
endh  = dendh[tstp]
#lmodel = ["NorESM1-M", "MIROC5","CanESM2"]
#lmodel = ["MIROC5", "CanESM2"]
#lmodel = ["MIROC5"]
lmodel = ["NorESM1-M"]
dexpr={}
dexpr["his"] = "historical"
dexpr["fut"] = "rcp85"
ens = "r1i1p1"
dyrange={}
dyrange["his"] = [1990, 1999]
dyrange["fut"] = [2086, 2095]
imon = 1
emon =12
miss_dbl  = -9999.0
miss_int = -9999
#####################################################
# functions
#####################################################
def xy2fortpos(ix, iy, nx):
  number = iy* nx + ix +1
  return number
#####################################################
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
#################################################
def mk_dir_tail(var, tstp, model, expr, ens):
  odir_tail = var + "/" + tstp + "/" +model + "/" + expr +"/"\
       +ens
  return odir_tail
#####################################################
def mk_namehead(var, tstp, model, expr, ens):
  namehead = var + "_" + tstp + "_" +model + "_" + expr +"_"\
       +ens
  return namehead
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
psldir_root     = "/media/disk2/data/CMIP5/bn/psl/%s"%(tstp)
pmeandir_root   = "/media/disk2/out/CMIP5/%s"%(tstp)
winddir_root    = "/media/disk2/out/CMIP5/day"
axisdir_root    = psldir_root
#
lastposdir_root  = "/media/disk2/out/CMIP5/%s"%(tstp)
pmindir_root    = "/media/disk2/out/CMIP5/%s"%(tstp)
iposdir_root    = "/media/disk2/out/CMIP5/%s"%(tstp)
idatedir_root   = "/media/disk2/out/CMIP5/%s"%(tstp)
timedir_root    = "/media/disk2/out/CMIP5/%s"%(tstp)
lifedir_root    = "/media/disk2/out/CMIP5/%s"%(tstp)
nextposdir_root = "/media/disk2/out/CMIP5/%s"%(tstp)
#****************************************************

for model in lmodel:
  #----------------------------------------------------
  ny = dny[model]
  nx = dnx[model]
  #****************************************************
  #for exprtype in ["his", "fut"]:
  for exprtype in ["his"]:
    expr = dexpr[exprtype]
    lyrange = dyrange[exprtype]
    iyear   = lyrange[0]
    eyear   = lyrange[1]
    #**************************************************
    # read lat, lon data
    #----------------------
    axisdir    = axisdir_root  + "/%s/%s/%s"%(model, expr, ens)
    latname    = axisdir  + "/lat.txt"
    lonname    = axisdir  + "/lon.txt"
    a1lat      = read_txtlist(latname)
    a1lon      = read_txtlist(lonname) 
    #**************************************************
    #**************************************************
    counter = 0
    iyear = 1990
    eyear = 1990
    imon  = 1
    emon  = 1
    for year in range(iyear, eyear+1):
    #for year in range(1990, 1990+1):
      #---------
      # dirs
      #---------
      for mon in range(imon, emon+1):
      #for mon in range(1, 1+1):
        ##############
        # no leap
        ##############
        if (mon==2)&(calendar.isleap(year)):
          ed = calendar.monthrange(year,mon)[1] -1
        else:
          ed = calendar.monthrange(year,mon)[1]
        ##############
        for day in range(1, ed+1):
        #for day in range(1, 1+1):
          for hour in range(0, endh+1, hinc):
            counter = counter + 1
            print "time1=",year, mon, day, hour
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
            #***************************************
            #* names for 0
            #---------------------------------------
            #   DIRS 
            #**********
            psldir0     = psldir_root     + "/%s/%s/%s/%04d"%(model,expr,ens, year0)
            pmeandir0   = pmeandir_root   + "/%s/%s/%s/pmean/%04d"%(model, expr, ens, year0)
            uadir0      = winddir_root    + "/%s/%s/%s/run.mean/ua/%04d"%(model, expr, ens, year0)
            vadir0      = winddir_root    + "/%s/%s/%s/run.mean/va/%04d"%(model, expr, ens, year0)
            #
            lastposdir0 = lastposdir_root + "/%s/%s/%s/lastpos/%04d"%(model, expr, ens, year0)
            pmindir0    = pmindir_root    + "/%s/%s/%s/pmin/%04d"%(model, expr, ens, year0)
            iposdir0    = iposdir_root    + "/%s/%s/%s/ipos/%04d"%(model, expr, ens, year0)
            idatedir0   = idatedir_root   + "/%s/%s/%s/idate/%04d"%(model, expr, ens, year0)
            timedir0       = timedir_root    + "/%s/%s/%s/time/%04d"%(model, expr, ens, year0)

            #----------
            #   names
            #**********
            pslname0    = psldir0   + "/psl_%sPlev_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh0)
            pmeanname0  = pmeandir0 + "/pmean_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh0)
            uaname0     = uadir0    + "/run.mean.700hPa.ua_day_%s_%s_%s_%s.bn"%(model, expr, ens, stimed0)
            vaname0     = vadir0    + "/run.mean.700hPa.va_day_%s_%s_%s_%s.bn"%(model, expr, ens, stimed0)
            #
            lastposname0 = lastposdir0     + "/lastpos_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh0) 
            pminname0    = pmindir0        + "/pmin_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh0) 
            iposname0    = iposdir0        + "/ipos_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh0)
            idatename0   = idatedir0       + "/idate_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh0)
            timename0    = timedir0           + "/time_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh0)
            #
            mk_dir(lastposdir0)
            mk_dir(pmindir0)
            mk_dir(iposdir0)
            mk_dir(iposdir0)
            mk_dir(idatedir0)
            mk_dir(timedir0)
            #***************************************
            #* names for 1
            #---------------------------------------
            #    DIRS
            #***********
            psldir1     = psldir_root      + "/%s/%s/%s/%04d"%(model,expr,ens, year)
            pmeandir1   = pmeandir_root    + "/%s/%s/%s/pmean/%04d"%(model, expr, ens, year)
            #
            lastposdir1 = lastposdir_root  + "/%s/%s/%s/lastpos/%04d"%(model, expr, ens, year1)
            pmindir1    = pmindir_root     + "/%s/%s/%s/pmin/%04d"%(model, expr, ens, year1)
            iposdir1    = iposdir_root     + "/%s/%s/%s/ipos/%04d"%(model, expr, ens, year1)
            idatedir1   = idatedir_root    + "/%s/%s/%s/idate/%04d"%(model, expr, ens, year1)
            timedir1    = timedir_root     + "/%s/%s/%s/time/%04d"%(model, expr, ens, year1)
            #------
            mk_dir(lastposdir1)
            mk_dir(pmindir1)
            mk_dir(iposdir1)
            mk_dir(iposdir1)
            mk_dir(idatedir1)
            mk_dir(timedir1)
            #----------
            #   names
            #**********
            pslname1   = psldir1           + "/psl_%sPlev_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh1)
            pmeanname1 = pmeandir1         + "/pmean_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh1)
            #
            lastposname1 = lastposdir1     + "/lastpos_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh1) 
            pminname1    = pmindir1        + "/pmin_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh1) 
            iposname1    = iposdir1        + "/ipos_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh1)
            idatename1   = idatedir1       + "/idate_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh1)
            timename1    = timedir1        + "/time_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh1)
            #***************************************
            # read data
            #---------------------------------------
            #   for 0
            #************
            if ( os.access(iposname0, os.F_OK) ):
              a2pmean0   = fromfile(pmeanname0,   float32).reshape(ny, nx)
              a2psl0     = fromfile(pslname0,     float32).reshape(ny, nx)
              a2ua0      = fromfile(uaname0,      float32).reshape(ny, nx)
              a2va0      = fromfile(vaname0,      float32).reshape(ny, nx)
              #--
              a2lastpos0 = fromfile(lastposname0, int32).reshape(ny, nx)
              a2pmin0    = fromfile(pminname0,    float32).reshape(ny, nx)
              a2ipos0    = fromfile(iposname0,    int32).reshape(ny, nx)
              a2idate0   = fromfile(idatename0,   int32).reshape(ny, nx)
              a2time0    = fromfile(timename0,    int32).reshape(ny, nx)
            elif ( counter == 1):
              a2pmean0   = array(ones(ny*nx).reshape(ny,nx)*miss_dbl, float32)
              a2psl0     = array(ones(ny*nx).reshape(ny,nx)*miss_dbl, float32)
              a2ua0      = array(zeros(ny*nx).reshape(ny,nx), float32)
              a2va0      = array(zeros(ny*nx).reshape(ny,nx), float32)
              #--
              a2lastpos0 = array(ones(ny*nx).reshape(ny,nx)*miss_int, int32)
              a2pmin0    = array(ones(ny*nx).reshape(ny,nx)*miss_dbl, float32)
              a2ipos0    = array(ones(ny*nx).reshape(ny,nx)*miss_int, int32)
              a2idate0   = array(ones(ny*nx).reshape(ny,nx)*miss_int, int32)
              a2time0    = array(ones(ny*nx).reshape(ny,nx)*miss_int, int32)
            else:
              print "nofiles: stimeh0 = ",stimeh0
              sys.exit()
            #------------
            #   for 1
            #************
            a2pmean1     = fromfile(pmeanname1, float32).reshape(ny, nx)
            a2psl1       = fromfile(pslname1,   float32).reshape(ny, nx)
            #****************************************
            # connectc
            ##***************************************
            ctrackout = ctrack.ctrack.connectc(\
               a2pmean0.T, a2pmean1.T, a2psl0.T, a2psl1.T, a2ua0.T, a2va0.T\
               , a2pmin0.T, a2ipos0.T, a2idate0.T, a2time0.T\
               , a1lon, a1lat, thdp, thdist, hinc, miss_dbl, miss_int\
               , year1, mon1, day1, hour1\
               )
            a2lastpos1 = array(ctrackout[0].T, int32)
            a2pmin1    = array(ctrackout[1].T, float32)
            a2ipos1    = array(ctrackout[2].T, int32)
            a2idate1   = array(ctrackout[3].T, int32)
            a2time1    = array(ctrackout[4].T, int32)
            #****************************************
            # write to file
            #----------------------------------------
            a2lastpos1.tofile(lastposname1)
            a2pmin1.tofile(pminname1)
            a2ipos1.tofile(iposname1)
            a2idate1.tofile(idatename1)
            a2time1.tofile(timename1)
            #*****************************************

            #for iy1 in range(0, ny):
            #  for ix1 in range(0, nx):
            #    psl1     = a2psl1[iy1, ix1]
            #    pmin1    = a2pmin1[iy1, ix1]
            #    ipos1    = a2ipos1[iy1, ix1]
            #    idate1   = a2idate1[iy1, ix1]
            #    time1    = a2time1[iy1, ix1]
            #    lastpos1 = a2lastpos1[iy1, ix1]
            #    (ix0, iy0) = fortpos2pyxy( lastpos1, nx, miss_int)
            #    if (ix0 != miss_int):
            #      psl0   = a2psl0[iy0, ix0]
            #      pmin0  = a2pmin0[iy0, ix0]
            #      time0  = a2time0[iy0, ix0]
            #      ipos0  = a2ipos0[iy0, ix0]
            #      idate0 = a2idate0[iy0, ix0]
            #      if (  (ipos1 == 610) and (idate1 == 1990010100) ):
            #        print timename1
            #        print "0, ix0, iy0, ipos0, idate0, time0", ix0, iy0, ipos0, idate0, time0, "pmin0",pmin0, "psl0", psl0
            #        print "1, ix1, iy1, ipos1, idate1, time1", ix1, iy1, ipos1, idate1, time1, "pmin1",pmin1, "psl1", psl1
            #        print "pmin0 - pmin1=", pmin0 - pmin1
            #        print "psl1 - pmin1=", psl1 - pmin1
    #*************************************************
    counter = 0
    for year in range(eyear, iyear -1, -1):
      for mon in range(emon, imon -1, -1):
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
            print stimeh1
            #***************************************
            #* names for 1
            #---------------------------------------
            #    DIRS
            #***********
            lastposdir1 = lastposdir_root  + "/%s/%s/%s/lastpos/%04d"%(model, expr, ens, year1)
            pmindir1    = pmindir_root     + "/%s/%s/%s/pmin/%04d"%(model, expr, ens, year1)
            iposdir1    = iposdir_root     + "/%s/%s/%s/ipos/%04d"%(model, expr, ens, year1)
            idatedir1   = idatedir_root    + "/%s/%s/%s/idate/%04d"%(model, expr, ens, year1)
            timedir1    = timedir_root     + "/%s/%s/%s/time/%04d"%(model, expr, ens, year1)
            #----------
            #   names
            #**********
            lastposname1 = lastposdir1     + "/lastpos_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh1) 
            pminname1    = pmindir1        + "/pmin_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh1) 
            iposname1    = iposdir1        + "/ipos_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh1)
            idatename1   = idatedir1       + "/idate_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh1)
            timename1    = timedir1        + "/time_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh1)
            #----------
            # read data
            #**********
            a2lastpos1   = fromfile(lastposname1, int32).reshape(ny,nx)
            a2pmin1      = fromfile(pminname1,  float32).reshape(ny,nx)
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
                  pmin1    = a2pmin1[iy1, ix1]
                  time1    = a2time1[iy1, ix1]
                  lifenext = a2lifenext[iy1, ix1]
                  (ix0,iy0) = fortpos2pyxy(a2lastpos1[iy1,ix1], nx, miss_int)
                  #---- 
                  if (lifenext == miss_int):
                    life1 = 10000 * int(pmin1) + time1
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
            lifedir1      = lifedir_root     + "/%s/%s/%s/life/%04d"%(model, expr, ens, year1)
            nextposdir0   = nextposdir_root      + "/%s/%s/%s/nextpos/%04d"%(model, expr, ens, year0)
            mk_dir(lifedir1)
            mk_dir(nextposdir0)
            #----------
            # out name
            #**********
            lifename1     = lifedir1          + "/life_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh1)
            nextposname0  = nextposdir0       + "/nextpos_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh0)

            #----------
            # write to file
            #**********
            a2life1.tofile(lifename1)
            a2nextpos0.tofile(nextposname0) 
            #----------
            # "nextpos" for last time
            #**********
            if counter == 1:
              nextposdir1   = nextposdir_root + "/%s/%s/%s/nextpos/%04d"%(model, expr, ens, year1)
              nextposname1  = nextposdir1     + "/nextpos_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh1)
              a2nextpos1    = array(ones(ny*nx).reshape(ny,nx)*miss_int, int32)
              a2nextpos1.tofile(nextposname1)
            #----------






