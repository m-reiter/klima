#!/usr/bin/env python
# coding: utf-8

""" Hardwaresteuerung für die Lüfter per 433MHz Funksteckdose.

    Unterstützt *keine* Intervalllüftung
"""

import subprocess
import shlex

COMMAND = "/usr/local/bin/send"
ONARGS = "11001 2 1"
OFFARGS = "11001 2 0"

def on():

  subprocess.call(COMMAND+shlex.split(ONARGS))

def off(force=False):

  subprocess.call(COMMAND+shlex.split(OFFARGS))
  

def supports_interval():

  return False

def interval(IntervalOn,IntervalOff):

  pass
