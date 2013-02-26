from dtanl_fsub import *
from numpy import *
import ctrack_fig
#---------------------------
nx      = 360
ny      = 180

lllat   = 20.
urlat   = 60.
lllon   = 110.
urlon   = 160.

miss    = -9999.0
a2in    = ones([ny,nx],float32)*miss

a2in[36+90,140] = 1
a2in[36+90+1, 140] = 1
a2in[36+90+2, 140] = 1
a2in[36+90+3, 140] = 1
#a2in[36+90+4, 140] = 1


soname1 = "/home/utsumi/temp/temp1.png"
soname2 = "/home/utsumi/temp/temp2.png"


a2out   = dtanl_fsub.del_front_3grids(a2in, miss)
ctrack_fig.mk_pict_saone_reg(a2in,  soname=soname1, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon)
ctrack_fig.mk_pict_saone_reg(a2out, soname=soname2, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon)




