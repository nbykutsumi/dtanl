from ctrack_fsub import *
from numpy import *

miss = -9999
a= ones([180,360],float32)*-9999.0
nx, ny = 360, 180
a[100,100]=1
a[50,50] = 1
a[51,50] = 1
a[52,50] = 1

out = ctrack_fsub.mk_territory_deg_saone(a.T, 2, miss).T


