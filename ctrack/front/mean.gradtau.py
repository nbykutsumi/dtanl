from numpy import *
import ctrack_para
import calendar
import ctrack_fig
from dtanl_fsub import *

lseason = ["ALL"]
iyear  = 1997
eyear  = 2004
iday   = 1
lhour  = [0,6,12,18]

ny  = 180
nx  = 360
plev = 850*100.0
thdura = 6
miss   = -9999.0

#thfmask1 = 0.5
#thfmask2 = 2.0
thfmask1 = 0.3
thfmask2 = 1.0
#********************************************************
def mk_front_loc_contour(a2thermo, a2gradthermo, thfmask1, thfmask2):
  a2fmask1 = dtanl_fsub.mk_a2frontmask1(a2thermo.T).T
  a2fmask2 = dtanl_fsub.mk_a2frontmask2(a2thermo.T).T
  a2fmask1 = a2fmask1 * (1000.0*100.0)**2.0  #[(100km)-2]
  a2fmask2 = a2fmask2 * (1000.0*100.0)       #[(100km)-1]

  (a2grad2x, a2grad2y) = dtanl_fsub.mk_a2grad_saone(a2gradthermo.T)
  a2grad2x = a2grad2x.T
  a2grad2y = a2grad2y.T
  a2loc    = dtanl_fsub.mk_a2axisgrad(a2grad2x.T, a2grad2y.T).T
  a2loc    = dtanl_fsub.mk_a2contour(a2loc.T, 0.0, 0.0, miss_out).T
  a2loc    = ma.masked_equal(a2loc, miss_out)
  a2loc    = ma.masked_where(a2fmask1 < thfmask1, a2loc)
  a2loc    = ma.masked_where(a2fmask2 < thfmask2, a2loc)
  return a2loc

#********************************************************

ntimes = 0
for season in lseason:
  #--- init -------
  a2mthermo = zeros([ny,nx],float32).reshape(ny,nx)
  a2mgrad   = zeros([ny,nx],float32).reshape(ny,nx)
  a2mloc    = zeros([ny,nx],float32).reshape(ny,nx)

  a2sthermo = zeros([ny,nx],float32).reshape(ny,nx)
  a2sgrad   = zeros([ny,nx],float32).reshape(ny,nx)
  a2sloc    = zeros([ny,nx],float32).reshape(ny,nx)

  a2sthermo2 = zeros([ny,nx],float32).reshape(ny,nx)
  a2sgrad2   = zeros([ny,nx],float32).reshape(ny,nx)
  
  #----------------
  for year in range(iyear, eyear+1):
    lmon = ctrack_para.ret_lmon(season)
    for mon in lmon:
      eday = calendar.monthrange(year, mon)[1]
      for day in range(iday,eday+1):
        print day
        for hour in lhour:
          ntimes = ntimes + 1
          #-- q: mixing ratio --------------------------
          qname = "/media/disk2/data/JRA25/sa.one/6hr/SPFH/%04d%02d/anal_p25.SPFH.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
          a2q   = fromfile(qname, float32).reshape(ny,nx)
          
          #-- t: mixing ratio --------------------------
          tname = "/media/disk2/data/JRA25/sa.one/6hr/TMP/%04d%02d/anal_p25.TMP.%04dhPa.%04d%02d%02d%02d.sa.one"%(year, mon, plev*0.01, year, mon, day, hour)
          a2t   = fromfile(tname, float32).reshape(ny,nx)
          
          #-- theta_e -----------------------------------
          a2theta_e = dtanl_fsub.mk_a2theta_e(plev, a2t.T, a2q.T).T

          #-- grad.theta_e ------------------------------------
          a2thermo         = a2theta_e
          a2gradtheta_e    = dtanl_fsub.mk_a2grad_abs_saone(a2thermo.T).T

          #-- loc ---------------------------------------
          a2loc     = mk_front_loc_contour(a2thermo, a2gradtheta_e, thfmask1, thfmask2)
          a2loc     = a2loc.filled(miss)
          a2loc     = ma.masked_greater(a2loc, miss).filled(1.0)
          a2loc     = ma.masked_equal(a2loc, miss).filled(0.0)
 
          #-- sum ---
          a2sthermo        = a2sthermo + a2thermo
          a2sgrad          = a2sgrad   + a2gradtheta_e
          a2sloc           = a2sloc    + a2loc

          #-- sum of square --
          a2sthermo2       = a2sthermo2 + a2thermo**2.0
          a2sgrad2         = a2sgrad2   + a2gradtheta_e**2.0
          
  #-------------------------
  a2mthermo   = a2sthermo / ntimes
  a2mgrad     = a2sgrad   / ntimes
  a2mloc      = a2sloc    / ntimes
  #
  a2stdthermo = (( a2sthermo2 - 2.0*a2mthermo*a2sthermo + ntimes*a2mthermo**2.0) /ntimes)**0.5 /a2mthermo
  a2stdgrad = (( a2sgrad2 - 2.0*a2mgrad*a2sgrad + ntimes*a2mgrad**2.0) /ntimes)**0.5 / a2mgrad
  #-- figure ---------------
  figdir = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/%02dh/mean/fig"
  figdir = "."
  figmthermoname   = figdir + "/mthermo.%s.png"%(season)
  figmgradname     = figdir + "/mgrad.%s.png"%(season)
  figmlocname      = figdir + "/mloc.%s.png"%(season)

  figstdthermoname = figdir + "/std.thermo.%s.png"%(season)
  figstdgradname   = figdir + "/std.grad.%s.png"%(season)

  cbarmthermoname   = figdir + "/mthermo.%s.cbar.png"%(season)
  cbarmgradname     = figdir + "/mgrad.%s.cbar.png"%(season)
  cbarmlocname      = figdir + "/mloc.%s.cbar.png"%(season)
  cbarstdthermoname = figdir + "/std.thermo.%s.cbar.png"%(season)
  cbarstdgradname   = figdir + "/std.grad.%s.cbar.png"%(season)

  #-------------------------
  #ctrack_fig.mk_pict_saone_reg(a2in=a2mthermo, soname=figmthermoname, cbarname=cbarmthermoname)
  #ctrack_fig.mk_pict_saone_reg(a2in=a2stdthermo, soname=figstdthermoname, cbarname=cbarstdthermoname)
  #ctrack_fig.mk_pict_saone_reg(a2in=a2mgrad, soname=figmgradname, cbarname=cbarmgradname)
  #ctrack_fig.mk_pict_saone_reg(a2in=a2stdgrad, soname=figstdgradname, cbarname=cbarstdgradname)
  ctrack_fig.mk_pict_saone_reg(a2in=a2mloc, soname=figmlocname, cbarname=cbarmlocname)
  #-------------------------
