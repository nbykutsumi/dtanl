from numpy import *
import ctrack_para
import ctrack_func
import calendar
import gsmap_func
import sys, os, subprocess, datetime
#------------------------------------------------
#iyear = 2001
#eyear = 2001

iyear = 2001
eyear = 2009
lseason = ["ALL"]
#lseason = [1]
#iday    = 1
iday    = 1
ny_org  = 1200
nx_org  = 3600
percent = 99.9 # (%)
#percent = 91 # (%)
#lnhour   = [1,3,6,12,24]
lnhour   = [1]

numrat  = 1.5  # numrat*ntop data will be stored
miss    = -9999.0
thmissrat = 0.8
#------------------------------------------------
idir_root = "/home/utsumi/mnt/iis.data2/GSMaP/standard/v5/hourly"
odir_root = "/media/disk2/data/GSMaP/sa.dec/1hr/ptot/ptile"
#***********************************************
lhour = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
#
#----- function -------------------------------
def timeave_gsmap_backward_org(year,mon,day,hour, hlen):
  lhlen = [1,2,3,6,12,24]
  if not hlen in lhlen:
    print "'hlen' should be" ,lhlen
    sys.exit()
  #-------------
  lh_inc     = range(hlen)
  now       = datetime.datetime(year,mon,day,hour)

  a2ave     = zeros([1200*3600],float32)
  for h_inc in lh_inc:
    dhour   = datetime.timedelta(hours = -h_inc)
    target  = now + dhour
    year_t  = target.year
    mon_t   = target.month
    day_t   = target.day
    hour_t  = target.hour
    idir_root = "/home/utsumi/mnt/iis.data2/GSMaP/standard/v5/hourly"
    idir      = idir_root + "/%04d/%02d/%02d"%(year_t,mon_t,day_t)
    iname     = idir + "/gsmap_mvk.%04d%02d%02d.%02d00.v5.222.1.dat.gz"%(year_t,mon_t,day_t,hour_t)
    dat_org   = subprocess.Popen(["gzip", "-dc", iname, " >", "/dev/stdout"], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()[0]
    a2in      = fromstring(dat_org, float32)
    a2ave     = a2ave + ma.masked_less(a2in, 0.0)
  #---
  #a2ave       = (a2ave /(len(lhlen)* 60.0*60.0)).filled(-9999.0)
  a2ave       = (a2ave /(hlen* 60.0*60.0)).filled(-9999.0)
  a2ave       = flipud(a2ave.reshape(1200,3600))
  return a2ave

def nonzero(a1in):
  return (a1in !=0.0)
#**
def nonmiss(a1in):
  return (a1in !=miss)
#-----------------------------------------------
for season in lseason:
  for nhour in lnhour:
    #-----------------------------------------------
    tottimes  = ctrack_para.ret_totaldays(iyear,eyear,season) * len(lhour)
    if ( 1       <=100-percent    <10):
      ntoprat    = 0.1
      ntop       = ceil(tottimes* ntoprat)
      segpercent = round(percent%10.0*10)
    elif (0.1    <=100-percent    <1):
      ntoprat    = 0.01
      ntop       = ceil(tottimes* ntoprat)
      segpercent = round(percent%1.0*100)
    elif (0.01   <=100-percent    <0.1):
      ntoprat    = 0.001
      ntop       = ceil(tottimes*ntoprat)
      segpercent = round(percent%0.1*1000)
    elif (0.001  <=100-percent    <0.01):
      ntoprat    = 0.0001
      ntop       = ceil(tottimes*ntoprat)
      segpercent = round(percent%0.01*10000)
    elif (0.0001 <=100-percent    <0.001):
      ntoprat    = 0.00001
      ntop  = ceil(tottimes*ntoprat)
      segpercent = round(percent%0.001*100000)
    else:
      print "the percent value is out of range",percent
      print "it should be >90(%)"
      sys.exit()
    #
    if ntop < 10.0:
      print "'percentile' is too large"
      print "num of samples is ",tottimes
      print "percentile=",percent
      sys.exit()
    #------------------------------------
    #totaldays = ctrack_para.ret_totaldays(iyear, eyear, season)
    wy  = int( 2.0e+9 / ( 4.0*nx_org*ntop*numrat) )
    #wy  = int( 2.0e+8 / ( 4.0*nx_org*ntop*numrat) )
    wy  = min( wy, ny_org)
    wy  = max( wy, 1)
    print "wy=",wy 
    lyfirst = range(0,ny_org,wy)
    lylast  = lyfirst[1:] + [ny_org]
    if lyfirst[-1] == ny_org:
      lyfirst = lyfirst[:-1]
      lylast  = lylast[:-1]
  
    #---- init --------------------------
    a2ptile   = ones([ny_org,nx_org],float32)*miss
    a2one     = ones([ny_org,nx_org],float32)
    #a2count   = zeros([ny_org,nx_org],float32)
    #------------------------------------
    for i in range(len(lyfirst)):
      yfirst    = lyfirst[i]
      ylast     = lylast[i]
      a2count   = zeros([ylast-yfirst,nx_org],float32)
      a3in      = ma.zeros([nhour, ylast-yfirst, nx_org],float32)
      a2one_seg = ma.ones([ylast-yfirst, nx_org],float32)

      itimes     = 0
      itimes_seg = 0
      for year in range(iyear, eyear+1):
        #-------------
        lmon  = ctrack_para.ret_lmon(season)
        for mon in lmon:
          idir  = idir_root + "/%04d%02d"%(year,mon)
          #-- leap year ------
          if (calendar.isleap(year) & (mon==2)):
            eday = 28 
          else:
            eday = calendar.monthrange(year, mon)[1]
  
          #-------------------
          for day in range(iday, eday+1):
            #-------------------
            if (year==iyear)&(mon==1)&(day==1):

              tempdir  ="/home/utsumi/mnt/iis.data2/GSMaP/standard/v5/hourly/%04d/12/31"%(year-1)
              tempname = tempdir + "/gsmap_mvk.%04d12331.2300.v5.222.1.dat.gz"%(year-1)

              if not os.access(tempname, os.F_OK):
                continue
            elif (year==eyear)&(mon==12)&(day==31):

              tempdir  ="/home/utsumi/mnt/iis.data2/GSMaP/standard/v5/hourly/%04d/01/01"%(year+1)
              tempname = tempdir + "/gsmap_mvk.%04d0101.0000.v5.222.1.dat.gz"%(year+1)

              if not os.access(tempname, os.F_OK):
                continue
            #-------------------
            print yfirst, year, mon, day, "nhour=",nhour, "percent=",percent
            #-------------------
            for hour in lhour:
              itimes     = itimes + 1
              itimes_seg = itimes_seg + 1
              icycle     = mod( (itimes -1), nhour)
              #-- load ---------------
              #a2in   = gsmap_func.timeave_gsmap_backward_org(year,mon,day,hour, nhour)
              #-- init --
              if itimes == 1:
                lh_inc = range(nhour) 
                now    = datetime.datetime(year,mon,day,hour)
                for h_inc in lh_inc[1:]:
                  target  = now + datetime.timedelta(hours = -h_inc)
                  year_t  = target.year
                  mon_t   = target.month
                  day_t   = target.day
                  hour_t  = target.hour
 
                  a3in[h_inc] = ma.masked_equal( timeave_gsmap_backward_org(year_t,mon_t,day_t,hour_t,1)[yfirst:ylast,:].copy(),  miss)
              #--
              a2inst_new   = ma.masked_equal( timeave_gsmap_backward_org(year,mon,day,hour,1)[yfirst:ylast,:].copy(),  miss)
              a3in[-icycle] = a2inst_new
              a2in_mask    = ma.any(a3in.mask, axis=0)
              a2in_seg     = ma.masked_array(mean(a3in,axis=0), mask=a2in_mask).filled(miss)

              #-- count --
              a2count = a2count + ma.masked_where(a2in_seg == miss, a2one_seg).filled(0.0)
  
              #-- init ---------------
              #a2in_seg   = a2in[yfirst:ylast, :].copy()
              if itimes == 1:
                a2stck   = a2in_seg
              else:
                a2stck   = r_[a2stck, a2in_seg]
              #-----------------------
              if itimes_seg > (ntop * numrat):
                print "sort!! on ",year,mon,day,hour
                a2stck   = a2stck.reshape(-1,ylast-yfirst,nx_org)
                for iiy in range( (ylast -yfirst)):
                  #iy     = yfirst + iiy
                  iy     = iiy
                  for iix in range(nx_org):
                    ix   = iix
                    a2stck[:,iiy,iix]  = sort(a2stck[:,iiy,iix])
                #**
                a2stck = a2stck[-ntop:]
                a2stck = a2stck.flatten().reshape(-1,nx_org)
                itimes_seg = ntop
      #----------------------------------
      a2stck       = a2stck.reshape(-1,ylast-yfirst,nx_org)
      a2ntop_final = ceil(a2count * ntoprat)
      for iiy in range( (ylast -yfirst)):
        iy     = yfirst + iiy
        print "iy=", iy
        for iix in range(nx_org):
          ix   = iix
          #**
          ntop_final= a2ntop_final[iiy,iix] 
          a1v       = sort(a2stck[:,iiy,iix])
          a1v       = a1v[-ntop_final:]
          #a1v       = a2stck[-ntop_final:,iiy,iix]
          #------------ 
          if (a2count[iiy,iix] < itimes * thmissrat):
            a2ptile[iy,ix]  = miss
          else:
            a2ptile[iy,ix]  = percentile(a1v, segpercent)
          #------------ 
    #----------------------------------
    odir  = odir_root + "/%04d-%04d"%(iyear, eyear)
    ctrack_func.mk_dir(odir)
    #
    soname = odir + "/gsmap_mvk.v5.222.1.movw%02dhr.%3.1f.p%05.2f.%s.sa.dec"%(nhour, thmissrat, percent, season)
    a2ptile.tofile(soname)
    print soname
    
