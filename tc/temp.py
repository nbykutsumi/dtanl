from numpy import *
import tc_func
year = 2001
idir ="/media/disk2/data/ibtracs/v03r04"
iname = idir + "/Year.%04d.ibtracs_all.v03r04.csv"%(year)

dlonlat = tc_func.ret_ibtracs_dlonlat(year)
dxy = tc_func.ret_ibtracs_dpyxy_saone(year)

lxy = [(50,50),(80,80)]
a2out = tc_func.lpyxy2map_saone(lxy, 1.0, -9999.0)



