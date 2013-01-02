from numpy import *
import sys
regname = "ASAS"
nx    = 1300
ny    = 900
#nx     = 300
#ny     = 300
ydom_first = 54
ydom_last  = 834
xdom_first = 74
xdom_last  = 1228
#idir  = "."
idir  = "./test"
lonlatcsv = idir + "/lonlat_%s.csv"%(regname)
miss  = -9999.0
#*******************************************
# FUNCTIONS -------------
def ret_rotated(x,y,rcos, rsin):
  rx   = x*rcos - y*rsin
  ry   = x*rsin + y*rcos
  return [rx,ry]

#-------------------------
def inner_value(x0,y0, x1,y1,v1, x2,y2,v2, x3,y3,v3):
  L2   = ((x2-x1)**2.0 + (y2-y1)**2.0)**0.5
  rcos = (x2-x1)/L2
  rsin = (y2-y1)/L2
  rcos_inv = rcos
  rsin_inv = -rsin

  rx0,ry0 = ret_rotated(x0,y0, rcos_inv, rsin_inv)
  rx1,ry1 = ret_rotated(x1,y1, rcos_inv, rsin_inv)
  rx2,ry2 = ret_rotated(x2,y2, rcos_inv, rsin_inv)
  rx3,ry3 = ret_rotated(x3,y3, rcos_inv, rsin_inv)

  if (ry3-ry1 == 0.0):
    v0    = v1+ (v3-v1)*(rx0-rx1)/(rx3-rx1)
  else:
    beta    = (ry0-ry1)/(ry3-ry1)
    alpha   = (rx0-rx1- beta*(rx3-rx1))/L2
    v0      = v1 + alpha*(v2-v1) + beta*(v3-v1)
  #--
  return  v0
#-------------------------
def check_innerpoint(x0,y0, x1,y1, x2,y2, x3,y3):
  v2  = numpy.array((x2-x1, y2-y1))
  v3  = numpy.array((x3-x1, y3-y1))
  vv1 = numpy.array((x1-x0, y1-y0))
  vv2 = numpy.array((x2-x0, y2-y0))
  vv3 = numpy.array((x3-x0, y3-y0))
  N   = cross(v2,v3)
  N1  = cross(vv1,vv2)
  N2  = cross(vv2,vv3)
  N3  = cross(vv3,vv1)
  if dot(N,N1) < 0:
    return False
  elif dot(N,N2) <0:
    return False
  elif dot(N,N3) <0:
    return False
  else:
    return True

#-------------------------
def ret_triangle(llonlat, ix, iy):
  llonlatdist = []
  for line in llonlat:
    (x,y,lon,lat) = line
    dist          = (x-ix)**2.0 + (y-iy)**2.0
    llonlatdist.append(line+[dist])
  #--
  llonlatdist.sort(cmp = lambda x,y: cmp(x[4],y[4])) # sort by "dist"
  #-- find triangle
  (x1, y1, lon1, lat1, dist1) = llonlatdist[0]
  (x2, y2, lon2, lat2, dist2) = llonlatdist[1]
  
  innerflag = False
  for line in llonlatdist[2:]:
    (x3,y3,lon3,lat3, dist3)  = line
    if check_innerpoint(ix,iy, x1,y1, x2,y2, x3,y3):
      innerflag = True
      break     
  #----
  if innerflag == False:
    x1,x2,x3 = miss, miss, miss
    y1,y2,y3 = miss, miss, miss 
  #----
  return [[x1,y1,lon1,lat1],[x2,y2,lon2,lat2],[x3,y3,lon3,lat3]]

#*******************************************
#-- read lonlat csv -------
f = open(lonlatcsv)
lines = f.readlines()
f.close()
llonlat  = []
for line in lines[1:]:
  line = map(float, line.strip().split(",") )
  if line[0] ==1:
    llonlat.append(line[1:])
#--------------------------
a2lon  = ones([ny,nx],float32)*miss
a2lat  = ones([ny,nx],float32)*miss

for iy in range(ydom_first,ydom_last+1):
  print "iy=",iy
  for ix in range(xdom_first, xdom_last+1):
    #-----
    ll = ret_triangle(llonlat, ix, iy)
    [[x1,y1,lon1,lat1],[x2,y2,lon2,lat2],[x3,y3,lon3,lat3]] = ll
    if x1 == miss:
      lon0 = miss
      lat0 = miss
    else:
      lon0 = inner_value(ix,iy, x1,y1,lon1, x2,y2,lon2, x3,y3,lon3)
      lat0 = inner_value(ix,iy, x1,y1,lat1, x2,y2,lat2, x3,y3,lat3)
    #-----
    a2lon[iy-1,ix-1] = lon0
    a2lat[iy-1,ix-1] = lat0









 
