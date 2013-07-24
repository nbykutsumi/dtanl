from numpy import *
import ctrack_func
import gsmap_func
import matplotlib.pyplot as plt
import chart_para
#-----------------------------------------------
iyear      = 2001
eyear      = 2009

sresol  = "anl_p"

lbstflag_tc = ["bst"]
#lbstflag_tc = ["","bst"]
#lbstflag_f  = ["","bst.high","bst.type"]
lbstflag_f  = [""]
#**
lregion    = ["W.JPN","E.JPN"]
lseason    = ["NDJFMA","JJASON","ALL"]
#lseason    = ["DJF"]
#lseason    = [1]
ltimescale = [1,3,6,12,24]
#ltimescale = [24]
#ltag       = ["tc","c","fbc","ot","nbcot"]
ltag       = ["tc","c","fbc","ot","nbc"]
percent    = 99.9
#*
nx, ny             = (360,180)
#**
dist_tc = 1000 #[km]
dist_c  = 1000 #[km]
dist_f  = 500 #[km]
#**
thdura_c  = 48
thdura_tc = thdura_c


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
  
        idir       = "/media/disk2/out/JRA25/sa.one.%s/6hr/tagpr/c%02dh.tc%02dh/%04d-%04d/%s"%(sresol, thdura_c, thdura_tc, iyear,eyear,season)
        pictdir    = idir + "/pict"
        ctrack_func.mk_dir(pictdir)
      
        #**** load *************
        da2in      = {}
        for tag in ltag:
          for timescale in ltimescale:
            if tag == "nbcot":
              iname_ot    = idir + "/rfreq.%stc%04d.c%04d.%sf%04d.%04d-%04d.%s.mov%02dhr.%05.2f.GSMaP.%s.sa.one"%(bstflag_tc, dist_tc, dist_c, bstflag_f, dist_f, iyear,eyear,season,timescale,percent,"ot")
              iname_nbc   = idir + "/rfreq.%stc%04d.c%04d.%sf%04d.%04d-%04d.%s.mov%02dhr.%05.2f.GSMaP.%s.sa.one"%(bstflag_tc, dist_tc, dist_c, bstflag_f, dist_f, iyear,eyear,season,timescale,percent,"nbc")

              a2in_ot     = fromfile(iname_ot, float32).reshape(ny,nx)
              a2in_ot     = ma.masked_equal(a2in_ot, miss).filled(0.0)
              a2in_nbc    = fromfile(iname_nbc, float32).reshape(ny,nx)
              a2in_nbc    = ma.masked_equal(a2in_nbc, miss).filled(0.0)
              da2in[tag,timescale]  = a2in_ot + a2in_nbc
            else:
              iname    = idir + "/rfreq.%stc%04d.c%04d.%sf%04d.%04d-%04d.%s.mov%02dhr.%05.2f.GSMaP.%s.sa.one"%(bstflag_tc, dist_tc, dist_c, bstflag_f, dist_f, iyear,eyear,season,timescale,percent,tag)
              da2in[tag,timescale]  = fromfile(iname, float32).reshape(ny,nx)
      
        #**** make sum-mask ****
        da2sum       = {}
        for timescale in ltimescale:
          da2sum[timescale]    = zeros([ny,nx],float32)
          for tag in ltag:
            da2sum[timescale]  = da2sum[timescale]  +  ma.masked_equal(da2in[tag,timescale], miss).filled(0.0)
      
        #***********************
        dv         = {}
        dstd       = {}
        for tag in ltag:
          #*****
          if tag not in dv.keys():
            dv[tag]   = []
            dstd[tag] = []
          #*****
          for timescale in ltimescale:
            a2in     = da2in[tag,timescale]
            #**
            a2in     = ma.masked_equal(a2in, miss)
            a2in     = ma.masked_where(da2sum[timescale]==0.0, a2in)
            a2in     = ma.masked_where(a2regionmask==0.0, a2in)
            v        = a2in.mean()
            std      = a2in.std()
            dv[tag].append(v) 
            dstd[tag].append(std)
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
        for tag in ltag:
          lx         = ltimescale
          ly         = dv[tag]
          axplot.plot(lx,ly, linewidth=3.0)
          #-- error range ---
          ly_up      = array(dv[tag]) + array(dstd[tag])
          ly_lw      = array(dv[tag]) - array(dstd[tag])
          #axplot.fill_between(lx, ly_lw, ly_up, facecolor="gray", alpha = 0.1)
          axplot.fill_between(lx, ly_lw, ly_up, alpha = 0.1)

        #-- sum --
        #axplot.plot(ltimescale, dv["sum"])

        #-- set axis limit --
        axplot.set_ylim( (0.0, 1.0))
        #-- legend ----
        axplot.legend(ltag+["sum"])
        #axplot.legend(ltag)
        #-- save ------
        figname    = pictdir + "/plot.rfreq.timescale.%stc%04d.c%04d.%sf%04d.%04d-%04d.%s.p%05.2f.GSMaP.%s.png"%(bstflag_tc, dist_tc, dist_c,bstflag_f, dist_f, iyear,eyear,season, percent,region)
        figplot.savefig(figname)
        print figname
