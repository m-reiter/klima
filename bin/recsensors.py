#!/usr/bin/python -u
# coding: utf-8
""" Einlesen der Temperaturdaten für Aussen und Keller,
    Berechnen der Werte für Absolute Feuchte und Taupunkt und
    Einspeichern in die RRDs
"""

import serial
import sys
import os
import rrdtool
import time
import feuchte
import logging
import mqtt

# directories
BASEDIR='/opt/klima'
LOGDIR=BASEDIR+'/log'
DATADIR=BASEDIR+'/data'

logging.basicConfig(filename=LOGDIR+'/recsensors.log',
                    format='%(asctime)s %(levelname)s: %(message)s',
                    level=logging.INFO)
# serial port of USB-WDE1
port = '/dev/ttyUSB0'

# MAIN
def main():
  logging.info('recsensors started')

  # open serial line
  ser = serial.Serial(port, 9600)
  if not ser.isOpen():
    logging.error("Unable to open serial port %s" % port)
    sys.exit(1)

  while(1==1):
    # read line from WDE1
    line = ser.readline()
    line = line.strip()
    data = line.split(';')
    if (len(data) == 25 and data[0] == '$1' and data[24] == '0'):
      for i, val in enumerate(data):
        data[i] = ('U' if val == '' else val.replace(',', '.'))
      Taussen = data[3]
      Tkeller = data[4]
      RHaussen = data[11]
      RHkeller = data[12]
      if ( Taussen == 'U' ) or (RHaussen == 'U'):
        logging.warn("Aussen: no valid sensor reading")
      else:
        AHaussen = str(feuchte.AF(float(RHaussen),float(Taussen)))
        DPaussen = str(feuchte.TD(float(RHaussen),float(Taussen)))
        logging.debug("Aussen: T %s°C, RH %s%%, AF %s g/m^3, TP %s°C" % ( Taussen,RHaussen,AHaussen,DPaussen ))
        rrdtool.update(DATADIR+'/aussen.rrd','N:'+Taussen+':'+RHaussen+':'+AHaussen+':'+DPaussen)
        mqtt.publishTH("aussen",Taussen,DPaussen,RHaussen,AHaussen)
      if ( Tkeller == 'U' ) or (RHkeller == 'U'):
        logging.warn("Keller: no valid sensor reading")
      else:
        AHkeller = str(feuchte.AF(float(RHkeller),float(Tkeller)))
        DPkeller = str(feuchte.TD(float(RHkeller),float(Tkeller)))
        logging.debug("Keller: T %s°C, RH %s%%, AF %s g/m^3, TP %s°C" % ( Tkeller,RHkeller,AHkeller,DPkeller ))
        rrdtool.update(DATADIR+'/keller.rrd','N:'+Tkeller+':'+RHkeller+':'+AHkeller+':'+DPkeller)
        mqtt.publishTH("keller",Tkeller,DPkeller,RHkeller,AHkeller)

if __name__ == '__main__':
  main()
