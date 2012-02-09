from numpy import *
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
def solvelife(number):
  pmin = int(number / 10000)
  dura = number - pmin *10000
  return (pmin, dura)
#####################################################
def fortpos2xy(number, nx, miss_int):
  if (number == miss_int):
    iy0 = miss_int
    ix0 = miss_int
  else:
    iy0 = int(number/nx)         # iy0 = 0, 1, 2, ..
    ix0 = number - nx*iy0 -1     # ix0 = 0, 1, 2, ..
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
nextposdir_root = "/media/disk2/out/CMIP5/%s"%(tstp)
lastposdir_root = "/media/disk2/out/CMIP5/%s"%(tstp)
pmindir_root    = "/media/disk2/out/CMIP5/%s"%(tstp)
iposdir_root    = "/media/disk2/out/CMIP5/%s"%(tstp)
idatedir_root   = "/media/disk2/out/CMIP5/%s"%(tstp)
timedir_root    = "/media/disk2/out/CMIP5/%s"%(tstp)
lifedir_root    = "/media/disk2/out/CMIP5/%s"%(tstp)
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
    foundflag = 0
    counter = 0
    iyear = 1990
    eyear = 1990
    imon  = 1
    emon  = 1
    a2trace = array(ones(ny*nx) * miss_int, float32).reshape(ny, nx)
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
            #print "time1=",year, mon, day, hour
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
            #* names for 
            #---------------------------------------
            #   DIRS
            #**********
            psldir1       = psldir_root     + "/%s/%s/%s/%04d"%(model,expr,ens, year1)
            lifedir1      = lifedir_root    + "/%s/%s/%s/life/%04d"%(model, expr, ens, year1)
            iposdir1      = lifedir_root    + "/%s/%s/%s/ipos/%04d"%(model, expr, ens, year1)
            idatedir1     = lifedir_root    + "/%s/%s/%s/idate/%04d"%(model, expr, ens, year1)
            nextposdir1   = nextposdir_root + "/%s/%s/%s/nextpos/%04d"%(model, expr, ens, year1) 
            #----------
            #   name
            #**********
            pslname1     = psldir1           + "/psl_%sPlev_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh1)
            lifename1    = lifedir1          + "/life_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh1)
            iposname1    = iposdir1          + "/ipos_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh1)
            idatename1   = idatedir1         + "/idate_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh1)
            nextposname1  = nextposdir1      + "/nextpos_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh1) 
            #***************************************
            #   read
            #---------------------------------------
            a2psl1       = fromfile(pslname1,   float32).reshape(ny, nx)
            a2life1      = fromfile(lifename1,   int32).reshape(ny, nx)
            a2ipos1      = fromfile(iposname1,    int32).reshape(ny, nx)
            a2idate1     = fromfile(idatename1,   int32).reshape(ny, nx)
            a2nextpos1   = fromfile(nextposname1, int32).reshape(ny, nx)
            #---------------------------------------
            ipos_t  = 610
            idate_t = 1990010100

            #if (foundflag == 0):
            for iy in range(0, ny):
              for ix in range(0, nx):
                psl1     = a2psl1[iy, ix]
                life1    = a2life1[iy, ix]
                (pmin1, dura1) = solvelife(life1)
                life1    = a2life1[iy, ix]
                ipos1    = a2ipos1[iy, ix]
                idate1   = a2idate1[iy, ix]
                nextpos1 = a2nextpos1[iy, ix]
                (ixnext, iynext) = fortpos2xy(nextpos1, nx, miss_int)
                foundflag = foundflag +1
                if ( (ipos1 == 610) and (idate1 == 1990010100) ):
                  print year, mon, day, hour,"yx", iy, ix, "yxnext",iynext, ixnext, "dura", dura1, "pmin", pmin1, "psl", psl1
                  a2trace[iy,ix] = psl1 
             
                  



                

