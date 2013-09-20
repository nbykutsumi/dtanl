from numpy import *
from chart_fsub import *
nx,ny = 360,180
miss  = -9999.0

a2loc = ones([ny,nx],float32)*miss
a2loc[100,100] = 1
a2loc[150,150] = 1


a2pr = ones([ny,nx],float32)*miss
a2pr[100,100] = 1.0
a2pr[101,100] = 2.0
a2pr[100,101] = 3.0

a2pr[150,150] = 30.0
a2pr[151,151] = 20.0
a2pr[149,149] = 10.0

a1pr = chart_fsub.mk_a1pr_9gridmax(a2loc.T, a2pr.T, miss)
print a1pr
