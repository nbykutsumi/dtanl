from numpy import *
#------------------------------------------------
def ret_thfmasktq(sresol="anl_p"):
  if sresol =="anl_p":
    thfmask1t = 0.3
    thfmask2t = 1.0
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

