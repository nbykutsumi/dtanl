'open /media/disk2/data/MERRA/bn/const/merra.2D.Nx.ctl'
'open /media/disk2/data/MERRA/bn/const/merra.2D.Cx.ctl'

'set dfile 1'
'set x 1 540'
'set y 1 361'
'set t 1'
*
'set dfile 2'
'set x 1 288'
'set y 1 144'
'set t 1'
*
'var= lterp(var.1, var.2)'
*'set fwrite -le out.bn'
*'set gxout fwrite'
'd var'
*'disable fwrite'
*'quit'
