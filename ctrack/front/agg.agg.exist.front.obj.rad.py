from numpy import *
from myfunc_fsub import *
import sys
import calendar
from ctrack_fsub import *
from dtanl_fsub import *
import ctrack_para, ctrack_func, ctrack_fig
import front_para, front_func
#---------------------------------
#filterflag = True
filterflag = False

#sum3x3flag = True
sum3x3flag = False

#singleday= True
singleday= False
calcflag = True
#calcflag = False

#iyear = 1997
#eyear = 2012
iyear  = 1980
eyear  = 1999
lyear   = range(iyear,eyear+1)
#lseason = ["ALL"]
#lseason = ["ALL","DJF","JJA"]
lseason = range(1,12+1)
iday  = 1
#lhour = [12]
lhour = [0,6,12,18]
ny    = 180
nx    = 360
miss  = -9999.0
thdist   = front_para.ret_thdistkm()  # (km)
#
countrad = 500  # (km) for frequency count
#countrad = 1.0  # (km) for frequency count
#
sresol   = "anl_p"
#lftype = ["t","q"]
lftype = ["t"]

#--------------
#a2filter = array(\
#           [[1,2,1]\
#           ,[2,4,2]\
#           ,[1,2,1]], float32)

#a2filter = array(\
#           [[1,1,1,1,1]\
#           ,[1,1,1,1,1]\
#           ,[1,1,1,1,1]\
#           ,[1,1,1,1,1]\
#           ,[1,1,1,1,1]], float32)

a2filter = array(\
           [[1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1,1,1,1,1]], float32)


#-- para for objective locator -------------
plev     = 850*100.0 # (Pa)
thorog     = ctrack_para.ret_thorog()
thgradorog = ctrack_para.ret_thgradorog()
thgrids    = front_para.ret_thgrids()
thfmask1t, thfmask2t, thfmask1q, thfmask2q   = front_para.ret_thfmasktq(sresol)
orogname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
gradname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/maxgrad.0200km.sa.one"
a2orog     = fromfile(orogname, float32).reshape(ny,nx)
a2gradorog = fromfile(gradname, float32).reshape(ny,nx)
#--- shade       ------
a2one    = ones([ny,nx],float32)
a2shade  = ma.masked_where( a2orog >=thorog, a2one).filled(miss)
a2shade  = ma.masked_where( a2gradorog >= thgradorog, a2shade).filled(miss)



#-------------------------------------------
lllat  = -89.5
lllon  = 0.5
urlat  = 89.5
urlon  = 359.5
#-------------------------------------------
#******************************
#-- out dir -----------------
idir_root  = "/media/disk2/out/JRA25/sa.one.%s/6hr/tenkizu/front/agg"%(sresol)
#-----------------------
for season  in lseason:
  lmon  = ctrack_para.ret_lmon(season)
  for ftype in lftype:
    #---- init -----
    a2count  = zeros([ny,nx],float32)
    #---------------
    for year in lyear:
      #--------------------- 
      if calcflag == False:
        continue
      #--------------------- 
      for mon in lmon:
        #********************************
        #-- for monthly data front ------
        idir_mon   = "/media/disk2/out/JRA25/sa.one.%s/6hr/front.%s/agg/%04d/%02d"%(sresol,ftype,year,mon)
        #----------
        if ftype == "t":
          thfmask1, thfmask2  = thfmask1t, thfmask2t
        elif ftype == "q":
          thfmask1, thfmask2  = thfmask1q, thfmask2q
        #----------
        iname       = idir_mon + "/count.front.%s.rad%04dkm.M1_%s_M2_%s.sa.one"%(ftype, countrad, thfmask1, thfmask2)
        a2count_mon = fromfile(iname, float32).reshape(ny,nx)
        a2count_mon = ma.masked_equal(a2count_mon, miss).filled(0.0)
        a2count     = a2count + a2count_mon
    #---------
    ntimes   = ctrack_para.ret_totaldays(iyear,eyear,season)*4
    a2freq   = (ma.masked_equal(a2count,miss) / ntimes).filled(miss)
    #---------
    odir     = "/media/disk2/out/JRA25/sa.one.%s/6hr/front.%s/agg/%04d-%04d.%s"%(sresol,ftype,iyear,eyear,season)
    ctrack_func.mk_dir(odir)
    oname    = odir + "/freq.front.%s.rad%04dkm.M1_%s_M2_%s.sa.one"%(ftype, countrad, thfmask1, thfmask2)
    a2freq.tofile(oname)
    print oname

    #***************************
    #  figure
    #---------------------------
    if sum3x3flag == True:
      bnd         = [5,10,15,20,25,30,35,40,45]  # (%)
      #bnd         = [10,40,70,100,130,160,190,220,250]  # (days/season)
    elif sum3x3flag == False:
      if countrad >= 500.0:
        bnd       = [10,20,30,40,50,60,70,80,90]  # (%)
      else:
        bnd         = [1,3,5,7,9,11,13,15,19]   # (%)
        #bnd         = [1,4,7,10,13,16,19,22,25]   # (days/season)
    #----------
    figdir   = odir + "/pict"
    ctrack_func.mk_dir(figdir)
    if (filterflag == True)&(sum3x3flag==True):
      figname  = figdir + "/filt.3x3.freq.front.%s.rad%04dkm.M1_%s_M2_%s.png"%(ftype, countrad, thfmask1, thfmask2)
    elif (filterflag == True)&(sum3x3flag==False):
      figname  = figdir + "/filt.freq.front.%s.rad%04dkm.M1_%s_M2_%s.png"%(ftype, countrad, thfmask1, thfmask2)
    elif (filterflag == False)&(sum3x3flag==True):
      figname  = figdir + "/3x3.freq.front.%s.rad%04dkm.M1_%s_M2_%s.png"%(ftype, countrad, thfmask1, thfmask2)
    elif (filterflag == False)&(sum3x3flag==False):
      figname  = figdir + "/freq.front.%s.rad%04dkm.M1_%s_M2_%s.png"%(ftype, countrad, thfmask1, thfmask2)
    #-----------
    if sum3x3flag == True:
      cbarname = figdir + "/3x3.freq.front.%s.rad%04dkm.cbar.png"%(ftype,countrad)
    elif sum3x3flag == False:
      cbarname = figdir + "/freq.front.%s.rad%04dkm.cbar.png"%(ftype,countrad)
    #----------

    #----------
    stitle   = "freq. %s: season:%s %04d-%04d"%(ftype, season,iyear, eyear)
    mycm     = "Spectral"
    datname  = oname
    figname  = figname
    a2figdat = fromfile(datname, float32).reshape(ny,nx)

    #---- unit ----
    totaldays = ctrack_para.ret_totaldays(iyear,eyear,season)
    a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
    #a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * totaldays / len(lyear)
    #-- filter --------------
    if filterflag == True:
      a2figdat = myfunc_fsub.mk_a2convolution(a2figdat.T, a2filter.T, miss).T
      #a2figdat = myfunc_fsub.mk_a2convolution(a2figdat.T, a2filter.T, miss).T
    elif filterflag ==False:
      pass
    else:
      print "check filterflag",filterflag
      sys.exit()

    #-- per 3.0 degree box --
    if sum3x3flag == True:
      a2figdat = myfunc_fsub.mk_3x3sum_one(a2figdat.T, miss).T  
    #------------------------

    ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
    print figname


  
   
  
