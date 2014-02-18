from dtanl_fsub import *
from numpy import *
import ctrack_fig
ny,nx = 180,360
miss  = -9999.0

p1 = 1000.0*100.0
p2 = 500*100.0
t1 = 20.0+ 273.15
q1 = 0.008

t2 = dtanl_fsub.t1_to_t2(p1,p2,t1,q1)
print t2, t2-273.15

a2t1 = ones([ny,nx],float32)*t1
a2q1 = ones([ny,nx],float32)*q1

a2t1[0,0:10] = miss

a2t2 = dtanl_fsub.a2t1_to_a2t2(p1,p2, a2t1.T, a2q1.T, miss).T
print a2t2
