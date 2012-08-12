import sys
from numpy import *
import calendar
import ctrack_func
import ctrack_para
from calcsound_fort_old import *
#-------------------
nz6h = 26
ny = 96
nx = 144
nzday = 8

model      = "NorESM1-M"
ens        = "r1i1p1"
lexpr      = ["historical"]
imon       = 1
emon       = 1
yrange      = [1990,1990]
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
def cut_underground_p(ps, a1plev, a1):
  aout = ma.masked_where(a1plev >ps, a1)
  aout = aout.compressed()
  return aout
#--------------------

lh       = [0, 6, 12, 18]
Nparcels = 3

for expr in lexpr:
  #(iyear, eyear)  = ctrack_para.ret_iy_ey(expr)
  (iyear, eyear)  = yrange

  for year in range(iyear, eyear+1):
    for mon in range(imon, emon+1):
      ##############
      # no leap
      ##############
      if (mon==2)&(calendar.isleap(year)):
        ed = calendar.monthrange(year,mon)[1] -1
      else:
        ed = calendar.monthrange(year,mon)[1]
      ##############
      for day in range(1, 1+1):
        #*******************************************
        # 6-hourly
        #*******************************************
        ddir_6hr  = {}
        dname_6hr = {}
        da3_6hr   = {}
        da2_6hr   = {}
        da1_6hr   = {}
        ddir_day  = {}
        dname_day = {}
        #--- read 3D ------------
        for var in ["ta", "hus", "pa"]:
          for h in lh:
            ddir_6hr[var]  = "/media/disk2/data/CMIP5/bn/%s/6hrLev/%s/%s/%s"%(var, model, expr, ens)
            dname_6hr[var, h] = ddir_6hr[var] + "/%04d/%s_6hrLev_%s_%s_%s_%04d%02d%02d%02d.bn"%(year, var, model, expr, ens, year, mon, day, h)
            da3_6hr[var, h]   = fromfile(dname_6hr[var, h], float32).reshape(nz6h, ny, nx)
        #--- ps -----------------
        for var in ["ps"]:
          for h in lh:
            ddir_6hr[var]  = "/media/disk2/data/CMIP5/bn/%s/6hrLev/%s/%s/%s"%(var, model, expr, ens)
            dname_6hr[var,h] = ddir_6hr[var] + "/%04d/%s_6hrLev_%s_%s_%s_%04d%02d%02d%02d.bn"%(year, var, model, expr, ens, year, mon, day, h)
            da2_6hr[var,h]   = fromfile(dname_6hr[var, h], float32).reshape(ny, nx)
        #--- pap : output ------
        for outvar in ["pap", "capep"]:
          ddir_day[outvar]  = "/media/disk2/data/CMIP5/bn/%s/day/%s/%s/%s/%04d"%(outvar, model, expr, ens, year)
          dname_day[outvar] = ddir_day[outvar] + "/%s_day_%s_%s_%s_%04d%02d%02d00.bn"%(outvar, model, expr, ens, year, mon, day)
          ctrack_func.mk_dir(ddir_day[outvar])
          print ddir_day[outvar]
          print dname_day[outvar]
        #*******************************************
        nresol = 5
        ddir   = {}
        dname  = {}
        da3    = {}
        da2    = {}
        da1    = {}
        
        
        #-- wap ---
        #for var in ["wap"]:
        #  ddir[var]  = "/media/disk2/data/CMIP5/bn/%s/day/NorESM1-M/historical/r1i1p1"%(var)
        #  dname[var] = ddir[var] + "/1990/%s_day_NorESM1-M_historical_r1i1p1_1990010100.bn"%(var)
        #  da3[var]   = fromfile(dname[var], float32).reshape(nzday, ny, nx)
        
        #--------------------------------
        iy0 = 40
        dacapep  = {}
        dapap    = {}
        dapr    = {}
        awap  = zeros([ny,nx], float32)
        
        for h in lh:
          dacapep[h] = zeros([ny,nx], float32)
          dapap[h]   = zeros([ny,nx], float32)
        
          for iy in range(0,96):
          #for iy in [50]:
          #for iy in range(iy0,iy0+4):
            #print h, iy
            #for ix in range(0, 144):
            for ix in [20]:
              #--------------------------------
              for var in ["ta", "hus", "pa"]:
                da1_6hr[var, h]  = da3_6hr[var, h][:,iy,ix]
          
              #----
              ps       = da2_6hr["ps", h][iy,ix]
              #----
              #a1plev     = da1_6hr["pa", h]
              #a1ta       = da1_6hr["ta", h]
              #a1hus      = da1_6hr["hus", h]
          
              a1plev     = cut_underground_p(ps, da1_6hr["pa", h], da1_6hr["pa", h])
              a1ta       = cut_underground_p(ps, da1_6hr["pa", h], da1_6hr["ta", h])
              a1hus      = cut_underground_p(ps, da1_6hr["pa", h], da1_6hr["hus", h])
          
          
              #----
              a1plev     = interp_fill(a1plev, nresol)
              a1ta       = interp_fill(a1ta,   nresol)
              a1hus      = interp_fill(a1hus,  nresol)
              #----
              lout = calcsound_fort_old.cape_1d(a1ta, a1plev, a1hus, Nparcels)
              dacapep[h][iy,ix]  = mean(lout[1])
              dapap[h][iy,ix]    = mean(lout[3])
        
              #if h ==0:
              #  awap[iy,ix]  = da3["wap"][3,iy,ix]
              print iy, mean(lout[1]),mean(lout[3])
        #---------------------
        acapep  = zeros([ny,nx], float32)
        apap    = zeros([ny,nx], float32)
        for h in lh:
          acapep = acapep + dacapep[h]
          apap   = apap  + dapap[h]
        #--
        acapep = acapep / len(lh)
        apap   = apap  / len(lh)
        #acapep.tofile(dname_day["capep"])
        #apap.tofile(dname_day["pap"])
        
        
        
