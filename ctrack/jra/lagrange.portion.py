from numpy import *
import ctrack_para
import ctrack_func
from cf.plot import *
import matplotlib.pyplot as plt
import os
#--------------------------
season    = "DJF"
latmin    = 30.0
#latmax    = 54.0
latmax    = 38.5
lonmin    = 60.0
lonmax    = 149.5
lvtype    = ["APHRO_MA","GSMaP","JRA","GPCP1DD"]
dpgradrange   = ctrack_para.ret_dpgradrange()
lclass        = dpgradrange.keys()
#aphromask = "TRUE"
aphromask = "FALSE"

ny    = 61
nx    = 61
xrad  = (nx-1)*0.5
yrad  = (ny-1)*0.5

sreg  = "%02d.%02d.%03d.%03d"%(latmin, latmax, lonmin, lonmax)
if aphromask =="TRUE":
  sidir = "/home/utsumi/bin/dtanl/ctrack/temp/%s/day/land/%s"%(season, sreg)
else:
  sidir = "/home/utsumi/bin/dtanl/ctrack/temp/%s/day/nomask/%s"%(season, sreg)
sodir = sidir + "/portion"
ctrack_func.mk_dir(sodir)
#-----------------------
for vtype in lvtype:
  #-------------------
  da2count   = {}
  da2mean    = {}
  da2sum     = {}
  da2portion = {}
  a2temp = zeros([ny,nx],float32)
  for iclass in lclass:
    thgrad_min  = dpgradrange[iclass][0]
    thgrad_max  = dpgradrange[iclass][1]
    #-- name ---------
    name_count  = sidir + "/count.day.%s.%s.%04.0f-%04.0f.bn"%(vtype, sreg, thgrad_min, thgrad_max)
    name_mean   = sidir + "/pr.day.%s.%s.%04.0f-%04.0f.bn"%(vtype, sreg, thgrad_min, thgrad_max)
  
    #-- load ---------
    da2count[iclass]  = fromfile(name_count, float32).reshape(ny, nx)
    da2mean[iclass]   = fromfile(name_mean,  float32).reshape(ny, nx)

  #---------------------  
  for iclass in lclass:
    da2sum[iclass]  = da2mean[iclass] * da2count[iclass]

  #---  
  for iclass in lclass[1:]:
    da2portion[iclass] = ma.masked_where(da2sum[0]==0.0, da2sum[iclass])/da2sum[0]
    da2portion[iclass].filled(0.0)

  ##--- figure -----
  #bnd       = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
  bnd       = arange(0,1.0+0.01, 0.1)
  for iclass in lclass[1:]:
    thgrad_min = dpgradrange[iclass][0]
    thgrad_max = dpgradrange[iclass][1]
    #--------------
    plt.clf()
    figmap  = plt.figure()
    axmap   = figmap.add_axes([0.0, 0.0, 1.0, 0.9])
    im      = axmap.imshow(da2portion[iclass], origin="lower", interpolation="nearest", norm=BoundaryNormSymm(bnd), cmap="jet")
    
    # title ----
    stitle  = "portion, %s class %02d lat%d-%d lon%d-%d, %s"%(vtype, iclass, latmin, latmax, lonmin, lonmax, season)
    #stitle  = stitle + "\n" + "mean = %.3f"%(mean(da2portion[iclass]))
    stitle  = stitle + "\n" + "portion :domain total = %.3f"%(da2sum[iclass].sum()/da2sum[0].sum())
    axmap.set_title(stitle)

    # center point --
    axmap.scatter(xrad, yrad, marker="+", color="r", s=300)

    # save ---
    name_portion  = sodir + "/portion.day.%s.%s.%04.0f-%04.0f.png"%(vtype, sreg, thgrad_min, thgrad_max)
    plt.savefig(name_portion)
    #plt.clf()
    print name_portion

    #-- colorbar ---
    figcbar  = plt.figure(figsize=(5,0.6))
    axcbar   = figcbar.add_axes([0, 0.4, 1.0, 0.6])
    bnd_cbar = bnd
    plt.colorbar(im, boundaries = bnd_cbar, cax=axcbar, orientation="horizontal")

    # cbar name --
    name_cbar = sodir + "/cbar.portion.%s.png"%(vtype)
    figcbar.savefig(name_cbar)
