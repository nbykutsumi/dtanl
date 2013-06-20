#lmodel = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3","test.1.5deg","test.10deg","test.5deg","test.3deg"]
lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]

iyear  = 2004
eyear  = 2004
idir_root   = "/media/disk2/out/obj.valid"

#*****************************************************
#--- dt ----------
#-----------------------
idir      = idir_root + "/tc.dt"
dlfrac    = {}
dlv       = {}
for model in lmodel:
  iname  = idir + "/dt.%s.%04d-%04d.csv"%(model,iyear,eyear)
  f = open(iname, "r"); lines=f.readlines(); f.close()
  #
  dlfrac[model]  = []
  dlv[model]     = []
  for line in lines[1:]:
    line = map(float,line.strip().split(","))
    dlfrac[model].append(line[0])

    dlv[model].append(line[1])
#--- make sout -----------
sout = "frac/dt(K)"
for model in lmodel:
  sout = sout +",%s"%(model)
sout = sout[1:] +"\n"

#-------------------------
lfrac = dlfrac[lmodel[0]]
for i in range(len(lfrac)):
  sout_temp = "%s"%(lfrac[i])
  for model in lmodel:
    sout_temp = sout_temp + ",%f"%(dlv[model][i])
  sout = sout + sout_temp +"\n"
#--------------------------
soname = idir + "/dt.%04d-%04d.csv"%(iyear,eyear)
f=open(soname,"w"); f.write(sout); f.close()
print soname

#*****************************************************
#--- vort ----------
#-----------------------
idir      = idir_root + "/tc.vort"
dlfrac    = {}
dlv       = {}
for model in lmodel:
  iname  = idir + "/vort.%s.%04d-%04d.csv"%(model,iyear,eyear)
  f = open(iname, "r"); lines=f.readlines(); f.close()
  #
  dlfrac[model]  = []
  dlv[model]     = []
  for line in lines[1:]:
    line = map(float,line.strip().split(","))
    dlfrac[model].append(line[0])

    dlv[model].append(line[1])
#--- make sout -----------
sout = "frac/vort(s-1)"
for model in lmodel:
  sout = sout +",%s"%(model)
sout = sout[1:] +"\n"

#-------------------------
lfrac = dlfrac[lmodel[0]]
for i in range(len(lfrac)):
  sout_temp = "%s"%(lfrac[i])
  for model in lmodel:
    sout_temp = sout_temp + ",%f"%(dlv[model][i])
  sout = sout + sout_temp +"\n"
#--------------------------
soname = idir + "/vort.%04d-%04d.csv"%(iyear,eyear)
f=open(soname,"w"); f.write(sout); f.close()
print soname


