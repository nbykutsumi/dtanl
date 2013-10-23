from numpy import *
import matplotlib.pyplot as plt
import ctrack_para, chart_para
import ctrack_func
import datetime

#**********************************************
iyear  = 2000
eyear  = 2010
lyear  = range(iyear,eyear+1)
lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]

lvtype = ["theta","theta_e"]
#lvtype  = ["theta_e"]
lftype  = [1,2,3,4]
ny,nx   = 180,360
miss    = -9999.0
distkm  = 200.0 # km

for vtype in lvtype:
  #*** init ****
  lplainv   = []
  dfrontv  = {}
  for ftype in lftype:
    dfrontv[ftype] = []
  #*************

  for year in lyear:
    for mon in lmon:
      print year,mon
      #***************************************
      # mask
      #------------------------
      region        = "ASAS"
      nx_fig,ny_fig    = chart_para.ret_nxnyfig(region, year, mon)
      paradate      = datetime.date(year,mon,1)
      xydatadir   = "/media/disk2/out/chart/ASAS/const"
      if (paradate < datetime.date(2006,1,1)):
        name_x_corres = xydatadir + "/stereo.xfort.fig2saone.ASAS.2000.01.bn"
        name_y_corres = xydatadir + "/stereo.yfort.fig2saone.ASAS.2000.01.bn"
        name_domain_mask = xydatadir + "/domainmask_saone.%s.2000.01.bn"%(region)
  
      if ( datetime.date(2006,1,1)<=paradate<datetime.date(2006,3,1)):
        name_x_corres = xydatadir + "/stereo.xfort.fig2saone.ASAS.2006.01.bn"
        name_y_corres = xydatadir + "/stereo.yfort.fig2saone.ASAS.2006.01.bn"
        name_domain_mask = xydatadir + "/domainmask_saone.%s.2006.01.bn"%(region)
  
      if ( datetime.date(2006,3,1)<=paradate):
        name_x_corres = xydatadir + "/stereo.xfort.fig2saone.ASAS.2006.03.bn"
        name_y_corres = xydatadir + "/stereo.yfort.fig2saone.ASAS.2006.03.bn"
        name_domain_mask = xydatadir + "/domainmask_saone.%s.2006.03.bn"%(region)
      #----
      a2xfort_corres   = fromfile(name_x_corres, float32).reshape(ny_fig, nx_fig)
      a2yfort_corres   = fromfile(name_y_corres, float32).reshape(ny_fig, nx_fig)
      a2domain_mask    = fromfile(name_domain_mask,float32).reshape(180,360)
      #***************************************


      idir   = "/media/disk2/out/obj.valid/gradtheta/%04d"%(year)
  
      plainname  = idir + "/anl_p.plain.grad%s.%04d.%02d.sa.one"%(vtype, year,mon)
      a2plain    = fromfile(plainname, float32).reshape(ny,nx)
      a2plain    = ma.masked_where(a2domain_mask==0.0, a2plain)
   
      lplainv.append( a2plain.mean() )  

      #***************
      for ftype in lftype:
        #--
        frontvname = idir + "/anl_p.front.grad%s.%04dkm.%s.%04d.%02d.sa.one"%(vtype, distkm, ftype, year,mon)
        #--

        a2frontv   = fromfile(frontvname,float32).reshape(ny,nx)
        a2frontv   = ma.masked_equal(a2frontv, miss)
        dfrontv[ftype].append( a2frontv.mean() ) 

  #** convert unit ******
  lplainv = array(lplainv)*1000.0*100.0
  for ftype in lftype:
    dfrontv[ftype]  = array(dfrontv[ftype])*1000.0*100.0

  #** output *******
  sout = ",warm,cold,occ,stat,plain\n"
  llabel = ["%04d-%02d"%(year,mon) for year in lyear for mon in lmon]
  for i in range(len(lyear)*len(lmon)):
    sout = sout + "%s,%s,%s,%s,%s,%s\n"%(llabel[i], dfrontv[1][i], dfrontv[2][i], dfrontv[3][i], dfrontv[4][i], lplainv[i])

  odir  = "/media/disk2/out/obj.valid/gradtheta/%04d-%04d"%(iyear,eyear)
  ctrack_func.mk_dir(odir)

  oname = odir + "/grad.%s.%04d-%04d.csv"%(vtype, iyear,eyear)
  f=open(oname,"w"); f.write(sout); f.close()
  print oname 

  #** output 3 months **
  sout = ",warm,cold,occ,stat,plain\n"
  for i in range(int(len(lyear)*len(lmon)/3.0)):
    frontv1  = sum(dfrontv[1][2+3*i:2+3*i+3])/3.0
    frontv2  = sum(dfrontv[2][2+3*i:2+3*i+3])/3.0
    frontv3  = sum(dfrontv[3][2+3*i:2+3*i+3])/3.0
    frontv4  = sum(dfrontv[4][2+3*i:2+3*i+3])/3.0
    plainv   = sum(lplainv[2+3*i:2+3*i+3])/3.0
    if i%4 ==0: season="MAM"
    if i%4 ==1: season="JJA"
    if i%4 ==2: season="SON"
    if i%4 ==3: season="DJF"
    print season,frontv1,frontv2,frontv3,frontv4,plainv
    sout  = sout + "%s,%s,%s,%s,%s,%s\n"%(season,frontv1,frontv2,frontv3,frontv4,plainv)
  #---    
  odir  = "/media/disk2/out/obj.valid/gradtheta/%04d-%04d"%(iyear,eyear)
  ctrack_func.mk_dir(odir)
  oname = odir + "/grad.3season.%04dkm.%s.%04d-%04d.csv"%(distkm, vtype, iyear,eyear)
  f=open(oname,"w"); f.write(sout); f.close()
  print oname




