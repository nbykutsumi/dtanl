import ctrack_para
import ctrack_func as func
from numpy import *
import matplotlib
import matplotlib.pyplot as plt
#**************************************
iyear_his   = 1990
eyear_his   = 1999
iyear_fut   = 2086
eyear_fut   = 2095


tstp  = "day"
model = "NorESM1-M"
lexpr  = ["historical","rcp85"]
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
miss_dbl = -9999.0e+10
#--------------------------------------
wline    = 3.0
col0     = "k"
titlesize= 25
#**************************************
lera    = ["his", "fut"]

diyear  = {"his": iyear_his, "fut": iyear_fut}
deyear  = {"his": eyear_his, "fut": eyear_fut}
#***************************************
dexpr   = {"his": "historical", "fut": "rcp85", "dif": "dif"}
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
lxth = [90.0, 0.0]
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
#******************************************************
# START crad and xth LOOP
#------------------------------------------------------
for crad in lcrad:
  for xth in lxth:
    #--------------------------
    print "xth=", xth

    daa       = {}
    dbb       = {}
    dxx       = {}
    dyy       = {}
    #--------------------------
    dlnum     = {}
    dlsp      = {}
    dlsp2     = {}
    dlsw      = {}
    dlsw2     = {}
    dlp       = {}
    dlw       = {} 
    dlsig_p   = {}
    dlsig_w   = {}
    dlrnum    = {}
    #--------------------------
    for era in lera:
      expr    = dexpr[era]
      #--------------------------
      dir_root = "/media/disk2/out/CMIP5/%s/%s/%s/%s/tracks/dura%02d/wfpr"%(tstp, model, expr, ens, thdura)
      pictdir = dir_root + "/pict/c%02dclasses"%(nclass)
      numdir = dir_root + "/num"
      spdir  = dir_root + "/sp"
      sp2dir = dir_root + "/sp2"
      swdir  = dir_root + "/sw"
      sw2dir = dir_root + "/sw2"
      #
      func.mk_dir(pictdir)
      #--------------------------
      #  read orography
      #----------------------
      orogdir_root = "/media/disk2/data/CMIP5/bn/orog/fx/%s/%s/r0i0p0"%(model, expr)
      orogname     = orogdir_root + "/orog_fx_%s_%s_r0i0p0.bn"%(model, expr)
      a2orog         = fromfile(orogname, float32).reshape(ny,nx)

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
        anum_reg = zeros((nclass+1)*nwbin).reshape(nclass+1, nwbin)
        #for iclass in lclass:
        for iclass in [-1] + lclass:
          dlnum[reg, expr, iclass] = []
          for iw in liw:
            num = da3num_reg[iclass][iw].sum() 
            dlnum[reg, expr, iclass].append(num)
            anum_reg[iclass, iw] = num

        #--------------------------------------    
        # regional sp
        #--------------------------------------
        #dlsp  = {}
        asp_reg = zeros((nclass+1)*nwbin).reshape(nclass+1, nwbin)
        #for iclass in lclass:
        for iclass in [-1] + lclass:
          dlsp[reg, expr, iclass] = []
          for iw in liw:
            sp  = da3sp_reg[iclass][iw].sum()
            dlsp[reg, expr, iclass].append(sp)
            asp_reg[iclass, iw] = sp
        #--------------------------------------    
        # regional sp2
        #--------------------------------------
        #dlsp2  = {}
        #for iclass in lclass:
        for iclass in [-1] + lclass:
          dlsp2[reg, expr, iclass] = []
          for iw in liw:
            sp2  = da3sp2_reg[iclass][iw].sum()
            dlsp2[reg, expr, iclass].append(sp2)
        #--------------------------------------    
        # regional sw
        #--------------------------------------
        #dlsw  = {}
        #for iclass in lclass:
        for iclass in [-1] + lclass:
          dlsw[reg, expr, iclass] = []
          for iw in liw:
            sw  = da3sw_reg[iclass][iw].sum()
            dlsw[reg, expr, iclass].append(sw)
        #--------------------------------------    
        # regional sw2
        #--------------------------------------
        #dlsw2  = {}
        #for iclass in lclass:
        for iclass in [-1] + lclass:
          dlsw2[reg, expr, iclass] = []
          for iw in liw:
            sw2  = da3sw2_reg[iclass][iw].sum()
            dlsw2[reg, expr, iclass].append(sw2)
        
        #**************************************
        # calc average intensity
        #--------------------------------------
        # precip intensity
        #----------------
        #dlp    = {}
        for iclass in lclass:
          dlp[reg, expr, iclass] = range(nwbin)
          for iw in liw:
            if dlnum[reg, expr, iclass][iw] == 0.0:
              dlp[reg, expr, iclass][iw] = miss_dbl
            else:
              dlp[reg, expr, iclass][iw] = dlsp[reg, expr, iclass][iw] / dlnum[reg, expr, iclass][iw]
        #
        ap = zeros((nclass+1)*nwbin).reshape((nclass+1), nwbin)
        for iclass in lclass:
          for iw in liw:
            ap[iclass, iw] = dlp[reg, expr, iclass][iw]
        #----------------
        # w intensity
        #----------------
        #dlw   = {}
        for iclass in lclass:
          dlw[reg, expr, iclass]  = range(nwbin)
          for iw in liw:
            if dlnum[reg, expr, iclass][iw]  == 0.0:
              dlw[reg, expr, iclass][iw]  = miss_dbl
            else:
              dlw[reg, expr, iclass][iw]  = dlsw[reg, expr, iclass][iw] / dlnum[reg, expr, iclass][iw]
        
        #
        aw = zeros((nclass+1)*nwbin).reshape((nclass+1), nwbin)
        for iclass in lclass:
          for iw in liw:
            aw[iclass, iw] = dlw[reg, expr, iclass][iw]
        #--------------------------------------
        # calc relative frequency
        #--------------------------------------
        for iclass in lclass:
          dlrnum[reg, expr, iclass] = range(nwbin)
          snum  = sum(dlnum[reg, expr, iclass])
          for iw in liw:
            if snum == 0.0:
              dlrnum[reg, expr, iclass][iw] = miss_dbl
            else:
              dlrnum[reg, expr, iclass][iw] = dlnum[reg, expr, iclass][iw] / snum
        #**************************************
        # calc sigma
        #--------------------------------------
        # sigma precip
        #----------------
        #dlsig_p = {}
        for iclass in lclass:
          dlsig_p[reg, expr, iclass] = range(nwbin)
          for iw in liw:
            n = dlnum[reg, expr, iclass][iw]
            if n == 0.0:
              sig = miss_dbl
            else:
              sx2 = dlsp2[reg, expr, iclass][iw] 
              mx  = dlp[reg, expr, iclass][iw]
              sig = sqrt( (sx2 - n*mx*mx)/n )
            #
            dlsig_p[reg, expr, iclass][iw] = sig
        #
        asig_p = zeros((nclass+1)*nwbin).reshape(nclass+1, nwbin)
        for iclass in lclass:
          for iw in liw:
            asig_p[iclass, iw] = dlsig_p[reg, expr, iclass][iw]
        
        
        #----------------
        # sigma omega
        #----------------
        #dlsig_w = {}
        for iclass in lclass:
          dlsig_w[reg, expr, iclass] = range(nwbin)
          for iw in liw:
            n = dlnum[reg, expr, iclass][iw]
            if n == 0.0:
              sig = miss_dbl
            else:
              sx2 = dlsw2[reg, expr, iclass][iw]
              mx  = dlw[reg, expr, iclass][iw]
              sig = sqrt( (sx2 - n*mx*mx)/n )
            #
            dlsig_w[reg, expr, iclass][iw] = sig
        #
        asig_w = zeros((nclass+1)*nwbin).reshape(nclass+1, nwbin)
        for iclass in lclass:
          for iw in liw:
            asig_w[iclass, iw] = dlsig_w[reg, expr, iclass][iw]
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
          sp  = sum(dlsp[reg, expr, -1])
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
          # c-w     # w: [hPa/sec] 
          #-----------------
          plt.clf()
          c_w_name = pictdir  + "/p%05.2f.r%04d.c.w.cn%02d.%s.png"%(xth, crad, nclass, reg)
          lx  = lclass[1:]
          ly  = -1.0*ma.masked_equal(aw[1:,0], miss_dbl) * 0.01
          #
          lx  = ma.masked_where(ly.mask, lx)
          #
          plt.plot(lx, ly, c=col0, lw = wline)
          #
          ye  = asig_w[1:, 0] * 0.01
          plt.errorbar(lx, ly, yerr = ye, c="%s"%(col0))
          plt.xlim(0, nclass+1)
          #
          plt.suptitle("C.vs.W")
          plt.title(sspec0)
          plt.savefig(c_w_name)

          dxx[era, xth] = array(lx)
          dyy[era, xth] = array(ly)
          daa[era, xth] = ye
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
            ly  = array(ap[iclass][1:])
            lx  = ma.masked_where(ly==miss_dbl, lwbin[1:]).filled(miss_dbl)
            lye = ma.masked_where(ly==miss_dbl, asig_p[iclass][1:]).filled(miss_dbl)
            #
            lx  = func.del_miss(lx,  miss_dbl)
            ly  = func.del_miss(ly,  miss_dbl)
            lye = func.del_miss(lye, miss_dbl)
            #
            ly  = array(ly) * 60.*60.*24.
            lye = array(lye)* 60.*60.*24.
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
            lx  = ma.masked_where(ly == miss_dbl, lwbin[1:]).filled(miss_dbl)
            lye = ma.masked_where(ly == miss_dbl, asig_p[iclass][1:]).filled(miss_dbl)
            #

            lx  = func.del_miss(lx,  miss_dbl)
            ly  = func.del_miss(ly,  miss_dbl)
            lye = func.del_miss(lye, miss_dbl)
            #
            ly  = array(ly)  *60*60*24.0
            lye = array(lye) *60*60*24.0
            #--------
            if len(lx) == 0:
              continue
            #--------
            plt.plot(lx, ly, lw = wline)
            ##
            dplt[iclass] = plt.errorbar(lx, ly, yerr = lye, lw=wline, label="%02d"%(iclass))[0]
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
            ly  = array(dlnum[reg, expr, iclass][1:])
            ly  = ma.masked_equal(ly, miss_dbl).filled(0.0)
            lx  = array(lwbin[1:])
            #
            lx  = func.del_miss(lx,  miss_dbl)
            ly  = func.del_miss(ly,  miss_dbl)
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
            ly  = array(dlnum[reg, expr, iclass][1:])
            ly  = ma.masked_equal(ly, miss_dbl).filled(0.0)
            lx  = array(lwbin[1:])
            #
            dplt[iclass] = plt.plot(lx, ly, lw = wline)[0]
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
            ly  = array(dlrnum[reg, expr, iclass][1:])
            ly  = ma.masked_equal(ly, miss_dbl).filled(0.0)
            lx  = array(lwbin[1:])
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
            ly  = array(dlrnum[reg, expr, iclass][1:])
            ly  = ma.masked_equal(ly, miss_dbl).filled(0.0)
            lx  = array(lwbin[1:])
            #
            #
            dplt[iclass] = plt.plot(lx, ly, lw = wline)[0]
            ##
          #--
          llegend = map(str, lclass[1:])
          plt.legend( dplt.values(), llegend, "upper right")
          #
          plt.suptitle("PDF(W|Ci)")
          plt.title(sspec0)
          plt.savefig(w_rn_name)

      # end reg loop *********************************
    #* end era loop ***********************************
    #-----------------------------
    # figures for two expr
    #----------------------------- 
    dir_root  = "/media/disk2/out/CMIP5/day/%s/dif/%s/%04d-%04d.%04d-%04d/tracks/dura%02d/wfpr"%(model, dexpr["fut"], diyear["his"], deyear["his"], diyear["fut"], deyear["fut"], thdura)
    pictdir = dir_root + "/plot/c%02dclasses"%(nclass)
    func.mk_dir(pictdir)

    dlstyle  = {"his":"-", "fut":"--"}

    #------------------
    # color
    #------------------
    lcol_seg1  = list(linspace(0,0.8, len(lclass)))
    lcol_seg2  = [v for v in reversed(lcol_seg1)]
    lcol_seg3  = lcol_seg1[len(lclass)/2:] + lcol_seg1[0:len(lclass)/2]

    lcol       = lcol_seg1 + lcol_seg2 + lcol_seg3
    acol       = array(lcol).reshape(3,-1).T
    for reg in lreg:
      sspec0 = "%s, r=%s, dura=%s, xth=%02d, %s"%(reg, crad, thdura, xth, expr)
      #------------------
      # w-rn, with two expr
      #------------------
      plt.clf()
      dplt = {}
      w_rn_name = pictdir  + "/p%05.2f.r%04d.w.rn.%02d.%s.png"%(xth, crad, nclass, reg)
      llegend = []
      lplt    = []
      dlw     = {}
      dlrn    = {}
      #----------
      for iclass in lclass[1:]:
        for era in lera:
          expr = dexpr[era]
          #--
          ly  = array(dlrnum[reg, expr, iclass][1:])
          ly  = ma.masked_equal(ly, miss_dbl).filled(0.0)
          lx  = array(lwbin[1:])

          dlw[era, iclass] = lx
          dlrn[era, iclass]= ly
          #
          dplt[expr, iclass] = plt.plot(lx, ly, lw = wline, linestyle=dlstyle[era], c=acol[iclass])[0]
          #--------
          lplt.append(dplt[expr, iclass])
          llegend.append("%s"%(iclass))
      ##
      #--
      plt.legend( lplt, llegend, "upper right")
      #
      plt.suptitle("dPDF(W|Ci)")
      plt.title(sspec0)
      plt.savefig(w_rn_name)
      #------------------
      # dif of w-rn
      #------------------
      plt.clf()
      dplt = {}
      w_rn_name = pictdir  + "/dif.p%05.2f.r%04d.w.rn.%02d.%s.png"%(xth, crad, nclass, reg)
      llegend = []
      lplt    = []
      #--- prep --
      figplt  = plt.figure()
      axplt   = figplt.add_subplot(111)

      #for iclass in lclass[1:]:
      for iclass in lclass:
        expr = dexpr[era]
        #--
        ay_his = array(dlrnum[reg, dexpr["his"], iclass][1:])
        ay_fut = array(dlrnum[reg, dexpr["fut"], iclass][1:])
        ay_his = ma.masked_equal(ay_his, miss_dbl).filled(0.0)
        ay_fut = ma.masked_equal(ay_fut, miss_dbl).filled(0.0)

        ly  = ay_fut - ay_his
        lx  = array(lwbin[1:])
        #
        #
        dplt[expr, iclass] = axplt.plot(lx, ly, lw = wline, c=acol[iclass])[0]
        #--------
        lplt.append(dplt[expr, iclass])
        llegend.append("%s"%(iclass))
      ##
      #--
      axplt.legend( lplt, llegend, "upper right")
      #
      axplt.set_ylim( (-0.2, 0.2) )
      axplt.grid(True)
      axplt.set_title(sspec0)
      figplt.suptitle("dPDF(W|Ci)")
      figplt.savefig(w_rn_name)

      #------------------
      # dPDF(wi|Ci) * P(w)
      #------------------
      plt.clf()
      dplt = {}
      w_rn_name = pictdir  + "/dif.p%05.2f.r%04d.dYZ.%02d.%s.png"%(xth, crad, nclass, reg)
      llegend = []
      lplt    = []
      #--- prep --
      figplt  = plt.figure()
      axplt   = figplt.add_subplot(111)

      for iclass in lclass[1:]:
        expr = dexpr[era]
        #-----
        ay_his    = array(dlrnum[reg, dexpr["his"], iclass][1:])
        ay_fut    = array(dlrnum[reg, dexpr["fut"], iclass][1:])
        ac_p_his  = array(dlp[   reg, dexpr["his"], iclass][1:])
        ay_his    = ma.masked_equal(ay_his  , miss_dbl).filled(0.0)
        ay_fut    = ma.masked_equal(ay_fut  , miss_dbl).filled(0.0)
        ac_p_his  = ma.masked_equal(ac_p_his, miss_dbl).filled(0.0)
        #-----
        ly  = (ay_fut - ay_his) * ac_p_his *60.*60.*24.
        lx  = array(lwbin[1:])
        #
        dplt[expr, iclass] = axplt.plot(lx, ly, lw = wline, c=acol[iclass])[0]
        #--------
        lplt.append(dplt[expr, iclass])
        llegend.append("%s"%(iclass))
      ##
      #--
      axplt.legend( lplt, llegend, "upper right")
      #
      axplt.grid(True)
      axplt.set_title(sspec0)
      figplt.suptitle("dPDF(W|Ci)*P(W|Ci)")
      figplt.savefig(w_rn_name)

      #------------------
      # PDF(Ci) * dPDF(wi|Ci) * P(w)
      #------------------
      plt.clf()
      dplt = {}
      figname = pictdir  + "/dif.p%05.2f.r%04d.XdYZ.%02d.%s.png"%(xth, crad, nclass, reg)
      llegend = []
      lplt    = []
      #--- prep --
      figplt  = plt.figure()
      axplt   = figplt.add_subplot(111)

      dly = {}
      for iclass in lclass[1:]:
        expr = dexpr[era]
        #-----
        num_all   = sum([ dlnum[ reg, dexpr["his"], itemp] for itemp in lclass[1:] ])  # total number of cyclone for all class & all w
        num_ci    = sum(  dlnum[ reg, dexpr["his"], iclass])
        if num_all == 0.0:
          ac_num  = 0.0
        else:
          ac_rnum  = num_ci / num_all
        #-----
        ay_his    = array(dlrnum[reg, dexpr["his"], iclass][1:])
        ay_fut    = array(dlrnum[reg, dexpr["fut"], iclass][1:])
        ac_p_his  = array(dlp[   reg, dexpr["his"], iclass][1:])
        ay_his    = ma.masked_equal(ay_his  , miss_dbl).filled(0.0)
        ay_fut    = ma.masked_equal(ay_fut  , miss_dbl).filled(0.0)
        ac_p_his  = ma.masked_equal(ac_p_his, miss_dbl).filled(0.0)

        ly  = ac_rnum * (ay_fut - ay_his) * ac_p_his
        ly  = ly* 60.*60.*24.
        lx  = array(lwbin[1:])
        #

        dly[reg, xth, iclass] = ly
        #
        dplt[expr, iclass] = axplt.plot(lx, ly, lw = wline, c=acol[iclass])[0]
        print "iclass, ac_rnum",iclass, ac_rnum
        #--------
        lplt.append(dplt[expr, iclass])
        llegend.append("%s"%(iclass))
      ##
      #--
      axplt.legend( lplt, llegend, "upper right")
      #
      #axplt.set_ylim( (-0.02, 0.02) )
      axplt.grid(True)
      axplt.set_title(sspec0)
      figplt.suptitle("PDF(Ci) * dPDF(W|Ci)*P(W|Ci)")
      figplt.savefig(figname)
      print figname
      print reg, xth, "sum=", sum([sum(dly[reg, xth, i]) for i in [1,2,3,4]])

              
