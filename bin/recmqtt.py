#!/usr/bin/python -u
# coding: utf-8
""" Messwerte von Homegear per MQTT abonnieren und in RRDs für einzelne Zimmer
    schreiben
"""

import rrdtool
import feuchte
import paho.mqtt.client as mqtt
import datetime

mqtt_host = "hive"
subscription = "haus/schlafzimmer/#"
tempsubject = "haus/schlafzimmer/temperature"
humsubject = "haus/schlafzimmer/humidity"
windowsubject = "haus/schlafzimmer/balkontuer"
valvesubject = "haus/schlafzimmer/heizung"
Tsollsubject = "haus/schlafzimmer/desired-temp"
datadir = "/opt/klima/data/"

class Recorder:

    def __init__(self, name, wall_sensor_id, heater_id):
        self.name = name
        self.wall_sensor_id = wall_sensor_id
        self.heater_id = heater_id
        self.temperature = None
        self.humidity = None
        self.windowstate = "U"
        self.valvestate = "U"
        self.Tsoll = "U"

        client = mqtt.Client()
        client.on_connect = self.on_connect
        client.on_message = self.on_message

        client.message_callback_add(tempsubject, self.on_temperature)
        client.message_callback_add(humsubject, self.on_humidity)
        client.message_callback_add(windowsubject, self.on_window)
        client.message_callback_add(valvesubject, self.on_valve)
        client.message_callback_add(Tsollsubject, self.on_Tsoll)

        client.connect(mqtt_host, 1883, 60)

        client.loop_forever()

    def on_connect(self, client, userdata, flags, rc):
        print "Verbunden! RC: %s" % rc
        #client.subscribe(subscription % self.wall_sensor_id)
        #client.subscribe(subscription % self.heater_id)
        client.subscribe(subscription)

    def on_message(self, client, userdata, msg):
        print "%s: Message erhalten:" % datetime.datetime.now()
        print msg.topic
        print msg.payload

    def on_temperature(self, client, userdata, msg):
        print "Temperatur erhalten: %s" % msg.payload
        self.temperature = float(msg.payload)
        self.check_record()

    def on_humidity(self, client, userdata, msg):
        print "Feuchte erhalten: %s" % msg.payload
        self.humidity = float(msg.payload)
        self.check_record()

    def on_window(self, client, userdata, msg):
        print "Fensterstatus erhalten: %s" % msg.payload
        #self.windowstate = str(int(eval(msg.payload.capitalize())))
        self.windowstate = str(int(msg.payload.capitalize() == "Open"))

    def on_valve(self, client, userdata, msg):
        print "Ventilstatus erhalten: %s" % msg.payload
        self.valvestate = int(msg.payload)

    def on_Tsoll(self, client, userdata, msg):
        print "Sollwert T erhalten: %s" % msg.payload
        self.Tsoll = float(msg.payload)

    def check_record(self):
        print "Check called: %s" % (self.temperature and self.humidity)
        if self.temperature and self.humidity:
            print "Wertesatz erhalten: T %s RH %s %%" % (self.temperature, self.humidity)
            print "Fensterzustand: %s, Ventiloeffnung: %s " % (self.windowstate, self.valvestate)

            AH = str(feuchte.AF(self.humidity, self.temperature))
            DP = str(feuchte.TD(self.humidity, self.temperature))

            rrdtool.update(datadir+self.name.lower()+'.rrd','N:'+str(self.temperature)+':'+str(self.humidity)+':'+AH+':'+DP+":"+self.windowstate+":"+str(self.valvestate)+":"+str(self.Tsoll))

            self.temperature = None
            self.humidity = None

schlafzimmer = Recorder("Schlafzimmer", 1, 2)
