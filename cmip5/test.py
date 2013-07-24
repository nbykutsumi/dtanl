import cmip_func

iyear = 2000
imon  = 2
iday  = 28
ihour = 0

year  = 2004
mon   = 3
day   = 1
hour  = 0

dhours= 6
noleapflag = True
pyindex = cmip_func.ret_pytimeindex(iyear,imon,iday,ihour,year,mon,day,hour,dhours,noleapflag)
print "pyindex",pyindex

pyindex_tmp = cmip_func.ret_pytimeindex_tmp(iyear,imon,iday,ihour,year,mon,day,hour,dhours,noleapflag)
print "pyindex_tmp",pyindex_tmp

t0 = datetime.datetime(iyear,imon,iday,ihour)
tt = datetime.datetime(year,mon,day,hour)



