#!/usr/bin/env python
# coding: utf-8

""" Template file zur Erstellung einer neuen Hardwaresteuerung für die Lüfter.

    Eine Hardwaresteuerung muss die folgenden Methoden unterstützen:

    on():

      Schaltet die Lüfter an.

    off(force=False):

      Schaltet die Lüfter aus. Wenn force=True, sofort, ansonsten mit eventuellen Verzögerungen.

    supports_interval():

      Liefert True zurück, wenn die Hardwaresteuerung Intervalllüftung unterstützt, anderenfalls False.

    interval(IntervalOn,IntervalOff):

      Schaltet die Intervalllüftung ein. Hierbei läuft der Lüfter für IntervalOn Minuten und pausiert
      anschließend für IntervalOff Minuten.
"""

def on():

  pass

def off(force=False):

  pass

def supports_interval():

  return False

def interval(IntervalOn,IntervalOff):

  pass
