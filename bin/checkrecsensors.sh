#!/bin/sh
#
# Skript um zu Überprüfen, ob recsensors noch läuft, und es ggfs. neu zu starten

BASEDIR="/home/reiter/klima"
BINDIR="$BASEDIR/bin"
LOGDIR="$BASEDIR/log"

until $BINDIR/recsensors.py; do
  echo "$(date): recsensors.py mit Returncode $? beendet, wird neu gestartet" >> $LOGDIR/checkrecsensors.log
  sleep 1
done
