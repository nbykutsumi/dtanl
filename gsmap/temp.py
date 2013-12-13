from numpy import *
import gsmap_func

a1,b1 = gsmap_func.timeave_gsmap_backward_nmiss_saone(2001,1,20,0,6,relaxflag=False)
a2,b2 = gsmap_func.timeave_gsmap_backward_nmiss_saone(2001,1,20,0,6,relaxflag=True)

print a1
print a2
