from numpy import *
import gsmap_func
from ctrack_fsub import *
#----------------------------------------------
idir    = "/media/disk2/out/chart/ASAS/front/agg/2004/04/prof"
numw    = idir  + "/num.maskrad.0000km.0000km.warm.sa.one"
numinw  = idir  + "/num.maskrad.in.0300km.0000km.warm.sa.one"

prw     = idir  + "/pr.0000km.warm.sa.one"
prinw   = idir  + "/pr.maskrad.in.0300km.0000km.warm.sa.one"
#
a2numw  = fromfile(numw,float32).reshape(180,360)
a2numinw= fromfile(numinw,float32).reshape(180,360)
a2prw   = fromfile(prw,float32).reshape(180,360)*60*60.
a2prinw = fromfile(prinw,float32).reshape(180,360)*60*60.

print "prw,   numw  ",a2prw.sum(), a2numw.sum()
print "prinw, numinw",a2prinw.sum(), a2numinw.sum()
