from numpy import *
from ctrack_fsub import *
import ctrack_func
import ctrack_para
#*******************************************
iyear     = 2004
eyear     = 2004
lmon      = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon      = [9]
lhour     = [0,6,12,18]
lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
#lmodel    = ["org"]
radkm     = 300.0   # (km)
lregion = ["GLB","PNW", "PNE","INN","INS", "PSW","ATN"]
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

for model in lmodel:
  for region in lregion:
    #-- region mask ---
    lllat, lllon, urlat, urlon = ctrack_para.ret_tcregionlatlon(region)
    a2domain  = ctrack_func.mk_region_mask(lllat, urlat, lllon, urlon, nx, ny, lat_first, lon_first, dlat, dlon)

    #-- init ----------
    lvort_rad   = []
    lvort       = []
    ldt         = []
  
    #------------------
    for year_loop in range(iyear, eyear+1):
      bestname  = bestdir + "/Year.%04d.ibtracs_all.v03r04.csv"%(year_loop)
      #-- open -------
      f = open(bestname, "r")
      lines = f.readlines()
      f.close()
      #-- init dictionary --
      ddat  = {}
      for mon in range(1,12+1):
        ddat[mon] = []
      #-- csv data loop -------------
      for line in lines[3:]:
        line     = line.split(",")
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
        #--- check nature --
        nature   = line[7].strip()
        if nature not in ["TS"]:
          continue
        #-----------------
        tcname   = line[5].strip()
        lat      = float(line[16])
        lon      = positive_lon(float(line[17]))
        ixpy     = int((lon-0.0)/dlon)
        iypy     = int((lat-(-90.0))/dlat)
        ixfort   = ixpy + 1
        iyfort   = iypy + 1

        #-- check region --
        if a2domain[iypy,ixpy] ==0.0:
          print "out of domain", region,lat,lon
          continue
        #------------------
        ldat_temp = [year,mon,day,hour,ixpy, iypy, tcname]
        ddat[mon].append(ldat_temp)
      #*************************************
      for mon in lmon:
        print model,year,mon
        lines    = ddat[mon]
        lines.sort(cmp = lambda x,y: cmp(x[2],y[2])) # sort by day
        for line in lines:
          year   = line[0]
          day    = line[2]
          hour   = line[3]
          ixpy   = line[4]
          iypy   = line[5]
          ixfort = ixpy +1
          iyfort = iypy +1
  
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
          psldir    = "/media/disk2/data/JRA25/sa.one.org/6hr/PRMSL/%04d%02d"%(year,mon)
          pslname   = psldir + "/anl_p.PRMSL.%04d%02d%02d%02d.sa.one"%(year,mon,day,hour)
          #*************************************
          #------  check psl minima ---
          a2psl     = fromfile(pslname,  float32).reshape(ny,nx)
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
          #-- W ---
          xtemp = xw
          ytemp = yw
          if a2psl[iypy,ixpy] >=a2psl[ytemp,xtemp]:
           centflag = centflag +1
          #-- E ---
          xtemp = xe
          ytemp = ye
          if a2psl[iypy,ixpy] >=a2psl[ytemp,xtemp]:
           centflag = centflag +1
      
          #-- NW ---
          xtemp = xnw
          ytemp = ynw
          if a2psl[iypy,ixpy] >=a2psl[ytemp,xtemp]:
           centflag = centflag +1
      
          #-- NE ---
          xtemp = xne
          ytemp = yne
          if a2psl[iypy,ixpy] >=a2psl[ytemp,xtemp]:
           centflag = centflag +1
      
          #-- SE ---
          xtemp = xse
          ytemp = yse
          if a2psl[iypy,ixpy] >=a2psl[ytemp,xtemp]:
           centflag = centflag +1
      
          #-- SW ---
          xtemp = xsw
          ytemp = ysw
          if a2psl[iypy,ixpy] >=a2psl[ytemp,xtemp]:
           centflag = centflag +1
          #
          if centflag >0:
            continue
      
          #------ load input data -----
          a2t850    = fromfile(tname850, float32).reshape(ny,nx)
          a2t500    = fromfile(tname500, float32).reshape(ny,nx)
          a2t250    = fromfile(tname250, float32).reshape(ny,nx)
          #
          a2u850    = fromfile(uname850, float32).reshape(ny,nx)
          a2v850    = fromfile(vname850, float32).reshape(ny,nx)
          #
          ##------ vort -----------------
          vort850rad   = ctrack_fsub.point_rvort_rad_saone(ixfort, iyfort, a2u850.T, a2v850.T, radkm, miss)
          vort850      = ctrack_fsub.point_rvort_saone(ixfort, iyfort, a2u850.T, a2v850.T, miss)
          dt850        = ctrack_fsub.point_dt_rad_saone(ixfort, iyfort, a2t850.T, radkm, miss)
          dt500        = ctrack_fsub.point_dt_rad_saone(ixfort, iyfort, a2t500.T, radkm, miss)
          dt250        = ctrack_fsub.point_dt_rad_saone(ixfort, iyfort, a2t250.T, radkm, miss)
          dt           = dt850 + dt500 + dt250
          #print vort850rad, vort850, dt850, dt500, dt250, dt
          lvort_rad.append(abs(vort850rad))
          lvort.append( abs(vort850))
          ldt.append(dt)
    #*******************************************
    # vort rad
    #--------
    sout = "frac/vort_rad(s-1),%s\n"%(model)
    odir   = "/media/disk2/out/obj.valid/tc.vort/%s"%(region)
    ctrack_func.mk_dir(odir)
    oname  = odir + "/vort.%s.%04d-%04d.%s.csv"%(model,iyear,eyear,region)
    ltemp  = lvort_rad
    ltemp  = sort(ltemp)
    lendat = len(ltemp)
    for i in range(lendat):
      frac = (i+1)/float(lendat)
      v    = ltemp[i]
      sout = sout + "%f,%f\n"%(frac, v)
    #
    f = open(oname,"w");  f.write(sout);  f.close()
    print oname
  
    #*******************************************
    # dt rad
    #--------
    sout = "frac/dt_rad(s-1),%s\n"%(model)
    odir   = "/media/disk2/out/obj.valid/tc.dt/%s"%(region)
    ctrack_func.mk_dir(odir)
    oname  = odir + "/dt.%s.%04d-%04d.%s.csv"%(model,iyear,eyear,region)
    ltemp  = ldt
    ltemp  = sort(ltemp)
    lendat = len(ltemp)
    for i in range(lendat):
      frac = (i+1)/float(lendat)
      v    = ltemp[i]
      sout = sout + "%f,%f\n"%(frac, v)
    #
    f = open(oname,"w");  f.write(sout);  f.close()
    print oname

