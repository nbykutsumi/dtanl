from numpy import *
import os
#-------------------------------------
tstp = "day"
model = "NorESM1-M"
ens  = "r1i1p1"
xth =99.0
nx = 144
ny = 96
rmiss = -9999
lvar = ["Prec","dynam", "lapse", "humid", "full", "LCL_full"]
#---------------------------
def mk_dir(sdir):
  try:
    os.makedirs(sdir)
  except:
    pass
#---------------------------
# set sofiles
#---------------------------
somapdir   = "/media/disk2/out/CMIP5/%s/%s/scales/%s/map"%(tstp, model, ens)
mk_dir(somapdir)
#---------------------------
dsiname={}
dsiname["Prec"]  = somapdir + "/dP.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
dsiname["dynam"] = somapdir + "/dP.dynam.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
dsiname["lapse"] = somapdir + "/dP.lapse.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
dsiname["humid"] = somapdir + "/dP.humid.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
dsiname["full"]  = somapdir + "/dP.full.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
dsiname["LCL_full"] = somapdir + "/dP.lcl_full.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
#---------------------------
dsoname={}
dsoname["Prec"]  = somapdir + "/msked.dP.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
dsoname["dynam"] = somapdir + "/msked.dP.dynam.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
dsoname["lapse"] = somapdir + "/msked.dP.lapse.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
dsoname["humid"] = somapdir + "/msked.dP.humid.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
dsoname["full"]  = somapdir + "/msked.dP.full.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
dsoname["LCL_full"] = somapdir + "/msked.dP.lcl_full.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
#---------------------------
for var in lvar:
  siname = dsiname[var]
  soname = dsoname[var]
  dat = fromfile( siname, float32)
  dat = ma.masked_equal(dat, rmiss)
  dat = ma.filled(dat, NaN)
  dat.tofile( soname )
  print soname 
#---------------------------
# for LCL_full 
#---------------------------
siname = dsoname[var]
soname = siname
sfull = dsiname["full"]
#--
datfull = fromfile( sfull, float32)
dat     = fromfile( siname, float32)
dat     = ma.masked_where( (-1 <= datfull) & (datfull <= 1), dat)
dat     = ma.filled(dat, NaN)
dat.tofile(soname)
