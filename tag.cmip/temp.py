import os, sys
from numpy import *
from mpl_toolkits.basemap import Basemap
import matplotlib
import matplotlib.pyplot as plt
from cf.plot import *

idir    = "/media/disk2/out/CMIP5/sa.one.MIROC5.rcp85/6hr/tagpr/c48h.tc48h/2080-2099.ALL.decomp"
iname_cf = idir  + "/dpr.cf.dtot.MIROC5.rcp85.r1i1p1.tc1000.c1000.f0500.2080-2099.ALL.sa.one"
iname_tc = idir  + "/dpr.tc.dtot.MIROC5.rcp85.r1i1p1.tc1000.c1000.f0500.2080-2099.ALL.sa.one"
iname_ot = idir  + "/dpr.ot.dtot.MIROC5.rcp85.r1i1p1.tc1000.c1000.f0500.2080-2099.ALL.sa.one"


a2cf     = fromfile(iname_cf, float32).reshape(180,360)
a2tc     = fromfile(iname_tc, float32).reshape(180,360)
a2ot     = fromfile(iname_ot, float32).reshape(180,360)

a2tot    = a2cf + a2tc + a2ot
