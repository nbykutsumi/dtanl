from numpy import *
#import dtanl_p_swa
#nz =3
#dP = 8.5
#a1lev = arange(nz)
#print a1lev, type(a1lev)
#print nz, type(nz)
#dtanl_p_swa.dtanl_p_swa.calc_swa(3, dP, a1lev)


import temp
nz = 3
dP =8.5
alev = arange(nz)
Tsfc = 10.0
qsfc = 0.5
Psfc = 1013.0
awap = arange(nz)*3

out = temp.dtanl_p_swa.calc_swa(dP,alev, Tsfc, qsfc, Psfc, awap)
print out

