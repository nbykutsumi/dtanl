from numpy import *
from dtanl_fsub import *
import calendar
import ctrack_fig
import ctrack_para
import ctrack_func
import gsmap_func
from ctrack_fsub import *
from mpl_toolkits.basemap import Basemap
import matplotlib
import matplotlib.pyplot as plt
from cf.plot import *

#----------------------------------------------------
#singleday =True
singleday = False
iyear = 2004
eyear = 2004
#lseason = [1,2,3,4,5,6,7,8,9,10,11,12]
lseason = [1]

dist_km = 300.0 #(km)
#dist_mask = 700.  # (km)
dist_mask = 0.  # (km)

lftype = [1,2,4]
#lftype = [2]

iday  = 1
ny    = 180
nx    = 360
lhour = [0,6,12,18]
#lhour = [0]

lllat = 10.0
lllon = 120
urlat = 60
urlon = 210

#lllat = 0.0
#lllon = 90.0
#urlat = 90.0
#urlon = 140.0

#lllat = 0.0
#lllon = 140.0
#urlat = 80.0
#urlon = 210.0



plev  = 850*100.0
#-----
miss  = -9999.0
chartdir_root = "/media/disk2/out/chart/ASAS/front"
tdir_root     = "/media/disk2/data/JRA25/sa.one/6hr/TMP"
qdir_root     = "/media/disk2/data/JRA25/sa.one/6hr/SPFH"
#------------------------
#************************
lat_first     = -89.5
dlat          = 1.0
dlon          = 1.0
#------------------------
for season in lseason:
  lmon     = ctrack_para.ret_lmon(season)
  #------------------------
  for year in range(iyear, eyear+1):
    for mon in lmon:
      print season, year, mon
      #------------------------
      if singleday ==True:
        eday = iday
      else:
        eday = calendar.monthrange(year,mon)[1]
      #----------------
      for day in range(iday, eday+1):
        for hour in lhour:
          chartdir  = chartdir_root + "/%04d%02d"%(year,mon)
          tdir      = tdir_root     + "/%04d%02d"%(year,mon)
          qdir      = qdir_root     + "/%04d%02d"%(year,mon)
          #
          chartname = chartdir      + "/front.ASAS.%04d.%02d.%02d.%02d.saone"%(year,mon,day,hour)
          tname     = tdir          + "/anal_p25.TMP.0850hPa.%04d%02d%02d%02d.sa.one"%(year,mon,day,hour)
          qname     = qdir          + "/anal_p25.SPFH.0850hPa.%04d%02d%02d%02d.sa.one"%(year,mon,day,hour)
          a2chart   = fromfile(chartname, float32).reshape(ny,nx)
          a2t       = fromfile(tname,     float32).reshape(ny,nx)
          a2q       = fromfile(qname,     float32).reshape(ny,nx)
          a2tv      = a2t * (1.0+0.61*a2q)
          a2theta   = dtanl_fsub.mk_a2theta_e(plev, a2t.T, a2q.T).T
          a2gradt   = dtanl_fsub.mk_a2grad_abs_saone(a2t.T).T
          a2gradtv  = dtanl_fsub.mk_a2grad_abs_saone(a2tv.T).T
          a2gradtheta=dtanl_fsub.mk_a2grad_abs_saone(a2theta.T).T 
          #-- load precipitation ----------
          a2pr      = gsmap_func.timeave_gsmap_backward_saone(year,mon,day,hour+1, 2)
          a2pr      = gsmap_func.gsmap2global_one(a2pr, miss) 
          a2pr      = (ma.masked_equal(a2pr, miss)*60.*60.).filled(miss)
          #***********************************
          ##-- maskout fronts close to other front type ----
          #a2chart_others     = ma.masked_equal(a2chart, ftype).filled(miss)
          #a2terr_others      = ctrack_fsub.mk_territory_saone(a2chart_others.T, dist_mask*1000., miss, lat_first, dlat, dlon).T
          ##-- make chart_seg ------------------------------
          #a2chart_seg        = ma.masked_not_equal(a2chart, ftype).filled(miss)
          #a2chart_seg        = ma.masked_where(a2terr_others !=miss, a2chart_seg).filled(miss)

          a2chart_seg         = a2chart
          #--------------------
          #** Precipitation ***********
          # Caution!
          # the warmer side is the lower side of the grad-theta
          #a2vecx, a2vecy     = ctrack_fsub.mk_a2highsidevector_saone(-a2gradtheta.T, a2chart_seg.T, dist_km*1000.0, miss)
          a2vecx, a2vecy     = ctrack_fsub.mk_a2highsidevector_saone(a2tv.T, a2chart_seg.T, dist_km*1000.0, miss)
          a2vecx             = a2vecx.T
          a2vecy             = a2vecy.T

          #** ready for drawing *******
          plt.clf()
          a1lat    = arange(-89.5, 89.5   + dlat*0.1, dlat)
          a1lon    = arange(0.5,   359.5  + dlon*0.1, dlon)
          #
          xdom_saone_first = int((lllon - 0.5 + 0.5)/1.0)
          xdom_saone_last  = int((urlon - 0.5 + 0.5)/1.0)
          ydom_saone_first = int((lllat -(-89.5) + 0.5)/1.0)
          ydom_saone_last  = int((urlat -(-89.5) + 0.5)/1.0)

          #----------------------------
          # Basemap
          #----------------------------
          figmap    = plt.figure()
          axmap     = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
          M         = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)

          #-- transform ---------------
          a2pr_trans     = a2pr[ydom_saone_first:ydom_saone_last+1,    xdom_saone_first:xdom_saone_last+1].copy()
          a2chart_trans  = a2chart[ydom_saone_first:ydom_saone_last+1, xdom_saone_first:xdom_saone_last+1].copy()
          a2vecx_trans   = a2vecx[ydom_saone_first:ydom_saone_last+1,  xdom_saone_first:xdom_saone_last+1].copy()
          a2vecy_trans   = a2vecy[ydom_saone_first:ydom_saone_last+1,  xdom_saone_first:xdom_saone_last+1].copy()

          #-- bnd and color ------------
          mycm       = "copper_r"
          bnd        = list(arange(0.0, 0.7, 0.02))
          bnd_cbar   = [-1.0e+40] + bnd + [1.0e+40]
          cminst     = matplotlib.cm.get_cmap(mycm, len(bnd))
          acm        = cminst( arange( len(bnd) ) )
          lcm        = [[1,1,1,1]]+ acm.tolist()
          mycm       = matplotlib.colors.ListedColormap( lcm )          
 

          #** imshow precipitation ******
          a2pr_trans    = ma.masked_less_equal(a2pr_trans, 0.0).filled(miss)
          im            = M.imshow(a2pr_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")

          #** imshow shade ******
          a2shade_trans = a2pr_trans 
          a2shade_trans = ma.masked_not_equal(a2shade_trans, miss)
          cmshade       = matplotlib.colors.ListedColormap([(0.8,0.8,0.8), (0.8,0.8,0.8)])
          im            = M.imshow(a2shade_trans, origin="lower", cmap=cmshade, interpolation="nearest")

          #** imshow chart ******
          a2chart_trans[0,0]=1.
          a2chart_trans[0,1]=2.
          a2chart_trans[0,2]=3.
          a2chart_trans[0,3]=4.
          a2chart_trans = ma.masked_equal(a2chart_trans, miss)
          im            = M.imshow(a2chart_trans, origin="lower", cmap="gist_rainbow", interpolation="nearest")

          #** vector ************
          a1lon_loc  = linspace(a1lon[xdom_saone_first], a1lon[xdom_saone_last], xdom_saone_last -xdom_saone_first +1 )
          a1lat_loc  = linspace(a1lat[ydom_saone_first], a1lat[ydom_saone_last], ydom_saone_last -ydom_saone_first +1 )
          LONS, LATS = meshgrid( a1lon_loc, a1lat_loc)
          #

          a2vecx_trans = ma.masked_equal(a2vecx_trans, miss)
          a2vecy_trans = ma.masked_equal(a2vecy_trans, miss)

          #im         = M.quiver(LONS, LATS, a2vecx_trans, a2vecy_trans, angles="xy", color="k", units="height", scale=80.)
          im         = M.quiver(LONS, LATS, a2vecx_trans, a2vecy_trans, angles="xy", color="k", units="height", scale=20.)
          #im         = M.quiver(LONS, LATS, a2vecx_trans, a2vecy_trans, angles="xy", color="k", units="height", scale=280000*30.)
          #im         = M.quiver(LONS, LATS, a2vecx_trans, a2vecy_trans, angles="xy", color="k", units="height", scale=280000*5.)


          #-- coastline ---------------
          print "coastlines"
          M.drawcoastlines()
        
          #-- meridians and parallels
          parallels = arange(-90.,90,10.)
          M.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
        
          meridians = arange(0.,360.,10.)
          M.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10,rotation=90) 

          #-- title -------------------
          axmap.set_title("%04d-%02d-%02d-%02d"%(year,mon,day,hour))

          #-- save --------------------
          figname = "/media/disk2/temp/highside/chart.highside.%04d.%02d.%02d.%02d.png"%(year,mon,day,hour)
          plt.savefig(figname)
          print figname
