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
BINDIR=BASEDIR+'/bin'
LOCKFILE=BASEDIR+'/fanctl.lock'

DRYRUN = False

FANINPORT = "1"
FANOUTPORT = "2"
SISPMCTL="/usr/bin/sispmctl"

# Parameter
AHmargin = 2.0		# Mindestdifferenz absolute Feuchte (zum Einschalten)
AHhysterese = 1.0       # Hysterese hierzu
DPmargin = 2.0		# Mindestdifferenz Taupunkt (zum Einschalten)
DPhysterese = 1.0       # Hysterese hierzu
Tkellermin = 10.0	# Mindesttemperatur Keller (zum Einschalten)
Tkellermax = 22.0	# Maximaltemperatur Keller (zum Einschalten)
Thysterese = 2.0

def usage():
  print """
Usage: fanctl.py <command> [<options>]

Available commands are:

   cron

      Checks current conditions and turns fan on or off automatically unless locked.

   on,off

      Turns fan on or off unless locked.

   lock <on|1|off|0> <duration>

      Turns fan on or off and locks fan state for <duration> minutes or indefinitely
      if <duration> is given as "inf".

   unlock

      Removes a previous lock. Fan will be automatically controlled by cron job.
"""
  return 2

def on(force=False):
  logging.debug("on called.")
  if islocked() and not force:
    logging.debug("Asked to swich fan on, but fan is locked")
    rrdtool.update(DATADIR+'/fan.rrd','N:'+getvalues.getValues()['Fan'])
  else:
    if not DRYRUN:
      subprocess.call([SISPMCTL,"-o "+FANINPORT])
      subprocess.call([SISPMCTL,"-A",FANOUTPORT,"--Aafter","2","--Ado","on"])
    if getvalues.getValues()['Fan'] == "0":
      logging.info("switched fan on.")
    rrdtool.update(DATADIR+'/fan.rrd','N:1')

def off(force=False):
  logging.debug("off called.")
  if islocked() and not force:
    logging.debug("Asked to swich fan off, but fan is locked")
    rrdtool.update(DATADIR+'/fan.rrd','N:'+getvalues.getValues()['Fan'])
  else:
    if not DRYRUN:
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
      margin = AHmargin - AHhysterese
    if AHaussen > AHkeller - margin:
      logging.debug("abs. hum. outside is larger, switching fan off")
      off()
    else:
      logging.debug("abs. hum. outside is smaller, considering further...")
      Tkeller = float(currentState["Tkeller"])
      DPkeller = float(currentState["DPkeller"])
      Taussen = float(currentState["Taussen"])
      if Taussen > Tkeller:
        if Fan == "0":
          margin = 0.0
        else:
          margin = Thysterese
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
          marginT = Thysterese
          marginDP = DPmargin - DPhysterese
        if ( Tkeller > Tkellermin -marginT ) and ( Tkeller > DPkeller + marginDP ):
          logging.debug("temp. outside is lower but cellar is warm enough and well above dew point, switching fan on.")
          on()
        else:
          logging.debug("temp. outside is lower and cellar is too cold or too close to dew point, switching fan off.")
          off()
  subprocess.call(BINDIR+'/makegraphs.sh')

def lock(state,duration):
  if duration == "inf":
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
  f.close()
  currentState = getvalues.getValues()['Fan']
  if str(state) == currentState:
    logging.debug("lock: Fan is already in state %s, not switching" % state)
  else:
    logging.debug("lock: Switching fan to state %s" % state)
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
    f.close()
    logging.debug("islocked read unlocktime %s" % unlocktime)
    if ( unlocktime == "inf" ):
      return "inf"
    elif ( int(unlocktime) > int(time.time()) ):
      return ( int(unlocktime) - int(time.time()) )
    else:
      unlock()
  return False

def main(argv=None):
  if argv is None:
    argv = sys.argv
  logging.debug("fanctl called with args %s" % argv[1:])
  if len(argv) == 1:
    return usage()
  if argv[1] == "cron" and len(argv) == 2:
    cron()
  elif argv[1] == "on" and len(argv) == 2:
    on()
  elif argv[1] == "off" and len(argv) == 2:
    off()
  elif argv[1] == "lock" and len(argv) == 4:
    state = argv[2]
    if state == "on" or state == "1":
      state = 1
    elif state == "off" or state == "0":
      state = 0
    else:
      return usage() 
    duration = argv[3]
    if not duration == "inf":
      try:
        int(duration)
      except ValueError:
        return usage()
    lock(state,duration)
  elif argv[1] == "unlock" and len(argv) == 2:
    unlock()
  else:
    return usage()

if __name__ == "__main__":
  logging.basicConfig(filename=LOGDIR+'/fanctl.log',
                      format='%(asctime)s %(levelname)s: %(message)s',
                      level=logging.DEBUG)
  sys.exit(main())
