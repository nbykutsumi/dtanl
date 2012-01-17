from numpy import *
import commands
import calendar
import os
import sys
###########################################################
cmd   = "/home/utsumi/bin/dtanl/cmip5/conditional_means"
lvar = ["hur", "ta", "rhs", "wap", "zg", "huss", "psl", "tas", "pr"]
lmodel = ["NorESM1-M", "MIROC5", "CanESM2"]
#lmodel = ["NorESM1-M",]
#lmodel = ["NorESM1-M"]
#lmodel = ["MIROC5"]
#lmodel = ["CanESM2"]
###################
# set dnz, dny, dnx
###################
dnx    = {}
dny    = {}
dnz    = {}
#
model = "NorESM1-M"
dnz.update({ (model,"hur"):8, (model,"ta"):8, (model,"wap"):8, (model,"zg"):8, (model,"huss"):1, (model,"psl"):1, (model,"tas"):1, (model,"prc"):1, (model,"pr"):1, (model,"rhs"):1})
dny[model] = 96
dnx[model] = 144
#
model = "MIROC5"
dnz.update({ (model,"hur"):8, (model,"ta"):8, (model,"wap"):8, (model,"zg"):8, (model,"huss"):1, (model,"psl"):1, (model,"tas"):1, (model,"prc"):1, (model,"pr"):1, (model,"rhs"):1})
dny[model] = 128
dnx[model] = 256
#
model = "CanESM2"
dnz.update({ (model,"hur"):8, (model,"ta"):8, (model,"wap"):8, (model,"zg"):8, (model,"huss"):1, (model,"psl"):1, (model,"tas"):1, (model,"prc"):1, (model,"pr"):1, (model,"rhs"):1})
dny[model] = 64
dnx[model] = 128
#####################################################

#nz = 8
#lvar = ["wap","zg"]  # multiple layers
#nz = 1
#lvar = ["huss","psl","tas"]  # single layer
#####################################################
tstp = "day"
lexpr = ["historical", "rcp85"]
ens   = "r1i1p1"
dlyrange={"historical":[1990,1999], "rcp85":[2086,2095]}
im = 1
em = 12 
xth = 0.0  # DO NOT CHANGE!
#------------------------------------------------------
idir_root = "/media/disk2/data/CMIP5/bn"
odir_root = idir_root
#
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
for model in lmodel:
  for expr in lexpr:
    print model, expr
    #-----------------------
    lyrange = dlyrange[expr]
    iy = lyrange[0]
    ey = lyrange[1]
    #-----------------------
    # make blank array
    #-----------------------
    for var in lvar:
      #nz = dnz[model, var]
      #ny = dny[model]
      #nx = dnx[model]
      #print "expr=", expr
      #print "iy,ey=", iy,ey
      #print "var=", var 
      ##-----------------------
      ## make blank array
      ##-----------------------
      #aout  = zeros(nz*ny*nx).reshape(nz, ny, nx)
      #aout  = array( aout, float32)
      ##----------------------------------------------------
      ## make meanfile name
      ##----------------------------------------------------
      ######
      #istep = -1
      #for y in range(iy, ey+1):
      #  print y
      #  dir_pr = odir_root + "/%s/%04d"%(mk_dir_tail("pr", tstp, model,expr,ens), y)
      #  dir_prc  = odir_root + "/%s/%04d"%(mk_dir_tail("prc", tstp, model,expr,ens), y)
      #  dir_Tsfc = odir_root + "/%s/%04d"%(mk_dir_tail("tas", tstp, model,expr,ens), y)
      #  dir_qsfc = odir_root + "/%s/%04d"%(mk_dir_tail("huss", tstp, model,expr,ens), y)
      #  dir_zsfc = odir_root + "/%s"%(mk_dir_tail("orog", "fx", model,expr,"r0i0p0"))
      #  dir_Psea = odir_root + "/%s/%04d"%(mk_dir_tail("psl", tstp, model,expr,ens), y)
      #  dir_zg = odir_root + "/%s/%04d"%(mk_dir_tail("zg", tstp, model,expr,ens), y) 
      #  dir_wap = odir_root + "/%s/%04d"%(mk_dir_tail("wap", tstp, model,expr,ens), y) 
      #  dir_hur = odir_root + "/%s/%04d"%(mk_dir_tail("hur", tstp, model,expr,ens), y) 
      #  dir_ta  = odir_root + "/%s/%04d"%(mk_dir_tail("ta" , tstp, model,expr,ens), y) 
      #  dir_rhs = odir_root + "/%s/%04d"%(mk_dir_tail("rhs", tstp, model,expr,ens), y) 
      #  #--------------------
      #  for m in range(1,12+1):
      #  #for m in range(1,1+1):
      #    ##############
      #    # no leap
      #    ##############
      #    if (m==2)&(calendar.isleap(y)):
      #      ed = calendar.monthrange(y,m)[1] -1
      #    else:
      #      ed = calendar.monthrange(y,m)[1]
      #    ##############
      #    for d in range(1, ed + 1):
      #    #for d in range(1, 1 + 1):
      #      istep = istep +1
      #      stime = "%04d%02d%02d%02d"%(y,m,d,0)
      #      dname = {}
      #      #-----------
      #      dname["pr"] = dir_pr + "/%s_%s.bn"%(mk_namehead("pr", tstp, model,expr,ens), stime)
      #      dname["prc"] = dir_prc + "/%s_%s.bn"%(mk_namehead("prc", tstp, model,expr,ens), stime)
      #      dname["tas"] = dir_Tsfc + "/%s_%s.bn"%(mk_namehead("tas", tstp, model,expr,ens), stime)
      #      dname["huss"] = dir_qsfc + "/%s_%s.bn"%(mk_namehead("huss", tstp, model,expr,ens), stime)
      #      dname["orog"] = dir_zsfc + "/%s.bn"%(mk_namehead("orog", "fx", model,expr,"r0i0p0"))
      #      dname["psl"] = dir_Psea + "/%s_%s.bn"%(mk_namehead("psl", tstp, model,expr,ens), stime)
      #      dname["zg"] = dir_zg + "/%s_%s.bn"%(mk_namehead("zg", tstp, model,expr,ens), stime)
      #      dname["wap"] = dir_wap + "/%s_%s.bn"%(mk_namehead("wap", tstp, model,expr,ens), stime)
      #      dname["hur"] = dir_hur + "/%s_%s.bn"%(mk_namehead("hur", tstp, model,expr,ens), stime)
      #      dname["ta"]  = dir_ta  + "/%s_%s.bn"%(mk_namehead("ta" , tstp, model,expr,ens), stime)
      #      dname["rhs"] = dir_rhs + "/%s_%s.bn"%(mk_namehead("rhs", tstp, model,expr,ens), stime)
      #      #-----------
      #      checkfile(dname["pr"])
      #      checkfile(dname[var])
      #      #-----------
      #      # ADD
      #      #-----------
      #      aout_seg = fromfile(dname[var], float32).reshape(nz,ny,nx)
      #      aout  = aout + aout_seg
      ##----------------------
      #aout = aout / istep
      ##----------------------
      ## output name
      ##----------------------
      ##sodir  = '/media/disk2/out/CMIP5/%s/%s/%s/%s/cnd.mean/%s/%04d-%04d/%02d-%02d'%(tstp, model, expr, ens, var, iy, ey, im, em)
      ##soname = sodir + "/%s_%s_%s_%s_%s_%06.2f.bn"\
      ##               %(var, tstp, model, expr, ens, xth)
      ##-----
      #try:
      #  os.makedirs(sodir)
      #except OSError:
      #  pass
      ##----------------------
      #aout.tofile(soname)
      #print soname
      #----------------------------
      # for pr_lw, pr_up
      #----------------------------
      if (var == "pr"):
        nz = dnz[model, var]
        ny = dny[model]
        nx = dnx[model]
        #------------------
        aout_lw      = zeros(nz*ny*nx).reshape(nz, ny, nx)
        aout_lw      = array( aout_lw, float32)
        aout_up      = ones(nz*ny*nx).reshape(nz, ny, nx) * 9999.0
        aout_up      = array( aout_up, float32)
        #------------------
        dir_prxth = "/media/disk2/out/CMIP5/%s/%s/%s/%s/prxth/%04d-%04d/%02d-%02d"\
                    %(tstp, model, expr, ens, iy, ey, im, em)
  
        sname_lw = "prxth_%s_%s_%s_%s_%06.2f_lw.bn"%(tstp, model, expr, ens, xth)
        sname_up = "prxth_%s_%s_%s_%s_%06.2f_up.bn"%(tstp, model, expr, ens, xth)
        #
        spr_lw = dir_prxth +"/%s"%(sname_lw)
        spr_up = dir_prxth +"/%s"%(sname_up) 
        #---------
        aout_lw.tofile(spr_lw)
        aout_up.tofile(spr_up)
        #print spr_up

