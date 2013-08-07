from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib
from numpy import *
import calendar
import ctrack_para
import ctrack_func
import sys, os
import gsmap_func
from cf.plot import *
import datetime
from dtanl_fsub import *
from ctrack_fsub import *
#-----------------------
singletime = True
#singletime = False

#lftype = ["t","q"]
lftype = ["q"]
lyear  = [2004]
#lmon   = [1,4,6,7]
lmon   = [7]
iday   = 6
hour  = 0

thgrids  = 7
resol    = "anl_p"

#--------
ny,nx  = 180,360

#-- mask thresholds ---
thfmask1t = 0.3   # sample for "t"
thfmask2t = 1.0   # sample for "t"

thfmask1q = 2.6 *1.0e-4  # sample for "q"
thfmask2q = 2.4 *1.0e-3  # sample for "q"

#-- for Berry et al.
#year  = 2001
#mon   = 11
#day   = 28
#hour  = 0

#local region ------
#corner points should be
#at the center of original grid box
lllat   = 0.
urlat   = 80.
lllon   = 70.
urlon   = 210.

##-- for Berry et al.
#lllat    = 0.0
#urlat    = 60.
#lllon    = 200.
#urlon    = 360.

#lllat    = 20.0
#urlat    = 60.0
#lllon    = 110.
#urlon    = 160.

plev     = 850 *100.0   #(Pa)
cbarflag = "True"
thdura   = 6
#-- init ---------

a2one    = ones([ny,nx],float32)

#-----------------
for year in lyear:
  for mon in lmon:
    #-------------
    if singletime==True:
      eday = iday 
    else:
      eday = calendar.monthrange(year,mon)[1]
    #-------------
    for day in range(iday,eday+1):
      for ftype in lftype:
        if ftype == "t":
          thfmask1   = thfmask1t    # sample for "t"
          thfmask2   = thfmask2t    # sample for "t"
        elif ftype   == "q":
          thfmask1   = thfmask1q    # sample for "q"
          thfmask2   = thfmask2q    # sample for "q"
        #-----------------------------
        #-----------------------------
        miss_out  = -9999.0
        ny  = 180
        nx  = 360
        highsidedist  = ctrack_para.ret_highsidedist()
        
        stime         = "%04d%02d%02d%02d"%(year, mon, day, hour)
        sodir         = "/home/utsumi/temp/tenkizu"
        cbardir       = sodir
        
        ctrack_func.mk_dir(sodir)
        
        dlat    = 1.0
        dlon    = 1.0
        a1lat   = arange(-89.5, 89.5  + dlat*0.1, dlat)
        a1lon   = arange(0.5,   359.5 + dlon*0.1, dlon)
        
        meridians = 10.0
        
        resol    = "anl_p"
        #-----------------------------
        #-----------------------------
        miss_out  = -9999.0
        ny  = 180
        nx  = 360
        highsidedist  = ctrack_para.ret_highsidedist()
        
        stime         = "%04d%02d%02d%02d"%(year, mon, day, hour)
        sodir         = "/home/utsumi/temp/tenkizu"
        cbardir       = sodir
        
        ctrack_func.mk_dir(sodir)
        
        dlat    = 1.0
        dlon    = 1.0
        a1lat   = arange(-89.5, 89.5  + dlat*0.1, dlat)
        a1lon   = arange(0.5,   359.5 + dlon*0.1, dlon)
        
        meridians = 10.0
        parallels = 10.0
        
        thorog  = ctrack_para.ret_thorog()
        thgradorog=ctrack_para.ret_thgradorog()
        #************************
        # for mapping
        nnx        = int( (urlon - lllon)/dlon)
        nny        = int( (urlat - lllat)/dlat)
        a1lon_loc  = linspace(lllon, urlon, nnx)
        a1lat_loc  = linspace(lllat, urlat, nny)
        LONS, LATS = meshgrid( a1lon_loc, a1lat_loc)
        
        xdom_saone_first = int((lllon - 0.5 + 0.5)/1.0)
        xdom_saone_last  = int((urlon - 0.5 + 0.5)/1.0)
        ydom_saone_first = int((lllat -(-89.5) + 0.5)/1.0)
        ydom_saone_last  = int((urlat -(-89.5) + 0.5)/1.0)
        
        #************************
        # FUNCTIONS
        #************************
        # front locator :contour
        #---------------
        def mk_front_loc_contour(a2thermo, a2gradthermo, thfmask1, thfmask2):
          a2fmask1 = dtanl_fsub.mk_a2frontmask1(a2thermo.T).T
          a2fmask2 = dtanl_fsub.mk_a2frontmask2(a2thermo.T).T
          a2fmask1 = a2fmask1 * (1000.0*100.0)**2.0  #[(100km)-2]
          a2fmask2 = a2fmask2 * (1000.0*100.0)       #[(100km)-1]
         
          (a2grad2x, a2grad2y) = dtanl_fsub.mk_a2grad_saone(a2gradthermo.T)
          a2grad2x = a2grad2x.T
          a2grad2y = a2grad2y.T
          a2loc    = dtanl_fsub.mk_a2axisgrad(a2grad2x.T, a2grad2y.T).T
          a2loc    = dtanl_fsub.mk_a2contour(a2loc.T, 0.0, 0.0, miss_out).T
          a2loc    = ma.masked_equal(a2loc, miss_out) 
          a2loc    = ma.masked_where(a2fmask1 < thfmask1, a2loc)
          a2loc    = ma.masked_where(a2fmask2 < thfmask2, a2loc)
          return a2loc
        
        #***************
        # drawing function
        #---------------
        def mk_regmap(a2in, bnd, scm, stitle, soname, cbarname, miss_out):
          #------------------------
          # Basemap
          #------------------------
          print "Basemap"
          figmap   = plt.figure()
          axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
          M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
          
          #-- transform -----------
          print "transform"
          #a2value_trans    = M.transform_scalar( a2in,   a1lon, a1lat, nnx, nny)
          a2value_trans    = a2in[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]
          #a2value_trans    = a2value_trans.filled(miss_out)
          #-- boundaries ----------
          bnd_cbar   = [-1.0e+40] + bnd + [1.0e+40]
          
          #-- color ---------------
          cminst   = matplotlib.cm.get_cmap(scm, len(bnd))
          acm      = cminst( arange( len(bnd) ) )
          lcm      = [[1,1,1,1]]+ acm.tolist()
          mycm     = matplotlib.colors.ListedColormap( lcm )
          
          #-- imshow    -----------
          im       = M.imshow(a2value_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")
        
          #-- shade     -----------
          a2shade_trans = ma.masked_not_equal(a2value_trans, miss_out)
          cmshade       = matplotlib.colors.ListedColormap([(0.8,0.8,0.8), (0.8,0.8,0.8)])
          im            = M.imshow(a2shade_trans, origin="lower", cmap=cmshade) 
          
          #-- coastline ---------------
          print "coastlines"
          M.drawcoastlines()
          
          #-- meridians and parallels
          M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1])
          M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0])
          #-- title -------------------
          axmap.set_title("%s"%(stitle))
          #-- save --------------------
          plt.savefig(soname)
          print soname 
          # for colorbar ---
          if cbarflag == "True":
            figmap   = plt.figure()
            axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
            M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
            a2v_trans    = M.transform_scalar( a2in,   a1lon, a1lat, nnx, nny)
            im       = M.imshow(a2value_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm)
          
            figcbar   = plt.figure(figsize=(5, 0.6))
            axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
            bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
            plt.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar, orientation="horizontal")
            figcbar.savefig(cbarname)
        
        #*************************************************
        def mk_regmap_contour(a2in, bnd, scm, stitle, soname, cbarname, miss_out):
          #------------------------
          # Basemap
          #------------------------
          print "Basemap"
          figmap   = plt.figure()
          axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
          M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
          
          #-- transform -----------
          print "transform"
          a2value_trans    = M.transform_scalar( a2in,   a1lon, a1lat, nnx, nny)
          a2value_trans    = a2value_trans.filled(miss_out)
        
          #-- to contour ----------
          a2value_trans    = dtanl_fsub.mk_a2contour_regional(a2value_trans.T, 0.0, 0.0, -9999.0).T
        
          #-- boundaries ----------
          bnd_cbar   = [-1.0e+40] + bnd + [1.0e+40]
          
          #-- color ---------------
          cminst   = matplotlib.cm.get_cmap(scm, len(bnd))
          acm      = cminst( arange( len(bnd) ) )
          lcm      = [[1,1,1,1]]+ acm.tolist()
          mycm     = matplotlib.colors.ListedColormap( lcm )
          
          #-- imshow    -----------
          im       = M.imshow(a2value_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")
        
          #-- shade     -----------
          a2shade_trans = ma.masked_not_equal(a2value_trans, miss_out)
          cmshade       = matplotlib.colors.ListedColormap([(0.8,0.8,0.8), (0.8,0.8,0.8)])
          im            = M.imshow(a2shade_trans, origin="lower", cmap=cmshade) 
          
          #-- coastline ---------------
          print "coastlines"
          M.drawcoastlines()
          
          #-- meridians and parallels
          M.drawmeridians(arange(0.0,360.0, meridians), labels=[0, 0, 0, 1])
          M.drawparallels(arange(-90.0,90.0, parallels), labels=[1, 0, 0, 0])
          #-- title -------------------
          axmap.set_title("%s"%(stitle))
          #-- save --------------------
          plt.savefig(soname)
          print soname 
          # for colorbar ---
          if cbarflag == "True":
            figmap   = plt.figure()
            axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
            M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
            a2v_trans    = M.transform_scalar( a2in,   a1lon, a1lat, nnx, nny)
            im       = M.imshow(a2value_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm)
          
            figcbar   = plt.figure(figsize=(5, 0.6))
            axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
            bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
            plt.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar, orientation="horizontal")
            figcbar.savefig(cbarname)
           
        #******************************************************
        #-- input name -----
        qname = "/media/disk2/data/JRA25/sa.one.%s/6hr/SPFH/%04d%02d/%s.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(resol,year, mon, resol, plev*0.01, year, mon, day, hour)
        tname = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP/%04d%02d/%s.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(resol, year, mon, resol, plev*0.01, year, mon, day, hour)
        
        #-- q: mixing ratio --------------------------
        if ftype == "q":
          a2q            = fromfile(qname, float32).reshape(ny,nx)
          a2gradq        = dtanl_fsub.mk_a2grad_abs_saone(a2q.T).T
          a2gradq        = a2gradq * 1000.0*100.0 # [kg/kg (100km)-1]
          a2thermo       = a2q   # K
          a2gradthermo   = a2gradq  # K/100km
          a2highsidegrad = a2gradq

          a2t            = fromfile(tname, float32).reshape(ny,nx)
          a2gradt        = dtanl_fsub.mk_a2grad_abs_saone(a2t.T).T
          a2gradt        = a2gradt * 1000.0*100.0 # [K (100km)-1]
        
        #-- t: ---------------------------------------
        if ftype == "t":
          a2t            = fromfile(tname, float32).reshape(ny,nx)
          a2gradt        = dtanl_fsub.mk_a2grad_abs_saone(a2t.T).T
          a2gradt        = a2gradt * 1000.0*100.0 # [K (100km)-1]
          a2thermo       = a2t   # K
          a2gradthermo   = a2gradt  # K/100km
          a2highsidegrad = a2gradt
        
        #-- theta_e --------
        if ftype == "theta_e":
          a2t            = fromfile(tname, float32).reshape(ny,nx)
          a2q            = fromfile(qname, float32).reshape(ny,nx)
          a2tv           = a2t * (1.0+0.61*a2q)
          a2gradtv       = dtanl_fsub.mk_a2grad_abs_saone(a2tv.T).T
        
          a2theta_e      = dtanl_fsub.mk_a2theta_e(plev, a2t.T, a2q.T).T
          a2gradtheta_e  = dtanl_fsub.mk_a2grad_abs_saone(a2theta_e.T).T
          a2gradtheta_e  = a2gradtheta_e * 1000.0*100.0 # [K (100km)-1]
          a2thermo       = a2theta_e   # K
          a2gradthermo   = a2gradtheta_e  # K/100km
          a2highsidegrad = a2gradtv
        ##**********************************************
        if ftype in ["t"]:
          thfmask1_name = thfmask1
          thfmask2_name = thfmask2
        elif ftype in ["q"]:
          thfmask1_name = thfmask1 * 1.0e+4
          thfmask2_name = thfmask2 * 1.0e+3
        #-------------      
        #bnd        = [0.1, 0.4, 0.7, 1.0,1.3,1.6,1.9,2.2,2.5]
        #bnd        = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
        bnd        = [0.0, 0.000005,  0.000007, 0.000009, 0.000011]
        scm        = "jet"
        if ftype in ["theta_e","t"]:
          stitle     = "loc.%s (K 100km-1)\n"%(ftype)
        elif ftype in ["q"]:
          stitle     = "loc.%s (kg/kg 100km-1)\n"%(ftype)
        
        stitle     = stitle + "M1:%3.2f M2:%3.2f\n"%(thfmask1_name, thfmask2_name)
        stitle     = stitle + "%04d-%02d-%02d  UTC %02d:00 (JST %02d:00)"%(year, mon, day, hour, hour+9)
        soname     = sodir + "/front.loc.%s.%04d.%02d.%02d.%02d.M1-%04.2f.M2-%04.2f.png"%(ftype, year, mon, day, hour, thfmask1_name, thfmask2_name)
        cbarname   = cbardir + "/cbar.loc.%s.png"%(ftype)
        
        #******************************************************
        #-- orog & grad orog ----
        orogname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
        gradname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/maxgrad.0200km.sa.one"
        a2orog     = fromfile(orogname, float32).reshape(ny,nx)
        a2gradorog = fromfile(gradname, float32).reshape(ny,nx)
        
        #
        #------
        a2loc    = mk_front_loc_contour(a2thermo, a2gradthermo, thfmask1, thfmask2)
        a2loc    = ma.masked_where(a2orog > thorog, a2loc).filled(miss_out)
        print type(a2loc)
        print a2loc
        a2loc     = dtanl_fsub.fill_front_gap(a2loc.T, miss_out).T
        a2loc    = ma.masked_where(a2orog > thorog, a2loc).filled(miss_out)
        a2loc    = ma.masked_where(a2gradorog > thgradorog, a2loc).filled(miss_out)
        a2loc    = dtanl_fsub.del_front_lesseq_ngrids(a2loc.T, miss_out, thgrids).T
        #--- for q ------
        if ftype == "q":
          a2loct  = mk_front_loc_contour(a2t, a2gradt, thfmask1t, thfmask2t)
          a2loct  = ma.masked_where(a2orog > thorog, a2loct).filled(miss_out)
          a2loct  = ma.masked_where(a2gradorog > thgradorog, a2loct).filled(miss_out)

          a2loct  = dtanl_fsub.fill_front_gap(a2loct.T, miss_out).T
          a2loct  = dtanl_fsub.del_front_lesseq_ngrids(a2loct.T, miss_out, thgrids).T
          a2terrt = ctrack_fsub.mk_territory_deg_saone(a2loct.T, 2, miss_out).T
          a2loc   = ma.masked_where(a2terrt==1.0, a2loc).filled(miss_out)

        #------
        mk_regmap(a2loc, bnd, scm, stitle, soname, cbarname, miss_out)
        #------
        
        
