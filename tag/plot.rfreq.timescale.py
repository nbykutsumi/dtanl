from numpy import *
import ctrack_func
import gsmap_func
import matplotlib.pyplot as plt
import chart_para
#-----------------------------------------------
iyear      = 2001
eyear      = 2009

sresol  = "anl_p"

lbstflag_tc = ["bst"]
#lbstflag_tc = ["","bst"]
#lbstflag_f  = ["","bst.high","bst.type"]
lbstflag_f  = [""]
lprtype      = ["GSMaP"]
#**
lregion    = ["W.JPN","E.JPN"]
#lseason    = ["NDJFMA","JJASON","ALL"]
lseason    = ["ALL"]
#lseason    = [1]

lfbctype    = ["nn","wn"]

#lnhour = [1,3,6,12,24]
lnhour = [1,3,6,12,24]
#ltag       = ["tc","c","fbc","ot","nbcot"]
ltag_org    = ["tc","c","fbc","ot","nbc"]
ptile       = 99.9
#*
#**
dist_tc = 1000 #[km]
dist_c  = 1000 #[km]
dist_f  = 500 #[km]
#**
thdura_c  = 48
thdura_tc = thdura_c


#**
dlat,dlon  = (1.0, 1.0)
lat_first  = -89.5
lon_first  = 0.5

iyear_dat  = 2001
eyear_dat  = 2009
miss       = -9999.0
#---------------------------
def ret_lkeys(fbctypeflag, tagflag, nhourflag):
  if (fbctypeflag, tagflag, nhourflag) == (True,True,True):
    lkeys = [ [fbctype,tag,nhour] for fbctype in lfbctype\
                                for tag   in ltag\
                                for nhour in lnhour]
    if (("nn" in lfbctype)&("nbc" in ltag)):
      for nhour in lnhour:
        lkeys.remove(["nn","nbc",nhour])
  #----
  if (fbctypeflag, tagflag, nhourflag) == (True,True,False):
    lkeys = [ [fbctype,tag] for fbctype in lfbctype\
                                for tag   in ltag]
    if (("nn" in lfbctype)&("nbc" in ltag)):
      lkeys.remove(["nn","nbc"])
  #----
  return lkeys
#----------------------------
def ret_ltag(fbctype, ltag_org):
  if fbctype=="wn":
    ltag = ltag_org
  elif fbctype=="nn":
    ltag = []
    for a in ltag_org:
      if a=="nbc":
        continue
      else:
        ltag.append(a)
  else:
    print "check ltag_org"
    sys.exit()
  #--
  return ltag
#----------------------------
for prtype,bstflag_tc, bstflag_f,season,region,fbctype in \
   [[prtype,bstflag_tc,bstflag_f,season,region,fbctype] for prtype in lprtype\
                                         for bstflag_tc in lbstflag_tc\
                                         for bstflag_f in lbstflag_f\
                                         for season in lseason\
                                         for region in lregion\
                                         for fbctype in lfbctype]:

  #*****************************
  ltag  = ret_ltag(fbctype, ltag_org)
  if prtype == "GSMaP":
    nx_dat, ny_dat     = (360,120)
    nx,ny              = (360,180)
  elif prtype == "GSMaP.ded":
    nx_dat, ny_dat     = (3600,1200)
    nx,ny              = (3600,1800)
  #*** region mask *************
  print "region=",region
  lllon, lllat, urlon, urlat = chart_para.ret_domain_corner_rect_forfig(region)
  a2regionmask  = ctrack_func.mk_region_mask(lllat, urlat, lllon, urlon, nx, ny, lat_first, lon_first, dlat, dlon)
  #-----------------------------
  
  idir_root = "/media/disk2/out/JRA25/sa.one.%s/6hr/tagexpr/%s.c%02dh.tc%02dh"%(sresol, fbctype, thdura_c, thdura_tc)
  
  #**** load *************
  da2in      = {}
  for tag in ltag:
    for nhour in lnhour:
      idir      = idir_root + "/%s.%04d-%04d.%s"%(prtype, iyear_dat, eyear_dat, season)
      iname     = idir + "/rfreq.%s.%s.mov%02dhr.%05.2f.%stc%04d.c%04d.%sf%04d.GSMaP.%s.sa.one"%(fbctype, prtype, nhour, ptile, bstflag_tc, dist_tc, dist_c, bstflag_f, dist_f,tag)
      da2in[tag,nhour]  = fromfile(iname, float32).reshape(ny_dat,nx_dat)
      #-- reshape --
      if prtype in ["GSMaP","GSMaP.dec"]:
        da2in[tag,nhour] = gsmap_func.gsmap2global(da2in[tag,nhour], miss)
      #-------------
  #**** make sum-mask ****
  da2sum       = {}
  for nhour in lnhour:
    da2sum[nhour]    = zeros([ny,nx],float32)
    for tag in ltag:
      da2sum[nhour]  = da2sum[nhour]  +  ma.masked_equal(da2in[tag,nhour], miss).filled(0.0)
  
  #***********************
  dv         = {}
  dstd       = {}
  for tag in ltag:
    #*****
    if tag not in dv.keys():
      dv[tag]   = []
      dstd[tag] = []
    #*****
    for nhour in lnhour:
      a2in     = da2in[tag,nhour]
      #**
      a2in     = ma.masked_equal(a2in, miss)
      a2in     = ma.masked_where(da2sum[nhour]==0.0, a2in)
      a2in     = ma.masked_where(a2regionmask==0.0, a2in)
      v        = a2in.mean()
      std      = a2in.std()
      dv[tag].append(v) 
      dstd[tag].append(std)
  #* sum all ************************
  dv["sum"] = []
  for i in range(len(lnhour)):
    vall    = 0.0
    a2temp_sum = zeros([ny,nx],float32)
    for tag in ltag:
      vall  = vall + dv[tag][i]
    #
    dv["sum"].append(vall)
  #**** plot ************************
  figplot  = plt.figure()
  axplot   = figplot.add_axes([0.2, 0.2, 0.7, 0.7])
  for tag in ltag:
    lx         = lnhour
    ly         = dv[tag]
    axplot.plot(lx,ly, linewidth=3.0)
    #-- error range ---
    ly_up      = array(dv[tag]) + array(dstd[tag])
    ly_lw      = array(dv[tag]) - array(dstd[tag])
    #axplot.fill_between(lx, ly_lw, ly_up, facecolor="gray", alpha = 0.1)
    axplot.fill_between(lx, ly_lw, ly_up, alpha = 0.1)

  #-- sum --
  #axplot.plot(lnhour, dv["sum"])

  #-- set axis limit --
  axplot.set_ylim( (0.0, 1.0))
  #-- legend ----
  axplot.legend(ltag+["sum"])
  #axplot.legend(ltag)
  #-- save ------
  pictdir    = idir_root + "/%s.%04d-%04d.%s/pict"%(prtype,iyear_dat,eyear_dat,season)
  ctrack_func.mk_dir(pictdir)
  figname    = pictdir + "/plot.rfreq.%s.%s.%05.2f.%stc%04d.c%04d.%sf%04d.%s.%s.png"%(fbctype, prtype, ptile, bstflag_tc, dist_tc, dist_c, bstflag_f,dist_f,season,region)
  figplot.savefig(figname)
  print figname
