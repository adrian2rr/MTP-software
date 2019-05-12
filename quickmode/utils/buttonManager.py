import RPi.GPIO as GPIO
from utils.ledManager import ledManager
import time


class buttonManager:
    def __init__(self):
        self.timeout = 5000
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(26, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.led = ledManager()
        self.button_pressed = True

    def getMode(self):
        millis = lambda: int(round(time.time() * 1000))
        mode = -1
        end = False
        self.waitPressed()
        self.led.white()
        start_waiting = millis()
        while(not end):
            if(GPIO.input(26) == GPIO.LOW):
                self.button_pressed = True
                while(self.button_pressed):
                    if(GPIO.input(26) == GPIO.HIGH):
                        self.button_pressed = False  
                start_waiting = millis()
                mode =(mode+1)%3
                if(mode == 0):
                    self.led.red()
                    print('Short Range mode')
                if(mode == 1):
                    self.led.blue()
                    print('Mid Range mode')
                if(mode == 2):
                    self.led.green()
                    print('Network mode')
            if(millis() - start_waiting > self.timeout):
                end = True
                self.led.off()
                print('Mode selected')
        return mode

    def getFunction(self):
        return GPIO.input(19)

    def example(self):
      while True:
          print(GPIO.input(19))
          time.sleep(0.3)

    def waitPressed(self):
        end = False
        while(not end):
            if(GPIO.input(26) == GPIO.LOW):
                 end = True
                 self.button_pressed = True  
                 print('Button pressed waiting for it to be unpressed')
                 while(self.button_pressed):
                     if(GPIO.input(26) == GPIO.HIGH):
                         self.button_pressed = False
