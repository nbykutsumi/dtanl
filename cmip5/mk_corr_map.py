from numpy import *
import calendar
import os
import sys
#################################################
nx = 288
ny = 144
nz = 25
#################################################
tstp  = "day"
iyear = 2001
eyear = 2008
imon = 1
emon = 12
xth = 99.0
model = "MERRA"
dP = 100.0 # [Pa], not [hPa]
rmiss = -9999.0
lscaletype=["swa","fromsurface"]
#------------------------------------------------
idir_root = "/media/disk2/data/%s/bn/%s"%(model,tstp)
dvname = {"pr":"prectot"}
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
def to_latlon(y,x, model):
  if model == "MERRA":
    lat0 = -179.375
    lon0 = -89.375
    dx = 1.25
    dy = 1.25
    #
    lat = lat0 + (y -1)*dy
    lon = lon0 + (x -1)*dx
    return [lat,lon]
  endif
#####################################################
for scaletype in lscaletype:
  #------
  # set sofiles
  #----------------------------------------------------
  odir_root = "/media/disk2/out/MERRA/day/scales/validate"
  odir = odir_root + "/%04d-%04d/%02d-%02d"%(iyear, eyear, imon, emon)
  #---
  mk_dir(odir)
  #---
  if scaletype == "swa":
    so_corr_re = odir + "/corr.p%s.%04d-%04d.%02d-%02d.bn"\
                          %(model, iyear, eyear, imon, emon)
    so_corr_gpcp = odir +"/corr.pGPCP.%04d-%04d.%02d-%02d.bn"\
                          %(iyear, eyear, imon, emon)
  elif scaletype == "fromsurface":
    so_corr_re = odir + "/corr.p%s.%04d-%04d.%02d-%02d.FS.bn"\
                          %(model, iyear, eyear, imon, emon)

    so_corr_gpcp = odir +"/corr.pGPCP.%04d-%04d.%02d-%02d.FS.bn"\
                          %(iyear, eyear, imon, emon)

  #----------------------------------------------------
  # set input file dir_root
  #----------------------------------------------------
  sp_re_dir_root= "/media/disk2/data/%s/bn/%s/%s"%(model, tstp, dvname["pr"])
  sgpcp_dir_root = "/media/disk2/data/GPCP1DD/data/merra1.25"
  #
  sswa_dir_root = "/media/disk2/out/%s/%s/scales/validate/swa.map"%(model, tstp)
  #----------------------------------------------------
  # make mean prec & mean swa
  #----------------------------------------------------
  dap_mean={}
  daswa_mean={}
  dn = {}
  #--
  dn["re"] = 0.0
  dap_mean["re"]   = zeros(nx*ny)
  daswa_mean["re"] = zeros(nx*ny)
  #--
  dn["gpcp"] = 0.0
  dap_mean["gpcp"]   = zeros(nx*ny)
  daswa_mean["gpcp"] = zeros(nx*ny)
  #=--------------------------------------
  for year in range(iyear, eyear+1):
    #--------
    sp_re_dir= sp_re_dir_root +"/%04d"%(year)
    sgpcp_dir= sgpcp_dir_root +"/%04d"%(year)
    #-
    sswa_dir = sswa_dir_root + "/%04d"%(year)
    #--------
    for mon in range(imon, emon+1):
      print year,mon
      for day in range(1, calendar.monthrange(year,mon)[1]+1):
        #*****************************************
        #***  with reanalysis precipitation ***
        #*****************************************
        # reanalysis prec
        #---------------------
        sp_re = sp_re_dir + \
               "/MERRA.day.prectot.%04d%02d%02d00.bn"%(year, mon, day)
        # 
        ap_re = fromfile(sp_re, float32)
        #
        dap_mean["re"] = dap_mean["re"] + ap_re
        #---------------------
        # swa
        #---------------------
        if scaletype == "swa":
          sswa = sswa_dir + "/%s.%s.swa.%04d.%02d.%02d.00.bn"%(model, tstp, year, mon, day)
        elif scaletype == "fromsurface":
          sswa = sswa_dir + "/%s.%s.swa.FS.%04d.%02d.%02d.00.bn"%(model, tstp, year, mon, day)
        #----
        aswa = fromfile(sswa, float32)
        daswa_mean["re"] = daswa_mean["re"] + aswa
        #---------------------
        dn["re"] = dn["re"] + 1
        #*****************************************
        #***  with GPCP1DD precipitation ***
        #*****************************************
        # reanalysis prec
        #---------------------
        sp_gpcp = sgpcp_dir + \
               "/gpcp_1dd_v1.1_p1d.Cx.%04d%02d%02d.bn"%(year, mon, day)
        # 
        ap_gpcp = fromfile(sp_gpcp, float32)
        #
        dap_mean["gpcp"] = dap_mean["gpcp"] + ap_gpcp
        #---------------------
        # swa
        #---------------------
        if scaletype == "swa":
          sswa = sswa_dir + "/%s.%s.swa.%04d.%02d.%02d.00.bn"%(model, tstp, year, mon, day)
        elif scaletype == "fromsurface":
          sswa = sswa_dir + "/%s.%s.swa.FS.%04d.%02d.%02d.00.bn"%(model, tstp, year, mon, day)
        #----
        aswa = fromfile(sswa, float32)
        daswa_mean["gpcp"] = daswa_mean["gpcp"] + aswa
        #---------------------
        dn["gpcp"] = dn["gpcp"] + 1
        #*****************************************
  #------
  dap_mean["re"] = dap_mean["re"] / dn["re"]
  daswa_mean["re"] = daswa_mean["re"] /dn["re"] 
  dap_mean["gpcp"] = dap_mean["gpcp"] / dn["gpcp"]
  daswa_mean["gpcp"] = daswa_mean["gpcp"] /dn["gpcp"] 
  
  #----------------------------------------------------
  # calc correlation coefficient
  #----------------------------------------------------
  dap =  {}
  daswa= {}
  dAB =  {}
  dA  =  {}
  dB  =  {}
  dap["re"]   = zeros(nx*ny)
  daswa["re"] = zeros(nx*ny)
  dAB["re"]   = zeros(nx*ny)
  dA["re"]    = zeros(nx*ny)
  dB["re"]    = zeros(nx*ny)
  
  dap["gpcp"]   = zeros(nx*ny)
  daswa["gpcp"] = zeros(nx*ny)
  dAB["gpcp"]   = zeros(nx*ny)
  dA["gpcp"]    = zeros(nx*ny)
  dB["gpcp"]    = zeros(nx*ny)
  #---
  
  for year in range(iyear, eyear+1):
    #--------
    sp_re_dir= sp_re_dir_root +"/%04d"%(year)
    sgpcp_dir= sgpcp_dir_root +"/%04d"%(year)
    #-
    sswa_dir = sswa_dir_root + "/%04d"%(year)
    #--------
    for mon in range(imon, emon+1):
      for day in range(1, calendar.monthrange(year,mon)[1]+1):
        #*********************************
        # with reanalysis prec
        #*********************************
        sp_re = sp_re_dir + \
               "/MERRA.day.prectot.%04d%02d%02d00.bn"%(year, mon, day)
        dap["re"]   = fromfile(sp_re, float32)
        #---------------------------
        # swa
        #---------------------------
        if scaletype == "swa":
          sswa = sswa_dir + "/%s.%s.swa.%04d.%02d.%02d.00.bn"%(model, tstp, year, mon, day)
        elif scaletype == "fromsurface":
          sswa = sswa_dir + "/%s.%s.swa.FS.%04d.%02d.%02d.00.bn"%(model, tstp, year, mon, day)
        #----------
        daswa["re"] = fromfile(sswa, float32)
        #---------------------------
        #calculation
        #---------------------------
        dAB["re"] = dAB["re"] + ( dap["re"] - dap_mean["re"]) * (daswa["re"] - daswa_mean["re"])
        #
        dA["re"]  = dA["re"] + (dap["re"] - dap_mean["re"])**2.0
        #
        dB["re"]  = dB["re"] + (daswa["re"] - daswa_mean["re"])**2.0
        #*********************************
        # with GPCP prec
        #********************************
        sp_gpcp = sgpcp_dir + \
               "/gpcp_1dd_v1.1_p1d.Cx.%04d%02d%02d.bn"%(year, mon, day)
        dap["gpcp"]   = fromfile(sp_gpcp, float32)
        #---------------------------
        # swa
        #---------------------------
        if scaletype == "swa":
          sswa = sswa_dir + "/%s.%s.swa.%04d.%02d.%02d.00.bn"%(model, tstp, year, mon, day)
        elif scaletype == "fromsurface":
          sswa = sswa_dir + "/%s.%s.swa.FS.%04d.%02d.%02d.00.bn"%(model, tstp, year, mon, day)
        #----------
        daswa["gpcp"] = fromfile(sswa, float32)
        #---------------------------
        #calculation
        #---------------------------
        dAB["gpcp"] = dAB["gpcp"] + ( dap["gpcp"] - dap_mean["gpcp"]) * (daswa["gpcp"] - daswa_mean["gpcp"])
        #
        dA["gpcp"]  = dA["gpcp"] + (dap["gpcp"] - dap_mean["gpcp"])**2.0
        #
        dB["gpcp"]  = dB["gpcp"] + (daswa["gpcp"] - daswa_mean["gpcp"])**2.0
  #******************************
  # write to file
  #******************************
  # with reanalysis
  #-------------------
  acorr = dAB["re"] / ( ( dA["re"]**0.5 )*(dB["re"]**0.5) )
  acorr = acorr.astype("float32")
  acorr.tofile(so_corr_re)
  #-------------------
  # with GPCP
  #-------------------
  acorr = dAB["gpcp"] / ( ( dA["gpcp"]**0.5 )*(dB["gpcp"]**0.5) )
  acorr = acorr.astype("float32")
  acorr.tofile(so_corr_gpcp)
  print so_corr_gpcp
