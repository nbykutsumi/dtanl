from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from numpy import *
from ctrack_fsub import *
import calendar
import ctrack_para
import ctrack_func
import tc_para
import tc_func
import sys, os
#--------------------------------------
model = "org"

#singleday = True
singleday = False
iyear   = 2000
eyear   = 2004
lseason = ["JJA","DJF"]
#season  = "JJA"
#season  = "DJF"
#season  = "ALL"
iday    = 1
ny      = 180
nx      = 360

miss_int= -9999
# local region ------
#
# corner points should be
# at the center of original grid box
#lllat   = 25.
#urlat   = 50.
#lllon   = 130.
#urlon   = 155.

lllat   = -89.5
urlat   = 89.5
lllon   = 0.5
urlon   = 359.5

thdura    = 72

for season in lseason:
  #----------------------------
  lmon = ctrack_para.ret_lmon(season)
  #lmon = [1]
  #----------------------------
  dlat    = 1.0
  dlon    = 1.0
  a1lat   = arange(-89.5, 89.5 +dlat*0.5,  dlat)
  a1lon   = arange(0.5,   359.5 +dlon*0.5, dlon)
  #----------------------------
  dpgradrange  = ctrack_para.ret_dpgradrange()
  lclass  = dpgradrange.keys()
  nclass  = len(lclass)
  thpgrad = dpgradrange[0][0]
  #----------------------------
  psldir_root     = "/media/disk2/data/JRA25/sa.one.%s/6hr/PRMSL"%(model)
  pgraddir_root   = "/media/disk2/out/JRA25/sa.one.%s/6hr/pgrad"%(model)
  lifedir_root    = "/media/disk2/out/JRA25/sa.one.%s/6hr/life"%(model)
  nextposdir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/nextpos"%(model)
  #************************************
  dtrack     = {}
  for iclass in lclass:
    dtrack[iclass] = []
  #------------------------------------
  for year in range(iyear, eyear+1):
    #************************
    # load TCs
    #------------------------
    dTC  = tc_func.ret_ibtracs_dpyxy_saone(year)

    #------------------------
    for mon in lmon:
      eday = calendar.monthrange(year,mon)[1]
      ###############
      ## no leap
      ###############
      #if (mon==2)&(calendar.isleap(year)):
      #  eday = calendar.monthrange(year,mon)[1] -1
      #else:
      #  eday = calendar.monthrange(year,mon)[1]
  
      #if singleday == True:
      #  eday = iday
      ##############
      for day in range(iday, eday+1):
        print "tracklines",model,year, mon, day
        for hour in [0, 6, 12, 18]:
  
          stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)
  
          psldir          = psldir_root     + "/%04d%02d"%(year, mon)
          pgraddir        = pgraddir_root   + "/%04d%02d"%(year, mon)
          lifedir         = lifedir_root    + "/%04d%02d"%(year, mon)
          nextposdir      = nextposdir_root + "/%04d%02d"%(year, mon)
          
          pslname         = psldir     + "/anl_p.PRMSL.%s.sa.one"%(stime)
          pgradname       = pgraddir   + "/pgrad.%s.sa.one"%(stime)
          lifename        = lifedir    + "/life.%s.sa.one"%(stime)
          nextposname     = nextposdir + "/nextpos.%s.sa.one"%(stime)
          
          a2psl           = fromfile(pslname,   float32).reshape(ny, nx)
          a2pgrad         = fromfile(pgradname, float32).reshape(ny, nx)
          a2life          = fromfile(lifename,  int32).reshape(ny, nx)
          a2nextpos       = fromfile(nextposname,  int32).reshape(ny, nx)
          #************************
          #------------------------
          for iy in range(0, ny):
            #---------------
            lat       = a1lat[iy]
            if ((lat < lllat) or (urlat < lat)):
              continue
            #---------------
            for ix in range(0, nx):
              #-------------
              lon     = a1lon[ix]
              if ((lon < lllon) or (urlon < lon)):
                continue
              #-------------
              pgrad   = a2pgrad[iy, ix]
              #------
              if (pgrad < thpgrad):
                continue
          
              #-- check duration -----
              life  = a2life[iy, ix]
              dura  = ctrack_func.solvelife_point_py(life, miss_int)[1]
              if  (dura < thdura):
                continue

              #-- check TC -----------
              tcflag = 0
              if (ix,iy) in dTC[year,mon,day,hour]:
                print "TC!, lat,lon=",year,mon,day,hour,iy-90.0, ix
                tcflag = tcflag +1
              else:
                ixfort = ix +1
                iyfort = iy +1
                a1surrxfort, a1surryfort = ctrack_fsub.mk_8gridsxy(ixfort, iyfort, nx, ny)
                for itemp in range(0,8):
                  ixt =  a1surrxfort[itemp] -1
                  iyt =  a1surryfort[itemp] -1
                  if (ixt,iyt) in dTC[year,mon,day,hour]:
                    print "TC!, lat,lon=",year,mon,day,hour,iy-90.0, ix
                    tcflag = tcflag + 1
              #
              if tcflag > 0:
                continue
            
              #-----------------------
              for iclass in range(0, nclass):
                pgrad_min = dpgradrange[iclass][0]
                pgrad_max = dpgradrange[iclass][1]
                if (pgrad_min <= pgrad < pgrad_max):
                  #------
                  nextpos   = a2nextpos[iy, ix]
                  x_next, y_next = ctrack_func.fortpos2pyxy(nextpos, nx, miss_int)
                  if ( (x_next == miss_int) & (y_next == miss_int) ):
                    continue
                  #------
                  lat_next  = a1lat[y_next]
                  lon_next  = a1lon[x_next]
                  #
                  dtrack[iclass].append([[year, mon, day, hour],[lat, lon, lat_next, lon_next]])
          
  #*************\***********
  # for mapping
  nnx        = int( (urlon - lllon)/dlon)
  nny        = int( (urlat - lllat)/dlat)
  a1lon_loc  = linspace(lllon, urlon, nnx)
  a1lat_loc  = linspace(lllat, urlat, nny)
  LONS, LATS = meshgrid( a1lon_loc, a1lat_loc)
  #------------------------
  # Basemap
  #------------------------
  print "Basemap"
  figmap   = plt.figure()
  axmap    = figmap.add_axes([0, 0.1, 1.0, 0.8])
  M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
  
  #-- draw cyclone tracks ------
  itemp = 1
  #for iclass in lclass[1:]:
  for iclass in lclass[2:]:
    if (len(dtrack[iclass]) ==  0.0):
      continue
    #-----------
    for track in dtrack[iclass]:
      itemp = itemp + 1
      year = track[0][0]
      mon  = track[0][1]
      day  = track[0][2]
      hour = track[0][3]
  
      lat1 = track[1][0]
      lon1 = track[1][1]
      lat2 = track[1][2]
      lon2 = track[1][3]
  
      if iclass ==1:
        #scol="gray"
        scol="r"
      elif iclass ==2:
        #scol="b"
        scol="r"
      elif iclass ==3:
        #scol="g"
        scol="r"
      elif iclass == 4:
        #scol="gray"
        scol="r"
   
      #------------------------------------
      if abs(lon1 - lon2) >= 180.0:
        #--------------
        if (lon1 > lon2):
          lon05_1  = 360.0
          lon05_2  = 0.0
          lat05    = lat1 + (lat2 - lat1)/(lon05_1 - lon1 + lon2 - lon05_2)*(lon05_1 - lon1)
        elif (lon1 < lon2):
          lon05_1  = 0.0
          lon05_2  = 360.0
          lat05    = lat1 + (lat2 - lat1)/(lon05_1 - lon1 + lon2 - lon05_2)*(lon05_1 - lon1)
        #--------------
        M.plot( (lon1, lon05_1), (lat1, lat05), linewidth=1, color=scol)
        M.plot( (lon05_2, lon2), (lat05, lat2), linewidth=1, color=scol)
        #--------------
      else:
        M.plot( (lon1, lon2), (lat1, lat2), linewidth=1, color=scol)
   
  
  #-- coastline ---------------
  print "coastlines"
  M.drawcoastlines(color="k")
  
  #-- save --------------------
  print "save"
  sodir   = "/media/disk2/out/cyclone/exc.track.w.bsttc"
  ctrack_func.mk_dir(sodir)
  soname  = sodir + "/exc.tracklines.w.bsttc.%s.%04d-%04d.%s.%02dh.png"%(model, iyear, eyear,season, thdura)
  plt.savefig(soname)
  plt.clf()
  print soname
  plt.clf()
