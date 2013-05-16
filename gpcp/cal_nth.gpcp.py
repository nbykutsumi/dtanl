from numpy import *
import ctrack_para
import ctrack_func
import calendar
#------------------------------------------------
iyear = 2001
eyear = 2001
#lseason = ["ALL"]
lseason = ["JJA"]
iday    = 1
ny      = 180
nx      = 360

percent = 99 # (%)
nhour   = 1
#------------------------------------------------
idir_root = "/media/disk2/data/GPCP1DD/v1.2/1dd"
odir_root = "/media/disk2/data/GPCP1DD/v1.2/1dd/ptile"
#***********************************************
#------ function -------------------------------
def nonzero(a1in):
  return (a1in !=0.0)
#-----------------------------------------------
for season in lseason:
  #------------------------------------
  totaldays = ctrack_para.ret_totaldays(iyear, eyear, season)
  wy  = int( 2.0e+8 / ( 4.0*nx*nhour*totaldays) )
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
    for year in range(iyear, eyear+1):
      idir  = idir_root + "/%04d"%(year)
      #-------------
      lmon  = ctrack_para.ret_lmon(season)
      for mon in lmon:
        print yfirst, year, mon
        eday = calendar.monthrange(year, mon)[1]
        for day in range(iday, eday+1):
          itimes = itimes + 1
          #-- name ---------------
          iname  = idir + "/gpcp_1dd_v1.2_p1d.%04d%02d%02d.bn"%(year, mon, day)
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
  soname = odir + "/pr.gpcp.p%04.2f.%s.bn"%(percent, season)
  a2ptile.tofile(soname)
  print soname
  
