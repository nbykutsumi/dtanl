from numpy import *
#***********************
alev = arange(1200.0*100, 100.0*100 -1.0, -25.0*100.0)
llev = list(alev)
#***********************
sout = "\n".join(map(str, llev))
sout = sout.strip()
#***********************
sfile = "./lev_f.txt"
f = open(sfile, "w")
f.write(sout)
f.close()
#---
print sout
print sfile
