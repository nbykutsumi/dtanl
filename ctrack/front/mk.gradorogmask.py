from numpy import *
from dtanl_fsub import *
import ctrack_fig
#----------------------------
nx = 360
ny = 180
miss = -9999.0
thorogmask1 = 0.0
thorogmask2 = 100.0
#*********************************************************
def mk_orogmask_loc(a2thermo, a2gradthermo, thfmask1, thfmask2):
  a2fmask1 = dtanl_fsub.mk_a2frontmask1(a2thermo.T).T
  a2fmask2 = dtanl_fsub.mk_a2frontmask2(a2thermo.T).T
  a2fmask1 = a2fmask1 *(1000.0*100.0)**2.0  #[(100km)-2]
  a2fmask2 = a2fmask2 *(1000.0*100.0)       #[(100km)-1]

  a2loc    = a2gradthermo
  a2loc    = ma.masked_where(a2fmask1 < thfmask1, a2loc)
  a2loc    = ma.masked_where(a2fmask2 < thfmask2, a2loc)
  return a2loc
#*********************************************************
cbarname              = "/media/disk2/data/JRA25/sa.one/const/topo/grad.topo.adj.cbar.png"

#---------------------------------
##-- adj orog & grad orog ----
#orogname   = "/media/disk2/data/JRA25/sa.one/const/topo/topo.sa.one"
#gradorog_adj_name = "/media/disk2/data/JRA25/sa.one/const/topo/grad.topo.adj.sa.one"
#fig_gradorog_adj_name = "/media/disk2/data/JRA25/sa.one/const/topo/grad.topo.adj.png"
#cbarname              = "/media/disk2/data/JRA25/sa.one/const/topo/grad.topo.adj.cbar.png"
#a2orog     = fromfile(orogname, float32).reshape(ny,nx)
#a2gradorog = dtanl_fsub.mk_a2grad_abs_saone(a2orog.T).T
#a2gradorogmask = dtanl_fsub.mk_a2adj(a2gradorog.T).T *1000.0 # m/km
#
#a2gradorogmask.tofile(gradorog_adj_name)
#
#bnd  = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0]
#ctrack_fig.mk_pict_saone_reg(a2gradorogmask, soname=fig_gradorog_adj_name, cbarname=cbarname, bnd=bnd)
#print gradorog_adj_name


#-- adj orog & grad orog ----
orogname   = "/media/disk2/data/JRA25/sa.one/const/topo/topo.sa.one"
gradorog_adj_name = "/media/disk2/data/JRA25/sa.one/const/topo/grad.topo.adj.twogrids.sa.one"
fig_gradorog_adj_name = "/media/disk2/data/JRA25/sa.one/const/topo/grad.topo.adj.twogrids.png"

a2orog     = fromfile(orogname, float32).reshape(ny,nx)
a2gradorog = dtanl_fsub.mk_a2grad_abs_saone(a2orog.T).T
a2gradorogmask = dtanl_fsub.mk_a2adj_multigrids(a2gradorog.T, 2).T *1000.0 # m/km

bnd  = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0]
a2gradorogmask.tofile(gradorog_adj_name)
ctrack_fig.mk_pict_saone_reg(a2gradorogmask, soname=fig_gradorog_adj_name, cbarname=cbarname, bnd=bnd)

print gradorog_adj_name

#-- orog fmask ----
orogname   = "/media/disk2/data/JRA25/sa.one/const/topo/topo.sa.one"
soname = "/media/disk2/data/JRA25/sa.one/const/topo/grad.topo.fmasked.sa.one"
figname = "/media/disk2/data/JRA25/sa.one/const/topo/grad.topo.fmasked.png"

a2orog     = fromfile(orogname, float32).reshape(ny,nx)
a2gradorog = dtanl_fsub.mk_a2grad_abs_saone(a2orog.T).T

a2out      = mk_orogmask_loc(a2orog, a2gradorog, thorogmask1, thorogmask2)
a2out      = a2out.filled(miss)

bnd  = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0]
a2out.tofile(soname)
ctrack_fig.mk_pict_saone_reg(a2out, soname=figname, cbarname=cbarname, bnd=bnd)

print figname


##-- adj orog & grad orog ----
#orogname   = "/media/disk2/data/JRA25/sa.one/const/topo/topo.sa.one"
#gradorog_adj_name = "/media/disk2/data/JRA25/sa.one/const/topo/grad.topo.adj.threegrids.sa.one"
#fig_gradorog_adj_name = "/media/disk2/data/JRA25/sa.one/const/topo/grad.topo.adj.threegrids.png"
#
#a2orog     = fromfile(orogname, float32).reshape(ny,nx)
#a2gradorog = dtanl_fsub.mk_a2grad_abs_saone(a2orog.T).T
#a2gradorogmask = dtanl_fsub.mk_a2adj_multigrids(a2gradorog.T, 3).T *1000.0 # m/km
#
#bnd  = [0.0, 2.0, 4.0, 6.0, 8.0, 10.0, 12.0, 14.0]
#a2gradorogmask.tofile(gradorog_adj_name)
#ctrack_fig.mk_pict_saone_reg(a2gradorogmask, soname=fig_gradorog_adj_name, cbarname=cbarname, bnd=bnd)
#
#print gradorog_adj_name



