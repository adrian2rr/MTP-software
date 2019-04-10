from __future__ import print_function
import time
from RF24 import *

from utils.packet_manager import PacketManager
from utils.radio import configure_radios
from utils.config import get_args, process_config

irq_gpio_pin = None

########### USER CONFIGURATION ###########
# See https://github.com/TMRh20/RF24/blob/master/pyRF24/readme.md

# CE Pin, CSN Pin, SPI Speed

# Setup for GPIO 22 CE and CE0 CSN with SPI Speed @ 8Mhz
# radio = RF24(RPI_V2_GPIO_P1_15, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_8MHZ)

# RPi B
# Setup for GPIO 15 CE and CE1 CSN with SPI Speed @ 8Mhz
# radio = RF24(RPI_V2_GPIO_P1_15, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_8MHZ)

# RPi B+
# Setup for GPIO 22 CE and CE0 CSN for RPi B+ with SPI Speed @ 8Mhz
# radio = RF24(RPI_BPLUS_GPIO_J8_15, RPI_BPLUS_GPIO_J8_24, BCM2835_SPI_SPEED_8MHZ)

# RPi Alternate, with SPIDEV - Note: Edit RF24/arch/BBB/spi.cpp and  set 'this->device = "/dev/spidev0.0";;' or as listed in /dev


# Setup for connected IRQ pin, GPIO 24 on RPi B+; uncomment to activate
# irq_gpio_pin = RPI_BPLUS_GPIO_J8_18
# irq_gpio_pin = 24

try:
    args = get_args()
    config = process_config(args.config)

except:
    print("missing or invalid arguments")
    exit(0)

millis = lambda: int(round(time.time() * 1000))

print('Quick Mode script! ')

print('TX Role: Ping Out, starting transmission')

channel_TX = 60
channel_RX = 75
payload_size = config.payload_size

radio_tx, radio_rx = configure_radios(channel_TX, channel_RX,1)

packet_manager = PacketManager(config.document_path)
packets = packet_manager.create()
print(packets[0])

radio_rx.startListening()
radio_tx.stopListening()

# loop over the packets to be sent
i=0
for packet in packets:
    # Take the time, and send it.  This will block until complete
    # print('Now sending message: {} ... '.format(packet), end="")
    radio_tx.write(packet)
    i+=1
    if(i>=100):
        break
    # Now, continue listening

    radio_rx.startListening()
    
    # Wait here until we get a response, or timeout
    started_waiting_at = millis()
    timeout = False
    retransmit = False
    num_retransmissions = 0
    ack_received = False

    while not ack_received:
        while (not radio_rx.available()) and (not timeout):
            if (millis() - started_waiting_at) > int(config.timeout_time):
                timeout = True
        # In case of time out: Resend
        if timeout:
            print('failed, response timed out.')
            num_retransmissions += 1
            print("Timeout --> resending message")
            print("Retransmission number {}".format(num_retransmissions))
            radio_tx.write(packet)
            timeout = False			
        else:
            # Grab the response
            ack = radio_rx.read(3)
            print('got response:')
            #  Analyze ACK
            if ack[0] == 0:
                print("ACK Received --> transmit the next packet")
                ack_received = True
                num_retransmissions = 0
            else:
                print("NACK - Message Lost --> retransmission required")
                frame_id = int.from_bytes(ack[1:2],byteorder='big')
                radio_tx.write(ack[frame_id])        



