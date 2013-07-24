import os

ldura = [48,72]

lyear = range(1997,2012+1)
lmon  = range(1,12+1)

idir_root = "/media/disk2/out/JRA25/sa.one.anl_p/6hr/tag"

for root, dirs, files in os.walk(idir_root):
  for sfile in files:
    iname = root + "/" + sfile
    if sfile[:16] == "tag.tc10.c10.f05":
      oname = root + "/tag.tc1000.c1000.f0500" + sfile[16:]
      os.rename(iname, oname)
      print oname
    elif sfile[:19] == "tag.bsttc10.c10.f05":
      oname = root + "/tag.bsttc1000.c1000.f0500" + sfile[19:]
      os.rename(iname, oname)
      print oname
    elif sfile[:19] == "tag.tc10.c10.bstf05":
      oname = root + "/tag.tc1000.c1000.bstf0500" + sfile[19:]
      os.rename(iname, oname)
      print "CC",oname
    
      
