from numpy import *
#----
dsp   = {}
dspc  = {}
drat  = {}
xth   = 90.0
sdir = "/media/disk2/out/CMIP5/day/NorESM1-M/historical/r1i1p1/tracks/dura24/wfpr"

name_sp  =  sdir + "/sp/sp.p%02d.00.c-1.04.r1000.nw17_DJF_day_NorESM1-M_historical_r1i1p1.bn"%(xth)
name_spc =  sdir + "/sp/sp.p%02d.00.c00.04.r1000.nw17_DJF_day_NorESM1-M_historical_r1i1p1.bn"%(xth)
dsp       = fromfile(name_sp,  float32).reshape(17,96,144)[0]
dspc      = fromfile(name_spc, float32).reshape(17,96,144)[0]
#
drat      = dspc / ma.masked_equal(dsp,0.0)
#
name_num    = sdir + "/num/num.p%02d.00.c-1.04.r1000.nw17_DJF_day_NorESM1-M_historical_r1i1p1.bn"%(xth)
name_numc   = sdir + "/num/num.p%02d.00.c01.04.r1000.nw17_DJF_day_NorESM1-M_historical_r1i1p1.bn"%(xth)
num         = fromfile(name_num,  float32).reshape(17, 96, 144)[0]
numc        = fromfile(name_numc, float32).reshape(17, 96, 144)[0]
ratnum      = numc / ma.masked_equal(num,0.0) 
