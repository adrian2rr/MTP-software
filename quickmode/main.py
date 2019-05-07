from utils.transceiver import transceiver
from utils.ledManager import ledManager
from utils.buttonManager import buttonManager


# Get arguments and initialize transceiver
try:
    args = get_args()
    config = process_config(args.config)

except:
    print("missing or invalid arguments")
    exit(0)
transceiver = transceiver(config.document_path, config.timeout_time)
# Initialize buttons and leds
buttons = buttonManager()
led = ledManager()

# Define end condition variables
chek_mode = True
end = False

while(not end):
    # Set ready led
    led.white()

    # Select mode
    mode = buttons.getMode()
    if(mode == 0):
        print('Short Range mode')
        led.red()
        end
    elif(mode == 1):
        print('Midle Range mode')
        led.green()
    elif(mode == 2):
        print('Network mode: not implemented')
        led.blue()
    else:
        chek_mode = False

    # Select function
    function = buttons.getFunction()
    if(function == 0 and chek_mode):
        print('Receiver')
        transceiver.receive(mode)
        end = True
    if(function == 1):
        print('Transmitter')
        transceiver.transmit(mode)
        end = True

# Set transmission finished led
led.yellow




