from datetime import datetime
import RPi.GPIO as GPIO
import time

row_channels = [6, 5, 19, 13]
column_channel = 26

class GPIODriver():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(row_channels, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(column_channel, GPIO.OUT)

    def wait_for_keypress(self, timeout=60):
        self.pressed = None

        def callback_1(channel):
            # print("Pressed key 1")
            self.pressed = 1

        def callback_2(channel):
            # print("Pressed key 2")
            self.pressed = 2

        def callback_3(channel):
            # print("Pressed key 3")
            self.pressed = 3

        def callback_4(channel):
            # print("Pressed key 4")
            self.pressed = 4

        GPIO.add_event_detect(row_channels[0], GPIO.RISING, callback=callback_1, bouncetime=500)
        GPIO.add_event_detect(row_channels[1], GPIO.RISING, callback=callback_2, bouncetime=500)
        GPIO.add_event_detect(row_channels[2], GPIO.RISING, callback=callback_3, bouncetime=500)
        GPIO.add_event_detect(row_channels[3], GPIO.RISING, callback=callback_4, bouncetime=500)
        GPIO.output(column_channel, GPIO.HIGH)
        start_time = datetime.now()
        while not self.pressed:
            time.sleep(1)
            current_time = datetime.now()
            delta = current_time - start_time
            if delta.seconds > timeout:
                for chan in row_channels:
                    GPIO.remove_event_detect(chan)
                GPIO.output(column_channel, GPIO.LOW)
                return None            

        for chan in row_channels:
            GPIO.remove_event_detect(chan)
        GPIO.output(column_channel, GPIO.LOW)
        return self.pressed
