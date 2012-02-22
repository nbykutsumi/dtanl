from numpy import *

ny = 96
nx = 144

mapdir = "/media/disk2/out/CMIP5/day/NorESM1-M/scales/r1i1p1/his.m.fut.m/map"
#********************
# input names
#--------------------
dp_full_name     = mapdir + "/epl.dP.full.day_NorESM1-M_r1i1p1_099.00.bn"
dp_lcl_name      = mapdir + "/epl.dP.humid.day_NorESM1-M_r1i1p1_099.00.bn"
#********************
# output names
#--------------------
dp_lcl_full_name = mapdir + "/epl.dP.lcl_full.day_NorESM1-M_r1i1p1_099.00.bn"

#********************
# read
#--------------------
a2dp_full        = fromfile(dp_full_name, float32).reshape(ny, nx)
a2dp_lcl         = fromfile(dp_lcl_name,  float32).reshape(ny, nx)
#********************
# mask
#--------------------
a2dp_full        = ma.masked_invalid(a2dp_full)
a2dp_lcl         = ma.masked_invalid(a2dp_lcl)
#--------------------
a2dp_lcl_full    = a2dp_lcl / abs(a2dp_full)

a2dp_lcl_full    = a2dp_lcl_full.filled(NaN)
#--------------------
a2dp_lcl_full.tofile(dp_lcl_full_name)
