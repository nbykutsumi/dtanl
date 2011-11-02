import commands
###############################
Psfc = 1000 # [hPa]
Psfc = 100.0* Psfc  #[hPa] -> [Pa]
Tsfc = 293.15
q    = 0.0087268
#####
cmd = "/home/utsumi/bin/dtanl/cmip5/lcl_rh_stdin"
###############################
lTsfc = range(-10,46,2)                       #[deg.C]
lRH    = [5,10,30,50,70,90,99]   #[%]
lRH = [float(x) for x in lRH]
#--- convert unit ------------
lTsfc = [ x+273.15 for x in lTsfc]  # [K]
########################################
soname = "/home/utsumi/temp/LCL-RH-Tsfc.csv"
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
llabel = ["T/RH"] + [x for x in lRH]
lout.append(llabel)
for Tsfc in lTsfc:
  lseg=[Tsfc]
  for RH in lRH:
    output = commands.getoutput("%s %s %s %s"%(cmd,Psfc, Tsfc, RH))
    output = float(output)*0.01   # [Pa] -> [hPa]
    lseg.append(output)
  lout.append(lseg)
#------------------------
sout = Array2csv(lout)
#
f = open(soname, "w")
f.write(sout)
f.close
print soname
