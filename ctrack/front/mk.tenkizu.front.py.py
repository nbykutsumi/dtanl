from numpy import *
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import calendar
import subprocess
import os, sys
import Image
import ctrack_func
#------------------------
if len(sys.argv) ==4:
  iyear  = int(sys.argv[1])
  eyear  = int(sys.argv[2])
  mon    = int(sys.argv[3])
  lmon   = [mon]
  resol  = sys.argv[4]
else:
  #singleday = True
  singleday = False
  iyear = 2004
  eyear = 2004
  #lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
  lmon  = [1,6,7,9,12]
  #lmon  = [9,12]
  #lmon  = [7]
  resol   = "anl_p"
#-------------------------
iday  = 1
lhour = [0]
lllat   = 0.0
urlat   = 80.0
lllon   = 70.0
urlon   = 210.0
#lllon = 67.5
#lllat = 0.5
#urlon = 208.5
#urlat = 70.5

plev    = 850*100.0  #(Pa)
thdura  = 6
#thfmasktheta1 = 0.0
#thfmasktheta2 = 0.3


subsize_x   = 800
subsize_y   = 600

#-------------------------------
for year in range(iyear, eyear+1):
  for mon in lmon:
    eday = calendar.monthrange(year, mon)[1]
    #eday = iday
    for day in range(iday, eday+1):
      for hour in lhour:
        lfigname  = []
        #------------------
        if singleday == True:
          if day != iday:
            continue
        #************************
        if (day == iday):
          cbarflag= "True"
        ##************************
        frontdir      = "/media/disk2/out/JRA25/sa.one.%s/6hr/tenkizu/%02dh/%04d%02d/front"%(resol,thdura, year, mon)
        tenkizudir    = "/media/disk2/out/JRA25/sa.one.%s/6hr/tenkizu/%02dh/%04d%02d"%(resol,thdura, year, mon)
        jraprecdir    = "/media/disk2/out/JRA25/sa.one.%s/6hr/tenkizu/%02dh/%04d%02d"%(resol,thdura, year, mon)
        ctrack_func.mk_dir(frontdir) 

        #************************
        # chart front
        chartname = "/media/disk2/out/chart/ASAS/front/%04d%02d/fig/front.ASAS.%04d.%02d.%02d.%02d.png"%(year,mon,year,mon,day,hour)
        charttemp = "/media/disk2/out/chart/ASAS/front/%04d%02d/fig/front.ASAS.%04d.%02d.%02d.%02d.temp.png"%(year,mon,year,mon,day,hour)
        plt.clf()
        figchart  = plt.figure(dpi=100, figsize=(subsize_x/100.,subsize_y/100.))
        axchart   = figchart.add_axes([0,0,1.0,1.0])
        a2chart   = mpimg.imread(chartname)
        a2chart   = a2chart[150:-150,30:-30]
        plt.imshow(a2chart)
        plt.savefig(charttemp) 
        print charttemp



        #************************
        # precipitation
        scmd = "python mk.tenkizu.py %s %s %s %s %s %s %s %s %s %s %s %s"\
                   %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev, cbarflag, thdura, resol)
        subprocess.call(scmd, shell=True)


        #************************
        # front loc 
        thfmasktheta1  = 0.3
        thfmasktheta2  = 4.0
        vtype= "loc.theta_e"
        scmd = "python mk.tenkizu.front.py %s %s %s %s %s %s %s %s %s %s %s %s %s %s"\
                   %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev, cbarflag, thdura, thfmasktheta1, thfmasktheta2, resol)
        subprocess.call(scmd, shell=True)
        iname     = frontdir + "/%02d/front.%s.%04d.%02d.%02d.%02d.M1-%4.2f.M2-%4.2f.png"%(day, vtype, year, mon, day, hour, thfmasktheta1, thfmasktheta2)
        tempfront1   = frontdir + "/%02d/front.%s.%04d.%02d.%02d.%02d.M1-%4.2f.M2-%4.2f.png"%(day, vtype, year, mon, day, hour, thfmasktheta1, thfmasktheta2)
        #************************
        # front loc 
        thfmasktheta1  = 0.7
        thfmasktheta2  = 4.0
        vtype= "loc.theta_e"
        scmd = "python mk.tenkizu.front.py %s %s %s %s %s %s %s %s %s %s %s %s %s %s"\
                   %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev, cbarflag, thdura, thfmasktheta1, thfmasktheta2, resol)
        subprocess.call(scmd, shell=True)
        tempfront2   = frontdir + "/%02d/front.%s.%04d.%02d.%02d.%02d.M1-%4.2f.M2-%4.2f.png"%(day, vtype, year, mon, day, hour, thfmasktheta1, thfmasktheta2)

        #************************
        # front loc 
        thfmasktheta1  = 1.1
        thfmasktheta2  = 4.0
        vtype= "loc.theta_e"
        scmd = "python mk.tenkizu.front.py %s %s %s %s %s %s %s %s %s %s %s %s %s %s"\
                   %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev, cbarflag, thdura, thfmasktheta1, thfmasktheta2, resol)
        subprocess.call(scmd, shell=True)
        tempfront3   = frontdir + "/%02d/front.%s.%04d.%02d.%02d.%02d.M1-%4.2f.M2-%4.2f.png"%(day, vtype, year, mon, day, hour, thfmasktheta1, thfmasktheta2)

        #************************
        # front loc 
        thfmasktheta1  = 0.3
        thfmasktheta2  = 3.0
        vtype= "loc.theta_e"
        scmd = "python mk.tenkizu.front.py %s %s %s %s %s %s %s %s %s %s %s %s %s %s"\
                   %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev, cbarflag, thdura, thfmasktheta1, thfmasktheta2, resol)
        subprocess.call(scmd, shell=True)
        iname     = frontdir + "/%02d/front.%s.%04d.%02d.%02d.%02d.M1-%4.2f.M2-%4.2f.png"%(day, vtype, year, mon, day, hour, thfmasktheta1, thfmasktheta2)
        tempfront4   = frontdir + "/%02d/front.%s.%04d.%02d.%02d.%02d.M1-%4.2f.M2-%4.2f.png"%(day, vtype, year, mon, day, hour, thfmasktheta1, thfmasktheta2)
        #************************
        # front loc 
        thfmasktheta1  = 0.7
        thfmasktheta2  = 3.0
        vtype= "loc.theta_e"
        scmd = "python mk.tenkizu.front.py %s %s %s %s %s %s %s %s %s %s %s %s %s %s"\
                   %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev, cbarflag, thdura, thfmasktheta1, thfmasktheta2, resol)
        subprocess.call(scmd, shell=True)
        tempfront5   = frontdir + "/%02d/front.%s.%04d.%02d.%02d.%02d.M1-%4.2f.M2-%4.2f.png"%(day, vtype, year, mon, day, hour, thfmasktheta1, thfmasktheta2)

        #************************
        # front loc 
        thfmasktheta1  = 1.1
        thfmasktheta2  = 3.0
        vtype= "loc.theta_e"
        scmd = "python mk.tenkizu.front.py %s %s %s %s %s %s %s %s %s %s %s %s %s %s"\
                   %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev, cbarflag, thdura, thfmasktheta1, thfmasktheta2, resol)
        subprocess.call(scmd, shell=True)
        tempfront6   = frontdir + "/%02d/front.%s.%04d.%02d.%02d.%02d.M1-%4.2f.M2-%4.2f.png"%(day, vtype, year, mon, day, hour, thfmasktheta1, thfmasktheta2)


        #************************
        # thetae
        scmd = "python mk.tenkizu.front.others.py %s %s %s %s %s %s %s %s %s %s %s %s"\
                   %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev, cbarflag, thdura, resol)
        subprocess.call(scmd, shell=True)

        ##************************************************
        ## joint figs
        ##************************************************
        figname = tempfront1 
        lfigname.append(figname)
        figname = tempfront2
        lfigname.append(figname)
        figname = tempfront3
        lfigname.append(figname)
        figname = tempfront4
        lfigname.append(figname)
        figname = tempfront5
        lfigname.append(figname)
        figname = tempfront6
        lfigname.append(figname)
        figname = frontdir + "/%02d/tenkizu.thetae.%04d.%02d.%02d.%02d.%04dhPa.png"%(day, year, mon, day, hour, plev*0.01)
        lfigname.append(figname)
        figname = charttemp
        lfigname.append(figname)
        figname = jraprecdir + "/tenkizu.%04d.%02d.%02d.%02d.JRA.png"%(year, mon, day, hour)
        lfigname.append(figname)
        ##--------------------------------
        nsub_x      = 3
        nsub_y      = 3
        full_x      = nsub_x * subsize_x
        full_y      = nsub_y * subsize_y

        pal = Image.new( "RGBA", (full_x, full_y))
        #-----
        isub          = -1
        for subname in lfigname:
          isub        = isub + 1 
          isub_x      = isub % nsub_x
          isub_y      = int(isub / nsub_x)
          ulx         = isub_x* subsize_x
          uly         = isub_y* subsize_y
          im_temp     = Image.open(subname)
          pal.paste( im_temp, (ulx,uly, ulx+subsize_x, uly+subsize_y))
        #-------
        soname_full   = frontdir + "/front.%04d.%02d.%02d.%02d.png"%(year, mon, day, hour)
        pal.save(soname_full)
        print soname_full

        #-- remove --
        os.remove(tempfront1)
        os.remove(tempfront2)
        os.remove(tempfront3)
        os.remove(tempfront4)
        os.remove(tempfront5)
        os.remove(tempfront6)
        os.remove(charttemp)
        print "******************************"
        print "Finish", year,mon,day,hour
        print "******************************"

        #------------

