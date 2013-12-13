from numpy import *
from myfunc_fsub import *
ny,nx = 180,360
miss = -9999.0
#filterflag = "3x3"
#filterflag = "5x5"
filterflag = "7x7"

idir = "/media/disk2/out/CMIP5/sa.one.HadGEM2-ES.historical/6hr/exc/freq.48h/1980-1999.ALL"
iname = idir + "/freq.exc.HadGEM2-ES.r2i1p1.rad0001km.1980-1999.ALL.sa.one"

a2in  = fromfile(iname, float32).reshape(180,360)

##--------------
#a2filter = array(\
#           [[1,2,1]\
#           ,[2,4,2]\
#           ,[1,2,1]], float32)
##--------------
a2filter3x3 = array(\
           [[1,1,1]\
           ,[1,1,1]\
           ,[1,1,1]], float32)
#--------------
a2filter5x5 = array(\
           [[1,1,1,1,1]\
           ,[1,1,1,1,1]\
           ,[1,1,1,1,1]\
           ,[1,1,1,1,1]\
           ,[1,1,1,1,1]], float32)
#--------------
a2filter7x7 = array(\
           [[1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1]\
           ,[1,1,1,1,1,1,1]], float32)
#--------------


#

if filterflag == "3x3":
  a2in1 = myfunc_fsub.mk_a2convolution_3x3(a2in.T,  a2filter3x3.T, miss).T
  a2in2 = myfunc_fsub.mk_a2convolution_3x3(a2in1.T, a2filter3x3.T, miss).T
  a2in3 = myfunc_fsub.mk_a2convolution_3x3(a2in2.T, a2filter3x3.T, miss).T
elif filterflag == "5x5":
  a2in1 = myfunc_fsub.mk_a2convolution_5x5(a2in.T,  a2filter5x5.T, miss).T
  a2in2 = myfunc_fsub.mk_a2convolution_5x5(a2in1.T, a2filter5x5.T, miss).T
  a2in3 = myfunc_fsub.mk_a2convolution_5x5(a2in2.T, a2filter5x5.T, miss).T
elif filterflag == "7x7":
  a2filter = a2filter7x7
  a2in1 = myfunc_fsub.mk_a2convolution(a2in.T,  a2filter.T, miss).T
  a2in2 = myfunc_fsub.mk_a2convolution(a2in1.T, a2filter.T, miss).T
  a2in3 = myfunc_fsub.mk_a2convolution(a2in2.T, a2filter.T, miss).T



m0  = mean(a2in,  axis=0)
m1  = mean(a2in1, axis=0)
m2  = mean(a2in2, axis=0)
m3  = mean(a2in3, axis=0)

#*********************
# JRA
#*********************
jradir   = "/media/disk2/out/JRA25/sa.one.anl_p/6hr/exc/c48h.bsttc/1980-1999.ALL"
jraname  = jradir + "/freq.exc.rad0001km.bsttc.1980-1999.ALL.sa.one"
a2jra    = fromfile(jraname, float32).reshape(ny,nx)

if filterflag == "3x3":
  a2jra1 = myfunc_fsub.mk_a2convolution_3x3(a2jra.T,  a2filter3x3.T, miss).T
  a2jra2 = myfunc_fsub.mk_a2convolution_3x3(a2jra1.T, a2filter3x3.T, miss).T
  a2jra3 = myfunc_fsub.mk_a2convolution_3x3(a2jra2.T, a2filter3x3.T, miss).T
elif filterflag == "5x5":
  a2jra1 = myfunc_fsub.mk_a2convolution_5x5(a2jra.T,  a2filter5x5.T, miss).T
  a2jra2 = myfunc_fsub.mk_a2convolution_5x5(a2jra1.T, a2filter5x5.T, miss).T
  a2jra3 = myfunc_fsub.mk_a2convolution_5x5(a2jra2.T, a2filter5x5.T, miss).T
elif filterflag == "7x7":
  a2filter = a2filter7x7
  a2jra1 = myfunc_fsub.mk_a2convolution(a2jra.T,  a2filter.T, miss).T
  a2jra2 = myfunc_fsub.mk_a2convolution(a2jra1.T, a2filter.T, miss).T
  a2jra3 = myfunc_fsub.mk_a2convolution(a2jra2.T, a2filter.T, miss).T


j0  = mean(a2jra,  axis=0)
j1  = mean(a2jra1, axis=0)
j2  = mean(a2jra2, axis=0)
j3  = mean(a2jra3, axis=0)





