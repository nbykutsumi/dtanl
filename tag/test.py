import gsmap_func, aphro_func
from numpy import *

iname = "/home/utsumi/mnt/mizu.tank/utsumi/tag.pr/c48h.tc48h.bsttc1000.c1000.f0500/APHRO_MA.day/200101/pr.c.2001.01.08.00.sa.one"

a  = aphro_func.loadas_a2global(iname, "MA", -9999.0)
b  = aphro_func.global2aphro_one( a, "MA")
#a = fromfile(iname, float32).reshape(70,360)
#b = gsmap_func.global2gsmap_one(a)
#b = aphro_func.global2aphro_one(a, "APHRO_MA")

print a
odir = "."
aphro_func.mk_metadata_one(odir, "MA")
