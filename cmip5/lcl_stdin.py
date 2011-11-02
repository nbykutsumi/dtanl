import commands
###############################
Psfc = 1000
Tsfc = 293.15
q    = 0.0087268
#####
cmd = "/home/utsumi/bin/dtanl/cmip5/lcl_stdin"
###############################
lTsfc = range(-10,46,2)                       #[deg.C]
lq    = [1,2,4,6,8,10,15,20,30,40,50,70,90]   #[g/kg]
#--- convert unit ------------
lTsfc = [ x+273.15 for x in lTsfc]  # [K]
lq    = [ x*0.001 for x in lq ]     # [kg/kg]
########################################
soname = "/home/utsumi/temp/LCL-q-Tsfc.csv"
########################################
# FUNCTIONS
########################################
def Array2csv(a):
  return "\n".join([",".join( map(str, sublist) ) for sublist in a ])
########################################
def mk_lm(im,em):
  if im <= em:
    lm = range(im, em+1)
  else:
    lm = range(im, 12+1) + range(1, em+1)
  return lm
########################################
lout = []
llabel = ["T/q"] + [x for x in lq]
lout.append(llabel)
for Tsfc in lTsfc:
  lseg=[Tsfc]
  for q in lq:
    output = commands.getoutput("%s %s %s %s"%(cmd,Psfc, Tsfc, q))
    lseg.append(output)
  lout.append(lseg)
#------------------------
sout = Array2csv(lout)
#
f = open(soname, "w")
f.write(sout)
f.close
