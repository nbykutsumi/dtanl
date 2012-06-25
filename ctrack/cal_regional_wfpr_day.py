import ctrack_para
import ctrack_func as func
from numpy import *
import matplotlib
import matplotlib.pyplot as plt
#**************************************
tstp  = "day"
model = "NorESM1-M"
expr  = "historical"
#expr  = "rcp85"
ens   = "r1i1p1"
nx    = 144
ny    = 96
#crad  = 1000
#lcrad  = [1000, 1500]
lcrad  = [1000]
season = "DJF"
thorog   = 1500.0
thdura   = 24
miss_dbl = -9999.0
#--------------------------------------
wline    = 3.0
col0     = "k"
titlesize= 25
#**************************************
lonlatinfo = ctrack_para.ret_lonlatinfo(model)
[lon_first, lat_first, dlon, dlat] = lonlatinfo
#
dpgradrange = ctrack_para.ret_dpgradrange()
lclass      = dpgradrange.keys()
nclass      = len(lclass) -1
#
dlwbin      = ctrack_para.ret_dlwbin()
liw         = dlwbin.keys()
nwbin       = len(liw)
#
#lxth        = ctrack_para.ret_lxth
#lxth        = [0.0, 50.0, 60.0,  70.0, 80.0, 90.0, 99.0]
#lxth = [0.0, 99.0]
lxth = [0.0]
#**************************************
dir_root = "/media/disk2/out/CMIP5/%s/%s/%s/%s/tracks/dura%02d/wfpr"%(tstp, model, expr, ens, thdura)
pictdir = dir_root + "/pict/c%02dclasses"%(nclass)
numdir = dir_root + "/num"
spdir  = dir_root + "/sp"
sp2dir = dir_root + "/sp2"
swdir  = dir_root + "/sw"
sw2dir = dir_root + "/sw2"
#
func.mk_dir(pictdir)
#**************************************
#--------------------
# make lwvalue
#--------------------
lwbin = []
for iw in liw:
  lwbin.append(mean(dlwbin[iw]))
#
lwbin[0]  = -9999.0
lwbin[1]  = lwbin[2]  - (lwbin[3] - lwbin[2])
lwbin[-1] = lwbin[-2] + (lwbin[3] - lwbin[2])

#*****************************************************
#  read orography
#----------------------
orogdir_root = "/media/disk2/data/CMIP5/bn/orog/fx/%s/%s/r0i0p0"%(model, expr)
orogname     = orogdir_root + "/orog_fx_%s_%s_r0i0p0.bn"%(model, expr)
a2orog         = fromfile(orogname, float32).reshape(ny,nx)
#******************************************************
# START crad and xth LOOP
#------------------------------------------------------
for crad in lcrad:
  for xth in lxth:
    print "xth=", xth
    #-------------------------------------
    #-------------------------------------
    # names
    #--------------------------------------
    # name for num
    #-------------------
    dnumname = {}
    #for iclass in lclass:
    for iclass in [-1] + lclass:
      dnumname[iclass] = numdir + "/num.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, iclass, nclass, crad, nwbin, season, tstp, model, expr, ens)
    #-------------------
    # name for sp
    #-------------------
    dspname = {}
    #for iclass in lclass:
    for iclass in [-1] + lclass:
      dspname[iclass] = spdir + "/sp.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, iclass, nclass, crad, nwbin, season, tstp, model, expr, ens)
    #-------------------
    # name for sp2
    #-------------------
    dsp2name = {}
    #for iclass in lclass:
    for iclass in [-1] + lclass:
      dsp2name[iclass] = sp2dir + "/sp2.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, iclass, nclass, crad, nwbin, season, tstp, model, expr, ens)
    #-------------------
    # name for sw
    #-------------------
    dswname = {}
    #for iclass in lclass:
    for iclass in [-1] + lclass:
      dswname[iclass] = swdir + "/sw.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, iclass, nclass, crad, nwbin, season, tstp, model, expr, ens)
    #-------------------
    # name for sw2
    #-------------------
    dsw2name = {}
    #for iclass in lclass:
    for iclass in [-1] + lclass:
      dsw2name[iclass] = sw2dir + "/sw2.p%05.2f.c%02d.%02d.r%04d.nw%02d_%s_%s_%s_%s_%s.bn"%(xth, iclass, nclass, crad, nwbin, season, tstp, model, expr, ens)
    
    #**************************************
    # read data
    #--------------------------------------
    # read num
    #-----------------
    da3num   = {}
    #for iclass in lclass:
    for iclass in [-1] + lclass:
      da3num[iclass] = fromfile(dnumname[iclass], float32).reshape(nwbin, ny, nx)
    #-----------------
    # read sp
    #-----------------
    da3sp   = {}
    #for iclass in lclass:
    for iclass in [-1] + lclass:
      da3sp[iclass] = fromfile(dspname[iclass], float32).reshape(nwbin, ny, nx)
    #-----------------
    # read sp2
    #-----------------
    da3sp2   = {}
    #for iclass in lclass:
    for iclass in [-1] + lclass:
      da3sp2[iclass] = fromfile(dsp2name[iclass], float32).reshape(nwbin, ny, nx)
    #-----------------
    # read sw
    #-----------------
    da3sw   = {}
    #for iclass in lclass:
    for iclass in [-1] + lclass:
      da3sw[iclass] = fromfile(dswname[iclass], float32).reshape(nwbin, ny, nx)
    #-----------------
    # read sw2
    #-----------------
    da3sw2   = {}
    #for iclass in lclass:
    for iclass in [-1] + lclass:
      da3sw2[iclass] = fromfile(dsw2name[iclass], float32).reshape(nwbin, ny, nx)
    
    
    #*****************************************************
    # make region mask
    #*****************************************************
    # region bound
    #-------------
    dbound = ctrack_para.ret_dbound()
    lreg   = dbound.keys()
    #lreg   = [lreg[0]] 
    #---------------------------------------
    for reg in lreg:
      [lat_min, lat_max, lon_min, lon_max] = dbound[reg]
      
      a2regionmask = func.mk_region_mask(lat_min, lat_max, lon_min, lon_max, nx, ny, lat_first, lon_first, dlat, dlon)
      a2regionmask = ma.masked_where(a2orog > thorog, a2regionmask).filled(0.0)
      #
      a3regionmask = zeros(nwbin* ny* nx).reshape(nwbin, ny, nx)
      for iw in liw:
        a3regionmask[iw] = a2regionmask
      
      
      
      #**************************************
      # mask
      #--------------------------------------
      # for num
      #---------
      da3num_reg = {}
      #for iclass in lclass:
      for iclass in [-1] + lclass:
        da3num_reg[iclass] = ma.masked_where(a3regionmask ==0.0, da3num[iclass])
      #---------
      # for sp
      #---------
      da3sp_reg = {}
      #for iclass in lclass:
      for iclass in [-1] + lclass:
        da3sp_reg[iclass] = ma.masked_where(a3regionmask ==0.0, da3sp[iclass])
      #---------
      # for sp2
      #---------
      da3sp2_reg = {}
      #for iclass in lclass:
      for iclass in [-1] + lclass:
        da3sp2_reg[iclass] = ma.masked_where(a3regionmask ==0.0, da3sp2[iclass])
      #---------
      # for sw
      #---------
      da3sw_reg = {}
      #for iclass in lclass:
      for iclass in [-1] + lclass:
        da3sw_reg[iclass] = ma.masked_where(a3regionmask ==0.0, da3sw[iclass])
      #---------
      # for sw2
      #---------
      da3sw2_reg = {}
      #for iclass in lclass:
      for iclass in [-1] + lclass:
        da3sw2_reg[iclass] = ma.masked_where(a3regionmask ==0.0, da3sw2[iclass])
      
      #**************************************
      # regional num
      #--------------------------------------
      dlnum = {}
      anum_reg = zeros((nclass+1)*nwbin).reshape(nclass+1, nwbin)
      #for iclass in lclass:
      for iclass in [-1] + lclass:
        dlnum[iclass] = []
        for iw in liw:
          num = da3num_reg[iclass][iw].sum() 
          dlnum[iclass].append(num)
          anum_reg[iclass, iw] = num
      #--------------------------------------    
      # regional sp
      #--------------------------------------
      dlsp  = {}
      asp_reg = zeros((nclass+1)*nwbin).reshape(nclass+1, nwbin)
      #for iclass in lclass:
      for iclass in [-1] + lclass:
        dlsp[iclass] = []
        for iw in liw:
          sp  = da3sp_reg[iclass][iw].sum()
          dlsp[iclass].append(sp)
          asp_reg[iclass, iw] = sp
      #--------------------------------------    
      # regional sp2
      #--------------------------------------
      dlsp2  = {}
      #for iclass in lclass:
      for iclass in [-1] + lclass:
        dlsp2[iclass] = []
        for iw in liw:
          sp2  = da3sp2_reg[iclass][iw].sum()
          dlsp2[iclass].append(sp2)
      #--------------------------------------    
      # regional sw
      #--------------------------------------
      dlsw  = {}
      #for iclass in lclass:
      for iclass in [-1] + lclass:
        dlsw[iclass] = []
        for iw in liw:
          sw  = da3sw_reg[iclass][iw].sum()
          dlsw[iclass].append(sw)
      #--------------------------------------    
      # regional sw2
      #--------------------------------------
      dlsw2  = {}
      #for iclass in lclass:
      for iclass in [-1] + lclass:
        dlsw2[iclass] = []
        for iw in liw:
          sw2  = da3sw2_reg[iclass][iw].sum()
          dlsw2[iclass].append(sw2)
      
      #**************************************
      # calc average intensity
      #--------------------------------------
      # precip intensity
      #----------------
      dlp    = {}
      for iclass in lclass:
        dlp[iclass] = range(nwbin)
        for iw in liw:
          if dlnum[iclass][iw] == 0.0:
            dlp[iclass][iw] = miss_dbl
          else:
            dlp[iclass][iw] = dlsp[iclass][iw] / dlnum[iclass][iw]
      #
      ap = zeros((nclass+1)*nwbin).reshape((nclass+1), nwbin)
      for iclass in lclass:
        for iw in liw:
          ap[iclass, iw] = dlp[iclass][iw]
      #----------------
      # w intensity
      #----------------
      dlw   = {}
      for iclass in lclass:
        dlw[iclass]  = range(nwbin)
        for iw in liw:
          if dlnum[iclass][iw]  == 0.0:
            dlw[iclass][iw]  = miss_dbl
          else:
            dlw[iclass][iw]  = dlsw[iclass][iw] / dlnum[iclass][iw]
      
      #
      aw = zeros((nclass+1)*nwbin).reshape((nclass+1), nwbin)
      for iclass in lclass:
        for iw in liw:
          aw[iclass, iw] = dlw[iclass][iw]
      #--------------------------------------
      # calc relative frequency
      #--------------------------------------
      dlrnum   = {}
      for iclass in lclass:
        dlrnum[iclass] = range(nwbin)
        snum  = sum(dlnum[iclass])
        for iw in liw:
          if snum == 0.0:
            dlrnum[iclass][iw] = miss_dbl
          else:
            dlrnum[iclass][iw] = dlnum[iclass][iw] / snum
      #**************************************
      # calc sigma
      #--------------------------------------
      # sigma precip
      #----------------
      dlsig_p = {}
      for iclass in lclass:
        dlsig_p[iclass] = range(nwbin)
        for iw in liw:
          n = dlnum[iclass][iw]
          if n == 0.0:
            sig = miss_dbl
          else:
            sx2 = dlsp2[iclass][iw] 
            mx  = dlp[iclass][iw]
            sig = sqrt( (sx2 - n*mx*mx)/n )
          #
          dlsig_p[iclass][iw] = sig
      #
      asig_p = zeros((nclass+1)*nwbin).reshape(nclass+1, nwbin)
      for iclass in lclass:
        for iw in liw:
          asig_p[iclass, iw] = dlsig_p[iclass][iw]
      
      
      #----------------
      # sigma omega
      #----------------
      dlsig_w = {}
      for iclass in lclass:
        dlsig_w[iclass] = range(nwbin)
        for iw in liw:
          n = dlnum[iclass][iw]
          if n == 0.0:
            sig = miss_dbl
          else:
            sx2 = dlsw2[iclass][iw]
            mx  = dlw[iclass][iw]
            sig = sqrt( (sx2 - n*mx*mx)/n )
          #
          dlsig_w[iclass][iw] = sig
      #
      asig_w = zeros((nclass+1)*nwbin).reshape(nclass+1, nwbin)
      for iclass in lclass:
        for iw in liw:
          asig_w[iclass, iw] = dlsig_w[iclass][iw]
      #**************************************
      # make pict
      #**************************************
      sspec0 = "%s, r=%s, dura=%s, xth=%02d, %s"%(reg, crad, thdura, xth, expr)
      #**************************************
      if xth in [0.0]:
        #-----------------
        # c-p
        #-----------------
        plt.clf()
        c_p_name = pictdir  + "/p%05.2f.r%04d.c.p.cn%02d.%s.png"%(xth, crad, nclass, reg)
        print c_p_name
        lx  = lclass[1:]
        ly  = array(ap[1:,0]) * 60.0 * 60.0* 24.0
        #
        plt.plot(lx, ly, lw=wline)
        #
        ye  = asig_p[1:,0] * 60.0 * 60.0 * 24.0
        plt.errorbar(lx, ly, yerr = ye)
        plt.xlim(0, nclass+1)
        plt.ylim(0, 18)
        #
        plt.savefig(c_p_name)
        #-----------------
        # c-rp
        #-----------------
        plt.clf()
        c_rp_name = pictdir  + "/p%05.2f.r%04d.c.rp.cn%02d.%s.png"%(xth, crad, nclass, reg)
        #--
        sp  = sum(dlsp[-1])
        lx  = array(lclass[1:])
        ly  = sum(asp_reg[1:], axis=1) / sp
        plt.bar(lx-0.5, ly)
        #---
        lcrp = []  # cumulative relative precipitation
        cp = 0.0
        for iclass in lclass[1:]:
          cp = cp + sum(asp_reg[iclass])
          lcrp.append(cp)
        lcrp = lcrp / sp
        plt.plot(lx, lcrp, c=col0, lw = wline)
        #---
        plt.xlim(0, nclass+1)
        #
        plt.suptitle("RP.vs.C")
        plt.title(sspec0)
        plt.savefig(c_rp_name)
        #-----------------
        # c-w     # w: [hPa/day] 
        #-----------------
        plt.clf()
        c_w_name = pictdir  + "/p%05.2f.r%04d.c.w.cn%02d.%s.png"%(xth, crad, nclass, reg)
        lx  = lclass[1:]
        ly  = -1.0*aw[1:,0] * 0.1*60.0*60.0*24.0
        #
        plt.plot(lx, ly, c=col0, lw = wline)
        #
        ye  = asig_w[1:, 0] * 0.1*60.0*60.0*24.0
        plt.errorbar(lx, ly, yerr = ye, c="%s"%(col0))
        plt.xlim(0, nclass+1)
        #
        plt.suptitle("C.vs.W")
        plt.title(sspec0)
        plt.savefig(c_w_name)
        #-----------------
        # c-n
        #-----------------
        plt.clf()
        c_n_name = pictdir  + "/p%05.2f.r%04d.c.n.cn%02d.%s.png"%(xth, crad, nclass, reg)
        lx  = lclass[1:]
        ly  = sum(anum_reg, axis=1)[1:]
        #-
        plt.plot(lx, ly, c="%s"%(col0), lw=wline)
        #
        plt.xlim(0, nclass+1)
        #
        plt.suptitle("C.vs.N")
        plt.title(sspec0)
        plt.savefig(c_n_name)
        print c_n_name
        #-----------------
        # c-rn
        #-----------------
        plt.clf()
        c_rn_name = pictdir  + "/p%05.2f.r%04d.c.rn.cn%02d.%s.png"%(xth, crad, nclass, reg)
        lx  = lclass[1:]
        ly  = (sum(anum_reg, axis=1)/anum_reg.sum())[1:]
        #-
        plt.plot(lx, ly, c="%s"%(col0), lw = wline)
        #
        plt.xlim(0, nclass+1)
        plt.ylim(0.0, 0.25)
        #
        plt.suptitle("PDF(Ci)")
        plt.title(sspec0)
        plt.savefig(c_rn_name)
         
        print c_rn_name
        #-----------------
        # w-p 
        #-----------------
        for iclass in [0]:
          plt.clf()
          w_p_name = pictdir  + "/p%05.2f.r%04d.w.p.c%02d.%02d.%s.png"%(xth, crad, iclass,nclass, reg)
          #
          ly  = array(ap[iclass][1:]) * 60.0 * 60.0 * 24.0
          #lx  = -ma.masked_equal(aw[iclass][1:], miss_dbl).filled(-miss_dbl)
          lx  = ma.masked_where(ly ==miss_dbl, lwbin[1:]).filled(miss_dbl)
          lye = asig_p[iclass][1:] * 60.0 * 60.0 * 24.0
          #
          #
          lx  = func.del_miss(lx,  miss_dbl)
          ly  = func.del_miss(ly,  miss_dbl)
          lye = func.del_miss(lye, miss_dbl)
          #
          plt.plot(lx, ly, c=col0, lw = wline)
          ##
          plt.errorbar(lx, ly, yerr = lye)
          ##
          plt.ylim(0, 120.0)
          #
          plt.suptitle("W.vs.P")
          plt.title(sspec0)
          plt.savefig(w_p_name)
        #-----------------------------
        # put all into one figure
        #-----------
        plt.clf()
        dplt = {}
        w_p_name = pictdir  + "/p%05.2f.r%04d.w.p.cmulti.%02d.%s.png"%(xth, crad, nclass, reg)
        for iclass in lclass[1:]:
          #
          ly  = array(ap[iclass][1:]) 
          #lx  = -ma.masked_equal(aw[iclass][1:], miss_dbl).filled(miss_dbl)
          lx  = ma.masked_where(ly ==miss_dbl, lwbin[1:]).filled(miss_dbl)
          lye = asig_p[iclass][1:] 
          #
          #
          lx  = array(func.del_miss(lx,  miss_dbl))
          ly  = array(func.del_miss(ly,  miss_dbl)) *60*60*24.0
          lye = array(func.del_miss(lye, miss_dbl)) *60*60*24.0
          #
          plt.plot(lx, ly, lw = wline)
          ##
          dplt[iclass] = plt.errorbar(lx, ly, yerr = lye, lw=wline, label="%02d"%(iclass))
          ##
        #--
        llegend = map(str, lclass[1:])
        plt.legend(loc="upper left")
        #plt.legend( dplt.values(), llegend, "upper left")
        #
        plt.ylim(0.0, 120.0)
        plt.suptitle("P(w|Ci)")
        plt.title(sspec0)
        plt.savefig(w_p_name)
        #*******************************
        #-----------------
        # w-n
        #-----------------
        for iclass in [0]:
          plt.clf()
          w_n_name = pictdir  + "/p%05.2f.r%04d.w.n.c%02d.%02d.%s.png"%(xth, crad, iclass, nclass, reg)
          #
          ly  = array(dlnum[iclass][1:])
          #lx  = -ma.masked_equal(aw[iclass][1:], miss_dbl).filled(miss_dbl)
          lx  = ma.masked_where(ly ==0.0, lwbin[1:]).filled(miss_dbl)
          #
          lx  = func.del_miss(lx,  miss_dbl)
          ly  = func.del_miss(ly,  0.0)
          #
          plt.plot(lx, ly, lw = wline)
          ##
          plt.suptitle("W.vs.N")
          plt.title(sspec0)
          plt.savefig(w_n_name)
        #-----------------------------
        # w-n : put all into one figure
        #-----------
        plt.clf()
        dplt = {}
        w_n_name = pictdir  + "/p%05.2f.r%04d.w.n.cmulti.%02d.%s.png"%(xth, crad, nclass, reg)
        for iclass in lclass[1:]:
          #
          ly  = array(dlnum[iclass][1:])
          #lx  = -ma.masked_equal(aw[iclass][1:], miss_dbl).filled(miss_dbl)
          lx  = ma.masked_where(ly ==0.0, lwbin[1:]).filled(miss_dbl)
          #
          lx  = func.del_miss(lx,  miss_dbl)
          ly  = func.del_miss(ly,  0.0)
          #
          dplt[iclass] = plt.plot(lx, ly, lw = wline)
          ##
        #--
        llegend = map(str, lclass[1:])
        plt.legend( dplt.values(), llegend, "upper right")
        #
        plt.suptitle("W.vs.N")
        plt.title(sspec0)
        plt.savefig(w_n_name)
        #*******************************
        #-----------------
        # w-rn,  relative frequency
        #-----------------
        for iclass in [0]:
          plt.clf()
          w_rn_name = pictdir  + "/p%05.2f.r%04d.w.rn.c%02d.%02d.%s.png"%(xth, crad, iclass, nclass, reg)
          #
          ly  = array(dlrnum[iclass][1:])
          #lx  = -ma.masked_equal(aw[iclass][1:], miss_dbl).filled(miss_dbl)
          lx  = ma.masked_where(ly ==0.0, lwbin[1:]).filled(miss_dbl)
          #
          lx  = func.del_miss(lx,  miss_dbl)
          ly  = func.del_miss(ly,  0.0)
          #
          plt.plot(lx, ly, c=col0, lw = wline)
          ##
          plt.suptitle("PDF(W|Ci)")
          plt.title(sspec0)
          plt.savefig(w_rn_name)
        #-----------------------------
        # w-rn : put all into one figure
        #-----------
        plt.clf()
        dplt = {}
        w_rn_name = pictdir  + "/p%05.2f.r%04d.w.rn.cmulti.%02d.%s.png"%(xth, crad, nclass, reg)
        for iclass in lclass[1:]:
          #
          ly  = array(dlrnum[iclass][1:])
          #lx  = -ma.masked_equal(aw[iclass][1:], miss_dbl).filled(miss_dbl)
          lx  = ma.masked_where(ly ==0.0, lwbin[1:]).filled(miss_dbl)
          #
          lx  = func.del_miss(lx,  miss_dbl)
          ly  = func.del_miss(ly,  0.0)
          #
          dplt[iclass] = plt.plot(lx, ly, lw = wline)
          ##
        #--
        llegend = map(str, lclass[1:])
        plt.legend( dplt.values(), llegend, "upper right")
        #
        plt.suptitle("PDF(W|Ci)")
        plt.title(sspec0)
        plt.savefig(w_rn_name)
#      ###------------------------------------------------------
#      ###-----------------
#      ### c-rp
#      ###-----------------
#      ##plt.clf()
#      ##c_rp_name = pictdir  + "/p%05.2f.r%04d.c.rp.cn%02d.%s.png"%(xth, crad, nclass, reg)
#      ###--
#      ##sp  = sum(dlsp[-1])
#      ##lx  = array(lclass[1:])
#      ##ly  = sum(asp_reg[1:], axis=1) / sp
#      ##plt.bar(lx-0.5, ly)
#      ###---
#      ##lcrp = []  # cumulative relative precipitation
#      ##cp = 0.0
#      ##for iclass in lclass[1:]:
#      ##  cp = cp + sum(asp_reg[iclass])
#      ##  lcrp.append(cp)
#      ##lcrp = lcrp / sp
#      ##plt.plot(lx, lcrp, c=col0, lw = wline)
#      ###---
#      ##plt.xlim(0, nclass+1)
#      ##plt.suptitle("RP(Ci)")
#      ##plt.title(sspec0)
#      ##plt.savefig(c_rp_name)
