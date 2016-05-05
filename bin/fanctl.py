#!/usr/bin/env python
# coding: utf-8

""" Dieses Skript soll die Lüftersteuerung übernehmen

es wird sowohl per crontab als auch aus anderen Skripten aufgerufen und
kann auch interaktiv gestartet werden.
"""

import getvalues
import rrdtool
import subprocess

FANINPORT = "1"
FANOUTPORT = "2"
SISPMCTL="/usr/bin/sispmctl"

# Parameter
AHmargin = 2.0		# Mindestdifferenz absolute Feuchte
DPmargin = 2.0		# Mindestdifferenz Taupunkt
Tkellermin = 8.0	# Mindesttemperatur Keller
Tkellermax = 24.0	# Maximaltemperatur Keller

def on(force=False):
  subprocess.call([SISPMCTL,"-o "+FANINPORT])
  subprocess.call([SISPMCTL,"-A",FANOUTPORT,"--Aafter","2","--Ado","on"])

def off(force=False):
  subprocess.call([SISPMCTL,"-f "+FANOUTPORT])
  subprocess.call([SISPMCTL,"-A",FANINPORT,"--Aafter","2","--Ado","off"])

def cron():
  currentState = getvalues.getValues()
  if "U" in currentState.itervalues():
    off()
  else:
    AHkeller = float(currentState["AHkeller"])
    AHaussen = float(currentState["AHaussen"])
    if AHaussen > AHkeller - AHmargin:
      off()
    else:
      Tkeller = float(currentState["Tkeller"])
      Taussen = float(currentState["Taussen"])
      if Taussen > Tkeller:
        if Tkeller < Tkellermax:
          on()
        else:
          off()
      else:
        if ( Tkeller > Tkellermin ) and ( Tkeller > DPkeller - DPmargin ):
          on()
        else:
          off()
