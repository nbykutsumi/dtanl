import datetime
import calendar, netCDF4
from numpy import *
#***************************************
def ret_times(iyear,eyear,lmon, sunit, scalendar, stepday):
  ldtime  = []
  ltnum   = []
  #-------
  for year in range(iyear, eyear+1):
    for mon in lmon:
      idtime = netCDF4.netcdftime.datetime(year, mon,1,0,0)
      itnum  = netCDF4.date2num(idtime, sunit, scalendar)
      tnum   = itnum - stepday
      while 1==1:
        tnum   = tnum + stepday
        dtime  = netCDF4.num2date(tnum, sunit, scalendar)
        #------------
        mont   = dtime.month
        #-- check ---
        if mont != mon:
          break
        #------------ 
        ldtime.append(dtime)
        ltnum.append(tnum)
  #---------
  return array(ldtime), array(ltnum)


#***************************************
def ret_filedate(var, dattype, model, expr, ens, iyear, imon, iday, ihour, imin, eyear, emon, eday, ehour, emin):
  #var    = "psl"
  #dattype= "6hrPlev"
  #model  = "MIROC5"
  #expr   = "historical"
  #ens    = "r1i1p1"
  #iyear,imon,iday,ihour  = (1995,3,13,0)
  #eyear,emon,eday,ehour  = (1999,4,5,0)

  iyear,imon,iday,ihour,imin = map(int, [iyear,imon,iday,ihour,imin])
  eyear,emon,eday,ehour,emin = map(int, [eyear,emon,eday,ehour,emin])

  idir = "/home/utsumi/mnt/iis.data2/CMIP5/cmip5.working"
  listname = idir + "/%s.%s.list.csv"%(model,expr)
  f = open(listname, "r")
  lines = f.readlines()
  f.close()
  itime  = datetime.datetime(iyear,imon,iday,ihour,imin)
  etime  = datetime.datetime(eyear,emon,eday,ehour,emin)

  #itime  = date2cmiptime(iyear,imon,iday,ihour,imin, noleapflag)
  #etime  = date2cmiptime(eyear,emon,eday,ehour,emin, noleapflag)
  #---------------
  lout  = []
  for line in lines:
    line = line.split(",")
    var_tmp     = line[0]
    dattype_tmp = line[1]
    model_tmp   = line[2]
    expr_tmp    = line[3]
    ens_tmp     = line[4]
    fyear0      = int(line[5])
    fmon0       = int(line[6])
    fday0       = int(line[7])
    fhour0      = int(line[8])
    fmin0       = int(line[9])
    #fdate0      = line[10]
    fyear1      = int(line[11])
    fmon1       = int(line[12])
    fday1       = int(line[13])
    fhour1      = int(line[14])
    fmin1       = int(line[15])
    #fdate1      = line[16]
    sunit       = line[17]
    scalendar   = line[18]
    ncname      = line[19].strip()
    #-- datetime ----
    ftime0      = datetime.datetime(fyear0,fmon0,fday0,fhour0,fmin0)
    ftime1      = datetime.datetime(fyear1,fmon1,fday1,fhour1,fmin1)

    #----
    lout_tmp    = [fyear0,fmon0,fday0,fhour0,fmin0,ftime0,fyear1,fmon1,fday1,fhour1,fmin1,ftime1,sunit,scalendar,ncname]
    #-- check -----
    if ((var_tmp == var)&(dattype_tmp==dattype)&(model_tmp==model)&(expr_tmp==expr)&(ens_tmp==ens)):
      #
      if (itime <= ftime0)&(ftime0 <= etime):
        lout.append(lout_tmp)
      elif (itime <= ftime1)&(ftime1 <= etime):
        lout.append(lout_tmp)
      elif (itime <= ftime0)&(ftime1 <= etime):
        lout.append(lout_tmp)
      elif (ftime0 <= itime)&(etime <= ftime1):
        lout.append(lout_tmp)
    #--------------
  return lout
  #----------------
#***************************************
def cmiptime2date(cmiptime, noleapflag=True):
  time0  = datetime.datetime(1850,1,1,0,0)
  timet  = time0 + datetime.timedelta(seconds=cmiptime*60*60*24)
  #---
  if noleapflag == True:
    for year_tmp in range(1850,timet.year+1):
      if calendar.isleap(year_tmp):
        if datetime.datetime(year_tmp,2,29,0) <= timet:
          timet = timet + datetime.timedelta(seconds=60*60*24)
  #---
  year   = timet.year
  mon    = timet.month
  day    = timet.day
  hour   = timet.hour
  minute = timet.minute 
  return year,mon,day,hour,minute


#***************************************
def date2cmiptime(year,mon,day,hour,minute, noleapflag=True):
  time0  = datetime.datetime(1850,1,1,0,0)
  timet  = datetime.datetime(year,mon,day,hour,minute)
  ds     = (timet - time0).total_seconds()
  #---
  if noleapflag == True:
    for year_tmp in range(1850,year+1):
      if calendar.isleap(year_tmp):
        if datetime.datetime(year_tmp,2,29,0) <= timet:
          ds = ds - 24*60*60
  #---
  dday   = ds / (24.*60.*60.)
  return dday     
#***************************************
def ret_pytimeindex(iyear,imon,iday,ihour,year,mon,day,hour, dhours, noleapflag=True):
  time0   = datetime.datetime(iyear,imon,iday,ihour)
  timet   = datetime.datetime(year,mon,day,hour)
  pyindex = (timet - time0).total_seconds() / (60*60*dhours)
  #-- check leap ---
  if noleapflag ==True:
    for year_tmp in range(iyear, year+1):
      if calendar.isleap(year_tmp):
        if datetime.datetime(iyear,imon,iday,ihour) <= datetime.datetime(year_tmp,2,29,0):
          if datetime.datetime(year_tmp,2,29,0) <= datetime.datetime(year,mon,day,hour):
            pyindex = pyindex - 24/dhours

  #--
  pyindex = int(pyindex)
  return pyindex

    
#***************************************

  
