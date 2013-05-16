from numpy import *
import ctrack_func
import gsmap_func
import matplotlib.pyplot as plt
import chart_para
#-----------------------------------------------
iyear      = 2001
eyear      = 2004

lbstflag_tc = [""]
#lbstflag_tc = ["","bst"]
lbstflag_f  = ["","bst.high","bst.type"]
#lbstflag_f  = [""]
#**
lregion    = ["W.JPN","E.JPN"]
lseason    = ["NDJFMA","JJASON","DJF","JJA","ALL"]
#lseason    = ["DJF"]
#lseason    = [1]
ltimescale = [1,3,6,12,24]
#ltimescale = [24]
ltag       = ["tc","c","fbc","nbc","ot"]
percent    = 99.9
#*
nx, ny             = (360,180)
#**
dist_tc = 500 #[km]
dist_c  = 1000 #[km]
dist_f  = 500 #[km]
#**
dlat,dlon  = (1.0, 1.0)
lat_first  = -89.5
lon_first  = 0.5
#**
miss       = -9999.0
#----------------------------------
for bstflag_tc in lbstflag_tc:
  for bstflag_f in lbstflag_f:
    for season in lseason:
      for region in lregion:
        print "region=",region
        #*** region mask *************
        lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region)
        a2regionmask  = ctrack_func.mk_region_mask(lllat, urlat, lllon, urlon, nx, ny, lat_first, lon_first, dlat, dlon)
        #-----------------------------
  
        idir       = "/media/disk2/out/JRA25/sa.one/6hr/tagpr/%04d-%04d/%s"%(iyear,eyear,season)
        pictdir    = idir + "/pict"
        ctrack_func.mk_dir(pictdir)
      
        #**** load *************
        da2in      = {}
        for tag in ltag:
          for timescale in ltimescale:
            iname    = idir + "/rfreq.%stc%02d.c%02d.%sf%02d.%04d-%04d.%s.mov%02dhr.%05.2f.GSMaP.%s.sa.one"%(bstflag_tc, dist_tc*0.01, dist_c*0.01, bstflag_f, dist_f*0.01, iyear,eyear,season,timescale,percent,tag)
            da2in[tag,timescale]  = fromfile(iname, float32).reshape(ny,nx)
      
        #**** make sum-mask ****
        da2sum       = {}
        for timescale in ltimescale:
          da2sum[timescale]    = zeros([ny,nx],float32)
          for tag in ltag:
            da2sum[timescale]  = da2sum[timescale]  +  ma.masked_equal(da2in[tag,timescale], miss).filled(0.0)
      
        #***********************
        dv         = {}
      
        for tag in ltag:
          #*****
          if tag not in dv.keys():
            dv[tag] = []
          #*****
          for timescale in ltimescale:
            a2in     = da2in[tag,timescale]
            #**
            a2in     = ma.masked_equal(a2in, miss)
            a2in     = ma.masked_where(da2sum[timescale]==0.0, a2in)
            a2in     = ma.masked_where(a2regionmask==0.0, a2in)
            v        = a2in.mean()
            dv[tag].append(v) 
      
        #* sum all ************************
        dv["sum"] = []
        for i in range(len(ltimescale)):
          vall    = 0.0
          a2temp_sum = zeros([ny,nx],float32)
          for tag in ltag:
            vall  = vall + dv[tag][i]
          #
          dv["sum"].append(vall)
        #**** plot ************************
        figplot  = plt.figure()
        axplot   = figplot.add_axes([0.2, 0.2, 0.7, 0.7])
        for tag in ltag + ["sum"]:
        #for tag in ltag:
          lx         = ltimescale
          ly         = dv[tag]
          axplot.plot(lx,ly)
        #-- set axis limit --
        axplot.set_ylim( (0.0, 1.0))
        #-- legend ----
        axplot.legend(ltag+["sum"])
        #axplot.legend(ltag)
        #-- save ------
        figname    = pictdir + "/plot.rfreq.timescale.%stc%02d.c%02d.%sf%02d.%04d-%04d.%s.p%05.2f.GSMaP.%s.png"%(bstflag_tc, dist_tc*0.01, dist_c*0.01,bstflag_f, dist_f*0.01, iyear,eyear,season, percent,region)
        figplot.savefig(figname)
        print figname
