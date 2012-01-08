from dtanl_cmip_sbs import *
from numpy import *
import calendar
import os
#--------------------------------------------------
nx = 144
ny = 96
nz = 8
tstp = "day"
model = "NorESM1-M"
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
rmiss = -9999.0
g = 9.8
odir_root ="/media/disk2/out/CMIP5/%s/%s" %(tstp, model)
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
# read orog file
#----------------------------------------------------
dir_zsfc = idir_root + "/%s"%(mk_dir_tail("orog", "fx", model,dexpr["fut"], "r0i0p0"))
sorog    = dir_zsfc + "/%s.bn"%(mk_namehead("orog", "fx", model,dexpr["fut"],"r0i0p0"))
check_file(sorog)
#--
a2orog = fromfile(sorog, float32).reshape(ny,nx)
a2orog = array(a2orog, float64)
#****************************************************
# read lev_c file
#----------------------------------------------------
slevdir_c = "/media/disk2/data/CMIP5/bn/zg/day/%s/historical/%s"\
          %(model, ens)
slev_c    = slevdir_c +"/lev.txt"
check_file(slev_c)
f         = open(slev_c, "r")
llev_c    = map( lambda x: x.strip(),  f.readlines() )
f.close()
llev_c    = map( float, llev_c)
nz_c      = len(llev_c)
#****************************************************
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
expr_m = "fut"
expr_v = "his"
iyear = dyrange[expr_v][0]
eyear = dyrange[expr_v][1]
dir_m = odir_root + "/%s/%s/wa.mean/%06.2f"%(dexpr[expr_m], ens, xth)
#****************************************************
# make map dir
#****************************************************
if ( expr_m == "his"):
  casename = "his.m.fut.v"
elif (expr_m == "fut"):
  casename = "his.v.fut.m"
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
#----------------------------------------------------
# read precip file
#----------------------------------------------------
iyear_his = dyrange["his"][0]
eyear_his = dyrange["his"][1]
iyear_fut = dyrange["fut"][0]
eyear_fut = dyrange["fut"][1]
dir_prxth_his = "/media/disk2/out/CMIP5/%s/%s/%s/%s/prxth/%04d-%04d/%02d-%02d"\
            %(tstp, model, dexpr["his"], ens, iyear_his, eyear_his, imon, emon)
dir_prxth_fut = "/media/disk2/out/CMIP5/%s/%s/%s/%s/prxth/%04d-%04d/%02d-%02d"\
            %(tstp, model, dexpr["fut"], ens, iyear_fut, eyear_fut, imon, emon)
#---
spr_his  = dir_prxth_his + "/prxth_%s_%s_%s_%s_%06.2f_lw.bn"%(tstp, model, dexpr["his"], ens, xth)
spr_fut  = dir_prxth_fut + "/prxth_%s_%s_%s_%s_%06.2f_lw.bn"%(tstp, model, dexpr["fut"], ens, xth)
#---
a2pr_his  = fromfile(spr_his, float32).reshape(ny,nx)
a2pr_fut  = fromfile(spr_fut, float32).reshape(ny,nx)
a2dprec   = (a2pr_fut - a2pr_his) / a2pr_his
a2dprec   = a2dprec *100.0
#----------------------------------------------------
# make prxth_lw & prxth_up name
#----------------------------------------------------
dir_prxth = "/media/disk2/out/CMIP5/%s/%s/%s/%s/prxth/%04d-%04d/%02d-%02d"\
            %(tstp, model, dexpr[expr_v], ens, iyear, eyear, imon, emon)

sname_lw = "prxth_%s_%s_%s_%s_%06.2f_lw.bn"%(tstp, model, dexpr[expr_v], ens, xth)
sname_up = "prxth_%s_%s_%s_%s_%06.2f_up.bn"%(tstp, model, dexpr[expr_v], ens, xth)
#
spr_lw = dir_prxth +"/%s"%(sname_lw)
spr_up = dir_prxth +"/%s"%(sname_up)
check_file(spr_lw)
check_file(spr_up)
#----
apr_lw = fromfile(spr_lw, float32).reshape(ny,nx)
apr_up = fromfile(spr_up, float32).reshape(ny,nx)
#** convert from float32 to float64 ***
apr_lw = array(apr_lw , float64)
apr_up = array(apr_up , float64)
#----------------------------------------------------
#* read mean file
#----------------------------------------------------
iyear_m = dyrange[expr_m][0]
eyear_m = dyrange[expr_m][1]
#iyear_m = 2086
#eyear_m = 2095
sdqdp_m = dir_m + "/dqdp/dqdp.mean.%04d-%04d.bn"%(iyear_m, eyear_m)
swap_m  = dir_m + "/wap/wap.mean.%04d-%04d.bn"%(iyear_m, eyear_m)
splcl_m = dir_m + "/plcl/plcl.mean.%04d-%04d.bn"%(iyear_m, eyear_m)
#-----
a3dqdp_m = array( fromfile(sdqdp_m, float32), float64).reshape(nz_f, ny, nx)
a3wap_m  = array( fromfile(swap_m,  float32), float64).reshape(nz_f, ny, nx)
a2plcl_m = array( fromfile(splcl_m,  float32), float64).reshape(ny, nx)
#----------------------------------------------------
# dummy
#----------------------------------------------------
a3swa    = zeros(nz_f*ny*nx, dtype=float64).reshape(nz_f, ny, nx)
a3sdwa   = zeros(nz_f*ny*nx, dtype=float64).reshape(nz_f, ny, nx)
a3swda   = zeros(nz_f*ny*nx, dtype=float64).reshape(nz_f, ny, nx)
a2swadlcl= zeros(ny*nx, dtype=float64).reshape(ny, nx) 
a2count  = zeros(ny*nx, dtype=float64).reshape(ny, nx)
##----------------------------------------------------
## start loop
##----------------------------------------------------
#for year in range(iyear, eyear+1):
##for year in range(1990, 1990+1):
#  dir_pr   = idir_root + "/%s/%04d"%(mk_dir_tail("pr", tstp, model, dexpr[expr_v], ens), year)
#  dir_Tsfc = idir_root + "/%s/%04d"%(mk_dir_tail("tas", tstp, model, dexpr[expr_v], ens), year)
#  dir_qsfc = idir_root + "/%s/%04d"%(mk_dir_tail("huss", tstp, model,dexpr[expr_v],ens), year)
#  dir_Psea = idir_root + "/%s/%04d"%(mk_dir_tail("psl", tstp, model, dexpr[expr_v],ens), year)
#  dir_zg = idir_root + "/%s/%04d"%(mk_dir_tail("zg", tstp, model,dexpr[expr_v],ens), year)
#  dir_wap = idir_root + "/%s/%04d"%(mk_dir_tail("wap", tstp, model, dexpr[expr_v],ens), year)
#  dir_rhs = idir_root + "/%s/%04d"%(mk_dir_tail("rhs", tstp, model, dexpr[expr_v],ens), year)
#  #-------------
#  for mon in range(imon, emon+1):
#  #for mon in range(1,1+1):
#    ##############
#    # no leap
#    ##############
#    if (mon==2)&(calendar.isleap(year)):
#      ed = calendar.monthrange(year,mon)[1] -1
#    else:
#      ed = calendar.monthrange(year,mon)[1]
#    ##############
#    dname={}
#    dadat={}
#    for day in range(1, ed+1):
#      stime = "%04d%02d%02d%02d"%(year,mon,day,0)
#      print stime
#      #------------------------
#      dname["pr"]   = dir_pr   + "/%s_%s.bn"%(mk_namehead("pr", tstp, model,dexpr[expr_v],ens), stime)
#      dname["tas"]  = dir_Tsfc + "/%s_%s.bn"%(mk_namehead("tas", tstp, model,dexpr[expr_v],ens), stime)
#      dname["huss"] = dir_qsfc + "/%s_%s.bn"%(mk_namehead("huss", tstp, model,dexpr[expr_v],ens), stime)
#      dname["psl"]  = dir_Psea + "/%s_%s.bn"%(mk_namehead("psl", tstp, model,dexpr[expr_v],ens), stime)
#      dname["zg"]   = dir_zg   + "/%s_%s.bn"%(mk_namehead("zg", tstp, model,dexpr[expr_v],ens), stime)
#      dname["wap"]  = dir_wap  + "/%s_%s.bn"%(mk_namehead("wap", tstp, model,dexpr[expr_v],ens), stime)
#      dname["rhs"]  = dir_rhs  + "/%s_%s.bn"%(mk_namehead("rhs", tstp, model,dexpr[expr_v],ens), stime)
#      #-------------------------
#      #-------------------------
#      check_file(dname["pr"])
#      check_file(dname["tas"])
#      check_file(dname["huss"])
#      check_file(dname["psl"])
#      check_file(dname["zg"])
#      check_file(dname["wap"])
#      check_file(dname["rhs"])
#      #--------------------------------------------
#      # open and read files
#      #--------------------------------------------
#      dadat["pr"]   = fromfile(dname["pr"], float32).reshape(ny,nx)
#      dadat["tas"]  = fromfile(dname["tas"], float32).reshape(ny,nx)
#      dadat["huss"] = fromfile(dname["huss"], float32).reshape(ny,nx)
#      dadat["psl"]  = fromfile(dname["psl"], float32).reshape(ny,nx)
#      dadat["zg"]   = fromfile(dname["zg"], float32).reshape(nz,ny,nx)
#      dadat["wap"]  = fromfile(dname["wap"], float32).reshape(nz,ny,nx)
#      dadat["rhs"]  = fromfile(dname["rhs"], float32).reshape(ny,nx)
#      #--------------------------------------------
#      for iy in range(0,ny):
#        for ix in range(0,nx):
#          pr_lw    = apr_lw[iy,ix]
#          pr_up    = apr_up[iy,ix]
#          pr       = dadat["pr"][iy,ix]
#          #---------------------------------
#          # check precip
#          #---------------------------------
#          if ( (pr < pr_lw) or (pr_up < pr) ):
#            continue
#          #---------------------------------
#          # counter
#          #---------------------------------
#          a2count[iy,ix] = a2count[iy,ix] + 1.0
#          #---------------------------------
#          Tsfc     = dadat["tas"][iy,ix]
#          qsfc     = dadat["huss"][iy,ix]
#          Psea     = dadat["psl"][iy,ix]
#          a1zg     = dadat["zg"][:,iy,ix]
#          a1wap_c  = dadat["wap"][:,iy,ix]
#          RHsfc    = dadat["rhs"][iy,ix]
#          zsfc     = a2orog[iy,ix]
#          Psfc = dtanl_cmip_sbs.psea2psfc(Tsfc, qsfc, zsfc, Psea) 
#          #------------------------------------------
#          Plcl_v = dtanl_cmip_sbs.lcl(Psfc, Tsfc, qsfc)
#          a1dqdp_fv = dtanl_cmip_sbs.dqdp_profile(flag_fill, rmiss, Psfc, Tsfc, qsfc, Plcl_v, llev_f)
#          a1wap_fv  = dtanl_cmip_sbs.omega_profile(0.0, Psfc, Plcl_v, llev_c, llev_f, a1wap_c)
#          #
#          Plcl_m    = a2plcl_m[iy,ix]
#          a1dqdp_fm = a3dqdp_m[:,iy,ix]
#          a1wap_fm  = a3wap_m[:,iy,ix]
#          #------------------------------------------
#          # calc scales
#          #------------------------------------------
#          if ( expr_m == "his" ):
#            a1dqdp1 = a1dqdp_fm
#            a1wap1  = a1wap_fm
#            Plcl1   = Plcl_m
#            a1dqdp2 = a1dqdp_fv
#            a1wap2  = a1wap_fv
#            Plcl2   = Plcl_v
#          else:
#            a1dqdp1 = a1dqdp_fv
#            a1wap1  = a1wap_fv
#            Plcl1   = Plcl_v
#            a1dqdp2 = a1dqdp_fm
#            a1wap2  = a1wap_fm
#            Plcl2   = Plcl_m
#          #------------------------------------------
#          a3swa[:,iy,ix]   = a3swa[:,iy,ix]  + dtanl_cmip_sbs.swa_profile(Plcl1, llev_f, a1wap1, a1dqdp1)
#          scales           = dtanl_cmip_sbs.scale_profile(Plcl1, llev_f, a1wap1, a1wap2, a1dqdp1, a1dqdp2,)
#          a3sdwa[:,iy,ix]  = a3sdwa[:,iy,ix] + scales[0]
#          a3swda[:,iy,ix]  = a3swda[:,iy,ix] + scales[1]
#          a2swadlcl[iy,ix] = a2swadlcl[iy,ix] + dtanl_cmip_sbs.cal_swadlcl(Plcl1, Plcl2, llev_f, a1wap1, a1dqdp1)
#
##****************************************************
## make mean scales (abs)
##****************************************************
#a2count   = array(a2count,  float32)
#a3swa     = array(a3swa,    float32)
#a3sdwa    = array(a3sdwa,   float32)
#a3swda    = array(a3swda,   float32)
#a2swadlcl = array(a2swadlcl,float32)
##****************************************************
## make mean scales (abs)
##****************************************************
#a2count   = ma.masked_equal(a2count, 0.0)
#a3swa     = a3swa    / a2count 
#a3sdwa    = a3sdwa   / a2count
#a3swda    = a3swda   / a2count
#a2swadlcl = a2swadlcl/ a2count
##--
#a3swa     = ma.filled(a3swa, rmiss)
#a3sdwa    = ma.filled(a3sdwa, rmiss)
#a3swda    = ma.filled(a3swda, rmiss)
#a2swadlcl = ma.filled(a2swadlcl, rmiss)
#----------------------------------------------------
# output name
#----------------------------------------------------
sswa_abs      = mapdir + "/abs.swa_%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
ssdwa_abs     = mapdir + "/abs.dP.dynam.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
sswda_abs     = mapdir + "/abs.dP.lapse.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
sswadlcl_abs  = mapdir + "/abs.dP.humid.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
##----------------------------------------------------
## write to file
##----------------------------------------------------
#a3swa.tofile(sswa_abs)
#a3sdwa.tofile(ssdwa_abs)
#a3swda.tofile(sswda_abs)
#a2swadlcl.tofile(sswadlcl_abs)
#print sswa_abs
##****************************************************
## make mean scales (frac)
##****************************************************
a3swa       = fromfile(sswa_abs,     float32).reshape(nz_f, ny, nx)
a3sdwa      = fromfile(ssdwa_abs,    float32).reshape(nz_f, ny, nx)
a3swda      = fromfile(sswda_abs,    float32).reshape(nz_f, ny, nx)
a2swadlcl   = fromfile(sswadlcl_abs, float32).reshape(ny, nx)
a2swa       = sum(ma.masked_equal(a3swa,   rmiss), axis=0)
a2sdwa      = sum(ma.masked_equal(a3sdwa,  rmiss), axis=0)
a2swda      = sum(ma.masked_equal(a3swda,  rmiss), axis=0)
#
a2sdwa_frac    = a2sdwa / a2swa  * 100.0
a2swda_frac    = a2swda / a2swa  * 100.0
a2swadlcl_frac = a2swadlcl / a2swa *100.0
a2full_frac    = a2sdwa_frac + a2swda_frac + a2swadlcl_frac
#
a2swa          =  ma.filled(a2swa           , rmiss)
a2sdwa_frac    =  ma.filled(a2sdwa_frac     , rmiss)
a2swda_frac    =  ma.filled(a2swda_frac     , rmiss)
a2swadlcl_frac =  ma.filled(a2swadlcl_frac  , rmiss)
a2full_frac    =  ma.filled(a2full_frac     , rmiss)

#----------------------------------------------------
# output name
#----------------------------------------------------
sswa_his       = mapdir + "/swa.his.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
ssdwa_frac     = mapdir + "/dP.dynam.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
sswda_frac     = mapdir + "/dP.lapse.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
sswadlcl_frac  = mapdir + "/dP.humid.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
sfull_frac     = mapdir + "/dP.full.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
#----------------------------------------------------
a2swa.tofile(sswa_his)
a2sdwa_frac.tofile(ssdwa_frac)   
a2swda_frac.tofile(sswda_frac)
a2swadlcl_frac.tofile(sswadlcl_frac)
a2full_frac.tofile(sfull_frac)
#
print sswda_frac
#****************************************************
# make mean scales (zonal)
#****************************************************
# make mask
#----------------
thres    = 1.0 / 24.0 / 60.0 / 60.0
a2swa    = fromfile(sswa_his, float32).reshape(ny,nx)
a2swa    = ma.masked_less(a2swa, thres)
#----------------
ssdwa_frac     = mapdir + "/dP.dynam.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
sswda_frac     = mapdir + "/dP.lapse.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
sswadlcl_frac  = mapdir + "/dP.humid.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
sfull_frac     = mapdir + "/dP.full.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
#---
a2sdwa_frac     = fromfile(ssdwa_frac,   float32).reshape(ny, nx)
a2swda_frac     = fromfile(sswda_frac,   float32).reshape(ny, nx)
a2swadlcl_frac  = fromfile(sswadlcl_frac, float32).reshape(ny, nx)
a2full_frac     = fromfile(sfull_frac,   float32).reshape(ny, nx)
#---
a2sdwa_frac     = ma.masked_where(a2swa.mask, a2sdwa_frac)
a2swda_frac     = ma.masked_where(a2swa.mask, a2swda_frac)
a2swadlcl_frac  = ma.masked_where(a2swa.mask, a2swadlcl_frac)
a2full_frac     = ma.masked_where(a2swa.mask, a2full_frac)
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
  dprec    = mean(a2dprec[i,:])
  full     = mean(a2full_frac[i,:])
  sdwa     = mean(a2sdwa_frac[i,:])
  swda     = mean(a2swda_frac[i,:])
  swadlcl  = mean(a2swadlcl_frac[i,:])
  sout_seg = "%s,%s,%.2f,%.2f,%.2f,%.2f,%.2f\n"%(i, llat[i], dprec, full, sdwa, swda, swadlcl)
  sout     = sout + sout_seg
#----------------------------------------------------
# output name
#----------------------------------------------------
sscales_zonal     = zonaldir + "/dP.dynam.%s_%s_%s_%06.2f.csv"%(tstp, model, ens, xth)
print sscales_zonal
#----------------------------------------------------
# write to file
#----------------------------------------------------
f = open(sscales_zonal, "w")
f.write(sout)
f.close()
#----------------------------------------------------
