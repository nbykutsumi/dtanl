from numpy import *
import sys
import calendar
from ctrack_fsub import *
from dtanl_fsub import *
import ctrack_para, ctrack_func
import front_para, front_func
#---------------------------------
#singleday= True
singleday= False
calcflag = True
#calcflag = False

iyear = 1997
eyear = 2012
lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon  = [1]
iday  = 1
#lhour = [12]
lhour = [0,6,12,18]
region= "ASAS"
ny    = 180
nx    = 360
miss  = -9999.0
thdist   = front_para.ret_thdistkm()  # (km)
#
sresol   = "anl_p"
lftype = ["t","q"]
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

#-------------------------------------------
a2one    = ones([ny,nx],float32)
#******************************
#-- out dir -----------------
odir_root  = "/media/disk2/out/JRA25/sa.one.%s/6hr/tenkizu/front/agg"%(sresol)
#-----------------------
for ftype in lftype:
  for year in range(iyear, eyear+1):
    #--------------------- 
    if calcflag == False:
      continue
    #--------------------- 
    for mon in lmon:
      itimes_mon  = 0
      #************************
      #-- init for front ------
      a2count_mon    = zeros([ny,nx],float32)
      #************************
      eday = calendar.monthrange(year, mon)[1]
      if singleday==True:
        eday = iday
      #----------------
      for day in range(iday, eday+1):
        ##---------------------
        #if ((year==iyear)&(mon==1)&(day==1)):
        #  continue
        #if ((year==eyear)&(mon==12)&(day==31)):
        #  continue 
        ##---------------------
        if singleday == True:
          if (day !=iday):
            continue
        #---------------------
        print ftype, year, mon, day, "single=",singleday
        #---------------------
        for hour in lhour:
          #-------------------
          itimes_mon = itimes_mon + 1
          #-------------------
          # for objective front locator
          #----------------------------- 
          # Name
          frontdir_t_root   = "/media/disk2/out/JRA25/sa.one.%s/6hr/front.t"%(sresol)
          frontdir_q_root   = "/media/disk2/out/JRA25/sa.one.%s/6hr/front.q"%(sresol)
          frontdir_t  = frontdir_t_root   + "/%04d%02d"%(year, mon)
          frontdir_q  = frontdir_q_root   + "/%04d%02d"%(year, mon)
          #
  
          fronttname1 = frontdir_t + "/front.t.M1.%04d.%02d.%02d.%02d.sa.one"%(year, mon, day, hour)
          fronttname2 = frontdir_t + "/front.t.M2.%04d.%02d.%02d.%02d.sa.one"%(year, mon, day, hour)
          frontqname1 = frontdir_q + "/front.q.M1.%04d.%02d.%02d.%02d.sa.one"%(year, mon, day, hour)
          frontqname2 = frontdir_q + "/front.q.M2.%04d.%02d.%02d.%02d.sa.one"%(year, mon, day, hour)  
  
          #-- front.t ---
          a2fbc1      = fromfile(fronttname1, float32).reshape(ny,nx)
          a2fbc2      = fromfile(fronttname2, float32).reshape(ny,nx)
          a2fbc       = front_func.complete_front_t_saone(a2fbc1, a2fbc2, thfmask1t, thfmask2t, a2orog, a2gradorog, thorog, thgradorog, thgrids, miss )
  
          #-- front.q ---
          if ftype == "q":
            a2nbc1      = fromfile(frontqname1, float32).reshape(ny,nx)
            a2nbc2      = fromfile(frontqname2, float32).reshape(ny,nx)
            a2nbc       = front_func.complete_front_q_saone(a2fbc, a2nbc1, a2nbc2, thfmask1q, thfmask2q, a2orog, a2gradorog, thorog, thgradorog, thgrids, miss)
    
          #-- count baloclinic front loc --
          if ftype == "t":
            a2loc = a2fbc
          elif ftype == "q":
            a2loc = a2nbc
          #-------------------
          a2temp         = ma.masked_where(a2loc ==miss, a2one).filled(miss)
    
          a2countterr    = ctrack_fsub.mk_8gridsmask_saone(a2temp.T, miss).T
          a2count_tmp    = ma.masked_where(a2countterr ==miss, a2one).filled(0.0)
  
          a2count_mon = a2count_mon + a2count_tmp
      #********************************
      #-- for monthly data front ------
      odir_mon   = "/media/disk2/out/JRA25/sa.one.%s/6hr/front.%s/agg/%04d/%02d"%(sresol,ftype,year,mon)
      ctrack_func.mk_dir(odir_mon)
      #----------
      if ftype == "t":
        thfmask1, thfmask2  = thfmask1t, thfmask2t
      elif ftype == "q":
        thfmask1, thfmask2  = thfmask1q, thfmask2q
      #----------
      name_temp = odir_mon + "/count.front.%s.3deg.M1_%s_M2_%s.sa.one"%(ftype, thfmask1, thfmask2)
      a2temp    = a2count_mon
      a2temp    = ma.masked_where(a2orog>thorog, a2temp).filled(miss)
      a2temp    = ma.masked_where(a2gradorog>thgradorog, a2temp).filled(miss)
      a2temp.tofile(name_temp)
      print name_temp
