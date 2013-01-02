def ret_nxnyfig(region):
  if region == "ASAS":
    nx_fig   = 1300
    ny_fig   = 900
    return (nx_fig, ny_fig)
#------------------------
def ret_lonlat_center(region):
  if region == "ASAS":
    lon0   = 140.0
    lat0   = 90.0
    return (lon0, lat0)
#------------------------
def ret_latts(region):
  if region == "ASAS":
    latts  = 40.0
    return latts
#------------------------
def ret_domain_corner(region):
  if region == "ASAS":
    lllon = 106.5
    lllat = 0.5
    urlon = 208.0
    urlat = 41.0
    return (lllon, lllat, urlon, urlat)
#------------------------
def ret_xydom_first_last(region):
  if region == "ASAS":
    xdom_first = 74
    xdom_last  = 1228
    ydom_first = 55
    ydom_last  = 834
    return (xdom_first, xdom_last, ydom_first, ydom_last)
#------------------------


