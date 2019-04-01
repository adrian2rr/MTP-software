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

radio_tx, radio_rx = configure_radios()


packet_manager = PacketManager(config.document_path)
packets = packet_manager.create()

# loop over the packets to be sent
for packet in packets:
    # First, stop listening so we can talk.
    radio_tx.stopListening()

    # Take the time, and send it.  This will block until complete
    print('Now sending message: {} ... '.format(packet), end="")
    radio_tx.write(packet)

    # Now, continue listening
    radio_tx.startListening()

    # Wait here until we get a response, or timeout
    started_waiting_at = millis()
    timeout = False
    retransmit = False
    num_retransmissions = 0
    ack_received = False

    while not ack_received:
        while (not radio_tx.available()) and (not timeout):
            if (millis() - started_waiting_at) > config.timeout_time:
                timeout = True

        # Describe the results
        if timeout:
            print('failed, response timed out.')
            retransmit = True
        else:
            # Grab the response, compare, and send to debugging spew
            len = radio_tx.getDynamicPayloadSize()
            ack = radio_tx.read(len)

            # Spew it
            print('got response: {}'.format(len, ack.decode('utf-8')))
            if ack.decode('utf-8') == "ACK":
                print("ACK Received --> transmit the next packet")
                retransmit = False
                ack_received = True
            else:
                print("NACK - Message Lost --> retransmission required")
                retransmit = True

        if retransmit:
            num_retransmissions += 1
            print("Timeout or NACK received --> resending message")
            print("Retransmission number {}".format(num_retransmissions))
            radio_tx.write(packet)


