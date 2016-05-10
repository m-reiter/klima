#!/bin/sh
BASEDIR=/opt/klima
BINDIR=$BASEDIR/bin
GRAPHDIR=$BASEDIR/graphics

for d in 24h 1w 1M
do
  $BINDIR/graphTemp.sh $d
  $BINDIR/graphRH.sh $d
done

$BINDIR/getvalues.py > $GRAPHDIR/sidebar_neu.html
/usr/bin/install $GRAPHDIR/sidebar_neu.html $GRAPHDIR/sidebar.html
/bin/rm $GRAPHDIR/sidebar_neu.html

$BINDIR/graphSmall.sh
