export TZ="CET"
export LC_ALL="de_DE.UTF-8"
BASEDIR=/opt/klima
GRAPHDIR=$BASEDIR/graphics
DATADIR=$BASEDIR/data
FILENAME=$GRAPHDIR/rh$1_$2.png

rrdtool graph $FILENAME -w 800 -h 300 -D -l 0 -s "-$1" -S $2 \
-P \
--slope-mode \
--title "Feuchte" \
--vertical-label "Rel. Feuchte / Laufzeit [%]" \
--right-axis-label "Abs. Feuchte [g/m<sup>3</sup>]" \
--right-axis 0.2:0 \
--right-axis-format %2.1lf \
DEF:aussen=$DATADIR/aussen.rrd:RH:AVERAGE \
DEF:keller=$DATADIR/keller.rrd:RH:AVERAGE \
DEF:kellerMIN=$DATADIR/keller.rrd:RH:MIN \
DEF:kellerMAX=$DATADIR/keller.rrd:RH:MAX \
CDEF:kellerDIFF=kellerMAX,kellerMIN,- \
DEF:AHaussen=$DATADIR/aussen.rrd:AH:AVERAGE \
DEF:AHaussenMIN=$DATADIR/aussen.rrd:AH:MIN \
CDEF:AHPaussenMIN=AHaussenMIN,.2,/ \
DEF:AHaussenMAX=$DATADIR/aussen.rrd:AH:MAX \
CDEF:AHaussenDIFF=AHaussenMAX,AHaussenMIN,-,.2,/ \
DEF:AHkeller=$DATADIR/keller.rrd:AH:AVERAGE \
DEF:AHkellerMIN=$DATADIR/keller.rrd:AH:MIN \
CDEF:AHPkellerMIN=AHkellerMIN,.2,/ \
DEF:AHkellerMAX=$DATADIR/keller.rrd:AH:MAX \
CDEF:AHkellerDIFF=AHkellerMAX,AHkellerMIN,-,.2,/ \
DEF:On=$DATADIR/fan.rrd:on:AVERAGE \
CDEF:Fan=On,100,* \
CDEF:AHPaussen=AHaussen,.2,/ \
CDEF:AHPkeller=AHkeller,.2,/ \
AREA:Fan#00ff0080 \
LINE0:kellerMIN#00000000: \
AREA:kellerDIFF#ff000050::STACK \
LINE0:AHPkellerMIN#00000000: \
AREA:AHkellerDIFF#ff00ff50::STACK \
LINE0:AHPaussenMIN#00000000: \
AREA:AHaussenDIFF#0000ff50::STACK \
LINE2:keller#ff0000:"Rel. Feuchte Keller" \
LINE2:AHPaussen#0000ff:"Abs. Feuchte aussen" \
LINE2:AHPkeller#ff00ff:"Abs. Feuchte Keller" \
TICK:Fan#00ff0080:0.0:"Lüfter"
