lmodel = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3","test.1.5deg","test.3deg","test.5deg","test.10deg"]
#lmodel = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3","test.1.5deg"]
#lmodel = ["HadGEM2-ES"]
iyear  = 2004
eyear  = 2004
var = "PRMSL"
#var = "UGRD"
#----------------------------------
def read_csv(csvname):
  f = open(csvname,"r")
  lines = f.readlines()
  f.close()
  ldist  = []
  lv     = []
  lsd    = []
  for line in lines[1:]:
    line = line.strip().split(",")
    dist = float(line[0])
    v    = float(line[1])
    sd   = float(line[2])
    ldist.append(dist)
    lv.append(v)
    lsd.append(sd)
  #
  return ldist, lv, lsd
#----------------------------------
dv   = {}
dsd  = {}

for model in lmodel:
  idir    = "/media/disk2/out/obj.valid/exc.%s"%(var)
  csvname = idir + "/%s.%s.%04d-%04d.csv"%(var, model, iyear, eyear)
  lout = read_csv(csvname) 
  ldist      = lout[0]
  dv[model]  = lout[1]
  dsd[model] = lout[2]
#----------------------------------
#-- write to file ----
odir    = idir
soname  = odir + "/%s.%04d-%04d.csv"%(var, iyear, eyear)

#--label --
sout = "dist"
for model in lmodel:
  sout = sout + ",%s"%(model)
#
sout = sout + "\n"

#--value --
for idist in range(len(ldist)):
  dist = ldist[idist]
  sout = sout + "%d"%(dist)
  for model in lmodel:
    v    = dv[model][idist]
    sout = sout + ",%s"%(v)
  #
  sout = sout + "\n"
#----------
f = open(soname,"w"); f.write(sout); f.close()
print soname 
