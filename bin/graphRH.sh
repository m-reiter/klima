export TZ="CET"
export LC_ALL="de_DE.UTF-8"
BASEDIR=/opt/klima
GRAPHDIR=$BASEDIR/graphics
DATADIR=$BASEDIR/data
FILENAME=$GRAPHDIR/temp$1.png

rrdtool graph $FILENAME -w 800 -h 400 -D -s "-$1" \
-P \
--title "Feuchte" \
--vertical-label "Rel. Feuchte [%]" \
--right-axis-label "Abs. Feuchte [g/m<sup>3</sup>]" \
--right-axis 0.15:0 \
--right-axis-format %2.1lf \
DEF:aussen=$DATADIR/aussen.rrd:RH:AVERAGE \
DEF:keller=$DATADIR/keller.rrd:RH:AVERAGE \
DEF:AHaussen=$DATADIR/aussen.rrd:AH:AVERAGE \
DEF:AHkeller=$DATADIR/keller.rrd:AH:AVERAGE \
DEF:on=$DATADIR/fan.rrd:on:AVERAGE \
CDEF:Fan=on,.9,GT,keller,0,IF \
CDEF:AHPaussen=AHaussen,.15,/ \
CDEF:AHPkeller=AHkeller,.15,/ \
AREA:Fan#00ff0080: \
LINE2:aussen#000000:"Rel. Feuchte aussen" \
LINE2:keller#ff0000:"Rel. Feuchte Keller" \
LINE2:AHPaussen#0000ff:"Abs. Feuchte aussen" \
LINE2:AHPkeller#ff00ff:"Abs. Feuchte Keller" \
TICK:Fan#00ff0080:0.0:"Lüfter an"
