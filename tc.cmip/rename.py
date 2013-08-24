import os
lvar = ["life","nextpos"]

ens  = "r1i1p1"
for var in lvar:
  sdir="/media/disk2/out/CMIP5/sa.one.MIROC5.historical/6hr/%s"%(var)
  for root, dirs, files in os.walk(sdir):
    for fname in files:
      shead = fname.split(".")[0]      
      shead2 = fname.split(".")[1]
      if (shead==var)&(shead2 != ens)&(fname[-6:] =="sa.one"):
        #iname = root + "/%s"%(fname)
        #oname = root + "/%s.%s.%s.sa.one"%(shead,ens,shead2)
        #print oname
