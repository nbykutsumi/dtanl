from numpy import *
import ctrack_para, ctrack_func
import matplotlib
import matplotlib.pyplot as plt
import ctrack_func

#----------------------------
calcflag = True
#calcflag = False
iyear    = 2007
#iyear    = 2000
eyear    = 2010
lseason  = ["ALL"]
#lftype   = [1,2,3,4]
lftype   = [4]
ldistkm  = [200]
sresol   = "anl_p"
nbin     = 100.0
#lvtype   = ["theta","theta_e"]
lvtype   = ["theta_e"]
dbackgroundave = {"theta":0.90, "theta_e":1.84}
#----------------------------
lyear = range(iyear,eyear+1)
for season in lseason:
  lmon  = ctrack_para.ret_lmon(season)
  for distkm in ldistkm:
    for vtype in lvtype:
      #-------------------
      dy = {}
      dx = {}
      #-------------------
      if calcflag ==True:
        for ftype in lftype:
          #-- init ---------
          a1out   =array([],float32)
          #-----------------
          for year in lyear:
            for mon in lmon:
              sidir   = "/media/disk2/out/JRA25/sa.one.%s/6hr/front/valid/%04d.%02d"%(sresol,year,mon)
              siname  = sidir + "/a1grad%s.%04dkm.%s.bn"%(vtype,distkm, ftype)
              #
              a1in = fromfile(siname,float32)
              #
              a1out = r_[a1out, a1in]
          #-----------------
          a1out = sort(a1out)
          #-----------------
          sodir  = "/media/disk2/out/JRA25/sa.one.%s/6hr/front/valid/%04d-%04d"%(sresol,iyear,eyear)
          soname = sodir + "/a1grad%s.%04dkm.%s.%s.bn"%(vtype,distkm, season, ftype)  
          ctrack_func.mk_dir(sodir)
          a1out.tofile(soname)
          #-----------------
          ytmp, xtmp, patches = plt.hist(a1out*1000.0*100.0, bins=nbin)  # K/m --> K/100km     

          #******************
          # PDF
          #-- convert to PDF --
          wbin = xtmp[1] - xtmp[0]
          ay = ytmp / (sum(ytmp)*wbin)
          ax = (xtmp[:-1] + xtmp[1:])/2.0
          #
          ay = array(ay,float32)
          ax = array(ax,float32)
  
          #---- write PDF -----
          pdfyname   = sodir + "/pdf.x.grad%s.%04dkm.%s.%s.bn"%(vtype,distkm,season,ftype)
          pdfxname   = sodir + "/pdf.y.grad%s.%04dkm.%s.%s.bn"%(vtype,distkm,season,ftype)
          #
          ax.tofile(pdfxname)
          ay.tofile(pdfyname)
      

          #******************
          # CDF
          #-- convert to CDF --
          acy = ( ytmp / float(sum(ytmp)) ).cumsum()
          acx = (xtmp[:-1] + xtmp[1:])/2.0

          acy = array(acy,float32)
          acx = array(acx,float32)
          #---- write CDF -----
          cdfyname   = sodir + "/cdf.x.grad%s.%04dkm.%s.%s.bn"%(vtype,distkm,season,ftype)
          cdfxname   = sodir + "/cdf.y.grad%s.%04dkm.%s.%s.bn"%(vtype,distkm,season,ftype)
          #
          acx.tofile(cdfxname)
          acy.tofile(cdfyname)
 

      #***********************
      ##--- PDF figure ---
      figplot  = plt.figure()
      axplot   = figplot.add_axes([0.2, 0.2, 0.7, 0.7])
      #-- ftypes --
      dname   = {1: "warm", 2:"cold", 3:"occ", 4:"stat"}
      dstyle  = {1: "-"   , 2:"--"  , 3:":"  , 4:"-."  }
      #------------
      sodir      = "/media/disk2/out/JRA25/sa.one.%s/6hr/front/valid/%04d-%04d"%(sresol,iyear,eyear)

      for ftype in lftype:
        pdfyname   = sodir + "/pdf.x.grad%s.%04dkm.%s.%s.bn"%(vtype,distkm,season,ftype)
        pdfxname   = sodir + "/pdf.y.grad%s.%04dkm.%s.%s.bn"%(vtype,distkm,season,ftype)

        ly    = fromfile(pdfyname, float32)
        lx    = fromfile(pdfxname, float32)
        axplot.plot(lx, ly, color="k", linewidth=3, linestyle=dstyle[ftype])
      #-- legend --
      legend = axplot.legend(dname.values(), )
      for label in legend.get_texts():
        label.set_fontsize(20)

      for line in legend.get_lines():
        line.set_linewidth(3.0)
      #-- ticks ---
      plt.xticks(fontsize=20)
      plt.yticks(fontsize=20)
      #-- label ---
      plt.xlabel("gradient (K/100km)",fontsize=20)
      plt.ylabel("probability density",fontsize=20)
      #-- title ---
      plt.title("%s gradient"%(vtype),fontsize=20)

      #------------
      figdir = sodir + "/pict"
      ctrack_func.mk_dir(figdir)
      figname = figdir + "/pdf.grad%s.%04d-%04d.%04dkm.%s.png"%(vtype,iyear,eyear,distkm,season)
      figplot.savefig(figname) 
      print figname

      #***********************
      ##--- CDF figure ---
      figplot  = plt.figure()
      axplot   = figplot.add_axes([0.2, 0.2, 0.7, 0.7])
      #-- ftypes --
      dname   = {1: "warm", 2:"cold", 3:"occ", 4:"stat"}
      dstyle  = {1: "-"   , 2:"--"  , 3:":"  , 4:"-."  }
      #------------
      sodir      = "/media/disk2/out/JRA25/sa.one.%s/6hr/front/valid/%04d-%04d"%(sresol,iyear,eyear)

      for ftype in lftype:
        cdfyname   = sodir + "/cdf.x.grad%s.%04dkm.%s.%s.bn"%(vtype,distkm,season,ftype)
        cdfxname   = sodir + "/cdf.y.grad%s.%04dkm.%s.%s.bn"%(vtype,distkm,season,ftype)

        ly    = fromfile(cdfyname, float32)
        lx    = fromfile(cdfxname, float32)
        axplot.plot(lx, ly, color="k", linewidth=3, linestyle=dstyle[ftype])

      #-- background ave ----
      xbackgroundave = dbackgroundave[vtype]
      axplot.plot([xbackgroundave, xbackgroundave], [0.0,1.0], linewidth=1.0, color="k")

      #-- legend --
      legend = axplot.legend(dname.values())
      for label in legend.get_texts():
        label.set_fontsize(20)

      for line in legend.get_lines():
        line.set_linewidth(3.0)
      #-- ticks ---
      plt.xticks(fontsize=20)
      plt.yticks(fontsize=20)
      #-- label ---
      plt.xlabel("gradient (K/100km)",fontsize=20)
      plt.ylabel("cumulative density",fontsize=20)
      #-- title ---
      plt.title("%s gradient"%(vtype),fontsize=20)

      #------------
      figdir = sodir + "/pict"
      ctrack_func.mk_dir(figdir)
      figname = figdir + "/cdf.grad%s.%04d-%04d.%04dkm.%s.png"%(vtype,iyear,eyear,distkm,season)
      figplot.savefig(figname) 
      print figname

  
