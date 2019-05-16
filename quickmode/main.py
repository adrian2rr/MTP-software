from utils import ledManager, buttonManager
from window.utils import get_args

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
end = False

while(not end):
    # Turn off led 
    led.off()
    # Select mode
    mode = buttons.getMode()
    #mode = 0
    if(mode == 0):
        print('Short Range mode selected')
        window = Window.Window(args.config, 2)
    if(mode == 1):
        print('Midle Range mode selected')
        window = Window.Window(args.config, 1)
    if(mode == 2):
        print('Network mode selected: not implemented')

    # Select function
    function = buttons.getFunction()
    #function = False
    if(not function):
        print('Receiver')
        buttons.waitPressed()
        print('Start button pressed')
        led.white()
        window.rx()
        end = True
    if(function):
        print('Transmitter')
        buttons.waitPressed()
        print('Start button pressed')
        led.white()
        window.tx()
        end = True

# Set transmission finished led
led.yellow

