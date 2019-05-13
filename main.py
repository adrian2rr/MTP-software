from utils.config import get_args, process_config
from utils.ledManager import ledManager
from utils.buttonManager import buttonManager
from window import Window
from network_mode.network_mode import start as network_mode_start
from RF24 import *

config = None
args = None
# Get arguments and initialize transceiver
try:
    args = get_args()
    config = process_config(args.config)
    config.update({
        "Tx_CS": RPI_V2_GPIO_P1_15,
        "Tx_CSN": BCM2835_SPI_CS1,
        "Rx_CS": RPI_V2_GPIO_P1_13,
        "Rx_CSN": BCM2835_SPI_CS0})
except:
    print("missing or invalid arguments")
    exit(0)


# Initialize buttons and leds
buttons = buttonManager()
led = ledManager()

# Define end condition variables
end = False

while not end:
    # Turn off led 
    led.off()
    # Select mode
    # mode = buttons.getMode()
    mode = 2
    if mode == 0:
        print('Short Range mode selected')
        window = Window.Window(args.config, 2, led)
    if mode == 1:
        print('Midle Range mode selected')
        window = Window.Window(args.config, 1, led)
    if mode == 2:
        print('Network mode selected')
        network_mode_start('tx', led, config)

    # Select function
    function = buttons.getFunction()
    # function = False
    if not function:
        print('Receiver')
        buttons.waitPressed()
        print('Start button pressed')
        led.white()
        window.rx()
        end = True

    if function:
        print('Transmitter')
        buttons.waitPressed()
        print('Start button pressed')
        led.white()
        window.tx()
        end = True

# Set transmission finished led
led.yellow()
