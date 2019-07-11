#!/usr/bin/env python3

import time
import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017
import rtmidi
import redis
import RPi.GPIO as GPIO

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

  # Initialize the I2C bus:
  i2c = busio.I2C(board.SCL, board.SDA)
 
  mcp = MCP23017(i2c,address=0x20)  # MCP23017
  mcp.interrupt_enable = 0xFFFF       # INTerrupt ENable top 8 bits
  mcp.interrupt_configuration = 0x0000  

  pin0 = mcp.get_pin(0)  # GPA0
  pin1 = mcp.get_pin(1)  # GPA1
  pin2 = mcp.get_pin(2) 
  pin3 = mcp.get_pin(3) 
  pin4 = mcp.get_pin(4) 
  pin5 = mcp.get_pin(5) 
  pin6 = mcp.get_pin(6) 
  pin7 = mcp.get_pin(7) 
  pin8 = mcp.get_pin(8) 
  pin9 = mcp.get_pin(9) 
  pin10 = mcp.get_pin(10) 
  pin11 = mcp.get_pin(11) 
  pin12 = mcp.get_pin(12) 
  pin13 = mcp.get_pin(13) 
  pin14 = mcp.get_pin(14) 
  pin15 = mcp.get_pin(15) 

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

  # Redis
  r = redis.Redis(host='localhost', port=6379, db=0)
  program = 0
  r.set('prog', program)

  def my_callback(self, arg):


    # Encoder A pressed
    if not self.pin0.value:
      print("0")
    
    # Encoder B pressed 
    if not self.pin1.value:
      print("1")

    # Encoder C pressed
    if not self.pin2.value:
      print("2")

    # Encoder D pressed
    if not self.pin3.value:
      print("3")

    # Encoder E pressed
    if not self.pin4.value:
      print("4")

    # Encoder F pressed
    if not self.pin5.value:
      print("5")

    # Encoder G pressed
    if not self.pin6.value:
      print("6")

    # Encoder H pressed
    if not self.pin7.value:
      print("7")

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
      if page > 8: 
        page = 8
      print("page", end =" ")
      print(page)
      self.r.set('page',page)

    # Green
    if self.pin13.value:
      print("13")


  def __init__(self):

        # print(GPIO.getmode()). -1=UNSET, 11=BCM, 10=BOARD
     # INT_1A_PIN = 5
      #INT_1B_PIN = 6
    INT_2A_PIN = 13
    INT_2B_PIN = 19
      #RESET_PIN = 26


    GPIO.setup(INT_2A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(INT_2B_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
     # GPIO.setup(RESET_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    GPIO.add_event_detect(INT_2A_PIN, GPIO.FALLING)
    GPIO.add_event_detect(INT_2B_PIN, GPIO.FALLING)
     #GPIO.add_event_detect(RESET_PIN, GPIO.FALLING)


    GPIO.add_event_callback(INT_2A_PIN, self.my_callback)
    GPIO.add_event_callback(INT_2B_PIN, self.my_callback)
      #GPIO.add_event_callback(RESET_PIN,  self.my_callback)
    print("init complete")
    self.my_callback(5)


m = GPIOListener()

while True:
  time.sleep(1000)