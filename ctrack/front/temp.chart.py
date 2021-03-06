from mpl_toolkits.basemap import Basemap, cm
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import chart_para
import ctrack_func
from numpy import *
from chart_fsub import *
import calendar
import subprocess
import os
from cf.plot import *
import datetime
#***************************************
region   = "ASAS"
lyear    = [2004]
lmon     = [1]
iday     = 29
lhour    = [6]
#---------------------------------------
#pdfdir_root = "/home/utsumi/mnt/export/nas_d/data/WeatherChart"
pdfdir_root = "/media/disk2/data/JMAChart/ASAS"
odir_root   = "/media/disk2/out/chart/ASAS/front"
xydatadir   = "/media/disk2/out/chart/ASAS/const"

miss     = -9999.0

#-- domain mask ----------------------------

#-------------------------------------------
for year in lyear:
  for mon in lmon:
    #----- parameter -------------------------
    #-- x and y data -----
    nx_fig,ny_fig    = chart_para.ret_nxnyfig(region, year, mon)
    paradate      = datetime.date(year,mon,1)
    #----
    if region == "ASAS":
      if (paradate < datetime.date(2006,1,1)):
        name_x_corres = xydatadir + "/stereo.xfort.fig2saone.ASAS.2000.01.bn"
        name_y_corres = xydatadir + "/stereo.yfort.fig2saone.ASAS.2000.01.bn"
        name_domain_mask = xydatadir + "/domainmask_saone.%s.2000.01.bn"%(region)

      if ( datetime.date(2006,1,1)<=paradate<datetime.date(2006,3,1)):
        name_x_corres = xydatadir + "/stereo.xfort.fig2saone.ASAS.2006.01.bn"
        name_y_corres = xydatadir + "/stereo.yfort.fig2saone.ASAS.2006.01.bn"
        name_domain_mask = xydatadir + "/domainmask_saone.%s.2006.01.bn"%(region)

      if ( datetime.date(2006,3,1)<=paradate):
        name_x_corres = xydatadir + "/stereo.xfort.fig2saone.ASAS.2006.03.bn"
        name_y_corres = xydatadir + "/stereo.yfort.fig2saone.ASAS.2006.03.bn"
        name_domain_mask = xydatadir + "/domainmask_saone.%s.2006.03.bn"%(region)
    #----
    a2xfort_corres   = fromfile(name_x_corres, float32).reshape(ny_fig, nx_fig)
    a2yfort_corres   = fromfile(name_y_corres, float32).reshape(ny_fig, nx_fig)
    a2domain_mask    = fromfile(name_domain_mask,float32).reshape(180,360)
    #-----------------------------------------
    #pdfdir  = pdfdir_root + "/%04d%02d/PDFDATA/ASMAP"%(year, mon)
    pdfdir = pdfdir_root + "/%04d%02d"%(year, mon)
    odir    = odir_root   + "/%04d%02d"%(year,mon)
    figdir  = odir_root   + "/%04d%02d/fig"%(year,mon)
    ctrack_func.mk_dir(odir)
    ctrack_func.mk_dir(figdir)
    #-----
    #eday    = calendar.monthrange(year, mon)[1]
    eday = iday
    for day in range(iday,eday+1):
      for hour in lhour:
        #-----
        if ((year==lyear[0])&(mon==lmon[0])&(day==iday)&(hour==lhour[0])):
          cbarflag = True
        else:
          cbarflag = False
        #-----
        pdfname1 = pdfdir + "/As_%04d%02d%02d%02d.pdf"%(year,mon,day,hour)
        pdfname2 = pdfdir + "/AS_%04d%02d%02d%02d.PDF"%(year,mon,day,hour)
        pdfname3 = pdfdir + "/As_%04d%02d%02d%02d.PDF"%(year,mon,day,hour)
        pdfname4 = pdfdir + "/AS_%04d%02d%02d%02d.pdf"%(year,mon,day,hour)
        jpgname  = odir   + "/As_%04d%02d%02d%02d.jpg"%(year,mon,day,hour)
        #bnname   = odir   + "/front.ASAS.%04d.%02d.%02d.%02d.saone"%(year,mon,day,hour)
        #ofigname= figdir + "/front.ASASll.%04d.%02d.%02d.%02d.png"%(year,mon,day,hour)
        bnname   = "./test.chart.sa.one" 
        ofigname = "./test.chart.png"

        #** convert pdf --> jpg and read jpg *************
        if os.access(pdfname1, os.F_OK):
          pdfname = pdfname1
        elif os.access(pdfname2, os.F_OK):
          pdfname = pdfname2
        elif os.access(pdfname3, os.F_OK):
          pdfname = pdfname3
        elif os.access(pdfname4, os.F_OK):
          pdfname = pdfname4
        else:
          print "no files", pdfname1
          print "no files", pdfname2
          print "no files", pdfname3
          print "no files", pdfname4
          sys.exit()
        
        #scmd = "convert -resize 1300x900 %s %s"%(pdfname, jpgname) # do not change size for ASAS
        scmd = "convert %s %s"%(pdfname, jpgname)
        print scmd
        subprocess.call(scmd, shell=True)
        a2jpg     = mpimg.imread(jpgname)

        #** extract fronts ******************
        #---------------------------------------
        a2one    = ones([ny_fig,nx_fig],float32)
        a2r      = a2jpg[:,:,0]
        a2g      = a2jpg[:,:,1]
        a2b      = a2jpg[:,:,2]
        
        a2front  = a2one*miss
        #-- warm front ----
        a2mask   = ma.masked_where(a2r < 130, a2one)
        a2mask   = ma.masked_where(a2g > 30, a2mask)
        a2mask   = ma.masked_where(a2b > 30, a2mask)
        a2mask   = a2mask.filled(miss)
        a2front  = ma.masked_where(a2mask != miss, a2front).filled(1.0)
        
        ##-- cold front ----
        a2mask   = ma.masked_where(a2r > 30, a2one)
        a2mask   = ma.masked_where(a2g > 30, a2mask)
        a2mask   = ma.masked_where(a2b < 110, a2mask)
        a2mask   = a2mask.filled(miss)
        a2front  = ma.masked_where(a2mask != miss, a2front).filled(2.0)
        #
        ##-- occ front
        a2mask   = ma.masked_where(a2r < 160, a2one)
        a2mask   = ma.masked_where(a2g > 80, a2mask)
        a2mask   = ma.masked_where(a2b < 160, a2mask)
        a2mask   = a2mask.filled(miss)
        a2front  = ma.masked_where(a2mask != miss, a2front).filled(3.0)
        
        #--
        a2front_saone = chart_fsub.chartfront2saone_new(\
                          a2front.T, a2xfort_corres.T, a2yfort_corres.T,\
                          miss).T
        a2front_saone.tofile(bnname)
        print bnname
        #** remove jpg file ********************
        os.remove(jpgname)
        
        #** draw saone fronts ******************
        # preparation #
        plt.clf()

        # color band #
        col = matplotlib.colors.ListedColormap(["white", "red", "blue", "purple","orange"])
        #col = "spectral"
        bnd = [-1.0e+10, 0.5, 1.5, 2.5, 3.5, 4.5]

        # Basemap #
        figmap = plt.figure(figsize=(8,8))
        axmap  = figmap.add_axes([0.1,0.1,0.8,0.8])

        # rectangular projection -------------------------
        lllon_rect, lllat_rect, urlon_rect, urlat_rect \
                   = chart_para.ret_domain_corner_rect(region)
        xdom_saone_first, xdom_saone_last, ydom_saone_first, ydom_saone_last = chart_para.ret_xydom_saone_rect_first_last(region)
        #M   = Basemap( resolution="l", llcrnrlat=lllat_rect+2.0, llcrnrlon=lllon_rect, urcrnrlat=urlat_rect+2.0, urcrnrlon=urlon_rect, ax=axmap)
        M   = Basemap( resolution="l", llcrnrlat=lllat_rect-0.5, llcrnrlon=lllon_rect-0.5, urcrnrlat=urlat_rect+0.5, urcrnrlon=urlon_rect+0.5, ax=axmap)
        # transform #
        a2front_saone_trans  = a2front_saone[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]

        # draw data #
        im  = M.imshow(a2front_saone_trans, norm=BoundaryNormSymm(bnd), cmap=col, interpolation="nearest")

        # sahde #
        a2shade_trans        = a2domain_mask[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]
        a2shade_trans        = ma.masked_not_equal(a2shade_trans, 0.0)
        cmshade              = matplotlib.colors.ListedColormap([(0.8, 0.8, 0.8), (0.8, 0.8, 0.8)])
        im                   = M.imshow(a2shade_trans, origin="lower", cmap=cmshade)

        ## stereo projection -------------------------
        #lon0,lat0  = chart_para.ret_lonlat_center(region)
        #latts      = chart_para.ret_latts(region)
        #lllon, lllat, urlon, urlat \
        #           = chart_para.ret_domain_corner(region)
        #M   = Basemap(projection="stere", lon_0=lon0, lat_0=lat0, lat_ts=latts,\
        #            llcrnrlat=lllat, urcrnrlat=urlat, llcrnrlon=lllon, urcrnrlon=urlon,\
        #            rsphere=6371200.,resolution="l",area_thresh=10000)
        ## transform #
        #a2front_saone        = ma.masked_equal(a2front_saone, miss).filled(0.0)
        #a2front_saone        = c_[ a2front_saone[:,180:360], a2front_saone[:,0:180] ]
        #a1lon = arange(-179.5, 179.5+0.5, 1.0)
        #a1lat = arange(-89.5, 89.5+0.5, 1.0)
        #a2front_saone_trans  = M.transform_scalar( a2front_saone, a1lon, a1lat, 900, 800)
        #a2zero_saone_trans   = a2front_saone_trans * 0.0
        #a2front_saone_trans_temp = ma.masked_where( (0.9<a2front_saone_trans)&(a2front_saone_trans<1.1), a2zero_saone_trans).filled(1.0)
        #a2front_saone_trans      = a2front_saone_trans_temp
        #
        ## draw data #
        #im  = M.imshow(a2front_saone_trans, norm=BoundaryNormSymm(bnd), cmap=col, interpolation="nearest")

        # coastlines #
        M.drawcoastlines()

        # draw parallels #
        parallels = arange(0.,90,10.)
        M.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)

        # draw meridians #
        meridians = arange(0.,360.,10.)
        M.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)

        # title #
        stitle  = "%04d-%02d-%02d %02d UTC"%(year,mon,day,hour)
        axmap.set_title(stitle)

        # save fig
        plt.savefig(ofigname)
        print ofigname

        ## colorbar #
        #if cbarflag == True:
        #  plt.clf()
        #  im        = imshow(a2front_saone, norm=BoundaryNormSymm(bnd), cmap=col)
        #  figcbar   = plt.figure(figsize=(5,0.6))                  
        #  axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
        #  plt.colorbar(im, boundaries=bnd, cax=axcbar, orientation="horizontal")
        #  #cbarname = figdir + "/front.%s.cbar.png"%(region)
        #  cbarname = "./cbar.png"
        #  figcbar.savefig(cbarname)
