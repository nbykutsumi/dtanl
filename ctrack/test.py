from ctrack_fsub import *
from numpy import *
from cf import *
from cf import _gridsintr
#--------------------
ilat = [0, 1, 2, 3]
olat = [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
ilon = [10., 11., 12., 13.]
olon = [10.0, 10.5, 11.0, 11.5, 12.0, 12.5, 13.0]

ain  = arange(16).reshape(4,4)

aout = biIntp(ilat, ilon, ain, olat, olon)
print aout

