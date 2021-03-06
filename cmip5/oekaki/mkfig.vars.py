import os
from numpy import *
#----------------------------------------------------
tstp = "day"
model = "NorESM1-M"
ens  = "r1i1p1"
lexpr = ["historical", "rcp85"]
dlyrange={"historical":[1990,1999], "rcp85":[2086,2095]}
lvar = ["pr"]
xth = 0.0
#xth  = 99.0
season = "DJF"
cmd = "/home/utsumi/oekaki/dtanl/cmip/dtanl.gmt"
ny = 96
nx = 144
#####################################################
if season == "ALL":
  (imon, emon) = (1, 12)
elif season == "DJF":
  (imon, emon) = (12, 2)

#####################################################
# functions
#####################################################
def mk_dir_tail(var, tstp, model, expr, ens):
  odir_tail = var + "/" + tstp + "/" +model + "/" + expr +"/"\
       +ens
  return odir_tail
#####################################################
def mk_namehead(var, tstp, model, expr, ens):
  namehead = var + "_" + tstp + "_" +model + "_" + expr +"_"\
       +ens
  return namehead
#####################################################
def checkfile(sname):
  if not (os.access(sname, os.F_OK)):
    print "nofile:", sname
    sys.exit()
#----------------------------------------------------
#####################################################
# scalestep
#-------------------------------
dscalestep={}
dscalestep["rhs"] = 10.0
dscalestep["pr"] = 5.0
#***********************************************
# cpt
#-------------------------------
cptdir        = "/home/utsumi/bin/dtanl/cmip5/oekaki/cpt"
dcpt          = {}
dcpt["rhs"]   = cptdir + "/rainbow.20.100.cpt"
dcpt["pr"]    = cptdir + "/rainbow.20.100.cpt"
#-----------------------------------------------
dcoef        = {}
dcoef["rhs"] = 1.0
dcoef["pr"]  = 60.0*60.0*24.0

#***********************************************
# overscale
#-------------------------------
doverscale        = {}
doverscale["rhs"] = 0
doverscale["pr"] = 1
#-------------------------------
for var in lvar:
  didir  = {}
  diname = {}
  dodir  = {}
  doname = {}
  dotitle= {}
  for expr in lexpr:
  #for expr in ["historical"]:
    #-----------------------
    lyrange = dlyrange[expr]
    iyear = lyrange[0]
    eyear = lyrange[1]
    #-----------------------
    didir[expr]  = '/media/disk2/out/CMIP5/%s/%s/%s/%s/cnd.mean/%s/%04d-%04d/%02d-%02d'%(tstp, model, expr, ens, var, iyear, eyear, imon, emon) 
    diname[expr] = didir[expr] + "/%s_%s_%s_%s_%s_%06.2f.bn"\
                   %(var, tstp, model, expr, ens, xth)
    dodir[expr]  = didir[expr]
    doname[expr] = didir[expr] + "/%s_%s_%s_%s_%s_%06.2f"\
                   %(var, tstp, model, expr, ens, xth)
    dotitle[expr]= "%s_%04d-%04d"%(var, iyear, eyear)
    checkfile(diname[expr])
    #-----------------------
    siname = diname[expr]
    scpt   = dcpt[var]
    soname = doname[expr]
    sotitle= dotitle[expr]
    sscalestep = dscalestep[var]
    overscale  = doverscale[var]
    print "-------------------------"
    print siname
    print scpt
    print soname
    print sscalestep
    print "-------------------------"
    #--------------------------------
    # change unit and make temporary file
    #--------------------------------
    atemp = fromfile(siname, float32)
    atemp = atemp * dcoef[var]
    siname_temp = siname + "temp"
    atemp.tofile(siname_temp)
    #--------------------------------
    os.system("%s %s %s %s %s %s %s"\
         %(cmd, siname_temp, scpt, soname, sotitle, sscalestep, overscale))
    os.remove(siname_temp)
#******************************************************
# differece file
#******************************************************
# scalestep
#-------------
dscalestep    = {}
dscalestep["rhs","dif"]  = 2
dscalestep["rhs","frac"] = 0.05
dscalestep["pr" ,"dif"]  = 0.5
dscalestep["pr" ,"frac"] = 0.2
#-------------
# overscale
#-------------
doverscale    = {}
doverscale["rhs","dif"]  = 1
doverscale["rhs","frac"] = 1
doverscale["pr", "dif"]  = 1
doverscale["pr", "frac"] = 1
#-------------
# title
#-------------
dotitle        = {}
for var in lvar:
  dotitle[var,"dif"]  = "chng_%s"%(var)
  dotitle[var,"frac"] = "frac_%s"%(var)
#-------------
# set cpt
#-------------
dcpt          = {}
dcpt["rhs","dif"]    = cptdir + "/polar.-10.10.cpt" 
dcpt["rhs","frac"]   = cptdir + "/polar.-0.2.0.2.cpt" 
#
dcpt["pr","dif"]    = cptdir + "/polar.-3.3.cpt" 
dcpt["pr","frac"]   = cptdir + "/polar.-1.1.cpt" 
#-------------
# years
#-------------
iyear1 = dlyrange["historical"][0]
eyear1 = dlyrange["historical"][1]
iyear2 = dlyrange["rcp85"][0]
eyear2 = dlyrange["rcp85"][1]
#-------------
# set names
#-------------
for var in lvar:
  didir["dif"]  = "/media/disk2/out/CMIP5/%s/%s/dif/%s/%04d-%04d.%04d-%04d/%02d-%02d"\
                 %(tstp, model, expr, iyear1, eyear1, iyear2, eyear2, imon, emon)
  diname[var,"dif"] = didir["dif"] + "/chng.%s_%s_%s_%s_%s_%06.2f.bn"\
                 %(var, tstp, model, expr, ens, xth)
  doname[var,"dif"] = didir["dif"] + "/chng.%s_%s_%s_%s_%s_%06.2f"\
                 %(var, tstp, model, expr, ens, xth)
  diname[var,"frac"] = didir["dif"] + "/frac.chng.%s_%s_%s_%s_%s_%06.2f.bn"\
                 %(var, tstp, model, expr, ens, xth)
  doname[var,"frac"] = didir["dif"] + "/frac.chng.%s_%s_%s_%s_%s_%06.2f"\
                 %(var, tstp, model, expr, ens, xth)
  ##-------------
  ## read files
  ##-------------
  #a1   = fromfile(diname["historical"], float32).reshape(ny, nx)
  #a2   = fromfile(diname["rcp85"], float32).reshape(ny, nx)
  #adif = a2 - a1
  #afrac= (a2 - a1) / a1
  ##-------------
  ## make input file for gmt
  ##-------------
  #adif.tofile(diname[var, "dif"])
  #afrac.tofile(diname[var, "frac"])
  #print doname[var, "dif"]
  #--------------------------------
  # change unit and make temporary file
  #--------------------------------
  diname_temp = {}
  for stype in ["dif", "frac"]:
    #-----------------
    if (stype == "dif"):
      coef = dcoef[var]
    elif (stype == "frac"):
      coef = 1.0
    #-----------------
    atemp = fromfile(diname[var, stype], float32)
    atemp = atemp * coef
    diname_temp[var, stype] = diname[var, stype] + "temp"
    atemp.tofile(diname_temp[var, stype])
  #--------------------------------
  #****************
  # GMT
  #****************
  # set variables
  #-------------
  for stype in ["dif", "frac"]:
    siname     = diname_temp[var, stype]
    scpt       = dcpt[var, stype]
    soname     = doname[var, stype]
    sotitle    = dotitle[var, stype] 
    sscalestep = dscalestep[var, stype]
    overscale  = doverscale[var, stype]
    #-------------
    os.system("%s %s %s %s %s %s %s"\
        %(cmd, siname, scpt, soname, sotitle, sscalestep, overscale))
    #
    os.remove(siname)

