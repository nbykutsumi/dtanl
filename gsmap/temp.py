from numpy import *
import gsmap_func
year = 2004
mon  = 4
day  = 3
hour = 0
a  =  gsmap_func.timeave_gsmap_backward_org(year,mon,day,hour, 1)
print a
