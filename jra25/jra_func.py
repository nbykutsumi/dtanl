from numpy import *
#-----------------------------
def mk_a1pyxy_from_anl_p():
  #*************************************
  slat_org=\
  "-89.142 -88.029 -86.911 -85.791 -84.670 -83.549 -82.428 -81.307 -80.185 -79.064\
   -77.943 -76.821 -75.700 -74.578 -73.457 -72.336 -71.214 -70.093 -68.971 -67.850\
   -66.728 -65.607 -64.485 -63.364 -62.242 -61.121 -60.000 -58.878 -57.757 -56.635\
   -55.514 -54.392 -53.271 -52.149 -51.028 -49.906 -48.785 -47.663 -46.542 -45.420\
   -44.299 -43.177 -42.056 -40.934 -39.813 -38.691 -37.570 -36.448 -35.327 -34.205\
   -33.084 -31.962 -30.841 -29.719 -28.598 -27.476 -26.355 -25.234 -24.112 -22.991\
   -21.869 -20.748 -19.626 -18.505 -17.383 -16.262 -15.140 -14.019 -12.897 -11.776\
   -10.654  -9.533  -8.411  -7.290  -6.168  -5.047  -3.925  -2.804  -1.682  -0.561\
     0.561   1.682   2.804   3.925   5.047   6.168   7.290   8.411   9.533  10.654\
    11.776  12.897  14.019  15.140  16.262  17.383  18.505  19.626  20.748  21.869\
    22.991  24.112  25.234  26.355  27.476  28.598  29.719  30.841  31.962  33.084\
    34.205  35.327  36.448  37.570  38.691  39.813  40.934  42.056  43.177  44.299\
    45.420  46.542  47.663  48.785  49.906  51.028  52.149  53.271  54.392  55.514\
    56.635  57.757  58.878  60.000  61.121  62.242  63.364  64.485  65.607  66.728\
    67.850  68.971  70.093  71.214  72.336  73.457  74.578  75.700  76.821  77.943\
    79.064  80.185  81.307  82.428  83.549  84.670  85.791  86.911  88.029  89.142"
  
  #*************************************
  def del_blank(l):
    #---------
    def func_tmp(s):
      return (s != "")
    #---------
    return filter(func_tmp, l)
  #*************************************
  ny_org, nx_org = 160, 320
  a1lat_org = map( float, del_blank( slat_org.split(" ") ))
  a1lon_org = linspace(0.0, 0.0+1.125*(320-1) ,320)
  lat_first_org = a1lat_org[0]
  lon_first_org = a1lon_org[0]
  
  ny, nx    = 180, 360
  a1lat     = linspace(-89.5, 89.5, 180)
  a1lon     = linspace(0.5,  359.5, 360)
  
  a1y_org    = ones(ny, int32)*-9999
  a1x_org    = ones(nx, int32)*-9999
  #---------------------------
  a1y_org[0]    = 0
  a1y_org[ny-1] = ny_org -1
  a1x_org[0]    = 0
  a1x_org[nx-1] = nx_org-1
  a1x_org[nx-2] = nx_org-1
  #---------------------------
  for iy in range(1,ny-1):
    lat  = a1lat[iy]
    for iy_org in range(1,ny_org-1):
      lat_org    = a1lat_org[iy_org]
      lat_org_lw = a1lat_org[iy_org-1]
      lat_org_up = a1lat_org[iy_org+1]
      bnd_lw     = (lat_org + lat_org_lw)*0.5
      bnd_up     = (lat_org + lat_org_up)*0.5
  
      if (bnd_lw <= lat < bnd_up):
        a1y_org[iy]  = iy_org
  
  #---------------------------
  for ix in range(1,nx-1):
    lon  = a1lon[ix]
    for ix_org in range(1,nx_org-1):
      lon_org    = a1lon_org[ix_org]
      lon_org_lw = a1lon_org[ix_org-1]
      lon_org_up = a1lon_org[ix_org+1]
      bnd_lw     = (lon_org + lon_org_lw)*0.5
      bnd_up     = (lon_org + lon_org_up)*0.5
  
      if (bnd_lw <= lon < bnd_up):
        a1x_org[ix]  = ix_org
  #----------------------------
  return a1x_org, a1y_org 


#-----------------------------
def del_miss(l, miss):
  #-----
  def f(x):
    if x != miss:
      return l
  #-----
  l = filter(f, l)
  return l
#-----------------------------

def read_llat(ctlname):
  f = open(ctlname, "r")
  lines = f.readlines()
  f.close()
  llats = []
  for i in range(len(lines)):
    line   = lines[i]
    s0     = line.split(" ")[0]
    if s0 == "ydef":
      i_first = i+1
      continue
    elif s0 == "tdef":
      i_last  = i-1
      break
  #--
  for line in lines[i_first:i_last+1]:
    ltemp = del_miss(line.split(" "), "")
    ltemp = map(float, ltemp)
    llats = llats + ltemp
  return llats

#def read_llat(ctlname, dattype):
#  f = open(ctlname, "r")
#  lines = f.readlines()
#  f.close()
#  llats = []
#  if dattype == "fcst_phy2m":
#    for i in range(len(lines)):
#      line   = lines[i]
#      s0     = line.split(" ")[0]
#      if s0 == "ydef":
#        i_first = i+1
#        continue
#      elif s0 == "tdef":
#        i_last  = i-1
#        break
#    #--
#    for line in lines[i_first:i_last+1]:
#      ltemp = del_miss(line.split(" "), "")
#      ltemp = map(float, ltemp)
#      llats = llats + ltemp
#    return llats
#  #---
#  if dattype == "anal_p25":
#    for i in range(len(lines)):
#      line   = lines[i]
#      s0     = line.split(" ")[0]
#      if s0 == "1000":
#        i_first = i
#        i_last  = i
#    #--
#    for line in lines[i_first:i_last+1]:
#      ltemp = del_miss(line.split(" "), "")
#      ltemp = map(float, ltemp)
#      llats = llats + ltemp
#    return llats

