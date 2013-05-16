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
  totaldays = ctrack_para.ret_totaldays(iyear, eyear, season)
  wy  = int( 1.0e+8 / ( 4.0*nx*nhour*totaldays) )
  wy  = min( wy, ny)
  wy  = max( wy, 1)
  
  lyfirst = range(0,ny,wy)
  lylast  = lyfirst[1:] + [ny]
  if lyfirst[-1] == ny:
    lyfirst = lyfirst[:-1]
    lylast  = lylast[:-1]

  #---- init --------------------------
  a2ptile   = zeros([ny,nx],float32)

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
            iname  = idir + "/fcst_phy2m.PR.%04d%02d%02d%02d.sa.one"%(year, mon, day,hour)
            a2in   = fromfile(iname, float32).reshape(ny,nx)
            #-- init ---------------
            a2in_seg   = a2in[yfirst:ylast, :]
            if itimes == 1:
              a2stck   = a2in_seg
            else:
              a2stck   = r_[a2stck, a2in_seg]
            #-----------------------
    #----------------------------------
    a2stck   = a2stck.reshape(-1,ylast-yfirst,nx)
      
    for iiy in range( (ylast -yfirst)):
      iy     = yfirst + iiy
      print "iy=", iy
      for iix in range(nx):
        ix   = iix
        #
        a1v       = a2stck[:,iiy,iix]
        a1nonzero = filter(nonzero, a1v)
        #------------ 
        if len(a1nonzero) == 0.0:
          a2ptile[iy,ix]  = 0.0
        else:
          a2ptile[iy,ix]  = percentile(a1v, percent)
        #------------ 
  #----------------------------------
  odir  = odir_root + "/%04d-%04d"%(iyear, eyear)
  ctrack_func.mk_dir(odir)
  #
  soname = odir + "/fcst_phy2m.PR.p%04.2f.%s.sa.one"%(percent, season)
  a2ptile.tofile(soname)
  print soname
  
