from ctrack_fsub import *
from numpy import *
import calendar
import os, sys
#--------------------------------------------------
tstp        = "6hr"
hinc        = 6
iyear       = 2002
eyear       = 2004
imon        = 1
emon        = 12
nx          = 360
ny          = 180
miss_dblout = -9999.0
thorog      = 1500.0     #[m]


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
psldir_root     = "/media/disk2/data/JRA25/sa.one/%s/PRMSL"%(tstp)
pslmeandir_root = "/media/disk2/data/JRA25/sa.one/my.mean/PRMSL"
pmeandir_root   = "/media/disk2/out/JRA25/sa.one/%s/pmean"%(tstp)
pgraddir_root   = "/media/disk2/out/JRA25/sa.one/%s/pgrad"%(tstp)
orogdir_root    = "/media/disk2/data/JRA25/sa.one/const/topo"
axisdir_root    = psldir_root

#****************************************************
# read lat, lon data
#----------------------
axisdir    = axisdir_root  + "/%04d%02d"%(iyear, imon)
latname    = axisdir  + "/lat.txt"
lonname    = axisdir  + "/lon.txt"
a1lat      = read_txtlist(latname)
a1lon      = read_txtlist(lonname)


#****************************************************
#  orog data
#--------------
orogdir  = orogdir_root
orogname = orogdir       + "/topo.sa.one"
a2orog   = fromfile(orogname, float32).reshape(ny, nx)
#**************************************************
# Mean Sea Level Pressure
#------------------------
pslmeanname = pslmeandir_root + "/fcst_phy2m.PRMSL.0000000000.sa.one"
a2pslmean = fromfile(pslmeanname, float32).reshape(ny, nx)
#------------------------
for year in range(iyear, eyear+1):
  #---------
  for mon in range(imon, emon+1):
    #---------
    # dirs
    #---------
    psldir   = psldir_root   + "/%04d%02d"%(year, mon)
    pmeandir = pmeandir_root + "/%04d%02d"%(year, mon)
    pgraddir = pgraddir_root + "/%04d%02d"%(year, mon)
    mk_dir(pmeandir)
    mk_dir(pgraddir)

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
        pslname   = psldir + "/fcst_phy2m.PRMSL.%s.sa.one"%(stimeh)
        check_file(pslname)
        pmeanname = pmeandir + "/pmean.%s.sa.one"%(stimeh)
        pgradname = pgraddir + "/pgrad.%s.sa.one"%(stimeh)

        #***************************************
        #***************************************
        # make pmean
        #***************************************
      
        a2psl   = fromfile(pslname,   float32).reshape(ny, nx)
        a2dpsl  = a2psl - a2pslmean
        a2dpsl   = ma.masked_where(a2orog > thorog , a2dpsl).filled(miss_dblout)
        findcyclone_out = array(ctrack_fsub.findcyclone(a2dpsl.T, a1lat, a1lon, -9999.0, miss_dblout), float32)
        #findcyclone_out = array(ctrack_fsub.findcyclone_old(apsl.T, a1lat, a1lon, -9999.0, miss_dblout), float32)
        a2pmean = findcyclone_out[0].T + a2pslmean
        a2pgrad = findcyclone_out[1].T
        a2pmean.tofile(pmeanname)
        a2pgrad.tofile(pgradname)

        print pgradname



 
