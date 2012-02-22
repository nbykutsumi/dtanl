import os
#---------------------
cmd = "makecpt"
table = "polar"
#vmin = -10
#vmax = +10
#vinc = 2
#vmin = -100
#vmax = +100
#vinc = 20
#vmin  = -1
#vmax  = 1
#vinc  = 0.2
vmin  = -0.3
vmax  = 0.3
vinc  = 0.1
#
oname = "%s.%s.%s.cpt"%(table,vmin,vmax)
#---------------------
os.system("makecpt -C%s -I -T%s/%s/%s > %s"%(table, vmin, vmax, vinc, oname))
#------------------------
# usage
#------------------------
# -I : inverse
#------------------------
