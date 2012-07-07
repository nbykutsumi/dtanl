from mpl_toolkits.basemap import Basemap
import ctrack_para
import ctrack_func as func
from numpy import *
import os, sys
from cf.plot import *
import matplotlib.pyplot as plt
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

xth         = 90.0
crad        = 1000.0
#***************************************
mnum_min    = 1.0
#***************************************
diyear  = {"his": iyear_his, "fut": iyear_fut}
deyear  = {"his": eyear_his, "fut": eyear_fut}
#***************************************
dexpr   = {"his": "historical", "fut": "rcp85", "dif": "dif"}
#***************************************
lera    = ["fut", "his"]
lvar    = ["num", "sp", "mnum"]
ldifvar = ["drnum", "drtotnum", "dmp"]

lvtype   = ["single", "acc"]
#***************************************
# class
#-----------------------------
dpgradrange   = ctrack_para.ret_dpgradrange()
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
ddir_root["his"] = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/wfpr"%(model, dexpr["his"], ens, thdura)

ddir_root["fut"] = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/wfpr"%(model, dexpr["fut"], ens, thdura)

ddir_root["dif"] = "/media/disk2/out/CMIP5/day/%s/dif/%s/%04d-%04d.%04d-%04d/tracks/dura%02d/wfpr"%(model, dexpr["fut"], diyear["his"], deyear["his"], diyear["fut"], deyear["fut"], thdura)

csvdir_root      = "/media/disk2/out/CMIP5/day/%s/dif/%s/tracks/csv"%(model, ens)
#-----
ddir  = {}
dname = {}
for era in lera:
  for var in lvar:
    ddir[era, var]  =  ddir_root[era] + "/%s"%(var)
#--------------------------
# dif dirs
#--------------------------
difdir_root = "/media/disk2/out/CMIP5/day/%s/dif/%s/%04d-%04d.%04d-%04d/tracks/dura%02d/wfpr"%(model, dexpr["fut"], diyear["his"], deyear["his"], diyear["fut"], deyear["fut"], thdura)

ddifdir = {}
for difvar in ldifvar:
  ddifdir[difvar] = difdir_root + "/%s"%(difvar)
  func.mk_dir(ddifdir[difvar])
#---
#**********************
# input names for each class
#----------------------
dname  = {}
for era in lera:
  expr = dexpr[era]
  for var in lvar:
    for iclass in lclass:
      dname[era, var, iclass] =  ddir[era, var] + "/%s.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(var, xth, iclass, nclass, crad, nwbin, season, model, expr, ens )


#**********************
# dif names for each class
#----------------------
ddifname = {}
for vtype in lvtype:
  for iclass in lclass:
    for difvar in ldifvar:
      for iclass in lclass:
        if vtype == "single":
          ddifname[vtype, difvar, iclass] = ddifdir[difvar] + "/%s.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(difvar, xth, iclass, nclass, crad, nwbin, season, model, expr, ens )
  
        elif vtype == "acc":
          ddifname[vtype, difvar, iclass] = ddifdir[difvar] + "/acc.%s.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(difvar, xth, iclass, nclass, crad, nwbin, season, model, expr, ens )
    
#**********************
dscalename = {}
#----------------------
# sxyz names for each class
#----------------------
xyzdir   = difdir_root + "/xyz"
func.mk_dir(xyzdir)
lscale1     = ["sxyz", "dpdf_c", "dpdf_w", "dp_w", "frac.dpdf_c", "frac.dpdf_w", "frac.dp_w"]
for vtype in lvtype:
  for iclass in lclass:
    for scale1 in lscale1:
      if vtype == "single":
        #----
        dscalename[vtype, scale1, iclass] = xyzdir + "/%s.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(scale1, xth, iclass, nclass, crad, nwbin, season, model, expr, ens )
  
      #----
      if vtype == "acc":
        for iclass in lclass[2:]:
          dscalename[vtype, scale1, iclass] = xyzdir + "/acc.%s.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(scale1, xth, iclass, nclass, crad, nwbin, season, model, expr, ens )

#----------------------
# nsxyz names for each class
#----------------------
nxyzdir   = difdir_root + "/nxyz"
func.mk_dir(nxyzdir)
lscale2     = ["nsxyz", "dnxyz", "ndpdf_c", "ndpdf_w", "ndp_w", "frac.dnxyz", "frac.ndpdf_c", "frac.ndpdf_w", "frac.ndp_w"]
#---
for vtype in lvtype:
  for iclass in lclass:
    for scale2 in lscale2:
      #----
      if vtype == "single":
        dscalename[vtype, scale2, iclass] = nxyzdir + "/%s.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(scale2, xth, iclass, nclass, crad, nwbin, season, model, expr, ens )
      #----
      if vtype == "acc":
        for iclass in lclass[2:]:
          dscalename[vtype, scale2, iclass] = nxyzdir + "/acc.%s.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(scale2, xth, iclass, nclass, crad, nwbin, season, model, expr, ens )
#----------------------

#*************************************
# make a2totnum_his, a2totnum_fut
# num for all cyclone (iclass = 0)
#-------------------------------------
da3totnum = {}
for vtype in lvtype:
  for iclass in lclass:
    if (vtype == "single"):
      #------------
      if iclass in lclass[1:]:
        continue
      #------------
      a2totnum_his = fromfile(dname["his", "num", 0], float32).reshape(nwbin, ny, nx)[0]
      a2totnum_fut = fromfile(dname["fut", "num", 0], float32).reshape(nwbin, ny, nx)[0]
  
    elif (vtype == "acc"):    
      a2totnum_his_temp = zeros([ny,nx], float32)
      a2totnum_fut_temp = zeros([ny,nx], float32)
      #-----
      for iiclass in range(iclass, lclass[-1]+1):
        a2totnum_his_temp = a2totnum_his_temp + fromfile(dname["his", "num", 0], float32).reshape(nwbin, ny, nx)[0]
        a2totnum_fut_temp = a2totnum_fut_temp + fromfile(dname["fut", "num", 0], float32).reshape(nwbin, ny, nx)[0]
      #-----
      a2totnum_his = a2totnum_his_temp
      a2totnum_fut = a2totnum_fut_temp
    #-------------     
    da3totnum[vtype, "his", iclass] = func.mul_a2(a2totnum_his, nwbin)
    da3totnum[vtype, "fut", iclass] = func.mul_a2(a2totnum_fut, nwbin)

#****************************************
for vtype in lvtype:
  for iclass in lclass:
    #------------
    if (vtype == "single")&(iclass in lclass[1:]):
      continue
    if (vtype == "acc")&(iclass in [0.1]):
      continue
    #------------
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
      #================================================
      if vtype == "single":
        da3num[era]    = fromfile(dname[era, "num", iclass], float32).reshape(nwbin, ny, nx)
        da3sp[era]     = fromfile(dname[era, "sp",  iclass], float32).reshape(nwbin, ny, nx)

      if vtype == "acc":
        num_temp    = zeros([nwbin, ny, nx], float32)
        sp_temp     = zeros([nwbin, ny, nx], float32)
        for iiclass in range(iclass, lclass[-1] +1):
          num_temp    = num_temp + fromfile(dname[era, "num", iiclass], float32).reshape(nwbin, ny, nx)
          sp_temp     = sp_temp  + fromfile(dname[era, "sp",  iiclass], float32).reshape(nwbin, ny, nx)

        #------
        da3num[era] = num_temp
        da3sp[era]  = sp_temp

      #================================================

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
      da3rtotnum[era]= ma.masked_where(da3totnum[vtype, era, iclass]==0.0, da3num[era]) / da3totnum[vtype, era, iclass]
      da3rtotnum[era]= da3rtotnum[era].filled(0.0)
      #----------------------
      da3mp[era]     = ma.masked_where(da3num[era]==0.0, da3sp[era]) / da3num[era]
      #da3mp[era]     = da3mp[era].filled(0.0)
    #----------------------
    # make dif
    #----------------------
    a3drnum         = da3rnum["fut"]    - da3rnum["his"]
    a3drtotnum      = da3rtotnum["fut"] - da3rtotnum["his"]
    a3dmp           = (da3mp["fut"]     - da3mp["his"]).filled(0.0)
    #
    a3drnum         = array(a3drnum,    float32)
    a3drtotnum      = array(a3drtotnum, float32)
    a3dmp           = array(a3dmp,      float32)
  
    #----------------------
    # write
    #----------------------
    a3drnum.tofile(ddifname[vtype, "drnum", iclass])
    a3drtotnum.tofile(ddifname[vtype, "drtotnum", iclass])
    a3dmp.tofile(ddifname[vtype, "dmp", iclass])



#***************************************************


da2c_rn   = {}
da3pdf_w  = {}
da3w_p    = {}

da2dc_rn  = {}
da3dpdf_w = {}
da3dw_p   = {}

for vtype in lvtype:
  for iclass in lclass:
    #-----------
    if (vtype == "acc") & (iclass in [0,1]):
      continue
    #-----------
    if vtype == "single":
      a2totnum_his   = da3totnum[vtype, "his", 0][0]
      a2totnum_fut   = da3totnum[vtype, "fut", 0][0]
    elif vtype == "acc":
      a2totnum_his   = da3totnum[vtype, "his", iclass][0]
      a2totnum_fut   = da3totnum[vtype, "fut", iclass][0]
    #------------

    if vtype == "single":
      a3num  = fromfile(dname["his", "num", iclass], float32).reshape(nwbin, ny, nx)
      a3sp   = fromfile(dname["his", "sp", iclass], float32).reshape(nwbin, ny, nx)
      a3snum = func.mul_a2( a3num[0], nwbin )

    if vtype == "acc":
      num_temp  = zeros([nwbin, ny, nx], float32)
      sp_temp   = zeros([nwbin, ny, nx], float32)
      snum_temp = zeros([nwbin, ny, nx], float32)

      for iiclass in range(iclass, lclass[-1]+1):
        num_temp  = num_temp  + fromfile(dname["his", "num", iiclass], float32).reshape(nwbin, ny, nx)
        sp_temp   = sp_temp   + fromfile(dname["his", "sp", iiclass], float32).reshape(nwbin, ny, nx)
        snum_temp = snum_temp + func.mul_a2( a3num[0], nwbin )
      #----
      a3num  = num_temp
      a3sp   = sp_temp
      a3snum = snum_temp
    #------------------
    # X= PDF(Ci)
    #------------------
    da2c_rn[vtype, iclass]  = ma.masked_where(a2totnum_his==0.0, a3num[0]) / a2totnum_his
    da2c_rn[vtype, iclass]  = da2c_rn[vtype, iclass].filled(0.0)
  
    #------------------
    # Y= PDF(wi|Ci)
    #------------------
    da3pdf_w[vtype, iclass] = ma.masked_where(a3snum==0.0, a3num) /  a3snum
    da3pdf_w[vtype, iclass] = da3pdf_w[vtype, iclass].filled(0.0)
  
    #------------------
    # Z= P(wi|Ci)
    #------------------
    da3w_p[vtype, iclass]   = ma.masked_where(a3num==0.0, a3sp) /  a3num  # devide by "a3num"
    da3w_p[vtype, iclass]   = da3w_p[vtype, iclass].filled(0.0)
  
    #------------------
    # dX=dPDF(Ci)
    #------------------
    da2dc_rn[vtype, iclass]  = fromfile(ddifname[vtype, "drtotnum", iclass], float32).reshape(nwbin, ny, nx)[0]
  
  
    #------------------
    # dY = PDF(wi|Ci)
    #------------------
    da3dpdf_w[vtype, iclass] = fromfile(ddifname[vtype, "drnum", iclass], float32).reshape(nwbin, ny, nx)
  
    #------------------
    # dZ= dP(wi|Ci)
    #------------------
    da3dw_p[vtype, iclass]   = fromfile(ddifname[vtype, "dmp", iclass], float32).reshape(nwbin, ny, nx)



da2XYZ    = {}
da2dXYZ   = {}
da2XdYZ   = {}
da2XYdZ   = {}

for vtype in lvtype:
  #***************************************************
  if vtype == "single": 
    da2XYZ[vtype,  0]       = zeros([ny,nx], float32)
    da2dXYZ[vtype, 0]       = zeros([ny,nx], float32)
    da2XdYZ[vtype, 0]       = zeros([ny,nx], float32)
    da2XYdZ[vtype, 0]       = zeros([ny,nx], float32)

  for iclass in lclass:
    #-----------
    if (vtype =="single")&(iclass in lclass[1:]):
      continue
    elif (vtype == "acc")&(iclass in [0,1]):
      continue
    #-----------
    #*************************************
    # a2XYZ , X=PDF(Ci), Y = PDF(wi|Ci), Z = P(wi|Ci)
    #-------------------------------------
    da2XYZ[vtype, iclass] = da2c_rn[vtype, iclass] * sum( (da3pdf_w[vtype, iclass] * da3w_p[vtype, iclass])[1:], axis = 0) 

    if vtype == "single":
      da2XYZ[vtype, 0]      = da2XYZ[vtype, 0] + da2XYZ[vtype, iclass]
  
    #*************************************
    # a2dXYZ, dX=dPDF(Ci), Y = PDF(wi|Ci), Z = P(wi|Ci)
    #-------------------------------------    
    da2dXYZ[vtype, iclass] = da2dc_rn[vtype, iclass] * sum( (da3pdf_w[vtype, iclass] * da3w_p[vtype, iclass])[1:], axis =0 )
    if vtype == "single":
      da2dXYZ[vtype, 0]      = da2dXYZ[vtype, 0] + da2dXYZ[vtype, iclass]
  
    #*************************************
    # a2XdYZ, X=PDF(Ci), dY = dPDF(wi|Ci), Z = P(wi|Ci)
    #-------------------------------------    
    da2XdYZ[vtype, iclass] = da2c_rn[vtype, iclass] * sum( (da3dpdf_w[vtype, iclass] * da3w_p[vtype, iclass])[1:], axis = 0) 
    if vtype == "single":
      da2XdYZ[vtype, 0]      = da2XdYZ[vtype, 0] + da2XdYZ[vtype, iclass]
  
    #*************************************
    # a2XYdZ , X=PDF(Ci), Y = PDF(wi|Ci), dZ = dP(wi|Ci)
    #-------------------------------------    
    da2XYdZ[vtype, iclass] = da2c_rn[vtype, iclass] * sum( (da3pdf_w[vtype, iclass] * da3dw_p[vtype, iclass])[1:], axis = 0)
    if vtype == "single":
      da2XYdZ[vtype, 0]      = da2XYdZ[vtype, 0] + da2XYdZ[vtype, iclass]


  #*************************************************************** 
  for iclass in lclass:
    #-----------
    if (vtype =="single")&(iclass in lclass[1:]):
      continue
    elif (vtype == "acc")&(iclass in [0,1]):
      continue
    #-----------
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
    for iiclass in lclass[1:]:
      a2SXYZ = a2SXYZ +  da2XYZ[vtype, iiclass]
    #
    a2nXYZ   = a2n * a2SXYZ
    #***************************************************************
    # a2dnXYZ
    #--------------------------------------
    a2dnXYZ   = a2dn * a2SXYZ
    #
    frac_a2dnXYZ   = a2dnXYZ / a2nXYZ   # zero -> NaN
    
    #***************************************************************
    # a2ndXYZ
    #--------------------------------------
    a2SdXYZ   = array(zeros(ny * nx).reshape(ny, nx), float32)
    for iiclass in lclass[1:]:
      a2SdXYZ = a2SdXYZ + da2dXYZ[vtype, iiclass]
    #
    a2ndXYZ   = a2n * a2SdXYZ
    #
    frac_a2SdXYZ   = a2SdXYZ / a2SXYZ   # zero -> NaN
    frac_a2ndXYZ   = a2ndXYZ / a2nXYZ   # zero -> NaN
    #
    #***************************************************************
    # a2nXdYZ
    #--------------------------------------
    a2SXdYZ   = array(zeros(ny * nx).reshape(ny, nx), float32)
    for iiclass in lclass[1:]:
      a2SXdYZ = a2SXdYZ + da2XdYZ[vtype, iiclass]
    #
    a2nXdYZ   = a2n * a2SXdYZ
    #
    frac_a2SXdYZ   = a2SXdYZ / a2SXYZ
    frac_a2nXdYZ   = a2nXdYZ / a2nXYZ
    
    #***************************************************************
    # a2nXYdZ
    #--------------------------------------
    a2SXYdZ   = array(zeros(ny * nx).reshape(ny, nx), float32)
    for iiclass in lclass[1:]:
      a2SXYdZ = a2SXYdZ + da2XYdZ[vtype, iiclass]
    #
    a2nXYdZ   = a2n * a2SXYdZ
    #
    frac_a2SXYdZ   = a2SXYdZ / a2SXYZ
    frac_a2nXYdZ   = a2nXYdZ / a2nXYZ
    
    #***************************************************************
    # write to file
    #--------------------------------------
    # XYZ
    #-----------
    print xyzdir
    array(a2SXYZ, float32).tofile(dscalename[ vtype, "sxyz"  , iclass])
    array(a2SdXYZ, float32).tofile(dscalename[vtype, "dpdf_c", iclass])
    array(a2SXdYZ, float32).tofile(dscalename[vtype, "dpdf_w", iclass])
    array(a2SXYdZ, float32).tofile(dscalename[vtype, "dp_w"  , iclass])
    #-----------
    # frac_XYZ
    #-----------
    array(frac_a2SdXYZ, float32).tofile(dscalename[vtype, "frac.dpdf_c"], iclass)
    array(frac_a2SXdYZ, float32).tofile(dscalename[vtype, "frac.dpdf_w" , iclass])
    array(frac_a2SXYdZ, float32).tofile(dscalename[vtype, "frac.dp_w"   , iclass])
    #-----------
    # nXYZ
    #-----------
    print nxyzdir
    array(a2nXYZ,  float32).tofile(dscalename[vtype, "nsxyz",   iclass])
    array(a2dnXYZ, float32).tofile(dscalename[vtype, "dnxyz",   iclass])
    array(a2ndXYZ, float32).tofile(dscalename[vtype, "ndpdf_c", iclass])
    array(a2nXdYZ, float32).tofile(dscalename[vtype, "ndpdf_w", iclass])
    array(a2nXYdZ, float32).tofile(dscalename[vtype, "ndp_w",   iclass])
    ##-----------
    ## frac_nXYZ
    ##-----------
    array(frac_a2dnXYZ, float32).tofile(dscalename[vtype, "frac.dnxyz",  iclass])
    array(frac_a2ndXYZ, float32).tofile(dscalename[vtype, "frac.ndpdf_c",iclass])
    array(frac_a2nXdYZ, float32).tofile(dscalename[vtype, "frac.ndpdf_w",iclass])
    array(frac_a2nXYdZ, float32).tofile(dscalename[vtype, "frac.ndp_w",  iclass])
  
  #** end iclass loop *********************************************** 
  
  for vtype in lvtype:
    #*************************************
    # make pict
    #*************************************
    # read mnum
    #-------------------------------------
    era    = "his"
    var    = "mnum"
    for iclass in lclass:
      dname[era, var, iclass] =  ddir[era, "mnum"] + "/%s.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_day_%s_%s_%s.bn"%(var, xth, iclass, nclass, crad, nwbin, season, model, expr, ens )
    #-------------------------------------
    
    da3mnum_his   = {}
    for iclass in lclass:
      da3mnum_his[iclass]  = fromfile(dname["his", "mnum", iclass], float32).reshape(nwbin, ny, nx)
    #**************************************
    for iclass in lclass:
      #-------
      if (vtype == "single")&(iclass in lclass[1:]):
        continue
      elif (vtype == "acc")&(iclass in [0,1]):
        continue
    
      #*************************************
      #----------------------
      # basemap
      #----------------------
      M         = Basemap(resolution = "l", llcrnrlat=-90.0, llcrnrlon=0.0, urcrnrlat=90.0, urcrnrlon=360.0)
      #----------------------
      # colormap
      #----------------------
      dcm  = {}
      for scale in  ["dpdf_c", "dpdf_w", "dp_w", "frac.dpdf_c", "frac.dpdf_w", "frac.dp_w"]:
        #--------
        dcm[scale] = "RdBu"
      for scale in lscale2:
        dcm[scale] = "RdBu"
      
      #----------------------
      # dmp
      #----------------------
      iname     = ddifname[vtype, "dmp", iclass]
      
      a2mask    = da3mnum_his[0][0]
      a         = fromfile(iname, float32) * 60.0 * 60.0 * 24.0
      a         = a.reshape(nwbin, ny, nx)
      a         = a[0]
      a         = ma.masked_where( a2mask < mnum_min, a)
      pngname   = iname[:-3] + ".png"
      
      
      bnd     = [-3.0, -2.0, -1.0, -0.5,  0.5 , 1.0, 2.0 , 3.0]
      im      = M.imshow(a, origin="lower", norm=BoundaryNormSymm(bnd), cmap=dcm[scale])
      M.drawcoastlines()
      bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
      plt.colorbar(boundaries = bnd_cbar, extend="both")
      savefig(pngname)
      plt.clf()
      print pngname
      
      #----------------------
      # dxyz
      #----------------------
      a2mask    = da3mnum_his[0][0]
      for scale in ["dpdf_c", "dpdf_w", "dp_w", "frac.dpdf_c", "frac.dpdf_w", "frac.dp_w"] + lscale2:
        #--------------
        if scale[:4] == "frac":
          coef  = 1.0
        else:
          coef  = 60.0 * 60.0 * 24.0
        #--------------
        iname   = dscalename[vtype, scale, iclass]
        pngname = iname[:-3] + ".png"
        a       = fromfile(iname, float32).reshape(ny, nx)
        a       = a * coef
        a       = ma.masked_where( a2mask < mnum_min, a)
        a       = ma.masked_invalid(a)
        #--------------
        if scale[:4] == "frac":
          bnd     = [-0.6, -0.4, -0.2, -0.05, 0.05, 0.2 , 0.4 , 0.6]
          
          im      = M.imshow(a, origin ="lower", norm=BoundaryNormSymm(bnd), cmap=dcm[scale])
          bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
          plt.colorbar(boundaries = bnd_cbar, extend="both")
        elif (scale in lscale2) & (scale not in ["nsxyz"]):
          #-----
          #bnd     = [-200, -150.0, -100.0, -50.0, -10.0,  10.0 , 50.0 , 100.0, 150.0, 200]
          #bnd     = [-90.0, -70.0, -50.0, -30.0, -10.0, 10.0, 30.0, 50.0, 70.0, 90.0]
          bnd     = [-90.0, -70.0, -50.0, -30.0, -10.0, 10.0, 30.0, 50.0, 70.0, 90.0]
          #-----
          
          im      = M.imshow(a, origin ="lower", norm=BoundaryNormSymm(bnd), cmap=dcm[scale])
          bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
          plt.colorbar(boundaries = bnd_cbar, extend="both")
      
          
        elif scale in ["dpdf_c", "dpdf_w", "dp_w"]:
          bnd     = [-3.0, -2.0, -1.0, -0.5, 0.5, 1.0, 2.0, 3.0]
          im      = M.imshow(a, origin ="lower", norm=BoundaryNormSymm(bnd), cmap=dcm[scale])
          bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
          plt.colorbar(boundaries = bnd_cbar, extend="both")
        else:
          im      = M.imshow(a, origin ="lower",vmax=800.)
          plt.colorbar()
          
        #-----
        M.drawcoastlines()
        savefig(pngname)
        plt.clf()
        print pngname
      
      
      #----------------------


##*************************************
## make pict
##*************************************
#cmd       = oekakidir + "/track.gmt.py"
#cptfile   = oekakidir + "cpt/polar.inv.-1.1.cpt"
##---------------------
#for var in lvar:
#  for iclass in lclass:
#    print "------------------------"
#    print "make pict", var, "class=", iclass
#    #----------------------
#    iname     = dname["dif", var, iclass]
#    pngname   = iname[:-3] + ".png"
#    psname    = iname[:-3] + ".ps"
#    title    = "dif"
#    scalestep = 0.2
#    overscale = 0
#    os.system("python %s %s %s %s %s %s %s"%(\
#             cmd                  \
#            ,iname                \
#            ,cptfile              \
#            ,pngname              \
#            ,title                \
#            ,scalestep            \
#            ,overscale            \
#            ))       
#    print pngname 
#  #****************************************
#
#
   
##****************************************
## make pict
##----------------------------------------
#cmd          = oekakidir + "/track.gmt.py"
#cptfile      = oekakidir + "/cpt/polar.inv.-1.1.cpt"
##-----------------
#print "-----------------------------------"
#print "make pict"
#for iclass in lclass:
#  #---------------
#  iname       = ddifname[iclass]
#  pngname     = ddifname[iclass][:-3] + ".png"
#  psfile      = ddifname[iclass][:-3] + ".ps"
#  title       = "dif"
#  scalestep   = 0.2
#  overscale   = 1 
#  #---------------
#  os.system("python %s %s %s %s %s %s %s"%(\
#           cmd                  \
#          ,iname                \
#          ,cptfile              \
#          ,pngname              \
#          ,title                \
#          ,scalestep            \
#          ,overscale            \
#          ))       
#  print pngname 
##****************************************
## regional dif
##----------------------------------------
#dbound   = ctrack_para.ret_dbound()
#lreg     = dbound.keys()
##******************
##
##------------------
#dfcm    = {}
#dmv     = {}
#dtv     = {}
#dlv     = {}
#for reg in lreg:
#  print reg
#  #******************
#  # regionmask
#  #------------------
#  [lat_min, lat_max, lon_min, lon_max] = dbound[reg]
#
#  a2regionmask  = func.mk_region_mask(lat_min, lat_max, lon_min, lon_max, nx, ny, lat_first, lon_first, dlat, dlon)
#  #--------------------
#  for iclass in lclass:
#    for era in ["his", "fut"]:
#      #--------------------------
#      dlv[reg, era, iclass] = []
#      iyear  = diyear[era]
#      eyear  = deyear[era]
#      #--------------------------
#      for year in range(iyear, eyear + 1):
#        #***************
#        # read
#        #---------------
#        a2dens  =  fromfile(ddensname[era, year, iclass], float32).reshape(96,144)
#        #---------------
#        # mask
#        #---------------
#        a2dens_tmp = ma.masked_where( a2regionmask ==0.0, a2dens)
#        a2dens_tmp = ma.masked_invalid(a2dens_tmp)
#        #---------------
#        # mean dens
#        #---------------
#        dlv[reg, era, iclass].append( a2dens_tmp.mean() )
#      #-----------------
#      # calc regional mean
#      #-----------------
#      dmv[reg, era, iclass]       = mean(dlv[reg, era, iclass])
#      #-----------------
#    #-----------------
#    # calc t-value
#    #-----------------
#    dtv[reg, iclass] = func.ret_tv_difmean(dlv[reg, "his",iclass], dlv[reg, "fut",iclass])
#    print iclass, dtv[reg, iclass]
#    #-----------------
#    # calc difference of regional mean
#    #-----------------
#    dfcm[reg, iclass] = (mean(dlv[reg, "fut", iclass]) - mean(dlv[reg, "his", iclass]))/mean(dlv[reg,"his",iclass]) * 100.0
#
##****************************************
## write csv
##----------------------------------------
#csvdir = csvdir_root + "/%04d.%04d-%04d.%04d"%(diyear["his"], deyear["his"], diyear["fut"], deyear["fut"])
#
#func.mk_dir(csvdir)
#
##------------
#for reg in lreg:
#  #--------
#  # name
#  #--------
#  statname = csvdir + "/stat.%s.csv"%(reg)
#  #--------
#  sstat = "class,his,fut,frac.chng,t\n"
#  for iclass in lclass:
#    sstat = sstat + "%s,%s,%s,%s,%s"%( iclass, dmv[reg, "his", iclass], dmv[reg, "fut", iclass], dfcm[reg, iclass], dtv[reg, iclass]) + "\n"
#  #--------
#  # write
#  #--------
#  f = open(statname, "w")
#  f.write(sstat)
#  f.close()
#  print statname 
#
#
#
#
