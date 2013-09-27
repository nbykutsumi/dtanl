from ctrack_fsub import *

lat_first = -89.5
dlon      = 1.0
dlat      = 1.0
radkm     = 300.0
miss_int  = -9999
ny,nx     = 180,360

lat = 24.5
a1,b1 = ctrack_fsub.circle_xy_real(lat, lat_first, dlon, dlat, radkm*1000.0, miss_int, nx, ny)


lat = 25.5
a2,b2 = ctrack_fsub.circle_xy_real(lat, lat_first, dlon, dlat, radkm*1000.0, miss_int, nx, ny)
