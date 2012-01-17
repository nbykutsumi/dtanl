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
iyear = 2002
eyear = 2002
im = 1
em = 12
xth =99.0
model = "MERRA"
dP = 100.0 # [Pa], not [hPa]
rmiss = -9999.0
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
odir_root = "/media/disk2/out/MERRA/day/scales/validate/swa.map"

#---------------------------
# set slev file
#---------------------------
slevdir = "/media/disk2/data/%s/bn/day/omega/%04d"\
          %(model, iyear)
slevfile = slevdir +"/lev.txt"
check_file(slevfile)
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
#---------------------------
# set prxth files
#---------------------------
prxthdir = "/media/disk2/out/%s/%s/prxth/%04d-%04d/%02d-%02d"%(model, tstp, iyear, eyear, im, em)

sprec_lw = prxthdir + "/prxth.%s.%s.%06.2f.lw.bn"%(model, tstp, xth)
sprec_up = prxthdir + "/prxth.%s.%s.%06.2f.up.bn"%(model, tstp, xth)
#---------------------------

difile={}
davar ={}

sout_raw = ""
for year in range(iyear, eyear+1):
  #---------
  # make odir
  #---------
  odir = odir_root + "/%04d"%(year)
  mk_dir(odir)
  #---------
  for mon in range(im, em+1):
    for day in range(1, calendar.monthrange(year,mon)[1] +1):
      print year,mon,day
      #---------------------------
      #- files for variables 
      #---------------------------
      for var in lvar:
         difile[var] = idir_root + "/%s/%04d/%s.%s.%s.%04d%02d%02d00.bn"%(dvname[var], year, model, tstp, dvname[var], year, mon, day)
      ##--------------------------
      ## output file name , SWA
      ##--------------------------
      #soname = odir + "/%s.%s.swa.%04d.%02d.%02d.00.bn"%(model, tstp, year, mon, day)
      ##--------------------------
      #dtanl_p_swa.dtanl_p_swa.calc_swa_map(\
      #       "swa"                 \
      #     , slevfile              \
      #     , difile["Tsfc"]        \
      #     , difile["qsfc"]        \
      #     , difile["Psfc"]        \
      #     , difile["omega"]       \
      #     , soname                \
      #     , dP                    \
      #     , rmiss                 \
      #     , nx                    \
      #     , ny                    \
      #     , nz)
      #--------------------------
      # output file name , fromsurface
      #--------------------------
      soname_FS = odir + "/%s.%s.swa.FS.%04d.%02d.%02d.00.bn"%(model, tstp, year, mon, day)
      #--------------------------
      dtanl_p_swa.dtanl_p_swa.calc_swa_map(\
             "fromsurface"         \
           , slevfile              \
           , difile["Tsfc"]        \
           , difile["qsfc"]        \
           , difile["Psfc"]        \
           , difile["omega"]       \
           , soname_FS             \
           , dP                    \
           , rmiss                 \
           , nx                    \
           , ny                    \
           , nz)
