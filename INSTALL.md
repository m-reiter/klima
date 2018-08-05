Installationsanleitung
======================

Vorbemerkung
------------

Es freut mich, daß Du Dich für mein Projekt einer feuchtegesteuerten Kellerlüftung interessierst oder es gar nachbauen möchtest. Ich leiste dabei auch gerne Hilfe, kann aber selbstverständlich für nichts garantieren: Wenn Du das Projekt nicht zum Laufen kriegst, wenn es nichts bringt, wenn es Deinen Weinkeller plündert, Deine Katze ärgert oder Dein Haus beschädigt, übernehme ich keinerlei Verantwortung. Alles, was Du tust, geschieht auf eigene Gefahr. 

In diesem Sinne:

**Viel Erfolg!**

Diese Anleitung stammt ursprünglich vom Nutzer YoYo aus dem Deutschen Raspberry Pi Forum und basiert auf seinen Notizen bei der Installation seines eigenen Systems. Ich habe sie noch etwas überarbeitet und Markdown-Formatierungen eingebaut.

Funktionsprinzip
----------------

Grundprinzip des Systems ist der Vergleich der absoluten Luftfeuchte von Keller- und Außenluft. Dazu werden außen und innen die Temperatur sowie die relative Luftfeuchte (in %) gemessen und daraus die absolute Luftfeuchte (in Gramm Waser pro Kubikmeter Luft) berechnet. Ist die Außenluft absolut trockener als die Innenluft wird die Lüftung ein- anderenfalls wird sie ausgeschaltet.

Es werden noch ein paar zusätzliche Parameter berücksichtigt (Hysterese, Temperaturgrenzen, damit der Keller nicht zu sehr aufheizt oder auskühlt), die unter Konfiguration kurz erläutert werden, Hauptparameter ist aber die absolute Feuchte.

Zu dieser Anleitung
-------------------

Die einzugebenden Befehle sind in dieser Anleitung in Codeblöcken aufgeführt. Das sieht dann so aus:

    $ uname -a

Das Dollarzeichen ($) symbolisiert hierbei das Prompt und muss nicht mit eingetippt werden.

Einige Befehle benötigen root-Rechte. Diese sind am vorgestellten "sudo" erkennbar und müssen unter einem Nutzer ausgeführt werden, der die entsprechenden sudo-Rechte besitzt. In einer Standardinstallation von Raspbian ist das der Nutzer "pi". Alle anderen Befehle müssen unter dem Nutzer "klima" ausgeführt werden, der im Zuge dieser Anleitung erstellt wird. Vor dem Ausführen dieser Befehle musst Du Dich also unter dieser Kennung anmelden oder ein

    $ su - klima

ausführen.

Übersicht
---------

Das Projekt besteht im wesentlichen aus drei Komponenten:

- Herzstück ist das eigentliche System zum Erfassen und Speichern der Messwerte und zum Steuern der Lüfter. Dieses System hat keine Bedienoberfläche, kann ohne angeschlossenes Display laufen und lässt sich über die Kommandozeile steuern. Im Prinzip ist dafür auch keine Netzwerkanbindung notwendig - ohne eine solche hat man aber natürlich keine Möglichkeit der Fernüberwachung oder -steuerung.

Die weiteren Komponenten sind optional:

- controller\_v3.py ist eine kleine graphische Oberfläche, die den aktuellen Status anzeigt und ein manuelles Steuern der Lüfter erlaubt. Die Oberfläche ist für ein Touchdisplay mit 320x480 Pixeln optimiert und kann direkt am Pi vor Ort als Anzeige- und Steuermodul dienen. Sie lässt sich aber auch remote per ssh mit X11-Forwarding aufrufen.

- Das Kernsystem erzeugt HTML-Seiten und Verlaufsgraphiken, die man sich über einen optional zu installierenden Webserver anzeigen lassen kann. Die Graphiken sind hierbei ausführlicher als auf der kleinen GUI, die Steuerungsmöglichkeiten sind im wesentlichen die selben.

Stückliste
----------

Du brauchst:

- 1 Raspberry Pi  
  Ich verwende einen Pi 3. Da das Projekt keine besonderen Anforderungen an Rechenleistung oder Speicher stellt, sollte es aber auch jedes andere Modell tun. Wichtig ist nur, daß der Pi über mindestens 2 USB-Anschlüsse verfügt. Eine Möglichkeit, ihn an ein Netzwerk anzuschließen, sollte ebenfalls gegeben sein.

- 1 USB-Empfänger WDE1-2 (von ELV)

- 2 Funksensoren ASH 2200 (von ELV)

- 1 USB-Steckdosenleiste Energenie EG-PMS2  
  Das ist meine Lösung, um die Ventilatoren zu schalten. Theoretisch ließe sich das Projekt natürlich auch auf andere Schaltmöglichkeiten anpassen. Wenn Du Daran Interesse hast, kannst Du mich gerne kontaktieren, dann werde ich versuchen, die Hardwaresteuerung soweit auszukoppeln, daß man ein angepasstes Modul einbinden kann.
  
Optional noch

- 1 3,5"-Touchscreen (320x480) (mit Gehäuse)  
  Brauchst Du, wenn Du eine Bedien- und Anzeigemöglichkeit direkt am Installationsort haben möchtest. Ich verwende das Modell von Tontec, weil es bereits ein Gehäuse mitbringt. Außerdem hat mein Exemplar einen Schalter für die Hintergrundbeleuchtung. Damit kann ich das Screenblanking deaktivieren und den Bildschirm trotzdem nur beleuchten, wenn ich ihn benutze. *Achtung*: Ich habe auch Bilder des Tontec-Displays ohne Schalter gesehen, wenn Dir das wichtig ist, evtl. beim Verkäufer nachfragen.
  
Alternativ würde ich zur Anschaffung von

- 1 Gehäuse (ohne Display)

raten, unbedingt notwendig ist das aber natürlich nicht.

Voraussetzung
-------------

Ausgangspunkt dieser Anleitung ist ein fertig aufgesetzter, bootfähiger und ans Netzwerk angeschlossener Raspberry Pi mit einem aktuellen Raspbian Stretch.

Die Einrichtung kann entweder über lokal angeschlossenes Display, Maus und Tastatur oder übers Netz per ssh erfolgen. Ein unter Windows verfügbarer ssh-client ist bspw. putty.

Vorbereitung des Systems
------------------------

### System auf den neuesten Stand bringen und einige benötigte Pakete installieren

    $ sudo apt-get update
    $ sudo apt-get upgrade
    $ sudo apt-get install mercurial rrdtool python-rrdtool sispmctl socat

### Gruppen und Benutzer anlegen

    $ sudo addgroup usb
    $ sudo adduser klima
    $ sudo usermod -a -G dialout,usb klima

### SPI-Bus aktivieren

Dies kann über die GUI erfolgen:

- Menu/Einstellungen/Raspberry-PI-Konfiguration
- Reiter Schnittstellen, den entsprechenden Radio-Button aktivieren

oder über die Kommandozeile:

    $ sudo raspi-config

- Advanced Options/SPI/Enable

### Die Software herunterladen

Gehört zwar streng genommen nicht zur Systemvorbereitung, wird aber für den nächsten Schritt benötigt.

Erst das Verzeichnis anlegen

    $ sudo install -d -o klima -g klima /opt/klima

Anschließend als User klima:

    $ cd /opt
    $ hg clone https://m_reiter@bitbucket.org/m_reiter/klima

Lädt das komplette Repository ins Verzeichnis /opt/klima.

#### Exkurs: Update der Software

Wenn Du die Software wie eben beschrieben installiert hast, kannst Du wie folgt überprüfen, ob Updates zur Verfügung stehen:

    $ cd /opt/klima
    $ hg incoming

Sollten Dir Updates angezeigt werden, kannst Du sie, immer noch im selben Verzeichnis, installieren:

    $ hg pull
    $ hg update

### Gruppenschreibrechte für USB-devices einrichten (für die Steckdosenleiste)

Standardmäßig darf in Raspbian nur root auf USB-devices schreiben. Um übermäßigen Gebrauch von sudo zu vermeiden, habe ich eine udev-Regel angelegt, die der Gruppe usb ebenfalls Schreibrechte einräumt. Du kannst sie wie folgt installieren:

    $ sudo cp /opt/klima/misc/99-usbgroup.rules /etc/udev/rules.d/

Anschließend den Raspberry rebooten.

    $ ls -l /dev/bus/usb/001/

sollte dann zeigen, daß die USB-Geräte der Gruppe usb gehören und für diese schreibbar sind.

    $ ls -l /dev/bus/usb/001/
    insgesamt 0
    crw-rw-r-- 1 root usb 189, 0 Aug  2 14:02 001
    crw-rw-r-- 1 root usb 189, 1 Aug  2 14:02 002
    crw-rw-r-- 1 root usb 189, 2 Aug  2 14:02 003
    crw-rw-r-- 1 root usb 189, 3 Aug  2 14:02 004
    crw-rw-r-- 1 root usb 189, 4 Aug  2 14:02 005
    crw-rw-r-- 1 root usb 189, 5 Aug  2 14:02 006
    crw-rw-r-- 1 root usb 189, 6 Aug  2 14:02 007

Vorbereitung (Hardware)
-----------------------

### Funksensoren adressieren

Da 2 Funksensoren des Typs ASH 2200 bei der vorgestellten Lösung zum Einsatz kommen, muss einer der Funksensoren eine
neue Adresse bekommen. Siehe dazu auch die Installationsanleitung von ELV.

Hierzu einfach mit einem kleinen Schraubenzieher einen Sensor aufschrauben und den Jumper auf Position 1 entfernen.
Damit bekommt der Sensor der Adresse 2. Das war's schon. Sensor wieder zusammenschrauben.

Der neu adressierte Sensor wird der Innensensor, der Sensor mit der Originalkonfiguration entsprechend der Außensensor.

Batterien in die beiden Funksensoren ASH2200 einlegen.

### USB-Empfänger WDE1-2 mit Raspberry verbinden

Hierzu das der Lieferung beiliegende USB-Kabel mit dem laufenden Raspberry PI verbinden.
Der USB-Empfänger wird erkannt und ist nun über das Device File /dev/ttyUSB0 erreichbar.

### Überprüfung USB-Empfänger und Funksensoren

Test der Sensoren mittels folgenden Aufruf

    $ socat /dev/ttyUSB0,b9600 STDOUT     

Nach einiger Zeit (kleiner 2 Minuten) solltet Ihr folgende Ausgabe im Terminalfenster sehen

    $ socat /dev/ttyUSB0,b9600 STDOUT
    $1;1;;25,7;20,9;;;;;;;42;70;;;;;;;;;;;;0
    $1;1;;25,6;20,9;;;;;;;41;70;;;;;;;;;;;;0

Hurra, die beiden Sensoren sind eingebunden und laufen.
Sensor1: 25,7°C und relative Luftfeuchte von 42 %
Sensor2: 20,9°C und relative Luftfeuchte von 70 %

Konfiguration der Software
--------------------------

Folgende Unterverzeichnisse sind noch unter /opt/klima anzulegen

    $ cd /opt/klima
    $ mkdir log
    $ mkdir data
    $ mkdir graphics
    $ mkdir -p ftp/uploads        * Verzeichnis für Wetterdaten des deutschen Wetterdiensts

Da Graphiken und HTML-Schnipsel für das Webinterface alle drei Minuten erzeugt werden, realisieren wir das Verzeichnis `/opt/klima/graphics` als RAM-Disk, um übermäßigen Verschleiß der SD-Karte zu vermeiden. Du musst dafür als root die folgende Zeile in der Datei `/etc/fstab` eintragen:

    none           /opt/klima/graphics   tmpfs    defaults,noatime,uid=klima,gid=klima,size=10M  0       0

und anschließend ein

    $ sudo mount /opt/klima/graphics

ausführen.

Anlegen der Datenbanktabellen mittels rrdtool

    $ cd /opt/klima
    $ ./bin/makerrd.sh data/aussen
    $ ./bin/makerrd.sh data/keller
    $ ./bin/makefanrrd.sh

#### Anpassen der Parameter

Anschließend kannst Du in der Datei `/opt/klima/bin/fanctl.py` die Parameter der Lüftungssteuerung an Deine Bedürfnisse anpassen. Im einzelnen sind dies:

- AHmargin und AHhysterese

  Die Hauptparameter. Ist die absolute Außenfeuchte um mindestens AHmargin Gramm pro Kubikmeter niedriger als die Innenfeuchte, wird die Lüftung eingeschaltet. Läuft die Lüftung bereits, wird sie wieder ausgeschaltet, wenn die Differenz den Wert (AHmargin-Ahhysterese) unterschreitet.

- Tkellermin, Tkellermax und Thysterese

  Minimal- und Maximaltemperatur um übermäßiges Abkühlen oder Aufheizen des Kellers zu vermeiden. Liegt die Außentemperatur unter Tkellermin und unter der Innentemperatur, wird die Lüftung nur eingeschaltet, wenn die Innentemperatur um mindestens Thysterese °C über Tkellermin liegt. Beim Erreichen von Tkellermin wird die Lüftung dann abgeschaltet. Analog wird auch mit Tkellermax verfahren.

- DPmargin und DPhysterese

  Ein Sicherheitsparameter, den ich eingebaut habe: Liegt die Außen- unter der Innentemperatur, wird die Lüftung nur eingeschaltet, wenn die Innentemperatur um mindestens DPmargin °C über dem Taupunkt liegt. Unterschreitet die Differenz den Wert (DPmargin-DPhysterese), wird die Lüftung ausgeschaltet.

- UseInterval, LockInterval, IntervalOn, IntervalOff

  Auf Anregung aus dem Forum habe ich eine optionala Intervalllüftung realisiert: Wenn UseInterval auf "True" steht, bedeutet ein "Einschalten" der Lüftung, daß diese zyklisch immer erst IntervalOn Minuten läuft und dann IntervalOff Minuten steht, um der zugeführten Frischluft Gelegenheit zu geben, Feuchte aus dem Keller aufzunehmen. Falls LockInterval auf "True" steht, wird die Intervalllüftung auch angewendet, wenn die Lüftung von Hand, d.h. über das Webinterface oder den Touchscreen eingeschaltet wird. Zur Effizienz der Intervall- im Vergleich zur Dauerlüftung kann ich keine Aussagen machen, wäre aber an entsprechenden Erfahrungswerten interessiert.

  Noch eine Anmerkung hierzu: Naturgemäß kann es bei der Verwendung der Intervalllüftung dazu kommen, daß der Lüfter steht, obwohl im Webinterface bzw. auf dem Display angezeigt wird, daß er eingeschaltet ist. Ich würde daher empfehlen, anfangs die Intervalllüftung auszuschalten, bis Du Dir sicher bist, daß das System korrekt funktioniert.

#### Installation der systemd service unit zur Aufnahme der Sensorwerte

Zuerst musst Du ein Verzeichnis für systemd user service units anlegen:

    $ mkdir -p ~/.config/systemd/user

und anschließend die service unit dorthin kopieren:

    $ cp /opt/klima/misc/recsensors.service ~/.config/systemd/user/

Dann musst Du noch dem Nutzer klima erlauben, auch dann services laufen zu haben, wenn er nicht eingeloggt ist:

    $ sudo loginctl enable-linger klima

und die service unit aktivieren:

    $ systemctl --user enable recsensors

#### Einrichten des cronjobs und Start des Systems

Wenn Du jetzt mit den folgenden Befehlen den cronjob für den Nutzer klima einrichtest und anschließend den Raspberry Pi neu startest, sollte das System bereits laufen.

    $ crontab /opt/klima/misc/crontab
    $ sudo reboot

Um besser überprüfen zu können, was das System tut, solltest Du Dir aber noch mindestens eines der Interfaces (Webinterface, Touchscreen) installieren.

_Optional:_ Einrichten der Bedienoberfläche auf dem Touchscreen
---------------------------------------------------------------

Die eigentliche Installation des Touchscreens geht über den Umfang dieser Anleitung hinaus. Sie war aber nach der mitgelieferten Dokumentation nicht allzu kompliziert. Bei der Kalibrierung des Touchscreens fand ich die Hinweise in dieser [Amazon-Rezension von Dr. Ralf Korell](https://www.amazon.de/gp/customer-reviews/R1VUZL5TK86QAF/) sehr hilfreich.

Wenn das Display eingerichtet ist, muss der automatische Start der Bedienoberfläche eingerichtet werden. Hierzu gibt es verschieden Methoden, ich verwende dazu den extrem schlanken Displaymanager nodm, der eigens für solche Anwendungen gedacht ist.

Zunächst einmal muss über raspi-config eingestellt werden, daß der Pi ohne automatisches Login in die GUI bootet:

    $ sudo raspi-config

und dann "Boot options"->"Desktop GUI, requiring user to login" auswählen. Anschließend wird nodm installiert:

    $ sudo apt-get install nodm

Hierbei wird direkt die textbasierte Konfiguration von nodm aufgerufen. Bei den meisten Optionen kannst Du den Defaultwert wählen. Im einzelnen sind die folgenden Optionen (**fett**) zu wählen:

- Start nodm on boot? **Yes**
- User to start a session for: **klima**
- Lowest numbered vt on which X may start: **7**
- Options for the X server: **-nolisten tcp -nocursor**
- Minimum time (in seconds) for a session to be considered OK: **60**
- X session to use: **/etc/X11/Xsession**

Anschließend musst Du noch nodm als Default Display Manager eintragen:

    $ sudo sh -c "echo /usr/sbin/nodm > /etc/X11/default-display-manager"

und die xsession des Nutzers klima installieren:

    $ cp /opt/klima/misc/xsession ~/.xsession

Nach einem Neustart des Pi mittels

    $ sudo shutdown -r now

sollte die Bedienoberfläche jetzt automatisch starten. Evtl. dauert das eine Weile, nach spätestens fünf Minuten sollte die Oberfläche aber zu sehen sein.

_Optional:_ Installation des Webservers nginx
---------------------------------------------

### Paket installieren

    $ sudo apt-get install nginx apache2-utils

nginx sollte nun installiert sein.

### PHP installieren

    $ sudo apt-get install php7.0-fpm php7.0-cgi php7.0-cli php7.0-common

### Anpassen der nginx-Konfiguration für die Applikation Feuchtegesteuerte Kellerlüftung

Die Datei klima.nginx unter misc nach /etc/nginx/sites-available/klima kopieren

    $ sudo cp /opt/klima/misc/klima.nginx /etc/nginx/sites-available/klima

In dieser Datei ist dann noch der Text "<DYNAMIC DNS HOSTNAME>" durch Deinen extern erreichbaren Hostnamen zu ersetzen, falls Du auch aus dem Internet auf die Steuerung zugreifen möchtest. Anderenfalls kannst Du diesen Text ersatzlos streichen.

Alle Zeilen, die "ssl" enthalten, brauchst Du nur, wenn Du den Zugriff auf die Webseite per SSL absichern möchtest. Bei einem Zugriff aus dem Internet würde ich dazu auf jeden Fall raten, im lokalen Netz kannst Du eventuell auch darauf verzichten (und die Zeilen aus /etc/nginx/sites-available/klima löschen).

Symlink in /etc/nginx/sites-enabled/ setzen

    $ cd /etc/nginx/sites-enabled
    $ sudo ln -s /etc/nginx/sites-available/klima klima
    $ sudo rm default    
    
### SSL einrichten

Wenn Du einen Zugriff per SSL ermöglichen willst, kannst Du mit den folgenden Befehlen Zertifikate generieren:

    $ sudo mkdir /etc/nginx/ssl && cd /etc/nginx/ssl
    $ sudo openssl genrsa -out server.key 2048
    $ sudo openssl req -new -key server.key -out server.csr
    $ sudo openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

Es handelt sich hierbei um sogenannte selbst-signierte Zertifikate, Dein Browser wird sich beim ersten Zugriff also beschweren, daß er den Zertifikaten nicht vertraut. Hierzu musst Du dann im Browser eine Ausnahmeregel anlegen.

Alternativ kannst Du natürlich auch professionalle Zertifikate, beispielsweise von [https://letsencrypt.org/], verwenden.

### htpasswd für Zugriff über Web setzen

Anlegen des users, hier klima:
    
    $ sudo htpasswd -c /etc/nginx/htpasswd klima

fordert Dich zur Eingabe eines Passworts für den Nutzer auf. **Achtung**: Wenn die Datei `/etc/nginx/htpasswd`
bereits existiert, wird sie durch diesen Befehl überschrieben. Um das zu vermeiden, kannst Du das `-c` einfach
weglassen.

### sudo-Rechte für Nutzer www-data vergeben

Damit auch eine Steuerung über das Webinterface möglich ist, muss der Nutzer www-data, unter dem nginx läuft, berechtigt sein, die Steuerungsskripte unter der Nutzerkennung klima aufzurufen. Um das zu ermöglichen, musst Du die Datei `/etc/sudoers` mit dem Kommando

    $ sudo visudo

bearbeiten und die folgende Zeile am besten am Ende eintragen:

    www-data ALL=(klima) NOPASSWD: /opt/klima/bin/fanctl.py

### nginx neu starten

    $ sudo /etc/init.d/nginx stop
    $ sudo /etc/init.d/nginx start
    
Die Webseite sollte jetzt unter

http://<IP-des-Pis>/klima

und

https://<IP-des-Pis>/klima

erreichbar sein.

_Optional:_ Einrichten von Log-Rotation
---------------------------------------

Ich habe für die Logfiles des Systems ein Skript für die wöchentliche Rotation eingerichtet. Dieses kannst Du per

    $ sudo install /opt/klima/misc/logrotate /etc/logrotate.d/klima

aktivieren. Du kannst das Skript natürlich auch noch an Deine Bedürfnisse anpassen.

_Optional:_ Überwachung des Systems durch Icinga 2
--------------------------------------------------

Die Konfiguration von Icinga 2 geht über den Rahmen dieser Anleitung hinaus und ist auf [http://docs.icinga.org/] ausführlich beschrieben. Falls Du Dir ein Icinga 2 einrichten möchtest, liefere ich mit /opt/klima/bin/nagios_check_klima ein Abfrageskript und mit /opt/klima/misc/icinga2_klima.conf eine Konfigurationsdatei für Icinga 2 mit.
