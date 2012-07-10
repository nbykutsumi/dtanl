from ctrack_fsub import *
import ctrack_para
from numpy import *
import calendar
import os
#--------------------------------------------------
thorog  = 1000.0 #[m]
thdp    = 30.0           #[Pa]
thdist  = 300.0*1000.0   #[m]
thdura  = 24             #[h]
thpgmax = 0*100          #[Pa/1000km], integer
#lcrad   = [300.0*1000.0, 1000.0*1000.0, 1500.0*1000.0, 2000.0*1000.0]
#lcrad   = [500.0*1000.0, 1000.0*1000.0, 1500.0*1000.0, 2000.0*1000.0]
#lcrad   = [500.0*1000.0]
lcrad    = ctrack_para.ret_lcrad()
lxth     = ctrack_para.ret_lxth()
miss_cmip  = 1.0e+20
miss_dbl = -9999.0
miss_int = -9999

###################
# set dnz, dny, dnx
###################
dnx    = {}
dny    = {}
dnz    = {}
diz500 = {}
#
model = "NorESM1-M"
dnz.update({(model,"psl"):1, (model,"ua"):1, (model,"va"):1, (model,"hus"):8, (model,"ta"):8, (model,"wap"):8, (model,"zg"):8, (model,"huss"):1, (model,"psl"):1, (model,"tas"):1, (model,"prc"):1, (model,"pr"):1, (model,"rhs"):1})
dny[model] = 96
dnx[model] = 144
diz500[model] = 3
#
model = "MIROC5"
dnz.update({(model,"psl"):1, (model,"ua"):1, (model,"va"):1, (model,"hus"):8, (model,"ta"):8, (model,"wap"):8, (model,"zg"):8, (model,"huss"):1, (model,"psl"):1, (model,"tas"):1, (model,"prc"):1, (model,"pr"):1, (model,"rhs"):1})
dny[model] = 128
dnx[model] = 256
#
model = "CanESM2"
dnz.update({(model,"psl"):1, (model,"ua"):1, (model,"va"):1, (model,"hus"):8, (model,"ta"):8, (model,"wap"):8, (model,"zg"):8, (model,"huss"):1, (model,"psl"):1, (model,"tas"):1, (model,"prc"):1, (model,"pr"):1, (model,"rhs"):1})
dny[model] = 64
dnx[model] = 128

#####################################################
tstp  = "6hr"
dhinc = { "6hr":6 }
hinc  = dhinc[tstp]
dendh = { "6hr":18}
endh  = int(dendh[tstp])
#lmodel = ["NorESM1-M", "MIROC5","CanESM2"]
#lmodel = ["MIROC5", "CanESM2"]
#lmodel = ["MIROC5"]
lmodel = ["NorESM1-M"]
lexprtype = ["his", "fut"]
#lexprtype = ["fut"]
dexpr={}
dexpr["his"] = "historical"
dexpr["fut"] = "rcp85"
ens = "r1i1p1"
dyrange={}
#dyrange["his"] = [1990, 1999]
#dyrange["fut"] = [2086, 2095]
dyrange["his"] = ctrack_para.ret_iy_ey(dexpr["his"])
dyrange["fut"] = ctrack_para.ret_iy_ey(dexpr["fut"])
imon = 1
emon = 12
#lseason = ["DJF", "JJA","ALL"]
lseason = ["DJF"]
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
# make area [km2] map
#----------------------
def cal_area(lat1, lat2, dlon):
  lat1  = pi * abs(lat1) / 180.   # [deg] -> [rad]
  lat2  = pi * abs(lat2) / 180.   # [deg] -> [rad]
  dlon  = pi * dlon / 180.        # [deg] -> [rad]
  r     = 6379.136  #[km]
  ecc2  = 0.00669447
  ecc   = sqrt(ecc2)
  f1 = 0.5 * sin(lat1) / (1 - ecc2 * sin(lat1) * sin(lat1))\
      + 0.25 /ecc * log( abs((1 + ecc* sin(lat1))/(1- ecc* sin(lat1))) )

  f2 = 0.5 * sin(lat2) / (1 - ecc2 * sin(lat2) * sin(lat2))\
      + 0.25 /ecc * log( abs((1 + ecc* sin(lat2))/(1- ecc* sin(lat2))) )
  #print "f1=", f1
  #print "f2=", f2
  #print "f2-f1=" , f2 - f1
  area = pi * r*r * (1 - ecc2) /180.0 * abs(f2 - f1)
  area = area * (dlon * 180. /pi)
  return area
#****************************************************
#****************************************************
#****************************************************

#****************************************************
bindir    = "/home/utsumi/bin/dtanl/ctrack"
oekakidir = "/home/utsumi/bin/dtanl/ctrack/oekaki"
for model in lmodel:
  #----------------------------------------------------
  ny = dny[model]
  nx = dnx[model]
  nz = dnz[model, "wap"]
  iz500 = diz500[model]
  #****************************************************
  #for exprtype in ["his", "fut"]:
  #for exprtype in ["fut"]:
  for exprtype in lexprtype:
    expr = dexpr[exprtype]
    lyrange = dyrange[exprtype]
    iyear   = lyrange[0]
    eyear   = lyrange[1]
    print expr, iyear, eyear
    #****************************************************
    # read lat, lon data
    #----------------------
    axisdir_root    = "/media/disk2/data/CMIP5/bn/psl/%s"%(tstp)
    axisdir    = axisdir_root  + "/%s/%s/%s"%(model, expr, ens)
    latname    = axisdir  + "/lat.txt"
    lonname    = axisdir  + "/lon.txt"
    a1lat      = read_txtlist(latname)
    a1lon      = read_txtlist(lonname)
    dlat       = a1lat[1] - a1lat[0]
    dlon       = a1lon[1] - a1lon[0]
    
    lat_first  = a1lat[0]
    #-------
    a2area = array(zeros(ny*nx), float32).reshape(96,144)
    #---
    for iy in [0, ny-1]:
      lat           = a1lat[iy]
      lat1          = abs(lat) - dlat*0.5
      lat2          = lat
      area          = cal_area(lat1, lat2, dlon) * 2.0
      a2area[iy,:] = area
    #---
    for iy in range(1,ny-1):
      lat           = a1lat[iy]
      lat1          = a1lat[iy] - dlat*0.5
      lat2          = a1lat[iy] + dlat*0.5
      area          = cal_area(lat1, lat2, dlon)
      a2area[iy,:] = area
    #---------------
    lat_first = a1lat[0]
    lon_first = a1lon[0]
    dlat      = a1lat[1] - a1lat[0]
    dlon      = a1lon[1] - a1lon[0]

    ##**************************************************
    ##  call findcyclone   # pgrad is made too.
    ##------------------
    #cmd = bindir + "/findcyclone.py"
    #os.system("python %s %s %s %s %s %s %s %s %s %s %s %s %s %s"\
    #  %(cmd           \
    #  ,model          \
    #  ,expr           \
    #  ,ens            \
    #  ,tstp           \
    #  ,hinc           \
    #  ,iyear          \
    #  ,eyear          \
    #  ,imon           \
    #  ,emon           \
    #  ,nx             \
    #  ,ny             \
    #  ,miss_dbl       \
    #  ,thorog         \
    #  ))
    ##**************************************************
    ##  call connectc.py
    ##------------------
    #cmd = bindir + "/connectc.py"
    #os.system("python %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s"\
    #  %(cmd           \
    #  ,model          \
    #  ,expr           \
    #  ,ens            \
    #  ,tstp           \
    #  ,hinc           \
    #  ,iyear          \
    #  ,eyear          \
    #  ,imon           \
    #  ,emon           \
    #  ,nx             \
    #  ,ny             \
    #  ,miss_dbl       \
    #  ,miss_int       \
    #  ,endh           \
    #  ,thdp           \
    #  ,thdist         \
    #  ))
    #
    ##**************************************************
    #  call cdens.py
    #------------------
    for season in lseason:
    #  ####-----------------
    #  cmd = bindir + "/cdens.py"
    #  os.system("python %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s"\
    #    %(cmd           \
    #    ,model          \
    #    ,expr           \
    #    ,ens            \
    #    ,tstp           \
    #    ,hinc           \
    #    ,iyear          \
    #    ,eyear          \
    #    ,season         \
    #    ,nx             \
    #    ,ny             \
    #    ,miss_dbl       \
    #    ,miss_int       \
    #    ,endh           \
    #    ,thdura         \
    #    ,thpgmax        \
    #    ,thorog         \
    #    ))
      #**************************************************
      # names
      #*****************
      dpgradrange       = ctrack_para.ret_dpgradrange()
      lclass            = dpgradrange.keys()
      nclass            = len(lclass) -1
      #-----------------
      doutdir           = {}
      for year in range(iyear, eyear+1) + [0]:
        doutdir[year]   = "/media/disk2/out/CMIP5/6hr/%s/%s/%s/tracks/map/%04d"%(model, expr, ens, year)
      #------------------
      ddens_area_name   = {}
      ddens_area_u_name = {}
      dtrack_name       = {}
      dtrack_u_name     = {}
      #---------------------------
      # names: dens and track
      #---------------------------
      for iclass in lclass:
        dtrack_name[iclass]              = doutdir[0]    + "/track.grid.dura%02d.nc%02d.c%02d_%s_%s_%s_%s_%s.bn"%(thdura, nclass, iclass, season, tstp, model, expr, ens)
        #--
        for year in range(iyear, eyear+1) + [0]:
          ddens_area_name[year, iclass]  = doutdir[year] + "/dens.area.dura%02d.nc%02d.c%02d_%s_%s_%s_%s_%s.bn"%(thdura, nclass, iclass, season, tstp, model, expr, ens)
      #---------------------------
      # names: dens and track for upper side
      #---------------------------
      for iclass in lclass[1:]:
        dtrack_u_name[iclass]          = doutdir[0] + "/u.track.grid.dura%02d.nc%02d.c%02d_%s_%s_%s_%s_%s.bn"%(thdura, nclass, iclass, season, tstp, model, expr, ens)
        #--
        for year in range(iyear, eyear+1) + [0]: 
          ddens_area_u_name[year, iclass]        = doutdir[year]    + "/u.dens.area.dura%02d.nc%02d.c%02d_%s_%s_%s_%s_%s.bn"%(thdura, nclass, iclass, season, tstp, model, expr, ens)


      ##************************************
      ## track pict
      ##------------------------------------
      #for iclass in lclass:
      #  print "---------------------"
      #  print "track pict"
      #  #-------
      #  # names
      #  #-------
      #  cptfile   = oekakidir + "/cpt/polar.-1.1.cpt"
      #  pngname   = dtrack_name[iclass][:-3] + ".png"
      #  psfile    = dtrack_name[iclass][:-3] + ".ps"
      #  title     = "track"
      #  scalestep = 0.5
      #  overscale = 0
      #  #-------
      #  cmd = oekakidir + "/track.gmt.py"
      #  os.system("python %s %s %s %s %s %s %s"%(\
      #     cmd                  \
      #    ,dtrack_name[iclass]  \
      #    ,cptfile              \
      #    ,pngname              \
      #    ,title                \
      #    ,scalestep            \
      #    ,overscale            \
      #    ))
      #  print pngname
      ##************************************
      ## track upper side pict
      ##------------------------------------
      #for iclass in lclass[1:]:
      #  print "---------------------"
      #  print "track upper side pict"
      #  #-------
      #  # names
      #  #-------
      #  cptfile   = oekakidir + "/cpt/polar.-1.1.cpt"
      #  pngname   = dtrack_u_name[iclass][:-3] + ".png"
      #  psfile    = dtrack_u_name[iclass][:-3] + ".ps"
      #  title     = "track"
      #  scalestep = 0.5
      #  overscale = 0
      #  #-------
      #  cmd = oekakidir + "/track.gmt.py"
      #  os.system("python %s %s %s %s %s %s %s"%(\
      #     cmd                  \
      #    ,dtrack_u_name[iclass]  \
      #    ,cptfile              \
      #    ,pngname              \
      #    ,title                \
      #    ,scalestep            \
      #    ,overscale            \
      #    ))
      #  print pngname
      ##************************************
      ## dens pict
      ##------------------------------------
      #for year in range(iyear, eyear+1) + [0]:
      #  for iclass in lclass:
      #    print "---------------------"
      #    print "dens pict"
      #    #-------
      #    # names
      #    #-------
      #    cptfile   = oekakidir + "/cpt/sealand.0.3.ov.cpt"
      #    pngname   = ddens_area_name[year, iclass][:-3] + ".png"
      #    psfile    = ddens_area_name[year, iclass][:-3] + ".ps"
      #    title     = "density"
      #    scalestep = 1.0
      #    overscale = 0
      #    #-------
      #    cmd = oekakidir + "/dens.gmt.py"
      #    os.system("python %s %s %s %s %s %s %s"%(\
      #       cmd                           \
      #      ,ddens_area_name[year, iclass] \
      #      ,cptfile                       \
      #      ,pngname                       \
      #      ,title                         \
      #      ,scalestep                     \
      #      ,overscale                     \
      #      ))
      #    print pngname



      ##************************************
      ## dens pict upper side
      ##------------------------------------
      #for year in range(iyear, eyear+1) + [0]:
      #  for iclass in lclass[1:]:
      #    print "---------------------"
      #    print "dens upperside pict"
      #    #-------
      #    # names
      #    #-------
      #    cptfile   = oekakidir + "/cpt/sealand.0.3.ov.cpt"
      #    pngname   = ddens_area_u_name[year, iclass][:-3] + ".png"
      #    psfile    = ddens_area_u_name[year, iclass][:-3] + ".ps"
      #    title     = "density"
      #    scalestep = 1.0
      #    overscale = 0
      #    #-------
      #    cmd = oekakidir + "/dens.gmt.py"
      #    os.system("python %s %s %s %s %s %s %s"%(\
      #       cmd                             \
      #      ,ddens_area_u_name[year, iclass] \
      #      ,cptfile                         \
      #      ,pngname                         \
      #      ,title                           \
      #      ,scalestep                       \
      #      ,overscale                       \
      #      ))
      #    print pngname

    #**********************************************************
    dpgradrange = ctrack_para.ret_dpgradrange()

    lclass     = dpgradrange.keys()
    outdir     = "/media/disk2/out/CMIP5/6hr/%s/%s/%s/tracks/dura%02d/aggr.pr"%(model, expr, ens, thdura)
    odaydir    = "/media/disk2/out/CMIP5/day/%s/%s/%s/tracks/dura%02d/aggr.pr"%(model, expr, ens, thdura)
    ##**************************************************
    ##
    ##  call aggr_pr.py   # 6hourly
    ##
    ##--------------------------------------------------
    #import aggr_pr
    #cmd = bindir + "/aggr.pr.py"
    #for crad in lcrad:
    #  for season in lseason:
    #    #----------------------------------------------------------
    #    #  names for agg.pr, count.cyclone, pgrad_mean
    #    #-----------
    #    # precip aggr
    #    #-----------
    #    daggname  = {}
    #    daggname_allkey = {}
    #    for i in range(len(lclass)):
    #      iclass = lclass[i]
    #      daggname[iclass] = outdir + "/aggr.pr.c%02d.r%04d_%s_%s_%s_%s_%s.bn"%(iclass, crad*0.001, season, tstp, model, expr, ens)
    #      daggname_allkey[crad, season, iclass] = daggname[iclass]
    #    #-----------
    #    # count  # counts the center of cyclone
    #    #-----------
    #    dcountname = {}
    #    dcountname_allkey = {}
    #    for i in range(len(lclass)):
    #      iclass = lclass[i]
    #      dcountname[iclass] = outdir + "/count.cyclone.c%02d.r%04d_%s_%s_%s_%s_%s.bn"%(iclass, crad*0.001, season, tstp, model, expr, ens)
    #      dcountname_allkey[crad, season, iclass] = dcountname[iclass]
    #    #-----------
    #    # pgrad_mean
    #    #-----------
    #    dpgrad_mean_name = {}
    #    dpgrad_mean_name_allkey = {}
    #    for i in range(len(lclass)):
    #      iclass = lclass[i]
    #      dpgrad_mean_name[iclass] = outdir + "/pgrad_mean.c%02d.r%04d_%s_%s_%s_%s_%s.bn"%(iclass, crad*0.001, season, tstp, model, expr, ens)
    #      dpgrad_mean_name_allkey[crad, season, iclass] = dpgrad_mean_name[iclass]
    #
    #    ##------------------
    #    #aggr_pr.main(\
    #    #           model      \
    #    #          ,expr       \
    #    #          ,ens        \
    #    #          ,tstp       \
    #    #          ,hinc       \
    #    #          ,iyear      \
    #    #          ,eyear      \
    #    #          ,season     \
    #    #          ,nx         \
    #    #          ,ny         \
    #    #          ,miss_dbl   \
    #    #          ,miss_int   \
    #    #          ,crad       \
    #    #          ,thdura     \
    #    #          ,thorog     \
    #    #          ,dpgradrange\
    #    #          ,daggname\
    #    #          ,dpgrad_mean_name\
    #    #          ,dcountname\
    #    #         )
    ##----------------
    ## calc regional value
    ##****************
    #import cal_regionvalue
    #cal_regionvalue.main(\
    #            nx\
    #           ,ny\
    #           ,lat_first\
    #           ,lon_first\
    #           ,dlat\
    #           ,dlon\
    #           ,miss_dbl\
    #           ,lcrad\
    #           ,lseason\
    #           ,lclass\
    #           ,daggname_allkey\
    #           )
    ##**************************************************
    #**************************************************
    #
    #  call aggr_pr.py   # daily
    #
    #--------------------------------------------------
    #cmd = bindir + "/aggr_pr_day.py"
    #for crad in lcrad:
    #  for season in lseason:
    #    os.system("python %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s" %(\
    #        cmd\
    #      , model\
    #      , expr\
    #      , ens\
    #      , tstp\
    #      , hinc\
    #      , iyear\
    #      , eyear\
    #      , season\
    #      , nx\
    #      , ny\
    #      , nz\
    #      , miss_dbl\
    #      , miss_int\
    #      , crad\
    #      , thdura\
    #      , thorog\
    #      , iz500\
    #      ))
    #**************************************************
    #  call aggr_wfpr_day.py  # make num, sp, sp2  
    #**************************************************
    cmd  = bindir + "/aggr_wfpr_day.py"
    print "cmd=", cmd
    print "lcrad=",lcrad
    print "lxth=",lxth
    for crad in lcrad:
      for season in lseason:
        for xth in lxth:
          print "xth=",xth, "crad=",crad
          os.system("python %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s"%(\
               cmd\
              ,model   \
              ,expr    \
              ,ens     \
              ,tstp    \
              ,hinc    \
              ,iyear   \
              ,eyear   \
              ,season  \
              ,nx      \
              ,ny      \
              ,nz      \
              ,miss_dbl\
              ,miss_int\
              ,crad    \
              ,thdura  \
              ,thorog  \
              ,iz500   \
              ,xth     \
              ))






