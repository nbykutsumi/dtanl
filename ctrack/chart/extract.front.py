import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import chart_para
from numpy import *
#from chart_fsub import *
from chart_fsub import *
#***************************************
region   = "ASAS"
jpgname  = "./As_2004071500.jpg"
ajpg     = mpimg.imread(jpgname)
nx_fig,ny_fig    = chart_para.ret_nxnyfig(region)
lon0,lat0        = chart_para.ret_lonlat_center(region)
latts            = chart_para.ret_latts(region)
lllon, lllat, urlon, urlat \
                 = chart_para.ret_domain_corner(region)
miss     = -9999.0
#---------------------------------------
a2one    = ones([ny_fig,nx_fig],float32)
a2r      = ajpg[:,:,0]
a2g      = ajpg[:,:,1]
a2b      = ajpg[:,:,2]

a2front  = a2one*miss
#-- warm front ----
a2mask   = ma.masked_where(a2r < 130, a2one)
a2mask   = ma.masked_where(a2g > 30, a2mask)
a2mask   = ma.masked_where(a2b > 30, a2mask)
a2mask   = a2mask.filled(miss)
a2front  = ma.masked_where(a2mask != miss, a2front).filled(1.0)

##-- cold front ----
a2mask   = ma.masked_where(a2r > 30, a2one)
a2mask   = ma.masked_where(a2g > 30, a2mask)
a2mask   = ma.masked_where(a2b < 110, a2mask)
a2mask   = a2mask.filled(miss)
a2front  = ma.masked_where(a2mask != miss, a2front).filled(2.0)
#
##-- occ front
a2mask   = ma.masked_where(a2r < 160, a2one)
a2mask   = ma.masked_where(a2g > 80, a2mask)
a2mask   = ma.masked_where(a2b < 160, a2mask)
a2mask   = a2mask.filled(miss)
a2front  = ma.masked_where(a2mask != miss, a2front).filled(3.0)

#--
name_x_corres = "/home/utsumi/bin/dtanl/ctrack/chart/stereo.xfort.fig2saone.ASAS.bn"
name_y_corres = "/home/utsumi/bin/dtanl/ctrack/chart/stereo.yfort.fig2saone.ASAS.bn"
#--
a2xfort_corres= fromfile(name_x_corres, float32).reshape(ny_fig, nx_fig)
a2yfort_corres= fromfile(name_y_corres, float32).reshape(ny_fig, nx_fig)

#--
a2front_saone = chart_fsub.chartfront2saone(\
                  a2front.T, a2xfort_corres.T, a2yfort_corres.T,\
                  miss, nx_fig, ny_fig).T



