from numpy import *
import sys
import ctrack_func
import ctrack_para
import matplotlib.pyplot as plt
#--------------------------
if len(sys.argv) ==1:
  iyear   = 2001
  eyear   = 2001
  lseason = [1,2,3,4,5,6,7,8,9,10,11,12]
  #lseason = [1]
  #lplev   = [925, 850, 700, 600, 500, 300, 250]
  lplev  = [850]
  lvtype = ["theta"]
  figflag = True
elif len(sys.argv) ==6:
  iyear   = int(sys.argv[1])
  eyear   = int(sys.argv[2])
  mon     = int(sys.argv[3])
  plev    = float(sys.argv[4])
  vtype   = sys.argv[5]
  lseason = [mon]
  lplev   = [plev]
  lvtype  = [vtype]
  figflag = False
else:
  print "usage: cmd [iyear] [eyaer] [mon] [plev (hPa)]"
  sys.exit()
#--------------------------
nx,ny  = 360,180 
#--------------------------
for vtype in lvtype:
  for season in lseason:
    lmon = ctrack_para.ret_lmon(season)
    for plev in lplev:
      #--- init --------------
      a2sum      = zeros([ny,nx],float32)
      #-----------------------
      for year in range(iyear, eyear+1):
        for mon in lmon:
          print plev, year, mon
          idir   = "/media/disk2/out/chart/ASAS/front/agg/%04d/%02d"%(year,mon)
          iname  = idir + "/sum.%s.%04dhPa.sa.one"%(vtype,plev)
          a2sum  = a2sum + fromfile(iname,float32).reshape(ny,nx)
      #--------------------------
      ntimes     = ctrack_para.ret_totaldays(iyear,eyear,season) * 4.0
      a2mean     = a2sum / ntimes
      #--------------------------
      odir       = "/media/disk2/out/chart/ASAS/front/agg/%04d-%04d/%s"%(iyear,eyear,season)
      ctrack_func.mk_dir(odir)
      oname      = odir + "/mean.%s.%04dhPa.sa.one"%(vtype,plev)
      a2mean.tofile(oname)
      print oname
    
    #------- contour figure -----
    if figflag == True:
      a2cont   = zeros([len(lplev), ny],float32)
      for iplev in range(len(lplev)):
        plev       = lplev[iplev]
        odir       = "/media/disk2/out/chart/ASAS/front/agg/%04d-%04d/%s"%(iyear,eyear,season)
        thetaname  = odir + "/mean.%s.%04dhPa.sa.one"%(vtype,plev)
        a2mean     = fromfile(thetaname, float32).reshape(ny,nx)
        print thetaname
        print plev, mean(a2mean)
        pictdir    = odir + "/pict" 
        ctrack_func.mk_dir(pictdir)
        a2cont[iplev]  = mean(a2mean, axis=1)
      #--
      plt.clf()
      figcont      = plt.figure()
      axcont       = figcont.add_axes([0.2,0.2,0.7,0.7])
      #-- for contour--
      lx           = arange(-89.5, 89.5+1, 1.0)
      ly           = lplev
      a2x, a2y     = meshgrid(lx, ly)
  
      levels       = arange(200,400,5)
      CS           = axcont.contour(a2x, a2y, a2cont, levels=levels, colors="k")
      #-- inversed axis ---
      axcont.invert_yaxis()
      #-- label -----------
      plt.clabel(CS, levels[::2,], fontsize=18, fmt="%d")
      #---
      contname     = pictdir + "/cont.%s.%04d-%04d.%s.png"%(vtype,iyear,eyear,season)
      figcont.savefig(contname)
      print contname
  
  
