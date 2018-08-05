export TZ="CET"
export LC_ALL="de_DE.UTF-8"
BASEDIR=/opt/klima
GRAPHDIR=$BASEDIR/graphics
DATADIR=$BASEDIR/data
FILENAME=$GRAPHDIR/temp_mqtt$1.png

rrdtool graph $FILENAME -w 800 -h 320 -D -l 0 -u 30 -s "-$1" \
-P \
--title "Temperatur" \
--vertical-label "T [°C]" \
--right-axis-label "T [°C]" \
--right-axis 1.0:0 \
DEF:Taussen=$DATADIR/aussen.rrd:T:AVERAGE \
DEF:T=$DATADIR/schlafzimmer.rrd:T:AVERAGE \
DEF:DPaussen=$DATADIR/aussen.rrd:DP:AVERAGE \
DEF:DP=$DATADIR/schlafzimmer.rrd:DP:AVERAGE \
DEF:FENSTER=$DATADIR/schlafzimmer.rrd:FENSTER:AVERAGE \
DEF:Tsoll=$DATADIR/schlafzimmer.rrd:Tsoll:AVERAGE \
CDEF:F=FENSTER,0.5,GT,T,0.0,IF \
CDEF:MINUS=Taussen,NEGINF,MIN \
AREA:F#00ff0080: \
AREA:MINUS#0000ff10: \
LINE2:T#ff0000:"Schlafzimmer" \
GPRINT:T:LAST:"Aktuell\:%8.1lf°C" \
GPRINT:T:AVERAGE:"Durchschnitt\:%8.1lf°C" \
GPRINT:T:MIN:"Minimum\:%8.1lf°C" \
GPRINT:T:MAX:"Maximum\:%8.1lf°C" \
LINE2:Taussen#000000:"Aussen      " \
GPRINT:Taussen:LAST:"Aktuell\:%8.1lf°C" \
GPRINT:Taussen:AVERAGE:"Durchschnitt\:%8.1lf°C" \
GPRINT:Taussen:MIN:"Minimum\:%8.1lf°C" \
GPRINT:Taussen:MAX:"Maximum\:%8.1lf°C" \
LINE2:Tsoll#00c0c0:"Solltemperatur" \
LINE2:DPaussen#0000ff:"Taupunkt aussen" \
LINE2:DP#ff00ff:"Taupunkt Schlafzimmer" \
TICK:FENSTER#00ff0080:0.0:"Fenster auf"
