import os, calendar
import ctrack_para, ctrack_func
#----------------------------------------------------
#singleday =True
singleday = False
filecheck = True
iyear = 2000
eyear = 2010
lseason = [1,2,3,4,5,6,7,8,9,10,11,12]
#lseason = [6]
#lvtype = ["theta","theta_e"]
lvtype = ["theta_e"]
#lseason = [1]
window = "no"
#window = "out"
#window = "in"
ldist_km = [-700,-600,-500,-400,-300,-200,-100,0,100,200,300,400,500,600,700] #(km)
#ldist_km = [300.0]  #(km)
#dist_mask = 500.  # (km)
#dist_mask = 1400.  # (km)
#dist_mask = 1800.  # (km)
#dist_mask = 2500.  # (km)
dist_mask = 0.  # (km)
lplev    = [925,850.,700., 600., 500.,300.,250.,]
#lplev    = [700., 600., 500.,300.,250.,]
#lplev    = [925.,850]
plev_sfc = 850
lftype = [1,2,3,4]
#lftype = [2]
sresol  = "anl_p"
iday  = 1
ny    = 180
nx    = 360
lhour = [0,6,12,18]
#lhour = [0]

lllat = 0.0
lllon = 90
urlat = 80
urlon = 210

#lllat = 0.0
#lllon = 90.0
#urlat = 90.0
#urlon = 140.0

#lllat = 0.0
#lllon = 140.0
#urlat = 80.0
#urlon = 210.0



#-----
miss  = -9999.0
chartdir_root = "/media/disk2/out/chart/ASAS/front"
tdir_root     = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP"%(sresol)
qdir_root     = "/media/disk2/data/JRA25/sa.one.%s/6hr/SPFH"%(sresol)
#------------------------
#************************
lat_first     = -89.5
dlat          = 1.0
dlon          = 1.0
#------------------------
for vtype in lvtype:
  for season in lseason:
    lmon     = ctrack_para.ret_lmon(season)
    #------------------------
    for year in range(iyear, eyear+1):
      for mon in lmon:
        #----------------
        eday = calendar.monthrange(year,mon)[1]
        for day in range(iday, eday+1):
          for hour in lhour:
            chartdir  = chartdir_root + "/%04d%02d"%(year,mon)
            tdir      = tdir_root     + "/%04d%02d"%(year,mon)
            qdir      = qdir_root     + "/%04d%02d"%(year,mon)
            #
            chartname = chartdir      + "/front.ASAS.%04d.%02d.%02d.%02d.sa.one"%(year,mon,day,hour)
            if os.path.exists(chartname) == False:
              print "no file", chartname 
            #-- load theta at each pressure level ------
            da2thermo_tmp  = {}
            #-----------------
            for plev in lplev:
              tname     = tdir          + "/%s.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,plev,year,mon,day,hour)
              qname     = qdir          + "/%s.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(sresol,plev,year,mon,day,hour)

              if os.path.exists(tname) == False:
                print "no file", tname
              if os.path.exists(qname) == False:
                print "no file", qname
