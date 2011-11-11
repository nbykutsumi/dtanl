from numpy import *
import os
import sys
################################################################
nx = 288
ny = 144
lvar = ["prectot", "ps", "qv10m", "t10m"]
nz = 1
#lvar = ["h", "omega"]
#nz = 25
#--------
iyear = 2001
eyear = 2002
im = 1
em = 12
tstp = "day"
xth  = 99
rmiss = -9999
################################################################
for var in lvar:
  idir = "/media/disk2/out/MERRA/%s/cnd.mean/%s/%04d-%04d/%02d-%02d"\
          %(tstp, var, iyear, eyear, im, em)
  siname = idir + "/%s.%s.%06.2f.bn"%(var, tstp, xth)
  #----
  if not os.access(siname, os.F_OK):
    print "no file:",siname
    sys.exit()
  #----
  idat = fromfile(siname, float32).reshape(nz,ny,nx)
  for iz in range(0,nz):
    for iy in range(0, ny):
      axs = ma.masked_equal(idat[iz,iy,:], rmiss)
      if (ma.count_masked(axs) == nx):
        ave = rmiss
      else:
        ave = mean(axs)
      #--
      idat[iz,iy,:] = ave
  #--------------------
  # output file
  #--------------------
  soname = idir + "/zmean.%s.%s.%06.2f.bn"%(var, tstp, xth) 
  idat.tofile(soname)
  print soname
      

  
