from numpy import *
from dtanl_fsub import *
import ctrack_func
import calendar
import datetime
import ctrack_fig
#------------------------------------
singleday = False
iyear  = 2003
eyear  = 2003
#lmon   = [6,7,2,4,8,9,11]
lmon   = [7,6]
iday   = 1
sresol = "anl_p"
ny,nx  = 180,360
miss   = -9999.0
#*************************************
#*************************************
def mk_a2dsta_adv_lateral(a2thetaelow,a2thetaeup,a2ulow,a2uup,a2vlow,a2vup,plevlow,plevup):
  adv_thetae_low = dtanl_fsub.mk_a2thermoadv(a2thetaelow.T, a2ulow.T, a2vlow.T).T
  adv_thetae_up  = dtanl_fsub.mk_a2thermoadv(a2thetaeup.T,  a2uup.T,  a2vup.T ).T
  return  (adv_thetae_low - adv_thetae_up) / (plevlow - plevup)

#-------------------------------------
def mk_a2dsta_adv_vertical(a2thetae1, a2thetae3, a2thetae5, a2omega2, a2omega4, plev1, plev2, plev3, plev4, plev5):
  # from lower to higher 1,2,3,4,5
  da2thetae_low    = (a2thetae1 - a2thetae3)/(plev1 - plev3)
  da2thetae_up     = (a2thetae3 - a2thetae5)/(plev3 - plev5)
  #
  return (a2omega2*0.01*da2thetae_low - a2omega4*0.01*da2thetae_up)/(plev2-plev4)

#*************************************
#-------------------------------------
for year in range(iyear,eyear+1):
  for mon in lmon:
    eday  = calendar.monthrange(year,mon)[1]
    #---------------
    if singleday == True:
      eday = iday
    #---------------
    for day in range(iday,eday+1):
      #---- instant value -------
      tname  = "/media/disk2/data/JRA25/sa.one.%s/day/TMP/%04d%02d/%s.TMP.0850hPa.%04d%02d%02d.sa.one"%(sresol, year,mon,sresol,year,mon,day)
      qname  = "/media/disk2/data/JRA25/sa.one.%s/day/SPFH/%04d%02d/%s.SPFH.0850hPa.%04d%02d%02d.sa.one"%(sresol, year,mon, sresol, year,mon,day)
      uname  = "/media/disk2/data/JRA25/sa.one.%s/day/UGRD/%04d%02d/%s.UGRD.0850hPa.%04d%02d%02d.sa.one"%(sresol, year,mon, sresol, year,mon,day)
      vname  = "/media/disk2/data/JRA25/sa.one.%s/day/VGRD/%04d%02d/%s.VGRD.0850hPa.%04d%02d%02d.sa.one"%(sresol, year,mon, sresol, year,mon,day)
      thetaename = "/media/disk2/out/JRA25/sa.one.%s/day/theta_e/%04d%02d/anl_p.thetae.0850hPa.%04d%02d%02d.sa.one"%(sresol,year,mon,year,mon,day)
      #
      a2t      = fromfile(tname, float32).reshape(180,360)
      a2theta  = dtanl_fsub.mk_a2theta(850.0*100, a2t.T).T
      a2q      = fromfile(qname, float32).reshape(180,360)
      a2thetae = fromfile(thetaename, float32).reshape(180,360)
      a2gradtheta  = dtanl_fsub.mk_a2grad_abs_saone(a2theta.T).T
      a2gradq      = dtanl_fsub.mk_a2grad_abs_saone(a2q.T).T
      a2gradthetae = dtanl_fsub.mk_a2grad_abs_saone(a2thetae.T).T

      #--- instant 6-hourly data ---
      tname6h  = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP/%04d%02d/%s.TMP.0850hPa.%04d%02d%02d00.sa.one"%(sresol, year,mon,sresol,year,mon,day)
      qname6h  = "/media/disk2/data/JRA25/sa.one.%s/6hr/SPFH/%04d%02d/%s.SPFH.0850hPa.%04d%02d%02d00.sa.one"%(sresol, year,mon, sresol, year,mon,day)
      #
      a2t6h    = fromfile(tname6h, float32).reshape(ny,nx)
      a2q6h    = fromfile(qname6h, float32).reshape(ny,nx)
      a2theta6h  = dtanl_fsub.mk_a2theta(850.0*100.,   a2t6h.T).T
      a2thetae6h = dtanl_fsub.mk_a2theta_e(850.0*100., a2t6h.T, a2q6h.T).T

      a2gradq6h       = dtanl_fsub.mk_a2grad_abs_saone(a2q6h.T).T
      a2gradtheta6h   = dtanl_fsub.mk_a2grad_abs_saone(a2theta6h.T).T
      a2gradthetae6h  = dtanl_fsub.mk_a2grad_abs_saone(a2thetae6h.T).T
      #***
      #*************************************************************************************************** 
      #*** figure **************************************************************************************** 
      ##****************************************
      #--- figure gradq -------
      figdir   = "/media/disk2/out/JRA25/sa.one.%s/6hr/tenkizu/06h/%04d%02d/gradq"%(sresol, year, mon)
      ctrack_func.mk_dir(figdir)
      bnd = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
      #bnd = False
      if day == iday:
        cbarname = figdir + "/gradq.cbar.png"
      # 6hr ------
      soname     = figdir + "/gradq.6hr.%04d.%02d.%02d.png"%(year,mon,day)
      stitle     = "grad q (1.0e-8 kg/kg/m) %s  6-hourly\n"%(sresol)
      stitle     = stitle + "%04d-%02d-%02d"%(year,mon,day)
      ctrack_fig.mk_pict_saone_reg(a2gradq6h*1.e+8, soname=soname, stitle=stitle, bnd=bnd, mycm="jet",cbarname=cbarname)
      print soname

      # daily ------
      soname     = figdir + "/gradq.day.%04d.%02d.%02d.png"%(year,mon,day)
      stitle     = "grad q (1.0e-8 kg/kg/m) %s  daily   \n"%(sresol)
      stitle     = stitle + "%04d-%02d-%02d"%(year,mon,day)
      ctrack_fig.mk_pict_saone_reg(a2gradq*1.e+8, soname=soname, stitle=stitle, bnd=bnd, mycm="jet",cbarname=cbarname)
      print soname


      #****************************************
      #--- figure gradtheta -------
      figdir   = "/media/disk2/out/JRA25/sa.one.%s/6hr/tenkizu/06h/%04d%02d/grad.theta"%(sresol, year, mon)
      ctrack_func.mk_dir(figdir)
      bnd = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
      #bnd = False
      if day == iday:
        cbarname = figdir + "/grad.theta.cbar.png"
      # 6hr ------
      soname     = figdir + "/grad.theta.6hr.%04d.%02d.%02d.png"%(year,mon,day)
      stitle     = "grad theta (1.0e-5 K/m) %s  6-hourly\n"%(sresol)
      stitle     = stitle + "%04d-%02d-%02d"%(year,mon,day)
      ctrack_fig.mk_pict_saone_reg(a2gradtheta6h*1.e+5, soname=soname, stitle=stitle, bnd=bnd, mycm="jet",cbarname=cbarname)
      print soname

      # daily ------
      soname     = figdir + "/grad.theta.day.%04d.%02d.%02d.png"%(year,mon,day)
      stitle     = "grad theta (1.0e-5 K/m) %s  daily   \n"%(sresol)
      stitle     = stitle + "%04d-%02d-%02d"%(year,mon,day)
      ctrack_fig.mk_pict_saone_reg(a2gradtheta*1.e+5, soname=soname, stitle=stitle, bnd=bnd, mycm="jet",cbarname=cbarname)
      print soname

      #****************************************
      #--- figure gradtheta_e -------
      figdir   = "/media/disk2/out/JRA25/sa.one.%s/6hr/tenkizu/06h/%04d%02d/grad.theta_e"%(sresol, year, mon)
      ctrack_func.mk_dir(figdir)
      bnd = [1.0,2.0,3.0,4.0,5.0,6.0]
      #bnd = False
      if day == iday:
        cbarname = figdir + "/grad.theta_e.cbar.png"
      # 6hr ------
      soname     = figdir + "/grad.theta_e.6hr.%04d.%02d.%02d.png"%(year,mon,day)
      stitle     = "grad theta_e (1.0e-5 K/m) %s  6-hourly\n"%(sresol)
      stitle     = stitle + "%04d-%02d-%02d"%(year,mon,day)
      ctrack_fig.mk_pict_saone_reg(a2gradthetae6h*1.e+5, soname=soname, stitle=stitle, bnd=bnd, mycm="jet",cbarname=cbarname)
      print soname

      # daily ------
      soname     = figdir + "/grad.theta_e.day.%04d.%02d.%02d.png"%(year,mon,day)
      stitle     = "grad theta_e (1.0e-5 K/m) %s  daily   \n"%(sresol)
      stitle     = stitle + "%04d-%02d-%02d"%(year,mon,day)
      ctrack_fig.mk_pict_saone_reg(a2gradthetae*1.e+5, soname=soname, stitle=stitle, bnd=bnd, mycm="jet",cbarname=cbarname)
      print soname


      ##--- figure gradt 6h -------
      ##bnd = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
      #bnd = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
      #ctrack_fig.mk_pict_saone_reg(a2gradt6h*1.e+5, soname="./grad.t.6h.png", bnd=bnd, mycm="jet",cbarname="./grad.t.cbar.png")

      ##--- figure gradt ----------
      ##bnd = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
      #bnd = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
      #ctrack_fig.mk_pict_saone_reg(a2gradt*1.e+5, soname="./grad.t.day.png", bnd=bnd, mycm="jet",cbarname="./grad.t.cbar.png")

      ##--- figure gradthetae 6h ----------
      ##bnd = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
      #bnd = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
      #ctrack_fig.mk_pict_saone_reg(a2gradthetae6h*1.e+5, soname="./grad.thetae.6h.png", bnd=bnd, mycm="jet",cbarname="./grad.t.cbar.png")

      ##--- figure gradthetae 6h ----------
      ##bnd = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
      #bnd = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
      #ctrack_fig.mk_pict_saone_reg(a2gradthetae*1.e+5, soname="./grad.thetae.day.png", bnd=bnd, mycm="jet",cbarname="./grad.t.cbar.png")

      ###--- figure gradqmean ------
      ##bnd = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
      ###bnd = False
      ##ctrack_fig.mk_pict_saone_reg(a2gradqmean*1.e+8, soname="./grad.qmean.png", bnd=bnd, mycm="jet",cbarname="./grad.q.cbar.png")

      ###--- figure gradtmean ------
      ###bnd = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
      ##bnd = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0]
      ##ctrack_fig.mk_pict_saone_reg(a2gradtmean*1.e+5, soname="./grad.tmean.png", bnd=bnd, mycm="jet",cbarname="./grad.t.cbar.png")

      ##--- figure dsta lateral----
      #bnd  = [-0.05, -0.03, -0.01, 0.01, 0.03, 0.05]
      #if len(ldday)==1:
      #  print "AAAA"
      #  bnd  = [-0.09,-0.07,-0.05, -0.03, -0.01, 0.01, 0.03, 0.05, 0.07,0.09]
      #ctrack_fig.mk_pict_saone_reg_symm(a2dsta_adv_lateral, soname="./dsta.late.png", bnd=bnd, mycm="RdBu",cbarname="./dstat.late.cbar.png")

      ##--- figure sta ----
      #bnd  = [-0.025, -0.015, -0.005, 0.005, 0.015, 0.025]
      ##bnd  = [-0.05,-0.03,-0.01,0.0, 0.01, 0.03, 0.05]
      #ctrack_fig.mk_pict_saone_reg_symm(a2sta, soname="./sta.png", bnd=bnd, mycm="RdBu",cbarname="./sta.cbar.png")

      ###--- figure dsta vertical ----
      ##bnd  = [-0.05, -0.03, -0.01, 0.01, 0.03, 0.05]
      ##ctrack_fig.mk_pict_saone_reg_symm(a2dsta_adv_vertical, soname="./dsta.vert.png", bnd=bnd, mycm="RdBu",cbarname="./dstat.vert.cbar.png")
      ###--- figure dsta  ----
      ##bnd  = [-0.05, -0.03, -0.01, 0.01, 0.03, 0.05]
      ##ctrack_fig.mk_pict_saone_reg_symm(a2dsta_adv, soname="./dsta.png", bnd=bnd, mycm="RdBu",cbarname="./dstat.cbar.png")

      ##--- figure adv850 ----
      #bnd   = [-20,-15,-10,-5,0,5,10,15,20]
      #ctrack_fig.mk_pict_saone_reg_symm(a2thetaeadv850, soname="./adv850.png", bnd=bnd, mycm="RdBu",cbarname="./adv.cbar.png")

      ##--- figure adv500 ----
      #bnd   = [-20,-15,-10,-5,0,5,10,15,20]
      #ctrack_fig.mk_pict_saone_reg_symm(a2thetaeadv500, soname="./adv500.png", bnd=bnd, mycm="RdBu",cbarname="./adv.cbar.png")

