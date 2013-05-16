import gsmap_func
from numpy import *
#------------------------
iyear = 2001
eyear = 2004
season = "ALL"
idir = "/media/disk2/out/JRA25/sa.one/6hr/tagpr/%04d-%04d/%s"%(iyear,eyear,season)
nhour = 1

ltag = ["tc","c","fbc","nbc","ot"]
#ltag  = ["tc","c","fbc","nbc","ot"]

nx,ny  = 360,180
miss   = -9999.0
diname = {}
da2in  = {}
a2all  = zeros([ny,nx],float32)
for tag in ltag:
  diname[tag] = idir + "/rfreq.tc05.c10.f05.%04d-%04d.%s.mov%02dhr.99.90.GSMaP.%s.sa.one"%(iyear,eyear,season, nhour, tag)
  da2in[tag]  = fromfile(diname[tag], float32).reshape(ny,nx)
  a2all       = a2all  + ma.masked_equal(da2in[tag], miss).filled(0.0)
