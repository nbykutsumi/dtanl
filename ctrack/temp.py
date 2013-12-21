from numpy import *
from ctrack_fsub import *

ny,nx  = 180,360
#ny_bn, nx_bn = 145,192
miss   = -9999.0

#---------------------
bndir_root = "/media/disk2/data/CMIP5/bn.HadGEM2-ES.historical/psl"
latname = bndir_root + "/lat.txt"
lonname = bndir_root + "/lon.txt"
dimname = bndir_root + "/dims.txt"
f=open(latname);lines= f.readlines(); f.close()
a1lat_bn = map(float, lines)

f=open(lonname);lines=f.readlines(); f.close()
a1lon_bn = map(float, lines)

f=open(dimname);lines=f.readlines(); f.close()
ny_bn = int(lines[1].split(" ")[1])
nx_bn = int(lines[2].split(" ")[1])
#---------------------
# local minima from bn
bndir  = "/media/disk2/data/CMIP5/bn.HadGEM2-ES.historical/psl/198001"
bnname  = bndir + "/psl.r2i1p1.198001151800.bn"
a2bn   = fromfile(bnname, float32).reshape(ny_bn, nx_bn)
a2out1 = ctrack_fsub.find_localminima_varres(a2bn.T, miss, miss).T
#---------------------

# bn --> one
a2out2 = ctrack_fsub.find_potcyclone_frombn(a2bn.T, a1lat_bn, a1lon_bn, miss, miss).T

#---------------------
# local minima from one
idir   = "/media/disk2/data/CMIP5/sa.one.HadGEM2-ES.historical/psl/198001"
pslname  = idir + "/psl.r2i1p1.198001151800.sa.one"
a2psl   = fromfile(pslname, float32).reshape(ny,nx)

a2out3  = ctrack_fsub.find_localminima_varres(a2psl.T, miss, miss).T
#----------------------
a1lat_one = arange(180) - 89.5
a1lon_one = arange(360) + 0.5
a2out4  = ctrack_fsub.mk_grad_cyclone_saone(a2out2.T, a2psl.T, a1lat_one, a1lon_one, miss, miss).T

