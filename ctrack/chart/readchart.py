import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import chart_para
from dtanl_fsub import *
#-------------------------------------------
region = "ASAS"
nx_fig,ny_fig    = chart_para.ret_nxnyfig(region)
lon0,lat0        = chart_para.ret_lonlat_center(region)
latts            = chart_para.ret_latts(region)
lllon, lllat, urlon, urlat \
                 = chart_para.ret_domain_corner(region)

xdom_first, xdom_last, ydom_first, ydom_last \
                 = chart_para.ret_xydom_first_last(region)
#------------------------------------------
jpgname = "./test/As_2004071500.jpg"
ajpg    = mpimg.imread(jpgname)
#
name_x_corres = "/home/utsumi/bin/dtanl/ctrack/chart/stereo.xfort.fig2saone.ASAS.bn"
name_y_corres = "/home/utsumi/bin/dtanl/ctrack/chart/stereo.yfort.fig2saone.ASAS.bn"
#



