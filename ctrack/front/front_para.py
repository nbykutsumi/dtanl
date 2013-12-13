from numpy import *
#------------------------------------------------
def ret_thfmasktq(sresol="anl_p"):
  if sresol in ["anl_p","MRI-CGCM3"]:
    thfmask1t = 0.3
    thfmask2t = 1.0
    thfmask1q = 2.0*1.0e-4
    thfmask2q = 1.5*1.0e-3
  if sresol =="HadGEM2-ES":
    thfmask1t = 0.3
    thfmask2t = 1.0
    thfmask1q = 2.0*1.0e-4
    thfmask2q = 1.5*1.0e-3
  if sresol =="IPSL-CM5A-MR":
    thfmask1t = 0.3
    thfmask2t = 1.0
    thfmask1q = 2.0*1.0e-4
    thfmask2q = 1.5*1.0e-3
  if sresol =="CNRM-CM5":
    thfmask1t = 0.26
    thfmask2t = 1.0
    thfmask1q = 2.0*1.0e-4
    thfmask2q = 1.5*1.0e-3
  if sresol =="MIROC5":
    thfmask1t = 0.26
    thfmask2t = 1.0
    thfmask1q = 2.0*1.0e-4
    thfmask2q = 1.5*1.0e-3
  if sresol =="inmcm4":
    thfmask1t = 0.26
    thfmask2t = 1.0
    thfmask1q = 2.0*1.0e-4
    thfmask2q = 1.5*1.0e-3
  if sresol =="MPI-ESM-MR":
    thfmask1t = 0.26
    thfmask2t = 0.6
    thfmask1q = 2.0*1.0e-4
    thfmask2q = 1.5*1.0e-3
  if sresol =="CSIRO-Mk3-6-0":
    thfmask1t = 0.26
    thfmask2t = 0.6
    thfmask1q = 2.0*1.0e-4
    thfmask2q = 1.5*1.0e-3
  if sresol =="NorESM1-M":
    thfmask1t = 0.26
    thfmask2t = 0.6
    thfmask1q = 2.0*1.0e-4
    thfmask2q = 1.5*1.0e-3
  if sresol =="IPSL-CM5B-LR":
    thfmask1t = 0.26
    thfmask2t = 0.6
    thfmask1q = 2.0*1.0e-4
    thfmask2q = 1.5*1.0e-3
  if sresol =="GFDL-CM3":
    thfmask1t = 0.26
    thfmask2t = 0.6
    thfmask1q = 2.0*1.0e-4
    thfmask2q = 1.5*1.0e-3
  #---
  return (thfmask1t, thfmask2t, thfmask1q, thfmask2q)
#------------------------------------------------
def ret_thgrids():
  return 5
#------------------------------------------------
def ret_thfmask(resol):
  if resol=="anl_p25":
    thfmasktheta1 = 0.6
    thfmasktheta2 = 2.0
  elif resol =="anl_p":
    thfmasktheta1 = 0.7
    thfmasktheta2 = 4.0
  #---
  return (thfmasktheta1, thfmasktheta2)
#-------------------------------------------------
def ret_thbc(resol="anl_p"):
  if resol =="anl_p":
    return 0.7 /1000.0/100.0  #(K/m)
#-------------------------------------------------
def ret_thdistkm():
  return 500.0 #  (km)
#-------------------------------------------------
def ret_disthighside():
  return 100.0 * 1000.0  #(m)

