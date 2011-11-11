import commands
import calendar
import os
import sys
###########################################################
cmd   = "/home/utsumi/bin/dtanl/merra/conditional_means_merra"
nx = 288
ny = 144
#---
#nz = 25
#lvar = ["h","omega"]  # multiple layers
#---
nz = 1
lvar = ["prectot","ps","qv10m","t10m"]  # single layer
#####################################################
tstp = "day"
iy = 2001
ey = 2002
im = 1
em = 12 
xth = 99.0
#------------------------------------------------------
idir_root = "/media/disk2/data/MERRA/bn/%s"%(tstp)
#
listfile_pr = "/home/utsumi/bin/dtanl/merra/conditional_means_namelist_pr.txt"
listfile_var = "/home/utsumi/bin/dtanl/merra/conditional_means_namelist_var.txt"
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
for var in lvar:
  #----------------------------------------------------
  # make meanfile name
  #----------------------------------------------------
  dir_mean = "/media/disk2/out/MERRA/%s/cnd.mean/%s/%04d-%04d/%02d-%02d"\
              %(tstp, var, iy, ey, im, em)
  sname_mean= "%s.%s.%06.2f.bn"%(var, tstp, xth)
  smeanfile = dir_mean +"/%s"%(sname_mean)
  try:
    os.makedirs(dir_mean)
  except OSError:
    pass
  #----------------------------------------------------
  # make prxth_lw & prxth_up name
  #----------------------------------------------------
  dir_prxth = "/media/disk2/out/MERRA/%s/prxth/%04d-%04d/%02d-%02d"\
              %(tstp, iy, ey, im, em)
  
  sname_lw = "prxth.MERRA.%s.%06.2f.lw.bn"%(tstp, xth)
  sname_up = "prxth.MERRA.%s.%06.2f.up.bn"%(tstp, xth)
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
    dir_prectot = idir_root + "/%s/%04d"%("prectot", y)
    dir_ps      = idir_root + "/%s/%04d"%("ps", y)
    dir_qv10m   = idir_root + "/%s/%04d"%("qv10m", y)
    dir_t10m    = idir_root + "/%s/%04d"%("t10m", y)
    dir_h       = idir_root + "/%s/%04d"%("h", y) 
    dir_omega   = idir_root + "/%s/%04d"%("omega", y) 
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
        dname["prectot"] = dir_prectot + "/MERRA.%s.%s.%s.bn"%(tstp, "prectot",stime)
        dname["ps"]      = dir_ps      + "/MERRA.%s.%s.%s.bn"%(tstp, "ps", stime)
        dname["qv10m"]   = dir_qv10m   + "/MERRA.%s.%s.%s.bn"%(tstp, "qv10m", stime)
        dname["t10m"]    = dir_t10m    + "/MERRA.%s.%s.%s.bn"%(tstp, "t10m", stime)
        dname["h"]       = dir_h       + "/MERRA.%s.%s.%s.bn"%(tstp, "h", stime)
        dname["omega"]   = dir_omega   + "/MERRA.%s.%s.%s.bn"%(tstp, "omega", stime)
        #-----------
        checkfile(dname["prectot"])
        checkfile(dname[var])
        #-----------
        sout_pr  = sout_pr + dname["prectot"]+"\n"
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
##----------------------------------------------------------
#sTsfc = "/media/disk2/data/CMIP5/bn/tas/day/NorESM1-M/historical/r1i1p1/1990/tas_day_NorESM1-M_historical_r1i1p1_1990010100.bn"
#sqsfc = "/media/disk2/data/CMIP5/bn/huss/day/NorESM1-M/historical/r1i1p1/1990/huss_day_NorESM1-M_historical_r1i1p1_1990010100.bn"
#szsfc = "/media/disk2/data/CMIP5/bn/orog/fx/NorESM1-M/historical/r0i0p0/orog_fx_NorESM1-M_historical_r0i0p0.bn"
#sPsea = "/media/disk2/data/CMIP5/bn/psl/day/NorESM1-M/historical/r1i1p1/1990/psl_day_NorESM1-M_historical_r1i1p1_1990010100.bn"
#sLCL  = "/home/utsumi/temp/LCL.bn"
##




