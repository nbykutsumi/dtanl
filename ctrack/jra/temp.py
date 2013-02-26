import matplotlib.pyplot as plt
from numpy import *
import ctrack_fig
from dtanl_fsub import *

siname = "/media/disk2/data/JRA25/sa.one/const/topo/topo.sa.one"
a2in   = fromfile(siname, float32).reshape(180,360)
a2grad = dtanl_fsub.mk_a2grad_abs_saone(a2in.T).T *1000.0

lllon = 67.5
lllat = 0.5
urlon = 208.5
urlat = 70.5
bnd   = arange(-50,1000.0+10, 50)
a2shade  = ma.masked_greater(a2in, 1500.0).filled(-9999.0)
a2shade  = ma.masked_where( a2grad >7, a2shade).filled(-9999.0)
ctrack_fig.mk_pict_saone_reg(a2in, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, a2shade=a2shade, bnd=bnd)



