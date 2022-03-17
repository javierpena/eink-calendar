#!/usr/bin/env python
# Inspiration from https://github.com/zli117/EInk-Calendar/tree/master/resources

import configparser
import os
from datetime import datetime, timedelta
from PIL import Image, ImageFont, ImageDraw
import sys
import time

from drivers.caldavprovider import CalDavProvider
from drivers.icalprovider import ICalProvider
from widgets.calendarwidget import CalendarWidget
from widgets.timewidget import TimeWidget
from widgets.weatherwidget import WeatherWidget

def today_calendar():
    fullimg = Image.new('1', (640, 384), color=255)
    fullimg2 = Image.new('1', (640, 384), color=255)
    weather = WeatherWidget(owm_api_key)
    fullimg.paste(weather.get_weather(owm_location), box=(0, 0))
    timewidget = TimeWidget()
    fullimg.paste(timewidget.get_time(), box=(128, 0))
    calendar = CalendarWidget(family_names)
    event_getter = CalDavProvider(calendar_username, calendar_password)
    ical_event_getter = ICalProvider()
    test_event_list = []

    today_start = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
    today_end = today_start.replace(hour=21, minute=0, second=0, microsecond=0)

    for url in calendar_list:
        if url.endswith('.ics'):
            # This is an iCal URL
            test_event_list.append(ical_event_getter.get_calendar(url, today_start, today_end))
        else:
            test_event_list.append(event_getter.get_calendar(url, today_start, today_end))
    img1, img2 = calendar.get_calendar(test_event_list)
    fullimg.paste(img1, box=(0, 80))
    fullimg2.paste(img2, box=(0, 80))
    return fullimg, fullimg2

def week_calendar(calid, name):
    fullimg = Image.new('1', (640, 384), color=255)
    fullimg2 = Image.new('1', (640, 384), color=255)
    weather = WeatherWidget(owm_api_key)
    fullimg.paste(weather.get_weather(owm_location), box=(0, 0))
    timewidget = TimeWidget()
    fullimg.paste(timewidget.get_time(), box=(128, 0))
    event_getter = CalDavProvider(calendar_username, calendar_password)
    ical_event_getter = ICalProvider()
    test_event_list = []

    today = datetime.today()
    curdate = today + timedelta(days=-today.weekday(), weeks=0)
    curdate = curdate.replace(hour=8, minute=0, second=0, microsecond=0)

    for day in range(7, 12):
        if calendar_list[calid].endswith('.ics'):
            # iCal calendar
            test_event_list.append(ical_event_getter.get_calendar(calendar_list[calid], curdate, curdate.replace(hour=21)))
        else:
            # CalDAV
            test_event_list.append(event_getter.get_calendar(calendar_list[calid], curdate, curdate.replace(hour=21)))
        curdate = curdate + timedelta(days=1)

    calendar = CalendarWidget(['L', 'M', 'X', 'J', 'V'])
   
    img1, img2 = calendar.get_calendar(test_event_list, title=name)
    fullimg.paste(img1, box=(0, 80))
    fullimg2.paste(img2, box=(0, 80))
    return fullimg, fullimg2

def special_image():
    today = datetime.now()
    filename = '%02d-%02d-%4d' % (today.day, today.month, today.year)
    filename_jpg = filename + '.jpg'
    filename_png = filename + '.png'
    img = None
    img2 = Image.new('1', (640, 384), color=255)
    if os.path.exists(os.path.join('./img', filename_jpg)):
        img = Image.open(os.path.join('./img', filename_jpg)).convert('1').resize((640,384))
    elif os.path.exists(os.path.join('./img', filename_png)):
       img = Image.open(os.path.join('./img', filename_png)).convert('1').resize((640,384))
    if img:
        return img, img2, True
    return img2, img2, False

def night_image():
    img = Image.open(os.path.join('./img', 'night_image.jpg')).convert('1').resize((640,384))
    img2 = Image.new('1', (640, 384), color=255)
    return img, img2

cp = configparser.RawConfigParser()
cp.read('config.ini')
video_driver = cp.get('DEFAULT', 'video')
kbd_driver = cp.get('DEFAULT', 'keyboard')
owm_api_key = cp.get('weather', 'owm_api_key')
owm_location = cp.getint('weather', 'owm_location')
calendar_username = cp.get('calendar', 'username')
calendar_password = cp.get('calendar', 'password')
calendar_list=[]
for item in cp.get('calendar', 'urls').split(','):
    calendar_list.append(item.strip())
family_names = []
for item in cp.get('calendar', 'names').split(','):
    family_names.append(item.strip())

if video_driver == 'pygame':
    from drivers.pygamedriver import PygameDriver
    video = PygameDriver(640, 384)
elif video_driver == 'eink':
    from drivers.einkdriver import EinkDriver
    video = EinkDriver(640, 384)

if kbd_driver == 'pygame':
    from drivers.pygamedriver import PygameKBDriver
    keyboard = PygameKBDriver()
elif kbd_driver == 'gpio':
    from drivers.gpiodriver import GPIODriver
    keyboard = GPIODriver()

current_screen = 0
try:
    while True:
        print("Reading calendar data", flush=True)
        start_time = datetime.now()
        images = []
        images.append(today_calendar())
        images.append(week_calendar(0, family_names[0]))
        images.append(week_calendar(1, family_names[1]))
        images.append(week_calendar(2, family_names[2]))
        special_img1, special_img2, is_today_special = special_image()
        if not is_today_special:
            special_img1, special_img2 = night_image()
        images.append([special_img1, special_img2])

        done = False
        refresh = True
        while not done:
            if refresh:
                print("Display", flush=True)
                video.display(image1=images[current_screen][0], image2=images[current_screen][1])
                refresh = False
            print("Wait for keypress", flush=True)
            value = keyboard.wait_for_keypress(timeout=60)
            print("Received keypress: %s" % value, flush=True)
            if value:
                current_screen = value - 1
                refresh = True
            else:
                current_time = datetime.now()
                if current_time.hour > 21 or current_time.hour < 7:
                    current_screen = 4
                else:
                    current_screen = 0
            current_time = datetime.now()
            delta_time = current_time - start_time
            if delta_time.seconds > 600: 
                # After 10 minutes, re-read calendar data
                done = True
finally:
    print("Quit", flush=True)
    video.end()
