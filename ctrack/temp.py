import ctrack_func
lnextpos = [1,360,360*180]
miss = -9999
nx   = 360
for nextpos in lnextpos:
  x_next,y_next = ctrack_func.fortpos2pyxy(nextpos, nx, miss)
  print "nextpos",nextpos,"x", x_next, "y",y_next
