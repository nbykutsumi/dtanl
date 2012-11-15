from numpy import *
import os, sys
import calendar
import datetime
#******************************************************
idir_root = "/media/disk2/data/CMIP5/sa.one"
#******************************************************
lvar   = ["va","ua"]
#tstp   = "day"
tstp   = "day"
lmodel = ["MIROC5"]
#lexpr  = ["historical", "rcp85"]
lexpr  = ["historical"]
ens    = "r1i1p1"
dw     = 7
#-----
plev   = 500

nx     = 360
ny     = 180
#******************************************************
# set dlyrange
#******************************************************
dlyrange     = {}
#
#dlyrange["NorESM1-M", "historical"]  = [[1980,1989],[1990,1999]]
dlyrange["NorESM1-M", "historical"]  = [1980,2005]
dlyrange["NorESM1-M", "rcp85"]       = [2076,2100]
#
dlyrange["MIROC5", "historical"]  = [1980,2005]
dlyrange["MIROC5", "rcp85"]       = [2080,2099]
#
dlyrange["CanESM2", "historical"]  = [1979,2005]
dlyrange["CanESM2", "rcp85"]       = [2081,2100]

#******************************************************
dnz    = {}
#
model = "NorESM1-M"
dnz.update({ (model, "ua"):8, (model, "va"):8, (model,"hur"):8, (model,"ta"):8, (model,"wap"):8, (model,"zg"):8, (model,"huss"):1, (model,"psl"):1, (model,"tas"):1, (model,"prc"):1, (model,"pr"):1, (model,"rhs"):1})
#
model = "MIROC5"
dnz.update({ (model, "ua"):8, (model, "va"):8, (model,"hur"):8, (model,"ta"):8, (model,"wap"):8, (model,"zg"):8, (model,"huss"):1, (model,"psl"):1, (model,"tas"):1, (model,"prc"):1, (model,"pr"):1, (model,"rhs"):1})
#
model = "CanESM2"
dnz.update({ (model, "ua"):8, (model, "va"):8, (model,"hur"):8, (model,"ta"):8, (model,"wap"):8, (model,"zg"):8, (model,"huss"):1, (model,"psl"):1, (model,"tas"):1, (model,"prc"):1, (model,"pr"):1, (model,"rhs"):1})
#****************************************************
imon = 1
emon = 12
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
for model in lmodel:
  for expr in lexpr:
    for var in lvar:
      #------------------------------
      nz = dnz[model, var]
      #------------------------------
   
      odir_root = "/media/disk2/out/CMIP5/sa.one/%s/%s/%s/%s/run.mean"%(tstp, model, expr, ens)
      #------------------------------
      # make heads and tails
      #------------------------------
      ihead     = var + "_" + tstp + "_" +model + "_" + expr +"_" + ens
      ohead     = ihead
      idir_tail = var + "/" + tstp + "/" +model + "/" + expr +"/" + ens
      odir_tail = var + "/" 
      #------------------------------
      lyrange = dlyrange[model, expr]
      y0 = lyrange[0]
      y1 = lyrange[1]
      for year in range(y0, y1+1):
      #for year in range(1981, 1981+1):
        #****
        itimerange = "%04d0101-%04d1231"%(y0,y1)
        #****
        odir       = odir_root + "/" + odir_tail + "/%04d"%(year)
        mk_dir(odir)
        #****
        for  mon in range(imon, emon + 1):
          #*************
          # no leap
          #*************
          if (mon==2)&(calendar.isleap(year)):
            ed = calendar.monthrange(year,mon)[1] -1
          else:
            ed = calendar.monthrange(year,mon)[1]
          #*************
          for day in range(1, ed + 1):
            stime  = "%04d%02d%02d%02d"%(year,mon,day,0)
            #***********
            oname  = odir + "/run.mean.%s_%s.%04dPa.sa.one"%(ihead, stime, plev)
            #*********************
            # start running mean
            #*********************
            # dummy
            #********
            aout  = zeros(ny*nx)
            aout  = array( aout , float32)
            ndays = 0
            #********
            for daydelta in ldaydelta:
              ndays = ndays + 1
              target     = date_slide( year, mon, day, daydelta)
              targetyear = target.year
              targetmon  = target.month
              targetday  = target.day
              #-------------------
              idir       = idir_root + "/" + idir_tail + "/%04d"%(targetyear)
              stime      = "%04d%02d%02d%02d"%(targetyear, targetmon, targetday, 0)
              iname  = idir + "/%s_%s.%04dPa.sa.one"%(ihead, stime, plev)
              if not os.access(iname, os.F_OK):
                print "no file", iname
                ndays = ndays - 1
                continue
              #--------------------
              # add 
              #--------------------
              ain   = fromfile(iname, float32)
              aout  = aout + ain
            #*****************
            aout    = aout / ndays
            #*****************
            print oname
            aout.tofile(oname)








