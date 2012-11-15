from ctrack_fsub import *
from numpy import *
import calendar
import os, sys
#--------------------------------------------------
if len(sys.argv) > 1:
  model       = sys.argv[1]
  expr        = sys.argv[2]
  ens         = sys.argv[3]
  tstp        = sys.argv[4]
  hinc        = int(sys.argv[5])
  iyear       = int(sys.argv[6])
  eyear       = int(sys.argv[7])
  imon        = int(sys.argv[8])
  emon        = int(sys.argv[9])
  nx          = int(sys.argv[10])
  ny          = int(sys.argv[11])
  miss_dblout = float(sys.argv[12])
  thorog      = float(sys.argv[13])

else:
  model       = "MIROC5"
  expr        = "historical"
  ens         = "r1i1p1"
  tstp        = "6hr"
  hinc        = 6
  iyear       = 1980
  eyear       = 2005
  imon        = 1
  emon        = 12
  nx          = 360
  ny          = 180
  miss_dblout = -9999.0
  thorog      = 1500.0     #[m]

print  model        #= "NorESM1-M"
print  expr         #= "historical"
print  ens          #= "r1i1p1"
print  tstp         #= "6hr"
print  hinc         #= 6
print  iyear        #= 1990
print  eyear        #= 1995
print  imon         #= 1
print  emon         #= 12
print  nx           #= 144
print  ny           #= 96
print  miss_dblout  #= -9999.0
print  thorog       #= 1500.0     #[m]


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
#****************************************************
def read_txtlist(iname):
  f = open(iname, "r")
  lines = f.readlines()
  f.close()
  lines = map(float, lines)
  aout  = array(lines, float32)
  return aout
#****************************************************
# dir_root
#---------------
psldir_root   = "/media/disk2/data/CMIP5/sa.one/psl/%s"%(tstp)
pmeandir_root = "/media/disk2/out/CMIP5/sa.one/%s"%(tstp)
pgraddir_root = "/media/disk2/out/CMIP5/sa.one/%s"%(tstp)
pgraddir_root = "/media/disk2/out/CMIP5/sa.one/%s"%(tstp)
orogdir_root  = "/media/disk2/data/CMIP5/sa.one/orog/fx"
axisdir_root  = psldir_root

#****************************************************
# read lat, lon data
#----------------------
axisdir    = axisdir_root  + "/%s/%s/%s"%(model, expr, ens)
latname    = axisdir  + "/lat.txt"
lonname    = axisdir  + "/lon.txt"
a1lat      = read_txtlist(latname)
a1lon      = read_txtlist(lonname)


#****************************************************
#  orog data
#--------------
orogdir  = orogdir_root  + "/%s/%s/r0i0p0"%(model, expr)
orogname = orogdir       + "/orog_fx_%s_%s_r0i0p0.sa.one"%(model, expr)
print orogname
print ny, nx
a2orog   = fromfile(orogname, float32).reshape(ny, nx)
#**************************************************
for year in range(iyear, eyear+1):
  #---------
  # dirs
  #---------
  psldir   = psldir_root   + "/%s/%s/%s/%04d"%(model,expr,ens, year)
  pmeandir = pmeandir_root + "/%s/%s/%s/pmean/%04d"%(model, expr, ens, year)
  pgraddir = pgraddir_root + "/%s/%s/%s/pgrad/%04d"%(model, expr, ens, year)
  mk_dir(pmeandir)
  mk_dir(pgraddir)
  print pmeandir
  #---------
  for mon in range(imon, emon+1):
    ##############
    # no leap
    ##############
    if (mon==2)&(calendar.isleap(year)):
      ed = calendar.monthrange(year,mon)[1] -1
    else:
      ed = calendar.monthrange(year,mon)[1]
    ##############
    for day in range(1, ed+1):
      for hour in range(0, 23+1, hinc):
        stimeh  = "%04d%02d%02d%02d"%(year,mon,day,hour)
        #***************************************
        #* names
        #---------------------------------------
        pslname   = psldir + "/psl_%sPlev_%s_%s_%s_%s.sa.one"%(tstp, model, expr, ens, stimeh)
        check_file(pslname)
        pmeanname = pmeandir + "/pmean_%s_%s_%s_%s_%s.sa.one"%(tstp, model, expr, ens, stimeh)
        pgradname = pgraddir + "/pgrad_%s_%s_%s_%s_%s.sa.one"%(tstp, model, expr, ens, stimeh)

        #***************************************
        #***************************************
        # make pmean
        #***************************************
      
        apsl   = fromfile(pslname,   float32).reshape(ny, nx)
        apsl   = ma.masked_where(a2orog > thorog , apsl).filled(miss_dblout)
        findcyclone_out = array(ctrack_fsub.findcyclone(apsl.T, a1lat, a1lon, -9999.0, miss_dblout), float32)
        apmean = findcyclone_out[0].T
        apgrad = findcyclone_out[1].T
        apmean.tofile(pmeanname)
        apgrad.tofile(pgradname)





 
