from numpy import *
import ctrack_fig
import ctrack_para, cmip_para, tc_para
import ctrack_func, cmip_func, tc_func

lmodel  = ["MIROC5"]
lexpr   = ["historical","rcp85"]
dyrange = {"historical":[1980,1999], "rcp85":[2080,2099]}
#lseason = ["ALL"]
lseason = ["DJF"]
ny,nx   = 180,360
thdura_c= 48
countrad= 300.0 # (km)
miss    = -9999.0

#-------------------------
lllat  = -89.5
lllon  = 0.5
urlat  = 89.5
urlon  = 359.5

#******************************
llkey = [[expr,model,season] for expr in lexpr for model in lmodel for season in lseason]
for expr, model, season in llkey:
  sunit, scalendar = cmip_para.ret_unit_calendar(model,expr)
  ens         = cmip_para.ret_ens(model, expr, "psl")
  iyear,eyear = dyrange[expr]
  lyear       = range(iyear,eyear+1)
  lmon        = ctrack_para.ret_lmon(season)
  #---- init --------
  a2num  = zeros([ny,nx], float32)
  #------------------
  for year in lyear:
    for mon in lmon:
      #---- load -----
      idir_root= "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/exc/freq.%02dh"%(model,expr,thdura_c)
      idir     = idir_root + "/%04d"%(year)

      iname    = idir + "/num.exc.%s.%s.rad%04dkm.%04d.%02d.sa.one"%(model, ens, countrad, year,mon)
      a2num_tmp= fromfile(iname,float32).reshape(ny,nx)
      a2num    = a2num_tmp + a2num
      #--
  #------------------
  totaltime = cmip_para.ret_totaldays_cmip(iyear,eyear,season,sunit=sunit,scalendar=scalendar) *4.0
  a2freq    = a2num / totaltime

  sodir_root = idir_root
  sodir      = sodir_root + "/%04d-%04d.%s"%(iyear,eyear,season)
  soname     = sodir + "/freq.exc.%s.%s.rad%04dkm.%04d-%04d.%s.sa.one"%(model, ens, countrad, iyear,eyear,season)
  ctrack_func.mk_dir(sodir)
  a2freq.tofile(soname)

  #*******************************
  # Figure
  #-----------
  #--- shade       ------
  thorog     = ctrack_para.ret_thorog()
  orogname   = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog/orog.%s.sa.one"%(model,expr,model)
  a2orog     = fromfile(orogname, float32).reshape(ny,nx)
  a2one    = ones([ny,nx],float32)
  a2shade  = ma.masked_where( a2orog >=thorog, a2one).filled(miss)


  bnd        = [0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0]
  figdir     = sodir
  figname    = soname[:-7] + ".png"
  cbarname   = soname[:-7] + ".cbar.png"
  #----------
  stitle   = "freq. %s.ExC season:%s %04d-%04d %s"%(model,season,iyear, eyear,ens)
  mycm     = "Spectral"
  datname  = soname
  a2figdat = fromfile(datname, float32).reshape(ny,nx)

  #-------------------------------
  a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
  ctrack_fig.mk_pict_saone_reg(a2figdat, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, bnd=bnd, mycm=mycm, soname=figname, stitle=stitle, miss=miss, a2shade=a2shade, cbarname=cbarname)
  print figname


