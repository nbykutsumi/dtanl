import subprocess

lyear = [2007,2008,2009,2010]
for year in lyear:
  scmd  = "python ./extract.front.py %s"%(year)
  subprocess.call(scmd, shell=True)
