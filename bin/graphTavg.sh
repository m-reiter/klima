export TZ="CET"
export LC_ALL="de_DE.UTF-8"
BASEDIR=/opt/klima
GRAPHDIR=$BASEDIR/graphics
DATADIR=$BASEDIR/data
FILENAME=$GRAPHDIR/temp$1_$2.png

rrdtool graph $FILENAME -w 800 -h 300 -D -l 0 -s "-$1" -S $2 \
-P \
--slope-mode \
--title "Temperatur" \
--vertical-label "T [°C]" \
--right-axis-label "T [°C]" \
--right-axis 1.0:0 \
DEF:aussen=$DATADIR/aussen.rrd:T:AVERAGE \
DEF:aussenMIN=$DATADIR/aussen.rrd:T:MIN \
DEF:aussenMAX=$DATADIR/aussen.rrd:T:MAX \
CDEF:aussenDIFF=aussenMAX,aussenMIN,- \
DEF:keller=$DATADIR/keller.rrd:T:AVERAGE \
DEF:kellerMIN=$DATADIR/keller.rrd:T:MIN \
DEF:kellerMAX=$DATADIR/keller.rrd:T:MAX \
CDEF:kellerDIFF=kellerMAX,kellerMIN,- \
DEF:TPkeller=$DATADIR/keller.rrd:DP:AVERAGE \
DEF:TPkellerMIN=$DATADIR/keller.rrd:DP:MIN \
DEF:TPkellerMAX=$DATADIR/keller.rrd:DP:MAX \
CDEF:TPkellerDIFF=TPkellerMAX,TPkellerMIN,- \
DEF:On=$DATADIR/fan.rrd:on:AVERAGE \
CDEF:Fan=On,100,* \
LINE0:aussenMIN#00000000: \
AREA:aussenDIFF#00000030::STACK \
LINE0:kellerMIN#00000000: \
AREA:kellerDIFF#ff000050::STACK \
LINE0:TPkellerMIN#00000000: \
AREA:TPkellerDIFF#ff00ff50::STACK \
LINE2:aussen#000000:"Aussen" \
LINE2:keller#ff0000:"Keller" \
LINE2:TPkeller#ff00ff:"Taupunkt Keller"
# LINE2:Fan#00ff00:"Lüfter an"
