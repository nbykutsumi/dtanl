iyear    = 2004
eyear    = 2004
#lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3","test.1.5deg","test.10deg","test.5deg","test.3deg"]
lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
thfrac   = 0.05

#***********************************
#--- dt ---------
idir     = "/media/disk2/out/obj.valid/tc.dt"
dv = {}
for model in lmodel:
  listname = idir + "/dt.%s.%04d-%04d.csv"%(model,iyear,eyear)
  f  = open(listname, "r"); lines = f.readlines();  f.close()
  #
  for line in lines[1:]:
    line  = map(float, line.split(","))
    frac  = line[0]
    if frac >= thfrac:
      dv[model] = line[1]
      #
      break
#--- print -----------
for model in lmodel:
  print \
'  if model=="%s":\n\
    thwcore = %.2f'%(model,dv[model])


print ""
#***********************************
#--- rvort ----
idir     = "/media/disk2/out/obj.valid/tc.vort"
dv = {}
for model in lmodel:
  listname = idir + "/vort.%s.%04d-%04d.csv"%(model,iyear,eyear)
  f  = open(listname, "r"); lines = f.readlines();  f.close()
  #
  for line in lines[1:]:
    line  = map(float, line.split(","))
    frac  = line[0]
    if frac >= thfrac:
      dv[model] = line[1]
      #
      break
#--- print -----------
for model in lmodel:
  print \
'  if model=="%s":\n\
    thrvort = %.1e'%(model,dv[model])

