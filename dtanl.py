from netCDF4 import *
from numpy import *
import pygrib
import calendar
import os
#########
IY,EY=1996,1998
IM,EM=6,8
WBIN=100  #[hPa]
intBIN_min=-30
intBIN_max=30
nBIN=61
res=0.5
nYp=361
nXp=720
fill_value=9.999e+20
#########
def MK_LM(IM,EM):
  if IM < EM:
    lm = range(IM,EM+1)
  else:
    lm = range(IM,12+1) + range(1,EM+1)

  return lm
###
IDIR="/media/disk2/out/dtanl/WcfsrPcfsr"
ODIR="/media/disk2/out/dtanl/WcfsrPcfsr/glob"
###
atimes=zeros(nYp*nXp*nBIN)
aSP=zeros(nYp*nXp*nBIN)
aSP2=zeros(nYp*nXp*nBIN)
###
idate="%04d-%04d-%02d-%02d"%(IY,EY,IM,EM)
stail="%sb-%s.nc"%(nBIN,res)
#####
# input file name
#####
iname_times= IDIR +"/wtim.%s-%s"%(idate,stail)
iname_pave= IDIR +"/pave.%s-%s"%(idate,stail)
iname_pstd= IDIR +"/pstd.%s-%s"%(idate,stail)
#####
# freq and omega_bin
f = Dataset(iname_times)
atimes = f.variables["dat"][:]
#####
# make times_sum
atimes_sum=sum(atimes, axis=0)
ltimes_sum=[]
for i in range(nBIN):
  ltimes_sum.append(atimes_sum)
atimes_sum= array(ltimes_sum)
#####
afreq  = (atimes / ma.masked_equal(atimes_sum, 0)).filled(0)
# omega_bin
abins = f.variables["omega_bin"]
f.close()
# pave
f = Dataset(iname_pave)
apave  = ma.masked_equal(f.variables["dat"][:], fill_value)  # Masked!!
f.close()
# pstd
f = Dataset(iname_pstd)
apstd  = f.variables["dat"][:]
f.close()
##########
# for large area
print apave
a1pave_all = array([ mean(a) for a in apave[:]])
a1freq_all= array([ mean(a) for a in afreq[:]])
#
aone=ones(nBIN* nYp* nXp).reshape(nBIN, nYp, nXp)

lpave_all=[]
lfreq_all=[]
#####
for i in range(nBIN):
  lpave_all.append( a1pave_all[i] * aone[i])
  lfreq_all.append( a1freq_all[i] * aone[i])
#####
apave_all   = ma.masked_invalid(array(lpave_all))  # Mask NaN
afreq_all= ma.masked_invalid(array(lfreq_all))
#####
adpave  = apave - apave_all
adfreq = afreq - afreq_all
#####
S1 = sum(adpave * afreq_all,  axis = 0).filled(fill_value)
S2 = sum(apave_all  * adfreq, axis = 0).filled(fill_value)
S3 = sum(adpave * adfreq, axis = 0).filled(fill_value)


#####
# names of output
#####
name_S1 = ODIR + "/thm.%s.%s.bin"%(idate,res)
name_S2 = ODIR + "/dyn.%s.%s.bin"%(idate,res)
name_S3 = ODIR + "/cov.%s.%s.bin"%(idate,res)
#####
# write
#####
S1.tofile(name_S1)
S2.tofile(name_S2)
S3.tofile(name_S3)
