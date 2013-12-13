import os, sys
from numpy import *
from mpl_toolkits.basemap import Basemap
import matplotlib
import matplotlib.pyplot as plt
from cf.plot import *

#dir1  = "/media/disk2/out/CMIP5/sa.one.MIROC5.rcp85/6hr/tagpr/c48h.tc48h.thpr0.50/2080-2099.ALL.decomp"
#
#
#tcname = dir1 + "/dpr.tc.dtot.MIROC5.rcp85.r1i1p1.tc1000.c1000.f0500.2080-2099.ALL.sa.one"
#cfname = dir1 + "/dpr.cf.dtot.MIROC5.rcp85.r1i1p1.tc1000.c1000.f0500.2080-2099.ALL.sa.one"
#otname = dir1 + "/dpr.ot.dtot.MIROC5.rcp85.r1i1p1.tc1000.c1000.f0500.2080-2099.ALL.sa.one"
#
#a2tc   = fromfile(tcname, float32).reshape(180,360)
#a2cf   = fromfile(cfname, float32).reshape(180,360)
#a2ot   = fromfile(otname, float32).reshape(180,360)
#a2sum  = a2tc + a2cf  + a2ot
sumname = "/media/disk2/out/CMIP5/sa.one.MME.rcp85/6hr/tagpr/c48h.tc48h.thpr0.50/2080-2099.ALL.decomp/dpr.plain.dtot.MME.rcp85.r1i1p1.tc1000.c1000.f0500.2080-2099.ALL.sa.one"
a2sum   = fromfile(sumname, float32).reshape(180,360)


plainname = "/media/disk2/out/CMIP5/sa.one.MME.rcp85/6hr/dpr.plain/2080-2099.ALL.decomp/dpr.plain.th0.50.MME.rcp85.r1i1p1.2080-2099.ALL.sa.one"
a2plain = fromfile(plainname,float32).reshape(180,360)

a2d    = a2plain - a2sum
