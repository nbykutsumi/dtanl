import commands
import calendar
import os
import sys
###########################################################
cmd   = "/home/utsumi/bin/dtanl/merra/dtanl_merra"
nx = 288
ny = 144
nz = 25
#####################################################
tstp = "day"
iyear = 2001
eyear = 2010
im = 1
em = 12
xth =99.0
#------------------------------------------------------
idir_root = "/media/disk2/out/MERRA/%s/cnd.mean"%(tstp)
lvar = ["h", "omega", "ps", "qv10m", "t10m"]
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
#################################################
def mk_dir_tail(var, tstp, model, expr, ens):
  odir_tail = var + "/" + tstp + "/" +model + "/" + expr +"/"\
       +ens
  return odir_tail
#####################################################
def mk_namehead(var, tstp, model, expr, ens):
  namehead = var + "_" + tstp + "_" +model + "_" + expr +"_"\
       +ens
  return namehead
#####################################################
# set sofiles
#---------------------------
#sodir_stm = "/media/disk2/out/MERRA/day/NorESM1-M/scales/r1i1p1"
sozonaldir = "/media/disk2/out/MERRA/%s/scales/zonal/%04d-%04d/%02d-%02d"%(tstp, iyear, eyear, im, em)
somapdir   = "/media/disk2/out/MERRA/%s/scales/map/%04d-%04d/%02d-%02d"%(tstp, iyear, eyear, im, em)
mk_dir(sozonaldir)
mk_dir(somapdir)
####
sofile1 = sozonaldir + "/scales.MERRA.%s.%06.2f.txt"%(tstp, xth)
sofile2 = sozonaldir + "/others.MERRA.%s.%06.2f.txt"%(tstp, xth)
sodPrec  = somapdir + "/dP.MERRA.%s.%06.2f.bn"%(tstp, xth)
soDdynam = somapdir + "/dP.dynam.MERRA.%s.%06.2f.bn"%(tstp, xth)
soDlapse = somapdir + "/dP.lapse.MERRA.%s.%06.2f.bn"%(tstp, xth)
soDhumid = somapdir + "/dP.humid.MERRA.%s.%06.2f.bn"%(tstp, xth)
soDps    = somapdir + "/dP.ps.MERRA.%s.%06.2f.bn"%(tstp, xth)
soDfull  = somapdir + "/dP.full.MERRA.%s.%06.2f.bn"%(tstp, xth)
soLCL_full = somapdir + "/dP.lcl_full.MERRA.%s.%06.2f.bn"%(tstp, xth)
#---------------------------
# set slev file
#---------------------------
slevdir = "/media/disk2/data/MERRA/bn/day/omega/%04d"\
          %(iyear)
slevfile = slevdir +"/lev.txt"
check_file(slevfile)
#---------------------------
smeanfile={}
sPrecfile={}
#---------------------------
# set Prec files
#---------------------------
dir_Prec = "/media/disk2/out/MERRA/%s/cnd.mean/prectot/%04d-%04d/%02d-%02d"\
            %(tstp, iyear, eyear, im, em)
sPrec_grid  = "prectot.%s.%06.2f.bn"%(tstp, xth)
sPrec_zmean = "zmean.prectot.%s.%06.2f.bn"%(tstp, xth)
sPrecfile["grid"]  = dir_Prec +"/%s"%(sPrec_grid)
sPrecfile["zmean"] = dir_Prec +"/%s"%(sPrec_zmean)
#
#---------------------------
for var in lvar:
  #----------------------------------------------------
  # make meanfile name
  #----------------------------------------------------
  dir_mean = "/media/disk2/out/MERRA/%s/cnd.mean/%s/%04d-%04d/%02d-%02d"\
              %(tstp, var, iyear, eyear, im, em)
  sname_grid ="%s.%s.%06.2f.bn" %(var,tstp, xth)
  sname_zmean="zmean.%s.%s.%06.2f.bn" %(var,tstp, xth)
  smeanfile[("grid",var)]  = dir_mean +"/%s"%(sname_grid)
  smeanfile[("zmean",var)] = dir_mean +"/%s"%(sname_zmean)
  #
  check_file(smeanfile[("grid",var)])
   
#----------------------------------------------------
os.system("%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s" \
          %(cmd \
          , smeanfile["zmean","t10m"] \
          , smeanfile["zmean","qv10m"]\
          , smeanfile["zmean","ps"]\
          , smeanfile["zmean","h"]\
          , smeanfile["zmean","omega"]\
          , sPrecfile["zmean"]\
          , smeanfile["grid","t10m"] \
          , smeanfile["grid","qv10m"]\
          , smeanfile["grid","ps"]\
          , smeanfile["grid","h"]\
          , smeanfile["grid","omega"]\
          , sPrecfile["grid"]\
          , slevfile\
          , sofile1\
          , sofile2\
          , sodPrec\
          , soDdynam\
          , soDlapse\
          , soDhumid\
          , soDps
          , soDfull\
          , soLCL_full\
          , nx\
          , ny\
          , nz) )
#----------------------------------------------------
# write dimension file
#----------------------------------------------------
dimname = somapdir + "/dim.txt"
sout_dim = "nx %s\n"%(nx) + "ny %s"%(ny)
f=open(dimname, "w")
f.write(sout_dim)
f.close()
