#!/usr/bin/env python3

import time
import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017
import redis
import rtmidi
import RPi.GPIO as GPIO
from Adafruit_LED_Backpack import SevenSegment

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
HALF_STEP     = True
STATE_TAB = HALF_TAB if HALF_STEP else FULL_TAB

class GPIOListener(object):

  midiout = rtmidi.MidiOut()
  available_ports = midiout.get_ports()
  print(available_ports)

  if available_ports:
    midiout.open_port(3)
    print("Opened port 3")
    print(available_ports[3])
  else:
    midiout.open_virtual_port("My virtual output")
  
  state0 = R_START
  state1 = R_START
  state2 = R_START
  state3 = R_START
  state4 = R_START
  state5 = R_START
  state6 = R_START
  state7 = R_START

  i2c = busio.I2C(board.SCL, board.SDA)
  mcp = MCP23017(i2c,address=0x20)  # MCP23017
  mcp.interrupt_enable = 0xFFFF       # INTerrupt ENable top 8 bits
  mcp.interrupt_configuration = 0x0000  

  mcp2 = MCP23017(i2c,address=0x21) 
  mcp2.interrupt_enable = 0xFFFF       # INTerrupt ENable top 8 bits
  mcp2.interrupt_configuration = 0x0000  
  pin0 = mcp2.get_pin(3)  
  pin1 = mcp2.get_pin(2)  
  pin2 = mcp2.get_pin(1) 
  pin3 = mcp2.get_pin(0) 
  pin4 = mcp2.get_pin(4) 
  pin5 = mcp2.get_pin(5) 
  pin6 = mcp2.get_pin(6) 
  pin7 = mcp2.get_pin(7)
  pin8 = mcp2.get_pin(8) 
  pin9 = mcp2.get_pin(9) 
  pin10 = mcp2.get_pin(10) 
  pin11 = mcp2.get_pin(11) 
  pin12 = mcp2.get_pin(12) 
  pin13 = mcp2.get_pin(13) 
  pin14 = mcp2.get_pin(14) 
  pin15 = mcp2.get_pin(15) 

  pin0.direction = digitalio.Direction.INPUT
  pin0.pull = digitalio.Pull.UP

  pin1.direction = digitalio.Direction.INPUT
  pin1.pull = digitalio.Pull.UP

  pin2.direction = digitalio.Direction.INPUT
  pin2.pull = digitalio.Pull.UP

  pin3.direction = digitalio.Direction.INPUT
  pin3.pull = digitalio.Pull.UP

  pin4.direction = digitalio.Direction.INPUT
  pin4.pull = digitalio.Pull.UP

  pin5.direction = digitalio.Direction.INPUT
  pin5.pull = digitalio.Pull.UP

  pin6.direction = digitalio.Direction.INPUT
  pin6.pull = digitalio.Pull.UP

  pin7.direction = digitalio.Direction.INPUT
  pin7.pull = digitalio.Pull.UP

  pin8.direction = digitalio.Direction.INPUT
  pin8.pull = digitalio.Pull.UP

  pin9.direction = digitalio.Direction.INPUT
  pin9.pull = digitalio.Pull.UP

  pin10.direction = digitalio.Direction.INPUT
  pin10.pull = digitalio.Pull.UP

  pin11.direction = digitalio.Direction.INPUT
  pin11.pull = digitalio.Pull.UP

  pin12.direction = digitalio.Direction.INPUT
  pin12.pull = digitalio.Pull.UP

  pin13.direction = digitalio.Direction.INPUT
  pin13.pull = digitalio.Pull.UP

  pin14.direction = digitalio.Direction.INPUT
  pin14.pull = digitalio.Pull.UP

  pin15.direction = digitalio.Direction.INPUT
  pin15.pull = digitalio.Pull.UP

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
  r.set('page',0)


  mcp.clear_ints()
  mcp2.clear_ints()

  def button_callback(self, arg):

    # Black Page down
    if self.pin8.value:
      page = int(self.r.get('page'))
      page -= 1
      if page < 0: 
        page = 0
      print("page", end =" ")
      print(page)
      self.r.set('page',page)
 
    # Rot
    if self.pin9.value:
      print("9")

      #Program Down
    if self.pin10.value:
      print("10")
      self.program  = int(self.r.get('prog')) - 1
      if self.program < 1:
        self.program = 128
      self.r.set('prog', self.program)
      prog_change = [0xC0, self.program ]
      self.midiout.send_message(prog_change)
      print(self.program)

    # Program Up
    if self.pin11.value:
      print("11")
      self.program = int(self.r.get('prog')) + 1
      if self.program > 128 :
        self.program = 1
      self.r.set('prog', self.program)
      prog_change = [0xC0, self.program ]
      self.midiout.send_message(prog_change)
      print(self.program)

    # Blue - Page up
    if self.pin12.value:
      page = int(self.r.get('page'))
      page += 1
      if page > 63: 
        page = 63
      print("page", end =" ")
      print(page)
      self.r.set('page',page)

    if self.pin13.value:
      print("13")

        # Green
    if self.pin14.value:
      print("14")

        # Green
    if self.pin15.value:
      print("15")


  def my_callback(self, arg):

    page = int(self.r.get('page'))

    if not self.mcp.int_flag:
      self.mcp.clear_ints()
      return

    lp = self.mcp.int_flag[0]
    # print(lp)

    # Encoder 0
    if lp == 0 or lp == 1:
      dt0 = not self.dt0.value
      clk0 = not self.clk0.value
      pinstate = (clk0 << 1) | dt0
      self.state0 = STATE_TAB[self.state0 & 0xf][pinstate]
      result = self.state0 & 0x30
      if result:
        key = "param" + str(page * 8 + 0)
        c = int(self.r.get(key))
        if result == 32:
          if self.pin0.value:
            c -= 1
          else:
            c -= 10
        else:
          if self.pin0.value:
            c += 1
          else:
            c += 10
        if c < 0:
          c = 0
        if c > 127:
          c = 127
        self.r.set(key,c)

    # Encoder 1
    if lp == 2 or lp == 3:
      dt = not self.dt1.value
      clk = not self.clk1.value
      pinstate = (clk << 1) | dt
      self.state1 = STATE_TAB[self.state1 & 0xf][pinstate]
      result = self.state1 & 0x30
      if result:
        key = "param" + str(page * 8 + 1)
        c = int(self.r.get(key))
        if result == 32:
          if self.pin1.value:
            c -= 1
          else:
            c -= 10
        else:
          if self.pin1.value:
            c += 1
          else:
            c += 10
        if c < 0:
          c = 0
        if c > 127:
          c = 127
        self.r.set(key,c)

    # Encoder 2
    if lp == 4 or lp == 5:
      dt = not self.dt2.value
      clk = not self.clk2.value
      pinstate = (clk << 1) | dt
      self.state2 = STATE_TAB[self.state2 & 0xf][pinstate]
      result = self.state2 & 0x30
      if result:
        key = "param" + str(page * 8 + 2)
        c = int(self.r.get(key))
        if result == 32:
          if self.pin2.value:
            c -= 1
          else:
            c -= 10
        else:
          if self.pin2.value:
            c += 1
          else:
            c += 10
        if c < 0:
          c = 0
        if c > 127:
          c = 127
        self.r.set(key,c)

    # Encoder 3
    if lp == 6 or lp == 7:
      dt = not self.dt3.value
      clk = not self.clk3.value
      pinstate = (clk << 1) | dt
      self.state3 = STATE_TAB[self.state3 & 0xf][pinstate]
      result = self.state3 & 0x30
      if result:
        key = "param" + str(page * 8 + 3)
        c = int(self.r.get(key))
        if result == 32:
          if self.pin3.value:
            c -= 1
          else:
            c -= 10
        else:
          if self.pin3.value:
            c += 1
          else:
            c += 10
        if c < 0:
          c = 0
        if c > 127:
          c = 127
        self.r.set(key,c)

    # Encoder 4
    if lp == 8 or lp == 9:
      dt = not self.dt4.value
      clk = not self.clk4.value
      pinstate = (clk << 1) | dt
      self.state4 = STATE_TAB[self.state4 & 0xf][pinstate]
      result = self.state4 & 0x30
      if result:
        key = "param" + str(page * 8 + 4)
        c = int(self.r.get(key))
        if result == 32:
          if self.pin4.value:
            c -= 1
          else:
            c -= 10
        else:
          if self.pin4.value:
            c += 1
          else:
            c += 10
        if c < 0:
          c = 0
        if c > 127:
          c = 127
        self.r.set(key,c)

    # Encoder 5
    if lp == 10 or lp == 11:
      dt = not self.dt5.value
      clk = not self.clk5.value
      pinstate = (clk << 1) | dt
      self.state5 = STATE_TAB[self.state5 & 0xf][pinstate]
      result = self.state5 & 0x30
      if result:
        key = "param" + str(page * 8 + 5)
        c = int(self.r.get(key))
        if result == 32:
          if self.pin5.value:
            c -= 1
          else:
            c -= 10
        else:
          if self.pin5.value:
            c += 1
          else:
            c += 10
        if c < 0:
          c = 0
        if c > 127:
          c = 127
        self.r.set(key,c)

    # Encoder 6
    if lp == 12 or lp == 13:
      dt = not self.dt6.value
      clk = not self.clk6.value
      pinstate = (clk << 1) | dt
      self.state6 = STATE_TAB[self.state6 & 0xf][pinstate]
      result = self.state6 & 0x30
      if result:
        key = "param" + str(page * 8 + 6)
        c = int(self.r.get(key))
        if result == 32:
          if self.pin6.value:
            c -= 1
          else:
            c -= 10
        else:
          if self.pin6.value:
            c += 1
          else:
            c += 10
        if c < 0:
          c = 0
        if c > 127:
          c = 127
        self.r.set(key,c)

    # Encoder 7
    if lp == 14 or lp == 15:
      dt = not self.dt7.value
      clk = not self.clk7.value
      pinstate = (clk << 1) | dt
      self.state7 = STATE_TAB[self.state7 & 0xf][pinstate]
      result = self.state7 & 0x30
      if result:
        key = "param" + str(page * 8 + 7)
        c = int(self.r.get(key))
        if result == 32:
          if self.pin7.value:
            c -= 1
          else:
            c -= 10
        else:
          if self.pin7.value:
            c += 1
          else:
            c += 10
        if c < 0:
          c = 0
        if c > 127:
          c = 127
        self.r.set(key,c)

    self.mcp2.clear_ints() 


  def __init__(self):
    INT_1A_PIN = 13 #5
    INT_1B_PIN = 19 # 6
    INT_2A_PIN = 5 #13
    INT_2B_PIN = 6 #19

    GPIO.setup(INT_1A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(INT_1A_PIN, GPIO.FALLING)
    GPIO.add_event_callback(INT_1A_PIN, self.my_callback)
    GPIO.setup(INT_1B_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(INT_1B_PIN, GPIO.FALLING)
    GPIO.add_event_callback(INT_1B_PIN, self.my_callback)

    GPIO.setup(INT_2A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(INT_2A_PIN, GPIO.FALLING)
    GPIO.add_event_callback(INT_2A_PIN, self.button_callback)


m = GPIOListener()
display = SevenSegment.SevenSegment()
display.begin()
display.clear()
lastProg = int(m.r.get('prog'))
display.print_float(lastProg,decimal_digits=0, justify_right=True)
display.write_display()
while True:
    newProg = int(m.r.get('prog'))
    if newProg != lastProg:
        display.clear()
        display.print_float(lastProg + 1,decimal_digits=0, justify_right=True)
        display.write_display()  
        lastProg = newProg
    time.sleep(0.1)

