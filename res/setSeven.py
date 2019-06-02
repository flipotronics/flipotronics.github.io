import redis
import time

display = SevenSegment.SevenSegment()
display.begin()
display.clear()

r = redis.Redis(host='localhost', port=6379, db=0)
lastProg = int(r.get('prog'))

display.print_float(lastProg,decimal_digits=0, justify_right=True)
display.write_display()

while True:
    newProg = int(r.get('prog'))
    if newProg != lastProg:
        display.clear()
        display.print_float(lastProg,decimal_digits=0, justify_right=True)
        display.write_display()  
        lastProg = newProg
    time.sleep(0.1)

