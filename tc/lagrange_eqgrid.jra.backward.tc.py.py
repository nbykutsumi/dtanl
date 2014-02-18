from numpy import *
from ctrack_fsub import *
import tc_func
import ctrack_func, ctrack_para, tc_para, gsmap_func
import os, sys, calendar, datetime
import matplotlib.pyplot as plt
import cf
import gsmap_func
#*************************************************************
singleday = False
#singleday = True
#calcflag  = False
calcflag  = True
bsttc     = True
#iyear     = 1997
#eyear     = 2012
iyear     = 2001
eyear     = 2009
lyear     = range(iyear,eyear+1)
lseason   = ["ALL"]
tstp      = "6hr"
nx_org    = 360
ny_org    = 180
sresol    = "anl_p"
var       = "pr"
thdura    = 48
iday      = 1
lhour     = [0, 6, 12, 18]
#region    = "PNW"
region    = "GLB"
#thgrad_min    = 500.0  # Pa/1000km
#thgrad_max    = 1000.0 # Pa/1000km
dpgradrange   = ctrack_para.ret_dpgradrange()
#lclass        = dpgradrange.keys()
lclass        = [0]

#vtype        = "GSMaP"  # "JRA", "GPCP1DD", "GSMaP"
#vtype        = "JRA"  # "JRA", "GPCP1DD", "GSMaP"
#vtype        = "GPCP1DD"  # "JRA", "GPCP1DD", "GSMaP"
#lvtype       = ["GSMaP", "JRA", "GPCP1DD"]
lvtype         = ["GSMaP"]
#lvtype        = ["GPCP1DD"]
#lvtype        = ["APHRO_MA"]

#---------------------
miss          = -9999.
nradeqgrid    = 30
nx     = nradeqgrid*2 + 1
ny     = nradeqgrid*2 + 1
#---------------------
llkey = [[vtype, season, iclass] for vtype in lvtype for season in lseason for iclass in lclass]
for vtype, season, iclass in llkey:
  lmon     = ctrack_para.ret_lmon(season)
  thgrad_min    = dpgradrange[iclass][0]
  thgrad_max    = dpgradrange[iclass][1]

  #---- dummy ------
  a2sum   = zeros([ny, nx],float32)
  a2num   = zeros([ny, nx],float32)
  #-----------------
  for year in lyear:
    for mon in lmon:
      print var, vtype, year, mon
      if bsttc == True:
        idir_root    = "/media/disk2/out/JRA25/sa.one.anl_p/composite/tc.bst.%s.%s.%s"%(var,vtype,region)
      elif bsttc == False:
        idir_root    = "/media/disk2/out/JRA25/sa.one.anl_p/composite/tc.obj.%s.%s.%s"%(var,vtype,region)
      else:
        print "check TC best flag"
        sys.exit()
      #
      idir        = idir_root + "/%04d%02d"%(year,mon)
      #-------
      iname_sum   = idir + "/sum.%04.0f-%04.0f.bn"%(thgrad_min, thgrad_max)
      iname_num   = idir + "/num.%04.0f-%04.0f.bn"%(thgrad_min, thgrad_max)
      #-------
      a2sum_tmp   = fromfile(iname_sum, float32).reshape(ny,nx)
      a2num_tmp   = fromfile(iname_num, float32).reshape(ny,nx)
      #
      a2sum       = a2sum  + a2sum_tmp
      a2num       = a2num  + a2num_tmp
  #---- mean   -----
  a2mean    = (ma.masked_where(a2num == 0.0, a2sum) / a2num).filled(0.0)
  #---- out name ---
  odir_root = idir_root
  odir      = odir_root + "/%04d-%04d.%s"%(iyear,eyear,season)
  ctrack_func.mk_dir(odir)
  oname     = odir + "/mean.%04.0f-%04.0f.bn"%(thgrad_min, thgrad_max)
  a2mean.tofile(oname)

  #-- figure ---------------------
  if var == "pr":
    #if vtype in ["GPCP1DD"]:
    if vtype in ["XXXX"]:
      figcoef = 1.0
    else:
      figcoef = 60*60*24.0
  else:
    figcoef = 1.0
  #--
  a2mean    = fromfile(oname, float32).reshape(ny, nx)
  #-- name --
  figname   = odir + "/tc.%s.%s.%04d-%04d.%s.%s.%04.0f-%04.0f.png"%(var,vtype,iyear,eyear,season,region,thgrad_min, thgrad_max)
  #----------
  plt.clf()
  plt.imshow(a2mean * figcoef, origin="lower", interpolation="nearest", vmin= 0.0, vmax=20.0)
  plt.colorbar()
  plt.savefig(figname)
  plt.clf()
  print figname
  
