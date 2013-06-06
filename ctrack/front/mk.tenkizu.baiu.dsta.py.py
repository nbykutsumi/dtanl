import subprocess
iyear  = 2004
eyear  = 2004
#lmon   = [6,7,2,4,8,9,11]
lmon   = [8,9,11]
sresol = "anl_p"

#-----------------------------------
for year in range(iyear,eyear+1):
  for mon in lmon:
    scmd  = "python ./mk.tenkizu.baiu.dsta.py %s %s %s"%(year,mon,sresol)
    subprocess.call(scmd, shell=True)
