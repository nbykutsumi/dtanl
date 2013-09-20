from numpy import *
import ctrack_func
import ctrack_para

iyear = 1997
eyear = 2012
lhour = [0,6,12,18]

ny    = 180
nx    = 360
dlat  = 1.0
dlon  = 1.0
idir ="/media/disk2/data/ibtracs/v03r04"
odir_root ="/media/disk2/out/ibtracs/sa.one"
#------------------
a2totnum = zeros([ny,nx],float32)
for year in range(iyear, eyear+1):
  siname = idir + "/Year.%04d.ibtracs_all.v03r04.csv"%(year)
  #-- open -------
  f = open(siname, "r")
  lines = f.readlines()
  f.close()
  #-- init dictionary --
  ddat  = {}
  for mon in range(1,12+1):
    ddat[mon] = []
  #-- csv data loop -------------
  for line in lines[3:]:
    line     = line.split(",")
    isotime  = line[6].split(" ")
    date     = map(int, isotime[0].split("-"))
    mon      = date[1]
    hour     = int(isotime[1].split(":")[0])
    #--- check hour --
    if hour not in lhour:
      continue
    #--- check nature --
    nature   = line[7].strip()
    if nature not in ["TS"]:
      continue
    #-----------------
    tcname   = line[5].strip()
    lat      = float(line[16])
    lon      = float(line[17])
    ix       = int((lon- 0.0)/dlon)
    iy       = int((lat-(-90.0))/dlat)
    ldat_temp = [ix, iy, tcname] 
    ddat[mon].append(ldat_temp)

  #-- mon loop --------
  for mon in range(1,12+1):
    odir   = odir_root + "/%04d/%02d"%(year, mon)
    ctrack_func.mk_dir(odir) 
    soname = odir + "/freq.ibtracs_all.v03r04.3deg.sa.one"
    #--- init  --------
    a2num = zeros([ny,nx],float32)
    for ldat in ddat[mon]:
      ix  = ldat[0]
      iy  = ldat[1]
      a2num[iy,ix] = a2num[iy,ix] + 1.0
    #--- num -> freq ---
    totalnum   = ctrack_para.ret_totaldays(year, year, mon) * len(lhour)
    a2freq     = a2num / totalnum
    #--- write to file --
    a2freq.tofile(soname)
    print soname
    #--------------------
    a2totnum = a2totnum + a2num 
