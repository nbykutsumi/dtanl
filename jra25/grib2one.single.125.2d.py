from numpy import *
import calendar
import subprocess
import os
import matplotlib.pyplot as plt
import cf
import sys

gribname = sys.argv[1]
ctlname  = sys.argv[2]
odir     = sys.argv[3]
if odir[-1] == "/":odir = odir[:-1]

idir     = "/".join(gribname.split("/")[:-1])
#--- LAT & LON & NX, NY : Original  ------------------------------
dlon_org      = 1.25
dlat_org      = 1.25

lat_first_org = -90.0
lat_last_org  = 90.0
lon_first_org = 0.0
lon_last_org  = 358.75
a1lat_org     = arange(lat_first_org, lat_last_org + dlat_org*0.1, dlat_org)
a1lon_org     = arange(lon_first_org, lon_last_org + dlon_org*0.1, dlon_org)
#--------------------------

ny_org     = len(a1lat_org)
nx_org     = len(a1lon_org)

print ny_org, nx_org
#-- modify a1lat_rog for interpolation at polar region --
a1lat_org[0]  = -90.0
a1lon_org[-1] = 90.0


#--- LAT & LON & NX, NY : After Interpolation  ------------------
dlat_fin   = 1.0
dlon_fin   = 1.0
a1lat_fin  = arange(-90.0+dlat_fin*0.5, 90.0 - dlat_fin*0.5 + dlat_fin*0.1, dlat_fin)
a1lon_fin  = arange(0.0+dlon_fin*0.5, 360.0 - dlon_fin*0.5 + dlon_fin*0.1, dlon_fin)

ny_fin     = len(a1lat_fin)
nx_fin     = len(a1lon_fin)
nz_fin     = 1
#********************************************
def mk_dir(sdir):
  if not os.access(sdir , os.F_OK):
    os.mkdir(sdir)
#********************************************
#-- discription file ----------------
#< dims >
sout   = "lev %d\nlat %d\nlon %d"%(nz_fin, ny_fin, nx_fin)
f      = open( odir + "/dims.txt", "w")
f.write(sout)
f.close()

#< lat >
sout   = "\n".join(map( str, a1lat_fin))
f      = open( odir + "/lat.txt", "w")
f.write(sout)
f.close()

#< lon >
sout   = "\n".join(map( str, a1lon_fin))
f      = open( odir + "/lon.txt", "w")
f.write(sout)
f.close()

#< dump >
dumpname = odir + "/dump.txt"
print dumpname
ptemp  = subprocess.call("wgrib -V %s > %s"%(gribname, dumpname), shell=True)
  
#-----------------
#----- Names ------------
oname_tail = gribname.split("/")[-1]
oname_tail = ".".join(oname_tail.split(".")[:-1])

tempname   = odir + "/%s.temp.sa.one"%(oname_tail)
oname      = odir + "/%s.sa.one"%(oname_tail)

#-- grib --> binary -----

args      = "wgrib %s | wgrib %s -i -nh -o %s"%(gribname, gribname, tempname)
#args      = "wgrib %s -nh -o %s"%(gribname, tempname)
ptemp     = subprocess.call(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#-- Interpolation and Flipud --------
a2org     = flipud(fromfile(tempname, float32).reshape(ny_org, nx_org))
a2fin     = cf.biIntp( a1lat_org, a1lon_org, a2org, a1lat_fin, a1lon_fin,)
a2fin.tofile( oname ) 
print oname

#-- delete temp file ----------------
os.remove(tempname)
#------------------------------------




