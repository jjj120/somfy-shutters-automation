# Shutters automation for usage with Somfy Remote

This project is a simple automation to control shutters with a Somfy Remote. It uses a Raspberry Pi Pico W and a modified Somfy Remote to control and automate the shutters.

## Hardware

- Raspberry Pi Pico W
- Somfy Remote (modified)

### Hardware modifications

![Hardware modifications](./images/hardware_mod.png)

For modifying the Somfy Remote, you need to solder a wire to the PCB of the remote. There are a few debug pads on there, which are easy to solder to. 

| Pad Name on Remote | Pin Number on Pi Pico |
|---|---|
| UP   | 26 - GPIO 20 |
| MY   | 25 - GPIO 19 |
| DOWN | 24 - GPIO 18 |
| PR   | 22 - GPIO 17 |
| GND  | 23 - GND     |


## Software

The software is written in MicroPython. The code in the `micropython` directory is the code that runs on the Raspberry Pi Pico W. 

### Dependencies

- Microdot
- Microdot-async
- mcron
- sched

### Installation

1. Install MicroPython on the Raspberry Pi Pico W
1. Add config file
1. Copy the content of the `micropython` directory to the Raspberry Pi Pico W
1. Modify the remote and connect it to the Raspberry Pi Pico W
1. Restart the Raspberry Pi Pico W to start the automation
1. Wait a bit for the Raspberry Pi Pico W to connect to the WiFi network and start the web server
1. Access the web interface at `http://<IP-Address>` to check if the automation is running
1. (Optional) Connect to your wifi router and set a static IP for the Raspberry Pi Pico W
1. (Optional) Add the URLs to raise and lower to the app [HTTP Request Shortcuts](https://play.google.com/store/apps/details?id=ch.rmy.android.http_shortcuts&hl=en&gl=US) to control the shutters with your phone

### Configuration

The configuration file is located at `micropython/config.py`. The file should contain the following content:

```python
WIFI_SSID = "<SSID>"
WIFI_PASSWORD = "<PW>"
TELEGRAM_TOKEN = "<token>" # can be empty string if telegram is not used
LAT_LOCATION = "<location-lat>"
LNG_LOCATION = "<location-lng>"
LOWER_TIME = <lower-time-sec>
RAISE_TIME = <raise-time-sec>
RAISE_OFFSET = <raise-offset-time-sec>
```

Replace `<SSID>` with the SSID of your WiFi network and `<PW>` with the password of your WiFi network. If you want to use the Telegram bot, you need to replace `<token>` with the token of your Telegram bot. You can get the token from the [BotFather](https://core.telegram.org/bots#6-botfather). 

Replace `<location-lat>` and `<location-lng>` with the latitude and longitude of your location. You can get the latitude and longitude of your location from for example [Google Maps](https://www.google.com/maps).

Replace `<lower-time-sec>` with the time in seconds the shutters need to close. Replace `<raise-time-sec>` with the time in seconds the shutters need to open, from the position, where the lower part starts rising. Replace `<raise-offset-time-sec>` with the time in seconds the shutters need to open fully closed to  the position, where the lower part starts rising.


### Usage

The Raspberry Pi Pico W will connect to the WiFi network and start a web server. You can access the web server by navigating to the IP address of the Raspberry Pi Pico W in your web browser. The web server will show a simple interface to control the shutters.


#### Automatic control

- **Holiday mode**: Shutters will open at sunrise and close at sunset
- **Summer mode**: Shutters will open at sunset to keep the house cool.
- **Winter mode**: Shutters will close at sunset to keep the house warm.

The automatic control is based on the current time and the time of the sunset and sunrise. The time of the sunset and sunrise will be fetched from the [sunrise-sunset.org](sunrise-sunset.org) API.

The modes can be switched with the web interface at `http://<IP-Address>`. The current mode will be displayed on the web interface.


#### Manual control with the web interface

The web interface will show a simple interface to control the shutters. You can open, stop and close the shutters with the buttons or set the shutters to some close percentage. The percentage is the percentage of the shutters that are closed. They are only estimates from the rise and lower times. It does not get set immediately, but the shutters will move to the set percentage after some time (depending on the rise and lower times). 

It also shows the current state of the shutters, the current time and the time of the sunset and sunrise.

You can also set the mode to holiday, summer or winter with the buttons on the web interface.

#### Manual control with your phone

To control the shutters with your phone, you can use the app [HTTP Request Shortcuts](https://play.google.com/store/apps/details?id=ch.rmy.android.http_shortcuts&hl=en&gl=US). 

- Open: `http://<IP-Address>/raise`
- Stop: `http://<IP-Address>/stop`
- Close: `http://<IP-Address>/lower`

Replace `<IP-Address>` with the IP address of the Raspberry Pi Pico W.

Then you can add these URLs to the app and create a shortcut on your home screen to control the shutters with your phone.

