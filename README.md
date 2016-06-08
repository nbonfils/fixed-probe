# Open design of a fixed probe for water quality monitoring in rivers and lakes

This is the repository containing all the code and instructions necessary to build 
and run your own probe for water monitoring.

This work has been done by **Nils Bonfils** for his Bachelor project at 
[EPFL](http://epfl.ch/) and is supervised by **Robin Scheibler**.

This project takes part in a wider one, [the Biodesign project](https://biodesign.cc/). 
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

Feel free to contact me if you manage to get it working with different componoents, 
so these instructions can be improved and be more helpful. 

## The probe

The core of the probe is a [Raspberry Pi][rpi] which will control the sensors and 
handle the collect of the datas, then store/send it.

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

   A basic usb webcam can be used. 
   (I used a [LogiLink](http://logilink.com/showproduct/UA0072.htm) webcam)

### Data collection

The _Raspberry Pi_ handles the sensors and gets the data from them, and then the data 
has three possible ways to go.
1. Network is available

   The datas will be sent through the GPRS with the HTTP protocol via the GET method 
   to a server, which then can parse, process and even display the datas with a web 
   interface. The image are sent via the PUT method.

2. No network but a USB drive is plugged in

   The datas are stored on the _USB root directory_ in the _CSV_ format in a file named 
   *sensors_data.csv*. The images taken by the webcam are store in a directory named 
   *probe_img* in the _root directory_ of the USB and the images are called 
   YYYYMMDDHHMMSS.jpg according to the time they were taken.

3. No network, no USB

   Everything is stored locally on the SD card of the _Raspberry PI_, thus being the file 
   system of the OS that runs the _Raspberry Pi_. The datas are stored in 
   */srv/sensors/sensors_data.csv* and the images in */srv/sensors/probe_img/*.

The data collection system works by level. This means that when the first level is 
available everything will be done that way, otherwise it will use the second way, and the 
worst is the third. And as soon as a higher level is avaible things are "transfered" to 
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
need to get/store/send datas.

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

I suggest to run some tests before setting it up to seeif the behaviour is as expected.

## Instructions to set up and build the probe

**WORK IN PROGRESS**

[bmp180]: https://www.adafruit.com/products/1603
[rpi]: https://www.raspberrypi.org/
[turb_sensor_img]: https://images.duckduckgo.com/iu/?u=http%3A%2F%2Fshop.aftabrayaneh.com%2Fimage%2Fcache%2Fdata%2Farduino%2Fsensors%2FLight_Color%2FB1286%2FTurbidity_Sensor_B1286-500x500.jpg&f=1
[mcp3008]: https://www.adafruit.com/products/856
[at_commands]: https://en.wikipedia.org/wiki/Hayes_command_set
[gsm_click]: http://www.mikroe.com/click/gsm/
[lipo_rider_pro]: http://seeedstudio.com/item_detail.html?p_id=992
[witty_pi]: http://www.uugear.com/witty-pi-realtime-clock-power-management-for-raspberry-pi/
[ip]: https://en.wikipedia.org/wiki/IP_Code
