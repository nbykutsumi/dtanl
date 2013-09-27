from numpy import *
from ctrack_fsub import *
import ctrack_para
import os, calendar
import matplotlib.pyplot as plt
import cf
import gsmap_func
#*************************************************************
iyear     = 2001
eyear     = 2004
season    = "DJF"
tstp      = "6hr"
nx_org    = 360
ny_org    = 180

var       = "pr"
lmon      = ctrack_para.ret_lmon(season)
#lmon      = [1]
lhour     = [0, 6, 12, 18]

#thgrad_min    = 500.0  # Pa/1000km
#thgrad_max    = 1000.0 # Pa/1000km
dpgradrange   = ctrack_para.ret_dpgradrange()
lclass        = dpgradrange.keys()

#prtype        = "GSMaP"  # "JRA", "GPCP1DD", "GSMaP"
#prtype        = "JRA"  # "JRA", "GPCP1DD", "GSMaP"
prtype        = "GPCP1DD"  # "JRA", "GPCP1DD", "GSMaP"
#---------------------
dkm           = 100.0  # equal area grid resolution [km]
nradeqgrid    = 30

#---------------------
nx_eqgrid     = nradeqgrid*2 + 1
ny_eqgrid     = nradeqgrid*2 + 1
#---------------------
latmin    = 30.0
latmax    = 60.0
lonmin    = 120.
lonmax    = 240.

#latmin    = 32.0
#latmax    = 34.0
#lonmin    = 136.0
#lonmax    = 138.0

#latmin    = 38.0
#latmax    = 40.0
#lonmin    = 136.0
#lonmax    = 138.0
#-------------------------------------------
miss_out  = -9999.0
#------------------------------------------

#---------------------
def readlatlon(fname):
  f = open(fname, "r")
  lines = f.readlines()
  f.close()
  lines = map(float, lines)
  return lines
#--------
def latlon2yx(lat, lon, lat_first, lon_first, dlat, dlon):
  iy    = int( (lat + 0.5*dlat - lat_first)/dlat )
  ix    = int( (lon + 0.5*dlon - lon_first)/dlon )
  return iy, ix

sreg="%02d.%02d.%03d.%03d"%(latmin, latmax, lonmin, lonmax)
#*************************************************************
didir_root   = {}
#--- precipitation directory -----
if prtype == "GSMaP":
  didir_root["pr"]   = "/media/disk2/data/GSMaP/sa.one/6hr/ptot"
elif prtype == "JRA":
  didir_root["pr"]   = "/media/disk2/data/JRA25/sa.one/6hr/PR"
elif prtype == "GPCP1DD":
  didir_root["pr"]   = "/media/disk2/data/GPCP1DD/data/1dd"
#---------------------------------
didir_root["life"]   = "/media/disk2/out/JRA25/sa.one/6hr" + "/%s"%("life")
didir_root["pgrad"]  = "/media/disk2/out/JRA25/sa.one/6hr" + "/%s"%("pgrad")
didir_root["wap"]    = "/media/disk2/out/JRA25/sa.one/6hr" + "/%s"%("wap")

#-------
odir         = "/home/utsumi/bin/dtanl/ctrack/temp"

#---- lat and lon data :original ----------
#latname      = didir_root["life"] + "/%04d%02d"%(iyear, lmon[0]) + "/lat.txt"
#lonname      = didir_root["life"] + "/%04d%02d"%(iyear, lmon[0]) + "/lon.txt"
#a1lat_org    = readlatlon(latname)
#a1lon_org    = readlatlon(lonname)
#
#dlat_org       = a1lat_org[1] - a1lat_org[0]
#dlon_org       = a1lon_org[1] - a1lon_org[0]
#
#lat_org_first  = a1lat_org[0]
#lon_org_first  = a1lon_org[0]

lat_org_first   = -89.5
lon_org_first   = 0.5
lat_org_last    = 89.5
lon_org_last    = 359.5

dlat_org        = 1.0
dlon_org        = 1.0

a1lat_org       = arange(lat_org_first, lat_org_last + dlat_org*0.5, dlat_org)
a1lon_org       = arange(lon_org_first, lon_org_last + dlon_org*0.5, dlon_org)

#---- lat and lon data : finner ---------
lat_fin_first = -89.95
lon_fin_first = 0.05
lat_fin_last  = 89.95
lon_fin_last  = 359.95

dlat_fin      = 0.2
dlon_fin      = 0.2
a1lat_fin     = arange(lat_fin_first, lat_fin_last + dlat_fin*0.5, dlat_fin)
a1lon_fin     = arange(lon_fin_first, lon_fin_last + dlon_fin*0.5, dlon_fin)

#------------------------------------------
ymin_org      = int( (latmin - lat_org_first)/dlat_org )
ymax_org      = int( (latmax - lat_org_first)/dlat_org )
if lonmin >= 0.0:
  xmin_org      = int( (lonmin - (lon_org_first-0.5*dlon_org))/dlon_org )
  xmax_org      = int( (lonmax - (lon_org_first-0.5*dlon_org))/dlon_org )
else:
  xmin_org      = int( (lonmin + 0.0001 - (lon_org_first + 0.5*dlon_org ))/dlon_org )
  xmax_org      = int( (lonmax + 0.0001 - (lon_org_first + 0.5*dlon_org ))/dlon_org )

lx_org      = range(xmin_org, xmax_org+1)
ly_org      = range(ymin_org, ymax_org+1)

#---- dummy ------------------------------
a2one             = ones([ny_eqgrid, nx_eqgrid], float32)

a2sum_eqgrid      = zeros([ny_eqgrid, nx_eqgrid], float32)
a2num_eqgrid      = zeros([ny_eqgrid, nx_eqgrid], float32)

#---- dummy for cor. coef ----------------
a2cor_num         = zeros([ny_eqgrid, nx_eqgrid], float32)
a2cor_SA          = zeros([ny_eqgrid, nx_eqgrid], float32)
a2cor_SB          = zeros([ny_eqgrid, nx_eqgrid], float32)
a2cor_SAB         = zeros([ny_eqgrid, nx_eqgrid], float32)
a2cor_SA2         = zeros([ny_eqgrid, nx_eqgrid], float32)
a2cor_SB2         = zeros([ny_eqgrid, nx_eqgrid], float32)
#-----------------------------------------

for iclass in lclass:
  thgrad_min    = dpgradrange[iclass][0]
  thgrad_max    = dpgradrange[iclass][1]
  
  #lnum   = []
  #lA     = []
  #lB     = []
  #lAB   = []
  #lA2   = []
  #lB2   = []
  #---------------------
  if var == "pr":
    oname_mean   = odir + "/%s.%s.%s.%04.0f-%04.0f.bn"%(var, prtype, sreg, thgrad_min, thgrad_max)
    oname_cor    = odir + "/cc.%s.%s.%s.%04.0f-%04.0f.bn"%(var, prtype, sreg, thgrad_min, thgrad_max)
  #---------------------
  
  i = 0
  for year in range(iyear, eyear+1):
    for mon in lmon:
    #for mon in [1]:
      #----------
      didir    = {}
      for var_temp in ["pr", "life", "pgrad","wap"]:
        if var_temp == "wap":
          didir[var_temp] = didir_root[var_temp] + "/day/%04d%02d"%(year, mon)
        if var_temp == "pr":
          #----
          if prtype in ["GSMaP", "JRA"]:
            didir[var_temp] = didir_root[var_temp] + "/%04d%02d"%(year, mon)
          elif prtype in ["GPCP1DD"]:
            didir[var_temp] = didir_root[var_temp] + "/%04d"%(year)
  
          #----
        else:
          didir[var_temp] = didir_root[var_temp] + "/%04d%02d"%(year, mon)
      #-- no leap ------
      if (mon ==2):
        eday = 28
      else:
        eday  = calendar.monthrange(year, mon)[1]
  
      #eday = 1
      #-----------------
      for day in range(1, eday+1):
      #for day in range(1,5):
        print year, mon, day
        for hour in lhour:
          #--- name ------------
          diname          = {}
          #-- prec name --
          if prtype == "GSMaP":
            diname["pr"]    = didir["pr"]    + "/gsmap_mvk.6rh.%04d%02d%02d.%02d00.v5.222.1.sa.one"%(year, mon, day, hour)
          elif prtype == "JRA":
            diname["pr"]    = didir["pr"]    + "/fcst_phy2m.PR.%04d%02d%02d%02d.sa.one"%(year, mon, day, hour)
          elif prtype == "GPCP1DD":
            diname["pr"]    = didir["pr"]    + "/gpcp_1dd_v1.1_p1d.%04d%02d%02d.bn"%(year, mon, day)
  
          #---------------
          diname["life"]  = didir["life"]  + "/life.%04d%02d%02d%02d.sa.one"%(year, mon, day, hour)
          diname["pgrad"] = didir["pgrad"] + "/pgrad.%04d%02d%02d%02d.sa.one"%(year, mon, day, hour)
          #diname["wap"]   = didir["wap"] + "/%s_day_%s_%s_%s_%04d%02d%02d00.bn"%(model, expr, ens, year, mon, day)
          #--- load ------------
          da2in           = {}
          #-- prec load --
          if var == "pr":
            if prtype == "GSMaP":
              da2in[var]      = fromfile(diname[var],  float32).reshape(120, 360)
              da2in[var]      = gsmap_func.gsmap2global_one(da2in[var], miss_out)
            elif prtype == "JRA":
              da2in[var]      = fromfile(diname[var],  float32).reshape(ny_org, nx_org)
            elif prtype == "GPCP1DD":
              da2in[var]      = flipud(fromfile(diname[var],  float32).reshape(ny_org, nx_org))
          #---------------
          da2in["pgrad"]  = fromfile(diname["pgrad"],float32).reshape(ny_org, nx_org)
          #da2in["life"]   = fromfile(diname["life"], int32).reshape(ny_org, nx_org)
  
          #--- original --> fine grid ---
          a2in_fin        = cf.biIntp(a1lat_org, a1lon_org, da2in[var], a1lat_fin, a1lon_fin, miss=miss_out)[0] 
  
          #--- cyclone center data -------------
          da2in["center"] = ma.masked_less(da2in["pgrad"], 0.0).filled(0.0)
          da2in["center"] = ma.masked_greater(da2in["center"], 0.0).filled(1.0)
          #-------------------------------------
          for iy_org in ly_org:
            for ix_org in lx_org:
              #-------------
              if thgrad_min <= da2in["pgrad"][iy_org, ix_org] < thgrad_max:
                i = i+1
                print iy_org, ix_org
                #---- project center position original --> fine grid
                lat_org          = a1lat_org[iy_org]
                lon_org          = a1lon_org[ix_org]
                iy_fin, ix_fin   = latlon2yx(lat_org, lon_org, lat_fin_first, lon_fin_first, dlat_fin, dlon_fin)
    
                iy_fin_fort  = iy_fin + 1
                ix_fin_fort  = ix_fin + 1
    
                #---- search and project to equal size grids -----
                a2sum_eqgrid_temp, a2num_eqgrid_temp =\
                        ctrack_fsub.eqgrid_aggr(\
                                      a2in_fin.T\
                                    , a1lat_fin\
                                    , a1lon_fin\
                                    , dkm\
                                    , nradeqgrid\
                                    , iy_fin_fort\
                                    , ix_fin_fort\
                                    , miss_out) 
     
                a2sum_eqgrid_temp = a2sum_eqgrid_temp.T
                a2num_eqgrid_temp = a2num_eqgrid_temp.T
                
                a2sum_eqgrid  = a2sum_eqgrid + a2sum_eqgrid_temp
                a2num_eqgrid  = a2num_eqgrid + a2num_eqgrid_temp
                
                #--- for correlation coefficient ------
                a2cor_num_temp= ma.masked_where( a2num_eqgrid_temp <=0.0, a2one).filled(0.0)
                a2cor_A_temp = (ma.masked_where(a2num_eqgrid_temp==0.0, a2sum_eqgrid_temp) / a2num_eqgrid_temp).filled(0.0)
                a2cor_B_temp = a2cor_num_temp * da2in["pgrad"][iy_org, ix_org]
                
                a2cor_num     = a2cor_num + a2cor_num_temp
                a2cor_SA      = a2cor_SA  + a2cor_A_temp
                a2cor_SB      = a2cor_SB  + a2cor_B_temp
                a2cor_SAB     = a2cor_SAB + a2cor_A_temp * a2cor_B_temp
                a2cor_SA2     = a2cor_SA2 + a2cor_A_temp **2.0
                a2cor_SB2     = a2cor_SB2 + a2cor_B_temp **2.0
    
                  
                #lnum.append(a2cor_num_temp[58,21])
                #lA.append(a2cor_A_temp[58,21])
                #lB.append(a2cor_B_temp[58,21])
                #lAB.append(a2cor_A_temp[58,21]*a2cor_B_temp[58,21])
                #lA2.append(a2cor_A_temp[58,21]**2.0)
                #lB2.append(a2cor_B_temp[58,21]**2.0)
  
  
  #----------------------------------------------
  a2mean_eqgrid  = ma.masked_where(a2num_eqgrid ==0.0, a2sum_eqgrid) / a2num_eqgrid
  a2mean_eqgrid  = a2mean_eqgrid.filled(0.0)
  
  #-- corr. coeff -------
  a2cor_MA       = (ma.masked_where(a2cor_num ==0.0, a2cor_SA) / a2cor_num).filled(0.0)
  a2cor_MB       = (ma.masked_where(a2cor_num ==0.0, a2cor_SB) / a2cor_num).filled(0.0)
  #
  a2cor_bunshi   = a2cor_SAB - a2cor_MB * a2cor_SA - a2cor_MA * a2cor_SB + a2cor_num * a2cor_MA * a2cor_MB
  
  a2cor_bunbo1   = a2cor_SA2 - 2.0 * a2cor_MA * a2cor_SA + a2cor_num * a2cor_MA**2.0
  
  a2cor_bunbo2   = a2cor_SB2 - 2.0 * a2cor_MB * a2cor_SB + a2cor_num * a2cor_MB**2.0
  
  a2cor_bunbo    = (a2cor_bunbo1 * a2cor_bunbo2)**0.5
  a2cor_eqgrid   = ( ma.masked_where(a2cor_bunbo == 0.0, a2cor_bunshi) / a2cor_bunbo ).filled(0.0)
  
  #-- save --------------
  a2mean_eqgrid.tofile(oname_mean)
  a2cor_eqgrid.tofile(oname_cor)
  #-- figure ---------------------
  
  if var == "pr":
    if prtype in ["GPCP1DD"]:
      coef = 1.0
    else:
      coef = 60*60*24.0
  else:
    coef = 1.0
  #--
  a2mean_eqgrid = fromfile(oname_mean, float32).reshape(ny_eqgrid, nx_eqgrid)
  figname_mean = oname_mean[:-3] + ".png"
  plt.clf()
  plt.imshow(a2mean_eqgrid * coef, origin="lower", interpolation="nearest", vmin= 0.0, vmax=15.0)
  plt.colorbar()
  plt.savefig(figname_mean)
  plt.clf()
  print figname_mean
  
  #-- figure corr. coef --------
  
  a2cor_eqgrid = fromfile(oname_cor, float32).reshape(ny_eqgrid, nx_eqgrid)
  figname_cor = oname_cor[:-3] + ".png"
  plt.clf()
  plt.imshow(a2cor_eqgrid, origin="lower", interpolation="nearest", vmin= -0.2, vmax=0.2)
  plt.colorbar()
  plt.savefig(figname_cor)
  plt.clf()
  print figname_cor
