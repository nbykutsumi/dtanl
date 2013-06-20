from numpy import *
from ctrack_fsub import *
import ctrack_func
#*******************************************
iyear     = 2004
eyear     = 2004
lmon      = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon      = [9]
lhour     = [0,6,12,18]
#lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel    = ["org"]
radkm     = 300.0   # (km)

ny        = 180
nx        = 360
dlat      = 1.0
dlon      = 1.0
lat_first = -89.5
lon_first = 0.5
a1lat     = arange(-89.5, 89.5+0.001,  1.0)
a1lon     = arange(0.5,   359.5+0.001, 1.0)
miss      = -9999.0

bestdir   = "/media/disk2/data/ibtracs/v03r04"
odir      = "/media/disk2/out/obj.valid/exc.pgrad"
#------------------
def positive_lon(lon):
  if lon <0.0:
    positive_lon = 360 + lon
  else:
    positive_lon = lon
  #
  return positive_lon
#------------------
#------------------
for model in lmodel:
  #-- init ----------
  lvort_rad   = []
  lvort       = []
  ldt         = []
  sout        = ""
  sout = "code,tcname,sisotime,nature,center,windrank,presrank,lon,lat,centflag,dt850,dt500,dt250,dt\n"

  #-- init ----------
  ldat  = [] 
  #------------------
  for year_loop in range(iyear, eyear+1):
    bestname  = bestdir + "/Year.%04d.ibtracs_all.v03r04.csv"%(year_loop)
    #-- open -------
    f = open(bestname, "r")
    lines = f.readlines()
    f.close()
    #-- csv data loop -------------
    for line in lines[3:]:
      line     = line.split(",")
      code     = line[0]
      tcname   = line[5]
      sisotime = line[6]
      nature   = line[7]
      center   = line[12]
      windrank = line[13]
      presrank = line[14]
      #-- time ------
      isotime  = line[6].split(" ")
      time     = map(int, isotime[0].split("-"))
      year     = time[0]
      mon      = time[1]
      day      = time[2]
      hour     = int(isotime[1].split(":")[0])
      #--- check year --
      if ((year <iyear)or(eyear<year)):
        continue      
      #--- check hour --
      if hour not in lhour:
        continue
      #--- check mon ---
      if mon not in lmon:
        continue
      ##--- check nature --
      #if nature not in ["TS"]:
      #  continue
      #-----------------
      #-----------------
      lat      = float(line[16])
      lon      = positive_lon(float(line[17]))
      ixpy     = int((lon-0.0)/dlon)
      iypy     = int((lat-(-90.0))/dlat)
      ixfort   = ixpy + 1
      iyfort   = iypy + 1
      #-----------------
      ltemp    = [code, tcname, sisotime, nature, center, windrank, presrank, year, mon, day, hour, lat, lon, ixpy, iypy]
      ldat.append(ltemp)
  #*************************************
  ldat.sort(cmp = lambda x,y: cmp(x[2],y[2])) # sort

  for line in ldat:
    #--------------------------------------------
    code      = line[0]
    tcname    = line[1]
    sisotime  = line[2]
    nature    = line[3]
    center    = line[4]
    windrank  = line[5]
    presrank  = line[6]
    year      = line[7]
    mon       = line[8]
    day       = line[9]
    hour      = line[10]
    lat       = line[11]
    lon       = line[12]
    ixpy      = line[13]
    iypy      = line[14]
    ixfort    = ixpy + 1
    iyfort    = iypy + 1

    print "sisotime=",sisotime
    #----- input names --------------------------
    tdir      = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP/%04d%02d"%(model,year,mon)
    tname850  = tdir + "/anl_p.TMP.0850hPa.%04d%02d%02d%02d.sa.one"%(year,mon,day,hour)
    tname500  = tdir + "/anl_p.TMP.0500hPa.%04d%02d%02d%02d.sa.one"%(year,mon,day,hour)
    tname250  = tdir + "/anl_p.TMP.0250hPa.%04d%02d%02d%02d.sa.one"%(year,mon,day,hour)
    #
    udir      = "/media/disk2/data/JRA25/sa.one.%s/6hr/UGRD/%04d%02d"%(model,year,mon)
    uname850  = udir + "/anl_p.UGRD.0850hPa.%04d%02d%02d%02d.sa.one"%(year,mon,day,hour)
    #
    vdir      = "/media/disk2/data/JRA25/sa.one.%s/6hr/VGRD/%04d%02d"%(model,year,mon)
    vname850  = vdir + "/anl_p.VGRD.0850hPa.%04d%02d%02d%02d.sa.one"%(year,mon,day,hour)
    #
    psldir    = "/media/disk2/data/JRA25/sa.one.%s/6hr/PRMSL/%04d%02d"%(model,year,mon)
    pslname   = psldir + "/anl_p.PRMSL.2004011306.sa.one"
    pslname   = psldir + "/anl_p.PRMSL.%04d%02d%02d%02d.sa.one"%(year,mon,day,hour)
    #*************************************
    #------ load input data -----
    a2t850    = fromfile(tname850, float32).reshape(ny,nx)
    a2t500    = fromfile(tname500, float32).reshape(ny,nx)
    a2t250    = fromfile(tname250, float32).reshape(ny,nx)
    #
    a2u850    = fromfile(uname850, float32).reshape(ny,nx)
    a2v850    = fromfile(vname850, float32).reshape(ny,nx)
    #
    a2psl     = fromfile(pslname,  float32).reshape(ny,nx)
    ##------ vort & dt ----------
    vort850rad   = ctrack_fsub.point_rvort_rad_saone(ixfort, iyfort, a2u850.T, a2v850.T, radkm, miss)
    vort850      = ctrack_fsub.point_rvort_saone(ixfort, iyfort, a2u850.T, a2v850.T, miss)
    dt850        = ctrack_fsub.point_dt_rad_saone(ixfort, iyfort, a2t850.T, radkm, miss)
    dt500        = ctrack_fsub.point_dt_rad_saone(ixfort, iyfort, a2t500.T, radkm, miss)
    dt250        = ctrack_fsub.point_dt_rad_saone(ixfort, iyfort, a2t250.T, radkm, miss)
    dt           = dt850 + dt500 + dt250
    #------- psl ----------------
    centflag = 0
    xn   = ixpy
    xs   = ixpy
    xw   = ixpy -1
    xnw  = ixpy -1
    xsw  = ixpy -1
    xe   = ixpy +1
    xne  = ixpy +1
    xse  = ixpy +1
    if ixpy ==0:
      xw = 359
      xwn = 359
      xws = 359
    elif ixpy ==359:
      xe = 0
      xen = 0
      xes = 0
    #--
    yw  = iypy
    ye  = iypy
    ys  = iypy -1
    ysw = iypy -1
    yse = iypy -1
    yn  = iypy +1
    ynw = iypy +1
    yne = iypy +1
    #-- N ---
    xtemp = xn
    ytemp = yn
    if a2psl[iypy,ixpy] >= a2psl[ytemp,xtemp]:
     centflag = centflag +1
    #-- S ---
    xtemp = xs
    ytemp = ys
    if a2psl[iypy,ixpy] >=a2psl[ytemp,xtemp]:
     centflag = centflag +1
    print a2psl[iypy,ixpy],a2psl[ytemp,xtemp]
    #-- W ---
    xtemp = xw
    ytemp = yw
    if a2psl[iypy,ixpy] >=a2psl[ytemp,xtemp]:
     centflag = centflag +1
    print a2psl[iypy,ixpy],a2psl[ytemp,xtemp]
    #-- E ---
    xtemp = xe
    ytemp = ye
    if a2psl[iypy,ixpy] >=a2psl[ytemp,xtemp]:
     centflag = centflag +1
    print a2psl[iypy,ixpy],a2psl[ytemp,xtemp]
    #-- NW ---
    xtemp = xnw
    ytemp = ynw
    if a2psl[iypy,ixpy] >=a2psl[ytemp,xtemp]:
     centflag = centflag +1
    print a2psl[iypy,ixpy],a2psl[ytemp,xtemp]

    #-- NE ---
    xtemp = xne
    ytemp = yne
    if a2psl[iypy,ixpy] >=a2psl[ytemp,xtemp]:
     centflag = centflag +1
    print a2psl[iypy,ixpy],a2psl[ytemp,xtemp]

    #-- SE ---
    xtemp = xse
    ytemp = yse
    if a2psl[iypy,ixpy] >=a2psl[ytemp,xtemp]:
     centflag = centflag +1
    print a2psl[iypy,ixpy],a2psl[ytemp,xtemp]

    #-- SW ---
    xtemp = xsw
    ytemp = ysw
    if a2psl[iypy,ixpy] >=a2psl[ytemp,xtemp]:
     centflag = centflag +1
    print a2psl[iypy,ixpy],a2psl[ytemp,xtemp]
    print "flag =",centflag
    #----------------------------
    sout  = sout + "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n"\
        %(code, tcname, sisotime, nature, center, windrank, presrank\
         ,lon, lat, centflag\
         ,dt850, dt500, dt250, dt)
  #-- write to file ------
  odir   = "/media/disk2/out/obj.valid/tc.dt"
  oname  = odir + "/dt.ibtracs.%04d-%04d.csv"%(iyear,eyear)
  f = open(oname,"w"); f.write(sout); f.close() 




