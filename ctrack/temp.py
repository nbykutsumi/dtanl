from numpy import *
from classtest import BoundaryNorm, BoundaryNormSymm
from matplotlib import colors
import matplotlib.pyplot as plt
from numpy import *
import matplotlib as mpl

a   =  arange(12).reshape(3,4)

bnd = [2,4,6,8]
b   = BoundaryNormSymm(bnd)
print "a=",a
print "b=",b(a)

plt.clf()
#plt.imshow(a,norm = b)
plt.imshow(a, interpolation='nearest', norm = b, cmap="RdBu")
plt.colorbar(boundaries=[-1.0e+20] + bnd + [1.0e+20], extend="both")
plt.show()
