import os
from pyowm import OWM
from PIL import Image, ImageFont, ImageDraw

class WeatherWidget():
    def __init__(self, api_key):
        self.api_key = api_key
        self.weatherfont = ImageFont.truetype(os.path.join('./fonts/', 'weathericons-regular-webfont.ttf'), 48)
        self.font16 =  ImageFont.truetype(os.path.join('./fonts/', 'DejaVuSansMono-Bold.ttf'), 16)
        self.owm = OWM(api_key)

    def get_weather(self, location):
        try:
            mgr = self.owm.weather_manager()
            current = mgr.weather_at_id(location)
            w = current.weather
            temp = w.temperature('celsius')['temp']
            wcode = w.weather_code
        except Exception:
            wcode = 900 # tornado
            temp = -273.0
        img = Image.new('1', (128, 64), color=255)
        imgdraw = ImageDraw.Draw(img)
        imgdraw.text((0, 0), self.wcode_to_unicode[wcode], font=self.weatherfont, fill=0)
        imgdraw.text((64, 32), '%.1fº' % temp, font=self.font16, fill=0)
        return img

    wcode_to_unicode = {
        200: u'\uf01e',
        201: u'\uf01e',
        202: u'\uf01e',
        210: u'\uf016',
        211: u'\uf016',
        212: u'\uf016',
        221: u'\uf016',
        230: u'\uf01e',
        231: u'\uf01e',
        232: u'\uf01e',
        300: u'\uf01c',
        301: u'\uf01c',
        302: u'\uf019',
        310: u'\uf017',
        311: u'\uf019',
        312: u'\uf019',
        313: u'\uf01a',
        314: u'\uf019',
        321: u'\uf01c',
        500: u'\uf01c',
        501: u'\uf019',
        502: u'\uf019',
        503: u'\uf019',
        504: u'\uf019',
        511: u'\uf017',
        520: u'\uf01a',
        521: u'\uf01a',
        522: u'\uf01a',
        531: u'\uf01d',
        600: u'\uf01b',
        601: u'\uf01b',
        602: u'\uf0b5',
        611: u'\uf017',
        612: u'\uf017',
        615: u'\uf017',
        616: u'\uf017',
        620: u'\uf017',
        621: u'\uf01b',
        622: u'\uf01b',
        701: u'\uf014',
        711: u'\uf062',
        721: u'\uf0b6',
        731: u'\uf063',
        741: u'\uf014',
        761: u'\uf063',
        762: u'\uf063',
        771: u'\uf011',
        781: u'\uf056',
        800: u'\uf00d',
        801: u'\uf011',
        802: u'\uf011',
        803: u'\uf012',
        804: u'\uf013',
        900: u'\uf056',
        901: u'\uf01d',
        902: u'\uf073',
        903: u'\uf076',
        904: u'\uf072',
        905: u'\uf021',
        906: u'\uf015',
        957: u'\uf050',
    }

