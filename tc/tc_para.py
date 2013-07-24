#*******************************************
def ret_thsst():
  return 273.15 + 25.0
def ret_thwcore(model="org"):
  #-------------------
  # thwcore : (K)
  #-------------------
  if model in ["org","anl_p"]:
      thwcore = 0.23
  if model=="HadGEM2-ES":
      thwcore = 0.22
  if model=="IPSL-CM5A-MR":
      thwcore = 0.18
  if model=="CNRM-CM5":
      thwcore = 0.22
  if model=="MIROC5":
      thwcore = 0.22
  if model=="inmcm4":
      thwcore = 0.21
  if model=="MPI-ESM-MR":
      thwcore = 0.22
  if model=="CSIRO-Mk3-6-0":
      thwcore = 0.22
  if model=="NorESM1-M":
      thwcore = 0.17
  if model=="IPSL-CM5B-LR":
      thwcore = 0.12
  if model=="GFDL-CM3":
      thwcore = 0.17

  #-------------------
  return thwcore
#*******************************************
def ret_thrvort(model="org"):
  #--------------------
  # thrvort : (s-1)
  #--------------------
  if model in ["org","anl_p"]:
      thrvort = 4.7e-05
  if model=="HadGEM2-ES":
      thrvort = 4.4e-05
  if model=="IPSL-CM5A-MR":
      thrvort = 3.9e-05
  if model=="CNRM-CM5":
      thrvort = 4.4e-05
  if model=="MIROC5":
      thrvort = 4.4e-05
  if model=="inmcm4":
      thrvort = 4.1e-05
  if model=="MPI-ESM-MR":
      thrvort = 4.1e-05
  if model=="CSIRO-Mk3-6-0":
      thrvort = 4.1e-05
  if model=="NorESM1-M":
      thrvort = 3.8e-05
  if model=="IPSL-CM5B-LR":
      thrvort = 3.4e-05
  if model=="GFDL-CM3":
      thrvort = 3.7e-05

  #--------------------
  return thrvort
#*******************************************
def ret_thwind():
  thwind = -9999.0
  return thwind
#*******************************************
