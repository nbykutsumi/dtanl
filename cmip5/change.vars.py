from numpy import *
import os
#######################################################################
nx = 144
ny = 96
dnz ={"zg":8, "wap":8, "tas":1, "psl":1, "pr":1, "prc":1, "huss":1, "prxth":1, "rhs":1}

#lvar = ["zg","wap","tas","psl","prc","huss", "prxth", "rhs"]
lvar = ["pr"]

tstp  = "day"
model = "NorESM1-M"
dexpr = {"his":"historical", "fut":"rcp85"}
ens   = "r1i1p1"
dlyrange = {"his":[1990,1999], "fut":[2086,2095]}
#season = "ALL"
season = "DJF"
xth = 0.0
###
exp_his = dexpr["his"]
exp_fut = dexpr["fut"]
iyear_his = dlyrange["his"][0]
eyear_his = dlyrange["his"][1]
iyear_fut = dlyrange["fut"][0]
eyear_fut = dlyrange["fut"][1]
#--
miss = -9999.0
#---------------------------
if season == "ALL":
  im = 1
  em = 12
elif season == "DJF":
  im = 12
  em = 2
#########################################################################
# function
#########################################################################
def expand_layers(anan, nz):
  aout = ma.array([])
  for i in range(1, nz+1):
    aout = ma.concatenate( (aout, anan) )
  #
  return aout
#####################################################
def mk_dir(sdir):
  try:
    os.makedirs(sdir)
  except:
    pass
#########################################################################
# NaN file
#########################################################################
#nandir = "/media/disk2/out/CMIP5/%s/%s/scales/%s/map" %(tstp, model, ens)
#nanfile = nandir + "/nan.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
#anan_org   = fromfile( nanfile, float32)
#########################################################################
for var in lvar:
  print "var=",var
  #-------------
  nz = dnz[var]
  #anan = expand_layers(anan_org, nz)
  #-------------
  # "pr"
  #-------------
  if var == "prxth":
    idir_his = "/media/disk2/out/CMIP5/%s/%s/%s/%s/prxth/%04d-%04d/%02d-%02d"\
            %(tstp, model, exp_his, ens, iyear_his, eyear_his, im, em)
    idir_fut = "/media/disk2/out/CMIP5/%s/%s/%s/%s/prxth/%04d-%04d/%02d-%02d"\
            %(tstp, model, exp_fut, ens, iyear_fut, eyear_fut, im, em)
    #
    iname_his = idir_his + "/prxth_%s_%s_%s_%s_%06.2f.bn"\
                          %(tstp, model, exp_his, ens, xth)
    iname_fut = idir_fut + "/prxth_%s_%s_%s_%s_%06.2f.bn"\
                          %(tstp, model, exp_fut, ens, xth)
  #-------------
  # other variables
  #-------------
  else: 
    idir_his = "/media/disk2/out/CMIP5/%s/%s/%s/%s/cnd.mean/%s/%04d-%04d/%02d-%02d"\
            %(tstp, model, exp_his, ens, var, iyear_his, eyear_his, im, em)
    idir_fut = "/media/disk2/out/CMIP5/%s/%s/%s/%s/cnd.mean/%s/%04d-%04d/%02d-%02d"\
            %(tstp, model, exp_fut, ens, var, iyear_fut, eyear_fut, im, em)
    #
    iname_his = idir_his + "/%s_%s_%s_%s_%s_%06.2f.bn"\
                          %(var, tstp, model, exp_his, ens, xth)
    iname_fut = idir_fut + "/%s_%s_%s_%s_%s_%06.2f.bn"\
                          %(var, tstp, model, exp_fut, ens, xth)
  #-------------
  #odir ="/media/disk2/out/CMIP5/%s/%s/scales/%s/map" %(tstp, model, ens)
  odir = "/media/disk2/out/CMIP5/day/%s/dif/%s/%04d-%04d.%04d-%04d/%02d-%02d"%(model, exp_fut, iyear_his, eyear_his, iyear_fut, eyear_fut, im, em)
  #----
  mk_dir(odir)
  #----
  oname_withmiss = odir + "/chng.%s_%s_%s_%s_%s_%06.2f.bn"%(var, tstp, model, exp_fut, ens, xth)
  oname_withnan  = odir + "/msked.chng.%s_%s_%s_%s_%s_%06.2f.bn"%(var, tstp, model, exp_fut, ens, xth)
  frac_withmiss = odir + "/frac.chng.%s_%s_%s_%s_%s_%06.2f.bn"%(var, tstp, model, exp_fut, ens, xth)
  frac_withnan  = odir + "/msked.frac.chng.%s_%s_%s_%s_%s_%06.2f.bn"%(var, tstp, model, exp_fut, ens, xth)
  #-----
  afut = fromfile(iname_fut,float32)
  ahis = fromfile(iname_his,float32)
  #######################################################################
  #  change
  #######################################################################
  aout = afut - ahis
  #aout = ma.masked_where(anan == 1.0, aout)
  #
  aout_withmiss= ma.filled(aout, miss)
  aout_withmiss.tofile(oname_withmiss)
  #
  aout_withnan = ma.filled(aout, NaN)
  aout_withnan.tofile(oname_withnan)
  print oname_withmiss
  #######################################################################
  #  fractional change
  #######################################################################
  #aout = (afut - ahis) / ma.masked_where(anan == 1.0, ahis)
  aout = (afut - ahis) / ahis
  #aout = ma.masked_where(anan == 1.0, aout)
  #
  aout_withmiss= ma.filled(aout, miss)
  aout_withmiss.tofile(frac_withmiss)
  #
  aout_withnan = ma.filled(aout, NaN)
  aout_withnan.tofile(frac_withnan)
  print frac_withmiss
