from numpy import *

year   = 1980
mon    = 1

ny,nx  = 180,360

tagdir   = "/media/disk2/out/CMIP5/sa.one.MIROC5.historical/6hr/tagpr/c48h.tc48h/%04d%02d"%(year,mon)
plaindir = "/media/disk2/data/CMIP5/sa.one.MIROC5.historical/pr/%04d%02d"%(year,mon)

plainname = plaindir + "/pr.r1i1p1.%04d%02d.sa.one"%(year,mon)
cname     = tagdir   + "/pr.c.MIROC5.historical.r1i1p1.tc1000.c1000.f0500.%04d.%02d.sa.one"%(year,mon)
tcname     = tagdir   + "/pr.tc.MIROC5.historical.r1i1p1.tc1000.c1000.f0500.%04d.%02d.sa.one"%(year,mon)
fname     = tagdir   + "/pr.fbc.MIROC5.historical.r1i1p1.tc1000.c1000.f0500.%04d.%02d.sa.one"%(year,mon)
otname     = tagdir   + "/pr.ot.MIROC5.historical.r1i1p1.tc1000.c1000.f0500.%04d.%02d.sa.one"%(year,mon)


a2plain  = fromfile(plainname,float32).reshape(ny,nx)
a2c  = fromfile(cname,float32).reshape(ny,nx)
a2tc  = fromfile(tcname,float32).reshape(ny,nx)
a2f  = fromfile(fname,float32).reshape(ny,nx)
a2ot  = fromfile(otname,float32).reshape(ny,nx)

a2sum = a2c + a2tc + a2f + a2ot
print a2plain.sum()
print (a2c + a2tc + a2f + a2ot).sum()


