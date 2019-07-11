#!/usr/bin/env python3

import time
import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017
import rtmidi
import redis
import RPi.GPIO as GPIO

R_CCW_BEGIN   = 0x1
R_CW_BEGIN    = 0x2
R_START_M     = 0x3
R_CW_BEGIN_M  = 0x4
R_CCW_BEGIN_M = 0x5

# Values returned by 'process_'
# No complete step yet.
DIR_NONE = 0x0
# Clockwise step.
DIR_CW = 0x10
# Anti-clockwise step.
DIR_CCW = 0x20
R_START = 0x0
R_CW_FINAL  = 0x1
R_CW_BEGIN  = 0x2
R_CW_NEXT   = 0x3
R_CCW_BEGIN = 0x4
R_CCW_FINAL = 0x5
R_CCW_NEXT  = 0x6

HALF_TAB = (
  # R_START (00)
  (R_START_M,           R_CW_BEGIN,     R_CCW_BEGIN,  R_START),
  # R_CCW_BEGIN
  (R_START_M | DIR_CCW, R_START,        R_CCW_BEGIN,  R_START),
  # R_CW_BEGIN
  (R_START_M | DIR_CW,  R_CW_BEGIN,     R_START,      R_START),
  # R_START_M (11)
  (R_START_M,           R_CCW_BEGIN_M,  R_CW_BEGIN_M, R_START),
  # R_CW_BEGIN_M
  (R_START_M,           R_START_M,      R_CW_BEGIN_M, R_START | DIR_CW),
  # R_CCW_BEGIN_M
  (R_START_M,           R_CCW_BEGIN_M,  R_START_M,    R_START | DIR_CCW),
)

FULL_TAB = (
  # R_START
  (R_START,    R_CW_BEGIN,  R_CCW_BEGIN, R_START),
  # R_CW_FINAL
  (R_CW_NEXT,  R_START,     R_CW_FINAL,  R_START | DIR_CW),
  # R_CW_BEGIN
  (R_CW_NEXT,  R_CW_BEGIN,  R_START,     R_START),
  # R_CW_NEXT
  (R_CW_NEXT,  R_CW_BEGIN,  R_CW_FINAL,  R_START),
  # R_CCW_BEGIN
  (R_CCW_NEXT, R_START,     R_CCW_BEGIN, R_START),
  # R_CCW_FINAL
  (R_CCW_NEXT, R_CCW_FINAL, R_START,     R_START | DIR_CCW),
  # R_CCW_NEXT
  (R_CCW_NEXT, R_CCW_FINAL, R_CCW_BEGIN, R_START),
)

# Enable this to emit codes twice per step.
# HALF_STEP == True: emits a code at 00 and 11
# HALF_STEP == False: emits a code at 00 only
HALF_STEP     = False
STATE_TAB0 = HALF_TAB if HALF_STEP else FULL_TAB
STATE_TAB1 = HALF_TAB if HALF_STEP else FULL_TAB
STATE_TAB2 = HALF_TAB if HALF_STEP else FULL_TAB
STATE_TAB3 = HALF_TAB if HALF_STEP else FULL_TAB
STATE_TAB4 = HALF_TAB if HALF_STEP else FULL_TAB
STATE_TAB5 = HALF_TAB if HALF_STEP else FULL_TAB
STATE_TAB6 = HALF_TAB if HALF_STEP else FULL_TAB
STATE_TAB7 = HALF_TAB if HALF_STEP else FULL_TAB

class GPIOListener(object):

  state0 = R_START
  state1 = R_START
  state2 = R_START
  state3 = R_START
  state4 = R_START
  state5 = R_START
  state6 = R_START
  state7 = R_START
  
  midiout = rtmidi.MidiOut()
  available_ports = midiout.get_ports()
  print(available_ports)

  if available_ports:
    midiout.open_port(3)
    print("Opened port 3")
    print(available_ports[3])
  else:
    midiout.open_virtual_port("My virtual output")

  i2c = busio.I2C(board.SCL, board.SDA)
  mcp = MCP23017(i2c,address=0x21)  # MCP23017
  mcp.interrupt_enable = 0xFFFF       # INTerrupt ENable top 8 bits
  mcp.interrupt_configuration = 0x0000  
  #mcp.interrupt_configuration = 0xFFFF 
  #mcp.default_value = 0xFFFF 
#  mcp.io_control = 0x44 
  mcp.clear_ints()   

  clk0  = mcp.get_pin(0)
  dt0 = mcp.get_pin(1)

  clk1  = mcp.get_pin(2)
  dt1 = mcp.get_pin(3)

  clk2  = mcp.get_pin(4)
  dt2 = mcp.get_pin(5)

  clk3  = mcp.get_pin(6)
  dt3 = mcp.get_pin(7)

  clk4  = mcp.get_pin(8)
  dt4 = mcp.get_pin(9)

  clk5  = mcp.get_pin(10)
  dt5 = mcp.get_pin(11)

  clk6  = mcp.get_pin(12)
  dt6 = mcp.get_pin(13)

  clk7  = mcp.get_pin(14)
  dt7 = mcp.get_pin(15)

  clk0.direction = digitalio.Direction.INPUT
  clk0.pull = digitalio.Pull.UP
  dt0.direction = digitalio.Direction.INPUT
  dt0.pull = digitalio.Pull.UP

  clk1.direction = digitalio.Direction.INPUT
  clk1.pull = digitalio.Pull.UP
  dt1.direction = digitalio.Direction.INPUT
  dt1.pull = digitalio.Pull.UP

  clk2.direction = digitalio.Direction.INPUT
  clk2.pull = digitalio.Pull.UP
  dt2.direction = digitalio.Direction.INPUT
  dt2.pull = digitalio.Pull.UP

  clk3.direction = digitalio.Direction.INPUT
  clk3.pull = digitalio.Pull.UP
  dt3.direction = digitalio.Direction.INPUT
  dt3.pull = digitalio.Pull.UP

  clk4.direction = digitalio.Direction.INPUT
  clk4.pull = digitalio.Pull.UP
  dt4.direction = digitalio.Direction.INPUT
  dt4.pull = digitalio.Pull.UP

  clk5.direction = digitalio.Direction.INPUT
  clk5.pull = digitalio.Pull.UP
  dt5.direction = digitalio.Direction.INPUT
  dt5.pull = digitalio.Pull.UP

  clk6.direction = digitalio.Direction.INPUT
  clk6.pull = digitalio.Pull.UP
  dt6.direction = digitalio.Direction.INPUT
  dt6.pull = digitalio.Pull.UP

  clk7.direction = digitalio.Direction.INPUT
  clk7.pull = digitalio.Pull.UP
  dt7.direction = digitalio.Direction.INPUT
  dt7.pull = digitalio.Pull.UP

  r = redis.Redis(host='localhost', port=6379, db=0)

  aLastState = clk4.value


  def my_callback(self, arg):
    print(self.mcp.int_flag)
    print(self.clk4.value)
    print(self.dt4.value)
    aState = self.clk4.value
    if (aState != self.aLastState):
      if (self.dt4.value != aState):
        print("up")
      else:
        print("down")

    self.aLastState = aState
    self.mcp.clear_ints()
    return


      # 4
    pinstate = (self.clk4.value << 1) | self.dt4.value
    self.state4 = STATE_TAB4[self.state4 & 0xf][pinstate]
    result = self.state4 & 0x30
    if result:
      if result == 32:
        print("4 down")
      else:
        print("4 up")
      return


      # 5
    pinstate = (self.clk5.value << 1) | self.dt5.value
    self.state5 = STATE_TAB5[self.state5 & 0xf][pinstate]
    result = self.state5 & 0x30
    if result:
      if result == 32:
        print("5 down")
      else:
        print("5 up")
      return

      # 6
    pinstate = (self.clk6.value << 1) | self.dt6.value
    self.state6 = STATE_TAB6[self.state6 & 0xf][pinstate]
    result = self.state6 & 0x30
    if result:
      if result == 32:
        print("6 down")
      else:
        print("6 up")
      return

      # 7
    pinstate = (self.clk7.value << 1) | self.dt7.value
    self.state7 = STATE_TAB7[self.state7 & 0xf][pinstate]
    result = self.state7 & 0x30
    if result:
      if result == 32:
        print("7 down")
      else:
        print("7 up")
      return

      # 0
    pinstate = (self.clk0.value << 1) | self.dt0.value
    self.state0 = STATE_TAB0[self.state0 & 0xf][pinstate]
    result = self.state0 & 0x30
    if result:
      if result == 32:
        print("0 down")
      else:
        print("0 up")
      return

      # 1
    pinstate = (self.clk1.value << 1) | self.dt1.value
    self.state1 = STATE_TAB1[self.state1 & 0xf][pinstate]
    result = self.state1 & 0x30
    if result:
      if result == 32:
        print("1 down")
      else:
        print("1 up")
      return

      # 2
    pinstate = (self.clk2.value << 1) | self.dt2.value
    self.state2 = STATE_TAB2[self.state2 & 0xf][pinstate]
    result = self.state2 & 0x30
    if result:
      if result == 32:
        print("2 down")
      else:
        print("2 up")
      return

     # 3
    pinstate = (self.clk3.value << 1) | self.dt3.value
    self.state3 = STATE_TAB3[self.state3 & 0xf][pinstate]
    result = self.state3 & 0x30
    if result:
      if result == 32:
        print("3 down")
      else:
        print("3 up")
      return

        
  def __init__(self):

    INT_1A_PIN = 5
#    INT_1B_PIN = 6

    GPIO.setup(INT_1A_PIN, GPIO.IN, GPIO.PUD_UP) # Set up Pi's pin as input, pull up
#    GPIO.setup(INT_1B_PIN, GPIO.IN, GPIO.PUD_UP)

    GPIO.add_event_detect(INT_1A_PIN, GPIO.FALLING, callback=self.my_callback, bouncetime=10)
#    GPIO.add_event_detect(INT_1B_PIN, GPIO.FALLING, callback=self.my_callback, bouncetime=10)

#    GPIO.setup(INT_1A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#    GPIO.setup(INT_1B_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#    GPIO.add_event_detect(INT_1A_PIN, GPIO.FALLING)
#    GPIO.add_event_detect(INT_1B_PIN, GPIO.FALLING)

#    GPIO.add_event_callback(INT_1A_PIN, self.my_callback)
#    GPIO.add_event_callback(INT_1B_PIN, self.my_callback)

   # GPIO.setup(INT_1A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
   # GPIO.setup(INT_1B_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

   # GPIO.add_event_detect(INT_1A_PIN, GPIO.FALLING)
   # GPIO.add_event_detect(INT_1B_PIN, GPIO.FALLING)

   # GPIO.add_event_callback(INT_1A_PIN, self.my_callback)
   # GPIO.add_event_callback(INT_1B_PIN, self.my_callback)
    print("init complete")
    self.my_callback(5)

m = GPIOListener()

try:
  while True:
    time.sleep(1000)
finally:
  GPIO.cleanup()