from numpy import *
import gsmap_func

rad = 300.
idir = "/media/disk2/out/chart/ASAS/front/agg/test/prof"
miss = -9999.

countc = idir + "/num.maskrad.0000km.cold.sa.one"
countw = idir + "/num.maskrad.0000km.warm.sa.one"
prc    = idir + "/pr.maskrad.0000km.cold.sa.one"
prw    = idir + "/pr.maskrad.0000km.warm.sa.one"

a2countc = fromfile(countc,float32).reshape(180,360)
a2countw = fromfile(countw,float32).reshape(180,360)
a2prc    = ma.masked_where(a2countc==0.0, fromfile(prc,float32).reshape(180,360))*60*60.
a2prw    = ma.masked_where(a2countw==0.0, fromfile(prw,float32).reshape(180,360))*60*60.


countinc = idir + "/num.maskrad.in.%04dkm.0000km.cold.sa.one"%(rad)
countinw = idir + "/num.maskrad.in.%04dkm.0000km.warm.sa.one"%(rad)
princ    = idir + "/pr.maskrad.in.%04dkm.0000km.cold.sa.one"%(rad)
prinw    = idir + "/pr.maskrad.in.%04dkm.0000km.warm.sa.one"%(rad)

a2countinc = fromfile(countinc,float32).reshape(180,360)
a2countinw = fromfile(countinw,float32).reshape(180,360)
a2princ    = ma.masked_where(a2countinc ==0.0, fromfile(princ,float32).reshape(180,360))*60.*60.
a2prinw    = ma.masked_where(a2countinw ==0.0, fromfile(prinw,float32).reshape(180,360))*60.*60


frontname1 = "/media/disk2/out/chart/ASAS/front/200404/front.ASAS.2004.04.05.00.saone"
frontname2 = "/media/disk2/out/chart/ASAS/front/200404/front.ASAS.2004.04.05.18.saone"
a2front1   = fromfile(frontname1,float32).reshape(180,360)
a2front2   = fromfile(frontname2,float32).reshape(180,360)

#-----------------------
a2gsmap1   = gsmap_func.timeave_gsmap_backward_saone(2004,4,5,0+1,2)*60*60.
a2gsmap2   = gsmap_func.timeave_gsmap_backward_saone(2004,4,5,18+1,2)*60*60.
a2gsmap1   = ma.masked_equal(gsmap_func.gsmap2global_one(a2gsmap1, miss), miss).filled(0.0)
a2gsmap2   = ma.masked_equal(gsmap_func.gsmap2global_one(a2gsmap2, miss), miss).filled(0.0)

#-----------------------
a2prmanw1  = ma.masked_where(a2front1 !=1.0 , a2gsmap1)
a2prmanc1  = ma.masked_where(a2front1 !=2.0 , a2gsmap1)

