#!/usr/bin/python

# MUST BE RUN AS ROOT (due to GPIO access)
#
# Required software includes Adafruit_Thermal, Python Imaging and PySerial
# libraries. Other libraries used are part of stock Python install.
#
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

from __future__ import print_function
import RPi.GPIO as GPIO
import random, time, Image, socket
from Adafruit_Thermal import *

fanPin       = 23
ledPin       = 18
buttonPin    = 25
printer      = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)


def sofi():
  GPIO.output(fanPin, True)
  x = random.randint(300,850)
  value = ["totally great","not great at all","great enough","not especially great"]
  v = random.choice(value)
  printer.doubleHeightOn()
  printer.setSize('L')
  printer.justify('C')
  printer.boldOn()
  printer.feed(5)
  printer.print(x)
  printer.feed(3)
  printer.print(v)
  printer.feed(5)

def hold():
  GPIO.output(ledPin, GPIO.HIGH)
  sofi()
 

# Initialization

# Use Broadcom pin numbers (not Raspberry Pi pin numbers) for GPIO
GPIO.setmode(GPIO.BCM)

# Enable LED and button (w/pull-up on latter)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(fanPin, GPIO.OUT)
GPIO.output(fanPin, False)
GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# LED on while working
GPIO.output(ledPin, GPIO.HIGH)

# Processor load is heavy at startup; wait a moment to avoid
# stalling during greeting.
time.sleep(5)
printer.feed(5)

while True:
  if ( GPIO.input(buttonPin) == False ):
        print("Printing")
        sofi()
        GPIO.output(fanPin, False)
        print("Printed")
        time.sleep(.1)

if KeyboardInterrupt:
  GPIO.cleanup()

