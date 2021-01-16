import os
from datetime import datetime
from PIL import Image, ImageFont, ImageDraw

class TimeWidget():
    def __init__(self):
        self.font =  ImageFont.truetype(os.path.join('./fonts/', 'DejaVuSansMono-Bold.ttf'), 24)

    def get_time(self):
        now = datetime.now()
        img = Image.new('1', (512, 64), color=255)
        imgdraw = ImageDraw.Draw(img)
        imgdraw.text((32, 24), '%s, %2d/%2d/%4d' % (self.weekdays[now.isoweekday()], now.day, now.month, now.year), font=self.font, fill=0)
        imgdraw.text((400, 24), '%02d:%02d' % (now.hour, now.minute), font=self.font, fill=0)
        return img

    weekdays = ['None', 'Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
