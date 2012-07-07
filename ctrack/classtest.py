from matplotlib import colors
from numpy import *
class BoundaryNormSymm(colors.Normalize):
    '''
    referred to [Matplotlib-users]
    http://www.mail-archive.com/matplotlib-users@lists.sourceforge.net/msg03096.html
    posted by Eric
    based on BoundaryNorm (by Hyungjun Kim), modified by N. Utsumi
    '''
    def __init__(self,boundaries):
        self.vmin       = boundaries[0]
        self.vmax       = boundaries[-1]
        self.boundaries = boundaries
        self.N          = len(self.boundaries)

    def __call__(self,x,clip=False):
        x   = array(x)
        ret = zeros(x.shape,'int')
        for i, b in enumerate(self.boundaries):
            ret[greater_equal(x,b)]   = i+1

        ret[less(x,self.vmin)]  = 0
        return ma.masked_equal(ret,-1)/float(self.N)


class BoundaryNorm(colors.Normalize):
    '''
    referred to [Matplotlib-users]
    http://www.mail-archive.com/matplotlib-users@lists.sourceforge.net/msg03096.html
    posted by Eric
    '''
    def __init__(self,boundaries):
        self.vmin       = boundaries[0]
        self.vmax       = boundaries[-1]
        self.boundaries = boundaries
        self.N          = len(self.boundaries)

    def __call__(self,x,clip=False):
        x   = array(x)
        ret = zeros(x.shape,'int')
        for i, b in enumerate(self.boundaries):
            ret[greater_equal(x,b)]   = i

        ret[less(x,self.vmin)]  = -1
        return ma.masked_equal(ret,-1)/float(self.N-1)

