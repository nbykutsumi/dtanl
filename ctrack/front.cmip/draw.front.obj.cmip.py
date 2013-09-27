from numpy import *
import front_func
import front_para, cmip_para, ctrack_para, chart_para
import ctrack_fig

model = "MIROC5"
expr  = "rcp85"
ens   = cmip_para.ret_ens(model, expr, "psl")
year = 2085
mon  = 10
day  = 1
hour = 0
ny,nx = 180,360
miss  = -9999.0
#--- draw region ---------
region_draw = "ASAS"
lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region_draw)

#--- orog mask -----------
thorog     = ctrack_para.ret_thorog()
thgradorog = ctrack_para.ret_thgradorog()
thgrids    = front_para.ret_thgrids()
thfmask1t, thfmask2t, thfmask1q, thfmask2q   = front_para.ret_thfmasktq(model)
orogname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/topo.sa.one"
gradname   = "/media/disk2/data/JRA25/sa.one.125/const/topo/maxgrad.0200km.sa.one"
a2orog     = fromfile(orogname, float32).reshape(ny,nx)
a2gradorog = fromfile(gradname, float32).reshape(ny,nx)

orogname     = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog/orog.%s.sa.one"%(model,expr,model)
gradorogname = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog/maxgrad.0200km.sa.one"%(model,expr)

a2orog     = fromfile(orogname, float32).reshape(ny,nx)
a2gradorog = fromfile(gradorogname, float32).reshape(ny,nx)

a2shade    = ones([ny,nx],float32)
a2shade    = ma.masked_where(a2orog > thorog, a2shade)
a2shade    = ma.masked_where(a2gradorog > thgradorog, a2shade)

#--- data processing ------
frontdir_t_root = "/media/disk2/out/CMIP5/sa.one.%s.%s/6hr/front.t"%(model,expr)
frontdir_t      = frontdir_t_root   + "/%04d%02d"%(year, mon)
fronttname1 = frontdir_t + "/front.t.M1.%04d.%02d.%02d.%02d.sa.one"%(year, mon, day, hour)
fronttname2 = frontdir_t + "/front.t.M2.%04d.%02d.%02d.%02d.sa.one"%(year, mon, day, hour)

a2fbc1      = fromfile(fronttname1, float32).reshape(ny,nx)
a2fbc2      = fromfile(fronttname2, float32).reshape(ny,nx)
a2fbc       = front_func.complete_front_t_saone(a2fbc1, a2fbc2, thfmask1t, thfmask2t, a2orog, a2gradorog, thorog, thgradorog, thgrids, miss )

#--- draw -----
figname  = "./temp.front.png"
stitle   = "%s %s %04d-%02d-%02d UTC%02d"%(model, expr, year,mon,day,hour)
ctrack_fig.mk_pict_saone_reg(a2in=a2fbc, soname=figname, stitle=stitle, lllat=lllat, lllon=lllon, urlat=urlat, urlon=urlon, a2shade=a2shade)


