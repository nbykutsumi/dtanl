import subprocess
import tc_para

#lbstflag = ["obj","bst"]
lbstflag = ["obj","bst"]
lyear   = [2008,2009,2010]
lseason  = ["JJAS"]
region   = "INDIA"

model = "org"
thsst    = tc_para.ret_thsst()
thwind   = tc_para.ret_thwind()
thrvort  = tc_para.ret_thrvort(model)
thwcore  = tc_para.ret_thwcore(model)

thdura  = 72
thwcore = thwcore
thsst   = thsst
thwind  = thwind
thrvort = thrvort
plev_low = 850*100.0
plev_mid = 500*100.0
plev_up  = 250*100.0  ##
tplev_low= 850*100.0  ##

for year in lyear:
  for season in lseason:
    for bstflag in lbstflag:
      if bstflag == "obj":
        scm = "./mk.tclines.obj.region.py"
        sarg = "python %s %s %s %s %s %s %s %s %s %s %s %s %s %s"\
           %(scm, year, season, thdura, thwcore, thsst, thwind, thrvort, plev_low, plev_mid, plev_up, tplev_low, model, region)
        subprocess.call(sarg, shell=True)

      if bstflag == "bst":
        scm = "./mk.tclines.ibtracs.region.py"
        sarg = "python %s %s %s %s"%(scm, year, season, region)
        subprocess.call(sarg, shell=True)




