import subprocess

#lyear  = [1999,2007,1990,1991,1992,1993,1994,1995,1996]
lyear  = [2000,2001,2002,2003,2005,2006]
lmon   = [1,2,3,4,5,6,7,8,9,10,11,12]
#lmon   = [4,5,6,7,8,9,10,11,12]

lmodel = ["org"]
#lmodel = ["HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3"]
#lmodel = ["org","HadGEM2-ES","IPSL-CM5A-MR","CNRM-CM5","MIROC5","inmcm4","MPI-ESM-MR","CSIRO-Mk3-6-0","NorESM1-M","IPSL-CM5B-LR","GFDL-CM3","test.1.5deg","test.10deg","test.5deg","test.3deg"]
#lmodel = ["test.1.5deg","test.10deg","test.5deg","test.3deg"]
#lmodel = ["HadGEM2-ES","IPSL-CM5B-LR"]

#lvar   = ["PRMSL", "SPFH", "TMP", "UGRD", "VGRD"]
#lvar   = ["UGRD", "VGRD"]
#lvar   = ["SPFH", "TMP", "UGRD", "VGRD"]
#lvar    = ["VGRD","UGRD"]
lvar   = ["TMP"]

#lplev  = [850, 500, 250]
lplev  = [500,250]

for year in lyear:
  for model in lmodel:
    for mon in lmon:
      for var in lvar:
        if var == "PRMSL":
          prog = "./grib2one.upscale.anl_p.sfc.py"
          scmd = "python %s %04d %02d %s %s"%(prog, year, mon, model, var)
          subprocess.call(scmd, shell=True)
        elif var in ["SPFH"]:
          for plev in [850]:
            prog = "./grib2one.upscale.atm.1layer.py"
            scmd = "python %s %04d %02d %s %s %s"%(prog, year, mon, model, var, plev)
            subprocess.call(scmd, shell=True)
        else:   
          for plev in lplev:
            prog = "./grib2one.upscale.atm.1layer.py"
            scmd = "python %s %04d %02d %s %s %s"%(prog, year, mon, model, var, plev)
            subprocess.call(scmd, shell=True)
    
  
