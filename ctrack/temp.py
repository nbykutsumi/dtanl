from numpy import *
from ctrack_fsub import *

ny,nx  = 180,360
ny_bn, nx_bn = 145,192
miss   = -9999.0
idir   = "/media/disk2/data/CMIP5/sa.one.HadGEM2-ES.historical/psl/198001"
iname  = idir + "/psl.r2i1p1.198001151800.sa.one"
a2in   = fromfile(iname, float32).reshape(ny,nx)

a2out1  = ctrack_fsub.find_localminima_varres(a2in.T, miss, miss).T


bndir  = "/media/disk2/data/CMIP5/bn.HadGEM2-ES.historical/psl/198001"
bnname  = bndir + "/psl.r2i1p1.198001151800.bn"
a2bn   = fromfile(bnname, float32).reshape(ny_bn, nx_bn)
a2out2 = ctrack_fsub.find_localminima_varres(a2bn.T, miss, miss).T

