import RPi.GPIO as GPIO

pin_green = 20
# pin_green = 19
pin_blue = 16
# pin_blue = 26
pin_red = 21


class LedManager:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(pin_blue, GPIO.OUT)
        GPIO.setup(pin_green, GPIO.OUT)
        GPIO.setup(pin_red, GPIO.OUT)
        self.state = 0

    def off(self):
        if self.state != 0:
            self.state = 0
            GPIO.output(pin_blue, GPIO.LOW)
            GPIO.output(pin_green, GPIO.LOW)
            GPIO.output(pin_red, GPIO.LOW)

    def green(self):
        if self.state != 1:
            self.off()
            self.state = 1
            GPIO.output(pin_green, GPIO.HIGH)

    def blue(self):
        if self.state != 2:
            self.off()
            self.state = 2
        GPIO.output(pin_blue, GPIO.HIGH)

    def red(self):
        if self.state != 3:
            self.off()
            self.state = 3
        GPIO.output(pin_red, GPIO.HIGH)

    def blue_green(self):
        if self.state != 4:
            self.off()
            self.state = 4
        GPIO.output(pin_green, GPIO.HIGH)
        GPIO.output(pin_blue, GPIO.HIGH)

    def violet(self):
        if self.state != 5:
            self.off()
            self.state = 5
        GPIO.output(pin_blue, GPIO.HIGH)
        GPIO.output(pin_red, GPIO.HIGH)

    def yellow(self):
        if self.state != 6:
            self.off()
            self.state = 6
        GPIO.output(pin_red, GPIO.HIGH)
        GPIO.output(pin_green, GPIO.HIGH)

    def white(self):
        if self.state != 7:
            self.off()
            self.state = 7
        GPIO.output(pin_blue, GPIO.HIGH)
        GPIO.output(pin_green, GPIO.HIGH)
        GPIO.output(pin_red, GPIO.HIGH)

    def network_starting(self):
        self.violet()

    def network_tx(self):
        self.yellow()

    def network_rx(self):
        self.blue()

    def network_error(self):
        self.red()

    def network_success(self):
        self.green()
