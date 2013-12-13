from numpy import *
#*************************
def aphro2global_one(a2org_one, dattype, miss):
  if dattype in ["MA", "APHRO_MA"]:
    a2glob = ones([180,360], float32)*miss
    a2glob[90-15: 90+54+1, 60:149+1] = a2org_one
    return a2glob
#*************************
def global2aphro_one(a2glob, dattype):
  if dattype in ["MA", "APHRO_MA"]:
    a2aphro  = a2glob[90-15: 90+54+1, 60:149+1]
    return a2aphro
#*************************
def loadas_a2global(iname, dattype, miss):
  if dattype in ["MA", "APHRO_MA"]:
    a2aphro  = fromfile(iname, float32).reshape(70,90)
    a2glob   = aphro2global_one(a2aphro, dattype, miss)
    return a2glob
#*************************
def mk_metadata_one(odir, dattype):
  sunit  = "(mm s-1)"

  if dattype in ["MA", "APHRO_MA"]:
    ny_one   = 70
    nx_one   = 90
    newShape = array([ny_one, nx_one], int)
    lon_one_first  = 60.5
    lon_one_last   = 149.5
    lat_one_first  = -14.5
    lat_one_last   = 54.5
    dlat_one       = 1.0
    dlon_one       = 1.0
    a1lat_one  = arange(lat_one_first, lat_one_last + dlat_one*0.5, dlat_one)
    a1lon_one  = arange(lon_one_first, lon_one_last + dlon_one*0.5, dlon_one)
  
  #---- for latlon ------------
  def mk_latlontxt(odir):
    sout     = "\n".join(map( str, a1lat_one))
    f        = open( odir + "/lat.txt", "w")
    f.write(sout)
    f.close()
    #
    sout     = "\n".join(map( str, a1lon_one))
    f        = open( odir + "/lon.txt", "w")
    f.write(sout)
    f.close()
  #---- for dimtxt ------------
  def mk_dimtxt(odir):
    sout   = "lev %d\nlat %d\nlon %d"%(1, ny_one, nx_one)
    f      = open( odir + "/dims.txt", "w")
    f.write(sout)
    f.close()
  #--- for unit file -----------
  def mk_unittxt(odir):
    sout   = "unit: %s"%(sunit)
    f      = open( odir + "/unit.txt","w")
    f.write(sout)
    f.close()
  #-- readme -------------------
  def mk_readme(odir):
    sout   = "mean precipitation rate (%s)\n"%(sunit)
    sout   = sout + "daily mean"
    f      = open( odir + "/readme.txt","w")
    f.write(sout)
    f.close()
  #-----------------------------
  mk_latlontxt(odir)
  mk_dimtxt(odir)
  mk_unittxt(odir)
  mk_readme(odir)
    

