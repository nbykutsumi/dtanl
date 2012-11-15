from numpy import *
import ctrack_para
import cf
import matplotlib.pyplot as plt

lvtype     = ["pr"]
ldataset   = ["GSMaP", "JRA", "GPCP1DD", "NorESM1-M"]
season  = "DJF"
lllat   = 30.0
urlat   = 60.0
lllon   = 120.0
urlon   = 240.0
#lllon   = 280.
#urlon   = 350.

#-- do not change --
lat_first = -89.5
lon_first = 0.5
dlat      = 1.0
dlon      = 1.0
#-------------------
nx      = 61
ny      = 61
dkm     = 100.0  # equal area grid resolution [km]
xc      = (nx-1)/2
yc      = (ny-1)/2   
#--------------------
dpgradrange   = ctrack_para.ret_dpgradrange()
lclass        = dpgradrange.keys() 
#--------------------
def find_radclass(dbnd, rad):
  lradclass   = sort(dbnd.keys())
  for irad in lradclass:
    rad_min   = dbnd[irad][0]
    rad_max   = dbnd[irad][1]
    if (rad_min <= rad < rad_max):
      break
  #
  return irad
#--------------------
def latlon2yx(lat, lon, lat_first, lon_first, dlat, dlon):
  iy    = int( (lat + 0.5*dlat - lat_first)/dlat )
  ix    = int( (lon + 0.5*dlon - lon_first)/dlon )
  return iy, ix
#--------------------

idir    = "/home/utsumi/bin/dtanl/ctrack/temp"
for vtype in lvtype:
  for dataset in ldataset:
    #--- mean data ------
    if dataset == "GSMaP":
      mdir   = "/media/disk2/data/GSMaP/sa.one/3hr/ptot"
      mname  = mdir + "/gsmap_mvk.2001-2004.%s.sa.one"%(season)
    elif dataset == "GPCP1DD":
      mdir   = "/media/disk2/data/GPCP1DD/data/1dd"
      mname  = mdir + "/gpcp_1dd_v1.1_p1d.2001-2004.%s.bn"%(season)
    elif dataset == "JRA":
      mdir   = "/media/disk2/data/JRA25/sa.one/6hr/PR"
      mname  = mdir + "/fcst_phy2m.PR.2001-2004.%s.sa.one"%(season)
    elif dataset in ["NorESM1-M"]:
      mdir   = "/media/disk2/data/CMIP5/sa.one/pr/3hr/%s/historical/r1i1p1"%(dataset)
      mname  = mdir + "/pr_3hr_NorESM1-M_historical_r1i1p1.1980-2004.%s.sa.one"%(season)
    #
    iy_min, ix_min = latlon2yx(lllat, lllon, lat_first, lon_first, dlat, dlon )
    iy_max, ix_max = latlon2yx(urlat, urlon, lat_first, lon_first, dlat, dlon )
    a2m      = fromfile(mname, float32).reshape(180,360)
    mval     = mean(a2m[iy_min:iy_max, ix_min:ix_max]) 
    if dataset == "GPCP1DD":
      mval   = mval / (60*60*24.0)

    #for iclass in lclass:
    da1mval      = {}
    da1mval_std  = {}
    #for iclass in [0]:
    for iclass in lclass:
      #--------------------
      lmval      = []
      lradclass  = arange(dkm*0.5, (nx-1)*0.5*dkm+ dkm*0.5 + 1, dkm*2)
      dval       = {}
      dnum       = {}
      dbnd       = {}
      dmval      = {}
      for irad in lradclass:
        dval[irad] = 0.0
        dnum[irad] = 0.0
        dbnd[irad] = [irad - dkm, irad+dkm]

      #--------------------
      pgrad_min  = dpgradrange[iclass][0]
      pgrad_max  = dpgradrange[iclass][1]
      #siname     = idir + "pr.GSMaP.30.60.120.240.1500-100000000000.png"
      siname     = idir + "/%s.%s.%d.%d.%d.%d.%04d-%04d.bn"%(vtype, dataset, lllat, urlat, lllon, urlon, pgrad_min, pgrad_max)
      a2in       = fromfile(siname, float32).reshape(ny, nx)
      #
      for iy in range(ny):
        for ix in range(nx):
          rad    = ( ((ix - xc)**2 + (iy - yc)**2)**0.5 )*dkm
          irad   = find_radclass(dbnd, rad)
          dval[irad] = dval[irad] + a2in[iy, ix]
          dnum[irad] = dnum[irad] + 1.0
      #----------
      for irad in lradclass:
        lmval.append(dval[irad] / dnum[irad])
      #----------
      da1mval[iclass]     = array(lmval) * 60*60*24.0
      da1mval_std[iclass] = array(lmval) / mval

    #- plot figure ----
    figname             = idir + "/pict" + "/rad.%s.%s.%d.%d.%d.%d.%s.png"%(vtype, dataset, lllat, urlat, lllon, urlon, season)
    stdname             = idir + "/pict" + "/std.rad.%s.%s.%d.%d.%d.%d.%s.png"%(vtype, dataset, lllat, urlat, lllon, urlon, season)
    
    #-- mval ------------
    plt.clf()
    for iclass in lclass[1:]:
      plt.plot(lradclass, da1mval[iclass])
    #
    plt.xlim(0, lradclass[-1])
    plt.ylim(0, 10)
    plt.title("%s.%s.%d.%d.%d.%d.%02d.%s"%(vtype, dataset, lllat, urlat, lllon, urlon, iclass, season))
    plt.legend(map(str, lclass[1:]), "upper right"  )
    plt.savefig(figname)
    print figname

    #-- std_mval ---------
    plt.clf()
    for iclass in lclass[1:]:
      plt.plot(lradclass, da1mval_std[iclass])
    #
    plt.xlim(0, lradclass[-1])
    plt.ylim(0, 4)
    plt.title("std.%s.%s.%d.%d.%d.%d.%02d.%s"%(vtype, dataset, lllat, urlat, lllon, urlon, iclass, season))
    plt.legend(map(str, lclass[1:]), "upper right"  )
    plt.savefig(stdname)
    print figname

