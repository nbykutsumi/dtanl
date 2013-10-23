import sys, math
#**********************************************
def combi(n,r):
  return math.factorial(n) / ( math.factorial(r)* math.factorial(n-r) )

#****************
def pcombi(n,r):
  p = 0.0
  for i in range(r,n+1):
    p = p + combi(n,i)
  #----
  p = p / (2.0**n)
  return p
#*****************
if len(sys.argv) >1:
  n = int(sys.argv[1])
  r = int(sys.argv[2])
else:
  print "usage: cmd [n] [r]"
  sys.exit()
  
print pcombi(n,r)
