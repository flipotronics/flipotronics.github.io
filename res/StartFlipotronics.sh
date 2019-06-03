#!/bin/bash
#sleep 5  # slows down execution of qjackctl/jackd

sudo jackd -dalsa -dhw:2 -r44100 -p128 -n2

#sudo jack_control start
#sudo jack_control ds alsa
#sudo jack_control dps device hw:Audio
#sudo jack_control dps rate 44100
#sudo jack_control dps nperiods 2
#sudo jack_control dps period 128
sleep 5
a2jmidid -e &
sleep 10
qjackctl &

sleep 5
/usr/bin/qsynth &

sleep 10

# Python Startups
nohup  /home/pi/encoder.py > encoder.log 2>&1 & 
nohup  /home/pi/setSeven.py > setSeven.log 2>&1 &