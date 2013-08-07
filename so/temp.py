from dtanl_fsub import *
from numpy import *
import ctrack_fig
#---------------------------
lllat = 0.0
lllon = 60.0
urlat = 60.0
urlon = 230.0
miss  = -9999.0
ny,nx = 180,360
thnum = 9
idir = "/media/disk2/out/JRA25/sa.one.anl_p/6hr/front/200401"
iname = idir + "/front.M1_0.7.M2_4.0.2004.01.02.00.sa.one"
a2in = fromfile(iname, float32).reshape(180,360)

a2out = dtanl_fsub.del_front_lesseq_ngrids(a2in.T, miss,thnum).T

fig1  = "/home/utsumi/bin/dtanl/so/fig_in.png"
fig2  = "/home/utsumi/bin/dtanl/so/fig_out.png"
ctrack_fig.mk_pict_saone_reg(a2in, soname=fig1, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon)
ctrack_fig.mk_pict_saone_reg(a2out, soname=fig2, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon)

print fig1



