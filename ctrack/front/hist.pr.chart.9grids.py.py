from numpy import *
from matplotlib.pyplot import *
import ctrack_para
import ctrack_func, myfunc
#*******************************
iyear = 2001
eyear = 2009
#eyear = 2001
lyear = range(iyear,eyear+1)
lftype  = [1,2,3,4]
lseason = ["ALL"]
lregion = ["JPN"]

wbin      = 0.5
#histrange = (0.0, 30.0*wbin)
histrange = (0.0, 30.0)
vmin      = 0.01
#*******************************

idir_root  = "/media/disk2/out/chart/ASAS/pr.max.9grids"
odir_root  = idir_root

for region in lregion:
  for season in lseason:
    lmon  = ctrack_para.ret_lmon(season)
    a1out = array([],float32)
    for ftype in lftype:
      #*********************
      # -- init ------------
      a1stck  = array([],float32)
      #*********************
      for year in lyear:
        idir  = idir_root + "/%04d"%(year)
        for mon in lmon:
          iname   = idir + "/pr.max.9grids.%s.%02d.f%s.bn"%(region,mon,ftype)
          a_seg   = fromfile(iname,float32) * 60.0*60.0  # (mm/hour)
          a1stck  = r_[ a1stck, a_seg ]
      #*********************
      # -- count zero -----
      nzero    = len(ma.masked_greater(a1stck, vmin).compressed())
      a1nonzero= ma.masked_less_equal(a1stck, vmin).compressed()

      # -- hist ------------
      lhist    = hist(a1nonzero, bins = histrange[1]/wbin, range=histrange)
      a1num    = map(float, lhist[0])
      a1bound  = lhist[1]
      #
      a1bins   = (a1bound[1:] + a1bound[:-1])/2.0

      print "f",ftype,mean(a1stck),mean(a1nonzero)

      # -- joint zero and non-zero --
      a1bins   = r_[array([0.0],float32), a1bins]
      a1num    = r_[array([nzero],float32), a1num]

      # -- freq -----------
      a1rfreq  = array(a1num,float32) / len(a1stck)

      #*********************
      a1out    = r_[a1out, a1rfreq]
    #*********************
    #-- reshape ----------
    a1out  = r_[ a1bins, a1out ]
    a2out  = a1out.reshape(5,-1).T
    sout   = myfunc.a2_to_csv(a2out)
    sout   = ",1,2,3,4\n" + sout    

    #*********************
    #-- write ------------
    odir     = odir_root + "/%04d-%04d.%s"%(iyear,eyear,season)
    ctrack_func.mk_dir(odir)
    oname    = odir  + "/rfreq.pr.max.9grids.%s.%s.wbin.%4.2f.vmin.%06.4f.csv"%(region,season, wbin, vmin)
    f=open(oname,"w"); f.write(sout); f.close()
    print oname



