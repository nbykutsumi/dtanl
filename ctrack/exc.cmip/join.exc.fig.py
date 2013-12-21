import Image,os
from numpy import *
import cmip_para, ctrack_para, tc_para, front_para
import cmip_func, ctrack_func, tc_func, front_func

#filterflag = True
filterflag = False

#sum3x3flag = True
sum3x3flag = False

lmodel = ["MRI-CGCM3","CNRM-CM5","MIROC5","HadGEM2-ES","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","IPSL-CM5A-MR","NorESM1-M","GFDL-CM3","IPSL-CM5B-LR"]
#lmodel = ["HadGEM2-ES"]
#lexpr   = ["historical", "rcp85"]
lexpr   = ["historical"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
thdura  = 48
#countrad = 300.0 #[km]
countrad = 1.0 #[km]
lseason  = ["ALL"]
#*** Figure para *********
iyfig  = 140
eyfig  = -100
ixfig  = 30
exfig  = -75

iyfig  = 100
eyfig  = -140
ixfig  = 75
exfig  = -30



#*************************
llkey  = [[season,expr] for season in lseason for expr in lexpr]

for season, expr in llkey:
  #-------  Init ---------
  da2dat = {}
  #-----------------------
  imodel = -1
  for model in lmodel:
    imodel = imodel + 1 
    #----
    ens   = cmip_para.ret_ens(model, expr, "psl")
    sunit, scalendar = cmip_para.ret_unit_calendar(model,expr)
    iyear,eyear = dyrange[expr]
    lyear       = range(iyear,eyear+1)
    lmon        = ctrack_para.ret_lmon(season)
  
    thsst    = tc_para.ret_thsst()
    thwind   = tc_para.ret_thwind()
    thrvort  = tc_para.ret_thrvort(model)
    thwcore  = tc_para.ret_thwcore(model)

    thfmask1t, thfmask2t, thfmask1q, thfmask2q   = front_para.ret_thfmasktq(model)
    #*** load figure *****
    idir  = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/exc/freq.%02dh/%04d-%04d.%s"%(model,expr,thdura,iyear,eyear,season)

    #-----------
    if (filterflag == True)&(sum3x3flag==True):
      pngname = idir + "/freq.exc.%s.%s.rad%04dkm.%04d-%04d.%s.filt.3x3.png"%(model,ens,countrad,iyear,eyear,season)
    if (filterflag == True)&(sum3x3flag==False):
      pngname = idir + "/freq.exc.%s.%s.rad%04dkm.%04d-%04d.%s.filt.png"%(model,ens,countrad,iyear,eyear,season)
    if (filterflag == False)&(sum3x3flag==True):
      pngname = idir + "/freq.exc.%s.%s.rad%04dkm.%04d-%04d.%s.3x3.png"%(model,ens,countrad,iyear,eyear,season)
    if (filterflag == False)&(sum3x3flag==False):
      pngname = idir + "/freq.exc.%s.%s.rad%04dkm.%04d-%04d.%s.png"%(model,ens,countrad,iyear,eyear,season)
    #-----------

    a2png  = Image.open(pngname)
    a2array= asarray(a2png)[iyfig:eyfig, ixfig:exfig]

    da2dat[imodel]  = a2array
  #*******************
  # JRA25
  #-------------------
  #jraname  = "/media/disk2/out/JRA25/sa.one.org/6hr/exc/c48h.bsttc/1980-1999.ALL/pict/freq.exc.bsttc.1980-1999.ALL.png"
  jradir   = "/media/disk2/out/JRA25/sa.one.org/6hr/exc/c%02dh.bsttc/%04d-%04d.%s/pict"%(thdura,iyear,eyear,season)
  if (filterflag==True)&(sum3x3flag==True):
    jraname  = jradir + "/filter.3x3.freq.exc.bsttc.%04d-%04d.%s.png"%(iyear,eyear,season)
  elif (filterflag==True)&(sum3x3flag==False):
    jraname  = jradir + "/filter.freq.exc.bsttc.%04d-%04d.%s.png"%(iyear,eyear,season)
  elif (filterflag==False)&(sum3x3flag==True):
    jraname  = jradir + "/3x3.freq.exc.bsttc.%04d-%04d.%s.png"%(iyear,eyear,season)
  elif (filterflag==False)&(sum3x3flag==False):
    jraname  = jradir + "/freq.exc.bsttc.%04d-%04d.%s.png"%(iyear,eyear,season)
  #----------
  a2pngbst = Image.open(jraname)
  da2dat[-1] = asarray(a2pngbst)[iyfig:eyfig, ixfig:exfig]
  #*******************
  # Dummy
  #-------------------
  da2dat[-9999] = ma.masked_equal(da2dat[-1] * 0.0, 0.0).filled(255)
  #---- Join ---------
  if len(lmodel) == 9:
    a2line1  = hstack([da2dat[-1], da2dat[-9999], da2dat[-9999]])
    a2line2  = hstack([da2dat[0], da2dat[1], da2dat[2]])
    a2line3  = hstack([da2dat[3], da2dat[4], da2dat[5]])
    a2line4  = hstack([da2dat[6], da2dat[7], da2dat[8]])
    a2oarray = vstack([a2line1, a2line2, a2line3, a2line4])

  elif len(lmodel) == 11:
    a2line1  = hstack([da2dat[-1], da2dat[-9999], da2dat[-9999]])
    a2line2  = hstack([da2dat[0], da2dat[1], da2dat[-9999]])
    a2line3  = hstack([da2dat[2], da2dat[3], da2dat[4]])
    a2line4  = hstack([da2dat[5], da2dat[6], da2dat[7]])
    a2line5  = hstack([da2dat[8], da2dat[9], da2dat[10]])
    a2oarray = vstack([a2line1, a2line2, a2line3, a2line4, a2line5])

  #-------------------
  
  oimg     = Image.fromarray(uint8(a2oarray))

  #---- write --------
  odir     = "/media/disk2/out/CMIP5/sa.one.MME.%s/6hr/cf/freq.%02dh/%04d-%04d.%s"%(expr,thdura,iyear,eyear,season)
  ctrack_func.mk_dir(odir)

  if (filterflag==True)&(sum3x3flag==True):
    oname    = odir + "/filt.3x3.join.exc.%04d-%04d.%s.png"%(iyear,eyear,season)
  elif (filterflag==True)&(sum3x3flag==False):
    oname    = odir + "/filt.join.exc.%04d-%04d.%s.png"%(iyear,eyear,season)
  elif (filterflag==False)&(sum3x3flag==True):
    oname    = odir + "/3x3.join.exc.%04d-%04d.%s.png"%(iyear,eyear,season)
  elif (filterflag==False)&(sum3x3flag==False):
    oname    = odir + "/join.exc.%04d-%04d.%s.png"%(iyear,eyear,season)
  #--------
  oimg.save(oname) 
  print oname

  #*******************
  # cbar
  #-------------------
  #-----------
  if sum3x3flag == True:
    cbarname = jradir + "/3x3.freq.exc.bsttc.cbar.%s.png"%(season)
  elif sum3x3flag == False:
    cbarname = jradir + "/freq.exc.bsttc.cbar.%s.png"%(season)
  #-----------
  os.system("cp %s %s"%(cbarname, odir)) 

