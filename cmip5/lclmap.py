import commands
import calendar
import os
import sys
###########################################################
cmd   = "/home/utsumi/bin/dtanl/cmip5/lclmap"
nx = 144
ny = 96
#####################################################
tstp = "day"
model = "NorESM1-M"
#expr = "historical" #historical, rcp85
expr = "rcp85" #historical, rcp85
ens  = "r1i1p1"
#lyrange= [ [1980,1999] ]
lyrange= [ [2075,2095] ]
#------------------------------------------------------
idir_root = "/media/disk2/data/CMIP5/bn"
odir_root = idir_root
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
for yrange in lyrange:
  y0 = yrange[0]
  y1 = yrange[1]
  #####
  istep = -1
  for y in range(y0, y1+1):
    dir_Tsfc = odir_root + "/%s/%04d"%(mk_dir_tail("tas", tstp, model,expr,ens), y)
    dir_qsfc = odir_root + "/%s/%04d"%(mk_dir_tail("huss", tstp, model,expr,ens), y)
    dir_zsfc = odir_root + "/%s"%(mk_dir_tail("orog", "fx", model,expr,"r0i0p0"))
    dir_Psea = odir_root + "/%s/%04d"%(mk_dir_tail("psl", tstp, model,expr,ens), y)
    dir_LCL = odir_root + "/%s/%04d"%(mk_dir_tail("lcl", tstp, model,expr,ens), y) 
    #--------------------
    try:
      os.makedirs(dir_LCL)
    except OSError:
      pass
    #--------------------
    for m in range(1,12+1):
      ##############
      # no leap
      ##############
      if (m==2)&(calendar.isleap(y)):
        ed = calendar.monthrange(y,m)[1] -1
      else:
        ed = calendar.monthrange(y,m)[1]
      ##############
      for d in range(1, ed + 1):
        istep = istep +1
        stime = "%04d%02d%02d%02d"%(y,m,d,0)
        #-----------
        sTsfc = dir_Tsfc + "/%s_%s.bn"%(mk_namehead("tas", tstp, model,expr,ens), stime)
        sqsfc = dir_qsfc + "/%s_%s.bn"%(mk_namehead("huss", tstp, model,expr,ens), stime)
        szsfc = dir_zsfc + "/%s.bn"%(mk_namehead("orog", "fx", model,expr,"r0i0p0"))
        sPsea = dir_Psea + "/%s_%s.bn"%(mk_namehead("psl", tstp, model,expr,ens), stime)
        sLCL = dir_LCL + "/%s_%s.bn"%(mk_namehead("lcl", tstp, model,expr,ens), stime)
        #-----------
        for siname in [sTsfc, sqsfc, szsfc, sPsea]:
          if not (os.access(siname, os.F_OK)):
             print "no file: ", siname
             sys.exit()
        #-----------
        os.system("%s %s %s %s %s %s %s %s"\
               %(cmd, sTsfc, sqsfc, szsfc, sPsea, sLCL, nx, ny))
        print sLCL
##----------------------------------------------------------
#sTsfc = "/media/disk2/data/CMIP5/bn/tas/day/NorESM1-M/historical/r1i1p1/1990/tas_day_NorESM1-M_historical_r1i1p1_1990010100.bn"
#sqsfc = "/media/disk2/data/CMIP5/bn/huss/day/NorESM1-M/historical/r1i1p1/1990/huss_day_NorESM1-M_historical_r1i1p1_1990010100.bn"
#szsfc = "/media/disk2/data/CMIP5/bn/orog/fx/NorESM1-M/historical/r0i0p0/orog_fx_NorESM1-M_historical_r0i0p0.bn"
#sPsea = "/media/disk2/data/CMIP5/bn/psl/day/NorESM1-M/historical/r1i1p1/1990/psl_day_NorESM1-M_historical_r1i1p1_1990010100.bn"
#sLCL  = "/home/utsumi/temp/LCL.bn"
##




