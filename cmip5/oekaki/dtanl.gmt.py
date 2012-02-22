import os
#---------------------------
tstp   = "day"
model  = "NorESM1-M"
ens    = "r1i1p1"
xth    = 99.0
#---------------------------
def mk_dirs(sdir):
  try:
    os.makedirs(sdir)
  except OSError:
    pass
#---------------------------
lvar = ["Prec", "dynam", "lapse", "humid", "full", "LCL_full"]
cmd_withsea="/home/utsumi/bin/dtanl/cmip5/oekaki/dtanl.gmt"
cmd_nosea="/home/utsumi/bin/dtanl/cmip5/oekaki/dtanl.nosea.gmt"
#----------
#simapdir   = "/media/disk2/out/CMIP5/%s/%s/scales/%s/map"%(tstp, model, ens)
#somapdir   = "/media/disk2/out/CMIP5/%s/%s/scales/%s/map/pict"%(tstp, model, ens)
simapdir   = "/media/disk2/out/CMIP5/%s/%s/scales/%s/his.m.fut.m/map"%(tstp, model, ens)
somapdir   = "/media/disk2/out/CMIP5/%s/%s/scales/%s/his.m.fut.m/map/pict"%(tstp, model, ens)

mk_dirs(somapdir)
#----------
dsiname={}
#dsiname["Prec"]     = simapdir + "/msked.dP.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
#dsiname["dynam"]    = simapdir + "/msked.dP.dynam.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
#dsiname["lapse"]    = simapdir + "/msked.dP.lapse.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
#dsiname["humid"]    = simapdir + "/msked.dP.humid.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
#dsiname["full"]     = simapdir + "/msked.dP.full.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
#dsiname["LCL_full"] = simapdir + "/msked.dP.lcl_full.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
dsiname["Prec"]     = simapdir + "/epl.dP.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
dsiname["dynam"]    = simapdir + "/epl.dP.dynam.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
dsiname["lapse"]    = simapdir + "/epl.dP.lapse.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
dsiname["humid"]    = simapdir + "/epl.dP.humid.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
dsiname["full"]     = simapdir + "/epl.dP.full.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
dsiname["LCL_full"] = simapdir + "/epl.dP.lcl_full.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)

#----------


#
#ifile="/home/utsumi/oekaki/dtanl/data/dP99.humid.bn"
cptfileLCL_full   = "/home/utsumi/bin/dtanl/cmip5/oekaki/cpt/polar.-0.3.0.3.finer.cpt"
cptfile10  = "/home/utsumi/bin/dtanl/cmip5/oekaki/cpt/polar.-10.10.cpt"
cptfile100 = "/home/utsumi/bin/dtanl/cmip5/oekaki/cpt/polar.-100.100.cpt"

for var in lvar:
  #--------------------
  if var == "LCL_full":
    cmd = cmd_nosea
    cptfile = cptfileLCL_full
    scalestep= 0.1
  elif var == "humid":
    cmd = cmd_withsea
    cptfile = cptfile10
    scalestep= 2
  else:
    cmd = cmd_withsea
    cptfile = cptfile100
    scalestep= 20
  #---------------------

  ifile = dsiname[var]
  ofile_title=  somapdir + "/" + ifile.split("/")[-1][:-3]
  title = "dP99_%s"%(var)
  #
  os.system("%s %s %s %s %s %s"%(cmd, ifile, cptfile, ofile_title, title, scalestep))
  print ofile_title
