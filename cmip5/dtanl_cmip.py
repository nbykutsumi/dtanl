import commands
import calendar
import os
import sys
###########################################################
cmd   = "/home/utsumi/bin/dtanl/cmip5/dtanl_cmip"
nx = 144
ny = 96
nz = 8
#####################################################
tstp = "day"
model = "NorESM1-M"
dexpr ={}
dexpr["his"] = "historical" #historical, rcp85
dexpr["fut"] = "rcp85" #historical, rcp85
ens  = "r1i1p1"
dyrange={}
dyrange["his"] = [1990,1999]
dyrange["fut"] = [2086,2095]
im = 1
em = 12
xth =99.0
#------------------------------------------------------
idir_root = "/media/disk2/data/CMIP5/bn"
odir_root = idir_root
cmd = "/home/utsumi/bin/dtanl/cmip5/dtanl_cmip"
lvar = ["tas", "huss", "rhs","psl", "zg", "wap","prc"]
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
#sodir_stm = "/media/disk2/out/CMIP5/day/NorESM1-M/scales/r1i1p1"
sozonaldir = "/media/disk2/out/CMIP5/%s/%s/scales/%s/zonal"%(tstp, model, ens)
somapdir   = "/media/disk2/out/CMIP5/%s/%s/scales/%s/map"%(tstp, model, ens)
mk_dir(sozonaldir)
mk_dir(somapdir)
####
sofile1 = sozonaldir + "/scales.%s_%s_%s_%06.2f.csv"%(tstp, model, ens, xth)
sofile2 = sozonaldir + "/others.%s_%s_%s_%06.2f.csv"%(tstp, model, ens, xth)
sodPrec  = somapdir + "/dP.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
soDdynam = somapdir + "/dP.dynam.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
soDlapse = somapdir + "/dP.lapse.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
soDhumid = somapdir + "/dP.humid.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
soDfull  = somapdir + "/dP.full.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
soLCL_full = somapdir + "/dP.lcl_full.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
sonan   = somapdir + "/nan.%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
soFracChngLCL = somapdir + "/frac.chng.LCL_%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
soFracChngRH = somapdir + "/frac.chng.RH_%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
soChngRH = somapdir + "/chng.RH_%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
soChngPsfc   = somapdir + "/chng.psfc_%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
soFracChngPsfc = somapdir + "/frac.chng.psfc_%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
soPsfc1 = somapdir + "/psfc1_%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
soPsfc2 = somapdir + "/psfc2_%s_%s_%s_%06.2f.bn"%(tstp, model, ens, xth)
#---------------------------
# set szgfile
#---------------------------
szgfile={}
szgdir="/media/disk2/data/CMIP5/bn/orog/fx/%s"%(model)
szgfile["his"]= szgdir + "/%s/r0i0p0/orog_fx_%s_%s_r0i0p0.bn"\
                %(dexpr["his"], model, dexpr["his"])
szgfile["fut"]= szgdir + "/%s/r0i0p0/orog_fx_%s_%s_r0i0p0.bn"\
                %(dexpr["fut"], model, dexpr["fut"])
check_file(szgfile["his"])
check_file(szgfile["fut"])
#---------------------------
# set slev file
#---------------------------
#slevdir = "/media/disk2/data/CMIP5/bn/zg/day/NorESM1-M/historical/r1i1p1"\
slevdir = "/media/disk2/data/CMIP5/bn/zg/day/%s/historical/%s"\
          %(model, ens)
slevfile = slevdir +"/lev.txt"
check_file(slevfile)
#---------------------------
smeanfile={}
sPrecfile={}
#---------------------------
for era in ["his", "fut"]: 
  expr = dexpr[era]
  iy = dyrange[era][0]
  ey = dyrange[era][1]

  #---------------------------
  # set Prec files
  #---------------------------
  dir_Prec = "/media/disk2/out/CMIP5/%s/%s/%s/%s/prxth/%04d-%04d/%02d-%02d"\
              %(tstp, model, expr, ens, iy, ey, im, em)
  sname_Prec= "prxth_%s_%s_%s_%s_%06.2f.bn"%(tstp, model, expr, ens, xth)
  #dir_Prec = "/media/disk2/out/CMIP5/%s/%s/%s/%s/cnd.mean/pr/%04d-%04d/%02d-%02d"%(tstp, model, expr, ens, iy, ey, im, em)
  #sname_Prec = "pr_%s_%s_%s_%s_%06.2f.bn"%(tstp, model, expr, ens, xth)
  #
  sPrecfile[(era)] = dir_Prec +"/%s"%(sname_Prec)

  #
  check_file(sPrecfile[(era)])

  #---------------------------
  for var in lvar:
    #----------------------------------------------------
    # make meanfile name
    #----------------------------------------------------
    dir_mean = "/media/disk2/out/CMIP5/%s/%s/%s/%s/cnd.mean/%s/%04d-%04d/%02d-%02d"\
                %(tstp, model, expr, ens, var, iy, ey, im, em)
    sname_mean= "%s_%s_%s_%s_%s_%06.2f.bn"%(var, tstp, model, expr
  , ens, xth)
    smeanfile[(era,var)] = dir_mean +"/%s"%(sname_mean)
    #
    check_file(smeanfile[(era,var)])

   
#----------------------------------------------------
os.system("%s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s" \
          %(cmd \
          , smeanfile["his","prc"] \
          , smeanfile["his","tas"] \
          , smeanfile["his","huss"]\
          , smeanfile["his","rhs"]\
          , smeanfile["his","psl"]\
          , smeanfile["his","zg"]\
          , smeanfile["his","wap"]\
          , szgfile["his"]\
          , sPrecfile["his"]\
          , smeanfile["fut","prc"] \
          , smeanfile["fut","tas"] \
          , smeanfile["fut","huss"]\
          , smeanfile["fut","rhs"]\
          , smeanfile["fut","psl"]\
          , smeanfile["fut","zg"]\
          , smeanfile["fut","wap"]\
          , szgfile["fut"]\
          , sPrecfile["fut"]\
          , slevfile\
          , sofile1\
          , sofile2\
          , sodPrec\
          , soDdynam\
          , soDlapse\
          , soDhumid\
          , soDfull\
          , soLCL_full\
          , sonan\
          , soFracChngLCL\
          , soFracChngRH\
          , soFracChngPsfc\
          , soChngRH\
          , soChngPsfc\
          , soPsfc1\
          , soPsfc2\
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
