export TZ="CET"
export LC_ALL="de_DE.UTF-8"
BASEDIR=/opt/klima
GRAPHDIR=$BASEDIR/graphics
DATADIR=$BASEDIR/data
FILENAME=$GRAPHDIR/temp$1.png

rrdtool graph $FILENAME -w 800 -h 300 -D -l 0 -u 30 -s "-$1" \
-P \
--title "Temperatur" \
--vertical-label "T [°C]" \
--right-axis-label "T [°C]" \
--right-axis 1.0:0 \
DEF:Taussen=$DATADIR/aussen.rrd:T:AVERAGE \
DEF:Tkeller=$DATADIR/keller.rrd:T:AVERAGE \
DEF:DPaussen=$DATADIR/aussen.rrd:DP:AVERAGE \
DEF:DPkeller=$DATADIR/keller.rrd:DP:AVERAGE \
DEF:DWD=$GRAPHDIR/dwd.rrd:T:AVERAGE \
DEF:on=$DATADIR/fan.rrd:on:AVERAGE \
CDEF:Fan=on,Tkeller,* \
AREA:Fan#00ff0080: \
LINE2:Taussen#000000:Aussen \
LINE2:DWD#80808080:"DWD Westend" \
LINE2:Tkeller#ff0000:Keller \
LINE2:DPaussen#0000ff:"Taupunkt aussen" \
LINE2:DPkeller#ff00ff:"Taupunkt Keller" \
TICK:Fan#00ff0080:0.0:"Lüfter an"
