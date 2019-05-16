from utils.config import get_args, process_config
from utils.LedManager import LedManager
from utils.ButtonManager import ButtonManager
from window.Window import Node as window
from network_mode.network_mode import start as network_mode_start
from RF24 import *
import logging
import subprocess
import time

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
        "Rx_CSN": BCM2835_SPI_CS0,
        "Log_Level": logging.CRITICAL,
        "json_path": '/home/pi/mtp_software/network_mode/config.json'
    })
except:
    print("missing or invalid arguments")
    exit(0)


# Initialize buttons and leds
buttons = ButtonManager()
led = LedManager()

# Define end condition variables
end = False

while not end:

    if buttons.start:
        led.off()
        if buttons.mode == 0:
            window = window(config, led, buttons.role)
            window.start()
        elif buttons.mode == 1:
            network_mode_start(buttons.role, led, config)
            time.sleep(4)
        elif buttons.mode == 2:
            end = True
        buttons.start = False

    else:
        if buttons.enter:
            if buttons.mode == 2:
                led.green()
            else:
                if buttons.role == 'tx':
                    led.yellow()
                else:
                    led.blue()
        else:
            if buttons.mode == 0:
                led.violet()
            elif buttons.mode == 1:
                led.white()
            elif buttons.mode == 2:
                led.red()

led.red()
subprocess.call(["sudo", "poweroff"])
