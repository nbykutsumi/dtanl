import os
sdir="/media/disk2/out/dtanl/WcfsrPcfsr"
lhead=["pac2","pacc","pave","pstd","wtim"]

iy=1996
ey=1998
lm= [6,7,8]
for head in lhead:
  for m in lm:
    iname= sdir + "/%s.%04d%02d-%04d%02d-61b-0.5.nc" %(head, iy, m, ey, m)
    oname= sdir + "/%s.%04d-%04d-%02d-61b-0.5.nc" %(head, iy,ey,m)
    os.system("mv %s %s"%(iname,oname))

