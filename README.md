

# FishPI 
## Aquarium touch screen interface and API for an

### Introduction
Fish PI is Actually version 3 of a design for a touch interface to drive an aquarium with an API backend allowing it's various functions to be connected to other IOT devices if required such as google home. 

Written in Python3 and running as a flask app with a flasgger swagger API. 

### Hardware

The hardware side is documented in a video which can be found here *link*

### Installation

Clone to github repo and run 
`pip3 -r requirements.txt`

Install the requirements to access GPIO pins for non-root users
`sudo nano /etc/udev/rules.d/50-gpio.rules`

`SUBSYSTEM=="gpio*", PROGRAM="/bin/sh -c '\
        chown -R root:gpiouser /sys/class/gpio && chmod -R 770 /sys/class/gpio;\
        chown -R root:gpiouser /sys/devices/virtual/gpio && chmod -R 770 /sys/devices/virtual/gpio;\
        chown -R root:gpiouser /sys$devpath && chmod -R 770 /sys$devpath\
'"`

`
sudo groupadd gpiouser
sudo adduser pi gpiouser
`

This gives the standard PI user access to user GPIO pins without the need for root access. 

W1ThermSensor is not installed via requirements.txt as it is available for certain OS but will cause errors if 
it was unable to find it the sensor installed. 

Install manually if you are running on a Raspberry PI 

`pip3 install W1ThermSensor`

