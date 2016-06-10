# Open design of a fixed probe for water quality monitoring in rivers and lakes

This is the repository containing all the code and instructions necessary to build 
and run your own probe for water monitoring.

This work has been done by **Nils Bonfils** for his Bachelor project at 
[EPFL](http://epfl.ch/) and is supervised by **Robin Scheibler** and **Sachiko Hirosue**.

This project takes part in a wider one, [the Biodesign project][biodesign]. 
It was done within the [LCAV lab](http://lcav.epfl.ch/) at _EPFL_ and sponsored by it. The 
[Hackuarium bio-hackerspace](http://www.hackuarium.ch/en/) also provided tools and a 
place to work.

## Is this for me ?

You just need to have some DIY skills, for scrapping some materials, figuring out 
how to assemble some things together and figuring out how some components work. The 
instructions given here should also be taken more like guidelines based on what 
I could do with the materials I had. So it is not required that you have the exact same 
sensors or else, they'll surely work a little different, but as they should do the same 
things, there will be similarities too. 

You'll also need motivation and good will ! :)

Feel free to contact me if you manage to get it working with different components, 
so these instructions can be improved and be more helpful. 

## The probe

The core of the probe is a [Raspberry Pi][rpi] which will control the sensors and 
handle the collect of the data, then store/send it.

All the code in this repo was done on a raspberry pi under raspbian jessie lite. 
The only compatibility issue with other OS might be the systemd units (.service files). 
Otherwise its python3 code and it should work anywhere where python3 is installed.

### The sensors

The sensors connected to the _Raspberry Pi_ are :
+ Turbidity sensor

   To measure the clarity of the water, see on 
   [Wikipedia](https://en.wikipedia.org/wiki/Turbidity).

   The sensor itself is a basic three pin (VIN, DATA, GND) 
   [turbidity sensor][turb_sensor_img], like you can found in dishwashers. 
   (Mine was bought for 2$ on AliExpress)

   This is an analog sensor and the _Raspberry Pi_ hasn't a built-in analog-digital 
   converter, you'll need an external one like the [MCP3008][mcp3008] which works 
   fine for that.

+ Waterproof temperature sensor

   To measure the temperature of the water.

   The sensor is a [Waterproof DS18b](https://www.sparkfun.com/products/11050).

+ Air temperature and barometric pressure sensor

   To measure the ambient temperature as well as the pressure, to have a clue on 
   the weather.

   The sensor is a [BMP180][bmp180] from Adafruit.

+ Capturing images

   To take images of the water and have some visual feedback.

   A basic usb web-cam can be used. 
   (I used a [LogiLink](http://logilink.com/showproduct/UA0072.htm) web-cam)

### Data collection

The _Raspberry Pi_ handles the sensors and gets the data from them, and then the data 
has three possible ways to go.

1. Network is available

   The data will be sent through the GPRS with the HTTP protocol via the GET method 
   to a server, which then can parse, process and even display the data with a web 
   interface. The image are sent via the PUT method.

2. No network but a USB drive is plugged in

   The data are stored on the _USB root directory_ in the _CSV_ format in a file named 
   *sensors_data.csv*. The images taken by the web-cam are store in a directory named 
   *probe_img* in the _root directory_ of the USB and the images are called 
   YYYYMMDDHHMMSS.jpg according to the time they were taken.

3. No network, no USB

   Everything is stored locally on the SD card of the _Raspberry PI_, thus being the file 
   system of the OS that runs the _Raspberry Pi_. The data are stored in 
   */srv/sensors/sensors_data.csv* and the images in */srv/sensors/probe_img/*.

The data collection system works by level. This means that when the first level is 
available everything will be done that way, otherwise it will use the second way, and the 
worst is the third. And as soon as a higher level is available things are "transfered" to 
this level. For example data are stored locally (3), but when an USB drive is available (2)
everything will be dumped to it, and if it was network (1) everything that has been stored,
since the network was unavailable, will be sent to the server.

The communication with the network is done by the use of a GSM/GPRS module connected with 
the serial GPIO pins of the _Raspberry Pi_ which communicate with the legacy 
[AT commands][at_commands] language. (The one I used is a [GSM Click][gsm_click] module)

### Battery and power management

The _Raspberry Pi_ on its own needs ~700mA, so using a [Lipo Rider Pro][lipo_rider_pro] 
which can output up to 1A seems a reasonable choice. The [Lipo Rider Pro][lipo_rider_pro] 
is used along with a battery and a solar panel, so the probe can sustain longer on its own.

Also a [Witty Pi][witty_pi] can be used to improve even further the sustainability of the 
probe. The [Witty Pi][witty_pi] is an extension module that will be used on the 
_Raspberry Pi_ in order to shut it down to spare battery and to wake it up when there is a 
need to get/store/send data.

### Other components

Other components that are used for the probe that are non electronic although essential.
+ Two boxes

   One big that'll contains the raspberry pi and what's connected to it, and a smaller box 
   for the [BMP180][bmp180], I highly recommend the big box to be waterproof [IP66/IP67][ip]
   so the electronics inside won't be damaged as the probe should be setup up near water. 
   The smaller one needs some air to pass inside in order for the temperature and pressure 
   measure to be correct, doing tiny holes in it is ok, but the holes needs to be 
   protected so water can't drip in (rain, etc...).

+ Some cables

   To connects the sensors to the _Raspberry Pi_ and in order for the sensors to reach the 
   water cables should be long enough (2-4m seems ok). The can also be used to link the two
   boxes. I recommend using cables with 4 wires.

+ Some cable clamp

   For the cables of the sensors can exits the boxes without breaking the impermeability.

## Usage

Once built and set up, the usage of the probe is trivial.

You install it near a river of lake, possibly somewhere stable, so the probe don't fall or 
tip because of the wind, and hidden, so it don't get stolen. Temperature and turbidity 
sensors goes in the water, power up the _Raspberry Pi_ and then data should collected every
10 min and sent to a server or stored on a USB drive.

I suggest to run some tests before setting it up to see if the behaviour is as expected.

## Instructions to set up and build the probe

It will be separated into two parts, the setting up and installations of software on 
the _Raspberry Pi_ and the hook up of the circuits. The building part is left up to you
as the boxes you may have chosen could differ a lot there are no real instructions to make
holes in boxes and finding a way to fit everything in there, just try to keep everything
as waterproof as possible.

### The Raspberry Pi

At the very first what you want is to install a distribution on your _Raspberry Pi_,
it's strongly suggested to download the iso of [Raspbian Jessie Lite][raspbian]. Then
you'll just have to follow the instructions related to your system on 
[this page][raspbian_install].

Once your SD card is good to go plug it in the raspberry and power it up. The default 
login and password are :

   **Login : pi**

   **Password : raspberry**

After that I recommend you to change the default password with the following command

```bash
passwd
```

Enter the current password (should be "raspberry") and then the new one. Now you'll need 
to install new software. In order to do that, you'll need to update the system first :

```bash
sudo apt-get update
sudo apt-get upgrade
```

This can take a little while, once done we can proceed with the installations. I will here
just give the commands to enter as I will not enter into detailed explanations here.
If you want to know more about what you're doing, take a look at some Adafruit guides :
+ [Raspberry Pi setup][rpi_install]
+ [BMP180 setup][bmp_install]
+ [DS18B setup][ds18b_install]
+ [MCP3008 setup][mcp3008_install]

```bash
sudo apt-get install git python3-dev python3-rpi.gpio python3-smbus i2c-tools build-essential python3-setuptools python3-w1thermsensor fswebcam python3-udiskie
git clone https://github.com/adafruit/Adafruit_Python_BMP.git
cd Adafruit_Python_BMP
sudo python3 setup.py install
```

After that you'll need to configure some things manually, like kernel support for I2C 
as well as for the DS18B.

```bash
sudo nano /etc/modules
```

And add these two lines at the end of the file :

```bash
i2c-bcm2708
i2c-dev
```

Then you'll also need to comment some lines (put a '#' in front) if they exists :

```bash
sudo nano /etc/modprobe.d/raspi-blacklist.conf
```

And those two lines are :

```bash
blacklist spi-bcm2708
blacklist i2c-bcm2708
```

And finally, modify */boot/config.txt*.

```bash
sudo nano /boot/config.txt
```

Add these lines at the end :

```bash
# Enable use of BMP180 sensor
dtparam=i2c_arm=on
dtparam=i2c1=on

# Enable use of DS18B sensor
dtoverlay=w1-gpio
```

Once everything is done, reboot !

```bash
sudo reboot
```

Last thing to do after the reboot, to finish the sensors configuration.

```bash
sudo modprobe w1-gpio
sudo modprobe w1-therm
```

So now the _Raspberry Pi_ is ready to get all the sensors working. The last thing to do 
is to set up the server. Clone this repository first.

```bash
git clone https://github.com/nbonfils/fixed-probe.git
```

Setup the systemd service so the server start when the _Raspberry Pi_ is powered up.

```bash
cd /etc/systemd/system
sudo ln -s /home/pi/fixed-probe/sensor-server.service
sudo ln -s /home/pi/fixed-probe/usb-hotplug.service
cd /usr/local/bin
sudo ln -s /home/pi/fixed-probe/sensor-server.py
sudo systemctl enable sensor-server.service
sudo systemctl enable usb-hotplug.service
```

And at the next startup the server will be running and collect data from sensors.
If at any time you want to stop or start the server you can just use the following 
commands :

```bash
sudo systemctl stop sensor-server.service
sudo systemctl start sensor-server.service
```

And that's it, the _Raspberry PI_ is configured and ready to run. You still need to hook up
the circuits and build the probe.

### Circuits hook up

Here will be presented the hook up of the different components separately.

Depending on the _Raspberry Pi_ model there are more or less pins, but the layout of the 
pins are the same for the pins we are going to use. Here is the layout :

![rpi pinout][rpi_pinout]

#### BMP180

It's really easy, just connect the following pins together :

| BMP180 | RPi  |
| ------ | ---- |
| VIN    | 3.3V |
| GND    | GND  |
| SCL    | SCL  |
| SDA    | SDA  |

Here is the schema from Adafruit tutorial :

![bmp180 hook up][bmp_hook]

#### DS18B

For this one you'll need a 10k Ohms resistor.

| DS18B | RPi  |
| ----- | ---- |
| VIN   | 3.3V |
| DATA  | #4   |
| GND   | GND  |

The resistor should link the DATA and the VIN as in the following schema (from Adafruit) :

![ds18b hook up][ds18b_hook]

#### MCP3008 with turbidity sensor

Here you'll need a 10k Ohms resistor too. The hook up is slightly more complicated.

The pinout of the MCP3008 :

![mcp3008 pinout][mcp_pins]

If you hook this up just as follows, everything should work fine.

| MCP3008 | RPi  |
| ------- | ---- |
| VDD     | 3.3V |
| VREF    | 3.3V |
| AGND    | GND  |
| CLK     | #18  |
| DOUT    | #23  |
| DIN     | #24  |
| CS/SHDN | #25  |
| DGND    | GND  |

That's for connecting the adc to the _Raspberry Pi_, then to connect the turbidity sensor
to the adc, just hook it up like this :

| Sensor | MCP3008 | RPi  |
| ------ | ------- | ---- |
| VIN    | X       | 3.3V |
| DATA   | CH0     | X    |
| GND    | X       | GND  |

Along with that the 10k resistor should be installed between the DATA and the GND.

#### GSM module

The last module to hook up is the GSM module and as it's supposed to be used as a serial 
device, it's fairly simple.

| GSM | RPi  |
| --- | ---- |
| VIN | 3.3V |
| GND | GND  |
| TX  | RXD  |
| RX  | TXD  |

And that's it, everything should be hooked up, and if you launch the server, everything 
should work fine. The *sensors_data.csv* should fill up with actual data. The last thing 
to do if not already done is building the frame of the probe and fitting everything in.

## Bachelor project

If you want to know more about how I've built such a probe myself, or if you're just 
curious to learn more about this project, I invite you to go check the [wiki page][wiki] 
of this project.

Also If you're interested in other Bio-tech stuff, I strongly recommend you to visit the 
[Biodesign blog][biodesign] along with its [wiki][biodesign_wiki].

[biodesign]: https://biodesign.cc/
[bmp180]: https://www.adafruit.com/products/1603
[rpi]: https://www.raspberrypi.org/
[turb_sensor_img]: https://images.duckduckgo.com/iu/?u=http%3A%2F%2Fshop.aftabrayaneh.com%2Fimage%2Fcache%2Fdata%2Farduino%2Fsensors%2FLight_Color%2FB1286%2FTurbidity_Sensor_B1286-500x500.jpg&f=1
[mcp3008]: https://www.adafruit.com/products/856
[at_commands]: https://en.wikipedia.org/wiki/Hayes_command_set
[gsm_click]: http://www.mikroe.com/click/gsm/
[lipo_rider_pro]: http://seeedstudio.com/item_detail.html?p_id=992
[witty_pi]: http://www.uugear.com/witty-pi-realtime-clock-power-management-for-raspberry-pi/
[ip]: https://en.wikipedia.org/wiki/IP_Code
[raspbian]: https://www.raspberrypi.org/downloads/raspbian/
[raspbian_install]: https://www.raspberrypi.org/documentation/installation/installing-images/README.md
[rpi_install]: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/overview
[bmp_install]: https://learn.adafruit.com/using-the-bmp085-with-raspberry-pi/overview
[ds18b_install]: https://learn.adafruit.com/adafruits-raspberry-pi-lesson-11-ds18b20-temperature-sensing/overview
[mcp3008_install]: https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/overview
[rpi_pinout]: https://cdn-learn.adafruit.com/assets/assets/000/003/059/original/learn_raspberry_pi_gpio-srm.png
[bmp_hook]: https://cdn-learn.adafruit.com/assets/assets/000/001/692/original/raspberry_pi_BMP085_Breadboard_1K.png
[ds18b_hook]: https://cdn-learn.adafruit.com/assets/assets/000/003/782/original/learn_raspberry_pi_breadboard-probe.png
[mcp_pins]: https://cdn-learn.adafruit.com/assets/assets/000/001/222/original/raspberry_pi_mcp3008pin.gif
[wiki]: http://wiki.biodesign.cc/wiki/Fixed_Sensor
[biodesign_wiki]: http://wiki.biodesign.cc/wiki/Main_Page
