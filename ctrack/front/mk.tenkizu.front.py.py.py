import subprocess

iyear = 2004
eyear = 2004
lmon  = [4,11]
sresol = "anl_p"
for year in range(iyear,eyear+1):
  for mon in lmon:
    scmd  = "python ./mk.tenkizu.front.py.py %d %d %d %s"%(iyear,eyear,mon,sresol)
    subprocess.call(scmd, shell=True)
