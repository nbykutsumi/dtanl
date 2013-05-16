import ctrack_fig
from numpy import *

idir1  = "/media/disk2/data/JRA25/sa.one/6hr/anl_p.SPFH/200101"
idir2  = "/media/disk2/data/JRA25/sa.one/6hr/SPFH/200101"

iname1 = idir1 + "/anl_p.SPFH.0850hPa.2001010100.sa.one"
iname2 = idir2 + "/anl_p25.SPFH.0850hPa.2001010100.sa.one"


a1  = fromfile(iname1, float32).reshape(180,360)
a2  = fromfile(iname2, float32).reshape(180,360)

#ctrack_fig.mk_pict_saone_reg(a1, soname="./a1.png")
#ctrack_fig.mk_pict_saone_reg(a2, soname="./a2.png")




