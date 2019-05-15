import RPi.GPIO as GPIO
import time

switch_channel = 19
button_channel = 26


class ButtonManager:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(button_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(switch_channel, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(button_channel, GPIO.FALLING, callback=self.get_mode)
        GPIO.add_event_detect(switch_channel, GPIO.BOTH, callback=self.get_role)
        self.mode = 0
        self.enter = False
        self.role = 'tx'
        self.start = False

    def get_mode(self, channel):
        start_time = time.time()
        now_time = start_time
        while not GPIO.input(channel) and now_time - start_time < 4:
            now_time = time.time()
        if now_time - start_time >= 0.3:
            if now_time - start_time >= 4:
                self.enter = not self.enter
            else:
                if self.enter:
                    self.start = True
                else:
                    self.mode = self.mode + 1 if self.mode < 2 else 0

    def get_role(self, channel):
        self.role = 'rx' if GPIO.input(channel) else 'tx'
