Readme.txt

Flipotronics Install Synth A1


INSTALL Manual 
==============

Base Image: 2019-04-08-raspbian-stretch.img

32Gb Micro SD - balenaEtcher

update rasp-config to latest version
America  UTF-8
Timezone: Los Angeles
enable VNC, SPI, I2C
boot to comand line autologon

sudo rpi-update -y
sudo reboot

sudo apt-get update -y
sudo apt-get upgrade -y
sudo reboot

cd ~
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/adafruit-pitft.sh
vi adafruit-pitft.sh 
override:   overlay=piscreen2r

chmod +x adafruit-pitft.sh
sudo ./adafruit-pitft.sh
4 480
1 Landscape



sudo ./adafruit-pitft.sh
reboot

sudo vi /boot/config.txt 
dtoverlay=piscreen2r



https://learn.adafruit.com/adafruit-pitft-3-dot-5-touch-screen-for-raspberry-pi/easy-install-2
http://ozzmaker.com/piscreen-driver-install-instructions-2/



Python Libraries Setup
========================
sudo pip3 install adafruit-circuitpython-mcp230xx


sudo apt-get install python-smbus python-imaging -y
sudo apt-get install build-essential python-dev -y

git clone https://github.com/adafruit/Adafruit_Python_LED_Backpack.git


Copy the PREEMPT Kernel in
=========================
copy kernel7_real.img to /boot pn the pi
add to /boot/config.txt :  kernel=kernel7_real.img




pip install Cython

PyGame
https://www.pygame.org/docs/ref/draw.html

PyAudio
https://people.csail.mit.edu/hubert/pyaudio/

PyMidi
https://github.com/mik3y/pymidi

PyFluidSynth
https://github.com/nwhitehead/pyfluidsynth



https://www.adafruit.com/product/4132



sudo apt-get install nginx
sudo apt-get install python3-pip
sudo pip3 install flask uwsgi

sudo apt-get install vmpk
sudo apt-get install patchage

rt-midi
==============
sudo apt-get install libjack-jackd2-dev
sudo apt-get install libasound2-dev
pip3 install Cython
pip3 install  python-rtmidi


screen timeout
===================
sudo nano ~/.config/lxsession/LXDE-pi/autostart
@xset s 0 0
@xset s noblank
@xset s noexpose
@xset dpms 0 0 0





note_on = [0x90, 60, 112] # channel 1, middle C, velocity 112
note_off = [0x80, 60, 0]
prog_change = [0xC0, 0x02] * channel 1, progr 3


