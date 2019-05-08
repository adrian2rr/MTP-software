import RPi.GPIO as GPIO
import time

class buttonManager:
    def __init__(self):
        self.timeout = 3000
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(29,GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.setup(31,GPIO.IN, pull_up_down = GPIO.PUD_UP)

    def getMode(self):
        millis = lambda: int(round(time.time() * 1000))
        mode = -1
        end = False
        while(end):
            if(not GPIO.input(29)):
                if(mode == -1):
                    start_waiting = millis()
                mode =+1
            if(millis()-start_waiting > self.timeout):
                end = True
        return mode

    def getFunction(self):
        return GPIO.input(31)
