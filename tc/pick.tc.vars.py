iyear    = 2004
eyear    = 2004
#lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3","test.1.5deg","test.10deg","test.5deg","test.3deg"]
#lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel = ["org"]
thfrac   = 0.05
lregion = ["GLB","PNW", "PNE","INN","INS", "PSW","ATN"]
#***********************************
for region in lregion:
  print ""
  print region
  print ""
  #--- dt ---------
  idir     = "/media/disk2/out/obj.valid/tc.dt/%s"%(region)
  dv = {}
  for model in lmodel:
    listname = idir + "/dt.%s.%04d-%04d.%s.csv"%(model,iyear,eyear,region)
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
    if model == "org":
      print \
    '  if model in ["org","anl_p"]:\n\
        thwcore = %.2f'%(dv[model])
    else: 
      print \
    '  if model=="%s":\n\
        thwcore = %.2f'%(model,dv[model])
    
  
  print ""
  #***********************************
  #--- rvort ----
  idir     = "/media/disk2/out/obj.valid/tc.vort/%s"%(region)
  dv = {}
  for model in lmodel:
    listname = idir + "/vort.%s.%04d-%04d.%s.csv"%(model,iyear,eyear,region)
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
    if model == "org":
      print \
    '  if model in ["org","anl_p"]:\n\
        thrvort = %.1e'%(dv[model])
    else:
       print \
    '  if model=="%s":\n\
        thrvort = %.1e'%(model,dv[model])
    
