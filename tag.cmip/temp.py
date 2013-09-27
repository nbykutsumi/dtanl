from numpy import *
ny,nx  = 180,360

idir= "/media/disk2/out/CMIP5/sa.one.MIROC5.rcp85/6hr/tagpr/c48h.tc48h/2080-2081.ALL.decomp"

dprname1 = idir + "/dpr.c.MIROC5.rcp85.r1i1p1.tc1000.c1000.f0500.2080-2081.ALL.sa.one"
dprname2 = idir + "/dpr2.c.MIROC5.rcp85.r1i1p1.tc1000.c1000.f0500.2080-2081.ALL.sa.one"

a2dpr1  = fromfile(dprname1,float32).reshape(ny,nx)
a2dpr2  = fromfile(dprname2,float32).reshape(ny,nx)

print a2dpr1
print a2dpr2
