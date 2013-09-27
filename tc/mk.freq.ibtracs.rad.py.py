from numpy import *
import calendar
import ctrack_fig, ctrack_para, ctrack_func

iyear  = 1997
eyear  = 2012
lseason = ["ALL","MJJASO","NDJFMA"]
lseason = ["ALL","MJJASO","NDJFMA"]

countrad  = 300.0 # [km]
#countrad  = 1.0 # [km]
ny,nx   = 180,360
miss    = -9999.0
#-------------------------
lllat  = -89.5
lllon  = 0.5
urlat  = 89.5
urlon  = 359.5
#--- shade       ------
thorog     = ctrack_para.ret_thorog()
orogname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
a2orog     = fromfile(orogname, float32).reshape(ny,nx)
a2one    = ones([ny,nx],float32)
a2shade  = ma.masked_where( a2orog >=thorog, a2one).filled(miss)
#-------------------------

for season in lseason:
  lmon  = ctrack_para.ret_lmon(season)
  #--- init ---
  a2num = zeros([ny,nx],float32)
  #------------
  for year in range(iyear,eyear+1):
    for mon in lmon:
      idir   = "/media/disk2/out/ibtracs/sa.one/%04d/%02d"%(year,mon)
      iname  = idir + "/num.ibtracs_all.v03r04.rad%04dkm.sa.one"%(countrad)
      a2num_tmp = fromfile(iname, float32).reshape(ny,nx)
      a2num  = a2num + a2num_tmp
  #------------
  totalnum   = ctrack_para.ret_totaldays(iyear,eyear,season) *4.0
  a2freq     =  a2num / totalnum
  #
  odir       = "/media/disk2/out/ibtracs/sa.one/%04d-%04d.%s"%(iyear,eyear,season)
  ctrack_func.mk_dir(odir)
  oname      = odir + "/freq.ibtracs_all.v03r04.rad%04dkm.%04d-%04d.%s.sa.one"%(countrad,iyear,eyear,season)
  a2freq.tofile(oname)
  
  #-- figure ---
  #---------------------------
  bnd        = [0.01,0.25,0.5,1.0,2.0,4.0,8.0]
  #bnd        = [0.25,0.5,1.0,2.0,4.0,8.0]
  #bnd         = [5,10,15,20,25,30,35,40,45]
  #bnd        = [10,20,30,40,50,60,70,80]
  figdir     = odir
  figname    = oname[:-7] + ".png"
  cbarname   = oname[:-7] + ".cbar.png"
  #----------
  stitle   = "freq. rad%04dkm bst.TC season:%s %04d-%04d"%(countrad, season,iyear, eyear)
  mycm     = "Spectral"
  datname  = oname
  a2figdat = fromfile(datname, float32).reshape(ny,nx)

  #-------------------------------
  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
  print figname 

