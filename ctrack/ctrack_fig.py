import os, sys
from numpy import *
from mpl_toolkits.basemap import Basemap
import matplotlib
import matplotlib.pyplot as plt
from cf.plot import *
#####################################################
def mk_pict_saone_reg(a2in, bnd=False, mycm="jet", soname="./temp.png", stitle=False, cbarname=False, miss=-9999.0, lllat=-89.5, lllon=0.5, urlat=89.5, urlon=359.5, a2shade=False, coef=1.0, lonlatfontsize=10.0, lonrotation=90):
  #-- prep ----------------
  plt.clf()
  dlat    = 1.0
  dlon    = 1.0
  a1lat   = arange(-89.5, 89.5  + dlat*0.1, dlat)
  a1lon   = arange(0.5,   359.5 + dlon*0.1, dlon)
  #-- 
  xdom_saone_first = int((lllon - 0.5 + 0.5)/1.0)
  xdom_saone_last  = int((urlon - 0.5 + 0.5)/1.0)
  ydom_saone_first = int((lllat -(-89.5) + 0.5)/1.0)
  ydom_saone_last  = int((urlat -(-89.5) + 0.5)/1.0)
  print lllat, urlat
  print ydom_saone_first,ydom_saone_last , xdom_saone_first,xdom_saone_last
  #------------------------
  # coef
  #------------------------
  a2in = (ma.masked_equal(a2in, miss)*coef)

  #------------------------
  # Basemap
  #------------------------
  print "Basemap"
  figmap   = plt.figure()
  #-------
  if lonlatfontsize >=20.0:
    axmap    = figmap.add_axes([0.15, 0.0, 0.8, 1.0])
  else:
    axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
  #-------
  M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)

  #-- transform -----------
  print "transform"
  #a2value_trans    = M.transform_scalar( a2in,   a1lon, a1lat, nnx, nny)
  #a2value_trans    = a2value_trans.filled(miss)

  a2value_trans  = a2in[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]

  #-- boundaries ----------
  if (type(bnd) != bool):
    bnd_cbar   = [-1.0e+40] + bnd + [1.0e+40]

  #-- color ---------------
  if (type(bnd) != bool):
    cminst   = matplotlib.cm.get_cmap(mycm, len(bnd))
    acm      = cminst( arange( len(bnd) ) )
    lcm      = [[1,1,1,1]]+ acm.tolist()
    mycm     = matplotlib.colors.ListedColormap( lcm )

  #-- imshow    -----------
  if (type(bnd) != bool):
    im       = M.imshow(a2value_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")
  else:
    print a2value_trans
    im       = M.imshow(a2value_trans, origin="lower", interpolation="nearest")

  #-- colorbar for self -
  if cbarname == "self":
    plt.colorbar(im)

  #-- shade     -----------
  if type(a2shade) != bool:
    a2shade_trans = a2shade[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]
    a2shade_trans = ma.masked_not_equal(a2shade_trans, miss)
    cmshade       = matplotlib.colors.ListedColormap([(0.8,0.8,0.8), (0.8,0.8,0.8)])
    im            = M.imshow(a2shade_trans, origin="lower", cmap=cmshade, interpolation="nearest")
    
  #-- coastline ---------------
  print "coastlines"
  M.drawcoastlines()

  #-- meridians and parallels
  parallels = arange(-90.,90,10.)
  M.drawparallels(parallels,labels=[1,0,0,0],fontsize=lonlatfontsize)

  meridians = arange(0.,360.,10.)
  M.drawmeridians(meridians,labels=[0,0,0,1],fontsize=lonlatfontsize,rotation=lonrotation)

  #-- title -------------------
  if stitle != False:
    axmap.set_title("%s"%(stitle))

  #-- save --------------------
  plt.savefig(soname)

  # for colorbar ---
  if (type(cbarname) != bool)&(cbarname !="self"):
    plt.clf()
    figmap   = plt.figure()
    axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
    M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
    figcbar   = plt.figure(figsize=(5, 0.6))
    axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
    #----------
    if type(bnd) == bool:
      im       = M.imshow(a2in, origin="lower", cmap=mycm)
      plt.colorbar(im, extend="both", cax=axcbar, orientation="horizontal")
    else:
      im       = M.imshow(a2in, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm)
      bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
      plt.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar, orientation="horizontal")
    #----------
    figcbar.savefig(cbarname)

#********************************************************
def mk_pict_saone_reg_symm(a2in, bnd=False, mycm="jet", soname="./temp.png", stitle=False, cbarname=False, miss=-9999.0, lllat=-89.5, lllon=0.5, urlat=89.5, urlon=359.5, a2shade=False, coef=1.0, lonlatfontsize=10.0, lonrotation=90):
  #-- prep ----------------
  plt.clf()
  dlat    = 1.0
  dlon    = 1.0
  a1lat   = arange(-89.5, 89.5  + dlat*0.1, dlat)
  a1lon   = arange(0.5,   359.5 + dlon*0.1, dlon)
  #-- 
  xdom_saone_first = int((lllon - 0.5 + 0.5)/1.0)
  xdom_saone_last  = int((urlon - 0.5 + 0.5)/1.0)
  ydom_saone_first = int((lllat -(-89.5) + 0.5)/1.0)
  ydom_saone_last  = int((urlat -(-89.5) + 0.5)/1.0)
  print lllat, urlat
  print ydom_saone_first,ydom_saone_last , xdom_saone_first,xdom_saone_last
  #------------------------
  # coef
  #------------------------
  a2in = (ma.masked_equal(a2in, miss)*coef)

  #------------------------
  # Basemap
  #------------------------
  print "Basemap"
  figmap   = plt.figure()
  #----------
  if lonlatfontsize >=20.0:
    axmap    = figmap.add_axes([0.15, 0.0, 0.8, 1.0])
  else:
    axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
  #----------
  M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)

  #-- transform -----------
  print "transform"
  #a2value_trans    = M.transform_scalar( a2in,   a1lon, a1lat, nnx, nny)
  #a2value_trans    = a2value_trans.filled(miss)

  a2value_trans  = a2in[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]

  #-- color ---------------
  if (type(bnd) != bool):
    #-- for symm --
    cminst   = matplotlib.cm.get_cmap(mycm, len(bnd)+1)
    acm      = cminst( arange( len(bnd)+1 ) )
    #-- for  lowest white --
    #cminst   = matplotlib.cm.get_cmap(mycm, len(bnd)+1)
    #acm      = cminst( arange( len(bnd)+1 ) )

    lcm      = acm.tolist()
    mycm     = matplotlib.colors.ListedColormap( lcm )

  #-- imshow    -----------
  if (type(bnd) != bool):
    im       = M.imshow(a2value_trans, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm, interpolation="nearest")
  else:
    print a2value_trans
    im       = M.imshow(a2value_trans, origin="lower", interpolation="nearest")

  #-- colorbar for self -
  if cbarname == "self":
    plt.colorbar(im)

  #-- shade     -----------
  if type(a2shade) != bool:
    a2shade_trans = a2shade[ydom_saone_first:ydom_saone_last +1, xdom_saone_first:xdom_saone_last+1]
    a2shade_trans = ma.masked_not_equal(a2shade_trans, miss)
    cmshade       = matplotlib.colors.ListedColormap([(0.8,0.8,0.8), (0.8,0.8,0.8)])
    im            = M.imshow(a2shade_trans, origin="lower", cmap=cmshade, interpolation="nearest")
    
  #-- coastline ---------------
  print "coastlines"
  M.drawcoastlines()

  #-- meridians and parallels
  parallels = arange(-90.,90,10.)
  M.drawparallels(parallels,labels=[1,0,0,0],fontsize=lonlatfontsize)

  meridians = arange(0.,360.,10.)
  M.drawmeridians(meridians,labels=[0,0,0,1],fontsize=lonlatfontsize,rotation=lonrotation)

  #-- title -------------------
  if stitle != False:
    axmap.set_title("%s"%(stitle))

  #-- save --------------------
  plt.savefig(soname)

  # for colorbar ---
  if (type(cbarname) != bool)&(cbarname !="self"):
    plt.clf()
    figmap   = plt.figure()
    axmap    = figmap.add_axes([0.1, 0.0, 0.8, 1.0])
    M        = Basemap( resolution="l", llcrnrlat=lllat, llcrnrlon=lllon, urcrnrlat=urlat, urcrnrlon=urlon, ax=axmap)
    figcbar   = plt.figure(figsize=(5, 0.6))
    axcbar    = figcbar.add_axes([0, 0.4, 1.0, 0.6])
    #----------
    if type(bnd) == bool:
      im       = M.imshow(a2in, origin="lower", cmap=mycm)
      plt.colorbar(im, extend="both", cax=axcbar, orientation="horizontal")
    else:
      im       = M.imshow(a2in, origin="lower", norm=BoundaryNormSymm(bnd), cmap=mycm)
      bnd_cbar  = [-1.0e+40] + bnd + [1.0e+40]
      plt.colorbar(im, boundaries= bnd_cbar, extend="both", cax=axcbar, orientation="horizontal")
    #----------
    figcbar.savefig(cbarname)

#********************************************************

