from netCDF4 import *
from numpy import *
import os
import calendar
#####################################################
odir_root ="/media/disk2/data/CMIP5/bn"
#####################################################
#var = "wap" #wap, zg, hur, hus
#lvar = ["wap", "zg"]
#lvar = ["ta","hus"]
lvar = ["ta"]
#tstp = "day"
#tstp  = "6hr"
tstp  = "6hrLev"
tinc  = {"6hr":6,  "6hrLev":6}
hlast = {"6hr":18, "6hrLev":18}

#hdattype = "Plev"
#lmodel = ["NorESM1-M", "MIROC5", "CanESM2"]
lmodel = ["NorESM1-M"]
#expr = "historical" #historical, rcp85
#expr = "rcp85"
#lexpr = ["historical", "rcp85"]
#lexpr = ["historical"]
lexpr = ["rcp85"]
ens  = "r1i1p1"
#####################################################
#####################################################
# Function
#####################################################
def mul_a2(a2, n):
  (ny, nx) = shape(a2)
  #----
  l  = a2.flatten().tolist() * n
  a3 = array(l).reshape(n, ny, nx)
  return a3
#-----------------------
def a1z_to_a3zyx(a1, ny, nx):
  nz = len(a1)
  l  = a1.tolist() * nx*ny
  a3 = array(l).reshape(nx,ny,nz).T
  return a3
#-----------------------
def dumpdata(iname, nc):
  print namedump
  #if not os.access( namedump, os.F_OK):
  ##########
  def a2s(a):
    s="\n".join(map(str, list(a))).strip()
    return s
  ##########
  def totext(filename, s):
    f = open(filename, "w")
    f.write(s)
    f.close()
  ##########
  os.system("ncdump -h %s > %s"%(iname, namedump))
  slat  = a2s( nc.variables["lat"][:])
  slon  = a2s( nc.variables["lon"][:])
  lenlat= len(nc.variables["lat"][:])
  lenlon= len(nc.variables["lon"][:])
  #--
  if tstp not in ["6hrLev"]:
    slev   = a2s( nc.variables["plev"][:])
    lenlev = len(nc.variables["plev"][:])
  else:
    lenlev = len(nc.variables["lev"][:])
  #--
  sdims="lev %s\nlat %s\nlon %s"\
        %(lenlev, lenlat, lenlon)
  ###
  totext(namelat, slat)
  totext(namelon, slon)
  if tstp not in["6hrLev"]:
    totext(namelev, slev)
  totext(namedims, sdims)
  print namedump
#####################################################
#####################################################
for model in lmodel:
  for expr in lexpr:
    for var in lvar:
      #####################################################
      # set dlyrange
      #####################################################
      dlyrange     = {}
      #
      if ( (var in ["ua","va"]) and (tstp in ["6hr"])):
        dlyrange["NorESM1-M", "historical"]  = [[1980,1984],[1985,1989],[1990,1994],[1995,1999]]
        dlyrange["NorESM1-M", "rcp85"]       = [[2076,2080],[2081,2085],[2086,2090],[2091,2095]]

      elif ( tstp in ["6hrLev"] ):
        #dlyrange["NorESM1-M", "historical"]  = [[1991,1991],[1992,1992], [1993,1993]]
        #dlyrange["NorESM1-M", "historical"]  = [[1998,1998]]
        dlyrange["NorESM1-M", "rcp85"]  = [[2086,2086],[2087,2087],[2088,2088],[2089,2089],[2090,2090],[2091,2091],[2092,2092],[2093,2093],[2094,2094],[2095,2095]]

      else:
        dlyrange["NorESM1-M", "historical"]  = [[1980,1989],[1990,1999]]
        dlyrange["NorESM1-M", "rcp85"]       = [[2076,2085],[2086,2095],[2096,2100]]
        #
        dlyrange["MIROC5", "rcp85"]       = [[2080,2089], [2090,2099]]
        #
        dlyrange["CanESM2", "historical"]  = [[1979,2005]]
        dlyrange["CanESM2", "rcp85"]       = [[2081,2090], [2091,2100]]
      #------
      if tstp in ["6hrLev"]:
        lmonrange = [[1,6], [7,12]]
        #lmonrange = [[7,12]]
        #lmonrange = [[1,6]]
      else:
        lmonrange = [[1,12]]
      #----------------------------------------------------
      #####################################################
      #------------------------------
      # make heads and tails
      #------------------------------
      if (tstp == "day"):
        ihead = var + "_" + tstp + "_" +model + "_" + expr +"_"\
               +ens
        ohead = ihead
        odir_tail = var + "/" + tstp + "/" +model + "/" + expr +"/"\
               +ens
        odir_dump = odir_root + "/" +odir_tail

      elif (tstp == "6hrLev"):
        ihead = var + "_" + tstp + "_" +model + "_" + expr +"_"\
               +ens
        ohead = ihead
        odir_tail = var + "/" + tstp + "/" +model + "/" + expr +"/"\
               +ens
        odir_dump = odir_root + "/" +odir_tail

      else:
        ihead = var + "_" + tstp + hdattype + "_" +model + "_" + expr +"_"\
               +ens
        ohead = var + "_" + tstp + "_" +model + "_" + expr +"_"\
               +ens
        odir_tail = var + "/" + tstp + "/" +model + "/" + expr +"/"\
               +ens
        odir_dump = odir_root + "/" +odir_tail

        
      #------------------------------
      # set dir for nc input
      #------------------------------
      #incdir = "/media/disk2/data/CMIP5/nc/day/NorESM1-M"
      incdir = "/media/disk2/data/CMIP5/nc/%s/%s"%(tstp, model)
      #------------------------------
      # make dump
      #------------------------------
      try:
        os.makedirs(odir_dump)
      except OSError:
        pass
      namedump = odir_dump +"/ncdump.txt"
      namelon  = odir_dump +"/lon.txt"
      namelat  = odir_dump +"/lat.txt"
      namelev = odir_dump +"/lev.txt"
      namedims  = odir_dump +"/dims.txt"
  
      #------------------------------
      lyrange = dlyrange[model, expr]
      for yrange in lyrange:
        y0 = yrange[0]
        y1 = yrange[1]
        for monrange in lmonrange:
          istep = -1
          imon = monrange[0]
          emon = monrange[1]
          #--------------------
          if (tstp == "day"):
            itimerange="%04d0101-%04d1231"%(y0,y1)
          elif (tstp == "3hr"):
            itimerange="%04d01010130-%04d12312230"%(y0,y1, hlast[tstp])
          elif ( tstp == "6hrLev")&(emon ==6):
            itimerange="%04d%02d0100-%04d%02d3018"%(y0,imon,y1,emon)
          elif ( tstp == "6hrLev")&(emon ==12):
            itimerange="%04d%02d0100-%04d%02d3118"%(y0,imon,y1,emon)
          else:
            itimerange="%04d010100-%04d1231%02d"%(y0,y1, hlast[tstp])
          ######
          iname = "%s/%s_%s.nc"%(incdir, ihead, itimerange)
          #####
          print os.access(iname, os.F_OK)
          print "iname=", iname
          nc = Dataset(iname, "r", format="NETCDF")
          #####
          dumpdata(iname, nc)
          ny    = len(nc.variables["lat"][:])
          nx    = len(nc.variables["lon"][:])
          #--
          if tstp in ["6hrLev"]:
            nz  = len(nc.variables["lev"][:])
          else:
            nz  = len(nc.variables["plev"][:])
          #--
          #####
          for y in range(y0, y1+1):
            print y
            #############
            odir = odir_root + "/%s/%04d"%(odir_tail, y)
            print odir
            try:
              os.makedirs(odir)
            except OSError:
              pass
            #************
            #############
            print odir
            for m in range(imon,emon+1):
              ##############
              # no leap
              ##############
              if (m==2)&(calendar.isleap(y)):
                ed = calendar.monthrange(y,m)[1] -1
              else:
                ed = calendar.monthrange(y,m)[1]
              ##############
              for d in range(1, ed + 1):
                if (tstp == "day"):
                  istep = istep +1
                  stime = "%04d%02d%02d%02d"%(y,m,d,0)
                  ########
                  data = nc.variables["%s"%(var)][istep]
                  ########
                  oname = odir + "/%s_%s.bn"%(ohead, stime)
                  ########
                  f = open(oname, "wb")
                  f.write(data)
                  f.close()
                #-------------
                elif (tstp == "3hr"):
                  for h in range(1, 22+1, tinc[tstp]):
                    istep = istep + 1
                    stime = "%04d%02d%02d%02d30"%(y,m,d,h)
                    ########
                    data = nc.variables["%s"%(var)][istep]
                    ########
                    oname = odir + "/%s_%s.bn"%(ohead, stime)
                    ########
                    f = open(oname, "wb")
                    f.write(data)
                    f.close()
                #-------------- 
                else:
                  for h in range(0, 23+1, tinc[tstp]):
                    istep = istep + 1
                    print istep, y, m, d, h
                    stime = "%04d%02d%02d%02d"%(y,m,d,h)
                    ########
                    data = nc.variables["%s"%(var)][istep]
                    ########
                    oname = odir + "/%s_%s.bn"%(ohead, stime)
                    ########
                    f = open(oname, "wb")
                    f.write(data)
                    f.close()
  
                    #----------------
                    # make pa for 6hrLev
                    #----------------
                    if tstp in ["6hrLev"]:
                      a1a    = nc.variables["a"][:]
                      a1b    = nc.variables["b"][:]
                      p0     = nc.variables["p0"][:]
                      a2ps   = nc.variables["ps"][istep]
                      ##
                      a3a    = a1z_to_a3zyx(a1a, ny, nx)
                      a3b    = a1z_to_a3zyx(a1b, ny, nx)
                      a3p0   = ones([nz, ny, nx], float32) * p0
                      a3ps   = mul_a2( a2ps, nz)
                      ##
                      a3pa   = a3a * a3p0 + a3b * a3ps
                      a3pa   = array(a3pa, float32)
                      #-- name -----------------
                      odir_tail_pa = "pa" + "/" + tstp + "/"\
                                     +model + "/" + expr +"/" +ens
                      odir_pa      = odir_root + "/%s/%04d"%(odir_tail_pa, y)
  
                      ihead_pa     = "pa" + "_" + tstp + "_" +model\
                                     + "_" + expr +"_"+ens
                      ohead_pa     = ihead_pa
                      oname_pa  = odir_pa  + "/%s_%s.bn"%(ohead_pa, stime)
                      try:
                        os.makedirs(odir_pa)
                      except OSError:
                        pass 
                      #-------------------------
                      f = open(oname_pa, "wb")
                      f.write(a3pa)
                      f.close()
  
