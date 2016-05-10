export TZ="CET"
export LC_ALL="de_DE.UTF-8"
BASEDIR=/opt/klima
GRAPHDIR=$BASEDIR/graphics
DATADIR=$BASEDIR/data
FILENAME=$GRAPHDIR/fan$1_$2.png

rrdtool graph $FILENAME -w 800 -h 300 -D -l 0 -u 100 -s "-$1" -S $2 \
-P \
--slope-mode \
--title "Lüfter" \
--vertical-label "Laufzeit [%]" \
--right-axis-label "Laufzeit [%]" \
--right-axis 1.0:0 \
DEF:On=$DATADIR/fan.rrd:on:AVERAGE \
CDEF:Fan=On,100,* \
AREA:Fan#00ff00:
