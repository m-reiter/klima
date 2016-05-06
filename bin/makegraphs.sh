#!/bin/sh
BASEDIR=/opt/klima
BINDIR=$BASEDIR/bin

for d in 24h 1w
do
  $BINDIR/graphTemp.sh $d
  $BINDIR/graphRH.sh $d
done
