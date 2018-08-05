#!/usr/bin/env python
# coding: utf-8

""" Dieses Skript soll die Lüftersteuerung übernehmen

es wird sowohl per crontab als auch aus anderen Skripten aufgerufen und
kann auch interaktiv gestartet werden.
"""

import subprocess

FANINPORT = "1"
FANOUTPORT = "2"
SISPMCTL="/usr/bin/sispmctl"

def on():
  subprocess.call([SISPMCTL,"-A "+FANINPORT])
  subprocess.call([SISPMCTL,"-o "+FANINPORT])
  subprocess.call([SISPMCTL,"-A",FANOUTPORT,"--Aafter","2","--Ado","on"])

def off(force=False):
  subprocess.call([SISPMCTL,"-A "+FANOUTPORT])
  subprocess.call([SISPMCTL,"-f "+FANOUTPORT])
  if force:
    subprocess.call([SISPMCTL,"-A "+FANINPORT])
    subprocess.call([SISPMCTL,"-f "+FANINPORT])
  else:
    subprocess.call([SISPMCTL,"-A",FANINPORT,"--Aafter","2","--Ado","off"])

def supports_interval():
  return True

def interval(IntervalOn,IntervalOff):
  subprocess.call([SISPMCTL,"-A "+FANINPORT])
  subprocess.call([SISPMCTL,"-o "+FANINPORT])
  subprocess.call([SISPMCTL,"-A",FANINPORT,"--Aafter",str(IntervalOn),"--Ado","off","--Aafter",str(IntervalOff),"--Ado","on","--Aloop",str(IntervalOn+IntervalOff)])
  subprocess.call([SISPMCTL,"-A",FANOUTPORT,"--Aafter","2","--Ado","on","--Aafter",str(IntervalOn-2),"--Ado","off","--Aloop",str(IntervalOn+IntervalOff)])
