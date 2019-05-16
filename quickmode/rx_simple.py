from __future__ import print_function
import time
from RF24 import *

from utils import configure_radios
from utils import get_args, process_config
from utils import PacketManagerAck

########### USER CONFIGURATION ###########
# See https://github.com/TMRh20/RF24/blob/master/pyRF24/readme.md

# CE Pin, CSN Pin, SPI Speed

# Setup for GPIO 22 CE and CE0 CSN with SPI Speed @ 8Mhz
#radio = RF24(RPI_V2_GPIO_P1_15, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_8MHZ)

#RPi B
# Setup for GPIO 15 CE and CE1 CSN with SPI Speed @ 8Mhz
#radio = RF24(RPI_V2_GPIO_P1_15, BCM2835_SPI_CS0, BCM2835_SPI_SPEED_8MHZ)

#RPi B+
# Setup for GPIO 22 CE and CE0 CSN for RPi B+ with SPI Speed @ 8Mhz
#radio = RF24(RPI_BPLUS_GPIO_J8_15, RPI_BPLUS_GPIO_J8_24, BCM2835_SPI_SPEED_8MHZ)

# RPi Alternate, with SPIDEV - Note: Edit RF24/arch/BBB/spi.cpp and  set 'this->device = "/dev/spidev0.0";;' or as listed in /dev


# Setup for connected IRQ pin, GPIO 24 on RPi B+; uncomment to activate
#irq_gpio_pin = RPI_BPLUS_GPIO_J8_18
#irq_gpio_pin = 24

try:
    args = get_args()
    config = process_config(args.config)

except:
    print("missing or invalid arguments")
    exit(0)

millis = lambda: int(round(time.time() * 1000))

print('Quick Mode script! ')

print('RX Role:Pong Back, awaiting transmission')

channel_RX = 60
channel_TX = 75
payload_size = config.payload_size

radio_tx, radio_rx = configure_radios(channel_TX, channel_RX,0)

radio_rx.startListening()
radio_tx.stopListening()
#radio_rx.printDetails()
frames = {}
last_packet = False
num_packets = 0
ACK = 0
NACK = 1
packet_manager_ack = PacketManagerAck()
# forever loop
while 1:  
    # Pong back role.  Receive each packet, dump it out, and send ACK
    if radio_rx.available():
        while radio_rx.available():
            #First check of the payload
            len = radio_rx.getDynamicPayloadSize()
            receive_payload = radio_rx.read(radio_rx.getDynamicPayloadSize())
            print('Got payload size={} value="{}"'.format(payload_size, receive_payload.decode('utf-8')))

            # Check if the id is correct
            frame_id = int.from_bytes(receive_payload[1:2],byteorder='big')
            print(frame_id)
            if last_packet:
                frames.update({str(frame_id): receive_payload[4:]})
            # If it is correct, update the collection            
            elif frame_id == 0 or len(frames) == frame_id:
                frames.update({str(frame_id): receive_payload[4:]})
            # If it is not correct, update the collection with empty
            else:
                while (len(frames)+1) != frame_id:
                    if len(frames) == frame_id:
                        frames.update({str(frame_id): receive_payload[4:]})
                    else:
                        frames.update({str(len(frames)+1): None})

            # Check if it is last packet
            if receive_payload[3] is 1:
                last_packet = True

            # If it is not the last packet it sends an ack
            if not last_packet:
                packet_ack = packet_manager_ack.create(ACK)
                radio_tx.write(packet_ack)
                print('Sent response.')
                pass
            else:
                # Check all packets are sent correctly
                for id_frame, value in frames:
                    if frames[id_frame] is None:
                        packet_ack = packet_manager_ack.create(NACK,id_frame)
                        radio_tx.write(packet_ack)
                        print('Some packet missing.')
                        break
                    else:
                        num_packets += 1

            if last_packet and len(frames) == num_packets:
                print('Reception complete.')
                
