


# FishPI 
## Aquarium touch screen interface and API for an

### Introduction
Fish PI is Actually version 3 of a design for a touch interface to drive an aquarium with an API backend allowing it's various functions to be connected to other IOT devices if required such as google home. 

Written in Python3 and running as a flask app with a flasgger swagger API. 

### Hardware

The hardware side is documented in a video which can be found here *link*

### Installation

Clone this Repo into an installation location such as 

`/usr/share/fishpi`

Within the fishpi directory is a config.ini file which contains details about the pins you are using. 
Set the pins to any GPIO you want to use, include your lighting pins and sensor pins. 

If starting from NOOBS you probably wont have pip3
`sudo apt-get python3-pip`

Clone to github repo and run 
`pip3 install -r requirements.txt`

Install the requirements to access GPIO pins for non-root users. Create new file
`sudo nano /etc/udev/rules.d/50-gpio.rules`

insert the following

`SUBSYSTEM=="gpio*", PROGRAM="/bin/sh -c '\
        chown -R root:gpiouser /sys/class/gpio && chmod -R 770 /sys/class/gpio;\
        chown -R root:gpiouser /sys/devices/virtual/gpio && chmod -R 770 /sys/devices/virtual/gpio;\
        chown -R root:gpiouser /sys$devpath && chmod -R 770 /sys$devpath\
'"`

now run

`
sudo groupadd gpiouser
`
`
sudo adduser pi gpiouser
`

This gives the standard PI user access to user GPIO pins without the need for root access. 

W1ThermSensor is not installed via requirements.txt as it is available for certain OS but will cause errors if 
it was unable to find it the sensor installed. 

Install manually if you are running on a Raspberry PI 

`pip3 install W1ThermSensor`

Next we want to install pi-blaster

[Follow the instrutions to build](https://github.com/sarfata/pi-blaster)

You probably, once compiled want to add a symbolic link to your /usr/bin/ directory allowing you call pi-blaster as
as a command. Ensure you have followed the instructions provided by sarfata to have pi-blaster auto start on boot. 

`sudo ln -s /home/pi/pi-blaster/pi-blaster /usr/bin/pi-blaster`

and finally you want to ensure pi-blaster on boot is configured to the correct pins. You can do this by adding to your
/etc/rc.local file

`sudo pi-blaster --gpio 13,27,19,21,26,20,16,12,7,5`

change your list of GPIO to the same pins you have configured for your lighting channels.

You should be able to boot fishpi for the first time

run `python3 /usr/share/fishpi/app.py`

FishPI will automaticly setup your Database on first boot and by default is available on port 54001





