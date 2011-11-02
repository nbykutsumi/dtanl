from numpy import *
from netCDF4 import *
import pygrib
import calendar
import os
########
IY,EY=1996,2009
IM,EM=8,8
########
IDIR_P="/media/disk2/data/CFSR/apcp/org"
IDIR_W= "/media/disk2/data/CFSR/vvel/org"
ODIR="/media/disk2/out/dtanl/WcfsrPcfsr"
LLEV=500  #hPa
DAYINC=5
WBIN=100  #[hPa]
#intBIN_min= -1
#intBIN_max= 1
intBIN_min=-30
intBIN_max=30
nBIN= intBIN_max -intBIN_min +1
nXp,nYp=720,361
fill_value=9.999e+20
########
class Listarrays:
  def __init__(self, la):
    self.la=la

  def acc(self):
    for i in range(len(self.la)):
      if i ==0:
        aTemp = self.la[i]
      else:
        aTemp= aTemp + self.la[i]

    return aTemp

  def ave(self):
    return self.acc() / float(len(self.la))
      
########
def RET_FILEDATE(Y,M,D):
  if D >= 26:
    D1,D2 = 26,calendar.monthrange(Y,M)[1]
  else:
    D1=int((D-1)/DAYINC) *DAYINC +1
    D2=D1 + 4

  return "%04d%02d%02d-%04d%02d%02d"%(Y,M,D1,Y,M,D2)
########
def Mk_Listarrays(lobj):
  lout=[]
  for i in range(len(lobj)):
    lout.append(lobj[i].values)

  return lout
########
def  write_netCDF(adata,oname,datunits):
  #open output file
  fout=Dataset(oname, "w", format="NETCDF4")
  ## dimensions
  fout.createDimension("latitude",361)
  fout.createDimension("longitude",720)
  fout.createDimension("omega_bin",nBIN)
  ## variables
  latitudes=fout.createVariable("latitude","f4",("latitude",))
  longitudes=fout.createVariable("longitude","f4",("longitude",))  
  omega_bins=fout.createVariable("omega_bin","f4",("omega_bin",))
  dats=fout.createVariable(\
      "dat","f4",("omega_bin","latitude","longitude",)\
      #,fill_value=9.999e+20\
      )
  ## units
  latitudes.units="degrees_north"
  longitudes.units="degrees_east"
  omega_bins.units="-hPa/day"
  dats.units="%s"%(datunits)
  ## FillValue
  #latitudes._FillValue=fill_value
  #longitudes._FillValue=fill_value
  #omega_bins._FillValue=fill_value
  #dats._FillValue=fill_value
  ## make data
  alat=arange(-90,90+0.1,0.5)
  alon=arange(0,359.5+0.1, 0.5)
  abin=range(intBIN_min*WBIN, intBIN_max*WBIN +1, WBIN)
  ## put data
  latitudes[:]=alat
  longitudes[:]=alon
  omega_bins[:]=abin
  dats[:]=adata
  ## close output file
  fout.close()

########


atimes=zeros(nYp*nXp*nBIN)
aSP=zeros(nYp*nXp*nBIN)
aSP2=zeros(nYp*nXp*nBIN)
#atimes=zeros(3*3*nBIN)
#aSP=zeros(3*3*nBIN)
#aSP2=zeros(3*3*nBIN)
for M in range(IM,EM+1):
  for Y in range(IY,EY+1):
    for D in range(1,calendar.monthrange(Y,M)[1]+1):
    #for D in range(1,2+1):
      iDATE=int("%04d%02d%02d"%(Y,M,D))
      print iDATE
      FILEDATE = RET_FILEDATE(Y,M,D)
      INAME_W= IDIR_W + "/pgbhnl.gdas.%s.subset"%(FILEDATE)
      INAME_P= IDIR_P + "/pgbh06.gdas.%s.subset"%(FILEDATE)
      print INAME_W
      ###
      if ((D % DAYINC) ==1) & (D !=31):
        IFILE_W= pygrib.open(INAME_W)
        IFILE_P= pygrib.open(INAME_P)
      ###
      loWorg= IFILE_W.select(dataDate=iDATE, level=LLEV)
      loPorg= IFILE_P.select(dataDate=iDATE)

      ###
      laW= Mk_Listarrays(loWorg)
      laP= Mk_Listarrays(loPorg)
      ###
      aWday=Listarrays(laW).ave() *-864  # Pa s**-1 --> -hPa day**-1
      aWday=aWday.flatten()        # Flatten!!
      aPday=Listarrays(laP).acc()
      aPday=aPday.flatten()        # Flatten!!

      ##############
      ## test
      ##############
      #print "aPday"
      #print aPday.reshape(nYp, nXp)


      ##############
      ## test data
      ##############
      #nXp=3
      #nYp=3
      #if D==1:
      #  aWday=array([[-10,-10,-10],[10,10,10],[101,101,101]])
      #else:
      #  aWday=array([[-10,-10,-10],[10,10,10],[10,10,10]])
      #
      #aPday=array([[1,1,1,],[1,1,1,],[1,1,1]])
      ############
      aWint=floor(aWday/ WBIN)
      aWint=(aWint> intBIN_max).choose(aWint,intBIN_max)
      aWint=(aWint< intBIN_min).choose(aWint,intBIN_min)
      ###
      atimes_tmp=array([])
      aSP_tmp=array([])
      ###############
      # for each bin
      ###############
      for i in range(intBIN_min,intBIN_max+1):
        amask= ma.masked_equal(aWint, i)*0  # if value is i, mask it.
        amask_not= ma.masked_not_equal(aWint,i)*0
        atimes_i= ma.filled(amask, 1)
        atimes_tmp  = append(atimes_tmp, atimes_i) 
        ######
        # precip
        ######
        aP_i = ma.masked_where(amask_not==True, aPday).filled(0) 
        aSP_tmp  = append(aSP_tmp, aP_i) 

      atimes= atimes + atimes_tmp
      aSP   = aSP    + aSP_tmp
      aSP2  = aSP2   + aSP_tmp**2 
      #########
      ## test
      #########
      #ain=aSP
      ##print "aSP"
      ##print ain.shape
      #ain=ain.reshape(nBIN, nYp, nXp)
      ##print ain.shape
      #atmp = zeros(nYp*nXp).reshape(nYp,nXp)
      #for i in range(0,nBIN):
      #  atmp = atmp + ain[i]
      #print atmp
      #print sum(atmp)
      #########
      ## test
      #########
      #ain=(aSP /ma.masked_equal(atimes,0)).filled(0)
      #print "aPave"
      #print ain.shape
      #ain=ain.reshape(nBIN, nYp, nXp)
      #print ain.shape
      #atmp = zeros(nYp*nXp).reshape(nYp,nXp)
      #for i in range(0,nBIN):
      #  atmp = atmp + ain[i]
      #print atmp
      #print sum(atmp)



  ###########
  # average
  ###########
  aPave= aSP /ma.masked_equal(atimes,0)
  ###########
  # sigma
  ###########
  aPstd =sqrt( (atimes * (aPave)**2 \
              -2 *aPave * aSP \
              +aSP2) *atimes**(-1))
  ###########
  # output name
  ###########
  odate="%04d-%04d%-%02d"%(IY,EY,M)
  name_tail="%s-%sb-0.5.nc"%(odate,nBIN)
  oname_Pave=  ODIR +"/pave.%s"%(name_tail)
  oname_Pstd=  ODIR +"/pstd.%s"%(name_tail)
  oname_SP2 =  ODIR +"/pac2.%s"%(name_tail)
  oname_SP  =  ODIR +"/pacc.%s"%(name_tail)
  oname_Wtime=ODIR +"/wtim.%s"%(name_tail)
  
  aPave=aPave.reshape(nBIN ,nYp, nXp)
  ###########
  # summary
  ###########
  # aPave: masked
  # aPstd: masked
  # aSP  : not masked
  # aSP2 : not masked
  # atimes:not masked
  
  ###########
  # write
  ###########
  aPave = aPave.filled(fill_value).reshape(nBIN,nYp,nXp)
  write_netCDF(aPave, oname_Pave, "mm/day")
  #
  aPstd = aPstd.filled(fill_value).reshape(nBIN,nYp,nXp)
  write_netCDF(aPstd, oname_Pstd, "mm/day")
  #
  aSP = aSP.reshape(nBIN,nYp,nXp)
  write_netCDF(aSP, oname_SP, "mm/day")
  #
  aSP2 = aSP2.reshape(nBIN,nYp,nXp)
  write_netCDF(aSP2, oname_SP2, "(mm/day)**2")
  #
  atimes = atimes.reshape(nBIN,nYp,nXp)
  write_netCDF(atimes, oname_Wtime, "days")
  ################
 
