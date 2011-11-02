from netCDF4 import *
from numpy import *
import pygrib
import calendar
import os
########
IY,EY=1996,1998
IM,EM=6,8
IDIR="/media/disk2/out/dtanl/WcfsrPcfsr"
ODIR="/media/disk2/out/dtanl/WcfsrPcfsr"
WBIN=100  #[hPa]
intBIN_min=-30
intBIN_max=30
nBIN=61
res=0.5
nYp=361
nXp=720
fill_value=9.999e+20
########
def  write_netCDF(adata,oname,datunits):
  #open output file
  fout=Dataset(oname, "w", format="NETCDF4")
  ## dimensions
  fout.createDimension("latitude",361)
  fout.createDimension("longitude",720)
  fout.createDimension("omega_bin",nBIN)
  ## variables
  latitudes=fout.createVariable("latitude","f4",("latitude",))
  longitudes=fout.createVariable("longitude","f4",("longitude",))
  omega_bins=fout.createVariable("omega_bin","f4",("omega_bin",))
  dats=fout.createVariable(\
      "dat","f4",("omega_bin","latitude","longitude",)\
      #,fill_value=9.999e+20\
      )
  ## units
  latitudes.units="degrees_north"
  longitudes.units="degrees_east"
  omega_bins.units="-hPa/day"
  dats.units="%s"%(datunits)
  ## FillValue
  #latitudes._FillValue=fill_value
  #longitudes._FillValue=fill_value
  #omega_bins._FillValue=fill_value
  #dats._FillValue=fill_value
  ## make data
  alat=arange(-90,90+0.1,0.5)
  alon=arange(0,359.5+0.1, 0.5)
  abin=range(intBIN_min*WBIN, intBIN_max*WBIN +1, WBIN)
  ## put data
  latitudes[:]=alat
  longitudes[:]=alon
  omega_bins[:]=abin
  dats[:]=adata
  ## close output file
  fout.close()
####
def MK_LM(IM,EM):
  if IM < EM:
    lm = range(IM,EM+1)
  else:
    lm = range(IM,12+1) + range(1,EM+1)

  return lm
####
def MK_LYS(IY,EY,M):
  lYS=[]
  Y1 = IY
  while Y1 <= EY:
    for Y2 in range(Y1,EY+1):
      YS = "%04d-%04d"%(Y1,Y2)
      iname_Pave=  IDIR +"/%s.%s-%02d-%s"%("pstd",YS,M,name_tail)
      if os.access(iname_Pave, os.F_OK):
        lYS.append(YS)
        Y1=Y2+1  # set next Y1
        break
      elif Y2==EY:
        print "no file."
        print "Y1=", Y1
        print "Y2=", Y2
        sys.exit()
    #####
    Y1=Y1+1
  if len(lYS)==0:
    print "no file such as",iname_Pave
  return lYS
########
name_tail="%sb-%s.nc"%(nBIN,res)
########
lM=MK_LM(IM,EM)
atimes = zeros(nYp*nXp*nBIN).reshape(nBIN, nYp, nXp)
apave = zeros(nYp*nXp*nBIN).reshape(nBIN, nYp, nXp)
apacc = zeros(nYp*nXp*nBIN).reshape(nBIN, nYp, nXp)
apac2 = zeros(nYp*nXp*nBIN).reshape(nBIN, nYp, nXp)

for M in lM:
  lYS = MK_LYS(IY,EY,M)
  for YS in lYS:
    iname_times= IDIR + "/%s.%s-%02d-%s"%("wtim", YS, M, name_tail)
    iname_pave= IDIR + "/%s.%s-%02d-%s"%("pave", YS, M, name_tail)
    iname_pacc= IDIR + "/%s.%s-%02d-%s"%("pacc", YS, M, name_tail)
    iname_pac2= IDIR + "/%s.%s-%02d-%s"%("pac2", YS, M, name_tail)
    iname_pstd= IDIR + "/%s.%s-%02d-%s"%("pstd", YS, M, name_tail)
    ########
    # times
    f = Dataset(iname_times, "r")
    atimes_i = f.variables["dat"][:].reshape(nBIN, nYp, nXp)
    f.close()
    atimes   = atimes + atimes_i
    ## pave
    #f = Dataset(iname_pave, "r")
    #apave_i = f.variables["dat"][:].reshape(nBIN, nYp, nXp)
    #apave_i = ma.masked_equal(apave_i, fill_value)     # Mask !!
    #f.close()
    #apave   = apave + apave* atimes_i 
    ########
    # pacc
    f = Dataset(iname_pacc, "r")
    apacc = apacc + f.variables["dat"][:].reshape(nBIN, nYp, nXp)
    f.close()
    ########
    # pac2
    f = Dataset(iname_pac2, "r")
    apac2 = apac2 + f.variables["dat"][:].reshape(nBIN, nYp, nXp)
    f.close()
    #######
#####
# calc apave
#apave = apave / ma.masked_equal(atimes,0)
#apave = apave.filled(fill_value)
atimes_masked = ma.masked_equal(atimes,0)
apave = apacc / atimes_masked
apave = apave.filled(fill_value)

# calc std
apstd = sqrt( apac2 - 2* apave* apacc + atimes_masked* apave**2   \
           / atimes_masked )
apstd = apstd.filled(fill_value)
#####
# names of output files
#####
OYS = "%04d-%04d"%(IY,EY)
oname_times= ODIR +"/%s.%s-%02d-%02d-%s"%("wtim", OYS, IM,EM, name_tail)
oname_pave= ODIR + "/%s.%s-%02d-%02d-%s"%("pave", OYS, IM,EM, name_tail)
oname_pacc= ODIR + "/%s.%s-%02d-%02d-%s"%("pacc", OYS, IM,EM, name_tail)
oname_pac2= ODIR + "/%s.%s-%02d-%02d-%s"%("pac2", OYS, IM,EM, name_tail)
oname_pstd= ODIR + "/%s.%s-%02d-%02d-%s"%("pstd", OYS, IM,EM, name_tail)
#####
# write file
#####
write_netCDF(atimes,oname_times,"days")
write_netCDF(apave, oname_pave, "mm/day")
write_netCDF(apacc, oname_pacc, "mm/day")
write_netCDF(apac2, oname_pac2, "(mm/day)**2")
write_netCDF(apstd, oname_pstd, "mm/day")
