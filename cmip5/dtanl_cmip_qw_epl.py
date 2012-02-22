from dtanl_cmip_sbs import *
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
#####################################################
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
for model in lmodel:
  odir_root ="/media/disk2/out/CMIP5/%s/%s" %(tstp, model)
  #----------------------------------------------------
  ny = dny[model]
  nx = dnx[model]
  #----------------------------------------------------
  # read lev_f file
  #----------------------------------------------------
  slevdir_f = "/media/disk2/out/CMIP5/%s/%s/rcp85/%s/wa.mean"\
            %(tstp, model, ens)
  slev_f    = slevdir_f +"/lev_f.txt"
  check_file(slev_f)
  f         = open(slev_f, "r")
  llev_f    = map( lambda x: x.strip(),  f.readlines() )
  f.close()
  llev_f    = map( float, llev_f)
  nz_f      = len(llev_f)
  #****************************************************
  dir_his = odir_root + "/%s/%s/wa.mean/%06.2f"%(dexpr["his"], ens, xth)
  dir_fut = odir_root + "/%s/%s/wa.mean/%06.2f"%(dexpr["fut"], ens, xth)
  #****************************************************
  # make map dir
  #****************************************************
  casename = "his.m.fut.m"
  mapdir   = odir_root + "/scales/%s/%s/map"%(ens, casename)
  zonaldir = odir_root + "/scales/%s/%s/zonal"%(ens, casename)
  mk_dir(mapdir)
  mk_dir(zonaldir)
  #****************************************************
  # make dims
  #****************************************************
  dimsname = mapdir + "/dims.txt"
  sdims = "nz = %s\nny = %s\nnx = %s"%(nz_f, ny, nx)
  f=open(dimsname, "w")
  f.write(sdims)
  f.close()
  os.system("cp %s %s"%(slev_f, mapdir))
  #------
  axisdir = "/media/disk2/data/CMIP5/bn/zg/%s/%s/historical/%s"\
            %(tstp, model, ens)
  latname = axisdir + "/lat.txt"
  lonname = axisdir + "/lon.txt"
  os.system("cp %s %s"%(latname, mapdir))
  os.system("cp %s %s"%(lonname, mapdir))
  #****************************************************
  # read precip file
  #****************************************************
  iyear_his = dyrange["his"][0]
  eyear_his = dyrange["his"][1]
  iyear_fut = dyrange["fut"][0]
  eyear_fut = dyrange["fut"][1]
  dir_prxth_his = "/media/disk2/out/CMIP5/%s/%s/%s/%s/prxth/%04d-%04d/%02d-%02d"\
              %(tstp, model, dexpr["his"], ens, iyear_his, eyear_his, imon, emon)
  dir_prxth_fut = "/media/disk2/out/CMIP5/%s/%s/%s/%s/prxth/%04d-%04d/%02d-%02d"\
              %(tstp, model, dexpr["fut"], ens, iyear_fut, eyear_fut, imon, emon)
  #---
  spr_his  = dir_prxth_his + "/prxth_%s_%s_%s_%s_%06.2f.bn"%(tstp, model, dexpr["his"], ens, xth)
  spr_fut  = dir_prxth_fut + "/prxth_%s_%s_%s_%s_%06.2f.bn"%(tstp, model, dexpr["fut"], ens, xth)
  print spr_his
  print spr_fut
  #---
  a2pr_his  = fromfile(spr_his, float32).reshape(ny,nx)
  a2pr_fut  = fromfile(spr_fut, float32).reshape(ny,nx)
  a2dprec_frac   = (a2pr_fut - a2pr_his) / a2pr_his
  a2dprec_frac   = a2dprec_frac *100.0
  #----------------------------------------------------
  #* read mean file
  #----------------------------------------------------
  sdqdp_his    = dir_his + "/dqdp/epl.dqdp.mean.%04d-%04d.bn"%(iyear_his, eyear_his)
  swap_his     = dir_his + "/wap/epl.wap.mean.%04d-%04d.bn"%(iyear_his, eyear_his)
  splcl_his    = dir_his + "/plcl/epl.plcl.mean.%04d-%04d.bn"%(iyear_his, eyear_his)
  swaplcl_his  = dir_his + "/plcl/epl.waplcl.mean.%04d-%04d.bn"%(iyear_his, eyear_his)
  sdqdplcl_his = dir_his + "/plcl/epl.dqdplcl.mean.%04d-%04d.bn"%(iyear_his, eyear_his)
  #
  sdqdp_fut    = dir_fut + "/dqdp/epl.dqdp.mean.%04d-%04d.bn"%(iyear_fut, eyear_fut)
  swap_fut     = dir_fut + "/wap/epl.wap.mean.%04d-%04d.bn"%(iyear_fut, eyear_fut)
  splcl_fut    = dir_fut + "/plcl/epl.plcl.mean.%04d-%04d.bn"%(iyear_fut, eyear_fut)
  #swaplcl_fut  = dir_fut + "/plcl/epl.waplcl.mean.%04d-%04d.bn"%(iyear_fut, eyear_fut)
  #sdqdplcl_fut = dir_fut + "/plcl/epl.dqdplcl.mean.%04d-%04d.bn"%(iyear_fut, eyear_fut)
  #-----
  print model
  print nz_f, ny, nx
  print sdqdp_his
  a3dqdp_his    = array( fromfile(sdqdp_his, float32), float64).reshape(nz_f, ny, nx)
  a3wap_his     = array( fromfile(swap_his,  float32), float64).reshape(nz_f, ny, nx)
  a2plcl_his    = array( fromfile(splcl_his,  float32), float64).reshape(ny, nx)
  a2waplcl_his  = array( fromfile(swaplcl_his,  float32), float64).reshape(ny, nx)
  a2dqdplcl_his = array( fromfile(sdqdplcl_his,  float32), float64).reshape(ny, nx)
  #
  a3dqdp_fut    = array( fromfile(sdqdp_fut, float32), float64).reshape(nz_f, ny, nx)
  a3wap_fut     = array( fromfile(swap_fut,  float32), float64).reshape(nz_f, ny, nx)
  a2plcl_fut    = array( fromfile(splcl_fut,  float32), float64).reshape(ny, nx)
  #a2waplcl_fut  = array( fromfile(swaplcl_fut,  float32), float64).reshape(ny, nx)
  #a2dqdplcl_fut = array( fromfile(sdqdplcl_fut,  float32), float64).reshape(ny, nx)
  #----------------------------------------------------
  # dummy
  #----------------------------------------------------
  a3swa    = zeros(nz_f*ny*nx, dtype=float64).reshape(nz_f, ny, nx)
  a3sdwa   = zeros(nz_f*ny*nx, dtype=float64).reshape(nz_f, ny, nx)
  a3swda   = zeros(nz_f*ny*nx, dtype=float64).reshape(nz_f, ny, nx)
  a2swadlcl= zeros(ny*nx, dtype=float64).reshape(ny, nx) 
  #------------------------------------------
  # calc scales
  #------------------------------------------
  for iy in range(0,ny):
    for ix in range(0,nx):
      a1dqdp1  = a3dqdp_his[:,iy,ix]
      a1wap1   = a3wap_his[:,iy,ix]
      Plcl1    = a2plcl_his[iy,ix]
      waplcl1  = a2waplcl_his[iy,ix]
      dqdplcl1 = a2dqdplcl_his[iy,ix]
      #
      a1dqdp2  = a3dqdp_fut[:,iy,ix]
      a1wap2   = a3wap_fut[:,iy,ix]
      Plcl2    = a2plcl_fut[iy,ix]
      #waplcl2  = a2waplcl_fut[iy,ix]
      #dqdplcl2 = a2dqdplcl_fut[iy,ix]
      #------------------------------------------
      a3swa[:,iy,ix]   = dtanl_cmip_sbs.swa_profile(Plcl1, llev_f, a1wap1, a1dqdp1)
      scales           = dtanl_cmip_sbs.scale_profile(Plcl1, llev_f, a1wap1, a1wap2, a1dqdp1, a1dqdp2,)
      a3sdwa[:,iy,ix]  = scales[0]
      a3swda[:,iy,ix]  = scales[1]
      a2swadlcl[iy,ix] = -(Plcl2 - Plcl1) * waplcl1 * dqdplcl1
  
  #****************************************************
  # make mean scales (abs)
  #****************************************************
  a3swa     = array(a3swa,    float32)
  a3sdwa    = array(a3sdwa,   float32)
  a3swda    = array(a3swda,   float32)
  a2swadlcl = array(a2swadlcl,float32)
  #****************************************************
  # output name
  #----------------------------------------------------
  sswa_abs      = mapdir + "/epl.abs.swa_%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
  ssdwa_abs     = mapdir + "/epl.abs.dP.dynam.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
  sswda_abs     = mapdir + "/epl.abs.dP.lapse.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
  sswadlcl_abs  = mapdir + "/epl.abs.dP.humid.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
  #----------------------------------------------------
  # write to file
  #----------------------------------------------------
  a3swa.tofile(sswa_abs)
  a3sdwa.tofile(ssdwa_abs)
  a3swda.tofile(sswda_abs)
  a2swadlcl.tofile(sswadlcl_abs)
  print sswa_abs
  #****************************************************
  # make mean scales (frac)
  #****************************************************
  
  a2swa      = array(sum(ma.masked_equal(a3swa,   rmiss), axis=0) , float32)
  a2sdwa     = array(sum(ma.masked_equal(a3sdwa,  rmiss), axis=0) , float32)
  a2swda     = array(sum(ma.masked_equal(a3swda,  rmiss), axis=0) , float32)
  #****************************************************
  # make mask
  #****************************************************
  thres = 1.0 / 24.0 / 60.0 /60.0
  a2swa    = ma.masked_less( a2swa, thres)
  #----------------------------------------------------
  a2sdwa_frac    = a2sdwa / a2swa  * 100.0
  a2swda_frac    = a2swda / a2swa  * 100.0
  a2swadlcl_frac = a2swadlcl / a2swa *100.0
  a2full_frac    = a2sdwa_frac + a2swda_frac + a2swadlcl_frac
  #a2full_frac    = a2sdwa_frac + a2swda_frac
  #----------------------------------------------------
  a2sdwa_frac    =  ma.masked_where( a2swa.mask, a2sdwa_frac)
  a2swda_frac    =  ma.masked_where( a2swa.mask, a2swda_frac)
  a2swadlcl_frac =  ma.masked_where( a2swa.mask, a2swadlcl_frac)
  a2full_frac    =  ma.masked_where( a2swa.mask, a2full_frac)
  #----------------------------------------------------
  #
  a2swa          =  ma.filled(a2swa           , nan)
  a2sdwa_frac    =  ma.filled(a2sdwa_frac     , nan)
  a2swda_frac    =  ma.filled(a2swda_frac     , nan)
  a2swadlcl_frac =  ma.filled(a2swadlcl_frac  , nan)
  a2full_frac    =  ma.filled(a2full_frac     , nan)
  #
  #----------------------------------------------------
  # output name
  #----------------------------------------------------
  sswa_his       = mapdir + "/epl.swa.his.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
  ssdwa_frac     = mapdir + "/epl.dP.dynam.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
  sswda_frac     = mapdir + "/epl.dP.lapse.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
  sswadlcl_frac  = mapdir + "/epl.dP.humid.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
  sfull_frac     = mapdir + "/epl.dP.full.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
  sdprec_frac    = mapdir + "/epl.dP.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
  #----------------------------------------------------
  a2swa.tofile(sswa_his)
  a2sdwa_frac.tofile(ssdwa_frac)   
  a2swda_frac.tofile(sswda_frac)
  a2swadlcl_frac.tofile(sswadlcl_frac)
  a2full_frac.tofile(sfull_frac)
  a2dprec_frac.tofile(sdprec_frac)
  #
  #****************************************************
  # make mean scales (zonal)
  #****************************************************
  # make mask
  #-------------------
  thres = 1.0 / 24.0 / 60.0 /60.0
  a2swa    = fromfile(sswa_his, float32).reshape(ny, nx)
  a2swa    = ma.masked_less( a2swa, thres)
  #-------------------
  ssdwa_frac     = mapdir + "/epl.dP.dynam.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
  sswda_frac     = mapdir + "/epl.dP.lapse.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
  sswadlcl_frac  = mapdir + "/epl.dP.humid.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
  sfull_frac     = mapdir + "/epl.dP.full.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
  #---
  a2sdwa_frac     = fromfile(ssdwa_frac,   float32).reshape(ny, nx)
  a2sdwa_frac     = fromfile(ssdwa_frac,   float32).reshape(ny, nx)
  a2swda_frac     = fromfile(sswda_frac,   float32).reshape(ny, nx)
  a2swadlcl_frac  = fromfile(sswadlcl_frac, float32).reshape(ny, nx)
  a2full_frac     = fromfile(sfull_frac,   float32).reshape(ny, nx)
  #---
  a2sdwa_frac     = ma.masked_where(a2swa.mask, a2sdwa_frac)
  a2swda_frac     = ma.masked_where(a2swa.mask, a2swda_frac)
  a2swadlcl_frac  = ma.masked_where(a2swa.mask, a2swadlcl_frac)
  a2full_frac     = ma.masked_where(a2swa.mask, a2full_frac)
  #---
  a2sdwa_frac     = ma.masked_invalid( a2sdwa_frac)
  a2swda_frac     = ma.masked_invalid( a2swda_frac)
  a2swadlcl_frac  = ma.masked_invalid( a2swadlcl_frac)
  a2full_frac     = ma.masked_invalid( a2full_frac)
  #----------------------------------------------------
  # make values
  #----------------------------------------------------
  f = open(latname, "r")
  llat = f.readlines()
  f.close()
  llat = map(float, llat)
  #-----
  sout = ""
  sout = "num,lat,dprec,full,dynam,w.h.c,sat.lev\n"
  for i in range(0,ny):
    dprec    = mean(a2dprec_frac[i,:])
    full     = mean(a2full_frac[i,:])
    sdwa     = mean(a2sdwa_frac[i,:])
    swda     = mean(a2swda_frac[i,:])
    swadlcl  = mean(a2swadlcl_frac[i,:])
    sout_seg = "%s,%s,%.2f,%.2f,%.2f,%.2f,%.2f\n"%(i, llat[i], dprec, full, sdwa, swda, swadlcl)
    #sout_seg = "%s,%s,%.2f,%.2f,%.2f,%.2f\n"%(i, llat[i], dprec, full, sdwa, swda)
    sout     = sout + sout_seg
  #----------------------------------------------------
  # output name
  #----------------------------------------------------
  sscales_zonal     = zonaldir + "/epl.dP.dynam.%s_%s_%s_%06.2f.csv"%(tstp, model, ens, xth)
  print sscales_zonal
  #----------------------------------------------------
  # write to file
  #----------------------------------------------------
  f = open(sscales_zonal, "w")
  f.write(sout)
  f.close()
  #----------------------------------------------------
