from math import floor
def percentile(list,percent):
  list.sort()
  n=int(floor(len(list)*percent*0.01)+1)
  for i in range(n,len(list)+1):
    if i ==len(list):
      n_up=len(list)
    elif list[i-1]*1.0  < list[(i+1)-1]*1.0:
      n_up=i
      break
  for i in range(n,0,-1):
    if list[i-1]*1.0 < list[n-1]*1.0:
      n_low=i
      break
    elif i==1:
      n_low=0


  CRF=percent*0.01    # Cumulative Relative Frequency
  CRF_up=(n_up*1.0)/(len(list)*1.0)
  x_up=list[n_up-1] +0.5
  if(n_low !=0):
    CRF_low=(n_low*1.0)/(len(list)*1.0)
    x_low=list[n_low-1] +0.5
  else:
    CRF_low=0.0
    x_low=0.5
  x=x_low + (x_up -x_low)*(CRF-CRF_low)/(CRF_up -CRF_low)
  return len(list), x_low, x_up, x

def _main():
  print "usage: percentile(list, percent)"
  print "return: len(list), x_low, x_up, x"

if __name__ == "__main__": _main()
