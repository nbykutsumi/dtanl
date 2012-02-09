from numpy import *
import calendar, datetime
import os
import shutil
#-----------------------------------------------
lvar = ["pr"]

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
#lmodel = ["NorESM1-M", "MIROC5","CanESM2"]

lmodel = ["NorESM1-M"]
lexprtype = ["his", "fut"]
#lexprtype = ["fut"]
dexpr={}
dexpr["his"] = "historical"
dexpr["fut"] = "rcp85"
ens = "r1i1p1"
dyrange={}
dyrange["his"] = [1990, 1999]
dyrange["fut"] = [2086, 2095]
imon = 1
emon = 12
#lseason = ["DJF", "JJA","ALL"]
lseason = ["DJF"]
#####################################################
# functions
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
def time_slide(year, mon, day, hour, hourdelta):
  now         = datetime.datetime(year, mon, day, hour)
  target      = now + datetime.timedelta(hours = hourdelta)
  targetyear  = target.year
  #***********
  if ( calendar.isleap(targetyear) ):
    targetmonth = target.month
    targetday   = target.day
    if ( (targetmonth == 2) and (targetday == 29)):
      if (hourdelta < 0):
        target = target + datetime.timedelta(hours = -24)
      elif (hourdelta >0):
        target = target + datetime.timedelta(hours = 24)
  #-----------
  return target

#****************************************************
#****************************************************
#****************************************************
for model in lmodel:
  #----------------------------------------------------
  ny = dny[model]
  nx = dnx[model]
  #****************************************************
  for var in lvar:
    #**************************************************
    #for exprtype in ["his", "fut"]:
    #for exprtype in ["fut"]:
    for exprtype in lexprtype:
      expr = dexpr[exprtype]
      lyrange = dyrange[exprtype]
      iyear   = lyrange[0]
      eyear   = lyrange[1]
      print expr, iyear, eyear
      #*************************************************
      for year in range(iyear, eyear+1):
      #for year in range(1990, 1990+1):
        #---------
        # dirs
        #---------
        dir3h_root    =  "/media/disk2/data/CMIP5/bn/%s/3hr/%s/%s/%s"%(var, model, expr, ens)
        dir6h_root    =  "/media/disk2/data/CMIP5/bn/%s/6hr/%s/%s/%s"%(var, model, expr, ens)
        dir6h         =  dir6h_root + "/%04d"%(year)
        mk_dir(dir6h)
        #---------
        # descriptions
        #---------
        for descname in ["lat.txt","lon.txt","ncdump.txt","dims.txt",]:
          descfile_in = dir3h_root + "/%s"%(descname)
          descfile_out= dir6h_root + "/%s"%(descname)
          try:
            shutil.copyfile(descfile_in, descfile_out)
          except IOError:
            pass
        #--
        readme = dir6h_root + "/readme.txt"
        f=open(readme, "w")
        f.write("This data is made from 3-hourly data.")
        f.close()
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
            for hour in range(0, 18+1, 3):
              stime6h     = "%04d%02d%02d%02d"%(year, mon, day, hour)
              #------------
              time_pre    = time_slide(year, mon, day, hour, -2) 
              year_pre    = time_pre.year
              mon_pre     = time_pre.month
              day_pre     = time_pre.day
              hour_pre    = time_pre.hour
              #------------
              time_nxt    = time_slide(year, mon, day, hour, 1) 
              year_nxt    = time_nxt.year
              mon_nxt     = time_nxt.month
              day_nxt     = time_nxt.day
              hour_nxt    = time_nxt.hour
              #------------
              stime3h_pre = "%04d%02d%02d%02d30"%(year_pre, mon_pre, day_pre, hour_pre)
              stime3h_nxt = "%04d%02d%02d%02d30"%(year_nxt, mon_nxt, day_nxt, hour_nxt)
              #************************
              # file names for input
              #------------------------
              head3h = "%s_3hr_%s_%s_%s_"%(var, model, expr, ens)
              head6h = "%s_6hr_%s_%s_%s_"%(var, model, expr, ens)
              #--
              ifile3h_pre = dir3h_root + "/%04d/%s%s.bn"%(year_pre, head3h, stime3h_pre)
              ifile3h_nxt = dir3h_root + "/%04d/%s%s.bn"%(year_nxt, head3h, stime3h_nxt)
              #************************
              # file names for output
              #------------------------
              ofile6h     = dir6h_root + "/%04d/%s%s.bn"%(year, head6h, stime6h)
              #--------
              # check files
              exists_pre = os.access(ifile3h_pre, os.F_OK)
              exists_nxt = os.access(ifile3h_nxt, os.F_OK)
              print ofile6h
              #--
              if ( exists_pre and exists_nxt):
                ain_pre  = fromfile(ifile3h_pre, float32)
                ain_nxt  = fromfile(ifile3h_nxt, float32)
              elif ( (not exists_pre) and ( exists_nxt) ):
                ain_nxt  = fromfile(ifile3h_nxt, float32)
                ain_pre  = ain_nxt
              elif ( ( exists_pre) and ( not exists_nxt) ):
                ain_pre  = fromfile(ifile3h_pre, float32)
                ain_nxt  = ain_pre 
                print exists_pre
              #--
              aout  = (ain_pre + ain_nxt) /2.0
              aout.tofile(ofile6h)


   
