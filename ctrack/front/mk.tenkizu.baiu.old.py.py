import calendar
import subprocess
import os
import Image
#------------------------

iyear = 2004
eyear = 2004
#lmon  = [7,6]
lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
iday  = 1
lhour = [0]
#lllat   = 0.0
#urlat   = 80.0
#lllon   = 60.0
#urlon   = 190.0
lllon = 67.5
lllat = 0.5
urlon = 208.5
urlat = 70.5

plev    = 850*100.0  #(Pa)
thdura  = 6
u850min = 5.0
duup_min={}
duup_min[500*100] = 10.0  # (m/s)
duup_min[250*100] = 14.0  # (m/s)

qmin    = 10.0*1.0e-3
thfmasktheta1 = 0.0
thfmasktheta2 = 0.6

for year in range(iyear, eyear+1):
  for mon in lmon:
    eday = calendar.monthrange(year, mon)[1]
    #eday = iday
    for day in range(iday, eday+1):
      for hour in lhour:
        lfigname  = []
        #************************
        if (day == iday):
          cbarflag= "True"
        #************************
        baiudir    = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/%02dh/%04d%02d/baiu"%(thdura, year, mon)
        tenkizudir = "/media/disk2/out/JRA25/sa.one/6hr/tenkizu/%02dh/%04d%02d"%(thdura, year, mon)
        ##************************
        ## precipitation
        #scmd = "python mk.tenkizu.py %s %s %s %s %s %s %s %s %s %s %s"\
        #           %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev, cbarflag, thdura)
        #subprocess.call(scmd, shell=True)


        #************************
        # baiu front loc @ 500hPa
        plev_up = 500.0*100.0
        scmd = "python mk.tenkizu.baiu.py %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s"\
                   %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev, cbarflag, thdura, plev_up, u850min, duup_min[plev_up], qmin, thfmasktheta1, thfmasktheta2)
        subprocess.call(scmd, shell=True)


        #************************
        # baiu front loc @ 250hPa
        plev_up = 250.0*100.0
        scmd = "python mk.tenkizu.baiu.py %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s"\
                   %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev, cbarflag, thdura, plev_up, u850min, duup_min[plev_up], qmin, thfmasktheta1, thfmasktheta2)
        subprocess.call(scmd, shell=True)

        ##************************
        ## zonal wind @ 850hPa
        #plev_wind = 850.0*100.0
        #scmd = "python mk.tenkizu.baiu.wind.py %s %s %s %s %s %s %s %s %s %s %s"\
        #           %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev_wind, cbarflag, thdura)
        #subprocess.call(scmd, shell=True)

        ##************************
        ## zonal wind @ 500hPa
        #plev_wind = 500.0*100.0
        #scmd = "python mk.tenkizu.baiu.wind.py %s %s %s %s %s %s %s %s %s %s %s"\
        #           %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev_wind, cbarflag, thdura)
        #subprocess.call(scmd, shell=True)

        ##************************
        ## zonal wind @ 250hPa
        #plev_wind = 250.0*100.0
        #scmd = "python mk.tenkizu.baiu.wind.py %s %s %s %s %s %s %s %s %s %s %s"\
        #           %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev_wind, cbarflag, thdura)
        #subprocess.call(scmd, shell=True)

        #************************
        # thermo, mixing ratio & thetae
        scmd = "python mk.tenkizu.baiu.others.py %s %s %s %s %s %s %s %s %s %s %s"\
                   %(year, mon, day, hour, lllat, urlat, lllon, urlon, plev, cbarflag, thdura)
        subprocess.call(scmd, shell=True)

        #************************************************
        # joint figs
        #************************************************
        figname = baiudir + "/%02d/baiu.loc.theta_e.%04d.%02d.%02d.%02d.ulev%04dhPa.png"%(day, year, mon, day, hour, 500)
        lfigname.append(figname)
        figname = baiudir + "/%02d/baiu.loc.theta_e.%04d.%02d.%02d.%02d.ulev%04dhPa.png"%(day, year, mon, day, hour, 250)
        lfigname.append(figname)
        figname = baiudir + "/%02d/tenkizu.thetae.%04d.%02d.%02d.%02d.%04dhPa.png"%(day, year, mon, day, hour, plev*0.01)
        lfigname.append(figname)
        figname = baiudir + "/%02d/tenkizu.wind.%04d.%02d.%02d.%02d.%04dhPa.png"%(day, year, mon, day, hour, 500)
        lfigname.append(figname)
        figname = baiudir + "/%02d/tenkizu.wind.%04d.%02d.%02d.%02d.%04dhPa.png"%(day, year, mon, day, hour, 250)
        lfigname.append(figname)
        figname = baiudir + "/%02d/tenkizu.wind.%04d.%02d.%02d.%02d.%04dhPa.png"%(day, year, mon, day, hour, 850)
        lfigname.append(figname)
        figname = baiudir + "/%02d/tenkizu.q.%04d.%02d.%02d.%02d.%04dhPa.png"%(day, year, mon, day, hour, plev*0.01)
        lfigname.append(figname)
        figname = tenkizudir + "/tenkizu.%04d.%02d.%02d.%02d.GSMaP.png"%(year, mon, day, hour)
        lfigname.append(figname)
        figname = tenkizudir + "/tenkizu.%04d.%02d.%02d.%02d.JRA.png"%(year, mon, day, hour)
        lfigname.append(figname)
        #--------------------------------
        nsub_x      = 3
        nsub_y      = 3
        subsize_x   = 800
        subsize_y   = 600
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
        soname_full   = baiudir + "/baiu.%04d.%02d.%02d.%02d.png"%(year, mon, day, hour)
        pal.save(soname_full)
        print soname_full





