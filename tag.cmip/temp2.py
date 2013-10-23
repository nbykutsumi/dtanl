from numpy import *
ny,nx  = 180,360

iyear  = 2080
eyear  = 2099

hisdir = "/media/disk2/out/CMIP5/sa.one.MIROC5.historical/6hr/tagpr/c48h.tc48h/%04d-%04d.ALL"%(iyear,eyear)
futdir = "/media/disk2/out/CMIP5/sa.one.MIROC5.rcp85/6hr/tagpr/c48h.tc48h/%04d-%04d.ALL"%(iyear,eyear)
decdir = "/media/disk2/out/CMIP5/sa.one.MIROC5.rcp85/6hr/tagpr/c48h.tc48h/%04d-%04d.ALL.decomp"%(iyear,eyear)
ny,nx  = 180,360

dpr_c   = decdir + "/dpr.c.dtot.MIROC5.rcp85.r1i1p1.tc1000.c1000.f0500.%04d-%04d.ALL.sa.one"%(iyear,eyear)
dpr_f  = decdir + "/dpr.fbc.dtot.MIROC5.rcp85.r1i1p1.tc1000.c1000.f0500.%04d-%04d.ALL.sa.one"%(iyear,eyear)
dpr_tc  = decdir + "/dpr.tc.dtot.MIROC5.rcp85.r1i1p1.tc1000.c1000.f0500.%04d-%04d.ALL.sa.one"%(iyear,eyear)
dpr_ot  = decdir + "/dpr.ot.dtot.MIROC5.rcp85.r1i1p1.tc1000.c1000.f0500.%04d-%04d.ALL.sa.one"%(iyear,eyear)

a2pr_c   = fromfile(dpr_c, float32).reshape(ny,nx)
a2pr_f   = fromfile(dpr_f, float32).reshape(ny,nx)
a2pr_tc  = fromfile(dpr_tc, float32).reshape(ny,nx)
a2pr_ot  = fromfile(dpr_ot, float32).reshape(ny,nx)
a2dall   = a2pr_c + a2pr_f + a2pr_tc + a2pr_ot


dplain   = "/media/disk2/data/CMIP5/sa.one.MIROC5.rcp85/pr/%04d-%04d.ALL/dif.pr.MIROC5.rcp85.r1i1p1.%04d-%04d.ALL.sa.one"%(iyear,eyear,iyear,eyear)
a2dplain = fromfile(dplain,float32).reshape(ny,nx)

sa=a2dall - a2dplain

print sa
