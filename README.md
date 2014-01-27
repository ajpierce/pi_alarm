# Raspberry Pi Alarm Clock
This project takes a Raspberry Pi and, web-enabling it, turns it into an alarm
clock. The Pi is attached to a PowerSwitch Tail and controls a light in place
of an audio-based alarm to wake us up.

The alarm is configured through a web interface, and has been optimized for
both desktop and mobile.

![Web](http://i.imgur.com/DHOGohY.png)
![Mobile](http://i.imgur.com/8kUayQ4.png)

I made this for my wife for Christmas 2013, and it was super simple!  After a
month in the field, this alarm clock has received highest marks from the wife,
who says it is a pleasant way of waking up.

Note that this project requires some "hardware hacking," but it's simple enough
that any beginner should be able to follow along with this tutorial to make a
light-up alarm clock.

## Materials you will need:
+ Raspberry Pi (Model B) -- $35
    - Micro USB power supply (2.1 Amps) -- $10
    - 8GB SD Card (4GB will work, but you will need to delete extra distros from
    NOOBS when installing Raspbian, so save yourself the time and just spend the
    extra $1 on an 8GB SD card) -- $6
+ USB Wireless Adapter (I bought [this one](http://www.microcenter.com/product/411056/W311Mi_Wireless_N_Pico_USB_20_Adapter)
from my local Microcenter) -- $10
+ [Powerswitch Tail](http://www.powerswitchtail.com/Pages/default.aspx) (to
control the light) -- $25
+ Tailed LED (I bought [this one](http://www.microcenter.com/product/390223/Tailed_Bue_LED_5mm_Bulk)
from my local microcenter). -- $3
+ Cheap clamp-on lamp and light bulb: ~$10

**Total Cost:** ~$99 USD

Note that some things, like MicroUSB power supplies, lamps, wireless adapters,
and light bulbs (etc.) you might already have laying around. No need to purchase
everything outlined above -- "hacking" it together is half the fun!

## Step 1: Install Raspbian
There are already plenty of guides online for installing Raspbian on your
Raspberry Pi. Covering this falls out of the scope of this guide, but I will at
least link the [NOOBS package](http://www.raspberrypi.org/downloads) I used.

## Step 2: Get the Wifi interface up on your Raspberry Pi
I used [this guide](http://www.howtogeek.com/167425/how-to-setup-wi-fi-on-your-raspberry-pi-via-the-command-line/),
substituting nano for vi because I'm a VIM guy.

## Step 3: Install Prerequisites
Install `git` and `screen` so we can check out the code and run it in the
background.
```
sudo apt-get update
sudo apt-get install git screen
```

Next, install virtualenv for python by following the Initial Setup section of
[this guide](http://raspberry.io/wiki/how-to-get-python-on-your-raspberrypi/).

## Step 4: Install Alarm Software
First, become root. Then, navigate to the directory in which the code will
live, and create a virtual environment:
```
sudo su -
cd /opt
virtuanenv pi_alarm
cd pi_alarm
```
Next, check out the project from git, and install the python libraries:
```
git clone git@bitbucket.org:andrewjpierce/pi_alarm.git
./pi_alarm/script/setup.sh
```

Finally, change the path of the ALARM_DATA in `config.py` to be the
fully-qualified path of the install directory:
```
ALARM_DATA = '/opt/pi_alarm/pi_alarm/app/alarm_data.p`
```

## Step 5: Hook up the LED
For testing purposes, we want to hook up the LED to make sure that the signal
processing works before attempting to attach the Pi to the PowerSwitch Tail.

I plugged the LED into Pin 10 on the Raspberry Pi, like so:
![Pin 10 and LED](http://i.imgur.com/er2vYOV.jpg)

## Step 6: Fire up the software!
As root,
```
cd /opt/pi_alarm/pi_alarm
./run.py
```

If all goes well, you the Flask webserver should let you know that the
application is running on `0.0.0.0:80`.

Navigate to the IP address of your Raspberry Pi from a browser on another
computer (or your mobile phone). If all goes well, you should see a web site
full of mushy happy things for my wife.

Press the "ON" button near the bottom of the page. Does the LED light up? If so,
you're in business!

## Step 7: Hook up the Pi to the PowerSwitch Tail
After confirming that the LED lights up, I simply cut off the LED and screwed
the two wires into the PowerSwitch Tail, like so:
![RPi to PST](http://i.imgur.com/VcjAyyh.jpg)
Afterwards, I attached the Pi to the PST with a zip tie, and the hardware
hacking was complete!

## Step 8: Configure the server to run on boot
To ensure the alarm starts on boot, follow the guide [here](http://www.stuffaboutcode.com/2012/06/raspberry-pi-run-program-at-start-up.html),
but your script will be the simple one outlined below:

```
#!/bin/bash
screen -S alarm python /opt/pi_alarm/pi_alarm/run.py
```

This starts a new screen (with the name "alarm" and invokes python to start
the alarm clock server.

## Step 9: Enjoy!
Plug your light into the PowerSwitch Tail, and the PST and Alarm into a couple
of outlets. You're done!

## Changing the Appearance
Mushy love notes to a woman you don't know not your design aesthetic? No
problem!

`app/templates/index.html` is where you can shorten the text to something
practical.

`app/static/css/alarm.less` is the LESS file that compiles to
`app/static/css/alarm.css`, in which you may adjust the color scheme to
something less purple.

Finally, if you like the random messages that appear in the header, you can
make your own by editing `config.py`. If you'd prefer not to have them, remove
the tag from `app/templates/footer.html`.
