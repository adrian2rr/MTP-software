from utils.ledManager import ledManager
from utils.buttonManager import buttonManager
from utils.config import get_args
import Window

# Get arguments and initialize transceiver
try:
    args = get_args()
    #config = process_config(args.config)

except:
    print("missing or invalid arguments")
    exit(0)


# Initialize buttons and leds
buttons = buttonManager()
led = ledManager()

# Define end condition variables
check_mode = True
end = False

while(not end):
    # Set ready led
    led.white()

    # Select mode
    # mode = buttons.getMode()
    mode = 0
    if(mode == 0):
        print('Short Range mode')
        window = Window.Window(args.config, 2)

        led.red()
        end
    elif(mode == 1):
        print('Midle Range mode')
        window = Window.Window(args.config, 1)

        led.green()
    elif(mode == 2):
        print('Network mode: not implemented')
        led.blue()
    else:
        check_mode = False

    # Select function
    # function = buttons.getFunction()
    function = 0
    if(function == 0 and check_mode):
        print('Receiver')
        window.rx()
        end = True
    if(function == 1 and check_mode):
        print('Transmitter')
        window.tx()
        end = True

# Set transmission finished led
led.yellow
