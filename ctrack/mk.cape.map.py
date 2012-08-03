import sys
from numpy import *
from calcsound_fort import *
#-------------------
nz = 8
ny = 96
nx = 144
#-------------------
def interp_fill(a1, nresol):
  n = len(a1)
  lout = []
  for i in range(n-1):
    ltemp  = list( linspace(a1[i], a1[i+1], nresol) )
    #-----
    lout   = lout + ltemp
  #----
  lout = lout + [a1[-1]]
  aout = array(lout)
  return aout
#--------------------
def cut_underground(orog, a1zg, a1):
  aout = ma.masked_where(a1zg <orog, a1)
  aout = aout.compressed()
  return aout
#--------------------
nresol = 10
ddir   = {}
dname  = {}
da3    = {}
da2    = {}
da1    = {}
#-- read data--------------------
for var in ["ta", "hus", "zg", "wap"]:
  ddir[var]  = "/media/disk2/data/CMIP5/bn/%s/day/NorESM1-M/historical/r1i1p1"%(var)
  dname[var] = ddir[var] + "/1990/%s_day_NorESM1-M_historical_r1i1p1_1990010100.bn"%(var)
  da3[var]   = fromfile(dname[var], float32).reshape(nz, ny, nx)

#-- read plev-------------------
dname["plev"] = ddir["ta"] + "/lev.txt"
f   = open(dname["plev"], "r")
da1["plev"]   = array( map(float, f.readlines()))

#-- orog ---
ddir["orog"]  = "/media/disk2/data/CMIP5/bn/%s/fx/NorESM1-M/historical/r0i0p0"%("orog")
dname["orog"] = ddir["orog"] + "/%s_fx_NorESM1-M_historical_r0i0p0.bn"%("orog")
da2["orog"]  = fromfile(dname["orog"], float32).reshape(ny, nx)

#-- prec ---
for var in ["pr"]:
  ddir[var]  = "/media/disk2/data/CMIP5/bn/%s/day/NorESM1-M/historical/r1i1p1"%(var)
  dname[var] = ddir[var] + "/1990/%s_day_NorESM1-M_historical_r1i1p1_1990010100.bn"%(var)
  da2[var]   = fromfile(dname[var], float32).reshape(ny, nx)

#--------------------------------
aoutp = zeros([ny,nx], float32)
apap  = zeros([ny,nx], float32)
apr   = zeros([ny,nx], float32)
awap  = zeros([ny,nx], float32)
iy0 = 40
#for iy in range(0,96):
#for iy in [50]:
for iy in range(iy0,iy0+4):
  for ix in range(0, 144):
  #for ix in [10]:
    #--------------------------------
    for var in ["ta", "hus", "zg"]:
      da1[var]  = da3[var][:,iy,ix]

    #----
    orog       = da2["orog"][iy,ix]
    #----
    a1plev     = cut_underground(orog, da1["zg"], da1["plev"])
    a1ta       = cut_underground(orog, da1["zg"], da1["ta"])
    a1hus      = cut_underground(orog, da1["zg"], da1["hus"])

    #----
    a1plev     = interp_fill(a1plev, nresol)
    a1ta       = interp_fill(a1ta,   nresol)
    a1hus      = interp_fill(a1hus,   nresol)
    #----
    lout = calcsound_fort.cape_1d(a1ta, a1plev, a1hus)
    #if orog > da3["zg"][0,iy,ix]:
    #  print "AAAAAAAAAAAAAAAAAAAAA" 
    print iy, ix, lout[1][0], lout[3][0]
    aoutp[iy,ix] = mean(lout[1][0:3])
    apap[iy,ix]  = mean(lout[3][0:3])
    apr[iy,ix]   = da2["pr"][iy,ix]
    awap[iy,ix]  = da3["wap"][3,iy,ix]
