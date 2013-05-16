from numpy import *
from dtanl_fsub import *
import calendar
import ctrack_fig
import ctrack_para
import ctrack_func
from ctrack_fsub import *

#----------------------------------------------------
sresol    = "anl_p"
#singleday =True
singleday = False
#figflag   = True
figflag   = False
iyear = 2001
eyear = 2001
lseason = [1,2,3,4,5,6,7,8,9,10,11,12]
#lseason = [7]
iday  = 1
ny    = 180
nx    = 360
lhour = [0,6,12,18]
#lhour = [0]
thorog = 1500 # (m)


lregion = ["W.JAPAN","E.JAPAN","ALL.JAPAN"]

#---------------------------
def ret_corners(region):
  if region == "ALL.JAPAN":
    lllat = 0.0
    lllon = 90
    urlat = 80
    urlon = 210
  elif region == "W.JAPAN": 
    lllat = 0.0
    lllon = 90.0
    urlat = 80.0
    urlon = 135.0
  elif region == "E.JAPAN":
    lllat = 0.0
    lllon = 135.0
    urlat = 80.0
    urlon = 210.0
  #
  return lllat, lllon, urlat, urlon
#---------------------------
# for transform
def ret_xydom(region):
  lllat,lllon,urlat,urlon = ret_corners(region)
  xdom_saone_first = int((lllon - 0.5 + 0.5)/1.0)
  xdom_saone_last  = int((urlon - 0.5 + 0.5)/1.0)
  ydom_saone_first = int((lllat -(-89.5) + 0.5)/1.0)
  ydom_saone_last  = int((urlat -(-89.5) + 0.5)/1.0)
  return xdom_saone_first, xdom_saone_last, ydom_saone_first, ydom_saone_last
#************************


plev  = 850*100.0
#dist  = 300.0 * 1000.0  #[m]
#dist  = 300.0 * 1000.0  #[m]
dist  = ctrack_para.ret_highsidedist()  # [m]
#ndist = 2.0  #[deg]
#-----
miss  = -9999.0
chartdir_root = "/media/disk2/out/chart/ASAS/front"
tdir_root     = "/media/disk2/data/JRA25/sa.one.%s/6hr/TMP"%(sresol)
qdir_root     = "/media/disk2/data/JRA25/sa.one.%s/6hr/SPFH"%(sresol)
lftype = [1,2,3,4]
#------------------------
a2one    = ones([ny,nx],float32)
#-- orog --------------------
orogname = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
a2orog   = fromfile(orogname, float32).reshape(ny,nx)
#-- domain ------------------
domname  = "/media/disk2/out/chart/ASAS/const/domainmask_saone.ASAS.2000-2006.bn"
a2domain = fromfile(domname , float32).reshape(ny,nx)
#-- shade  ------------------
a2shade  = ma.masked_where( a2domain==0.0, a2one).filled(miss)
a2shade  = ma.masked_where( a2orog > thorog, a2shade).filled(miss)


#-- init ----------------
a2one      = ones([ny,nx],float32)
dgradtv    = {}
dcount     = {}

dshighside = {}
dshighside2= {}
dmhighside = {}
dstdhighside = {}

for region in lregion:
  for season in lseason:
    for ftype in lftype:
      dgradtv[region, season, ftype]    = 0
  
      dshighside[region, season, ftype]  = 0
      dshighside2[region, season, ftype] = 0
  
      dcount[region, season, ftype]     = 0
#------------------------
for season in lseason:
  lmon     = ctrack_para.ret_lmon(season)
  for year in range(iyear, eyear+1):
    for mon in lmon:
      print season, year, mon
      #----------------
      if singleday ==True:
        eday = iday
      else:
        eday = calendar.monthrange(year,mon)[1]
      #----------------
      for day in range(iday, eday+1):
        for hour in lhour:
          chartdir  = chartdir_root + "/%04d%02d"%(year,mon)
          tdir      = tdir_root     + "/%04d%02d"%(year,mon)
          qdir      = qdir_root     + "/%04d%02d"%(year,mon)
          #
          chartname = chartdir      + "/front.ASAS.%04d.%02d.%02d.%02d.saone"%(year,mon,day,hour)
          tname     = tdir          + "/%s.TMP.0850hPa.%04d%02d%02d%02d.sa.one"%(sresol,year,mon,day,hour)
          qname     = qdir          + "/%s.SPFH.0850hPa.%04d%02d%02d%02d.sa.one"%(sresol,year,mon,day,hour)
          a2chart   = fromfile(chartname, float32).reshape(ny,nx)
          a2t       = fromfile(tname,     float32).reshape(ny,nx)
          a2q       = fromfile(qname,     float32).reshape(ny,nx)
          a2tv      = a2t * (1.0+0.61*a2q)
          a2theta   = dtanl_fsub.mk_a2theta_e(plev, a2t.T, a2q.T).T
          a2gradt   = dtanl_fsub.mk_a2grad_abs_saone(a2t.T).T
          a2gradtv  = dtanl_fsub.mk_a2grad_abs_saone(a2tv.T).T
          a2gradtheta=dtanl_fsub.mk_a2grad_abs_saone(a2theta.T).T 
  
          #-- high side value -------------
          a2highside     = ctrack_fsub.find_highsidevalue_saone(a2gradtheta.T, a2chart.T, a2gradtv.T, dist, miss).T

          for region in lregion:
            #-- transform -------------------
            xdom_saone_first, xdom_saone_last, ydom_saone_first, ydom_saone_last  = ret_xydom(region)
            #---
            a2one_trans      = a2one[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]
  
            a2chart_trans    = a2chart[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]
  
            a2highside_trans = a2highside[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]
  
            #---------------------------------
  
            for ftype in lftype:
              if ma.count( ma.masked_not_equal(a2chart_trans ,ftype) ) ==0.0:
                continue
              else:
                dshighside[region, season, ftype] = dshighside[region, season, ftype]  + ma.masked_where(a2chart_trans != ftype, a2highside_trans).sum()
                dshighside2[region, season, ftype]= dshighside2[region, season, ftype] + (ma.masked_where(a2chart_trans != ftype, a2highside_trans)**2.0).sum()
  
                dcount[region, season, ftype]     = dcount[region, season, ftype]      + ma.masked_where(a2chart_trans != ftype, a2one_trans).sum()
 

#***********************************
#  colder side 
#---------------------------
for region in lregion:
  for season in lseason:
    for ftype in lftype:
      if dcount[region, season, ftype] !=0.0:
        dmhighside[region, season, ftype] = dshighside[region,season, ftype] /dcount[region, season, ftype]
        print season, ftype
        n    = dcount[region, season, ftype]
        sv2  = dshighside2[region, season, ftype]
        sv   = dshighside[region, season, ftype]
        mv   = sv  / n
        std  = ((sv2 - 2.0*mv*sv + n*mv*mv)/n)**0.5
        dstdhighside[region, season, ftype] = std
  #--- write to file -----------
  #sodir   = "/home/utsumi/temp"
  sodir  = "/media/disk2/out/JRA25/sa.one.%s/6hr/front/valid/%04d-%04d"%(sresol, iyear, eyear)
  soname  = sodir + "/chart.%s.gradTv.%04d-%04d.%s.lowside%03d.csv"%(sresol,iyear,eyear,region,dist*0.001)
  sout    = ""
  #-- label ---
  sout    = sout + "season,"
  for ftype in lftype:
    sout  = sout + "gradtv.%02d,"%(ftype)
  for ftype in lftype:
    sout  = sout + "std.%02d,"%(ftype)
  
  sout    = sout[:-1] + "\n"
  #------------
  for season in lseason:
    sout  = sout  + "%s,"%(season)
    for ftype in lftype:
      sout = sout + "%s,"%(dmhighside[region, season, ftype])
    for ftype in lftype:
      sout = sout + "%s,"%(dstdhighside[region, season, ftype])
    #---
    sout   = sout[:-1] + "\n"
  #--------------
  if singleday != True:
    f = open(soname, "w")
    f.write(sout)
    f.close()
    print soname
#
#

