import subprocess, cmip_para
###-------
#iyear = 1980
#eyear = 1999
#lexpr     = ["historical"]
#-------
iyear = 2080
eyear = 2099
lexpr     = ["rcp85"]
#-------

#lmodel=["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3","MRI-CGCM3"]
lmodel=["MRI-CGCM3"]

#*********************************
# fx
#---------------------------------
lloop = [[expr,model] for expr in lexpr for model in lmodel]
for expr, model in lloop:
  progname = "./nc2one.sfc.fx.py"
  print expr,model,"fx"
  scmd     = "python %s %s %s"%(progname, model, expr)
  subprocess.call(scmd, shell=True)

#*********************************
# atmosphere 6hrPlev
#---------------------------------
dattype = "6hrPlev"
tinc  = 6
lvar  = ["ua","va","ta"]
#lvar  = ["ua","ta"]
#lvar  = ["va"]
lyear = range(iyear,eyear+1)
lmon  = range(1,12+1)
llev  = [850, 500, 250]

lloop = [[expr, model, lev, var, year,mon] for expr in lexpr for model in lmodel for lev in llev for var in lvar for year in lyear for mon in lmon]

for expr, model, lev, var, year, mon in lloop:
  ens   = cmip_para.ret_ens(model,expr,var)
  progname = "./nc2one.atm.1lev.py"
  print "wrap-atm.1lev",expr, model, ens, lev, var, year, mon

  ##-- temp --
  #if (expr=="historical")&(model=="IPSL-CM5A-MR")&(var in ["ta","ua"]):
  #  print "skip",expr,lev,var,year,mon
  #  continue
  #elif (expr=="historical")&(model=="IPSL-CM5A-MR")&(var in ["va"])&(lev != 250):
  #  print "skip",expr,lev,var,year,mon
  #  continue


  #elif (expr=="rcp85")&(model=="IPSL-CM5A-MR")&(var in ["ua","va"]):
  #  print "skip",expr,lev,var,year,mon
  #  continue
  #elif (expr=="rcp85")&(model=="IPSL-CM5A-MR")&(var in ["ta"])&(lev != 250):
  #  print "skip",expr,lev,var,year,mon
  #  continue
  ##----------
  scmd     = "python %s %s %s %s %s %s %s %s %s %s"\
    %(progname, var, model, expr, ens, year, mon, dattype, tinc, lev)
  subprocess.call(scmd, shell=True)
#*********************************
# sea level pressure psl: 6hrPlev
#---------------------------------
var = "psl"
lyear = range(iyear,eyear+1)
lmon  = range(1,12+1)

lloop = [[expr, model, year, mon] for expr in lexpr for model in lmodel for year in lyear for mon in lmon]
for expr, model, year, mon in lloop:
  ens = cmip_para.ret_ens(model,expr,var)
  #
  progname = "./nc2one.psl.py"
  scmd     = "python %s %s %s %s %s %s"%(progname, model,expr,ens,year,mon)
  subprocess.call(scmd, shell=True)

#*********************************
# pr: day
#---------------------------------
lyear = range(iyear,eyear+1)
lmon  = range(1,12+1)

lloop = [[expr, model, year, mon] for expr in lexpr for model in lmodel for year in lyear for mon in lmon]
for expr, model, year, mon in lloop:
  ens = cmip_para.ret_ens(model,expr,"pr")
  #
  progname = "./nc2one.pr.day.py"
  scmd     = "python %s %s %s %s %s %s"%(progname,model,expr,ens,year,mon)
  subprocess.call(scmd, shell=True)


##*********************************
# monthly SST :Amon
#---------------------------------
var    = "ts"

lloop  = [[expr, model] for expr in lexpr for model in lmodel]
for expr, model in lloop:
  ens  = cmip_para.ret_ens(model,expr,var)
  #
  progname = "./nc2one.sfc.Amon.py"
  scmd     = "python %s %s %s %s %s %s %s"%(progname, var, model, expr, ens, iyear, eyear)
  subprocess.call(scmd, shell=True)


##*********************************
## pr: 3hr
##---------------------------------
#lyear = range(iyear,eyear+1)
#lmon  = range(1,12+1)
#
#lloop = [[expr, model, year, mon] for expr in lexpr for model in lmodel for year in lyear for mon in lmon]
#for expr, model, year, mon in lloop:
#  ens = cmip_para.ret_ens(model,expr,"pr")
#  #
#  progname = "./nc2one.pr.3hr.py"
#  scmd     = "python %s %s %s %s %s %s"%(progname,model,expr,ens,year,mon)
#  subprocess.call(scmd, shell=True)


