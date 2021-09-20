import os
from datetime import datetime
from pyowm import OWM
from PIL import Image, ImageFont, ImageDraw

def get_local_ip():
    import socket
    """Try to determine the local IP address of the machine."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # Use Google Public DNS server to determine own IP
        sock.connect(('192.168.1.1', 80))

        return sock.getsockname()[0]
    except socket.error:
        try:
            return socket.gethostbyname(socket.gethostname())
        except socket.gaierror:
            return '127.0.0.1'
    finally:
        sock.close()

class CalendarWidget():
    def __init__(self, column_names):
        self.column_names = column_names
        self.font14 =  ImageFont.truetype(os.path.join('./fonts/', 'DejaVuSansMono-Bold.ttf'), 14)

    def create_entry_box(self, inittime, finishtime, text, width):
        """
        both inittime and finishtime are objects of type datetime.datetime
        """ 
        timediff = finishtime - inittime
        hours = timediff.seconds / 3600

        img = Image.new('1', (width, int(hours * 20)), color=0)
        imgdraw = ImageDraw.Draw(img)
        imgdraw.text((8, 0), text, font=self.font14, fill=255)
        return img

    def get_calendar(self, column_events, title=None):
        """
        column_events contains a list of columns, and each of them is a list of hashes containing:
            - event_start: start time
            - event_end:   ending time
            - event_title: event title
        """
        img = Image.new('1', (640, 304), color=255)
        img2 = Image.new('1', (640, 304), color=255)
        imgdraw = ImageDraw.Draw(img)
        imgdraw2 = ImageDraw.Draw(img2)
        index = 0
        distance = 540 // len(self.column_names)
        boxwidth = 570 // len(self.column_names)

        for column in self.column_names:
            imgdraw.text((128 + distance*index, 0), column, font=self.font14, fill=0)
            index += 1
        if title:
            imgdraw.text((8, 0), title, font=self.font14, fill=0)
        imgdraw.text((540, 294), get_local_ip())

        # Draw Calendar lines
        for i in range(0, 14):
            imgdraw2.line([(0,30 + 20*i), (639, 30 + 20*i)], fill=0, width=1)
        for i in range(0, 14):
            imgdraw.text((0, 30 + 20*i), '%2d:00' % (i+8), font=self.font14, fill=0)

        column_number = 0
        for column_list in column_events:
            for event in column_list:
                if event['event_start'].hour >= 8 and event['event_start'].hour <= 21:
                    eventimg = self.create_entry_box(event['event_start'],
                                                     event['event_end'],
                                                     event['event_title'],
                                                     boxwidth)
                    x = column_number + 64 + (boxwidth * column_number)
                    y = 30 + int(20 * (event['event_start'].hour + (event['event_start'].minute / 60) - 8.0))
                    img2.paste(eventimg, box = (x, y))
            column_number += 1
        return img, img2
