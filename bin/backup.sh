#!/bin/sh
TODAY=$(date +"%Y%m%d")
BACKUPDIR=/platte/backups/keller
[ -d $BACKUPDIR ] && {
  cd /opt/klima
  tar -czf $BACKUPDIR/klimadata-$TODAY.tgz data/
}
