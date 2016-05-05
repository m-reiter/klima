#!/usr/bin/env python
# coding: utf-8

""" Dieses Skript soll die Lüftersteuerung übernehmen

es wird sowohl per crontab als auch aus anderen Skripten aufgerufen und
kann auch interaktiv gestartet werden.
"""

import getvalues
import rrdtool
import subprocess
import sys
import logging
import time
import os

# directories
BASEDIR='/opt/klima'
LOGDIR=BASEDIR+'/log'
DATADIR=BASEDIR+'/data'
LOCKFILE="/var/lock/fanctl.lock"

logging.basicConfig(filename=LOGDIR+'/fanctl.log',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.DEBUG)

FANINPORT = "1"
FANOUTPORT = "2"
SISPMCTL="/usr/bin/sispmctl"

# Parameter
AHmargin = 1.0		# Mindestdifferenz absolute Feuchte (zum Einschalten)
AHhysterese = 0.5       # Hysterese hierzu
DPmargin = 2.0		# Mindestdifferenz Taupunkt (zum Einschalten)
DPhysterese = 1.0       # Hysterese hierzu
Tkellermin = 10.0	# Mindesttemperatur Keller (zum Einschalten)
Tkellermax = 22.0	# Maximaltemperatur Keller (zum Einschalten)
Thysterese = 2.0

def on(force=False):
  if islocked() and not force:
    logging.debug("Asked to swich fan on, but fan is locked")
    rrdtool.update(DATADIR+'/fan.rrd','N:'+getvalues.getValues()['Fan'])
  else:
    subprocess.call([SISPMCTL,"-o "+FANINPORT])
    subprocess.call([SISPMCTL,"-A",FANOUTPORT,"--Aafter","2","--Ado","on"])
    if getvalues.getValues()['Fan'] == "0":
      logging.info("switched fan on.")
    rrdtool.update(DATADIR+'/fan.rrd','N:1')

def off(force=False):
  if islocked() and not force:
    logging.debug("Asked to swich fan off, but fan is locked")
    rrdtool.update(DATADIR+'/fan.rrd','N:'+getvalues.getValues()['Fan'])
  else:
    subprocess.call([SISPMCTL,"-f "+FANOUTPORT])
    if force:
      subprocess.call([SISPMCTL,"-f "+FANINPORT])
    else:
      subprocess.call([SISPMCTL,"-A",FANINPORT,"--Aafter","2","--Ado","off"])
    if getvalues.getValues()['Fan'] == "1":
      logging.info("switched fan off.")
    rrdtool.update(DATADIR+'/fan.rrd','N:0')

def cron():
  currentState = getvalues.getValues()
  Fan = currentState["Fan"]
  logging.debug("cron called. Current values are %s" % currentState)
  if "U" in currentState.itervalues():
    logging.info("cron: switching fan off due to invalid state (%s)" % currentState)
    off()
  else:
    AHkeller = float(currentState["AHkeller"])
    AHaussen = float(currentState["AHaussen"])
    if Fan == "0":
      margin = AHmargin
    else:
      margin = margin - AHhysterese
    if AHaussen > AHkeller - margin:
      logging.debug("abs. hum. outside is larger, switching fan off")
      off()
    else:
      logging.debug("abs. hum. outside is smaller, considering further...")
      Tkeller = float(currentState["Tkeller"])
      Taussen = float(currentState["Taussen"])
      if Taussen > Tkeller:
        if Fan == "0":
          margin = 0.0
        else:
          margin = Tmargin
        if Tkeller < Tkellermax + margin: 
          logging.debug("temp. outside is higher and cellar is not too warm, switching fan on.")
          on()
        else:
          logging.debug("temp. outside is higher but cellar is too warm, switching fan off.")
          off()
      else:
        if Fan == "0":
          marginT = 0.0
          marginDP = DPmargin
        else:
          marginT = Tmargin
          marginDP = DPmargin - DPhysterese
        if ( Tkeller > Tkellermin -marginT ) and ( Tkeller > DPkeller + marginDP ):
          logging.debug("temp. outside is lower but cellar is warm enough and well above dew point, switching fan on.")
          on()
        else:
          logging.debug("temp. outside is lower and cellar is too cold or too close to dew point, switching fan off.")
          off()

def lock(state,duration):
  if duration is "inf":
    unlocktime = "inf"
  else:
    try:
      unlocktime = int(duration)
      unlocktime = int(time.time())+unlocktime*60
    except:
      logging.error("Ungültige Angabe für Sperrdauer: %s" % duration)
      return False
  logging.info("Locking fan to %s for %s minutes" % ( state, duration ))
  f = open(LOCKFILE,'w')
  f.write(str(unlocktime))
  currentState = getvalues.getValues()['Fan']
  if str(state) == currentState:
    logging.debug("lock: Fan is already in state %s, not switching" % state)
  else:
    logging.debug("lock: Switching fan to state %s")
    if state == 0:
      off(force=True)
    elif state == 1:
      on(force=True)

def unlock():
  if os.path.isfile(LOCKFILE):
    logging.info("Unlocking fan")
    os.remove(LOCKFILE)
  else:
    logging.debug("Unlock called, but no lock set")

def islocked():
  if os.path.isfile(LOCKFILE):
    f = open(LOCKFILE,'r')
    unlocktime = f.readline()
    if ( unlocktime == "inf" ) or ( int(unlocktime) > int(time.time()) ):
      return True
    else:
      unlock()
  return False

def main(argv=None):
  if argv is None:
    argv = sys.argv
  logging.debug("fanctl called with args %s" % argv[1:])
  cron()

if __name__ == "__main__":
  sys.exit(main())
