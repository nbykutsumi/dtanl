from dtanl_fsub import *
from numpy import *
import ctrack_fig
ny,nx = 180,360
miss  = 0.0
thnum = 8.0
wgtflag = 0

a2rat = dtanl_fsub.mk_a2arearat_sphere_saone().T

a2in = zeros([ny,nx],float32)
a2in[90,100:108] = 1.0
a2in[91,104:108] = 1.0
a2in[80,100:108] = 1.0
a2in[81,104:108] = 1.0
a2in[70,100:108] = 1.0
a2in[71,104:108] = 1.0
a2in[60,100:108] = 1.0
a2in[61,104:108] = 1.0
a2in[50,100:108] = 1.0
a2in[51,104:108] = 1.0
a2in[40,100:108] = 1.0
a2in[41,104:108] = 1.0
a2in[30,100:108] = 1.0
a2in[31,104:108] = 1.0
a2in[20,100:108] = 1.0
a2in[21,104:108] = 1.0

a2out = dtanl_fsub.del_front_lesseq_ngrids(a2in.T, miss, thnum, wgtflag).T
print sum(a2out)

