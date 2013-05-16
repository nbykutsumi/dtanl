import datetime
def ret_nxnyfig(region, year, mon):
  today = datetime.date(year, mon, 1)
  if region == "ASAS":
    if (today < datetime.date(2006,1,1)):
      nx_fig   = 1300
      ny_fig   = 900
    if ( datetime.date(2006,1,1)<=today<datetime.date(2006,3,1)):
      nx_fig   = 1300
      ny_fig   = 900
    if ( datetime.date(2006,3,1)<=today):
      nx_fig   = 1190
      ny_fig   = 842
    return (nx_fig, ny_fig)
#------------------------
def ret_lonlat_center(region):
  if region == "ASAS":
    lon0   = 140.0
    lat0   = 90.0
    return (lon0, lat0)
#------------------------
def ret_latts(region, year, mon):
  # center latitude of the domain
  today = datetime.date(year, mon, 1)
  if region == "ASAS":
    if (today < datetime.date(2006,1,1)):
      latts  = 40.0
    if ( datetime.date(2006,1,1)<=today<datetime.date(2006,3,1)):
      latts  = 35.0
    if ( datetime.date(2006,3,1)<=today):
      latts  = 35.0

    return latts
#------------------------
def ret_domain_corner(region,year,mon):
  today = datetime.date(year, mon, 1)
  if region == "ASAS":
    if (today < datetime.date(2006,1,1)):
      #lllon = 106.5
      #lllat = 0.5
      #urlon = 208.0
      #urlat = 41.0

      # better?
      lllon = 106.5
      lllat = 0.5
      urlon = 208.5
      urlat = 40.5

    if ( datetime.date(2006,1,1)<=today<datetime.date(2006,3,1)):
      lllon = 109.5
      lllat = -5.5
      urlon = 219.5
      urlat = 32.5
    if ( datetime.date(2006,3,1)<=today):
      lllon = 109.5
      lllat = -5.5
      urlon = 219.5
      urlat = 32.5

  return (lllon, lllat, urlon, urlat)

#------------------------
def ret_domain_corner_rect(region):
  if region == "ASAS":
    lllon = 67.5
    lllat = 0.5
    urlon = 208.5
    urlat = 70.5

  return (lllon, lllat, urlon, urlat)
#------------------------
def ret_domain_corner_rect_forfig(region):
  if region == "ASAS":
    lllon = 66.0
    lllat = 0.0
    urlon = 210.0
    urlat = 74.0
  if region == "GLOB":
    lllon = 0.0
    lllat = -80.0
    urlon = 360.0
    urlat = 80.0
  if region == "JPN":
    lllon = 120.0
    lllat = 22.0
    urlon = 155
    urlat = 50.0
  if region == "W.JPN":
    lllon = 120.
    lllat = 27.
    urlon = 140.
    urlat = 40.
  if region == "E.JPN":
    lllon = 140.
    lllat = 30.
    urlon = 160.
    urlat = 40.

  return (lllon, lllat, urlon, urlat)



#------------------------
def ret_xydom_first_last(region, year, mon):
  today = datetime.date(year, mon, 1)
  if region == "ASAS":
    if (today < datetime.date(2006,1,1)):
      xdom_first = 74
      xdom_last  = 1228
      ydom_first = 55
      ydom_last  = 834
    if ( datetime.date(2006,1,1)<=today<datetime.date(2006,3,1)):
      xdom_first = 74
      xdom_last  = 1127
      ydom_first = 54
      ydom_last  = 860
    if ( datetime.date(2006,3,1)<=today):
      xdom_first = 74
      xdom_last  = 1163
      ydom_first = 6
      ydom_last  = 841

    return (xdom_first, xdom_last, ydom_first, ydom_last)
#------------------------
def ret_xydom_saone_rect_first_last(region):
  if region == "ASAS":
    lllon, lllat, urlon, urlat = ret_domain_corner_rect(region)
    xdom_saone_first = int((lllon - 0.5 + 0.5)/1.0)
    xdom_saone_last  = int((urlon - 0.5 + 0.5)/1.0)
    ydom_saone_first = int((lllat -(-89.5) + 0.5)/1.0)
    ydom_saone_last  = int((urlat -(-89.5) + 0.5)/1.0) 
    return (xdom_saone_first, xdom_saone_last, ydom_saone_first, ydom_saone_last)


