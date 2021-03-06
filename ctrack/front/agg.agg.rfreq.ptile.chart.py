from numpy import *
import calendar
import ctrack_para
import ctrack_func
import ctrack_fig
import chart_para
#-------------------------------------
iyear      = 2000
eyear      = 2010
lseason    = ["ALL","DJF","MAM","JJA","SON"]
lftype     = ["all"]
thdist     = 500
percent    = 90  # (%)
region     = "ASAS"
miss       = -9999.0
thorog     = 1500 # (m)

#lllat  = 0.0
#lllon  = 60.0
#urlat  = 80.0
#urlon  = 210.0
lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region)


ny   = 180
nx   = 360
#----------------------------
a2one    = ones([ny,nx], float32)
#-- orog --------------------
orogname = "/media/disk2/data/JRA25/sa.one/const/topo/topo.sa.one"
a2orog   = fromfile(orogname, float32).reshape(ny,nx)
#-- domain ------------------
domname  = "/media/disk2/out/chart/%s/const/domainmask_saone.%s.2000-2006.bn"%(region,region)
a2domain = fromfile(domname , float32).reshape(ny,nx)
#-- shade  ------------------
a2shade  = ma.masked_where( a2domain==0.0, a2one).filled(miss)
a2shade  = ma.masked_where( a2orog > thorog, a2shade).filled(miss)

#-------------------------------------
idir_root  = "/media/disk2/out/chart/ASAS/front/agg"
for ftype in lftype:
  for season in lseason:
    lmon     = ctrack_para.ret_lmon(season)
    #--- out name ---  
    odir_root   = "/media/disk2/out/chart/ASAS/front/agg"
    odir        = odir_root + "/%04d-%04d/%s"%(iyear, eyear, season)
    ctrack_func.mk_dir(odir)

    oname_rfreq = odir + "/rfreq.rad%04d.p%05.2f.%s.saone"%(thdist, percent, season)
    #--- fig name ---
    figdir        = odir + "/pict"
    ctrack_func.mk_dir(figdir)
    figname_rfreq = figdir + "/rfreq.rad%04d.p%05.2f.%s.png"%(thdist, percent, season)
    #--- init  ------
    a2numfront  = zeros([ny,nx],float32)
    a2numplain  = zeros([ny,nx],float32)
    #----------------
    for year in range(iyear, eyear+1):
      for mon in lmon:
        #-- in name ---- 
        idir            = idir_root + "/%04d/%02d/rfreq"%(year, mon)
        iname_numfront  = idir + "/num.rad%04d.p%05.2f.%s.saone"%(thdist, percent, ftype)
        iname_numplain  = idir + "/num.p%05.2f.saone"%(percent)
        #--------------- 
        a2numfront_temp = fromfile(iname_numfront, float32).reshape(ny,nx) 
        a2numplain_temp = fromfile(iname_numplain, float32).reshape(ny,nx)
        #---------------
        a2numfront      = a2numfront + a2numfront_temp
        a2numplain      = a2numplain + a2numplain_temp
        #---------------
    #----------------- 
    a2rfreq    = (ma.masked_where( a2numplain ==0.0, a2numfront) / a2numplain).filled(0.0)
    a2rfreq    = ma.masked_where( a2shade == miss, a2rfreq).filled(miss)
    a2rfreq.tofile(oname_rfreq)

    #--- figure ------
    bnd      = [10,20,30,40,50,60,70,80]
    cbarname = figdir + "/rfreq.cbar.png"
    stitle   = "count proportion, type:%s p%d%%, season:%s %04d-%04d"%(ftype, percent, season,iyear, eyear)
    mycm     = "Spectral"
    datname  = oname_rfreq
    figname  = figname_rfreq
    a2figdat = fromfile(datname, float32).reshape(ny,nx)
    a2figdat = ma.masked_equal(a2figdat, miss).filled(0.0) * 100.0
    ctrack_fig.mk_pict_saone_reg(a2figdat, bnd=bnd, mycm=mycm, soname=figname, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, cbarname=cbarname, stitle=stitle, miss=miss, a2shade=a2shade)
    print figname


