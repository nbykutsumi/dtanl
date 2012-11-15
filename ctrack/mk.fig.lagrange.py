from numpy import *
from ctrack_fsub import *
import ctrack_para
import os, calendar, datetime
import matplotlib.pyplot as plt
import cf
from cf.plot import *
import gsmap_func
#*************************************************************
dpgradrange   = ctrack_para.ret_dpgradrange()
lclass        = dpgradrange.keys()

var           = "pr"

#vtype        = "GSMaP"  # "JRA", "GPCP1DD", "GSMaP"
#vtype        = "JRA"  # "JRA", "GPCP1DD", "GSMaP"
#vtype        = "GPCP1DD"  # "JRA", "GPCP1DD", "GSMaP"
#lvtype       = ["GSMaP", "NorESM1-M", "JRA", "GPCP1DD","MIROC5"]
lvtype       = ["MIROC5"]

latmin    = 30.0
latmax    = 60.0
#lonmin    = 120.
#lonmax    = 240.
lonmin    = 280
lonmax    = 350
miss_out  = -9999.0
sreg="%02d.%02d.%03d.%03d"%(latmin, latmax, lonmin, lonmax)

ny_eqgrid = 61
nx_eqgrid = 61
xrad      = (nx_eqgrid - 1)/2.0
yrad      = (ny_eqgrid - 1)/2.0

for vtype in lvtype:
  for iclass in lclass:    
    plt.clf()
    thgrad_min  = dpgradrange[iclass][0]
    thgrad_max  = dpgradrange[iclass][1] 
    #-- data names ---
    idir = "/home/utsumi/bin/dtanl/ctrack/temp"
    oname_mean   = idir + "/%s.%s.%s.%04.0f-%04.0f.bn"%(var, vtype, sreg, thgrad_min, thgrad_max)
    #-----------------
    bnd       = [1,3,5,7,9,11,13,15]
    #-----------------
    if var == "pr":
      if vtype in ["GPCP1DD"]:
        coef = 1.0
      else:
        coef = 60*60*24.0
    else:
      coef = 1.0
    #--
    a2mean_eqgrid = fromfile(oname_mean, float32).reshape(ny_eqgrid, nx_eqgrid)
    figname_mean = oname_mean[:-3] + ".png"
    plt.clf()
    #---------
    figmap   = plt.figure()
    axmap    = figmap.add_axes([0.0, 0.0, 1.0, 0.9])
    im       = axmap.imshow(a2mean_eqgrid * coef, origin="lower", interpolation="nearest", norm=BoundaryNormSymm(bnd), cmap="jet")

    # title
    stitle   = "%s class %02d lat%d-%d lon%d-%d"%(vtype, iclass, latmin, latmax, lonmin, lonmax) 
    axmap.set_title(stitle)

    # center point
    #axmap.plot(xrad, yrad, "x", s=100)
    axmap.scatter(xrad, yrad, marker="+",color="r", s=300)

    #-----------
    plt.savefig(figname_mean)
    plt.clf()
    print figname_mean

    # colorbar --
    figcbar   = plt.figure(figsize=(5, 0.6))
    axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
    bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
    plt.colorbar(im, boundaries=bnd_cbar, extend="both", cax=axcbar, orientation="horizontal")
    cbarname  = figname_mean[:-4] + ".cbar.png" 
    figcbar.savefig(cbarname)
 
    ##-- figure corr. coef --------
    #
    #a2cor_eqgrid = fromfile(oname_cor, float32).reshape(ny_eqgrid, nx_eqgrid)
    #figname_cor = oname_cor[:-3] + ".png"
    #plt.clf()
    #plt.imshow(a2cor_eqgrid, origin="lower", interpolation="nearest", vmin= -0.2, vmax=0.2)
    #plt.colorbar()
    #plt.savefig(figname_cor)
    #plt.clf()
    #print figname_cor
