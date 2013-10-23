from numpy import *
from ctrack_fsub import *
from dtanl_fsub import *
import ctrack_fig
import sys
#*********************************
if len(sys.argv) >1:
  model  = sys.argv[1]
  expr   = sys.argv[2]
  lmodel = [model]
  lexpr  = [expr]
#------------------
else:
  lmodel=["inmcm4","MPI-ESM-MR","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
  lexpr  = ["historical","rcp85"] 
#------------------

calcflag  = True
#calcflag  = False
ny,nx = (180,360)
radkm = 200.0  # (km)
miss  = -9999.0
thorog = 1300 #(m)
thgrad = 3    # (m/km)
thgrad2= 0.05  # (m/km/km)

lloop = [[model,expr] for model in lmodel for expr in lexpr]
for model, expr in lloop:
  print model,expr  
  idir  = "/media/disk2/data/CMIP5/sa.one.%s.%s/orog"%(model,expr)
  odir  = idir
  iname = idir + "/orog.%s.sa.one"%(model)
  maxorogname     = odir + "/maxtopo.%04dkm.sa.one"%(radkm)
  maxgradname     = odir + "/maxgrad.%04dkm.sa.one"%(radkm)
  maxgrad2name    = odir + "/maxgrad2.%04dkm.sa.one"%(radkm)
  
  if calcflag==True:
   
    a2orog     = fromfile(iname,float32).reshape(ny,nx)
    a2maxorog  = ctrack_fsub.mk_a2max_rad_saone(a2orog.T, radkm).T
    
    a2grad     = dtanl_fsub.mk_a2grad_abs_saone(a2orog.T).T
    a2maxgrad  = ctrack_fsub.mk_a2max_rad_saone(a2grad.T, radkm).T
  
    a2grad2    = dtanl_fsub.mk_a2grad_abs_saone(a2grad.T).T
    a2maxgrad2 = ctrack_fsub.mk_a2max_rad_saone(a2grad2.T, radkm).T
    
    #--- write to file -------
    a2maxorog.tofile(maxorogname)
    #
    a2maxgrad.tofile(maxgradname)
    #
    a2maxgrad2.tofile(maxgrad2name)
  
  #--- figure: max grad2  ----
  datname    = maxgrad2name
  a2maxgrad2 = fromfile(datname, float32).reshape(ny,nx) *1000.0*1000.0 # (m/km)
  a2maxgrad2 = ma.masked_greater_equal(a2maxgrad2, thgrad2)
  figname    = datname[:-7] + ".png"
  cbarname   = datname[:-7] + ".cbar.png"
  ctrack_fig.mk_pict_saone_reg(a2maxgrad2, soname=figname, cbarname=cbarname)
  print figname  
   
  
  #--- figure: max orog ----
  datname    = maxorogname
  a2maxorog  = ma.masked_greater_equal(fromfile(datname, float32).reshape(ny,nx), thorog)
  figname    = datname[:-7] + ".png"
  cbarname   = datname[:-7] + ".cbar.png"
  ctrack_fig.mk_pict_saone_reg(a2maxorog, soname=figname, cbarname=cbarname)
  print figname  
    
  #--- figure: max grad  ----
  datname    = maxgradname
  a2maxgrad  = fromfile(datname, float32).reshape(ny,nx) *1000.0 # (m/km)
  a2maxgrad  = ma.masked_greater_equal(a2maxgrad, thgrad)
  figname    = datname[:-7] + ".png"
  cbarname   = datname[:-7] + ".cbar.png"
  ctrack_fig.mk_pict_saone_reg(a2maxgrad, soname=figname, cbarname=cbarname)
  print figname  
  
