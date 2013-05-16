from numpy import *
import ctrack_para
import ctrack_func
import calendar
#------------------------------------------------
iyear = 2001
eyear = 2001
#lseason = ["ALL"]
lseason = [1]
iday    = 1
ny      = 180
nx      = 360
lhour   = [0,6,12,18]
percent = 99 # (%)
nhour   = len(lhour)
numrat  = 1.5  # numrat *ntop data will be sotred
miss    = -9999.0
#------------------------------------------------
idir_root = "/media/disk2/data/JRA25/sa.one/6hr/PR"
odir_root = "/media/disk2/data/JRA25/sa.one/6hr/PR/ptile"
#***********************************************
#------ function -------------------------------
def nonzero(a1in):
  return (a1in !=0.0)
#-----------------------------------------------
for season in lseason:
  #------------------------------------
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
    print "it shoudl be >90(%)"
    sys.exit()
  #
  if ntop < 10.0:
    print "'percentile' is too large"
    print "num of samples is ",tottimes
    print "percentile=",percent
    sys.exit()
  #------------------------------------
  wy  = int( 2.0e+8 / ( 4.0*nx*ntop*numrat) )
  wy  = min( wy, ny)
  wy  = max( wy, 1)
  print "wy=",wy
  lyfirst = range(0,ny,wy)
  lylast  = lyfirst[1:] + [ny]
  if lyfirst[-1] == ny:
    lyfirst = lyfirst[:-1]
    lylast  = lylast[:-1]

  #---- init --------------------------
  a2ptile   = ones([ny,nx],float32) * miss
  #------------------------------------
  for i in range(len(lyfirst)):
    yfirst    = lyfirst[i]
    ylast     = lylast[i]
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
          print yfirst, year, mon, day
          for hour in lhour:
            itimes      = itimes + 1
            itimes_seg  = itimes_seg + 1
            #-- name ---------------
            iname  = idir + "/fcst_phy2m.PR.%04d%02d%02d%02d.sa.one"%(year, mon, day,hour)
            a2in   = fromfile(iname, float32).reshape(ny,nx)
            #-- init ---------------
            a2in_seg   = a2in[yfirst:ylast, :]
            if itimes == 1:
              a2stck   = a2in_seg
            else:
              a2stck   = r_[a2stck, a2in_seg]
            #-----------------------
            if itimes_seg > (ntop * numrat):
              print "sort!! on ",year,mon,day,hour
              a2stck   = a2stck.reshape(-1,ylast-yfirst,nx)
              for iiy in range( (ylast -yfirst)):
                iy     = yfirst + iiy
                for iix in range(nx):
                  ix   = iix
                  a2stck[:,iiy,iix]  = sort(a2stck[:,iiy,iix])
              #**
              a2stck = a2stck[-ntop:]
              a2stck = a2stck.flatten().reshape(-1,nx)
              itimes_seg = ntop

    #----------------------------------
    a2stck   = a2stck.reshape(-1,ylast-yfirst,nx)
      
    for iiy in range( (ylast -yfirst)):
      iy     = yfirst + iiy
      print "iy=", iy
      for iix in range(nx):
        ix   = iix
        #
        a1v       = sort(a2stck[:,iiy,iix])
        a1v       = a1v[-ntop:]
        a2ptile[iy,ix]  = percentile(a1v, segpercent)
        #------------ 
  #----------------------------------
  odir  = odir_root + "/%04d-%04d"%(iyear, eyear)
  ctrack_func.mk_dir(odir)
  #
  soname = odir + "/fcst_phy2m.PR.p%04.2f.%s.sa.one"%(percent, season)
  a2ptile.tofile(soname)
  print soname
  
