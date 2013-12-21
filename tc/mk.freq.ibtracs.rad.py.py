from numpy import *
from myfunc_fsub import *
import calendar
import ctrack_fig, ctrack_para, ctrack_func

filterflag = True
#filterflag = False

#sum3x3flag = True
sum3x3flag = False

#iyear  = 1997
#eyear  = 2012
iyear  = 1980
eyear  = 1999
lyear  = range(iyear,eyear+1)

#lseason = ["ALL","MJJASO","NDJFMA"]
lseason = ["ALL"]
#lseason = [1,2,3,4,5,6,7,8,9,10,11,12]
#countrad  = 300.0 # [km]
countrad  = 1.0 # [km]
ny,nx   = 180,360
miss    = -9999.0

#-------------------------
#a2filter = array(\
#           [[1,2,1]\
#           ,[2,4,2]\
#           ,[1,2,1]], float32)

a2filter = array(\
           [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]], float32)

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
  for year in lyear:
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
  if len(lmon) ==12:
    if sum3x3flag == True:
      #bnd        = [0.01,0.25,0.5,1.0,2.0,4.0]
      bnd        = [0.1,0.25,0.5,1.0,2.0,4.0]
    if sum3x3flag == False:
      bnd        = [0.01, 0.025, 0.5, 0.1, 0.2, 0.4]
  elif len(lmon) ==3:
    #bnd        = [0.01,0.25,0.5,1.0,2.0,4.0]
    bnd        = [0.1,0.25,0.5,1.0,2.0,4.0]
  elif len(lmon) ==1:
    #bnd        = [0.01,0.25,0.5,1.0,2.0,4.0]
    bnd        = [0.1,0.25,0.5,1.0,2.0,4.0]
  #---------------------------
  figdir     = odir
  #-----------
  if (filterflag == True)&(sum3x3flag==True):
    figname    = oname[:-7] + ".filt.3x3.png"
  if (filterflag == True)&(sum3x3flag==False):
    figname    = oname[:-7] + ".filt.png"
  if (filterflag == False)&(sum3x3flag==True):
    figname    = oname[:-7] + ".3x3.png"
  if (filterflag == False)&(sum3x3flag==False):
    figname    = oname[:-7] + ".png"
  #-----------
  if sum3x3flag == True:
    cbarname   = oname[:-7] + ".3x3.cbar.png"
  elif sum3x3flag== False:
    cbarname   = oname[:-7] + ".cbar.png"
  #----------
  stitle   = "freq (days/season) bst.TC season:%s %04d-%04d"%(season,iyear, eyear)
  mycm     = "Spectral"
  datname  = oname
  a2figdat = fromfile(datname, float32).reshape(ny,nx)
  #-------------------------------
  totaldays = ctrack_para.ret_totaldays(iyear,eyear,season)
  #a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
  a2figdat = ma.masked_equal(a2freq, miss).filled(0.0) * totaldays / len(lyear)  # [days per season]

  #--- filtering ----
  if filterflag == True:
    a2figdat = myfunc_fsub.mk_a2convolution(a2figdat.T, a2filter.T, miss).T
    #a2figdat = myfunc_fsub.mk_a2convolution(a2figdat.T, a2filter.T, miss).T

  #---- 3x3 -----
  if sum3x3flag == True:
    a2figdat = myfunc_fsub.mk_3x3sum_one(a2figdat.T, miss).T

  #-----------------
  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
  print figname 

