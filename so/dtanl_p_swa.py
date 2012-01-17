from numpy import *
import calendar
import os
import sys
import dtanl_p_swa
###########################################################
nx = 288
ny = 144
nz = 25
#####################################################
tstp = "day"
iyear = 2001
eyear = 2001
im = 1
em = 2
xth =99.0
model = "MERRA"
ptype = "GPCP"
dP = 100.0 # [Pa], not [hPa]
#------------------------------------------------------
idir_root = "/media/disk2/data/%s/bn/%s"%(model,tstp)

lvar = ["Tsfc", "qsfc", "Psfc", "omega"]
dvname = {"Tsfc": "t10m", "qsfc": "qv10m", "Psfc":"ps", "omega":"omega", "pr":"prectot"}
l2dvar = ["Psfc", "qsfc", "Tsfc"]
l3dvar = ["omega"]
#####################################################
# functions
#####################################################
def check_file(sname):
  if not os.access(sname, os.F_OK):
    print "no file:",sname
    sys.exit()
#####################################################
def mk_dir(sdir):
  try:
    os.makedirs(sdir)
  except:
    pass
#####################################################
def read2list(sfile):
  f=open(sfile, "r")
  line = f.readlines()
  f.close()
  line = map(float, line)
  return line
#####################################################
# set sofiles
#---------------------------
#sodir_stm = "/media/disk2/out/MERRA/day/NorESM1-M/scales/r1i1p1"

#---------------------------
# set slev file
#---------------------------
slevdir = "/media/disk2/data/%s/bn/day/omega/%04d"\
          %(model, iyear)
slevfile = slevdir +"/lev.txt"
check_file(slevfile)
f = open(slevfile, "r")
line = f.readlines()
f.close()
a1lev = ma.array(map(float, line))
#----
# convert from [hPa] --> [Pa]
#----
a1lev = 100.0 * a1lev
#---------------------------
smeanfile={}
sPrecfile={}
#---------------------------
# set lat & lon files
#---------------------------
slatfile = idir_root + "/%s/%04d/lat.txt"%(dvname["pr"], iyear)
slonfile = idir_root + "/%s/%04d/lon.txt"%(dvname["pr"], iyear)
llat = read2list(slatfile)
llon = read2list(slonfile)
##---------------------------
## set prxth files
##---------------------------
#prxthdir = "/media/disk2/out/%s/%s/prxth/%04d-%04d/%02d-%02d"%(model, tstp, iyear, eyear, im, em)
#
#sprec_lw = prxthdir + "/prxth.%s.%s.%06.2f.lw.bn"%(model, tstp, xth)
#sprec_up = prxthdir + "/prxth.%s.%s.%06.2f.up.bn"%(model, tstp, xth)
#aprec_lw = fromfile(sprec_lw, float32).reshape(ny,nx)
#aprec_up = fromfile(sprec_up, float32).reshape(ny,nx)
#---------------------------
difile={}
davar ={}

sout_raw = ""
for year in range(iyear, eyear+1):
  #if year != 2001:
  #  continue
  for mon in range(im, em+1):
    #if mon != 1:
    #  continue
    for day in range(1, calendar.monthrange(year,mon)[1] +1):
      #if day > 3:
      #  continue
      print year,mon,day
      #***************************
      # set prec files
      #***************************
      # with reanalysis
      #---------------------------
      if ptype == "MERRA":
        sprec = idir_root + "/%s/%04d/%s.%s.%s.%04d%02d%02d00.bn"\
               %(dvname["pr"], year, model, tstp, dvname["pr"], year, mon, day)
      #***************************
      # with GPCP
      #---------------------------
      if ptype == "GPCP":
        precdir = "/media/disk2/data/GPCP1DD/data/merra1.25/%04d"%(year)
        sprec = precdir + "/gpcp_1dd_v1.1_p1d.Cx.%04d%02d%02d.bn"%(year, mon, day)
      #***************************
      aprec = fromfile(sprec, float32).reshape(ny,nx)
      #---------------------------
      #- files for variables 
      #---------------------------
      for var in lvar:
         difile[var] = idir_root + "/%s/%04d/%s.%s.%s.%04d%02d%02d00.bn"%(dvname[var], year, model, tstp, dvname[var], year, mon, day)
         #--
         if var in l2dvar:
           davar[var] = fromfile(difile[var], float32).reshape(ny,nx)
         elif var in l3dvar:
           davar[var] = fromfile(difile[var], float32).reshape(nz, ny,nx)
      #--------------------------
      for iy in range(0,ny):
        lat  = llat[iy]
        if not ( ( -15.0 <lat ) & (lat <15.0)):
          continue
        for ix in range(0,nx):
          lon  = llon[ix]
          if not ( (-90.0 < lon)&(lon < 30.0)  ):
            continue
          #----------------------------
          # filter with precipitation threshold
          #----------------------------
          prec = aprec[iy,ix]
          #if (prec < aprec_lw[iy,ix]) or (aprec_up[iy,ix] <= prec)  :
          #  continue 
          #----------------------------
          Tsfc = davar["Tsfc"][iy,ix]
          qsfc = davar["qsfc"][iy,ix]
          Psfc = davar["Psfc"][iy,ix]
          #
          a1omega = davar["omega"][:,iy,ix]
          #
          #print "nz",nz
          #print "dP",dP
          #print "a1lev",a1lev
          #print "Tsfc", Tsfc
          #print "Psfc", Psfc
          #print "qsfc", qsfc
          #print "a1omega",a1omega
          SWA = dtanl_p_swa.dtanl_p_swa.calc_swa(dP, a1lev, Tsfc, qsfc, Psfc, a1omega)
          sout_raw = sout_raw + "%04d,%02d,%02d,%s,%s,%s,%s\n"%(year, mon, day, lat, lon, SWA, prec)
#-----------------------------------------------------
# write to file
#-----------------------------------------------------
odir = "/media/disk2/out/%s/%s/scales/validate/%04d-%04d/%02d-%02d"%(model, tstp, iyear, eyear, im, em)
#
mk_dir(odir)
#
sraw_list = odir + "/%s.rawlist.p%s.%04d-%04d.%02d-%02d.csv"%(model,ptype, iyear, eyear, im, em)
f=open(sraw_list, "w")
f.write(sout_raw)
f.close()
print sraw_list
