from numpy import *
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

