#!/bin/sh
START=$(( $(date -d$(head -1 /opt/klima/graphics/de-dwd-nkdz-req-TAUUHV.csv|cut -d, -f2) +%s) - 1 ))
rrdtool create /opt/klima/graphics/dwd.rrd --start $START --step 3600 \
DS:T:GAUGE:3600:-30:70 \
DS:RH:GAUGE:3600:0:100 \
RRA:AVERAGE:0.5:1:744
for t in $(cut -d"," -f2 /opt/klima/graphics/de-dwd-nkdz-req-TAUUHV.csv)
do
  tics=$(date -d "$t" +%s)
  values=$(grep $t /opt/klima/graphics/de-dwd-nkdz-req-TAUUHV.csv|cut -d"," -f4,7|sed -e "s/,/:/")
  rrdtool update /opt/klima/graphics/dwd.rrd "$tics:$values"
done
