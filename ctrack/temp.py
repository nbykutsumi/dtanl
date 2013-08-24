import ctrack_func
from ctrack_fsub import *
miss = -9999.0
a = ones([180,360],float32)*miss
a[100:110,150] = 1.0
b = ctrack_fsub.mk_8gridsmask_saone(a.T,miss).T





