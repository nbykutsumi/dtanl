import os, shutil

idir_root = "/media/disk2/out/JRA25/sa.one.anl_p/6hr/tagexpr/wn.c48h.tc48h"

for root, dirs, files in os.walk(idir_root):
  for ifile in files:
    if (ifile[:9]=="num.GSMaP")or(ifile[:10]=="totalcount"):
      iname = root + "/%s"%(ifile)
      odir      = "/".join(root.split("/")[:-2]) + "/nn.c48h.tc48h/" + root.split("/")[-1]
      oname = odir + "/%s"%(ifile)

