#!/usr/bin/env python
# coding: utf-8
""" Absolute Feuchte und Taupunkt aus relativer Feuchte und Temperatur
berechnen.

Quelle fuer die Formeln: http://www.wetterochs.de/wetter/feuchte.html

Variablen:

r = relative Feuchte [%]
T = Temperatur in °C
TK = Temperatur in Kelvin
TD = Taupunkttemperatur in °C
DD = Dampfdruck in hPa
SDD = Sättigungsdamfdruck in hPa
AF = absolute Feuchte in g/m^3

"""

import math
import sys

# Parameter
a = [ 7.5, 7.6 ]
b = [ 237.3, 240.7 ] 	# Parametersaetze fuer T >= 0 und T < 0
Rstar = 8314.3	# universelle Gaskonstante in J(Kmol*K)
mw = 18.016	# Molekulargewicht des Wasserdampfes in kg/kmol
OffsetKelvin = 273.15

def TK(T):
  return T+OffsetKelvin

def SDD(T):	# Saettigungsdampfdruck
  if ( T >= 0 ):
    i=0
  else:
    i=1
  return 6.1078*math.pow(10,((a[i]*T)/(b[i]+T)))

def DD(r,T):	# Dampfdruck
  return r/100.0*SDD(T)

def TD(r,T):	# Taupunkt
  if ( r == 0.):
    return 'U'
  if ( T >= 0 ):
    i=0
  else:
    i=1
  v=math.log10(DD(r,T)/6.1078)
  return b[i]*v/(a[i]-v)

def AF(r,T):	# absolute Feuchte
  return 100000.0*mw/Rstar*DD(r,T)/TK(T)

if __name__ == '__main__':
  if len(sys.argv) == 3:
    T = float(sys.argv[1])
    r = float(sys.argv[2])
    print "T:  %7.2f °C" % T
    print "RH: %7.2f %%" % r
    print "TP: %7.2f °C" % TD(r,T)
    print "AF: %7.2f g/m^3" % AF(r,T)
