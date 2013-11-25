# Raspberry Pi Alarm Clock
This project takes a Raspberry Pi and, web-enabling it, turns it into an alarm
clock. Our alarm clock will turn on a light to wake us up in the morning, which,
though not as *precise* as a traditional alarm clock, is a much more pleasant
way of waking up!

Note that this is really just an excuse to try "hardware hacking," and any
beginner should be able to follow along with this tutorial to make a
light-up alarm clock. I made this for my wife for Christmas 2013, and it was
super-simple. We're going to have fun!

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
+ Female to Male jumper cables (for connecting the GPIO pins on the Pi to the
Powerswitch tail; something like [this](http://www.adafruit.com/products/826))
-- $6
+ Cheap clamp-on lamp and light bulb: ~$10

**Total Cost:** ~$102 USD

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

## Step 3:
