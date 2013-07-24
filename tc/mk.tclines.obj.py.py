import subprocess
import tc_para

iyear   = 2004
eyear   = 2004
#lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel = ["org"]
for model in lmodel:
  
  thsst    = tc_para.ret_thsst()
  thwind   = tc_para.ret_thwind()
  thrvort  = tc_para.ret_thrvort(model)
  thwcore  = tc_para.ret_thwcore(model)
  
  lseason  = ["ALL"]
  lthdura  = [72]
  lthwcore = [thwcore]
  lthsst   = [thsst]
  lthwind  = [thwind]
  lthrvort = [thrvort]
  lplev_low = [850*100.0]
  lplev_mid = [500*100.0]
  lplev_up  = [250*100.0]  ##
  ltplev_low= [850*100.0]  ##

  for season in lseason:
    for thdura in lthdura:
      for thwcore in lthwcore:
        for thsst in lthsst:
          for thwind in lthwind:
            for thrvort in lthrvort:
              for plev_low in lplev_low:
                for plev_mid in lplev_mid:
                  for plev_up in lplev_up:
                    for tplev_low in ltplev_low:
                      scm = "./mk.tclines.obj.py"
                      sarg = "python %s %s %s %s %s %s %s %s %s %s %s %s %s %s"\
                         %(scm, iyear, eyear, season, thdura, thwcore, thsst, thwind, thrvort, plev_low, plev_mid, plev_up, tplev_low, model)
                      subprocess.call(sarg, shell=True)
