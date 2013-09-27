from numpy import *
from ctrack_fsub import *
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import calendar
import ctrack_para
import ctrack_func
import tc_para, cmip_para, cmip_func
#-----------------------------------------
#singleday = True
singleday = False
lmodel   = ["MIROC5"]
lexpr    = ["historical"]
iyear    = 1980
eyear    = 1999
#lmon     = [1,2,3,4,5,6,7,8,9,10,11,12]
season   = "ALL"
thdura  = 48


lmon     = ctrack_para.ret_lmon(season)
stepday  = 0.25
miss     = -9999.0
miss_int = -9999

ny     = 180
nx     = 360
#----------------------------
dlat    = 1.0
dlon    = 1.0
a1lat   = arange(-89.5, 89.5 +dlat*0.5,  dlat)
a1lon   = arange(0.5,   359.5 +dlon*0.5, dlon)
#----------------------------

dpgradrange   = ctrack_para.ret_dpgradrange()
lclass  = dpgradrange.keys()
nclass  = len(lclass)
thpgrad = dpgradrange[1][0] 
#----------------------------
lllat   = -80.0
urlat   = 80.0
lllon   = 0.0
urlon   = 360.0
#----------------------------
for expr,model in [[expr, model] for expr in lexpr for model in lmodel]:
  #----
  ens   = cmip_para.ret_ens(model, expr, "psl")
  sunit, scalendar = cmip_para.ret_unit_calendar(model,expr)
  #----
  #thsst    = 273.15 + 25.0
  #thwind   = 0.0 #m/s 
  #thrvort  = 7.0e-5
  #thwcore  = 0.5  # (K)
  thsst    = tc_para.ret_thsst()
  thwind   = tc_para.ret_thwind()
  thrvort  = tc_para.ret_thrvort(model)
  thwcore  = tc_para.ret_thwcore(model)
  
  plev_low = 850*100.0 # (Pa)
  plev_mid = 500*100.0 # (Pa)
  plev_up  = 250*100.0 # (Pa)

  tplev_low = 850*100.0
 
  psldir_root     = "/media/disk2/data/CMIP5/sa.one.%s.%s/psl"%(model,expr)
  pgraddir_root   = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/pgrad"%(model,expr)
  lifedir_root    = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/life"%(model,expr)
  lastposdir_root = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/lastpos"%(model,expr)
  iposdir_root    = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/ipos"%(model,expr)
  nextposdir_root = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/nextpos"%(model,expr)
  #
  tdir_root       = "/media/disk2/data/CMIP5/sa.one.%s.%s/ta"%(model,expr)
  udir_root       = "/media/disk2/data/CMIP5/sa.one.%s.%s/ua"%(model,expr)
  vdir_root       = "/media/disk2/data/CMIP5/sa.one.%s.%s/va"%(model,expr)
  #
  sstdir_root     = "/media/disk2/data/CMIP5/sa.one.%s.%s/ts"%(model,expr)
  #
  sodir_root      = "/media/disk2/out/obj.valid/tc.tracklines.cmip5"
  sodir           = sodir_root + "/%04d-%04d"%(iyear,eyear)
  ctrack_func.mk_dir(sodir)
  #** land sea mask -------------------
  landseadir      = "/media/disk2/data/CMIP5/sa.one.%s.%s/sftlf"%(model,expr)
  landseaname     = landseadir + "/sftlf.%s.sa.one"%(model)
  a2landsea       = fromfile(landseaname, float32).reshape(ny,nx)
  a2landsea       = ma.masked_greater(a2landsea, 0.0).filled(1.0) 

  #************************************
  dtrack     = {}
  for iclass in lclass:
    dtrack[iclass] = []
  #-------
  a2lastflag      = ones([ny,nx], float32)*miss
  initflag        = -1

  #*****************************************
  # Time Loop
  #*****************************************
  a1dtime,a1tnum  = cmip_func.ret_times(iyear,eyear,lmon,sunit,scalendar,stepday)
  for dtime, tnum in map(None, a1dtime, a1tnum):
    year,mon,day,hour = dtime.year, dtime.month, dtime.day, dtime.hour
    print "tcline",year,mon,day,hour
    #-- init --
    #sodir  = sodir_root + "/%04d/%02d"%(year,mon)
    #ctrack_func.mk_dir(sodir)
    a2num  = zeros([ny,nx],float32).reshape(ny,nx)
    ##############
    #  SST
    #-------------
    sstdir   = sstdir_root + "/%04d"%(year)
    sstname  = sstdir + "/ts.%s.%04d%02d000000.sa.one"%(ens, year, mon)
    a2sst    = fromfile( sstname, float32).reshape(ny,nx)
    #-------------
    initflag        = initflag + 1
    stime  = "%04d%02d%02d%02d00"%(year, mon, day, hour)
    #
    pgraddir        = pgraddir_root   + "/%04d%02d"%(year, mon)
    lifedir         = lifedir_root    + "/%04d%02d"%(year, mon)
    iposdir         = iposdir_root    + "/%04d%02d"%(year, mon)
    lastposdir      = lastposdir_root + "/%04d%02d"%(year, mon)
    nextposdir      = nextposdir_root + "/%04d%02d"%(year, mon)
    tdir            = tdir_root       + "/%04d%02d"%(year, mon)
    udir            = udir_root       + "/%04d%02d"%(year, mon)
    vdir            = vdir_root       + "/%04d%02d"%(year, mon)
    #
    pgradname       = pgraddir   + "/pgrad.%s.%s.sa.one"%(ens, stime)
    lifename        = lifedir    + "/life.%s.%s.sa.one"%(ens, stime)
    nextposdir      = nextposdir_root + "/%04d%02d"%(year, mon)
    iposname        = iposdir    + "/ipos.%s.%s.sa.one"%(ens, stime)
    lastposname     = lastposdir + "/lastpos.%s.%s.sa.one"%(ens, stime)
    nextposname     = nextposdir + "/nextpos.%s.%s.sa.one"%(ens, stime)
    tlowname        = tdir       + "/ta.%04dhPa.%s.%s.sa.one"%(plev_low*0.01, ens, stime)
    tmidname        = tdir       + "/ta.%04dhPa.%s.%s.sa.one"%(plev_mid*0.01, ens, stime)
    tupname         = tdir       + "/ta.%04dhPa.%s.%s.sa.one"%(plev_up *0.01, ens, stime)
    ulowname        = udir       + "/ua.%04dhPa.%s.%s.sa.one"%(plev_low*0.01, ens, stime)
    uupname         = udir       + "/ua.%04dhPa.%s.%s.sa.one"%(plev_up *0.01, ens, stime)
    vlowname        = vdir       + "/va.%04dhPa.%s.%s.sa.one"%(plev_low*0.01, ens, stime)
    vupname         = vdir       + "/va.%04dhPa.%s.%s.sa.one"%(plev_up *0.01, ens, stime)
    #
    a2pgrad         = fromfile(pgradname, float32).reshape(ny, nx)
    a2life          = fromfile(lifename,  int32).reshape(ny, nx)
    a2ipos          = fromfile(iposname,  int32).reshape(ny, nx)
    a2lastpos       = fromfile(lastposname,int32).reshape(ny, nx)
    a2nextpos       = fromfile(nextposname,  int32).reshape(ny, nx)
  
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
  
    #tout_old        = ctrack_fsub.find_tc_saone_old(\
    #                  a2pgrad.T, a2life.T, a2lastpos.T, a2lastflag.T, a2tlow.T, a2tmid.T, a2tup.T, a2ulow.T, a2uup.T, a2vlow.T, a2vup.T, a2sst.T, a2landsea.T\
    #                , thpgrad, thdura, thsst, thwind, thrvort, initflag, miss)
  
  
  
    #
    a2tcloc         = tout[0].T
    a2lastflag      = tout[1].T
    #
    a2tcloc  = ma.masked_less(a2tcloc, thwcore).filled(miss)
    a2tcloc  = ma.masked_not_equal(a2tcloc, miss).filled(1.0)
    a2tcloc  = ma.masked_equal(a2tcloc, miss).filled(0.0)
    #******************
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

#************************
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
stitle = "CMIP TCobj res=%s %04d-%04d %s %02dh wc:%3.1f\n"%(model, iyear, eyear, season, thdura, thwcore)
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


#-- save --------------------
print "save"
#soname  = sodir + "/tclines.%04d-%04d.%s.%02dh.%3.2f.png"%(iyear, eyear,season, thdura, thwcore)
soname  = sodir + "/cmip.tclines.%s.%04d-%04d.%s.%02dh.wc%3.2f.sst%d.wind%d.vor%.1e.tplow%d.pup%d.png"%(model, iyear, eyear,season, thdura, thwcore, thsst -273.15, thwind, thrvort, tplev_low*0.01, plev_up*0.01)
plt.savefig(soname)
plt.clf()
print soname
plt.clf()

#----------------------------





