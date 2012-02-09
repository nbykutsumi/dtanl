from ctrack import *
from numpy import *
import calendar
import os
#--------------------------------------------------
thorog  = 1500.0 #[m]
thdp    = 30.0           #[Pa]
thdist  = 300.0*1000.0   #[m]
thdura  = 72             #[h]
thpgmax = 20*100       #[Pa/1000km]

miss_cmip  = 1.0e+20
miss_dbl = -9999.0
miss_int = -9999

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
endh  = int(dendh[tstp])
#lmodel = ["NorESM1-M", "MIROC5","CanESM2"]
#lmodel = ["MIROC5", "CanESM2"]
#lmodel = ["MIROC5"]
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
#****************************************************
#****************************************************
bindir    = "/home/utsumi/bin/dtanl/ctrack"
oekakidir = "/home/utsumi/bin/dtanl/ctrack/oekaki"
for model in lmodel:
  #----------------------------------------------------
  ny = dny[model]
  nx = dnx[model]
  #****************************************************
  #for exprtype in ["his", "fut"]:
  #for exprtype in ["fut"]:
  for exprtype in lexprtype:
    expr = dexpr[exprtype]
    lyrange = dyrange[exprtype]
    iyear   = lyrange[0]
    eyear   = lyrange[1]
    print expr, iyear, eyear
    ##**************************************************
    ##  call findcyclone   # pgrad is made too.
    ##------------------
    #cmd = bindir + "/findcyclone.py"
    #os.system("python %s %s %s %s %s %s %s %s %s %s %s %s %s %s"\
    #  %(cmd           \
    #  ,model          \
    #  ,expr           \
    #  ,ens            \
    #  ,tstp           \
    #  ,hinc           \
    #  ,iyear          \
    #  ,eyear          \
    #  ,imon           \
    #  ,emon           \
    #  ,nx             \
    #  ,ny             \
    #  ,miss_dbl       \
    #  ,thorog         \
    #  ))
    ##**************************************************
    ##  call connectc.py
    ##------------------
    #cmd = bindir + "/connectc.py"
    #os.system("python %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s"\
    #  %(cmd           \
    #  ,model          \
    #  ,expr           \
    #  ,ens            \
    #  ,tstp           \
    #  ,hinc           \
    #  ,iyear          \
    #  ,eyear          \
    #  ,imon           \
    #  ,emon           \
    #  ,nx             \
    #  ,ny             \
    #  ,miss_dbl       \
    #  ,miss_int       \
    #  ,endh           \
    #  ,thdp           \
    #  ,thdist         \
    #  ))
    #
    #**************************************************
    #  call cdens.py
    #------------------
   
    for season in lseason:
      #-----------------
      # names
      #*****************
      outdir          = "/media/disk2/out/CMIP5/6hr/%s/%s/%s/tracks/map"%(model, expr, ens)
      
      dens_area_name  = outdir + "/dens.area_%s_%s_%s_%s_%s.bn"%(season, tstp, model, expr, ens)
      track_name      = outdir + "/track.grid_%s_%s_%s_%s_%s.bn"%(season, tstp, model, expr, ens)
      #-----------------
      cmd = bindir + "/cdens.py"
      os.system("python %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s"\
        %(cmd           \
        ,model          \
        ,expr           \
        ,ens            \
        ,tstp           \
        ,hinc           \
        ,iyear          \
        ,eyear          \
        ,season         \
        ,nx             \
        ,ny             \
        ,miss_dbl       \
        ,miss_int       \
        ,endh           \
        ,thdura         \
        ,thpgmax         \
        ,dens_area_name \
        ,track_name     \
        ))
      #----------------
      # dens and track pict
      #****************
      # names
      #-------
      cptfile   = oekakidir + "/cpt/polar.-1.1.cpt"
      pngname   = track_name[:-3] + ".png"
      psfile    = track_name[:-3] + ".ps"
      title     = "track"
      scalestep = 0.5
      overscale = 0
      #-------
      cmd = oekakidir + "/dens.gmt.py"
      os.system("python %s %s %s %s %s %s %s"%(\
         cmd
        ,track_name     \
        ,cptfile        \
        ,pngname        \
        ,title          \
        ,scalestep      \
        ,overscale      \
        ))
      print pngname
    #**************************************************
