#lmodel    = ["MIROC5","CCSM4","CNRM-CM5","CSIRO-Mk3-6-0","GFDL-CM3","HadGEM2-ES","IPSL-CM5A-MR","IPSL-CM5B-LR","MPI-ESM-MR","NorESM1-M"]
lmodel    = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]

#lexpr     = ["historical"]
lexpr     = ["rcp85"]

idir      = "/home/utsumi/mnt/iis.data2/CMIP5/cmip5.working"

for expr in lexpr:
  print expr
  print ""
  for model in lmodel:
  
    iname = idir + "/%s.%s.list.csv"%(model, expr)
    f=open(iname,"r"); lines=f.readlines(); f.close()
    #
    line = lines[0].split(",")
    sunit, scalendar = line[17], line[18]
    #
    sout ='elif model == "%s":sunit,scalendar = "%s", "%s"'%(model, sunit,scalendar)
    print sout

 
