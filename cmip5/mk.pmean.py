from ctrack import *
from numpy import *
import calendar
import os
#--------------------------------------------------
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
emon = 12
miss_in  = 1.0e+20
miss_out = -9999.0
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
#****************************************************
# dir_root
#---------------
psldir_root   = "/media/disk2/data/CMIP5/bn/psl/%s"%(tstp)
pmeandir_root = "/media/disk2/out/CMIP5/%s"%(tstp)
#****************************************************

for model in lmodel:
  #----------------------------------------------------
  ny = dny[model]
  nx = dnx[model]
  #****************************************************
  for exprtype in ["his", "fut"]:
    expr = dexpr[exprtype]
    lyrange = dyrange[exprtype]
    iyear   = lyrange[0]
    eyear   = lyrange[1]
    #**************************************************
    for year in range(iyear, eyear+1):
      #---------
      # dirs
      #---------
      psldir   = psldir_root   + "/%s/%s/%s/%04d"%(model,expr,ens, year)
      pmeandir = pmeandir_root + "/%s/%s/%s/pmean/%04d"%(model, expr, ens, year)
      mk_dir(pmeandir)
      print pmeandir
      #---------
      for mon in range(imon, emon+1):
        ##############
        # no leap
        ##############
        if (mon==2)&(calendar.isleap(year)):
          ed = calendar.monthrange(year,mon)[1] -1
        else:
          ed = calendar.monthrange(year,mon)[1]
        ##############
        for day in range(1, ed+1):
          for hour in range(0, 23+1, hinc):
            stimeh  = "%04d%02d%02d%02d"%(year,mon,day,hour)
            #***************************************
            #* names
            #---------------------------------------
            pslname   = psldir + "/psl_%sPlev_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
            check_file(pslname)
            pmeanname = pmeandir + "/pmean_%s_%s_%s_%s_%s.bn"%(tstp, model, expr, ens, stimeh)
            #***************************************
            #***************************************
            # make pmean
            #***************************************
            apsl   = fromfile(pslname,   float32).reshape(ny, nx)
            apmean = array(ctrack.findcyclone(apsl.T, miss_in, miss_out), float32)
            apmean = apmean.T
            apmean.tofile(pmeanname)
            pmeanname





 
