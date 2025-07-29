# protocol.py  06/18  Pasco Tang

# Eventually there will be sub modules to the protocol
# to include I2C, SPI, Uart, PWM, code load, and other stuff.
# For now, it only supports the GPIO module and it is loaded
# as the default context
from builtins import bytes
import time
def trace(msg):
  print(msg)

def error(msg):
  trace("error:" + str(msg))

IN  = 0
OUT = 1

GPIO_MODE_INPUT  = "I"
GPIO_MODE_OUTPUT = "O"

GPIO_READ       = "?"
GPIO_ANALOG       = "A"
GPIO_VALUE_HIGH = "1"
GPIO_VALUE_LOW  = "0"

PUD_DOWN = 21
PUD_UP = 22
PUD_OFF = 20
GPIO_PULL_DOWN  = "D"
GPIO_PULL_UP  = "U"
GPIO_PULL_NONE = "N"

def _pinch(channel):
  return chr(channel+ord('a'))

def _valuech(value):
  if value == None or value == 0 or value == False:
    return GPIO_VALUE_LOW
  return GPIO_VALUE_HIGH

def _modech(mode):
  if mode == None or mode == IN:
    return GPIO_MODE_INPUT
  return GPIO_MODE_OUTPUT

def _pudch(pud):
  if pud == PUD_DOWN:
    return GPIO_PULL_DOWN
  elif pud == PUD_UP:
    return GPIO_PULL_UP
  else:
    return GPIO_PULL_NONE

def _parse_valuech(ch):
  if ch == GPIO_VALUE_LOW:
    return False
  if ch == GPIO_VALUE_HIGH:
    return True
  error("Unknown value ch:" + str(ch))
  return GPIO_VALUE_HIGH

def _parse_avalue(ch):
  self.trace(ch)
  if ch == GPIO_VALUE_LOW:
    return False
  if ch == GPIO_VALUE_HIGH:
    return True
  error("Unknown value ch:" + str(ch))
  return GPIO_VALUE_HIGH


# CLIENT ===============================================================

class GPIOClient:
  """ The GPIO command set
      Assumes the wire protocol is already in the GPIO mode.
      As we only support the GPIO module at the moment,
      that's a simple assumption to make.
  """
  IN = 0
  OUT = 1
  DEBUG = False
  PUD_DOWN = 21
  PUD_UP = 22
  BOARDMODE = 0


  def trace(self, msg):
    if self.DEBUG:
      trace(msg)

  def __init__(self, wire, debug=False):
    self.wire = wire
    self.DEBUG = debug


  def setup(self, channel, mode, pull_up_down=None, initial=0):
    #TODO outer wrapper needs to do validation
    #if channel < self.MIN_PIN or channel > self.MAX_PIN:
    #  raise ValueError("Invalid pin")

    pinch = _pinch(channel)
    self.trace(pinch)

    modech = _modech(mode)
    
    # For input mode, default to pull up if not specified
    if mode == IN:
      if pull_up_down is None:
        pull_up_down = PUD_UP
      pudch = _pudch(pull_up_down)
      self._write(pinch + modech + pinch + pudch + 'Z')
    # For output mode, don't set pull up/down but set initial value
    elif mode == OUT:
      # Set initial value (defaults to LOW/0)
      self._write(pinch + modech + pinch + _valuech(initial) + 'Z')


  def input(self, channel):
    pinch = _pinch(channel)
    time.sleep(0.01)
    response = self._write(pinch + GPIO_READ + 'Z')
    
    # Parse response in format "GPIO18: 1"
    try:
        response_str = response.decode(encoding='UTF-8').strip()
        gpio_num = int(response_str.split(':')[0].replace('GPIO', ''))
        value = int(response_str.split(':')[1].strip())
        
        # Verify GPIO number matches requested channel
        if gpio_num == channel:
            return value
        else:
            error(f"GPIO number mismatch: expected {channel}, got {gpio_num}")
            return False
    except (ValueError, IndexError) as e:
        error(f"Failed to parse response: {response_str}")
        return False



  def output(self, channel, value):
    #TODO outer wrapper needs to do validation
    #if channel < self.MIN_PIN or channel > self.MAX_PIN:
    #  raise ValueError("Invalid pin")
    ch = _pinch(channel)
    v = _valuech(value)

    time.sleep(0.01)
    if value == None or value == 0 or value == False:
      self._write(ch + GPIO_VALUE_LOW + 'Z')
    else:
      self._write(ch + GPIO_VALUE_HIGH + 'Z')
    #TODO read and verify echoback

  def cleanup(self):
    pass


  # redirector to wrapped comms link
  def _open(self, *args, **kwargs):
    self.trace("open")
    self.wire.open(*args, **kwargs)

  def _write(self, *args, **kwargs):
    self.trace("write:" + str(*args) + " " + str(**kwargs))
    self.wire.write(*args, **kwargs)
    time.sleep(0.01)
    v=self._read(100, termset="\n")
    self.trace("read back:" + v.decode(encoding='UTF-8'))
    return v

  def _read(self, *args, **kwargs):
    self.trace("read")
    return self.wire.read(*args, **kwargs)

  def _close(self):
    self.trace("close")
    self.wire.close()
