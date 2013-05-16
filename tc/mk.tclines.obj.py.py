import subprocess

iyear   = 2004
eyear   = 2004
lseason  = ["ALL"]
lthdura  = [36]
#lthwcore = [1.0,0.5]
lthwcore = [2.0]
lthlat   = [90.0]
lthwind  = [10, 15]
lthrvort = [2.0e-5, 3.5e-5, 7.0e-5]
lplev_low = [850*100.0]
lplev_mid = [500*100.0]
lplev_up  = [300*100.0]  ##
ltplev_low= [700*100.0]  ##
#ltplev_low= [850*100.0]  ##

for season in lseason:
  for thdura in lthdura:
    for thwcore in lthwcore:
      for thlat in lthlat:
        for thwind in lthwind:
          for thrvort in lthrvort:
            for plev_low in lplev_low:
              for plev_mid in lplev_mid:
                for plev_up in lplev_up:
                  for tplev_low in ltplev_low:
                    scm = "./mk.tclines.obj.py"
                    sarg = "python %s %s %s %s %s %s %s %s %s %s %s %s %s"\
                       %(scm, iyear, eyear, season, thdura, thwcore, thlat, thwind, thrvort, plev_low, plev_mid, plev_up, tplev_low)
                    subprocess.call(sarg, shell=True)
