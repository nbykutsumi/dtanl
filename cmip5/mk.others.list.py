from numpy import *

#---------------------------------------------
# set dnz, dny, dnx
#---------------------------------------------

dnx    = {}
dny    = {}
dnz    = {}
#
model = "NorESM1-M"
dnz.update({(model,"hus"):8, (model,"ta"):8, (model,"wap"):8, (model,"zg"):8, (model,"huss"):1, (model,"psl"):1, (model,"tas"):1, (model,"prc"):1, (model,"pr"):1, (model,"rhs"):1})
dny[model] = 96
dnx[model] = 144
#
model = "MIROC5"
dnz.update({(model,"hus"):8, (model,"ta"):8, (model,"wap"):8, (model,"zg"):8, (model,"huss"):1, (model,"psl"):1, (model,"tas"):1, (model,"prc"):1, (model,"pr"):1, (model,"rhs"):1})
dny[model] = 128
dnx[model] = 256
#
model = "CanESM2"
dnz.update({(model,"hus"):8, (model,"ta"):8, (model,"wap"):8, (model,"zg"):8, (model,"huss"):1, (model,"psl"):1, (model,"tas"):1, (model,"prc"):1, (model,"pr"):1, (model,"rhs"):1})
dny[model] = 64
dnx[model] = 128
#---------------------------------------------
tstp = "day"
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
xth  = 99.0
#xth  = 90.0
rmiss = -9999.0
g = 9.8
idir_root = "/media/disk2/data/CMIP5/bn"
lvar = ["tas", "huss", "rhs","psl", "zg", "wap"]
flag_fill = 1
#---------------------------------------------
iyear_his = dyrange["his"][0]
eyear_his = dyrange["his"][1]
iyear_fut = dyrange["fut"][0]
eyear_fut = dyrange["fut"][1]



for model in lmodel:
  #------------
  ny  = dny[model]
  nx  = dnx[model]

  #----------------------------------------------------
  # read lat, lon
  #---------------
  lalodir = "/media/disk2/data/CMIP5/bn/pr/day/%s/historical/%s"%(model, ens)
  
  latname = lalodir + "/lat.txt"
  lonname = lalodir + "/lon.txt"
  #---
  f = open(latname)
  llat = map(float, f.readlines())
  f.close()
  f = open(lonname)
  llon = map(float, f.readlines())
  f.close()
  #----------------------------------------------------
  #* dirs 
  #----------------------------------------------------
  epldir_his   = "/media/disk2/out/CMIP5/day/%s/%s/%s/wa.mean/%06.2f"%(model, dexpr["his"], ens, xth)
  epldir_fut   = "/media/disk2/out/CMIP5/day/%s/%s/%s/wa.mean/%06.2f"%(model, dexpr["fut"], ens, xth)
  cnddir_his   = "/media/disk2/out/CMIP5/day/%s/%s/%s/cnd.mean"%(model, dexpr["his"], ens)
  cnddir_fut   = "/media/disk2/out/CMIP5/day/%s/%s/%s/cnd.mean"%(model, dexpr["fut"], ens)
  
  date_his     = "%04d-%04d/%02d-%02d"%(iyear_his, eyear_his, imon, emon)
  date_fut     = "%04d-%04d/%02d-%02d"%(iyear_fut, eyear_fut, imon, emon)
  #----------------------------------------------------
  #* names of files
  #----------------------------------------------------
  sRH_his      = cnddir_his  + "/rhs/" + date_his + "/rhs_day_%s_%s_%s_%06.2f.bn"%(model, dexpr["his"], ens, xth)
  sRH_his      = cnddir_his  + "/rhs/" + date_his + "/rhs_day_%s_%s_%s_%06.2f.bn"%(model, dexpr["his"], ens, xth)
  stas_his     = cnddir_his  + "/tas/" + date_his + "/tas_day_%s_%s_%s_%06.2f.bn"%(model, dexpr["his"], ens, xth)
  shuss_his    = cnddir_his  + "/huss/"+ date_his + "/huss_day_%s_%s_%s_%06.2f.bn"%(model, dexpr["his"], ens, xth)
  splcl_his    = epldir_his  + "/plcl/epl.plcl.mean.%04d-%04d.bn"%(iyear_his, eyear_his)
  #----
  sRH_fut      = cnddir_fut  + "/rhs/" + date_fut + "/rhs_day_%s_%s_%s_%06.2f.bn"%(model, dexpr["fut"], ens, xth)
  stas_fut     = cnddir_fut  + "/tas/" + date_fut + "/tas_day_%s_%s_%s_%06.2f.bn"%(model, dexpr["fut"], ens, xth)
  shuss_fut    = cnddir_fut  + "/huss/"+ date_fut + "/huss_day_%s_%s_%s_%06.2f.bn"%(model, dexpr["fut"], ens, xth)
  splcl_fut    = epldir_fut  + "/plcl/epl.plcl.mean.%04d-%04d.bn"%(iyear_fut, eyear_fut)
  #----------------------------------------------------
  #* read files
  #----------------------------------------------------
  rh_his       = fromfile( sRH_his,   float32).reshape(ny, nx)
  tas_his      = fromfile( stas_his,  float32).reshape(ny, nx)
  huss_his     = fromfile( shuss_his, float32).reshape(ny, nx)
  plcl_his     = fromfile( splcl_his, float32).reshape(ny, nx)
  #---
  rh_fut       = fromfile( sRH_fut,   float32).reshape(ny, nx)
  tas_fut      = fromfile( stas_fut,  float32).reshape(ny, nx)
  huss_fut     = fromfile( shuss_fut, float32).reshape(ny, nx)
  plcl_fut     = fromfile( splcl_fut, float32).reshape(ny, nx)
  #----------------------------------------------------
  # frac.change
  #---------------
  frac_rh      = 100.0 * (rh_fut   - rh_his)   / rh_his
  frac_tas     = 100.0 * (tas_fut  - tas_his)  / tas_his
  frac_huss    = 100.0 * (huss_fut - huss_his) / huss_his
  frac_plcl    = 100.0 * (plcl_fut - plcl_his) / plcl_his
  #-----------------------------------------------------

  sout   = "i, lat, Tsfc, RHsfc, qsfc, Plcl\n"
  for i in range(ny):
    ilat = llat[i]
    rh   = frac_rh[i].mean()
    tas  = frac_tas[i].mean()
    huss = frac_huss[i].mean()
    plcl = frac_plcl[i].mean()
    sout = sout + "%s,%s,%s,%s,%s,%s\n"%(i, ilat, tas, rh, huss, plcl)
  #-----------------------------------------------------
  zonaldir = "/media/disk2/out/CMIP5/day/%s/scales/r1i1p1/his.m.fut.m/zonal"%(model)
  soname   = zonaldir + "/epl.others.day_%s_%s_%06.2f.csv"%(model, ens, xth)
  #---------
  f = open(soname, "w")
  f.write(sout)
  f.close()
  print soname
