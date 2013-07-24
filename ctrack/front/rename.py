import os

idir_root = "/media/disk2/out/chart/ASAS/front"
for root, dirs, names in os.walk(idir_root):
  for sname in names:
    if sname[-6:] == ".saone":
      oldname = root+"/" + sname
      newname = root+"/" + sname[:-6] + ".sa.one"
      print oldname 
      print newname
      #os.rename(oldname, newname)
