#!/usr/bin/env python

import sys

RED="/sys/class/leds/led1/"
GREEN="/sys/class/leds/led0/"

def canswitch(colour):
  with open(colour+"trigger","r") as trigger:
    return trigger.read().find("[none]") != -1

def green():

  if canswitch(RED):
    with open(RED+"brightness","w") as red:
      red.write("0")
  if canswitch(GREEN):
    with open(GREEN+"brightness","w") as green:
      green.write("1")
    
def red():

  if canswitch(RED):
    with open(RED+"brightness","w") as red:
      red.write("1")
  if canswitch(GREEN):
    with open(GREEN+"brightness","w") as green:
      green.write("2")

if sys.argv[0] == "green":
  green()
if sys.argv[0] == "red":
  red()
