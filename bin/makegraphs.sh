#!/bin/sh
BASEDIR=/opt/klima
BINDIR=$BASEDIR/bin
WEBDIR=$BASEDIR/web

for d in 24h 1w
do
  $BINDIR/graphTemp.sh $d
  $BINDIR/graphRH.sh $d
done

$BINDIR/getvalues.py > $WEBDIR/sidebar_neu.html
/usr/bin/install $WEBDIR/sidebar_neu.html $WEBDIR/sidebar.html
/bin/rm $WEBDIR/sidebar_neu.html
