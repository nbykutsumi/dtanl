import os, sys
from numpy import *
import scipy.stats


tv, pv = scipy.stats.ttest_ind(a,b, equal_var=False)
