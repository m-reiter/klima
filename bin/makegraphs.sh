#!/bin/sh
BASEDIR=/opt/klima
BINDIR=$BASEDIR/bin
GRAPHDIR=$BASEDIR/graphics

for d in 24h 1w 1M
do
  $BINDIR/graphTemp.sh $d
  $BINDIR/graphRH.sh $d
done

# Tagesdurchschnitte
for d in 1month 3months 6months
do
  $BINDIR/graphTavg.sh $d 86400
  $BINDIR/graphRHavg.sh $d 86400
  $BINDIR/graphFan.sh $d 86400
done

$BINDIR/getvalues.py > $GRAPHDIR/sidebar_neu.html
/usr/bin/install $GRAPHDIR/sidebar_neu.html $GRAPHDIR/sidebar.html
/bin/rm $GRAPHDIR/sidebar_neu.html

$BINDIR/graphSmall.sh
