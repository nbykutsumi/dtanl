lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3","test.1.5deg","test.10deg","test.5deg","test.3deg"]

iyear  = 2004
eyear  = 2004
idir   = "/media/disk2/out/obj.valid/exc.pgrad"

dlfrac    = {}
dlv       = {}
for model in lmodel:
  iname  = idir + "/cum.pgrad.%s.%04d-%04d.csv"%(model,iyear,eyear)
  f = open(iname, "r"); lines=f.readlines(); f.close()
  #
  dlfrac[model]  = []
  dlv[model]     = []
  for line in lines[1:]:
    line = map(float,line.strip().split(","))
    dlfrac[model].append(line[1])
    dlv[model].append(line[0])
#--- make sout -----------
sout = "fraction/pgrad(hPa/100km)"
for model in lmodel:
  sout = sout +",%s"%(model)
sout = sout +"\n"

lfrac = dlfrac[lmodel[0]]
for i in range(len(lfrac)):
  sout = sout + "%f"%(lfrac[i])
  for model in lmodel:
    sout = sout + ",%.3f"%(dlv[model][i])
  sout = sout + "\n"
#--------------------------
soname = idir + "/cum.pgrad.%04d-%04d.csv"%(iyear,eyear)
f=open(soname,"w"); f.write(sout); f.close()
print soname



