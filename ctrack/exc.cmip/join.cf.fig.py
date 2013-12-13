import Image
from numpy import *
import cmip_para, ctrack_para, tc_para, front_para
import cmip_func, ctrack_func, tc_func, front_func
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
    #idir  = "/media/disk2/out/CMIP5/sa.one.NorESM1-M.historical/6hr/cf/freq.48h.M1_0.26.M2_0.6/1980-1999.ALL"
    idir  = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/cf/freq.%02dh.M1_%s.M2_%s/%04d-%04d.%s"%(model,expr,thdura,thfmask1t,thfmask2t,iyear,eyear,season)
    #pngname = idir + "/freq.cf.NorESM1-M.r1i1p1.rad0300km.1980-1999.ALL.png"
    pngname = idir + "/freq.cf.%s.%s.rad%04dkm.%04d-%04d.%s.png"%(model,ens,countrad,iyear,eyear,season)
    a2png  = Image.open(pngname)
    a2array= asarray(a2png)[iyfig:eyfig, ixfig:exfig]

    da2dat[imodel]  = a2array
  #*******************
  # JRA25
  #-------------------
  jraname  = "/media/disk2/out/JRA25/sa.one.anl_p/6hr/cf/c48h.bsttc.M1_0.30.M2_1.0/1997-2011.ALL/pict/freq.exc.bsttc.1997-2011.ALL.png"
  a2pngbst = Image.open(jraname)
  da2dat[-1] = asarray(a2pngbst)[iyfig:eyfig, ixfig:exfig]
  #*******************
  # Dummy
  #-------------------
  da2dat[-9999] = ma.masked_equal(da2dat[-1] * 0.0, 0.0).filled(255)
  #---- Join ---------
  if len(lmodel) == 9:
    a2line1  = hstack([da2dat[-1], da2dat[-2], da2dat[-9999]])
    a2line2  = hstack([da2dat[0], da2dat[1], da2dat[2]])
    a2line3  = hstack([da2dat[3], da2dat[4], da2dat[5]])
    a2line4  = hstack([da2dat[6], da2dat[7], da2dat[8]])
  elif len(lmodel) == 11:
    a2line1  = hstack([da2dat[-1], da2dat[-2], da2dat[-9999]])
    a2line2  = hstack([da2dat[0], da2dat[1], da2dat[-9999]])
    a2line3  = hstack([da2dat[2], da2dat[3], da2dat[4]])
    a2line4  = hstack([da2dat[5], da2dat[6], da2dat[7]])
    a2line5  = hstack([da2dat[8], da2dat[9], da2dat[10]])
  #-------------------

  a2oarray = vstack([a2line1, a2line2, a2line3, a2line4])
  oimg     = Image.fromarray(uint8(a2oarray))

  #---- write --------
  odir     = "/media/disk2/out/CMIP5/sa.one.MME.%s/6hr/cf/freq.%02dh/%04d-%04d.%s"%(expr,thdura,iyear,eyear,season)
  ctrack_func.mk_dir(odir)
  oname    = odir + "/join.cf.%04d-%04d.%s.png"%(iyear,eyear,season)
  oimg.save(oname) 
  print oname


