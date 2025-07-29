# anyio/arduino/GPIO.py  21/04/2014  D.J.Whale
#
# An ardunio (serial) based GPIO link

# CONFIGURATION ========================================================

DEBUG = False
# There was the option to use the serial library pre-installed. This has changed so that we know the python lib in use is the one distributed with the doer library.
#If you wish to use the built in one instead change the import doerserial to import serial which is below (Approx line 38)

MIN_PIN = 0
MAX_PIN = 27

IN      = 0
OUT     = 1
BCM     = 0
BOARD   = 1
HIGH    = 1
LOW     = 0

PUD_OFF = 20
PUD_DOWN = 21
PUD_UP = 22

VERSION = "DoerGPIO.GPIO 0.2"

# OS INTERFACE =========================================================

from DoerGPIO import protocol
from DoerGPIO import adaptors


#from os import sys, path
#thisdir = path.dirname(path.abspath(__file__))
#sys.path.append(thisdir)

#import doerserial as serial

#Temporarily changing back to normal serial

from DoerGPIO import doerserial

instance = protocol.GPIOClient(adaptors.SerialAdaptor(doerserial.s), DEBUG)

def setwarnings(option):
  instance.setwarnings(option)

def setmode(mode):
  instance.setmode(mode)

def setup(channel, mode,pull_up_down=None,initial=0):
  if type(channel) is list:
    for c in channel:
      instance.setup(c, mode,pull_up_down,initial)
  else:
    instance.setup(channel, mode,pull_up_down,initial)

def input(channel):
  return instance.input(channel)

def output(channel, value):
  instance.output(channel, value)

def cleanup(number=0):
  instance.cleanup()


# END
