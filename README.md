# Shutters automation for usage with Somfy Remote

This project is a simple automation to control shutters with a Somfy Remote. It uses a Raspberry Pi Pico and a modified Somfy Remote to control the shutters.

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
2. Add config file
3. Copy the content of the `micropython` directory to the Raspberry Pi Pico W

### Configuration

The configuration file is located at `micropython/config.py`. The file should contain the following content:

```python
WIFI_SSID = "<SSID>"
WIFI_PASSWORD = "<PW>"
```

Replace `<SSID>` with the SSID of your WiFi network and `<PW>` with the password of your WiFi network.

### Usage

The Raspberry Pi Pico W will connect to the WiFi network and start a web server. You can access the web server by navigating to the IP address of the Raspberry Pi Pico W in your web browser. The web server will show a simple interface to control the shutters.

The Pico will also start a cron job to close the shutters sunset, opening is not implemented, because you can open the shutters with the remote or your phone.

#### Manual control with the web interface

The web interface will show a simple interface to control the shutters. You can open, stop and close the shutters with the buttons. It also shows the current state of the shutters, the current time and the time of the sunset and sunrise.

#### Manual control with your phone

To control the shutters with your phone, you can use the app [HTTP Request Shortcuts](https://play.google.com/store/apps/details?id=ch.rmy.android.http_shortcuts&hl=en&gl=US). 

- Open: `http://<IP-Address>/raise`
- Stop: `http://<IP-Address>/stop`
- Close: `http://<IP-Address>/lower`

Replace `<IP-Address>` with the IP address of the Raspberry Pi Pico W.

Then you can add these URLs to the app and create a shortcut on your home screen to control the shutters with your phone.

