from numpy import *
import calendar
import ctrack_para
import ctrack_func
import sys, os
import gsmap_func
import datetime
from dtanl_fsub import *
from ctrack_fsub import *
#---------------------------------
iyear   = 2001
eyear   = 2004
lmon    = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon    = [1]
iday    = 1
lhour   = [0,6,12,18]
#lhour   = [0]
#----
plev    = 850*100.0  #(Pa)
sresol  = "anl_p"
lthfmask1  = [0.1,0.3,0.5,0.7,0.9,1.1]
lthfmask2  = [1.0,2.0,3.0,4.0,5.0,6.0]
#************************
thorog  = ctrack_para.ret_thorog()
highsidedist  = ctrack_para.ret_highsidedist()
miss_out = -9999.0
ny       = 180
nx       = 360

lat_first= -89.5
lon_first= 0.5
dlat, dlon  = 1.0, 1.0
#** region mask **********
lllat    = 25.
lllon    = 125.
urlat    = 50.
urlon    = 155.
#--
a2regionmask  = ctrack_func.mk_region_mask(lllat,urlat,lllon,urlon,nx,ny,lat_first,lon_first,dlat,dlon)
#*************************

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

#******************************************************
#-- orog & grad orog ----
orogname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
#gradorogadjname= "/media/disk2/data/JRA25/sa.one.125/const/topo/grad.topo.adj.twogrids.sa.one"
a2orog     = fromfile(orogname, float32).reshape(ny,nx)
#a2gradorogmask = fromfile(gradorogadjname, float32).reshape(ny,nx)

#******************************************************
#--  init ---------
a2one   = ones([ny,nx],float32)

#******************************************************
for year in range(iyear, eyear+1):
  for mon in lmon:
    #-- init monthly data --
    da2hit      = {}
    da2miss     = {}
    da2os       = {}
    da2num_obj  = {}

    for thfmask1 in lthfmask1:
      for thfmask2 in lthfmask2:
        key = (thfmask1,thfmask2)
        da2hit[key]       = zeros([ny,nx],float32)
        da2miss[key]      = zeros([ny,nx],float32)
        da2os[key]        = zeros([ny,nx],float32)
        da2num_obj[key]   = zeros([ny,nx],float32)
    #
    a2num_chart     = zeros([ny,nx],float32)
    #-----------
    eday  = calendar.monthrange(year,mon)[1]
    #-----------
    for day in range(iday, eday+1):
      for hour in lhour:
        stime   = "%04d%02d%02d%02d"%(year, mon, day, hour)
        #******************************************************
        #-- load gridded chart -
        chartdir  = "/media/disk2/out/chart/ASAS/front/%04d%02d"%(year,mon)
        chartname = chartdir + "/front.ASAS.%04d.%02d.%02d.%02d.saone"%(year,mon,day,hour)  
        a2chart   = fromfile(chartname, float32).reshape(ny,nx)
        a2chart   = ma.masked_where(a2chart==miss_out, a2one).filled(0.0)
        a2num_chart =  a2num_chart + a2chart

        #******************************************************
        #-- q: mixing ratio --------------------------
        qname = "/media/disk2/data/JRA25/sa.one.%s/6hr/SPFH/%04d%02d/%s.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,year, mon, sresol, plev*0.01, year, mon, day, hour)
        a2q   = fromfile(qname, float32).reshape(ny,nx)

        #-- t: ---------------------------------------
        tname = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP/%04d%02d/%s.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,year, mon, sresol, plev*0.01, year, mon, day, hour)
        a2t   = fromfile(tname, float32).reshape(ny,nx)

        #-- tv: --------------------------------------
        a2tv  = a2t * (1.0+0.61*a2q)
        #-- a2gradtv ---------------------------------
        a2gradtv  = dtanl_fsub.mk_a2grad_abs_saone(a2tv.T).T

        #-- theta_e -----------------------------------
        a2theta_e = dtanl_fsub.mk_a2theta_e(plev, a2t.T, a2q.T).T
        #-- grad.theta_e ------------------------------------
        a2thermo         = a2theta_e
        a2gradtheta_e    = dtanl_fsub.mk_a2grad_abs_saone(a2thermo.T).T

        #**********************************************
        # base: grad.theta_e
        a2gradtheta_e  = a2gradtheta_e * 1000.0*100.0 # [K (100km)-1]

        ##**********************************************
        # front locator: theta_e
        a2thermo             = a2theta_e # K
        a2gradthermo         = a2gradtheta_e   # K/100km
        #***********
        for thfmask1 in lthfmask1:
          for thfmask2 in lthfmask2:
            key      = (thfmask1,thfmask2)
            print year,mon,day,hour,thfmask1,thfmask2
            #------
            a2loc    = mk_front_loc_contour(a2thermo, a2gradthermo, thfmask1, thfmask2)
            a2loc    = ma.masked_where(a2orog > thorog, a2loc).filled(miss_out)
            #a2loc    = ma.masked_where(a2gradorogmask > thgradorog, a2loc).filled(miss_out)
            a2loc    = dtanl_fsub.del_front_2grids(a2loc.T, miss_out).T
            a2loc    = ctrack_fsub.find_highsidevalue_saone(a2gradtheta_e.T, a2loc.T, a2gradtv.T, highsidedist, miss_out).T
            a2loc    = ma.masked_equal(a2loc, miss_out).filled(0.0)
            #******************************************
            a2obj    = ma.masked_where(a2loc ==0.0, a2one).filled(0.0)
            #******************************************
            #--- hit ------
            a2hittmp       =  ma.masked_where(a2obj==0.0,   a2one).filled(0.0)
            a2hittmp       =  ma.masked_where(a2chart==0.0, a2hittmp).filled(0.0)
            da2hit[key]    =  da2hit[key]  + a2hittmp

            #--- missed --
            da2miss[key]   =  da2miss[key] + ma.masked_where(a2obj >= a2chart, a2one).filled(0.0)

            #--- over estimated --
            da2os[key]     =  da2os[key]   + ma.masked_where(a2obj <= a2chart, a2one).filled(0.0)

            #--- count ---
            da2num_obj[key]   =  da2num_obj[key]   + a2obj

    #---- write to files -----------
    # names --
    sodir  = "/media/disk2/out/JRA25/sa.one.%s/6hr/front/valid/%04d%02d"%(sresol,year,mon)
    ctrack_func.mk_dir(sodir)

    #-- save num chart -- 
    namenumchart = sodir + "/num.chart.sa.one"
    a2num_chart.tofile(namenumchart)

    #-- save others    -- 
    for thfmask1 in lthfmask1:
      for thfmask2 in lthfmask2: 
        key          = thfmask1, thfmask2
        #--
        namehit      = sodir + "/num.hit.M1-%04.2f.M2-%04.2f.sa.one"%(thfmask1,thfmask2)
        namemiss     = sodir + "/num.miss.M1-%04.2f.M2-%04.2f.sa.one"%(thfmask1,thfmask2)
        nameos       = sodir + "/num.os.M1-%04.2f.M2-%04.2f.sa.one"%(thfmask1,thfmask2)
        namenumobj   = sodir + "/num.obj.M1-%04.2f.M2-%04.2f.sa.one"%(thfmask1,thfmask2)
        namenumchart = sodir + "/num.chart.M1-%04.2f.M2-%04.2f.sa.one"%(thfmask1,thfmask2)
        #--
        da2hit[key].tofile(namehit)
        da2miss[key].tofile(namemiss)
        da2os[key].tofile(nameos)
        da2num_obj[key].tofile(namenumobj)
    #
    print namehit






