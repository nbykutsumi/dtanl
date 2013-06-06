import ctrack_para
import cf

miss      = -9999.0
#-- load lat & lon info ----
model     = "NorESM1-M"
listname  = "/media/disk2/data/CMIP5/meta/list.6hrPlev.sfc.csv"
f = open(listname,"r")
lines     = f.readlines()
f.close()
for line in lines:
  line  =  line.split(",")
  if model == line[0]:
    a1lat_out  = sort(array(map(float, line[5].split(" "))))
    a1lon_out  = sort(array(map(float, line[6].split(" "))))

#--- make lat & lon in finner resolution ---
#-- lon ---
ndiv_lon   = round(float(len(a1lon_org))/len(a1lon_out)) +1
a1dlon_out = (a1lon_out[1:] - a1lon_out[:-1])/(ndiv_lon*2.0)
#
a1lon_fin  = ones(ndiv_lon*len(a1lon_out))*(-9999.0)
for i in range(ndiv_lon):
  a1lon_fin[
#a1lon_fin[1:-2][::2] = a1lon_out[:-1] + a1dlon_out
#a1lon_fin[2:-1][::2] = a1lon_out[1:]  - a1dlon_out
#a1lon_fin[0]   = a1lon_out[0]  - (a1lon_out[0]  + 360.0 - a1lon_out[-1])/4.0
#a1lon_fin[1]   = a1lon_out[0]  + (a1lon_out[1]  - a1lon_out[0])/4.0
#a1lon_fin[-2]  = a1lon_out[-1] - (a1lon_out[-1] - a1lon_out[-2])/4.0
#a1lon_fin[-1]  = a1lon_out[-1] + (a1lon_out[0]  + 360.0 - a1lon_out[-1])/4.0
#
#
#a2org     = arange(180*360).reshape(180,360)
#a1lat_org = arange(-89.5, 89.5+0.001, 1.0)
#a1lon_org = arange(0.5, 359.5+0.001, 1.0)
#a1lat_fin = a1lat_org
#a2fin     = cf.biIntp( a1lat_org, a1lon_org, a2org, a1lat_fin, a1lon_fin, miss = miss)[0]

