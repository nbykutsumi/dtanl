from numpy import *
import ctrack_func, cmip_func, front_func
import ctrack_para, cmip_para, front_para
import tc_para
import matplotlib.pyplot as plt
#-------------------------------------------
iyear = 1980
eyear = 1999
expr  = "historical"
#lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
season="ALL"
lmon  =ctrack_para.ret_lmon(season) 
thdura= 48
bstflag_tc = "bst"
#lmodel = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
lmodel = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","GFDL-CM3"]
#lmodel = ["HadGEM2-ES"]

ny    = 180
nx    = 360

lat_first = -89.5
lon_first = 0.5
dlat      = 1.0
dlon      = 1.0
#------------------------
countrad  = 1.0 # [km]
stepday   = 0.25
miss      = -9999.
#--- region -----
#lregion    = ["PNW", "PNE","INN","INS", "PSW","ATN"]
lregion    = ["GLB","SH","NH","NPA","NAT","EUR","SIP","SAT"]
da2regmask = {}
for region in lregion:
  #lllat, lllon, urlat, urlon = ctrack_para.ret_tcregionlatlon(region) 
  lllat, lllon, urlat, urlon = ctrack_para.ret_excregionlatlon(region) 
  da2regmask[region]  = ctrack_func.mk_region_mask(lllat, urlat, lllon, urlon, nx, ny, lat_first, lon_first, dlat, dlon) 
#----------------
dmfreq_jra  = {}
dmfreq_obj  = {}
#----------------
for mon in lmon:
  #***************************
  # JRA25 
  #---------------------------
  thfmask1t, thfmask2t, thfmask1q, thfmask2q   = front_para.ret_thfmasktq("anl_p")
  idir_jra        = "/media/disk2/out/JRA25/sa.one.%s/6hr/front.%s/agg/%04d-%04d.%s"%("anl_p","t",iyear,eyear,mon)
  ctrack_func.mk_dir(idir_jra)
  iname_jra       = idir_jra + "/freq.front.%s.rad%04dkm.M1_%s_M2_%s.sa.one"%("t", countrad, thfmask1t, thfmask2t)

  a2freq_jra_mon  = fromfile(iname_jra, float32).reshape(ny,nx) 

  for region in lregion:
    a2freq_jra_temp = ma.masked_where(da2regmask[region] !=1.0, a2freq_jra_mon)
    dmfreq_jra[region, mon] = a2freq_jra_temp.mean()

  #****************************
  # multi resolition 
  #----------------------------
  for model in lmodel:
    #-------------------
    thfmask1t, thfmask2t, thfmask1q, thfmask2q   = front_para.ret_thfmasktq(model)
    ens   = cmip_para.ret_ens(model, expr, "psl") 
    #-------------------
    idir_obj   = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/front.t/freq/%04d-%04d.%s"%(model,expr, iyear, eyear, mon)
    iname_obj  = idir_obj + "/freq.t.front.%s.%s.rad%04dkm.M1_%4.2f_M2_%3.1f.%04d-%04d.%s.sa.one"%(model,ens, countrad, thfmask1t, thfmask2t, iyear,eyear,mon)


    a2freq_obj_mon  = fromfile(iname_obj, float32).reshape(ny,nx)
    #
    for region in lregion:
      a2freq_obj_temp = ma.masked_where(da2regmask[region] !=1.0, a2freq_obj_mon)
      dmfreq_obj[model, region, mon] = a2freq_obj_temp.mean()
#---------

#---- montly graph -----------
for region in lregion:
  #*****************************
  # jra 
  #-----------------------------
  lv_jra = []
  ltime  = []
  for mon in lmon:
    ltime.append(mon)
    lv_jra.append(dmfreq_jra[region, mon])

  #*****************************
  # multi model
  #-----------------------------
  dlv_obj  = {}
  for model in lmodel:
    dlv_obj[model] = []
    for mon in lmon:
      dlv_obj[model].append(dmfreq_obj[model, region, mon])

  #*****************************
  plt.clf()
  figplot  = plt.figure()
  axplot   = figplot.add_axes([0.1,0.2,0.8,0.6])
  #-- plot ---
  axplot.plot( array(lv_jra) )  
  for model in lmodel:
    axplot.plot( array(dlv_obj[model]) )
  #- xticks --
  #plt.xticks( range(len(ltime))[::3],ltime[::3], rotation=90)
  plt.xticks( range(len(ltime)),ltime, rotation=0, fontsize=18)

  plt.yticks(fontsize=18)
  #- axis limit ---
  #axplot.set_ylim((0, 0.0006))

  #-- title --
  stitle   = "%s"%(region)
  axplot.set_title(stitle)
  #-- save ---
  odir      = "/media/disk2/out/CMIP5/sa.one.MME.%s/6hr/fbc/freq.%02dh/%04d-%04d.%s"%(expr,thdura,iyear,eyear,season)
  ctrack_func.mk_dir(odir)
  soname    = odir + "/plot.freq.fbc.%02dh.rad%04dkm.%04d-%04d.%s.%s.png"%(thdura, countrad, iyear,eyear,expr, region)
  figplot.savefig(soname)
  print soname

  #************************
  #- legend --
  if region == lregion[0]:
    #----
    lines    = axplot.get_lines()
    #----
    figleg   = plt.figure(figsize=(5,5))
    leg      = figleg.legend( lines, ["JRA25"]+lmodel, "center")
    
    legname  = odir + "/plot.freq.fbc.legent.png"
    figleg.savefig(legname)
  
  #*******************************
  # write to csv
  #-------------------------------
  sout = "time/freq"
  sout = sout + ",JRA25"
  for model in lmodel:
    sout = sout + ",%s"%(model)
  sout = sout + "\n"
  #
  for mon in lmon:
    sout = sout + "%02d"%(mon)
    sout = sout + ",%f"%(dmfreq_jra[region,mon])
    for model in lmodel:
      sout = sout + ",%f"%(dmfreq_obj[model,region,mon])
    #
    sout = sout + "\n"
  #---
  soname    = odir + "/plot.freq.fbc.%02dh.rad%04dkm.%04d-%04d.%s.%s.csv"%(thdura, countrad, iyear,eyear, expr, region)
  f = open(soname, "w"); f.write(sout); f.close()
  print soname
