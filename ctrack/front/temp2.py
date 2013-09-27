import front_func
year = 2004
mon  = 4
day  = 6
hour = 0
a2t  = front_func.wrap_front_t_saone(year,mon,day,hour, miss=-9999.0)
print a2t.max()

a2q  = front_func.wrap_front_q_saone(year,mon,day,hour, miss=-9999.0)
print a2q.max()


