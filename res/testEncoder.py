# Flipotronics.com
# Testing GPIO Expander from Adafruit und 8 rotary encodeders
# Adafruit GPIO Expander Bonnet - 16 Additional I/O over I2C
# Encoder: PEC11R-4220F-S0024   Mouser: https://www.mouser.com/ProductDetail/652-PEC11R-4220F-S24

# sudo pip3 install RPI.GPIO
# sudo pip3 install adafruit-blinka
# sudo pip3 install adafruit-circuitpython-mcp230xx

import time
import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017
import rtmidi
from Adafruit_LED_Backpack import SevenSegment

display = SevenSegment.SevenSegment()
display.begin()
display.clear()

display.clear()
display.print_float(0,decimal_digits=0, justify_right=True)
display.write_display()

midiout = rtmidi.MidiOut()
available_ports = midiout.get_ports()
print(available_ports)

if available_ports:
    midiout.open_port(3)
else:
    midiout.open_virtual_port("My virtual output")


i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c)  # MCP23017

#mcp = MCP23017(i2c, address=0x21)  # MCP23017 w/ A0 set
# 0 to 15 for the GPIOA0...GPIOA7, GPIOB0...GPIOB7 pins (i.e. pin 12 is GPIOB4).
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

counter0 = 0
counter1 = 0
counter2 = 0
counter3 = 0
counter4 = 0
counter5 = 0
counter6 = 0
counter7 = 0

clkLastState0 = clk0.value
clkLastState1 = clk1.value
clkLastState2 = clk2.value
clkLastState3 = clk3.value
clkLastState4 = clk4.value
clkLastState5 = clk5.value
clkLastState6 = clk6.value
clkLastState7 = clk7.value

try:
  while True:

    clkState0 = clk0.value
    dtState0 = dt0.value
    if clkState0 != clkLastState0:
      if dtState0 != clkState0:
        counter0 += 1
      else:
        counter0 -= 1
        print ("encoder 0: ")
        print (counter0)
        clkLastState0 = clkState0

    clkState1 = clk1.value
    dtState1 = dt1.value
    if clkState1 != clkLastState1:
      if dtState1 != clkState1:
        counter1 += 1
      else:
        counter1 -= 1
        print ("encoder 1: ")
        print (counter1)
        clkLastState1 = clkState1

    clkState2 = clk2.value
    dtState2 = dt2.value
    if clkState2 != clkLastState2:
      if dtState2 != clkState2:
        counter2 += 1
      else:
        counter2 -= 1
        print ("encoder 2: ")
        print (counter2)
        clkLastState2 = clkState2

    clkState3 = clk3.value
    dtState3 = dt3.value
    if clkState3 != clkLastState3:
      if dtState3 != clkState3:
        counter3 += 1
      else:
        counter3 -= 1
      if counter3 < 0:
        counter3 = 255
      if counter3 > 255:
        counter3 = 0
      prog_change = [0xC0, counter3 / 2]
      midiout.send_message(prog_change)
 
      print ("encoder 3: ")
      print (counter3 / 2)
      display.clear()
      display.print_float(counter3 / 2,decimal_digits=0, justify_right=True)
      display.write_display()
      clkLastState3 = clkState3

    clkState4 = clk4.value
    dtState4 = dt4.value
    if clkState4 != clkLastState4:
      if dtState4 != clkState4:
        counter4 += 1
      else:
        counter4 -= 1
        print ("encoder 4: ")
        print (counter4)
        clkLastState4 = clkState4
    
    clkState5 = clk5.value
    dtState5 = dt5.value
    if clkState5 != clkLastState5:
      if dtState5 != clkState5:
        counter5 += 1
      else:
        counter5 -= 1
        print ("encoder 5: ")
        print (counter5)
        clkLastState5 = clkState5  

    clkState6 = clk6.value
    dtState6 = dt6.value
    if clkState6 != clkLastState6:
      if dtState6 != clkState6:
        counter6 += 1
      else:
        counter6 -= 1
        print ("encoder 6: ")
        print (counter6)
        clkLastState6 = clkState6

    clkState7 = clk7.value
    dtState7 = dt7.value
    if clkState7 != clkLastState7:
      if dtState7 != clkState7:
        counter7 += 1
      else:
        counter7 -= 1
        print ("encoder 7: ")
        print (counter7)
        clkLastState7 = clkState7

        time.sleep(0.001)
finally:
  print("done")