import RPi.GPIO as GPIO

# pin_green = 20
pin_green = 19
# pin_blue = 16
pin_blue = 26
pin_red = 21


class ledManager:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(pin_blue, GPIO.OUT)
        GPIO.setup(pin_green, GPIO.OUT)
        GPIO.setup(pin_red, GPIO.OUT)

    def off(self):
        GPIO.output(pin_blue, GPIO.LOW)
        GPIO.output(pin_green, GPIO.LOW)
        GPIO.output(pin_red, GPIO.LOW)

    def green(self):
        self.off()
        GPIO.output(pin_green, GPIO.HIGH)

    def blue(self):
        self.off()
        GPIO.output(pin_blue, GPIO.HIGH)

    def red(self):
        self.off()
        GPIO.output(pin_red, GPIO.HIGH)

    def blueGreen(self):
        self.off()
        GPIO.output(pin_green, GPIO.HIGH)
        GPIO.output(pin_blue, GPIO.HIGH)

    def violet(self):
        self.off()
        GPIO.output(pin_blue, GPIO.HIGH)
        GPIO.output(pin_red, GPIO.HIGH)

    def yellow(self):
        self.off()
        GPIO.output(pin_red, GPIO.HIGH)
        GPIO.output(pin_green, GPIO.HIGH)

    def white(self):
        self.off()
        GPIO.output(pin_blue, GPIO.HIGH)
        GPIO.output(pin_green, GPIO.HIGH)
        GPIO.output(pin_red, GPIO.HIGH)

    def network_starting(self):
        self.off()
        self.violet()

    def network_tx(self):
        self.off()
        self.yellow()

    def network_rx(self):
        self.off()
        self.blue()

    def network_error(self):
        self.off()
        self.red()

    def network_success(self):
        self.off()
        self.green()
