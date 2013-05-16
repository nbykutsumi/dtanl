from numpy import *
#------------------------------------------------
def ret_thfmask(resol):
  if resol=="anl_p25":
    thfmasktheta1 = 0.6
    thfmasktheta2 = 2.0
  elif resol =="anl_p":
    thfmasktheta1 = 0.6
    thfmasktheta2 = 2.0
  #---
  return (thfmasktheta1, thfmasktheta2)
#-------------------------------------------------

