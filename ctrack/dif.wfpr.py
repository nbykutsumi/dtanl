from mpl_toolkits.basemap import Basemap
import ctrack_para
import ctrack_func as func
from numpy import *
import os, sys
from cf.plot import *
import matplotlib.pyplot as plt
import matplotlib
import pylab
#***************************************
iyear_his   = 1990
eyear_his   = 1999
iyear_fut   = 2086
eyear_fut   = 2095 
nx          = 144
ny          = 96
model       = "NorESM1-M"
ens         = "r1i1p1"
thdura      = 24
season      = "DJF"
lon_first   = 0.0
lat_first   = -90.0
dlon        = 2.5
dlat        = 1.8947368

xth         = 0.0
crad        = 1000.0
#***************************************
# for mapping
lats        = linspace(-90.0, 90.0, ny)
lons        = linspace(0.0, 360.0 -  360.0/nx, nx)
#lllat       = 15.0
#lllon       = 120.0
#urlat       = 50.0
#urlon       = 140.0

lllat       = -90.0
lllon       = 0.0
urlat       = 90.0
urlon       = 360.0

meridians   = 30.0
parallels   = 30.0

#
nnx         = int( (urlon - lllon)/ dlon)
nny         = int( (urlat - lllat)/ dlat)

#***************************************
mnum_min    = 1.0
#***************************************
diyear  = {"his": iyear_his, "fut": iyear_fut}
deyear  = {"his": eyear_his, "fut": eyear_fut}
#***************************************
(imon, emon) = ctrack_para.ret_im_em(season)
#***************************************
dexpr   = {"his": "historical", "fut": "rcp85", "dif": "dif"}
#***************************************
lera    = ["fut", "his"]
lvar    = ["num", "sp", "mnum"]
ldifvar = ["drnum", "drtotnum", "dmp"]
#***************************************
# class
#-----------------------------
dpgradrange   = ctrack_para.ret_dpgradrange()
cmin          = dpgradrange[0][0]

lclass        = dpgradrange.keys()
nclass        = len(lclass) -1
#***************************************
# wbin
#-----------------------------
dlwbin        = ctrack_para.ret_dlwbin()
liw           = dlwbin.keys()
nwbin         = len(liw)
#***************************************
oekakidir     = "/home/utsumi/bin/dtanl/ctrack/oekaki"

#----------------------
# colormap
#----------------------
def ret_colormap(scale):
  dcm  = {}
  if scale in  ["dpdf_c", "dpdf_w", "dp_w", "frac.dpdf_c", "frac.dpdf_w", "frac.dp_w"]:
    #--------
    dcm[scale] = pylab.cm.get_cmap("RdBu")
  elif scale in lscale2:
    dcm[scale] = pylab.cm.get_cmap("RdBu")
  else:
    dcm[scale] = pylab.cm.get_cmap("RdBu")
  return dcm[scale]
#
#***************************************
#  read orography
#----------------------
orogdir_root = "/media/disk2/data/CMIP5/bn/orog/fx/%s/%s/r0i0p0"%(model, "historical")
orogname     = orogdir_root + "/orog_fx_%s_%s_r0i0p0.bn"%(model, "historical")
a2orog         = fromfile(orogname, float32).reshape(ny,nx)

#*******************************************************************
# dirs
#-------------------------
ddir_root        = {}
ddir_root["his"] = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d"%(model, dexpr["his"], ens, thdura, imon, emon, nclass, cmin )

ddir_root["fut"] = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d"%(model, dexpr["fut"], ens, thdura, imon, emon, nclass, cmin)

ddir_root["dif"] = "/media/disk2/out/CMIP5/day/%s/dif/%s/%04d-%04d.%04d-%04d/tracks/dura%02d/%02d-%02d/c%02d/cmin%04d"%(model, dexpr["fut"], diyear["his"], deyear["his"], diyear["fut"], deyear["fut"], thdura, imon, emon, nclass, cmin)
#-----
ddir  = {}
dname = {}
for era in lera:
  for var in lvar:
    ddir[era, var]  =  ddir_root[era] + "/%s"%(var)
#--------------------------
# dif dirs
#--------------------------
#difdir_root = "/media/disk2/out/CMIP5/day/%s/dif/%s/%04d-%04d.%04d-%04d/tracks/dura%02d/wfpr"%(model, dexpr["fut"], diyear["his"], deyear["his"], diyear["fut"], deyear["fut"], thdura)
difdir_root  = ddir_root["dif"]

ddifdir = {}
for difvar in ldifvar:
  ddifdir[difvar] = difdir_root + "/%s"%(difvar)
  func.mk_dir(ddifdir[difvar])
#---
#**********************
# input names for each class
#----------------------
dname  = {}
for class_lb in lclass[1:]:
  for era in lera:
    expr = dexpr[era]
    for var in lvar:
      for iclass in lclass:
        if iclass == 0:
          dname[class_lb, era, var, iclass] =  ddir[era, var] + "/acc.%s.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(var, xth, cmin, class_lb, nclass, crad, nwbin, season, model, expr, ens )
        else:
          dname[class_lb, era, var, iclass] =  ddir[era, var] + "/%s.p%05.2f.cmin%04d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(var, xth, cmin, iclass, nclass, crad, nwbin, season, model, expr, ens )
            
#**********************
# dif names for each class
#----------------------
ddifname = {}
for class_lb in lclass[1:]:
  for difvar in ldifvar:
    for iclass in lclass:
      ddifname[class_lb, difvar, iclass] = ddifdir[difvar] + "/up.%s.p%05.2f.cmin%04d.up%02d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(difvar, xth, cmin, class_lb, iclass, nclass, crad, nwbin, season, model, expr, ens )

#**********************
dscalename = {}
#----------------------
# sxyz names for each class
#----------------------
xyzdir   = difdir_root + "/xyz"
func.mk_dir(xyzdir)
lscale1     = ["sxyz", "dpdf_c", "dpdf_w", "dp_w", "frac.dpdf_c", "frac.dpdf_w", "frac.dp_w"]
for class_lb in lclass[1:]:
  for scale1 in lscale1:
    dscalename[class_lb, scale1] = xyzdir + "/up.%s.p%05.2f.cmin%04d.up%02d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(scale1, xth, cmin, class_lb, 0, nclass, crad, nwbin, season, model, expr, ens )
#----------------------
# nsxyz names for each class
#----------------------
nxyzdir   = difdir_root + "/nxyz"
func.mk_dir(nxyzdir)
lscale2     = ["nsxyz", "dnxyz", "ndpdf_c", "ndpdf_w", "ndp_w", "frac.dnxyz", "frac.ndpdf_c", "frac.ndpdf_w", "frac.ndp_w"]
for class_lb in lclass[1:]:
  for scale2 in lscale2:
    dscalename[class_lb, scale2] = nxyzdir + "/up.%s.p%05.2f.cmin%04d.up%02d.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(scale2, xth, cmin, class_lb, 0, nclass, crad, nwbin, season, model, expr, ens )
#----------------------
#*******************************************************
# make num, sp, mnum for vtype=="up"
#*******************************************************
iclass = 0
for era in lera:
  for var in lvar:
    for class_lb in lclass[1:]:
      aup      = zeros([nwbin, ny, nx], float32)
      #-- sumup ----
      for iiclass in range(class_lb, lclass[-1]+1):
        iname       = dname[class_lb, era, var, iiclass]
        aup_temp    = fromfile(iname, float32).reshape(nwbin, ny, nx)
        aup         = aup + aup_temp

      #-- write ----
      aup.tofile(dname[class_lb, era, var, iclass])

#*******************************************************

for class_lb in lclass[1:]:
  lclass_seg  = [0] + range(class_lb, lclass[-1]+1)
  #*************************************
  # make a2totnum_his, a2totnum_fut
  # num for all cyclone (iclass = 0)
  #-------------------------------------
  a2totnum_his = fromfile(dname[class_lb, "his", "num", 0], float32).reshape(nwbin, ny, nx)[0]
  a2totnum_fut = fromfile(dname[class_lb, "fut", "num", 0], float32).reshape(nwbin, ny, nx)[0]
  
  da3totnum = {}
  da3totnum["his"] = func.mul_a2(a2totnum_his, nwbin)
  da3totnum["fut"] = func.mul_a2(a2totnum_fut, nwbin)
  #****************************************
  #for iclass in lclass:
  for iclass in lclass_seg:
    #*************************************
    da3num  = {}
    da3sp   = {}
    da3snum = {}
    da3rtotnum = {}
    da3rnum = {}
    da3mp   = {}
  
    print "iclass",iclass
    #**********************
    # read 
    #----------------------
    for era in lera:
      da3num[era]    = fromfile(dname[class_lb, era, "num", iclass], float32).reshape(nwbin, ny, nx)
      da3sp[era]     = fromfile(dname[class_lb, era, "sp",  iclass], float32).reshape(nwbin, ny, nx)
      #----------------------
      da3snum[era]   = func.mul_a2( da3num[era][0], nwbin)
      da3snum[era]   = ma.masked_equal( da3snum[era], 0.0)
      #----------------------
      # relative num for each class
      #---
      da3rnum[era]   = ma.masked_where(da3snum[era]==0.0, da3num[era]) / da3snum[era]
      da3rnum[era]   = da3rnum[era].filled(0.0)
      #----------------------
      #  num(iclass, wbin) per num of all cyclone class, all wbin
      #---
      da3rtotnum[era]= ma.masked_where(da3totnum[era]==0.0, da3num[era]) / da3totnum[era]
      da3rtotnum[era]= da3rtotnum[era].filled(0.0)
      #----------------------
      da3mp[era]     = ma.masked_where(da3num[era]==0.0, da3sp[era]) / da3num[era]
      #da3mp[era]     = da3mp[era].filled(0.0)
    #----------------------
    # make dif
    #----------------------
    #
    a3drnum         = da3rnum["fut"]    - da3rnum["his"]
    a3drtotnum      = da3rtotnum["fut"] - da3rtotnum["his"]
    a3dmp           = (da3mp["fut"]      - da3mp["his"]).filled(0.0)
    #
    a3drnum         = array(a3drnum,    float32)
    a3drtotnum      = array(a3drtotnum, float32)
    a3dmp           = array(a3dmp,      float32)
  
    #----------------------
    # write
    #----------------------
    a3drnum.tofile(   ddifname[class_lb, "drnum"   , iclass])
    a3drtotnum.tofile(ddifname[class_lb, "drtotnum", iclass])
    a3dmp.tofile(     ddifname[class_lb, "dmp"     , iclass])
  
  
  
  #***************************************************
  
  da2XYZ    = {}
  da2dXYZ   = {}
  da2XdYZ   = {}
  da2XYdZ   = {}
  
  da2c_rn   = {}
  da3pdf_w  = {}
  da3w_p    = {}
  
  da2dc_rn  = {}
  da3dpdf_w = {}
  da3dw_p   = {}
  
  #for iclass in lclass:
  for iclass in lclass_seg:
    a3num  = fromfile(dname[class_lb, "his", "num", iclass], float32).reshape(nwbin, ny, nx)
    a3sp   = fromfile(dname[class_lb, "his", "sp", iclass], float32).reshape(nwbin, ny, nx)
    a3snum = func.mul_a2( a3num[0], nwbin )
  
    #------------------
    # X= PDF(Ci)
    #------------------
    da2c_rn[iclass]  = ma.masked_where(a2totnum_his==0.0, a3num[0]) / a2totnum_his
    da2c_rn[iclass]  = da2c_rn[iclass].filled(0.0)
  
    #------------------
    # Y= PDF(wi|Ci)
    #------------------
    da3pdf_w[iclass] = ma.masked_where(a3snum==0.0, a3num) /  a3snum
    da3pdf_w[iclass] = da3pdf_w[iclass].filled(0.0)
  
    #------------------
    # Z= P(wi|Ci)
    #------------------
    da3w_p[iclass]   = ma.masked_where(a3num==0.0, a3sp) /  a3num  # devide by "a3num"
    da3w_p[iclass]   = da3w_p[iclass].filled(0.0)
  
    #------------------
    # dX=dPDF(Ci)
    #------------------
    da2dc_rn[iclass]  = fromfile(ddifname[class_lb, "drtotnum", iclass], float32).reshape(nwbin, ny, nx)[0]
  
  
    #------------------
    # dY = PDF(wi|Ci)
    #------------------
    da3dpdf_w[iclass] = fromfile(ddifname[class_lb, "drnum", iclass], float32).reshape(nwbin, ny, nx)
  
    #------------------
    # dZ= dP(wi|Ci)
    #------------------
    da3dw_p[iclass]   = fromfile(ddifname[class_lb, "dmp", iclass], float32).reshape(nwbin, ny, nx)
  
  #***************************************************
  
  da2XYZ[0]        = zeros([ny,nx], float32)
  da2dXYZ[0]       = zeros([ny,nx], float32)
  da2XdYZ[0]       = zeros([ny,nx], float32)
  da2XYdZ[0]       = zeros([ny,nx], float32)
  #for iclass in lclass[1:]:
  for iclass in lclass_seg[1:]:
    #*************************************
    # a2XYZ , X=PDF(Ci), Y = PDF(wi|Ci), Z = P(wi|Ci)
    #-------------------------------------    
    da2XYZ[iclass] = da2c_rn[iclass] * sum( (da3pdf_w[iclass] * da3w_p[iclass])[1:], axis = 0) 
    da2XYZ[0]      = da2XYZ[0] + da2XYZ[iclass]
  
    #*************************************
    # a2dXYZ, dX=dPDF(Ci), Y = PDF(wi|Ci), Z = P(wi|Ci)
    #-------------------------------------    
    da2dXYZ[iclass] = da2dc_rn[iclass] * sum( (da3pdf_w[iclass] * da3w_p[iclass])[1:], axis =0 )
    da2dXYZ[0]      = da2dXYZ[0] + da2dXYZ[iclass]
  
    #*************************************
    # a2XdYZ, X=PDF(Ci), dY = dPDF(wi|Ci), Z = P(wi|Ci)
    #-------------------------------------    
    da2XdYZ[iclass] = da2c_rn[iclass] * sum( (da3dpdf_w[iclass] * da3w_p[iclass])[1:], axis = 0) 
    da2XdYZ[0]      = da2XdYZ[0] + da2XdYZ[iclass]
  
    #*************************************
    # a2XYdZ , X=PDF(Ci), Y = PDF(wi|Ci), dZ = dP(wi|Ci)
    #-------------------------------------    
    da2XYdZ[iclass] = da2c_rn[iclass] * sum( (da3pdf_w[iclass] * da3dw_p[iclass])[1:], axis = 0)
    da2XYdZ[0]      = da2XYdZ[0] + da2XYdZ[iclass]
  
  #***************************************************************
  # a2n, a2dn
  #-------------------------------------
  a2dn = (a2totnum_fut - a2totnum_his)
  a2dn = a2dn / (eyear_his - iyear_his +1)   # total -> diff of num per season
  a2n  = a2totnum_his
  a2n  = a2n  / (eyear_his - iyear_his +1)   # total -> num per season
  
  
  #***************************************************************
  # a2nXYZ
  #--------------------------------------
  a2SXYZ   = array(zeros(ny * nx).reshape(ny, nx), float32)
  #for iclass in lclass[1:]:
  for iclass in lclass_seg[1:]:
    a2SXYZ = a2SXYZ +  da2XYZ[iclass]
  #
  a2nXYZ   = a2n * a2SXYZ
  #***************************************************************
  # a2dnXYZ
  #--------------------------------------
  a2dnXYZ   = a2dn * a2SXYZ
  #
  frac_a2dnXYZ   = ma.masked_where(a2nXYZ==0.0, a2dnXYZ) / a2nXYZ   # zero -> NaN
  
  #***************************************************************
  # a2ndXYZ
  #--------------------------------------
  a2SdXYZ   = array(zeros(ny * nx).reshape(ny, nx), float32)
  #for iclass in lclass[1:]:
  for iclass in lclass_seg[1:]:
    a2SdXYZ = a2SdXYZ + da2dXYZ[iclass]
  #
  a2ndXYZ   = a2n * a2SdXYZ
  #
  frac_a2SdXYZ   = ma.masked_where(a2SXYZ==0.0, a2SdXYZ) / a2SXYZ   # zero -> NaN
  frac_a2ndXYZ   = ma.masked_where(a2nXYZ==0.0, a2ndXYZ) / a2nXYZ   # zero -> NaN
  #
  #***************************************************************
  # a2nXdYZ
  #--------------------------------------
  a2SXdYZ   = array(zeros(ny * nx).reshape(ny, nx), float32)
  #for iclass in lclass[1:]:
  for iclass in lclass_seg[1:]:
    a2SXdYZ = a2SXdYZ + da2XdYZ[iclass]
  #
  a2nXdYZ   = a2n * a2SXdYZ
  #
  frac_a2SXdYZ   = ma.masked_where(a2SXYZ==0.0, a2SXdYZ) / a2SXYZ
  frac_a2nXdYZ   = ma.masked_where(a2nXYZ==0.0, a2nXdYZ) / a2nXYZ
  
  #***************************************************************
  # a2nXYdZ
  #--------------------------------------
  a2SXYdZ   = array(zeros(ny * nx).reshape(ny, nx), float32)
  #for iclass in lclass[1:]:
  for iclass in lclass_seg[1:]:
    a2SXYdZ = a2SXYdZ + da2XYdZ[iclass]
  #
  a2nXYdZ   = a2n * a2SXYdZ
  #
  frac_a2SXYdZ   = ma.masked_where(a2SXYZ==0.0, a2SXYdZ) / a2SXYZ
  frac_a2nXYdZ   = ma.masked_where(a2nXYZ==0.0, a2nXYdZ) / a2nXYZ
  
  #***************************************************************
  # write to file
  #--------------------------------------
  # XYZ
  #-----------
  print xyzdir
  array(a2SXYZ, float32).tofile(dscalename[ class_lb, "sxyz"])
  array(a2SdXYZ, float32).tofile(dscalename[class_lb, "dpdf_c"])
  array(a2SXdYZ, float32).tofile(dscalename[class_lb, "dpdf_w"])
  array(a2SXYdZ, float32).tofile(dscalename[class_lb, "dp_w"])
  #-----------
  # frac_XYZ
  #-----------
  array(frac_a2SdXYZ, float32).tofile(dscalename[class_lb, "frac.dpdf_c"])
  array(frac_a2SXdYZ, float32).tofile(dscalename[class_lb, "frac.dpdf_w"])
  array(frac_a2SXYdZ, float32).tofile(dscalename[class_lb, "frac.dp_w"])
  #-----------
  # nXYZ
  #-----------
  print nxyzdir
  array(a2nXYZ,  float32).tofile(dscalename[class_lb, "nsxyz"])
  array(a2dnXYZ, float32).tofile(dscalename[class_lb, "dnxyz"])
  array(a2ndXYZ, float32).tofile(dscalename[class_lb, "ndpdf_c"])
  array(a2nXdYZ, float32).tofile(dscalename[class_lb, "ndpdf_w"])
  array(a2nXYdZ, float32).tofile(dscalename[class_lb, "ndp_w"])
  ##-----------
  ## frac_nXYZ
  ##-----------
  array(frac_a2dnXYZ, float32).tofile(dscalename[class_lb, "frac.dnxyz"])
  array(frac_a2ndXYZ, float32).tofile(dscalename[class_lb, "frac.ndpdf_c"])
  array(frac_a2nXdYZ, float32).tofile(dscalename[class_lb, "frac.ndpdf_w"])
  array(frac_a2nXYdZ, float32).tofile(dscalename[class_lb, "frac.ndp_w"])
  #*************************************
  # read mnum
  #-------------------------------------
  era    = "his"
  var    = "mnum"
  #for iclass in lclass:
  #  dname[era, var, iclass] =  ddir[era, "mnum"] + "/%s.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(var, xth, iclass, nclass, crad, nwbin, season, model, expr, ens )
  ##-------------------------------------
  
  da3mnum_his   = {}
  #for iclass in lclass:
  for iclass in lclass_seg:
    da3mnum_his[iclass]  = fromfile(dname[class_lb, "his", "mnum", iclass], float32).reshape(nwbin, ny, nx)
  
  #*************************************
  # make pict
  #*************************************
  dcm = {}
  #----------------------
  # basemap
  #----------------------
  #M         = Basemap(resolution = "l", llcrnrlat=-90.0, llcrnrlon=0.0, urcrnrlat=90.0, urcrnrlon=360.0)
  M         = Basemap(resolution = "l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon)
  ##----------------------
  ## colormap
  ##----------------------
  #dcm  = {}
  #for scale in  ["dpdf_c", "dpdf_w", "dp_w", "frac.dpdf_c", "frac.dpdf_w", "frac.dp_w"]:
  #  #--------
  #  dcm[scale] = pylab.cm.get_cmap("RdBu")
  #  #dcm[scale].set_bad(color="gray")

  #for scale in lscale2:
  #  dcm[scale] = pylab.cm.get_cmap("RdBu")
  #  dcm[scale] = dcm[scale].set_bad( (0.8, 0.8, 0.8))
  ##
  
  
  #----------------------
  # dmp
  #----------------------
  iname     = ddifname[class_lb, "dmp", 0]
  stitle    = "%s up%02d"%("dmp", class_lb)
  a2mask    = da3mnum_his[0][0]
  a         = fromfile(iname, float32) * 60.0 * 60.0 * 24.0
  a         = a.reshape(nwbin, ny, nx)
  a         = a[0]
  pngname   = iname[:-3] + ".png"
  
  # transform the data  ---
  a_trans   = M.transform_scalar( a, lons, lats, nnx, nny)
  #------------------------
  scale     = "dmp"
  dcm[scale] = ret_colormap(scale) 
  bnd       = [-3.0, -2.0, -1.0, -0.5,  0.5 , 1.0, 2.0 , 3.0]
  im        = M.imshow(a_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=dcm[scale])
  M.drawcoastlines()
  plt.title(stitle)
  savefig(pngname)
  plt.clf()
  print pngname

  cbarname  = iname[:-3] + ".cbar.png"
  bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
  figcbar   = plt.figure(figsize=(1,5))
  #axcbar    = figcbar.add_axes([0,0,0.9,1])
  axcbar    = figcbar.add_axes([0,0,0.4,1.0])
  plt.colorbar(im, boundaries = bnd_cbar, extend="both", cax=axcbar)
  savefig(cbarname)
  plt.clf()
  #----------------------
  # dxyz
  #----------------------
  a2mask    = da3mnum_his[0][0]
  for scale in ["dpdf_c", "dpdf_w", "dp_w", "frac.dpdf_c", "frac.dpdf_w", "frac.dp_w"] + lscale2:
    #--------------
    dcm[scale]   = ret_colormap(scale)
    #--------------
    if scale[:4] == "frac":
      coef  = 1.0
    else:
      coef  = 60.0 * 60.0 * 24.0
    #--- prep for map -------
    iname   = dscalename[class_lb, scale]
    pngname = iname[:-3] + ".png"
    a       = fromfile(iname, float32).reshape(ny, nx)
    a       = a * coef
    ##------------------------

    figmap  = plt.figure()
    axmap   = figmap.add_axes([0, 0.1, 1.0, 0.8])
    M       = Basemap(resolution = "l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)

    # transform ---
    a_trans = M.transform_scalar(a, lons, lats, nnx, nny)
    a2mask_trans = M.transform_scalar(a2mask, lons, lats, nnx, nny)
    #-- mask mnum_his < xxxx-----
    #a_trans = ma.masked_where(a2mask_trans < mnum_min, a_trans)
    a_trans = ma.masked_invalid(a_trans) 
    #--- prep for colorbar --
    cbarname  = iname[:-3] + ".cbar.png"
    figcbar   = plt.figure(figsize=(1,5))
    #axcbar    = figcbar.add_axes([0,0,0.9,1])
    axcbar    = figcbar.add_axes([0,0,0.4,1.0])
    #------------------------

    if scale[:4] == "frac":
      #----
      continue
      #----
      bnd     = [-0.6, -0.4, -0.2, -0.05, 0.05, 0.2 , 0.4 , 0.6]
      im      = M.imshow(a_trans, origin ="lower", norm=BoundaryNormSymm(bnd), cmap=dcm[scale])
      bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
      plt.colorbar(im, boundaries = bnd_cbar, extend="both", cax=axcbar)
    elif (scale in lscale2) & (scale not in ["nsxyz"]):
      #-----
      #bnd     = [-200, -150.0, -100.0, -50.0, -10.0,  10.0 , 50.0 , 100.0, 150.0, 200]
      #bnd     = [-90.0, -70.0, -50.0, -30.0, -10.0, 10.0, 30.0, 50.0, 70.0, 90.0]
      bnd     = [-90.0, -70.0, -50.0, -30.0, -10.0, 10.0, 30.0, 50.0, 70.0, 90.0]
      #-----
      
      im      = M.imshow(a_trans, origin ="lower", norm=BoundaryNormSymm(bnd), cmap=dcm[scale])
      bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
      plt.colorbar(im, boundaries = bnd_cbar, extend="both", cax=axcbar)
      
    elif scale in ["dpdf_c", "dpdf_w", "dp_w"]:
      bnd     = [-3.0, -2.0, -1.0, -0.5, 0.5, 1.0, 2.0, 3.0]
      im      = M.imshow(a_trans, origin ="lower", norm=BoundaryNormSymm(bnd), cmap=dcm[scale], interpolation="nearest")
      bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
      plt.colorbar(im, boundaries = bnd_cbar, extend="both", cax=axcbar)

    else:
      im      = M.imshow(a_trans, origin ="lower",vmax=800.)
      plt.colorbar(im, cax=axcbar)
    #-- superimpose shade(mask) -----
    cmshade = matplotlib.colors.ListedColormap([(0.8, 0.8, 0.8), (0.8, 0.8, 0.8)])
    ashade  = ma.masked_where(a2mask_trans > mnum_min, a2mask_trans)
    im      = M.imshow(ashade, origin="lower", cmap=cmshade, interpolation="nearest")
    #-----
    stitle = "%s up%02d nc%02d, P%s"%(scale, class_lb, nclass,xth)
    axmap.set_title(stitle)
    M.drawcoastlines()

    # draw lat/lon grid lines
    M.drawmeridians(arange(0,360,meridians),  labels=[0, 0, 0, 1])
    M.drawparallels(arange(-90,90,parallels), labels=[1, 0, 0, 0])

    figmap.savefig(pngname)
    print pngname

    figcbar.savefig(cbarname)
    plt.clf()
  #----------------------



