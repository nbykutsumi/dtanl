import os, sys
######################
#INPUT
######################
#
INPUTFILE=sys.argv[1]
CPTFILE=sys.argv[2]
PNGNAME=sys.argv[3]
PSFILE="%s.ps"%(PNGNAME[:-3])
PNGFILE=PNGNAME
TITLE=sys.argv[4]
SCALESTEP=float(sys.argv[5])
OVERSCALE=int(sys.argv[6])   # 1:"yes" or 0:"no"


#INPUTFILE   ="/media/disk2/out/CMIP5/6hr/NorESM1-M/historical/r1i1p1/tracks/map/track.grid_DJF_6hr_NorESM1-M_historical_r1i1p1.bn"
#CPTFILE     ='/home/utsumi/bin/dtanl/ctrack/oekaki/cpt/polar.-0.2.0.2.cpt'
#PNGNAME     ='/media/disk2/out/CMIP5/6hr/NorESM1-M/historical/r1i1p1/tracks/map/track.grid_DJF_6hr_NorESM1-M_historical_r1i1p1.png'
##PSFILE     =${OUTNAME}.ps
#PSFILE      ="%s[:-3].ps"%(PNGNAME)
##PNGFILE    =${OUTNAME}.png
#PNGFILE     =PNGNAME
#TITLE       ="AAAAAA"
#SCALESTEP   =0.5
#OVERSCALE   =0   # 1:"yes" or 0:"no"


#
##################################################
# make .xyz file
##################################################
#
#./bn2xyz.out $INPUTFILE > xyztemp.xyz
#/home/utsumi/oekaki/dtanl/cmip/bn2xyz.out $INPUTFILE > xyztemp.xyz
#os.system("./bn2xyz.out %s > xyztemp.xyz"%(INPUTFILE))
os.system("/home/utsumi/bin/dtanl/ctrack/oekaki/bn2xyz.out %s > xyztemp.xyz"%(INPUTFILE))
#
############################################################
# Define File Names
############################################################
DATFILE="./xyztemp.xyz"
#PSFILE="./image.ps"       #image file (output)
GRDFILE="./grd"           #temporary file
#CPTFILE="./grad.cpt"      #color paltette table file
#
############################################################
# Define Mapping Area
############################################################
XMIN=0.00               #Horizontal minimum [degree]
XMAX=360.00             #Horizontal maximum [degree]
#XMIN=-180               #Horizontal minimum [degree]
#XMAX=180.00             #Horizontal maximum [degree]
YMIN=-80.00             #Vertical minimum [degree]
YMAX=80.00              #Vertical maximum [degree]
XWID=21.0               #Width of image [cm]
YWID=10.5               #Height of image [cm]
DXa=90.0                #a:Horizontal Anotation Interval [degree]
DXf=30.0                #f:Horizontal Frame Interval [degree]
DXg=10.0                #G:Horizontal Grid Interval [degree]
DYa=30.0                #a:Vertical Anotation Interval [degree]
DYf=30.0                #f:Vertical Frame Interval [degree]
DYg=10.0                #g:Vertical Grid Interval [degree]
D=5.0                   #grid size
############################################################
# Short Cuts for Options
############################################################
#RFLAG="-R${XMIN}/${XMAX}/${YMIN}/${YMAX}"
RFLAG="-R%s/%s/%s/%s"%(XMIN, XMAX, YMIN, YMAX)
#JFLAG="-J$X${XWID}d/${YWID}d"
JFLAG="-JX%sd/%sd"%(XWID, YWID)
#BFLAG="-Ba${DXa}f${DXf}g${DXg}:Longitude:/a${DYa}f${DYf}g${DYg}:Latitude:neWS"
BFLAG="-Ba%sf%sg%s:Longitude:/a%sf%sg%s:Latitude:neWS"%(DXa, DXf, DXg, DYa, DYf, DYg)
############################################################
# Overscales  (sidebar)
############################################################
if OVERSCALE == 0:
  EFLAG=""
elif OVERSCALE == 1:
  EFLAG="-E0.6"
else:
  print "error!  OVERSCALE=", OVERSCALE
  print "EFLAG=", EFLAG
  sys.exit()
############################################################
#---Jobs
############################################################
#awk '($2==1){print $4, $3, $5}' $DATAFILE | \
#xyz2grd     $RFLAG -G$GRDFILE -I${D}/${D} -F
#xyz2grd     $RFLAG -G$GRDFILE -I${D}/${D} -F $DATFILE

#os.system("xyz2grd    -fg $RFLAG -G$GRDFILE -I2.5/1.895 $DATFILE")
os.system("xyz2grd    -fg %s -G%s -I2.5/1.895 %s"%(RFLAG, GRDFILE, DATFILE))

#psbasemap   $RFLAG $JFLAG $BFLAG -X3.5 -Y4.0         -K  > $PSFILE
os.system("psbasemap   %s %s %s -X3.5 -Y4.0         -K  > %s"%(RFLAG, JFLAG, BFLAG, PSFILE))

#grdimage -O $RFLAG $JFLAG $GRDFILE -C$CPTFILE        -K >> $PSFILE
os.system("grdimage -O %s %s %s -C%s        -K >> %s"%(RFLAG, JFLAG, GRDFILE, CPTFILE, PSFILE))

#pscoast  -O $RFLAG $JFLAG -Dc -W5 -N1 -I1      -K >> $PSFILE
os.system("pscoast  -O %s %s -Dc -W5 -N1 -I1      -K >> %s"%(RFLAG, JFLAG, PSFILE))

#psscale  -O -C$CPTFILE -D11.0/-1.5/17/0.5h $EFLAG -B$SCALESTEP    -K >> $PSFILE
os.system("psscale  -O -C%s -D11.0/-1.5/17/0.5h %s -B%s    -K >> %s"%(CPTFILE, EFLAG, SCALESTEP, PSFILE))

#pstext   -O $RFLAG $JFLAG -N                     << EOF >> $PSFILE
#0 100 24 0.0 1 6 $TITLE
#EOF

#os.system("pstext   -O %s %s -N                     << EOF >> %s\
#\0 100 24 0.0 1 6 %s\
#\EOF"%(RFLAG, JFLAG, PSFILE))

############################################################
# ps2png
############################################################
#convert -density 150 -rotate +90 -trim $PSFILE $PNGFILE
os.system("convert -density 150 -rotate +90 -trim %s %s"%(PSFILE, PNGFILE))

#rm -f $PSFILE
os.system("rm -f %s"%(PSFILE))


############################################################
# Comments for Options
############################################################
#-R: Option specifies region of interest
#-J: Option for mapping projection (JX: projection type)
#-B: Option for frame
#-O: Option for "Omit Header" i.e. following GMT command
#-K: Option for "Omit Trailer" i.e. GMT commands follow on
#
#--psbasemap
#
#draw basemap
#-X: Shift plot origin x-direction [cm]
#-Y: Shift plot origin y-direction [cm]
#
#--xyz2grd
#
#convert ASCII-xyz-data into binary-grid-data
#
#--gridimage
#
#conert binary-grid-data into colored mosaic image
