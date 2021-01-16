from . import epd7in5bc

class EinkDriver():
    def __init__(self, xres, yres):
        self.epd = epd7in5bc.EPD()
        self.epd.init()
        self.epd.Clear()
        self.xres = xres
        self.yres = yres

    # image1: black/white image
    # image2: black/yellow image
    def display(self, image1=None, image2=None):
        self.epd.init()
        self.epd.display(self.epd.getbuffer(image1), self.epd.getbuffer(image2))
        self.epd.sleep()

    def end(self):
        print("Ending e-ink driver")
        self.epd.init()
        self.epd.Clear()
        self.epd.sleep()
        self.epd.Dev_exit()
        print("e-ink driver finished")

