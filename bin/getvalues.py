#!/usr/bin/env python
# coding: utf-8

""" Liest die letzten Werte aus der Datenbank und prüft sie auf Alter und Gültigkeit
"""

import rrdtool
import time

# directories
BASEDIR='/opt/klima'
LOGDIR=BASEDIR+'/log'
DATADIR=BASEDIR+'/data'

def getValues():
  now = int(time.time())
  kellerinfo = rrdtool.info(DATADIR+'/keller.rrd')
  ausseninfo = rrdtool.info(DATADIR+'/aussen.rrd')
  faninfo = rrdtool.info(DATADIR+'/fan.rrd')
  if ( now - kellerinfo["last_update"] > 180 ):
    Tkeller = "U"
    RHkeller = "U"
    DPkeller = "U"
    AHkeller = "U"
  else:
    Tkeller = kellerinfo["ds[T].last_ds"]
    RHkeller = kellerinfo["ds[RH].last_ds"]
    DPkeller = kellerinfo["ds[DP].last_ds"]
    AHkeller = kellerinfo["ds[AH].last_ds"]
  if ( now - ausseninfo["last_update"] > 180 ):
    Taussen = "U"
    RHaussen = "U"
    DPaussen = "U"
    AHaussen = "U"
  else:
    Taussen = ausseninfo["ds[T].last_ds"]
    RHaussen = ausseninfo["ds[RH].last_ds"]
    DPaussen = ausseninfo["ds[DP].last_ds"]
    AHaussen = ausseninfo["ds[AH].last_ds"]
  if ( now - faninfo["last_update"] > 240 ):
    Fan = "U"
  else:
    Fan = faninfo["ds[on].last_ds"]
  return {
    'last_keller' : kellerinfo["last_update"],
    'Tkeller' : Tkeller,
    'RHkeller' : RHkeller,
    'DPkeller' : DPkeller,
    'AHkeller' : AHkeller,
    'last_aussen' : ausseninfo["last_update"],
    'Taussen' : Taussen,
    'RHaussen' : RHaussen,
    'DPaussen' : DPaussen,
    'AHaussen' : AHaussen,
    'last_fan' : faninfo["last_update"],
    'Fan': Fan
  }

if __name__ == '__main__':
  values = getValues()
  if values['Tkeller'] == 'U':
    Tkeller = '--'
    RHkeller = '--'
    DPkeller = '--'
    AHkeller = '--'
  else:
    Tkeller = "%.1f&deg;C" % float(values['Tkeller'])
    if float(values['RHkeller']) > 60.0:
      color = "red"
    else:
      color = "green"
    RHkeller = '<font color="%s">%.0f%%</font>' % ( color, float(values['RHkeller']) )
    DPkeller = "%.1f&deg;C" % float(values['DPkeller'])
    AHkeller = "%.1f g/m&sup3;" % float(values['AHkeller'])
  if values['Taussen'] == 'U':
    Taussen = '--'
    RHaussen = '--'
    DPaussen = '--'
    AHaussen = '--'
  else:
    Taussen = "%.1f&deg;C" % float(values['Taussen'])
    RHaussen = '%.0f%%' % float(values['RHaussen'])
    DPaussen = "%.1f&deg;C" % float(values['DPaussen'])
    AHaussen = "%.1f g/m&sup3;" % float(values['AHaussen'])
  if values['Fan'] == 'U':
    color = "white"
    textcolor = "black"
    Fan = '--'
  else:
    if float(values['Fan']) > .99:
      color="green"
      textcolor = "white"
      Fan = 'AN'
    else:
      color="red"
      textcolor = "white"
      Fan = 'AUS'
  print '''\
<link rel="stylesheet" href="../klima/sidebar.css">
<center>
<h3>Aktuelle Werte</h3>
<small>Zuletzt aktualisiert: %s</small>
</center>
<table align="center" textalign="bottom" width="100%%">
  <tr>
    <td>Keller:</td>
    <td></td>
    <td align="right">%s</td>
    <td></td>
    <td>RF</td>
    <td align="center">%s</td>
  </tr>
  <tr>
    <td></td>
    <td>TP</td>
    <td align="right">%s</td>
    <td></td>
    <td>AF</td>
    <td align="center">%s</td>
  </tr>
  <tr>
    <td>Aussen:</td>
    <td></td>
    <td align="right">%s</td>
    <td></td>
    <td>RF</td>
    <td align="center">%s</td>
  </tr>
  <tr>
    <td></td>
    <td>TP</td>
    <td align="right">%s</td>
    <td></td>
    <td>AF</td>
    <td align="center">%s</td>
  </tr>
  <tr>
    <td>L&uuml;fter:</td>
    <td colspan="5" , bgcolor="%s" align="center"><font color="%s">%s</font></td>
  </tr>
</table>
<hr>
<h3>Verlauf</h3>
<ul>
<li><a href="../klima/24h.html" target="_top">24 Stunden</a><br></li>
<li><a href="../klima/1w.html" target="_top">1 Woche</a></li>
<li><a href="../klima/1M.html" target="_top">1 Monat</a></li>
</ul>
<h3>Tagesmittel</h3>
<ul>
<li><a href="../klima/1Mavg.html" target="_top">1 Monat</a></li>
<li><a href="../klima/3Mavg.html" target="_top">3 Monate</a></li>
<li><a href="../klima/6Mavg.html" target="_top">6 Monate</a></li>
</ul>
<h3>Monatssmittel</h3>
<ul>
<li><a href="../klima/1Ymonthly.html" target="_top">1 Jahr</a></li>
<li><a href="../klima/2Ymonthly.html" target="_top">2 Jahre</a></li>
</ul>
<a href="../klima/control.php" target="_top"><h3>Steuerung</h3></a>
''' % ( time.strftime("%-d.%-m.%Y, %-H:%M"),
        Tkeller, RHkeller, DPkeller, AHkeller, Taussen, RHaussen, DPaussen, AHaussen, color, textcolor, Fan )
