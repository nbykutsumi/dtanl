from numpy import *
import os
#----------------------------------------------------
nx = 144
ny = 96
nz = 8
#----------------------------------------------------
tstp = "day"
model = "NorESM1-M"
ens = "r1i1p1"
xth = 99
miss = -9999
#####################################################
# set sofiles
#---------------------------
somapdir   = "/media/disk2/out/CMIP5/%s/%s/scales/%s/map"%(tstp, model, ens)
#
sodPrec  = somapdir + "/dP.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
soDfull  = somapdir + "/dP.full.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
#
print os.access(sodPrec, os.F_OK)
print os.access(soDfull, os.F_OK)
sanldir = somapdir + "/anl"
#-----------------------------
try:
  os.makedirs(sanldir)
except OSError:
  pass
#-----------------------------
sdifbin = sanldir + "/dif.full.dP.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
sdifbin_masked = sanldir + "/masked.dif.full.dP.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
print sdifbin
#-----------------------------
adP    = fromfile(sodPrec, float32)
aDfull = fromfile(soDfull, float32)
#--- mask --------------------
adP    = ma.masked_equal(adP, miss)
aDfull = ma.masked_equal(aDfull, miss)
#-----------------------------
adif_masked = ma.filled(aDfull - adP , NaN)
adif        = ma.filled(aDfull - adP , miss)
#-----------------------------
adif.tofile(sdifbin)
adif_masked.tofile(sdifbin_masked)
#-----------------------------
#################################
#  pict
#################################
cmdpict_withsea = "/home/utsumi/oekaki/dtanl/cmip/dtanl.gmt"
#---------
for sea in ["withsea"]:
  #------------------------
  if (sea == "withsea"):
    ifile       = sdifbin_masked
    ofile_title = sdifbin_masked[:-3]
    cmd         = cmdpict_withsea
  #------------------------
  scalestep = 20
  title = "dP.fullscaling-dP"
  #cptfile = "/home/utsumi/oekaki/dtanl/cmip/cpt/polar.-100.100.cpt"
  cptfile = "/home/utsumi/oekaki/dtanl/cmip/cpt/polar.-20.20.cpt"
  #---------
  os.system("%s %s %s %s %s %s"%(cmd, ifile, cptfile, ofile_title, title, scalestep))
  print ofile_title
