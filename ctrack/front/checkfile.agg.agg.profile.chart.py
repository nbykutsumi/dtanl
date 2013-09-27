import ctrack_para
import ctrack_func, os
#-----------------------------
#lseason = ["ALL","JJA","DJF"]
lseason = ["ALL"]
#lseason = [1]
lvtype  = ["theta","theta_e"]
lftype  = ["warm","cold","occ","stat"]
#lftype  = ["warm","cold","stat"]
lplev     = [925., 850.,700., 600., 500., 300., 250.]
#lplev     = [850.,700., 600., 500., 300., 250.]
ldist_km = [-700,-600,-500,-400,-300,-200,-100,0,100,200,300,400,500,600,700]
region  = "ASAS"
window  = "no"
#window  = "out"
#window  = "in"

dist_mask= 0. # (km)
#dist_mask= 300. # (km)
#dist_mask= 500. # (km)
#dist_mask= 1000. # (km)

iyear   = 2000
eyear   = 2010
#eyear   = 2001
nx,ny   = (360,180)
plev_sfc  = 850.0
#***********************
for vtype in lvtype:
  for season in lseason:
    lmon  = ctrack_para.ret_lmon(season)
    #--------------
    for ftype in lftype: 
      #-----
      for dist_km in ldist_km:
        #--------------------------
        for year in range(iyear, eyear+1):
          for mon in lmon:
            #----------
            if ((year==2010)&(mon==12)):
              continue
            #***** theta *************************
            idir            = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d/prof"%(year,mon)
            for plev in lplev:
              #print vtype,ftype,year,mon,plev
              #--- mean theta ----------
              climdir         = "/media/disk2/out/chart/ASAS/front/agg/%04d-%04d/%s"%(iyear,eyear,mon)
              climname        = climdir  + "/mean.%s.%04dhPa.sa.one"%(vtype,plev_sfc) 
              if os.path.exists(climname) == False:
                print "nofile",climname
              #-------------------------
              if window == "no":
                iname_thermo         =  idir + "/%s.maskrad.%04dkm.%s.%04dhPa.sa.one"%(vtype, dist_km, ftype, plev)
                iname_num_thermo     =  idir + "/num_%s.maskrad.%04dkm.%s.%04dhPa.sa.one"%(vtype, dist_km, ftype, plev)
              elif window in ["in","out"]:
                iname_thermo         =  idir + "/%s.maskrad.%s.%04dkm.%04dkm.%s.%04dhPa.sa.one"%(vtype, window, dist_mask, dist_km, ftype, plev)
                iname_num_thermo     =  idir + "/num_%s.maskrad.%s.%04dkm.%04dkm.%s.%04dhPa.sa.one"%(vtype, window, dist_mask, dist_km, ftype, plev)
              #--
              if os.path.exists(iname_thermo) ==False:
                print "nofile", iname_thermo
              if os.path.exists(iname_num_thermo) ==False:
                print "nofile", iname_num_thermo
  
            #***** grad.theta *************************
            idir            = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d/prof"%(year,mon)
            if window == "no":
              iname_gradthermo         =  idir + "/grad.%s.maskrad.%04dkm.%s.sa.one"%(vtype, dist_km, ftype)
              iname_num_gradthermo     =  idir + "/num_grad.%s.maskrad.%04dkm.%s.sa.one"%(vtype, dist_km, ftype)
            elif window in ["in","out"]:
              iname_gradthermo         =  idir + "/grad.%s.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(vtype, window, dist_mask, dist_km, ftype)
              iname_num_gradthermo     =  idir + "/num_grad.%s.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(vtype, window, dist_mask, dist_km, ftype)
            #--
            if os.path.exists(iname_gradthermo) ==False:
              print iname_gradthermo

            if os.path.exists(iname_num_gradthermo) ==False:
              print iname_num_gradthermo
  
            #***** grad2.theta *************************
            idir            = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d/prof"%(year,mon)
            if window == "no":
              iname_grad2thermo         =  idir + "/grad2.%s.maskrad.%04dkm.%s.sa.one"%(vtype, dist_km, ftype)
              iname_num_grad2thermo     =  idir + "/num_grad2.%s.maskrad.%04dkm.%s.sa.one"%(vtype, dist_km, ftype)
            elif window in ["in","out"]:
              iname_grad2thermo         =  idir + "/grad2.%s.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(vtype, window,dist_mask, dist_km, ftype)
              iname_num_grad2thermo     =  idir + "/num_grad2.%s.maskrad.%s.%04dkm.%04dkm.%s.sa.one"%(vtype, window,dist_mask, dist_km, ftype)
            #--
            if os.path.exists(iname_grad2thermo) ==False:
              print iname_grad2thermo

            if os.path.exists(iname_num_grad2thermo) ==False:
              print iname_num_grad2thermo
 

  
 
 
