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
#lsresol = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lsresol = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
#lsresol = ["test.1.5deg","test.10deg","test.5deg","test.3deg"]
#lsresol = ["MIROC5"]
iyear   = 2004
eyear   = 2004
lmon    = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon    = [1]
iday    = 1
lhour   = [0,6,12,18]
#lhour   = [0]
#----
plev    = 850*100.0  #(Pa)
ftype   = "t"
if ftype == "t":
  lthfmask1  = [0.18,0.22,0.26,0.30,0.34,0.38,0.42,0.46]
  lthfmask2  = [0.2,0.6,1.0,1.4,1.8]
elif ftype == "q":
  thfmask1_t = 0.3
  thfmask2_t = 1.0
  lthfmask1  = array([0.5,1.0,1.5,2.0,2.5])*1.0e-4
  lthfmask2  = array([0.5,1.0,1.5,2.0,2.5,3.0])*1.0e-3

thgrids = 7
delwgtflag = 1
#************************
thorog        = ctrack_para.ret_thorog()
thgradorog    = ctrack_para.ret_thgradorog()
highsidedist  = ctrack_para.ret_highsidedist()
miss_out = -9999.0
ny       = 180
nx       = 360

lat_first= -89.5
lon_first= 0.5
dlat, dlon  = 1.0, 1.0
miss     = -9999.0
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
gradname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/maxgrad.0200km.sa.one"
a2orog     = fromfile(orogname, float32).reshape(ny,nx)
a2grad     = fromfile(gradname, float32).reshape(ny,nx)

##---- baiu region -----
#lllat = 0.0
#urlat = 75.0
#lllon = 65.0
#urlon = 135.0
#a2region_baiu = ctrack_func.mk_region_mask(lllat,urlat,lllon,urlon,nx,ny,lat_first,lon_first,dlat,dlon)
#******************************************************
#******************************************************
for sresol in lsresol:
  #--  init ---------
  a2one   = ones([ny,nx],float32)
  #------------------
  for year in range(iyear, eyear+1):
    for mon in lmon:
      if ((ftype in ["q"])&(mon not in [5,6,7])):
        continue
      #-- init monthly data --
      da2num_obj  = {}
  
      for thfmask1 in lthfmask1:
        for thfmask2 in lthfmask2:
          key = (thfmask1,thfmask2)
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
          chartname = chartdir + "/front.ASAS.%04d.%02d.%02d.%02d.sa.one"%(year,mon,day,hour)
          a2chart   = fromfile(chartname, float32).reshape(ny,nx)
          #----
          a2chart   = ma.masked_where(a2chart==miss_out, a2one).filled(0.0)
  
          a2chart   = ma.masked_where(a2orog > thorog, a2chart).filled(0.0)
          a2chart   = ma.masked_where(a2grad > thgradorog, a2chart).filled(0.0)
          a2num_chart =  a2num_chart + a2chart
          #******************************
          #-- input name
          tname = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP/%04d%02d/anl_p.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,year, mon, plev*0.01, year, mon, day, hour)
          qname = "/media/disk2/data/JRA25/sa.one.%s/6hr/SPFH/%04d%02d/anl_p.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,year, mon, plev*0.01, year, mon, day, hour)
  
          #******************************************************
          #-- q: mixing ratio --------------------------
          if ftype == "q":
            a2thermo       = fromfile(qname, float32).reshape(ny,nx)
            a2gradthermo   = dtanl_fsub.mk_a2grad_abs_saone(a2thermo.T).T
            a2gradthermo   = a2gradthermo * 1000.0*100.0 # [kg/kg (100km)-1]
  
            a2t            = fromfile(tname, float32).reshape(ny,nx)
            a2gradt        = dtanl_fsub.mk_a2grad_abs_saone(a2t.T).T
            a2gradt        = a2gradt * 1000.0*100.0 # [K (100km)-1]
          #-- t: ---------------------------------------
          if ftype == "t":
            a2thermo       = fromfile(tname, float32).reshape(ny,nx)
            a2gradthermo   = dtanl_fsub.mk_a2grad_abs_saone(a2thermo.T).T
            a2gradthermo   = a2gradthermo * 1000.0*100.0 # [K (100km)-1]
  
          #-- theta_e -----------------------------------
          if ftype == "theta_e":
            a2t   = fromfile(tname, float32).reshape(ny,nx)
            a2q   = fromfile(qname, float32).reshape(ny,nx)
            a2tv  = a2t * (1.0 + 0.61*a2q)
  
            a2thermo       = dtanl_fsub.mk_a2theta_e(plev, a2t.T, a2q.T).T
            a2gradthermo   = dtanl_fsub.mk_a2grad_abs_saone(a2thermo.T).T
            a2gradthermo   = a2gradthermo * 1000.0*100.0 # [K (100km)-1]
            a2gradtv       = dtanl_fsub.mk_a2grad_abs_saone(a2tv.T).T
            a2gradtv       = a2gradtv * 1000.0*100.0  # [K (100km)-1]
          ##**********************************************
          for thfmask1 in lthfmask1:
            for thfmask2 in lthfmask2:
              key      = (thfmask1,thfmask2)
              print sresol,"%s"%(ftype), year,mon,day,hour,thfmask1,thfmask2
              #------
              a2loc    = mk_front_loc_contour(a2thermo, a2gradthermo, thfmask1, thfmask2)
              a2loc    = ma.masked_where(a2orog > thorog, a2loc).filled(miss_out)
              a2loc    = ma.masked_where(a2grad > thgradorog, a2loc).filled(miss_out)
              a2loc    = dtanl_fsub.fill_front_gap(a2loc.T, miss_out).T
              a2loc    = dtanl_fsub.del_front_lesseq_ngrids(a2loc.T, delwgtflag, miss_out, thgrids).T
              if ftype == "q":
                a2loct  = mk_front_loc_contour(a2t, a2gradt, thfmask1_t, thfmask2_t)
                a2loct  = ma.masked_where(a2orog > thorog, a2loct).filled(miss_out)
                a2loct  = ma.masked_where(a2grad > thgradorog, a2loct).filled(miss_out)
  
                a2loct  = dtanl_fsub.fill_front_gap(a2loct.T, miss_out).T
                a2loct  = dtanl_fsub.del_front_lesseq_ngrids(a2loct.T, delwgtflag, miss_out, thgrids).T
                a2terrt = ctrack_fsub.mk_territory_deg_saone(a2loct.T, 2, miss_out).T
                a2locq  = ma.masked_where(a2terrt==1.0, a2loc).filled(miss_out)
                a2loc   = ma.masked_where( (a2locq==miss_out)&(a2loct==miss_out), a2one).filled(miss_out)
              #-------
              if ftype == "theta_e": 
                a2loc    = ctrack_fsub.find_highsidevalue_saone(a2gradtheta_e.T, a2loc.T, a2gradtv.T, highsidedist, miss_out).T
              #-------
              #******************************************
              a2obj    = ma.masked_where(a2loc == miss_out, a2one).filled(0.0)
              #******************************************
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
          if ftype == "t":
            namenumobj   = sodir + "/num.%s.obj.M1-%04.2f.M2-%04.2f.gt%02d.sa.one"%(ftype, thfmask1,thfmask2,thgrids)
            #namenumchart = sodir + "/num.%s.chart.M1-%04.2f.M2-%04.2f.gt%02d.sa.one"%(ftype, thfmask1,thfmask2,thgrids)
          if ftype == "q":
            thfmask1_tmp, thfmask2_tmp = thfmask1*1.0e+4, thfmask2*1.0e+3
            namenumobj   = sodir + "/num.%s.obj.M1-%04.2f.M2-%04.2f.gt%02d.sa.one"%(ftype, thfmask1_tmp,thfmask2_tmp,thgrids)
            #namenumchart = sodir + "/num.%s.chart.M1-%04.2f.M2-%04.2f.gt%02d.sa.one"%(ftype, thfmask1_tmp,thfmask2_tmp,thgrids)
            print namenumobj
  
          #--
          da2num_obj[key].tofile(namenumobj)
      #
      print namenumobj
  
  
  
  
  

