#!/usr/bin/env python3

import time
import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017
import RPi.GPIO as GPIO

class GPIOListener(object):

  i2c = busio.I2C(board.SCL, board.SDA)
  mcp = MCP23017(i2c,address=0x21)  # MCP23017
  mcp.interrupt_enable = 0xFFFF       # INTerrupt ENable top 8 bits
  mcp.interrupt_configuration = 0x0000  
  #mcp.interrupt_configuration = 0xFFFF 
#  mcp.default_value = 0xFFFF 
#  mcp.io_control = 0x44 

  clk0  = mcp.get_pin(0)
  dt0 = mcp.get_pin(1)

  clk0.direction = digitalio.Direction.INPUT
  clk0.pull = digitalio.Pull.UP
  dt0.direction = digitalio.Direction.INPUT
  dt0.pull = digitalio.Pull.UP

  aLastState = clk0.value

  mcp.clear_ints()  

  def my_callback(self, arg):
    print(self.mcp.int_flag)
    aState = self.clk0.value
    if (aState != self.aLastState):
      if (self.dt0.value != aState):
        print("up")
      else:
        print("down")

    self.aLastState = aState
    self.mcp.clear_ints()

  def __init__(self):
    INT_1A_PIN = 5
    GPIO.setup(INT_1A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.add_event_detect(INT_1A_PIN, GPIO.FALLING)
    GPIO.add_event_callback(INT_1A_PIN, self.my_callback)

    #GPIO.setup(INT_1A_PIN, GPIO.IN, GPIO.PUD_UP) # Set up Pi's pin as input, pull up
    #GPIO.add_event_detect(INT_1A_PIN, GPIO.FALLING, callback=self.my_callback, bouncetime=10)

m = GPIOListener()
while True:
  time.sleep(1000)