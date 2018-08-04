#!/bin/sh
rrdtool create $1.rrd --step 180 \
DS:T:GAUGE:360:-30:70 \
DS:RH:GAUGE:360:0:100 \
DS:AH:GAUGE:360:0:100 \
DS:DP:GAUGE:360:-70:70 \
DS:FENSTER:GAUGE:360:0:1 \
DS:HEIZUNG:GAUGE:360:0:100 \
DS:Tsoll:GAUGE:360:4.5:31.5 \
RRA:AVERAGE:0.5:1:351360 \
RRA:AVERAGE:0.5:480:3660 \
RRA:MIN:0.5:480:3660 \
RRA:MAX:0.5:480:3660 \
RRA:AVERAGE:0.5:14880:240 \
RRA:MIN:0.5:14880:240 \
RRA:MAX:0.5:14880:240
