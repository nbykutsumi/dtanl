import Image
from numpy import *
import calendar
#--------------------
singleflag = False
lyear  = [2004]
lmon   = [1,4,6,7]
iday   =1
lhour  = [0]
idir   = "/home/utsumi/temp/tenkizu"
"""
"""
for year in lyear:
  for mon in lmon:
    #----
    if singleflag == True:
      eday  = iday
    else:
      eday  = calendar.monthrange(year,mon)[1]
    #----
    for day in range(iday,eday+1):
      for hour in lhour:
        tname1 = idir + "/front.loc.t.%04d.%02d.%02d.%02d.M1-0.30.M2-1.00.png"%(year,mon,day,hour)
        qname1 = idir + "/front.loc.q.%04d.%02d.%02d.%02d.M1-1.50.M2-1.50.png"%(year,mon,day,hour)
        qname2 = idir + "/front.loc.q.%04d.%02d.%02d.%02d.M1-2.00.M2-1.50.png"%(year,mon,day,hour)
        imgt1 = Image.open(tname1)
        #imgt2 = Image.open(tname2)
        imgq1 = Image.open(qname1)
        imgq2 = Image.open(qname2)
        a2t1  = asarray(imgt1)
        #a2t2  = asarray(imgt2)
        a2q1  = asarray(imgq1)
        a2q2  = asarray(imgq2)
        a2blank = ones(shape(a2t1), dtype=uint8) *255
        #--------
        a2join1  = concatenate((a2t1,a2blank),axis=1)
        a2join2  = concatenate((a2q1, a2q2) ,axis=1)
        a2join   = concatenate( (a2join1, a2join2), axis=0)
        imgjoin = Image.fromarray(a2join)
        oname   = idir + "/join.front.%04d.%02d.%02d.%02d.png"%(year,mon,day,hour)
        imgjoin.save(oname)
        print oname


