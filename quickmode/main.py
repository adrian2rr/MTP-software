from utils.transceiver import transceiver
from utils.ledManager import ledManager
from utils.switchManager import switchManager
import time

# Get arguments and initialize transceiver
try:
    args = get_args()
    config = process_config(args.config)

except:
    print("missing or invalid arguments")
    exit(0)
transceiver = transceiver(config.document_path, config.timeout_time)
# Initialize switches and leds
switches = switchManager()
led = ledManager()

# Reset timeouts for selecting modes and functions
mode_timeout = 0
function_timeout = 0

# Select mode
while(mode_timeout == 0):
    if(switches.getSwitch0):
        print('Short Range mode')
        mode = 0
        time.sleep(5)
        if(switches.getSwitch0):
            mode_timeout = 1
            led.blue()
    else:
        print('Midle Range mode')
        mode = 1
        time.sleep(5)
        if not (switches.getSwitch0):
            mode_timeout = 1
            led.green()

# Select function
while(function_timeout == 0):
    if(switches.getSwitch1):
        print('Receiver')
        function = 0
        time.sleep(5)
        if(switches.getSwitch1):
            function_timeout = 1
            led.red()
            transceiver.receive(mode)
    else:
        print('Transmitter')
        function = 1
        time.sleep(5)
        if not (switches.getSwitch1):
            function_timeout = 1
            led.yellow()
            transceiver.transmit(mode)




