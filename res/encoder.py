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

state = R_START

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
STATE_TAB = HALF_TAB if HALF_STEP else FULL_TAB

class GPIOListener(object):
  
  state = R_START
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
  mcp = MCP23017(i2c,address=0x20)  # MCP23017

  mcp.interrupt_enable = 0xFFFF       # INTerrupt ENable top 8 bits
  mcp.interrupt_configuration = 0x0000  


  i2c = busio.I2C(board.SCL, board.SDA)
  mcp = MCP23017(i2c,address=0x20)  # MCP23017

  mcp.interrupt_enable = 0xFFFF       # INTerrupt ENable top 8 bits
  mcp.interrupt_configuration = 0x0000  

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
  r = redis.Redis(host='localhost', port=6379, db=0)

  program = 0
  last_state = 0

  def my_callback(self, arg):

    # Encoder A0
    if arg == 5:
      pinstate = (self.clk3.value << 1) | self.dt3.value
      self.state = STATE_TAB[self.state & 0xf][pinstate]
      result = self.state & 0x30
      if result:
        if result == 32:
          self.program = self.program - 1
          if self.program < 1:
            self.program = 128
        else:
          self.program = self.program + 1
          if self.program > 128:
            self.program = 1
        self.r.set('prog', self.program)
        prog_change = [0xC0, self.program ]
        self.midiout.send_message(prog_change)
        print(self.program)
        time.sleep(0.05)

    # Encoder A1
    # Encoder A2
    # Encoder A3

    # Encoder B0
    # Encoder B1
    # Encoder B2
    # Encoder B3

    # Button A0
    # Button A1
    # Button A2
    # Button A3

    # Button B0
    # Button B1
    # Button B2
    # Button B3


        
  def __init__(self):

      # print(GPIO.getmode()). -1=UNSET, 11=BCM, 10=BOARD
    INT_1A_PIN = 5
    INT_1B_PIN = 6
    INT_2A_PIN = 13
    INT_2B_PIN = 19
    RESET_PIN = 26

    GPIO.setup(INT_1A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(INT_1B_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(INT_2A_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(INT_2B_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.setup(RESET_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    GPIO.add_event_detect(INT_1A_PIN, GPIO.FALLING)
    GPIO.add_event_detect(INT_1B_PIN, GPIO.FALLING)
    GPIO.add_event_detect(INT_2A_PIN, GPIO.FALLING)
    GPIO.add_event_detect(INT_2B_PIN, GPIO.FALLING)
    GPIO.add_event_detect(RESET_PIN, GPIO.FALLING)


    GPIO.add_event_callback(INT_1A_PIN, self.my_callback)
    GPIO.add_event_callback(INT_1B_PIN, self.my_callback)
    GPIO.add_event_callback(INT_2A_PIN, self.my_callback)
    GPIO.add_event_callback(INT_2B_PIN, self.my_callback)
    GPIO.add_event_callback(RESET_PIN,  self.my_callback)
    print("init complete")
    self.my_callback(5)


m = GPIOListener()

while True:
  time.sleep(1)




