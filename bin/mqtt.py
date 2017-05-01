#!/usr/bin/python -u
# coding: utf-8
""" Messwerte von Homegear per MQTT abonnieren und in RRDs für einzelne Zimmer
    schreiben
"""

use_mqtt = False

if use_mqtt:
  import paho.mqtt.publish as mqtt

mqtt_host = "hive"
tempsubject = "haus/%s/temperature"
dpsubject = "haus/%s/dewpoint"
humsubject = "haus/%s/humidity"
ahsubject = "haus/%s/absolute_humidity"
fansubject = "haus/keller/fan"

def publishTH(room,T,DP,RH,AH):

  if not use_mqtt:
    return True

  mqtt.multiple([(tempsubject % room, str(T), 2, True),
                  (dpsubject % room, str(DP), 2, True),
                  (humsubject % room, str(RH), 2, True),
                  (ahsubject % room, str(AH), 2, True)],
                  hostname=mqtt_host)

def publishFan(Fan):

  if not use_mqtt:
    return True

  mqtt.single(fansubject, payload=str(Fan), qos=2, retain=True, hostname=mqtt_host)
