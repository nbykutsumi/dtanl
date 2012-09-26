from numpy import *
from cf import *
from ctrack_fsub import *

ny           = 96
nx           = 144

thpgrad      = 500.
dkm          = 100.0   # equal area grid resolution [km]
nradkmgrid   = 20

nx_kmgrid    = nradkmgrid*2 + 1
ny_kmgrid    = nradkmgrid*2 + 1
#-------------------------------------------
prdir_org    = "/media/disk2/data/CMIP5/bn/pr/day/NorESM1-M/historical/r1i1p1"
pgraddir_org = "/media/disk2/out/CMIP5/6hr/NorESM1-M/historical/r1i1p1/pgrad"

#prname       = prdir_org + "/1991" + "/pr_day_NorESM1-M_historical_r1i1p1_1991010100.bn"
#pgradname    = pgraddir_org + "/1991" + "/pgrad_6hr_NorESM1-M_historical_r1i1p1_1991010100.bn"

prname       = "/home/utsumi/bin/dtanl/ctrack/temp/pr.bn"
pgradname    = "/home/utsumi/bin/dtanl/ctrack/temp/pgrad.bn"

#-------------------------------------------
def readlatlon(fname):
  f = open(fname, "r")
  lines = f.readlines()
  f.close()
  lines = map(float, lines)
  return lines
#--------
def latlon2yx(lat, lon, lat_first, lon_first, dlat, dlon):
  iy    = int( (lat + 0.5*dlat - lat_first)/dlat )
  ix    = int( (lon + 0.5*dlon - lon_first)/dlon )
  return iy, ix
#-------------------------------------------
latname    = prdir_org + "/lat.txt"
lonname    = prdir_org + "/lon.txt"
a1latin    = readlatlon(latname)
a1lonin    = readlatlon(lonname)

latin_first  = a1latin[0]
lonin_first  = a1lonin[0]


a1latout   = arange(-89.95, 89.95, 0.25)
a1lonout   = arange(0.0, 359.95, 0.25)
latout_first = a1latout[0]
lonout_first = a1lonout[0]
dlatout      = a1latout[1] - a1latout[0]
dlonout      = a1lonout[1] - a1lonout[0]

#-------------------------------------------
a2pr_org   = fromfile(prname, float32).reshape(ny, nx)
a2pr_fin   = biIntp(a1latin, a1lonin, a2pr_org, a1latout, a1lonout)[0]
#--
a2pgrad    = fromfile(pgradname, float32).reshape(ny, nx)
#-- dummy---
a2sum      = zeros([ny_kmgrid, nx_kmgrid], float32)
a2num      = zeros([ny_kmgrid, nx_kmgrid], float32)
#-----------
for iy in range(0, ny):
  for ix in range(0, nx):
    if a2pgrad[iy, ix] >= thpgrad:
      print "iy, ix=", iy, ix
      lat   = a1latin[iy]
      lon   = a1lonin[ix]
      iy_fin, ix_fin  = latlon2yx(lat, lon, latout_first, lonout_first, dlatout, dlonout)
      #-- python type --> fortran type
      iy_fin_fort = iy_fin + 1
      ix_fin_fort = ix_fin + 1
      #-------------------------------
      a2sum_temp, a2num_temp = ctrack_fsub.eqgrid_aggr(a2pr_fin.T, a1latout, a1lonout, dkm, nradkmgrid, iy_fin_fort, ix_fin_fort)
      a2sum = a2sum + a2sum_temp 
      a2num = a2num + a2num_temp

a2sum, a2num = a2sum.T, a2num.T

#iy_fin, ix_fin = 292 ,585
#iy_fin  = 12
#ix_fin  = 12
#a2sum, a2num = ctrack_fsub.eqgrid_aggr(a2pr_fin.T, a1latout, a1lonout, dkm, nradkmgrid, iy_fin, ix_fin)
#a2sum, a2num = a2sum.T, a2num.T


