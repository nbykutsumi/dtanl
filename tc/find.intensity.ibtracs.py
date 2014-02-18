idir  =  "/media/disk2/data/ibtracs/v03r04"
lregion = ["WP","NA"]
lyear = range(1970,2012+1)

dlwind  = {}
dlpres  = {}
for region in lregion:
  dlwind[region]   = []
  dlpres[region]   = []
  for year in lyear:
    iname = idir + "/Year.%04d.ibtracs_all.v03r04.csv"%(year)
    f=open(iname,"r"); lines=f.readlines(); f.close()

    for line in lines[3:]:
      line  = line.split(",")
      region_tmp  = line[3].strip()
      wind_tmp    = float(line[10])
      pres_tmp    = float(line[11])
      if (region_tmp == region):
        if wind_tmp > 0.0:
          dlwind[region].append(wind_tmp)
        if pres_tmp > 0.0:
          dlpres[region].append(pres_tmp)
      


