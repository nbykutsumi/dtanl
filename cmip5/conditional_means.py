import commands
import calendar
import os
import sys
###########################################################
cmd   = "/home/utsumi/bin/dtanl/cmip5/conditional_means"
nx = 144
ny = 96
dnz ={"wap":8, "zg":8, "huss":1, "psl":1, "tas":1, "prc":1}
lvar = ["prc"]

#nz = 8
#lvar = ["wap","zg"]  # multiple layers
#nz = 1
#lvar = ["huss","psl","tas"]  # single layer
#####################################################
tstp = "day"
model = "NorESM1-M"
#expr = "historical" #historical, rcp85
#expr = "rcp85" #historical, rcp85
ens  = "r1i1p1"
lexpr = ["historical", "rcp85"]
dlyrange={"historical":[1990,1999], "rcp85":[2086,2095]}
#iy = 1990
#ey = 1999
#iy = 2086
#ey = 2095
im = 1
em = 12 
xth = 99.0
#------------------------------------------------------
idir_root = "/media/disk2/data/CMIP5/bn"
odir_root = idir_root
#
listfile_pr = "/home/utsumi/bin/dtanl/cmip5/conditional_means_namelist_pr.txt"
listfile_var = "/home/utsumi/bin/dtanl/cmip5/conditional_means_namelist_var.txt"
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
#####################################################
# start variable loop
#----------------------------------------------------
for expr in lexpr:
  #-----------------------
  lyrange = dlyrange[expr]
  iy = lyrange[0]
  ey = lyrange[1]
  #-----------------------
  for var in lvar:
    nz = dnz[var]
    print "expr=", expr
    print "iy,ey=", iy,ey
    print "var=", var 
    #----------------------------------------------------
    # make meanfile name
    #----------------------------------------------------
    dir_mean = "/media/disk2/out/CMIP5/%s/%s/%s/%s/cnd.mean/%s/%04d-%04d/%02d-%02d"\
                %(tstp, model, expr, ens, var, iy, ey, im, em)
    sname_mean= "%s_%s_%s_%s_%s_%06.2f.bn"%(var, tstp, model, expr, ens, xth)
    smeanfile = dir_mean +"/%s"%(sname_mean)
    try:
      os.makedirs(dir_mean)
    except OSError:
      pass
    #----------------------------------------------------
    # make prxth_lw & prxth_up name
    #----------------------------------------------------
    dir_prxth = "/media/disk2/out/CMIP5/%s/%s/%s/%s/prxth/%04d-%04d/%02d-%02d"\
                %(tstp, model, expr, ens, iy, ey, im, em)
    
    sname_lw = "prxth_%s_%s_%s_%s_%06.2f_lw.bn"%(tstp, model, expr, ens, xth)
    sname_up = "prxth_%s_%s_%s_%s_%06.2f_up.bn"%(tstp, model, expr, ens, xth)
    #
    spr_lw = dir_prxth +"/%s"%(sname_lw)
    spr_up = dir_prxth +"/%s"%(sname_up)
    checkfile(spr_lw)
    checkfile(spr_up)
    #----------------------------------------------------
    # make listfile
    #----------------------------------------------------
    dname={}
    sout_pr  =""
    sout_var =""
    #
    #####
    istep = -1
    for y in range(iy, ey+1):
      print y
      dir_pr = odir_root + "/%s/%04d"%(mk_dir_tail("pr", tstp, model,expr,ens), y)
      dir_prc  = odir_root + "/%s/%04d"%(mk_dir_tail("prc", tstp, model,expr,ens), y)
      dir_Tsfc = odir_root + "/%s/%04d"%(mk_dir_tail("tas", tstp, model,expr,ens), y)
      dir_qsfc = odir_root + "/%s/%04d"%(mk_dir_tail("huss", tstp, model,expr,ens), y)
      dir_zsfc = odir_root + "/%s"%(mk_dir_tail("orog", "fx", model,expr,"r0i0p0"))
      dir_Psea = odir_root + "/%s/%04d"%(mk_dir_tail("psl", tstp, model,expr,ens), y)
      dir_zg = odir_root + "/%s/%04d"%(mk_dir_tail("zg", tstp, model,expr,ens), y) 
      dir_wap = odir_root + "/%s/%04d"%(mk_dir_tail("wap", tstp, model,expr,ens), y) 
      #--------------------
      for m in range(1,12+1):
      #for m in range(1,1+1):
        ##############
        # no leap
        ##############
        if (m==2)&(calendar.isleap(y)):
          ed = calendar.monthrange(y,m)[1] -1
        else:
          ed = calendar.monthrange(y,m)[1]
        ##############
        for d in range(1, ed + 1):
        #for d in range(1, 1 + 1):
          istep = istep +1
          stime = "%04d%02d%02d%02d"%(y,m,d,0)
          #-----------
          dname["pr"] = dir_pr + "/%s_%s.bn"%(mk_namehead("pr", tstp, model,expr,ens), stime)
          dname["prc"] = dir_prc + "/%s_%s.bn"%(mk_namehead("prc", tstp, model,expr,ens), stime)
          dname["tas"] = dir_Tsfc + "/%s_%s.bn"%(mk_namehead("tas", tstp, model,expr,ens), stime)
          dname["huss"] = dir_qsfc + "/%s_%s.bn"%(mk_namehead("huss", tstp, model,expr,ens), stime)
          dname["orog"] = dir_zsfc + "/%s.bn"%(mk_namehead("orog", "fx", model,expr,"r0i0p0"))
          dname["psl"] = dir_Psea + "/%s_%s.bn"%(mk_namehead("psl", tstp, model,expr,ens), stime)
          dname["zg"] = dir_zg + "/%s_%s.bn"%(mk_namehead("zg", tstp, model,expr,ens), stime)
          dname["wap"] = dir_wap + "/%s_%s.bn"%(mk_namehead("wap", tstp, model,expr,ens), stime)
          #-----------
          checkfile(dname["pr"])
          checkfile(dname[var])
          #-----------
          sout_pr  = sout_pr + dname["pr"]+"\n"
          sout_var = sout_var + dname[var]+"\n"
    #-----------
    f = open(listfile_pr, "w")
    f.write(sout_pr)
    f.close()
    f = open(listfile_var, "w")
    f.write(sout_var)
    f.close()
    #-----------
    os.system("%s %s %s %s %s %s %s %s %s" \
              %(cmd, listfile_var, listfile_pr, spr_lw, spr_up, smeanfile, nx, ny, nz)) 
    #-----------
    os.remove(listfile_var)
    os.remove(listfile_pr)
    print smeanfile
##  ----------------------------------------------------------
#s  Tsfc = "/media/disk2/data/CMIP5/bn/tas/day/NorESM1-M/historical/r1i1p1/1990/tas_day_NorESM1-M_historical_r1i1p1_1990010100.bn"
#s  qsfc = "/media/disk2/data/CMIP5/bn/huss/day/NorESM1-M/historical/r1i1p1/1990/huss_day_NorESM1-M_historical_r1i1p1_1990010100.bn"
#s  zsfc = "/media/disk2/data/CMIP5/bn/orog/fx/NorESM1-M/historical/r0i0p0/orog_fx_NorESM1-M_historical_r0i0p0.bn"
#s  Psea = "/media/disk2/data/CMIP5/bn/psl/day/NorESM1-M/historical/r1i1p1/1990/psl_day_NorESM1-M_historical_r1i1p1_1990010100.bn"
#s  LCL  = "/home/utsumi/temp/LCL.bn"
##  




