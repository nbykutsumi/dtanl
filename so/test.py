from dtanl_fsub import *
from numpy import *
iname = "/media/disk2/data/CMIP5/sa.one.MIROC5.historical/ta/199801/ta.0850hPa.r1i1p1.199801010000.sa.one"
miss = -9999.0

a2in = fromfile(iname,float32).reshape(180,360)
a2in_tmp = ma.masked_equal(a2in,miss).filled(274.0)

a2out1 = dtanl_fsub.mk_a2grad_abs_saone(a2in.T, miss=miss).T
a2out2 = dtanl_fsub.mk_a2grad_saone(a2in.T, miss=miss)

a2out3 = dtanl_fsub.mk_a2frontmask2(a2in_tmp.T).T * (1000.0*100.0)
a2out4 = dtanl_fsub.mk_a2frontmask2(a2in.T, miss=miss).T * (1000.0*100.0)

a2out5 = dtanl_fsub.mk_a2frontmask1(a2in_tmp.T).T * (1000.0*100.0)**2.0
a2out6 = dtanl_fsub.mk_a2frontmask1(a2in.T, miss=miss).T * (1000.0*100.0)**2.0


print a2out1
print a2out2
print a2out3
print a2out4
print a2out5
print a2out6
