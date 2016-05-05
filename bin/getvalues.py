#!/usr/bin/env python
# coding: utf-8

""" Liest die letzten Werte aus der Datenbank und prüft sie auf Alter und Gültigkeit
"""

import rrdtool
import time

# directories
BASEDIR='/opt/klima'
LOGDIR=BASEDIR+'/log'
DATADIR=BASEDIR+'/data'

def getValues():
  now = int(time.time())
  kellerinfo = rrdtool.info(DATADIR+'/keller.rrd')
  ausseninfo = rrdtool.info(DATADIR+'/aussen.rrd')
  faninfo = rrdtool.info(DATADIR+'/fan.rrd')
  if ( now - kellerinfo["last_update"] > 180 ):
    Tkeller = "U"
    RHkeller = "U"
    DPkeller = "U"
    AHkeller = "U"
  else:
    Tkeller = kellerinfo["ds[T].last_ds"]
    RHkeller = kellerinfo["ds[RH].last_ds"]
    DPkeller = kellerinfo["ds[DP].last_ds"]
    AHkeller = kellerinfo["ds[AH].last_ds"]
  if ( now - ausseninfo["last_update"] > 180 ):
    Taussen = "U"
    RHaussen = "U"
    DPaussen = "U"
    AHaussen = "U"
  else:
    Taussen = ausseninfo["ds[T].last_ds"]
    RHaussen = ausseninfo["ds[RH].last_ds"]
    DPaussen = ausseninfo["ds[DP].last_ds"]
    AHaussen = ausseninfo["ds[AH].last_ds"]
  if ( now - faninfo["last_update"] > 240 ):
    Fan = "U"
  else:
    Fan = faninfo["ds[on].last_ds"]
  return {
    'last_keller' : kellerinfo["last_update"],
    'Tkeller' : Tkeller,
    'RHkeller' : RHkeller,
    'DPkeller' : DPkeller,
    'AHkeller' : AHkeller,
    'last_aussen' : ausseninfo["last_update"],
    'Taussen' : Taussen,
    'RHaussen' : RHaussen,
    'DPaussen' : DPaussen,
    'AHaussen' : AHaussen,
    'last_fan' : faninfo["last_update"],
    'Fan': Fan
  }

if __name__ == '__main__':
  print getValues()
