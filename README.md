# Eink family calendar

## What is it?
I needed to have an updatable calendar to keep track of my children's school agenda,
as well as some post-school activities. So instead of using a whiteboard, I thought
it would be a nice holiday project to do it with a Raspberry Pi 2 and an e-ink
screen. I got some inspiration from [this similar project](https://github.com/zli117/EInk-Calendar)
and went for it, and here's the result:

<img src="https://raw.githubusercontent.com/javierpena/eink-calendar/main/img/calendar.jpg" width="600">

## What do you need
- A Raspberry Pi (any model would do, I did it with a Pi 2), with the Raspberry Pi OS.
- Eink display: [640x384, 7.5inch E-Ink display HAT for Raspberry Pi, yellow/black/white three-color](https://www.waveshare.com/product/displays/e-paper/epaper-1/7.5inch-e-paper-hat-c.htm).
- A [1x4 matrix keypad](https://www.adafruit.com/product/1332) to allow you to switch
  between the different calendars. There are multiple clones in different shops.
- A photo frame to house the setup. I bought one at a local shop, just make sure it has
  enough depth to host all the hardware.
- One or more Caldav calendars to display.

By default, the e-ink display includes a hat to connect it directly on top of the GPIO
connectors. However, since we want to connect the keypad too, we need to use the cables
directly. Refer to [the vendor notes](https://www.waveshare.com/wiki/7.5inch_e-Paper_HAT_(B))
to check the GPIO pins you need to connect them to.

The keypad will be connected to GPIO pins 29, 31, 33, 35 and 37. 

## Configuring
Once the basic setup and connections are done, you will need to set up the `config.ini` file. 
This is its syntax:

```ini
[DEFAULT]
video = pygame
keyboard = pygame

[weather]
owm_api_key = <insert API key here>
owm_location = <insert location id here>

[calendar]
urls = http://example.com/caldavcal1, http://example.com/caldavcal2, http://example.com/ical3.ics
names = user1, user2, user3
username = user
password = password
```

### Driver configuration
We can use two different drivers to be used for both video output and keyboard input.
This allows us to hack and tests locally without using the e-ink screen all the time.

- For video, we can use `pygame` for the [Pygame](https://github.com/pygame/pygame)
  driver, or `eink` to use the e-ink screen.
- For keyboard input, we can use `pygame` to get input from your computer's keyboard,
  or `gpio` to use the 1x4 keypad connected to the GPIO pins 29, 31, 33, 35 and 37
  (5, 6, 13, 19 and 26 if you use the BCM2835 pin notation).

### Open Weather Map API configuration
You need to subscribe to the "Current Weather Data" [API](https://openweathermap.org/api).
Note that you need to sign in as a user (it's free). Once you get the API key and the
location id for your town, add them to the `owm_api_key` and `owm_location` keys in
the configuration file.

### Calendar configuration
You can use any CalDav or iCal link; in my case, I set up 3 calendars in a [Synology](https://www.synology.com)
DiskStation using Synology Calendar. The code should adapt to any number of calendars,
but keep in mind the resolution and font size.

The `urls` parameter is a comma-separated list of CalDav or iCal URLs. Currently,
iCal URLs are identified by a trailing `.ics` in the calendar URL. This may be
improved in the future.

Since each of those calendars will correspond to an actual person, `names` will
contain the list of names for each url. Make sure you spefify the same number
of URLs and names.

The `username` and `password` fields are self-explaining: include the user and
password to access the calendars, only for CalDav URLs.

If you want to use a different type of calendar, such as Google Calendar, you
will need to create a new driver. However, it is possible to export a read-only,
secret address for your Google Calendar following [this guide](https://support.google.com/calendar/answer/37648?hl=en#zippy=%2Cget-your-calendar-view-only).

Note that the library used for iCal support, [icalevents](https://pypi.org/project/icalevents/) has a bug in version 0.1.25
that may prevent events from being properly loaded. This was fixed by [this commit](https://github.com/jazzband/icalevents/pull/70),
so you will need to update to version 0.1.26 or later. As of this writing, version 0.1.26
is not available on PyPi.

## Running
The scripts directory contains a simple launcher script using a virtual environment,
and a systemd unit file you can use to ensure the program runs on startup.

When the application is stopped, it should clear the e-ink display, which is a good
idea to avoid displa burnout. In some cases, it may not happen (for example if
you get a power disruption). You can use the `reset_eink.py` script in those
cases to clear the screen.

## Usage
When started, the calendar will show today's calendar for everyone, from 8:00 to
21:00 (times are not configurable at the moment). You can switch to a weekly, Monday-to-Friday
calendar for each person by pressing the 2, 3 or 4 buttons in the keypad, and
switch back to the daily calendar by pressing 1. Yes, that means that having
more than 3 calendars could require code changes ;).

After 9 PM, the calendar will enter in screensaver mode, and display the image
in the `img/night_image.jpg` file. The image will be converted to a 1-bit format,
so it's better if you use a 1-bit image already.

If there is a JPG or PNG file named after today's date, in DD-MM-YYYY format
(for example, 01-01-2022.png for January 1st, 2022), the screensaver will use that
image instead of the default one. Be creative!

## License
Refer to the LICENSE file for licensing details.

The weathericons-regular-webfont font is licensed under the [SIL OFL 1.1](http://scripts.sil.org/OFL)
license.

The [DejaVuSansMono-Bold font](https://dejavu-fonts.github.io/) is licensed under the
Bitstream Vera and Public Domain.

The `epd7in5bc.py` and `epdconfig.py` files are taken from the [Waveshare e-Paper repository](https://github.com/waveshare/e-Paper/),
including patches inspired by [this pull request](https://github.com/waveshare/e-Paper/pull/104)
to improve screen refresh performance.

## Anything missing?
Feel free to contact me. This project was mainly created to scratch a personal itch,
but if it can be helpful to anyone, I'd be more than happy to improve it and
its documentation.

## Author
Javier Peña (@fj_pena).
