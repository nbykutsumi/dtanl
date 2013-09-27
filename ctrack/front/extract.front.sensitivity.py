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
import os, sys
from cf.plot import *
import datetime
#***************************************
singleday = True
#singleday = False
region   = "ASAS"
#--------------------------
if len(sys.argv) >1:
  iyear   = int(sys.argv[1])
  lyear   = [iyear]
else:
  #lyear    = [2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011]
  #lyear    = [2006,2007,2008,2009,2010,2011]
  #lyear    = [2000,2001,2002,2003]
  lyear    = [2004]
#--------------------------
#lmon     = [1,2,3,4,5,6,7,8,9,10,11,12]
lmon     = [1]
#lmon     = [10,11,12]
#lmon     = [1]
iday     = 11
#lhour    = [6]
#lhour    = [0, 6,12, 18]
lhour    = [0]
#
lthaa    = [2,4,7,10]
lthbb    = [3]
lthcc    = [1,3,9]
#llflagth     = [[0,0,0,0],[1,1,1,1],[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]]
#llflagth     = [[0,0,0,0],[1,1,1,1],[0,1,1,1],[1,0,1,1],[1,1,0,1],[1,1,1,0]]
#llflagth     = [[0,0,1,1],[0,1,0,1],[0,1,1,0]]
llflagth     = [[1,1,1,1]]
llflagnum    = [[1,1,1,1]]
#---------------------------------------
#pdfdir_root = "/home/utsumi/mnt/export/nas_d/data/WeatherChart"
pdfdir_root = "/media/disk2/data/JMAChart/ASAS"
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
    #-----
    eday    = calendar.monthrange(year, mon)[1]
    #-----
    if singleday == True:
      eday = iday
    #-----
    for day in range(iday,eday+1):
      #--------
      for hour in lhour:
        #-----
        if ((year==lyear[0])&(mon==lmon[0])&(day==iday)&(hour==lhour[0])):
          cbarflag = True
        else:
          cbarflag = False
        #-----
        jpgname  = "/media/disk2/temp/chart/sens"  + "/As_%04d%02d%02d%02d.jpg"%(year,mon,day,hour)

        pdfname1 = pdfdir + "/As_%04d%02d%02d%02d.pdf"%(year,mon,day,hour)
        pdfname2 = pdfdir + "/AS_%04d%02d%02d%02d.PDF"%(year,mon,day,hour)
        pdfname3 = pdfdir + "/As_%04d%02d%02d%02d.PDF"%(year,mon,day,hour)
        pdfname4 = pdfdir + "/AS_%04d%02d%02d%02d.pdf"%(year,mon,day,hour)

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
        a2mask   = ma.masked_where(a2r < 145, a2one)
        a2mask   = ma.masked_where(a2g > 23, a2mask)
        a2mask   = ma.masked_where(a2b > 23, a2mask)
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
        #a2mask   = ma.masked_where(a2r < 160, a2one)
        #a2mask   = ma.masked_where(a2g > 80, a2mask)
        #a2mask   = ma.masked_where(a2b < 160, a2mask)

        a2mask   = ma.masked_where(a2r < 120, a2one)
        a2mask   = ma.masked_where(a2g > 80, a2mask)
        a2mask   = ma.masked_where(a2b < 160, a2mask)

        a2mask   = a2mask.filled(miss)
        a2front  = ma.masked_where(a2mask != miss, a2front).filled(3.0)

        #** remove jpg file ********************
        os.remove(jpgname)
 
        
        #---- EXTRACT -----
        for lflagth in llflagth:      
          fa,fb,fc,fe = lflagth

          for lflagnum in llflagnum:
            f1,f2,f3,f4 = lflagnum 
    

            #odir_root   = "/media/disk2/temp/chart/sens/fth.%s.%s.%s.%s/fnum.%s.%s.%s.%s"%(fa,fb,fc,fe,f1,f2,f3,f4)
            odir_root   = "/media/disk2/temp/chart/sens/flags"
            odir    = odir_root + "/%02d.%02d"%(mon,day)
            figdir  = odir_root + "/%02d.%02d/fig"%(mon,day)
            bnname   = odir   + "/front.ASAS.%04d.%02d.%02d.%02d.sa.one"%(year,mon,day,hour)
            ctrack_func.mk_dir(odir)
            ctrack_func.mk_dir(figdir)



            llths = [[thaa,thbb,thcc]\
                   for thaa in lthaa\
                   for thbb in lthbb\
                   for thcc in lthcc]
            for lths in llths:
              thaa,thbb,thcc = lths  
              thee  = thaa - 1

              a2front_saone = chart_fsub.chartfront2saone_test(\
                                a2front.T, a2xfort_corres.T, a2yfort_corres.T,\
                                miss,\
                                f1,f2,f3,f4,fa,fb,fc,fe,\
                                thaa,thbb,thcc,thee).T
      
      
              #a2front_saone = chart_fsub.chartfront2saone_new(\
              #                  a2front.T, a2xfort_corres.T, a2yfort_corres.T,\
              #                  miss).T
      
      
              a2front_saone.tofile(bnname)
              print bnname
             
              #** draw saone fronts ******************
              # preparation #
              plt.clf()
      
              # color band #
              #col = matplotlib.colors.ListedColormap(["white", "red", (0,102./255.,1), (204/255.,102/255.,255/255.),"orange"])
              #col = matplotlib.colors.ListedColormap(["white", "red", "blue", (204/255.,0/255.,255/255.),"orange"])
              #col = matplotlib.colors.ListedColormap(["white", (255/255., 51/255., 0), (0,102/255.,1), "purple", "orange" ])
              col = matplotlib.colors.ListedColormap(["white", (255/255., 51/255., 0), (0,153/255.,1), (153/255., 0, 153/255.), "orange" ])
              col = matplotlib.colors.ListedColormap(["white", (255/255., 30/255., 0), (0,153/255.,1), (153/255., 0, 153/255.), "orange" ])
              #col = "spectral"
              bnd = [-1.0e+10, 0.5, 1.5, 2.5, 3.5, 4.5]
      
              # Basemap #
              figmap = plt.figure(figsize=(8,8))
              axmap  = figmap.add_axes([0.1,0.1,0.8,0.8])
      
              # rectangular projection -------------------------
              lllon_rect, lllat_rect, urlon_rect, urlat_rect \
                         = chart_para.ret_domain_corner_rect(region)
              xdom_saone_first, xdom_saone_last, ydom_saone_first, ydom_saone_last = chart_para.ret_xydom_saone_rect_first_last(region)
              #M   = Basemap( resolution="l", llcrnrlat=lllat_rect-0.5, llcrnrlon=lllon_rect-0.5, urcrnrlat=urlat_rect+0.5, urcrnrlon=urlon_rect+0.5, ax=axmap)
              M   = Basemap( resolution="l", llcrnrlat=lllat_rect, llcrnrlon=lllon_rect, urcrnrlat=urlat_rect, urcrnrlon=urlon_rect, ax=axmap)
              # transform #
              a2front_saone_trans  = a2front_saone[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]
      
              # draw data #
              im  = M.imshow(a2front_saone_trans, norm=BoundaryNormSymm(bnd), cmap=col, interpolation="nearest")
      
              # sahde #
              a2shade_trans        = a2domain_mask[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]
              a2shade_trans        = ma.masked_not_equal(a2shade_trans, 0.0)
              cmshade              = matplotlib.colors.ListedColormap([(0.8, 0.8, 0.8), (0.8, 0.8, 0.8)])
              im                   = M.imshow(a2shade_trans, origin="lower", cmap=cmshade)
      
              # coastlines #
              M.drawcoastlines()
      
              # draw parallels #
              parallels = arange(0.,90,10.)
              M.drawparallels(parallels,labels=[1,0,0,0],fontsize=10)
      
              # draw meridians #
              meridians = arange(0.,360.,10.)
              M.drawmeridians(meridians,labels=[0,0,0,1],fontsize=10)
      
              # title #
              stitle  = "fth.%s.%s.%s.%s. fnum.%s.%s.%s.%s\n"%(fa,fb,fc,fe,f1,f2,f3,f4)
              stitle  = stitle + "a:%s b:%s c:%s e:%s  "%(thaa,thbb,thcc,thee)
              stitle  = stitle + "%04d-%02d-%02d %02d UTC"%(year,mon,day,hour)
              axmap.set_title(stitle)
      
              # save fig
              #ofigname= figdir + "/front.ASAS.%04d.%02d.%02d.%02d.png"%(year,mon,day,hour)
              ofigname= figdir + "/front.ASAS.thf.%s.%s.%s.%s.thnum.%s.%s.%s.%s.a-%s.b-%s.c-%s.e-%s.png"%(fa,fb,fc,fe,f1,f2,f3,f4,thaa,thbb,thcc,thee)
              plt.savefig(ofigname)
              print ofigname
      
              ## colorbar #
              #if cbarflag == True:
              #  plt.clf()
              #  im        = imshow(a2front_saone, norm=BoundaryNormSymm(bnd), cmap=col)
              #  figcbar   = plt.figure(figsize=(5,0.6))                  
              #  axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
              #  plt.colorbar(im, boundaries=bnd, cax=axcbar, orientation="horizontal")
              #  cbarname = figdir + "/front.%s.cbar.png"%(region)
              #  figcbar.savefig(cbarname)
