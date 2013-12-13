import sys, netCDF4
#***************************************
def ret_upflag(model):
  #---
  if model in ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]:
    upflag = False
  elif model in ["MRI-CGCM3"]:
    upflag = True
  #---
  return upflag

#***************************************
def ret_lhour_6hr_cmip(model):
  if model in ["HadGEM2-ES","MIROC5","inmcm4","MPI-ESM-MR","NorESM1-M","MRI-CGCM3"]:
    lhour = [0,6,12,18]
  elif model in ["CNRM-CM5","CSIRO-Mk3-6-0","GFDL-CM3"]:
    lhour = [6,12,18,0]
  elif model in ["IPSL-CM5A-MR","IPSL-CM5B-LR"]:
    lhour = [3,9,15,21]
#lmodel=["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
  else:
    print "no model",model
    sys.exit()
  #
  return lhour

#***************************************
def ret_totaldays_cmip(iyear,eyear,season,sunit,scalendar):
  lyear = range(iyear,eyear+1)
  lmon  = ret_lmon(season)

  days  = 0
  for year in lyear:
    for mon in lmon:
      #-- last day ----
      if mon ==12:
        nextyear = year+1
        nextmon  = 1
      else:
        nextyear = year
        nextmon  = mon + 1

      nextmondate = netCDF4.netcdftime.datetime(nextyear,nextmon,1)
      etnum       = netCDF4.date2num( nextmondate, units=sunit, calendar=scalendar) - 1.0
      #-- first day ---
      idate       = netCDF4.netcdftime.datetime(year,mon,1)
      itnum       = netCDF4.date2num( idate, units=sunit, calendar=scalendar) 
      #-- days --------
      days = days + (etnum - itnum +1)
  #----
  return int(days)

#***************************************
def ret_lmon(season):
  if season == "DJF":
    lmon  = [1,2, 12]
  elif season == "MAM":
    lmon  = [3,4,5]
  elif season == "JJA":
    lmon  = [6,7,8]
  elif season == "SON":
    lmon  = [9,10,11]
  elif season == "ALL":
    lmon  = [1,2,3,4,5,6,7,8,9,10,11,12]
  elif type(season) == int:
    lmon  = [season]
  elif season == "NDJFMA":
    lmon  = [11,12,1,2,3,4]
  elif season == "MJJASO":
    lmon  = [5,6,7,8,9,10]
  elif season == "JJASON":
    lmon  = [6,7,8,9,10,11]
  elif season == "JJAS":
    lmon  = [6,7,8,9]
  return lmon

#***************************************
def ret_unit_calendar(model, expr):
  #*************************
  if expr in ["historical"]:
    if model == "HadGEM2-ES":sunit,scalendar = "days since 1859-12-01", "360_day"
    elif model == "IPSL-CM5A-MR":sunit,scalendar = "days since 1850-01-01 00:00:00", "noleap"
    elif model == "CNRM-CM5":sunit,scalendar = "days since 1850-1-1", "gregorian"
    elif model == "MIROC5":sunit,scalendar = "days since 1850-1-1", "noleap"
    elif model == "inmcm4":sunit,scalendar = "days since 1850-1-1", "365_day"
    elif model == "MPI-ESM-MR":sunit,scalendar = "days since 1850-1-1 00:00:00", "proleptic_gregorian"
    elif model == "CSIRO-Mk3-6-0":sunit,scalendar = "days since 1850-01-01 00:00:00", "noleap"
    elif model == "NorESM1-M":sunit,scalendar = "days since 1850-01-01 00:00:00", "noleap"
    elif model == "IPSL-CM5B-LR":sunit,scalendar = "days since 1850-01-01 00:00:00", "noleap"
    elif model == "GFDL-CM3":sunit,scalendar = "days since 1860-01-01 00:00:00", "noleap"
    elif model == "MRI-CGCM3":sunit,scalendar = "days since 1850-01-01", "standard"
  #*************************
  elif expr in ["rcp85","rcp45"]:    
    if model == "HadGEM2-ES":sunit,scalendar = "days since 1859-12-01", "360_day"
    elif model == "IPSL-CM5A-MR":sunit,scalendar = "days since 2006-01-01 00:00:00", "noleap"
    elif model == "CNRM-CM5":sunit,scalendar = "days since 2006-01-01 00:00:00", "gregorian"
    elif model == "MIROC5":sunit,scalendar = "days since 1850-1-1", "noleap"
    elif model == "inmcm4":sunit,scalendar = "days since 2006-1-1", "365_day"
    elif model == "MPI-ESM-MR":sunit,scalendar = "days since 1850-1-1 00:00:00", "proleptic_gregorian"
    elif model == "CSIRO-Mk3-6-0":sunit,scalendar = "days since 1850-01-01 00:00:00", "noleap"
    elif model == "NorESM1-M":sunit,scalendar = "days since 2006-01-01 00:00:00", "noleap"
    elif model == "IPSL-CM5B-LR":sunit,scalendar = "days since 2006-01-01 00:00:00", "noleap"
    elif model == "GFDL-CM3":sunit,scalendar = "days since 2006-01-01 00:00:00", "noleap"
    elif model == "MRI-CGCM3":sunit,scalendar = "days since 1850-01-01", "standard"
  #*************************
  #
  return sunit, scalendar
#***************************************
def ret_ens(model, expr, var):
  #-- default --
  ens = "r1i1p1"
  #-------------
  if expr =="historical":
    #-- fx -----
    if var in ["orog","sftlf"]:
      if model in ["HadGEM2-ES"]:
        ens = "r1i1p1"
      else:
        ens = "r0i0p0"
    else:
      if model in ["HadGEM2-ES"]:
        ens = "r2i1p1"

  elif expr =="rcp85":
    #-- fx -----
    if var in ["orog","sftlf"]:
      if model in ["HadGEM2-ES"]:
        ens = "r1i1p1"
      else:
        ens = "r0i0p0"
    #--- other vars --

  else:
    print "check expr",expr
    sys.exit()
  #-----------
  return ens
#----------------------


