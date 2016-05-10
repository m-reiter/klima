export TZ="CET"
export LC_ALL="de_DE.UTF-8"
BASEDIR=/opt/klima
DATADIR=$BASEDIR/data
GRAPHDIR=$BASEDIR/graphics

rrdtool graph $GRAPHDIR/rhsmall.png -w 320 -h 80 -D -s "-24h" \
-P \
DEF:keller=$DATADIR/keller.rrd:RH:AVERAGE \
DEF:on=$DATADIR/fan.rrd:on:AVERAGE \
CDEF:Fan=on,.9,GT,keller,0,IF \
AREA:Fan#00ff0080: \
LINE2:keller#ff0000:

rrdtool graph $GRAPHDIR/ahsmall.png -w 320 -h 80 -D -s "-24h" \
-P \
DEF:AHkeller=$DATADIR/keller.rrd:AH:AVERAGE \
DEF:AHaussen=$DATADIR/aussen.rrd:AH:AVERAGE \
DEF:on=$DATADIR/fan.rrd:on:AVERAGE \
CDEF:Fan=on,.9,GT,AHkeller,0,IF \
AREA:Fan#00ff0080: \
LINE2:AHkeller#ff00ff: \
LINE2:AHaussen#0000ff:
