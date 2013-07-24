iyear    = 2004
eyear    = 2004
idir     = "/media/disk2/out/obj.valid/exc.pgrad"
lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3","test.1.5deg","test.10deg","test.5deg","test.3deg"]
thfrac   = 0.05

dpgradmin = {}

for model in lmodel:
  listname = idir + "/cum.pgrad.%s.%04d-%04d.csv"%(model,iyear,eyear)
  f  = open(listname, "r"); lines = f.readlines();  f.close()
  #
  for line in lines[1:]:
    line  = map(float, line.split(","))
    frac  = line[1]
    print model, frac
    if frac >= thfrac:
      dpgradmin[model] = line[0]
      #
      break
#--- print -----------
for model in lmodel:
  if model == "org":
    print \
  '  if model in ["org","anl_p"]:\n\
      pgradmin = %.3f'%(dpgradmin[model])
  else:
    print \
  '  if model=="%s":\n\
      pgradmin = %.3f'%(model,dpgradmin[model])

