from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from numpy import *
from ctrack_fsub import *
import calendar
import ctrack_para
import ctrack_func
import tc_para
import sys, os
#--------------------------------------
print len(sys.argv), sys.argv
if len(sys.argv) > 1:
  print "from py.py"
  year     = int(sys.argv[1])
  season    = sys.argv[2]
  #-----
  try:
    season  = int(season)
  except ValueError:
    season  = season
  #-----
  thdura    = int(sys.argv[3])
  thwcore   = float(sys.argv[4])
  thsst     = float(sys.argv[5])
  thwind    = float(sys.argv[6])
  thrvort   = float(sys.argv[7])
  plev_low  = float(sys.argv[8])
  plev_mid  = float(sys.argv[9])
  plev_up   = float(sys.argv[10])
  tplev_low = float(sys.argv[11])
  model     = sys.argv[12]
  region    = sys.argv[13]
else:
  print "NOT from py.py"
  model    = "org"
  year   = 2004
  #season  = "DJF"
  #season  = 8
  season  = "ALL"
  #season  = 8
  #thdura  = 72
  thdura  = 48
  dpgradrange   = ctrack_para.ret_dpgradrange()
  thpgrad        = dpgradrange[1][0]
  thsst    = tc_para.ret_thsst()
  thwind   = tc_para.ret_thwind()
  thrvort  = tc_para.ret_thrvort(model)
  thwcore  = tc_para.ret_thwcore(model)

  plev_low = 850*100.0 # (Pa)
  plev_mid = 500*100.0 # (Pa)
  plev_up  = 250*100.0 # (Pa)
  
  tplev_low = 850*100.0
#---------------------------------
ny      = 180
nx      = 360

miss    = -9999.0
miss_int= -9999
# local region ------
#
# corner points should be
# at the center of original grid box
if region =="JPN":
  lllat   = 25.
  urlat   = 60.
  lllon   = 110.
  urlon   = 180.
elif region == "INDIA":
  lllat   = 0.
  urlat   = 30.
  lllon   = 50.
  urlon   = 100.


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
lastposdir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/lastpos"%(model)
iposdir_root    = "/media/disk2/out/JRA25/sa.one.%s/6hr/ipos"%(model)
#
tdir_root       = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP"%(model)
udir_root       = "/media/disk2/data/JRA25/sa.one.%s/6hr/UGRD"%(model)
vdir_root       = "/media/disk2/data/JRA25/sa.one.%s/6hr/VGRD"%(model)
#
sstdir_root     = "/media/disk2/data/JRA25/sa.one.anl_p25/mon/WTMPsfc"
#
sodir_root      = "/media/disk2/out/cyclone/tc.obj"
sodir           = sodir_root
ctrack_func.mk_dir(sodir_root)
ctrack_func.mk_dir(sodir)
#** land sea mask -------------------
landseadir      = "/media/disk2/data/JRA25/sa.one.anl_land/const/landsea"
landseaname     = landseadir + "/landsea.sa.one"
a2landsea       = fromfile(landseaname, float32).reshape(ny,nx)

#************************************
dtrack     = {}
for iclass in lclass:
  dtrack[iclass] = []
#-------
a2lastflag    = ones([ny,nx],float32)*miss
initflag      = -1
#------------------------------------
for mon in lmon:
  #eday = 1
  eday = calendar.monthrange(year,mon)[1]
  ##############
  #  SST 
  #-------------
  sstdir   = sstdir_root + "/%04d"%(year)
  sstname  = sstdir + "/fcst_phy2m.WTMPsfc.%04d%02d.sa.one"%(year,mon)
  a2sst    = fromfile( sstname, float32).reshape(ny,nx)
  #-------------
  for day in range(1, eday+1):
    print year, mon, day, thdura, thwcore, thsst, thwind, thrvort, plev_up*0.01, tplev_low*0.01
    for hour in [0, 6, 12, 18]:
      initflag = initflag + 1
      stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)

      psldir          = psldir_root     + "/%04d%02d"%(year, mon)
      pgraddir        = pgraddir_root   + "/%04d%02d"%(year, mon)
      lifedir         = lifedir_root    + "/%04d%02d"%(year, mon)
      tdir            = tdir_root       + "/%04d%02d"%(year, mon)
      udir            = udir_root       + "/%04d%02d"%(year, mon)
      vdir            = vdir_root       + "/%04d%02d"%(year, mon)
      nextposdir      = nextposdir_root + "/%04d%02d"%(year, mon)
      lastposdir      = lastposdir_root + "/%04d%02d"%(year, mon)
      iposdir         = iposdir_root    + "/%04d%02d"%(year, mon)
      
      pslname         = psldir     + "/anl_p.PRMSL.%s.sa.one"%(stime)
      pgradname       = pgraddir   + "/pgrad.%s.sa.one"%(stime)
      lifename        = lifedir    + "/life.%s.sa.one"%(stime)
      tlowname        = tdir       + "/anl_p.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(tplev_low*0.01, year, mon, day, hour)
      tmidname        = tdir       + "/anl_p.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_mid*0.01, year, mon, day, hour)
      tupname         = tdir       + "/anl_p.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_up *0.01, year, mon, day, hour)
      ulowname        = udir       + "/anl_p.UGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_low*0.01, year, mon, day, hour)
      uupname         = udir       + "/anl_p.UGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_up *0.01, year, mon, day, hour)
      vlowname        = vdir       + "/anl_p.VGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_low*0.01, year, mon, day, hour)
      vupname         = vdir       + "/anl_p.VGRD.%04dhPa.%04d%02d%02d%02d.sa.one"%(plev_up *0.01, year, mon, day, hour)
      nextposname     = nextposdir + "/nextpos.%s.sa.one"%(stime)
      lastposname     = lastposdir + "/lastpos.%s.sa.one"%(stime)
      iposname        = iposdir    + "/ipos.%s.sa.one"%(stime)
      
      a2psl           = fromfile(pslname,   float32).reshape(ny, nx)
      a2pgrad         = fromfile(pgradname, float32).reshape(ny, nx)
      a2life          = fromfile(lifename,  int32).reshape(ny, nx)
      a2nextpos       = fromfile(nextposname,  int32).reshape(ny, nx)
      a2lastpos       = fromfile(lastposname,  int32).reshape(ny, nx)
      a2ipos          = fromfile(iposname,  int32).reshape(ny, nx)
      a2tlow          = fromfile(tlowname,  float32).reshape(ny, nx)
      a2tmid          = fromfile(tmidname,  float32).reshape(ny, nx)
      a2tup           = fromfile(tupname,   float32).reshape(ny, nx)
      a2ulow          = fromfile(ulowname,  float32).reshape(ny, nx)
      a2uup           = fromfile(uupname,   float32).reshape(ny, nx)
      a2vlow          = fromfile(vlowname,  float32).reshape(ny, nx)
      a2vup           = fromfile(vupname,   float32).reshape(ny, nx)

      #--------------------------------
      tout            = ctrack_fsub.find_tc_saone(\
                        a2pgrad.T, a2life.T, a2lastpos.T, a2lastflag.T, a2tlow.T, a2tmid.T, a2tup.T, a2ulow.T, a2uup.T, a2vlow.T, a2vup.T, a2sst.T, a2landsea.T\
                      , thpgrad, thdura, thsst, thwind, thrvort, initflag, miss)
      a2tcloc         =  tout[0].T
      a2lastflag      =  tout[1].T
      #
      a2tcloc  = ma.masked_less(a2tcloc, thwcore).filled(miss)
      a2tcloc  = ma.masked_not_equal(a2tcloc, miss).filled(1.0)
      a2tcloc  = ma.masked_equal(a2tcloc, miss).filled(0.0)
      #
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

          if a2tcloc[iy, ix] > 0.0:

            nextpos   = a2nextpos[iy, ix]
            x_next, y_next = ctrack_func.fortpos2pyxy(nextpos, nx, miss_int)
            if ( (x_next == miss_int) & (y_next == miss_int) ):
              continue
            #------
            lat_next  = a1lat[y_next]
            lon_next  = a1lon[x_next]
            #
            dtrack[0].append([[year, mon, day, hour],[lat, lon, lat_next, lon_next]])
        
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
axmap    = figmap.add_axes([0.1, 0.1, 0.9, 0.7])
M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)

#-- coastline ---------------
print "coastlines"
M.drawcoastlines(color="k")

#-- meridians and parallels
meridians = 10.0
parallels = 10.0
M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1], rotation=90)
M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0])
#-- title -------------------
stitle = "TCobj res=%s %04d %s %02dh wc:%3.1f\n"%(model, year, season, thdura, thwcore)
stitle = stitle + "sst:%.0f wind:%d vort:%.1e tplow:%d wpup:%d"%(thsst-273.15, thwind, thrvort, tplev_low*0.01, plev_up*0.01)
axmap.set_title(stitle)

#-- draw cyclone tracks ------
itemp = 1
for iclass in [0]:
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

    if iclass == 0:
      scol = "r"
 
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

    #-- text -------------------
    if hour in [0,12]:
      xtext, ytext = M(lon1,lat1)
      plt.text(xtext,ytext-1, "%02d.%02d.%02d"%(mon, day,hour) ,fontsize=12, rotation=-90) 

#-- save --------------------
print "save"
soname  = sodir + "/tclines.%s.%s.%04d.%s.%02dh.wc%3.2f.sst%d.wind%d.vor%.1e.tplow%d.pup%d.png"%(model, region, year, season, thdura, thwcore, thsst -273.15, thwind, thrvort, tplev_low*0.01, plev_up*0.01)
plt.savefig(soname)
plt.clf()
print soname
plt.clf()

