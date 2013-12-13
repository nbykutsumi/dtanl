from numpy import *
import gsmap_func
import calendar

year  = 2001
mon   = 1
eday  = calendar.monthrange(year,mon)[1]
ny,nx = 180,360
miss  = -9999.0

idir = "/home/utsumi/mnt/mizu.tank/utsumi/tag.pr/c48h.tc48h.bsttc1000.c1000.f0500/GSMaP.day/%04d%02d"%(year,mon)

name_all  = idir + "/pr.plain.%04d.%02d.sa.one"%(year,mon)
name_tc   = idir + "/pr.tc.%04d.%02d.sa.one"%(year,mon)
name_c    = idir + "/pr.c.%04d.%02d.sa.one"%(year,mon)
name_fbc  = idir + "/pr.fbc.%04d.%02d.sa.one"%(year,mon)
name_ot   = idir + "/pr.ot.%04d.%02d.sa.one"%(year,mon)

a2all  = fromfile(name_all,float32).reshape(ny,nx)
a2tc   = fromfile(name_tc,float32).reshape(ny,nx)
a2c    = fromfile(name_c,float32).reshape(ny,nx)
a2fbc  = fromfile(name_fbc,float32).reshape(ny,nx)
a2ot   = fromfile(name_ot,float32).reshape(ny,nx)

a2all  = ma.masked_equal(a2all, miss).filled(0.0)
a2tc   = ma.masked_equal(a2tc,  miss).filled(0.0)
a2c    = ma.masked_equal(a2c,   miss).filled(0.0)
a2fbc  = ma.masked_equal(a2fbc, miss).filled(0.0)
a2ot   = ma.masked_equal(a2ot,  miss).filled(0.0)

a2sum  = a2tc + a2c + a2fbc + a2ot

print a2all.sum(), a2sum.sum()


a2org   = zeros([ny,nx],float32)
orgdir    = "/media/disk2/data/GPCP1DD/v1.2/1dd/2001"
for day in range(1,eday+1):
  orgname     = orgdir + "/gpcp_1dd_v1.2_p1d.%04d%02d%02d.bn"%(year,mon,day)
  a2org_tmp   = flipud(fromfile(orgname, float32).reshape(ny,nx))
  a2org_tmp   =  ma.masked_equal(a2org_tmp, -99999.0).filled(0.0)
  a2org       = a2org + a2org_tmp

a2org = a2org / eday / (60*60*24.0)
print a2org.sum()


idir2 = "/media/disk2/out/JRA25/sa.one.anl_p/6hr/tagpr/c48h.tc48h/200101"
name_all2 = idir2 + "/pr.plain.bsttc1000.c1000.f0500.2001.01.GPCP1DD.sa.one"
name_tc2  = idir2 + "/pr.tc.bsttc1000.c1000.f0500.2001.0001.GPCP1DD.sa.one"
name_c2   = idir2 + "/pr.c.bsttc1000.c1000.f0500.2001.01.GPCP1DD.sa.one"
name_fbc2 = idir2 + "/pr.fbc.bsttc1000.c1000.f0500.2001.01.GPCP1DD.sa.one"
name_ot2  = idir2 + "/pr.ot.bsttc1000.c1000.f0500.2001.01.GPCP1DD.sa.one"

a2all2    = fromfile(name_all2, float32).reshape(ny,nx)
a2tc2     = fromfile(name_tc2,  float32).reshape(ny,nx)
a2c2      = fromfile(name_c2,   float32).reshape(ny,nx)
a2fbc2    = fromfile(name_fbc2, float32).reshape(ny,nx)
a2ot2     = fromfile(name_ot2,  float32).reshape(ny,nx)

a2sum2    = a2tc2 + a2c2 + a2fbc2 + a2ot2
print a2sum2.sum()

print "------------"
print "tc",a2tc.sum(), a2tc2.sum()
print "c",a2c.sum(), a2c2.sum()
print "fbc",a2fbc.sum(), a2fbc2.sum()
print "ot",a2ot.sum(), a2ot2.sum()
print "all-1", a2tc.sum() + a2c.sum() + a2fbc.sum() + a2ot.sum()
print "all-2", a2tc2.sum() + a2c2.sum() + a2fbc2.sum() + a2ot2.sum()


