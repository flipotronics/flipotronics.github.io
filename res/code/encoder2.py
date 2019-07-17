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

  i2c = busio.I2C(board.SCL, board.SDA)
  mcp = MCP23017(i2c,address=0x20)  # MCP23017
  mcp.interrupt_enable = 0xFFFF       # INTerrupt ENable top 8 bits
  mcp.interrupt_configuration = 0x0000  

  clk0  = mcp.get_pin(0)
  dt0 = mcp.get_pin(1)


  clk0.direction = digitalio.Direction.INPUT
  clk0.pull = digitalio.Pull.UP
  dt0.direction = digitalio.Direction.INPUT
  dt0.pull = digitalio.Pull.UP

  def my_callback(self, arg):
    print(arg)
  
        
  def __init__(self):

      # print(GPIO.getmode()). -1=UNSET, 11=BCM, 10=BOARD
    INT_1A_PIN = 5
    INT_1B_PIN = 6


    GPIO.setup(INT_1A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(INT_1B_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)


    GPIO.add_event_detect(INT_1A_PIN, GPIO.FALLING)
    GPIO.add_event_detect(INT_1B_PIN, GPIO.FALLING)


    GPIO.add_event_callback(INT_1A_PIN, self.my_callback)
    GPIO.add_event_callback(INT_1B_PIN, self.my_callback)

    self.my_callback(5)


m = GPIOListener()

while True:
  time.sleep(1000)