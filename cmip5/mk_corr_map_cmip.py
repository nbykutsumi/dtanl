from numpy import *
from dtanl_cmip_sbs import *
import calendar
import os
import sys
#****************************************************
flag_fill = 1

#------------------------------
tstp = "day"
#lmodel = ["NorESM1-M", "MIROC5", "CanESM2"]
#lmodel = ["NorESM1-M", "CanESM2"]
#lmodel = ["MIROC5"]
lmodel = ["NorESM1-M"]
lexpr  = ["his", "fut"]
dexpr ={}
dexpr["his"] = "historical" #historical, rcp85
dexpr["fut"] = "rcp85" #historical, rcp85
ens  = "r1i1p1"
###################
# set dnz, dny, dnx
###################
dnx    = {}
dny    = {}
dnz    = {}
#
model = "NorESM1-M"
dnz.update({ (model,"hus"):8, (model,"ta"):8, (model,"wap"):8, (model,"zg"):8, (model,"huss"):1, (model,"psl"):1, (model,"tas"):1, (model,"prc"):1, (model,"pr"):1, (model,"rhs"):1})
dny[model] = 96
dnx[model] = 144
#
model = "MIROC5"
dnz.update({ (model,"hus"):8, (model,"ta"):8, (model,"wap"):8, (model,"zg"):8, (model,"huss"):1, (model,"psl"):1, (model,"tas"):1, (model,"prc"):1, (model,"pr"):1, (model,"rhs"):1})
dny[model] = 128
dnx[model] = 256
#
model = "CanESM2"
dnz.update({ (model,"hus"):8, (model,"ta"):8, (model,"wap"):8, (model,"zg"):8, (model,"huss"):1, (model,"psl"):1, (model,"tas"):1, (model,"prc"):1, (model,"pr"):1, (model,"rhs"):1})
dny[model] = 64
dnx[model] = 128
#####################################################
rmiss_cmip = (1.0e+20) *0.1
rmiss = -9999.0
flag_fill =1
#####################################################
dyrange={}
dyrange["his"] = [1990,1999]
dyrange["fut"] = [2086,2095]
imon = 1
emon = 12
#xth =99.0
xth =50.0
#------------------------------------------------------
idir_root = "/media/disk2/data/CMIP5/bn"
lvar = ["tas", "huss", "rhs","psl", "zg", "wap"]
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
#####################################################
for model in lmodel:
  ny = dny[model]
  nx = dnx[model]
  #####################################################
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
  ##****************************************************
  # make lev_f file
  #----------------------------------------------------
  slevdir_f = "/media/disk2/out/CMIP5/%s/%s/rcp85/%s/wa.mean"\
            %(tstp, model, ens)
  #
  mk_dir(slevdir_f)
  alev = arange(1200.0*100, 100.0*100 -1.0, -25.0*100.0)
  llev = list(alev)
  #***********************
  sout = "\n".join(map(str, llev))
  sout = sout.strip()
  #***********************
  sfile = slevdir_f + "/lev_f.txt"
  f = open(sfile, "w")
  f.write(sout)
  f.close()
  #---
  print sout
  print sfile
  
  ##****************************************************
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
  # read variables
  #****************************************************
  for expr in lexpr:
    odir_root = "/media/disk2/out/CMIP5/%s/%s/%s/%s"\
              %(tstp, model, dexpr[expr], ens)
    iyear = dyrange[expr][0]
    eyear = dyrange[expr][1]
    #----------------------------------------------------
    # make prxth_lw & prxth_up name
    #----------------------------------------------------
    dir_prxth = "/media/disk2/out/CMIP5/%s/%s/%s/%s/prxth/%04d-%04d/%02d-%02d"\
                %(tstp, model, dexpr[expr], ens, iyear, eyear, imon, emon)
  
    sname_lw = "prxth_%s_%s_%s_%s_%06.2f_lw.bn"%(tstp, model, dexpr[expr], ens, xth)
    sname_up = "prxth_%s_%s_%s_%s_%06.2f_up.bn"%(tstp, model, dexpr[expr], ens, xth)
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
    for year in range(iyear, eyear+1):
    #for year in range(1991, 1991+1):
      dir_pr   = idir_root + "/%s/%04d"%(mk_dir_tail("pr", tstp, model, dexpr[expr], ens), year)
      dir_Tsfc = idir_root + "/%s/%04d"%(mk_dir_tail("tas", tstp, model, dexpr[expr], ens), year)
      dir_qsfc = idir_root + "/%s/%04d"%(mk_dir_tail("huss", tstp, model,dexpr[expr],ens), year)
      dir_Psea = idir_root + "/%s/%04d"%(mk_dir_tail("psl", tstp, model, dexpr[expr],ens), year)
      dir_zg   = idir_root + "/%s/%04d"%(mk_dir_tail("zg", tstp, model,dexpr[expr],ens), year)
      dir_wap  = idir_root + "/%s/%04d"%(mk_dir_tail("wap", tstp, model, dexpr[expr],ens), year)
      dir_ta   = idir_root + "/%s/%04d"%(mk_dir_tail("ta", tstp, model, dexpr[expr],ens), year)
      dir_rhs  = idir_root + "/%s/%04d"%(mk_dir_tail("rhs", tstp, model, dexpr[expr],ens), year)
      #*************
      # dummy sum
      #*************
      a3wap_sum     = zeros(nz_f*ny*nx, dtype=float64).reshape(nz_f,ny,nx)
      a3dqdp_sum    = zeros(nz_f*ny*nx, dtype=float64).reshape(nz_f,ny,nx)
      a3dpxdqdp_sum = zeros(nz_f*ny*nx, dtype=float64).reshape(nz_f,ny,nx)
      a2Plcl_sum    = zeros(ny*nx, dtype=float64).reshape(ny,nx)
      a2dqdplcl_sum = zeros(ny*nx, dtype=float64).reshape(ny,nx)
      a2waplcl_sum  = zeros(ny*nx, dtype=float64).reshape(ny,nx)
      a2count       = zeros(ny*nx, dtype=float64).reshape(ny,nx)
      #-------------
      for mon in range(imon, emon+1):
      #for mon in range(12, 12+1):
        ##############
        # no leap
        ##############
        if (mon==2)&(calendar.isleap(year)):
          ed = calendar.monthrange(year,mon)[1] -1
        else:
          ed = calendar.monthrange(year,mon)[1]
        ##############
        dname={}
        dadat={}
        for day in range(1, ed+1):
        #for day in range(19, 19+1):
          stime = "%04d%02d%02d%02d"%(year,mon,day,0)
          print stime
          #------------------------
          dname["pr"]   = dir_pr   + "/%s_%s.bn"%(mk_namehead("pr", tstp, model,dexpr[expr],ens), stime)
          dname["tas"]  = dir_Tsfc + "/%s_%s.bn"%(mk_namehead("tas", tstp, model,dexpr[expr],ens), stime)
          dname["huss"] = dir_qsfc + "/%s_%s.bn"%(mk_namehead("huss", tstp, model,dexpr[expr],ens), stime)
          dname["psl"]  = dir_Psea + "/%s_%s.bn"%(mk_namehead("psl", tstp, model,dexpr[expr],ens), stime)
          dname["zg"]   = dir_zg   + "/%s_%s.bn"%(mk_namehead("zg", tstp, model,dexpr[expr],ens), stime)
          dname["wap"]  = dir_wap  + "/%s_%s.bn"%(mk_namehead("wap", tstp, model,dexpr[expr],ens), stime)
          dname["ta"]   = dir_ta   + "/%s_%s.bn"%(mk_namehead("ta",  tstp, model,dexpr[expr],ens), stime)
          dname["rhs"]  = dir_rhs  + "/%s_%s.bn"%(mk_namehead("rhs", tstp, model,dexpr[expr],ens), stime)
          #-------------------------
          check_file(dname["pr"])
          check_file(dname["tas"])
          check_file(dname["huss"])
          check_file(dname["psl"])
          check_file(dname["zg"])
          check_file(dname["wap"])
          check_file(dname["ta"])
          check_file(dname["rhs"])
          #--------------------------------------------
          # open and read files
          #--------------------------------------------
          dadat["pr"]   = fromfile(dname["pr"], float32).reshape(ny,nx)
          dadat["tas"]  = fromfile(dname["tas"], float32).reshape(ny,nx)
          dadat["huss"] = fromfile(dname["huss"], float32).reshape(ny,nx)
          dadat["psl"]  = fromfile(dname["psl"], float32).reshape(ny,nx)
          dadat["zg"]   = fromfile(dname["zg"], float32).reshape(dnz[model,"zg"],ny,nx)
          dadat["wap"]  = fromfile(dname["wap"], float32).reshape(dnz[model,"wap"],ny,nx)
          dadat["ta"]   = fromfile(dname["ta"], float32).reshape(dnz[model,"ta"],ny,nx)
          dadat["rhs"]  = fromfile(dname["rhs"], float32).reshape(ny,nx)
          #--------------------------------------------
          # convert from float32 to float64
          #--------------------------------------------
          dadat["pr"]   = array( dadat["pr"]   ,float64) 
          dadat["tas"]  = array( dadat["tas"]  ,float64) 
          dadat["huss"] = array( dadat["huss"] ,float64) 
          dadat["psl"]  = array( dadat["psl"]  ,float64) 
          dadat["zg"]   = array( dadat["zg"]   ,float64) 
          dadat["wap"]  = array( dadat["wap"]  ,float64)
          dadat["ta"]   = array( dadat["ta"]   ,float64)
          dadat["rhs"]  = array( dadat["rhs"]  ,float64) 
          #--------------------------------------------
          dval ={}
          for iy in range(0, ny):
            for ix in range(0, nx):
              pr_lw    = apr_lw[iy,ix]
              pr_up    = apr_up[iy,ix]
              pr       = dadat["pr"][iy,ix]
              #---------------------------------
              # check precip
              #---------------------------------
              if ( (pr < pr_lw) or (pr_up < pr) ):
                continue
              #---------------------------------
              # counter
              #---------------------------------
              a2count[iy,ix] = a2count[iy,ix] + 1.0
              #---------------------------------
              Tsfc     = dadat["tas"][iy,ix]
              qsfc     = dadat["huss"][iy,ix]
              Psea     = dadat["psl"][iy,ix]
              a1zg     = dadat["zg" ][:,iy,ix]
              a1wap_c  = dadat["wap"][:,iy,ix]
              a1T_c   = dadat["ta" ][:,iy,ix]
              RHsfc    = dadat["rhs"][iy,ix]
              zsfc     = a2orog[iy,ix]
              #---------------------------------
              # replace rmiss_cmip with zero
              #---------------------------------
              a1zg     = ma.filled(ma.masked_greater(a1zg, rmiss_cmip), 0.0)
              a1wap_c  = ma.filled(ma.masked_greater(a1wap_c, rmiss_cmip), 0.0)
              a1T_c  = ma.filled(ma.masked_greater(a1T_c, rmiss_cmip), 0.0)
              #---------------------------------
              Psfc     = dtanl_cmip_sbs.psea2psfc(Tsfc, qsfc, zsfc, Psea)
              Plcl     = dtanl_cmip_sbs.lcl(Psfc, Tsfc, qsfc)
              #------------------------------------------
              a1wap_f  = dtanl_cmip_sbs.omega_profile(0.0, Psfc, Psfc, llev_c, llev_f, a1wap_c)
              a1dqdp_f = dtanl_cmip_sbs.dqdp_profile_epl(Plcl, Psfc, Tsfc, llev_c, llev_f, a1T_c)
              a1dpxdqdp_f = dtanl_cmip_sbs.dpxdqdp_profile(Plcl, a1dqdp_f, llev_f)
              #------------------------------------------
              # at LCL
              #------------------------------------------
              iz_btm   = dtanl_cmip_sbs.findiz_btm(llev_f, Psfc)
              waplcl   = dtanl_cmip_sbs.omega_atp(iz_btm, a1wap_f, llev_f, Psfc, Plcl, 0.0)
              Tlcl     = dtanl_cmip_sbs.t1tot2dry(Tsfc, Psfc, Plcl)
              dqdplcl  = dtanl_cmip_sbs.cal_rdqdp(Plcl, Tlcl, 10.0)
              #------------------------------------------
              # make sum
              #------------------------------------------
              a3wap_sum[:,iy,ix]     = a3wap_sum[:,iy,ix]   + a1wap_f
              a3dqdp_sum[:,iy,ix]    = a3dqdp_sum[:,iy,ix]  + a1dqdp_f
              a3dpxdqdp_sum[:,iy,ix] = a3dpxdqdp_sum[:,iy,ix] + a1dpxdqdp_f
              a2Plcl_sum[iy,ix]      = a2Plcl_sum[iy,ix]    + Plcl
              a2waplcl_sum[iy,ix]    = a2waplcl_sum[iy,ix]  + waplcl
              a2dqdplcl_sum[iy,ix]   = a2dqdplcl_sum[iy,ix] + dqdplcl
              #if ((iy == 30)&(ix == 135)):
              #  print year, mon, day
              #  #print a1wap_f
              #  print "aaaaa"
              #  print a1wap_c
              #  print rmiss_cmip
      #----------------------------------------------
      # out file name
      #----------------------------------------------
      odir_wap   = odir_root + "/wa.mean/%06.2f/wap"%(xth)
      odir_dqdp  = odir_root + "/wa.mean/%06.2f/dqdp"%(xth)
      odir_Plcl  = odir_root + "/wa.mean/%06.2f/plcl"%(xth)
      odir_count = odir_root + "/wa.mean/%06.2f/count"%(xth)
      mk_dir(odir_wap)
      mk_dir(odir_dqdp)
      mk_dir(odir_Plcl)
      mk_dir(odir_count)
      swap_sum     = odir_wap +  "/epl.wap.sum.%04d.bn"%(year)
      sdqdp_sum    = odir_dqdp + "/epl.dqdp.sum.%04d.bn"%(year)
      sPlcl_sum    = odir_Plcl + "/epl.plcl.sum.%04d.bn"%(year)
      swaplcl_sum  = odir_Plcl + "/epl.waplcl.sum.%04d.bn"%(year)
      sdqdplcl_sum = odir_Plcl + "/epl.dqdplcl.sum.%04d.bn"%(year)
      scountfile   = odir_count+ "/epl.count.%04d.bn"%(year)
      #----------------------------------------------
      # write to file
      #----------------------------------------------
      a3wap_sum      = array(a3wap_sum, float32)
      a3dqdp_sum     = array(a3dqdp_sum, float32)
      a2Plcl_sum     = array(a2Plcl_sum, float32)
      a2waplcl_sum   = array(a2waplcl_sum, float32)
      a2dqdplcl_sum  = array(a2dqdplcl_sum, float32)
      a2count        = array(a2count, float32)
      #----------------------------
      a3wap_sum.tofile(swap_sum)
      a3dqdp_sum.tofile(sdqdp_sum)
      a2Plcl_sum.tofile(sPlcl_sum)
      a2waplcl_sum.tofile(swaplcl_sum)
      a2dqdplcl_sum.tofile(sdqdplcl_sum)
      a2count.tofile(scountfile)
      #----------------------------------------------
      print "swap_sum",swap_sum
      print "sdqdp_sum",sdqdp_sum
      print sPlcl_sum
      print scountfile
  #****************************************************************
  # make mean file
  #****************************************************************
  for expr in lexpr:
    print model, expr
    #-------------------------------------
    odir_root = "/media/disk2/out/CMIP5/%s/%s/%s/%s"\
              %(tstp, model, dexpr[expr], ens)
    #-------------------------------------
    iyear = dyrange[expr][0]
    eyear = dyrange[expr][1]
    #-------------------------------------
    # make dummy
    #-------------------------------------
    a3wap_mean     = zeros(nz_f*ny*nx, dtype=float32).reshape(nz_f, ny, nx)
    a3dqdp_mean    = zeros(nz_f*ny*nx, dtype=float32).reshape(nz_f, ny, nx)
    a2Plcl_mean    = zeros(ny*nx, dtype=float32).reshape(ny, nx)
    a2waplcl_mean  = zeros(ny*nx, dtype=float32).reshape(ny, nx)
    a2dqdplcl_mean = zeros(ny*nx, dtype=float32).reshape(ny, nx)
    a2count        = zeros(ny*nx, dtype=float32).reshape(ny,nx)
    for year in range(iyear, eyear+1):
    #for year in range(2086, 2086+1):
      #----------------------------------------------
      # out file name
      #----------------------------------------------
      odir_wap     = odir_root  + "/wa.mean/%06.2f/wap"%(xth)
      odir_dqdp    = odir_root  + "/wa.mean/%06.2f/dqdp"%(xth)
      odir_Plcl    = odir_root  + "/wa.mean/%06.2f/plcl"%(xth)
      odir_count   = odir_root  + "/wa.mean/%06.2f/count"%(xth)
      swap_sum     = odir_wap   + "/epl.wap.sum.%04d.bn"%(year)
      sdqdp_sum    = odir_dqdp  + "/epl.dqdp.sum.%04d.bn"%(year)
      sPlcl_sum    = odir_Plcl  + "/epl.plcl.sum.%04d.bn"%(year)
      swaplcl_sum  = odir_Plcl  + "/epl.waplcl.sum.%04d.bn"%(year)
      sdqdplcl_sum = odir_Plcl  + "/epl.dqdplcl.sum.%04d.bn"%(year)
      scountfile   = odir_count + "/epl.count.%04d.bn"%(year)
      #----------------------------------------------
      # read files
      #----------------------------------------------
      a3wap_seg      = fromfile(swap_sum,  float32).reshape(nz_f, ny, nx)
      a3dqdp_seg     = fromfile(sdqdp_sum, float32).reshape(nz_f, ny, nx)
      a2Plcl_seg     = fromfile(sPlcl_sum, float32).reshape(ny, nx)
      a2waplcl_seg   = fromfile(swaplcl_sum, float32).reshape(ny, nx)
      a2dqdplcl_seg  = fromfile(sdqdplcl_sum, float32).reshape(ny, nx)
      a2count_seg    = fromfile(scountfile,float32).reshape(ny,nx)
      #----------------------------------------------
      # calulation
      #----------------------------------------------
      a3wap_mean       = a3wap_mean + a3wap_seg
      a3dqdp_mean      = a3dqdp_mean + a3dqdp_seg
      a2Plcl_mean      = a2Plcl_mean + a2Plcl_seg
      a2waplcl_mean    = a2waplcl_mean + a2waplcl_seg
      a2dqdplcl_mean   = a2dqdplcl_mean + a2dqdplcl_seg
      a2count          = a2count + a2count_seg
    #----------
    a3wap_mean         = a3wap_mean / a2count
    a3dqdp_mean        = a3dqdp_mean/ a2count
    #----------
    a2Plcl_mean        = a2Plcl_mean / a2count
    a2waplcl_mean      = a2waplcl_mean / a2count
    a2dqdplcl_mean     = a2dqdplcl_mean / a2count
    #------------------------
    swap_mean     =odir_wap   + "/epl.wap.mean.%04d-%04d.bn"%(iyear, eyear)
    sdqdp_mean    =odir_dqdp  + "/epl.dqdp.mean.%04d-%04d.bn"%(iyear, eyear)
    sPlcl_mean    =odir_Plcl  + "/epl.plcl.mean.%04d-%04d.bn"%(iyear, eyear)
    swaplcl_mean  =odir_Plcl  + "/epl.waplcl.mean.%04d-%04d.bn"%(iyear, eyear)
    sdqdplcl_mean =odir_Plcl  + "/epl.dqdplcl.mean.%04d-%04d.bn"%(iyear, eyear)
    scount_all    =odir_count + "/epl.count.all.%04d-%04d.bn"%(iyear, eyear)
    #------------------------
    # write to file
    #------------------------
    a3wap_mean.tofile(swap_mean)
    a3dqdp_mean.tofile(sdqdp_mean)
    a2Plcl_mean.tofile(sPlcl_mean)
    a2waplcl_mean.tofile(swaplcl_mean)
    a2dqdplcl_mean.tofile(sdqdplcl_mean)
    a2count.tofile(scount_all)
    #-------------
    print swap_mean
