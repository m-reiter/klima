export TZ="CET"
export LC_ALL="de_DE.UTF-8"
BASEDIR=/opt/klima
GRAPHDIR=$BASEDIR/graphics
DATADIR=$BASEDIR/data
FILENAME=$GRAPHDIR/rh_mqtt$1.png

rrdtool graph $FILENAME -w 800 -h 320 -D -s "-$1" \
-P \
-l 0 -u 100 -r \
--title "Feuchte" \
--vertical-label "Rel. Feuchte [%]" \
--right-axis-label "Abs. Feuchte [g/m<sup>3</sup>]" \
--right-axis 0.2:0 \
--right-axis-format %2.1lf \
DEF:aussen=$DATADIR/aussen.rrd:RH:AVERAGE \
DEF:schlafzimmer=$DATADIR/schlafzimmer.rrd:RH:AVERAGE \
DEF:AHaussen=$DATADIR/aussen.rrd:AH:AVERAGE \
DEF:AHschlafzimmer=$DATADIR/schlafzimmer.rrd:AH:AVERAGE \
DEF:HEIZUNGschlafzimmer=$DATADIR/schlafzimmer.rrd:HEIZUNG:AVERAGE \
CDEF:Hon=HEIZUNGschlafzimmer,0,GT,1,0,IF,60,/ \
VDEF:Heizzeit=Hon,TOTAL \
CDEF:AHPaussen=AHaussen,.2,/ \
CDEF:AHPschlafzimmer=AHschlafzimmer,.2,/ \
CDEF:TEN=10,aussen,POP \
AREA:TEN: \
AREA:TEN#00000010::STACK \
AREA:TEN::STACK \
AREA:TEN#00000010::STACK \
AREA:TEN::STACK \
AREA:TEN#00000010::STACK \
AREA:TEN::STACK \
AREA:TEN#00000010::STACK \
AREA:TEN::STACK \
AREA:TEN#00000010::STACK \
AREA:HEIZUNGschlafzimmer#ffb000b0: \
LINE2:schlafzimmer#ff0000:"Rel. Feuchte Schlafzimmer" \
GPRINT:schlafzimmer:LAST:"Aktuell\:%5.0lf%%" \
GPRINT:schlafzimmer:AVERAGE:"Durchschnitt\:%5.0lf%%" \
GPRINT:schlafzimmer:MIN:"Minimum\:%5.0lf%%" \
GPRINT:schlafzimmer:MAX:"Maximum\:%5.0lf%%" \
LINE2:aussen#000000:"Rel. Feuchte aussen      " \
GPRINT:aussen:LAST:"Aktuell\:%5.0lf%%" \
GPRINT:aussen:AVERAGE:"Durchschnitt\:%5.0lf%%" \
GPRINT:aussen:MIN:"Minimum\:%5.0lf%%" \
GPRINT:aussen:MAX:"Maximum\:%5.0lf%%" \
LINE2:AHPschlafzimmer#ff00ff:"Abs. Feuchte Schlafzimmer\g" \
LINE2:AHPaussen#0000ff:"Abs. Feuchte aussen      " \
TICK:HEIZUNGschlafzimmer#ffb000b0:0.0:"Heizung" \
GPRINT:HEIZUNGschlafzimmer:LAST:"Aktuell\:%5.0lf%%" \
GPRINT:Heizzeit:"Heizdauer\: %.0lf Minuten"
