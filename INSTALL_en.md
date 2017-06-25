Installation instructions
=========================

Disclaimer: NO WARRANTIES
-------------------------

I'm happy that you're interested in my humidity controlled cellar ventilation project. I'll also be happy to help you implement it to the best of my abilities. I must stress, however, that this project comes with NO WARRANTIES, EXPRESS, IMPLIED, OR OTHERWISE, WHATSOEVER. If you fail to get it running, if it annoys your cat, even if it burns your house down, or causes any other damage, it's entirely your responsibility. I've programmed this as best I could and have had it running productively for over a year now without any problems. However, EVERYTHING YOU DO IS AT YOUR OWN RISK.

In this sense:

**Good luck and have fun!**

These instructions are based on installtion notes by user YoYo from the german Raspberry Pi Forum.

Functional principle
--------------------

The system works by comparing the absolute humidity of inside and outside air. This is calculated from the measured temperature and relative humidity. If the outside air is dryer than the inside air, the fans are turned on, otherwise they are turned off.

A few other parameters (hysteresis, temperature limits to avoid overheating or overcooling the cellar) which are explained under 'configuration' are also taken into account. Main parameter, however, is absolute humidity (measured in grams of water per cubic meter of air).

How to use these instructions
-----------------------------

Commands to be entered are shown in code blocks which look like this:

    $ uname -a

The dollar sign ($) symbolises the shell prompt and should not be entered.

Some commands need root rights. These are recognisable by the "sudo" prefix and should be executed by a user with appropriate sudo rights. All other commands should be executed as user "klima" which will created in the course of installation. Before executing these commands you therefore need to log in as "klima" or execute a

    $ su - klima

Overview
--------

The project consists of three components:

- central piece is the actual script collection vor reading and storing the measurements and controlling the fans. This system doesn't have an UI, can be run without an attached display and could in principle also be run without a network connection - which would of course mean that there wouldn't be any possibility for remote monitoring or control.

the other components are optional:

- controller\_v3.py is a GUI that displays the curent status and allows manual control of the fans. It's optimised for a 320x480 touch display and can be used directly on site. It can also be used remotely via X11 forwarding.

- The core system creates HTML pages and progression charts. These can be accessed via an optional web server installed on the Pi. The charts are somewhat more detailed than in the GUI, the control options are basically the same.

Parts needed
------------

You need:

- 1 Raspberry Pi  
  I use a Pi 3, but every other model should work as well. Just make sure that the Pi offers 2 USB ports and can be connected to a network.

- 1 USB receiver WDE1-2 (by german company ELV, www.elv.de)

- 2 radio sensors ASH 2200 (ELV)

- 1 USB power strip Energenie EG-PMS2
  This is my solution to switch the fans. The project could of course be adapted to other switching methods. If you're interested in that, please contact me and I'll be happy to help.
  
And optionally

- 1 3,5" touch screen (320x480) (possibly with case)
  Needed if you want to have a display and controls directly at the installation site. I use the Tontec model since it comes with a case. It also has a physical switch for the backlighgt which allows me to deactivate screen blanking and still only light the display when needen. *Caution*: I've seen pictures of the Tontec display without this switch. If this is important for you, I'd advise you to contact the seller before buying.
  
Alternatively, I'd recommend getting

- 1 case for the Pi (w/o display)

although that's of course not strictly necessary.

Requirements
------------

Starting point for these instructions is a fully installed, booting Raspberry Pi running a recent version of Raspbian Jessie and connected to the network. 

Preparing the system
--------------------

### Update and install some required packages

    $ sudo apt-get update
    $ sudo apt-get upgrade
    $ sudo apt-get install mercurial rrdtool python-rrdtool sispmctl socat

### Create groups and users

    $ sudo addgroup usb
    $ sudo adduser klima
    $ sudo usermod -a -G dialout,usb klima

### Activate SPI bus

This can be done via the GUI:

- Menu/Settings/Raspberry PI configuration
- Tab interfaces, activate the radio button for SPI

(Note: these have been translated back from German since I don't run a GUI myself. Please let me know what the actual wording is in the GUI.)

or via cli:

    $ sudo raspi-config

- Advanced Options/SPI/Enable

### Installing the software

Create the directory first

    $ sudo install -d -o klima -g klima /opt/klima

The, logged in as user klima:

    $ cd /opt
    $ hg clone https://m_reiter@bitbucket.org/m_reiter/klima

This will download the complete repository to /opt/klima.

#### Updating the software

If you installed the software as per these instructions, the following commands will tell you whether there are any updates available:

    $ cd /opt/klima
    $ hg incoming

If there are any updates, you can install them via:

    $ hg pull
    $ hg update

### Granting group write permissions for USB devices (for the power strip)

In standard Raspbian installation, only root is allowed to write to USB devices. To avoid inflationary use of sudo, I created a udev rule that also gives write permissions to group usb. You can install this rule as follows:

    $ sudo cp /opt/klima/misc/99-usbgroup.rules /etc/udev/rules.d/

Please reboot the Pi afterwards.

    $ ls -l /dev/bus/usb/001/

should then show you that the USB devices belong to group usb and are writable by this group.

    $ ls -l /dev/bus/usb/001/
    insgesamt 0
    crw-rw-r-- 1 root usb 189, 0 Aug  2 14:02 001
    crw-rw-r-- 1 root usb 189, 1 Aug  2 14:02 002
    crw-rw-r-- 1 root usb 189, 2 Aug  2 14:02 003
    crw-rw-r-- 1 root usb 189, 3 Aug  2 14:02 004
    crw-rw-r-- 1 root usb 189, 4 Aug  2 14:02 005
    crw-rw-r-- 1 root usb 189, 5 Aug  2 14:02 006
    crw-rw-r-- 1 root usb 189, 6 Aug  2 14:02 007

Preparation (Hardware)
----------------------

### Adressing the radio sensors

Since 2 sensors ASH 2200 are used, one must be given a new address as described in the instructions by ELV.

To this end, open the sensor with a small screwdriver and remove the jumper at position 1. This will give this sensor address 2.

The newly addressed sensor wil be used as the inside sensor, the other one as the outside sensor.

Insert batteries into both sensors.

### Connecting USB receiver WDE1-2 to the Raspberry

Just connect the USB cable enclosed with the sensor to the running Raspberry Pi. The sensor should be detected and accessible as /deb/ttyUSB0.

### Checking receiver and sensors

You can test the sensors with the command

    $ socat /dev/ttyUSB0,b9600 STDOUT     

This should produce, after some time (< 3 minutes) output similar to this:

    $ socat /dev/ttyUSB0,b9600 STDOUT
    $1;1;;25,7;20,9;;;;;;;42;70;;;;;;;;;;;;0
    $1;1;;25,6;20,9;;;;;;;41;70;;;;;;;;;;;;0

This shows both sensors are transmitting measurements.

Sensor 1: 25.7°C and 42 % relative humidity
Sensor 2: 20.9°C and 70 % relative humidity

Configuring the software
------------------------

Create the following directories under /opt/klima

    $ cd /opt/klima
    $ mkdir log
    $ mkdir data
    $ mkdir graphics
    $ mkdir -p ftp/uploads        * Note: I use this directory to upload German met service data for comparison. The system will happily run if this is just empty.

Since graphs and HTML fragments for the web interface are created every 3 minutes, we realise directory `/opt/klima/graphics` as a RAM disk to prevent SD card wear. You need to enter the following line (as root) into `/etc/fstab`:

    none           /opt/klima/graphics   tmpfs    defaults,noatime,uid=klima,gid=klima,size=10M  0       0

and execute

    $ sudo mount /opt/klima/graphics

afterwards.

Create the databases with rrdtool:

    $ cd /opt/klima
    $ ./bin/makerrd.sh data/aussen
    $ ./bin/makerrd.sh data/keller
    $ ./bin/makefanrrd.sh

#### Adjusting the parameters

You can now adjust the parameters in `/opt/klima/bin/fanctl.py` to your need. The parameters are:

- AHmargin and AHhysterese

  The main parameters. If absolute humidity on the outside is lower than on the inside by at least AHmargin grams per cubic meter, the fans will be switched on. If the fans are already running, they will be switched off if the difference drops below (AHmargin-Ahhysterese).

- Tkellermin, Tkellermax, and Thysterese

  Minimum and maximum temperature to prevent overheating or -cooling the cellar. If outside is colder than inside and lower then Tkellermin, the fans are only switched on if the inside temperature is at least Thysterese °C above Tkellermin. When the inside temperature reaches Tkellermin, the fans will be switched off. Tkellermax is handled correspondingly.

- DPmargin und DPhysterese

  A safety parameter: If outside is colder than inside, the fans will only be switched on if the inside temperature is at least DPmargin °C above the dew point. When the difference drops below (DPmargin-DPhysterese), the fans are switched off.
  
- UseInterval, LockInterval, IntervalOn, IntervalOff

  Parameters for optional interval ventilation: If UseInterval is set to "True", "switching on" the fans will mean that they will repeatedly run for IntervalOn minutes and then stay of for IntervalOff minutes so the fresh air just intaken has some time to absorb humidity from the cellar. If LockInterval is set to "True", interval ventilation will also be applied if ventilation is switched on manually, i.e. via the GUI or web interface.
  
  One remark: Naturally, if you use interval ventilation, the fans will at times stand still although they are shown as running in the GUI or web interface. To avoid confusion, I would therefore recommend not to use interval ventilation until you're sure that the system is working correctly.

#### Configuring a cron job and starting the system

If you now create a cron job for user klima with the following commands and reboot the Pi, the system should already be running.

    $ crontab /opt/klima/misc/crontab
    $ sudo reboot

To be able to control what the system does, I'd recommend installing at least one of the optional interfaces, though.

_Optional:_ Configuring the touch screen GUI
--------------------------------------------

Installation of the touch screen itself is beyond the scope of this document. If it's not straightforward using the instructions supplied with the screen, I'd recommend you try to get help on the [forum](https://www.raspberrypi.org/forums).

Once the display is installed, autostart of the GUI has to be configured. There are several methods to achieve this. I use the extremely light weight display manager nodm.

First, you have to configure the Pi to boot into the GUI without login:

    $ sudo raspi-config

choose "Boot options"->"Desktop GUI, requiring user to login". Afterwards, install nodm:

    $ sudo apt-get install nodm

This will drop you into the text based nodm configuration. You can choose the default for most options. The individual option to choose (in **bold**) are:

- Start nodm on boot? **Yes**
- User to start a session for: **klima**
- Lowest numbered vt on which X may start: **7**
- Options for the X server: **-nolisten tcp -nocursor**
- Minimum time (in seconds) for a session to be considered OK: **60**
- X session to use: **/etc/X11/Xsession**

Afterwards, you have to configure nodm as the default display manager:

    $ sudo sh -c "echo /usr/sbin/nodm > /etc/X11/default-display-manager"

and install the xsession for user klima:

    $ cp /opt/klima/misc/xsession ~/.xsession

After a reboot of the Pi via

    $ sudo shutdown -r now

the GUI should start automatically. This might not be instantaneous but should take no longer tan 5 minutes.

_Optional:_ Installation of the nginx web server
------------------------------------------------

### Install the package

    $ sudo apt-get install nginx apache2-utils


### install PHP

    $ sudo apt-get install php5-fpm php5-cgi php5-cli php5-common

### Configuring nginx for the cellar ventilation web interface

Copy the file klima.nginx from misc to /etc/nginx/sites-available/klima

    $ sudo cp /opt/klima/misc/klima.nginx /etc/nginx/sites-available/klima

Afterwards, you need to replace the text "<DYNAMIC DNS HOSTNAME>" by your external hostname if you want to be able to access the web interface from the internet. Otherwise, you can just delete the text.

All lines containing "ssl" are only needed if you want to secure access to the web interface via SSL. I'd definitely recommend that if you plan to make it available from the internet. If you only allow local access, you might not need it. In that case, just delete the lines from /etc/nginx/sites-available/klima.

Create a symlink in /etc/nginx/sites-enabled/

    $ cd /etc/nginx/sites-enabled
    $ sudo ln -s /etc/nginx/sites-available/klima klima
    $ sudo rm default    
    
### Configuring SSL

If you want to enable SSL access, you can generate certificates with the following commands:

    $ sudo mkdir /etc/nginx/ssl && cd /etc/nginx/ssl
    $ sudo openssl genrsa -out server.key 2048
    $ sudo openssl req -new -key server.key -out server.csr
    $ sudo openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

These will be so called "self signed" certificates, so your browser will complain at first access and you will have to add an exception for the certificates.

Alternatively, you can of course use professional certificates, e.g. from [https://letsencrypt.org/].

### Configure htpasswd for web access

Create the web user, e.g. 'klima':
    
    $ sudo htpasswd -c /etc/nginx/htpasswd klima

will prompt you to enter a password for this user. **Caution**: If the file `/etc/nginx/htpasswd`already exists, it will be overwritten. To avoid that, leave out the `-c`.

### Granting sudo rights for user www-data

To enable control via the web interface, the user www-data under which nginx runs, must be able to execute the control scripts as user klima. To enable this, edit `/etc/sudoers` with the command

    $ sudo visudo

and add the following line at the end:

    www-data ALL=(klima) NOPASSWD: /opt/klima/bin/fanctl.py

### Restart nginx

    $ sudo /etc/init.d/nginx stop
    $ sudo /etc/init.d/nginx start
    
The web interface should now be reachable at

http://<IP-of-your-Pi>/klima

and

https://<IP-of-your-Pi>/klima

_Optional:_ Configuring log rotation
---------------------------------------

I created a config file for weekly rotation of the system's log files. You can activate it via

    $ sudo install /opt/klima/misc/logrotate /etc/logrotate.d/klima

You can of course edit the file to suit your needs.

_Optional:_ Monitoring the system with Icinga 2
--------------------------------------------------

Configuration of Icinga 2 is beyond the scope of these instructions. It's described in detail at [http://docs.icinga.org/]. If you want to use Icinga 2, I provide a monitoring plugin as /opt/klima/bin/nagios_check_klima and an Icinga 2 config file as /opt/klima/misc/icinga2_klima.conf.
