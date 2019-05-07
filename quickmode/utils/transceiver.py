from __future__ import print_function
import time

from packet_manager_simple import PacketManager
from config import get_args, process_config
from ledManager import ledManager
from radio import configure_radios

# try:
    # args = get_args()
    # config = process_config(args.config)

# except:
    # print("missing or invalid arguments")
    # exit(0)

class transceiver(object):
    def __init__(self, document_path, timeout_time = 0, payload_size =32):
        self.timeout_time = timeout_time
        self.document_path = document_path
        self.payload_size = payload_size
    
    def transmit(self, mode):
        millis = lambda: int(round(time.time() * 1000))

        print('TX Role: Ping Out, starting transmission')

        # Set led Manager
        led = ledManager()
        led.red()

        # Define comunication parameters
        channel_TX = 60
        channel_RX = 70

        # Start radios
        if (mode == 0):
            radio_tx, radio_rx = configure_radios(channel_TX, channel_RX,1,1)
        else:
            radio_tx, radio_rx = configure_radios(channel_TX, channel_RX,1,0)

        radio_rx.startListening()
        radio_tx.stopListening()

        # Create packets
        packet_manager = PacketManager(self.document_path)
        packets = packet_manager.create()

        #Define loop variables

        # loop over the packets to be sent
        led.violet()
        i=0
        for packet in packets:
            #Send the packet
            radio_tx.write(packet)
            print('Sending packet {}'.format(i))
            i+=1

            # Reset variables

            timeout = False
            num_retransmissions = 0
            ack_received = False

            while not ack_received:
                # Start timing
                started_waiting_at = millis()
                while (not radio_rx.available()) and (not timeout):
                    if (millis() - started_waiting_at) > int(self.timeout_time):
                        timeout = True
                # In case of time out: Resend
                if timeout:
                    led.yellow()
                    print('failed, response timed out.')
                    num_retransmissions += 1
                    print("Timeout --> resending message")
                    print("Retransmission number {}".format(num_retransmissions))
                    radio_tx.write(packet)
                    timeout = False
                else:
                    led.violet()
                    # Grab the response
                    ack = radio_rx.read(1)
                    print('got response:{}'.format(ack))
                    #  Analyze ACK
                    if ack == bytes([0]):
                        print("ACK Received --> transmit the next packet")
                        ack_received = True

        led.off()

    def receive(self, mode):
        print('RX Role:Pong Back, awaiting transmission')

        # Set led Manager
        led = ledManager()
        led.red()

        # Set comunication parameters
        channel_RX = 60
        channel_TX = 70

        # Initialize radio
        if (mode == 0):
            radio_tx, radio_rx = configure_radios(channel_TX, channel_RX,0,1)
        else:
            radio_tx, radio_rx = configure_radios(channel_TX, channel_RX,0,0)
        
        radio_rx.startListening()
        radio_tx.stopListening()

        # Create local variables
        frames = []
        last_packet = False
        num_file = 0

        led.blue()
        loop = 1
        packet_number = 0

        # forever loop
        while loop:

            # Pong back role.  Receive each packet, dump it out, and send ACK
            if radio_rx.available():
                while radio_rx.available():
                    #First check of the payload
                    receive_payload = radio_rx.read(radio_rx.getDynamicPayloadSize())
                    #print('Got payload eot={} value="{}"'.format(receive_payload[0], receive_payload[1:31].decode('utf-8')))
                    
                    # Save it if is not a duplicate packet
                    print('received_payload'+str(receive_payload[0]))
                    if receive_payload[0] == packet_number:
                        packet_number = (packet_number+1)%2
                        print('packet number'+str(packet_number))
                        # Append the information
                        frames += receive_payload[2:]
                    
                    # Check if it is last packet            
                    if receive_payload[1] == 1:
                        print('Last packet')
                        last_packet = True

                    # Send Ack
                    radio_tx.write(bytes([0]))
                    print('Sent response.')

                    # If it is the last packet save the txt
                    if last_packet:
                        led.green()
                        print('Reception complete.')
                        f = open('file'+str(num_file)+'.txt','wb')
                        f.write(bytes(frames))
                        f.close()
                        print('File saved')
                        frames = []
                        last_packet = False
                        num_file += 1
                        input('Press Enter to finish')
                        led.off()
                        loop = 0


        
