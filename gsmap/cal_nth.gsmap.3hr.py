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
ny_org  = 120
nx_org  = 360
lhour   = [0,6,12,18]
percent = 99 # (%)
nhour   = len(lhour)
miss    = -9999.0
thmissrat = 0.9
#------------------------------------------------

idir_root = "/media/disk2/data/GSMaP/sa.one/3hr/ptot"
odir_root = "/media/disk2/data/GSMaP/sa.one/3hr/ptot/ptile"
#***********************************************
#------ function -------------------------------
def nonzero(a1in):
  return (a1in !=0.0)
#**
def nonmiss(a1in):
  return (a1in !=0.0)

#-----------------------------------------------
for season in lseason:
  #------------------------------------
  totaldays = ctrack_para.ret_totaldays(iyear, eyear, season)
  wy  = int( 1.0e+8 / ( 4.0*nx_org*nhour*totaldays) )
  wy  = min( wy, ny_org)
  wy  = max( wy, 1)
  
  lyfirst = range(0,ny_org,wy)
  lylast  = lyfirst[1:] + [ny_org]
  if lyfirst[-1] == ny_org:
    lyfirst = lyfirst[:-1]
    lylast  = lylast[:-1]

  #---- init --------------------------
  a2ptile   = ones([ny_org,nx_org],float32)*miss

  #------------------------------------
  for i in range(len(lyfirst)):
    yfirst    = lyfirst[i]
    ylast     = lylast[i]
    itimes  = 0
    a2stck  = 0
    for year in range(iyear, eyear+1):
      #-------------
      lmon  = ctrack_para.ret_lmon(season)
      for mon in lmon:
        idir  = idir_root + "/%04d%02d"%(year,mon)
        print yfirst, year, mon
        #-- leap year ------
        if (calendar.isleap(year) & (mon==2)):
          eday = 28 
        else:
          eday = calendar.monthrange(year, mon)[1]
        #-------------------
        for day in range(iday, eday+1):
          for hour in lhour:
            itimes = itimes + 1
            #-- name ---------------
            iname  = idir + "/gsmap_mvk.3rh.%04d%02d%02d.%02d00.v5.222.1.sa.one"%(year, mon, day, hour)
            a2in   = fromfile(iname, float32).reshape(ny_org,nx_org)
            #-- init ---------------
            a2in_seg   = a2in[yfirst:ylast, :].copy()
            if itimes == 1:
              a2stck   = a2in_seg
            else:
              a2stck   = r_[a2stck, a2in_seg]
            #-----------------------
    #----------------------------------
    a2stck   = a2stck.reshape(-1,ylast-yfirst,nx_org)
      
    for iiy in range( (ylast -yfirst)):
      iy     = yfirst + iiy
      print "iy=", iy
      for iix in range(nx_org):
        ix   = iix
        #
        a1v       = a2stck[:,iiy,iix]
        #a1nonzero = filter(nonzero, a1v)
        a1nonmiss = filter(nonmiss, a1v)
        #------------ 
        if len(a1nonmiss) < itimes*thmissrat :
          a2ptile[iy,ix]  = miss
        else:
          a2ptile[iy,ix]  = percentile(a1v, percent)
        #------------ 
  #----------------------------------
  odir  = odir_root + "/%04d-%04d"%(iyear, eyear)
  ctrack_func.mk_dir(odir)
  #
  soname = odir + "/gsmap_mvk.3rh.v5.222.1.p%04.2f.%s.sa.one"%(percent, season)
  a2ptile.tofile(soname)
  print soname
  
