import os
idir_root = "/media/disk2/out/ibtracs/sa.one"
for (root, ldir, lfile) in os.walk(idir_root):
  if ldir == []:
    for sfile in lfile:
      if sfile[-6:] == ".saone":
        siname = root + "/" + sfile
        soname = root + "/" + sfile[:-6] + ".sa.one"
        os.rename(siname, soname)
        print siname
        print soname
