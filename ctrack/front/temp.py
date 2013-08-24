from ctrack_fsub import *
from numpy import *
import front_func
import ctrack_para, front_para
thfmask1t, thfmask2t, thfmask1q, thfmask2q   = front_para.ret_thfmasktq()

ny,nx      = 180,360
thorog     = ctrack_para.ret_thorog()
thgradorog = ctrack_para.ret_thgradorog()
thgrids    = front_para.ret_thgrids()
miss       = -9999.0

orogname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
gradname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/maxgrad.0200km.sa.one"
a2orog     = fromfile(orogname, float32).reshape(ny,nx)
a2gradorog = fromfile(gradname, float32).reshape(ny,nx)

iname1t = "/media/disk2/out/JRA25/sa.one.anl_p/6hr/front.t/200404/front.t.M1.2004.04.06.00.sa.one"
iname2t = "/media/disk2/out/JRA25/sa.one.anl_p/6hr/front.t/200404/front.t.M2.2004.04.06.00.sa.one"
a2pott1 = fromfile(iname1t,float32).reshape(180,360)
a2pott2 = fromfile(iname2t,float32).reshape(180,360)

a2loct  = front_func.complete_front_t_saone(a2pott1, a2pott2, thfmask1t, thfmask2t, a2orog, a2gradorog, thorog, thgradorog, thgrids, miss )
print a2loct.max()

iname1q = "/media/disk2/out/JRA25/sa.one.anl_p/6hr/front.q/200404/front.q.M1.2004.04.06.00.sa.one"
iname2q = "/media/disk2/out/JRA25/sa.one.anl_p/6hr/front.q/200404/front.q.M2.2004.04.06.00.sa.one"
a2potq1 = fromfile(iname1q,float32).reshape(180,360)
a2potq2 = fromfile(iname2q,float32).reshape(180,360)

a2locq  = front_func.complete_front_q_saone(a2loct, a2potq1, a2potq2, thfmask1q, thfmask2q, a2orog, a2gradorog, thorog, thgradorog, thgrids, miss)

