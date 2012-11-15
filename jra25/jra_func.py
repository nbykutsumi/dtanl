#-----------------------------
def del_miss(l, miss):
  #-----
  def f(x):
    if x != miss:
      return l
  #-----
  l = filter(f, l)
  return l
#-----------------------------

def read_llat(ctlname):
  f = open(ctlname, "r")
  lines = f.readlines()
  f.close()
  llats = []
  for i in range(len(lines)):
    line   = lines[i]
    s0     = line.split(" ")[0]
    if s0 == "ydef":
      i_first = i+1
      continue
    elif s0 == "tdef":
      i_last  = i-1
      break
  #--
  for line in lines[i_first:i_last+1]:
    ltemp = del_miss(line.split(" "), "")
    ltemp = map(float, ltemp)
    llats = llats + ltemp
  return llats
