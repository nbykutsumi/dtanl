import cmip_func
import cmip_para
import ctrack_para

sunit="days since 1850-1-1"
scalendar = "360_day"
iyear = 2000
eyear = 2000

for season in range(1,12+1):
#for season in [11]:
  n1 = cmip_para.ret_totaldays_cmip(iyear,eyear,season,sunit=sunit, scalendar=scalendar)
  n2 = ctrack_para.ret_totaldays(iyear,eyear,season)
  print season,n1,n2



