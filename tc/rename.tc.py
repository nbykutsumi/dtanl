import os
model  = "anl_p"
thdura = 48
idir  = "/media/disk2/out/JRA25/sa.one.%s/6hr/tc/pot.tc.%02dh.sst25.wind-9999.vor4.7e-05"%(model,thdura)


for path, dirs, fnames in os.walk(idir):
  for fname in fnames:
    iname  = path + "/" + fname
    if (fname[:6] == "tc.sst")&(fname[-6:]=="sa.one"):
      oname  = path + "/pot.tc." + fname[30:]
      print "*****************************"
      print oname
      os.rename(iname, oname)
