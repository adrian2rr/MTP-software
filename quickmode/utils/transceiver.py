from __future__ import print_function
from packet_manager_simple import PacketManager
from ledManager import ledManager
from radio import configure_radios
import time
import zlib


class transceiver(object):
    def __init__(self, document_path, timeout_time = 0, compression = True):
        self.timeout_time = timeout_time
        self.document_path = document_path
        self.compression = compression
    
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
        packets = packet_manager.create_window()

        # We'll have tot_packets/WINDOW_SIZE windows sent, in each window we'll send WINDOW_SIZE packets
        tot_packets = len(packets)
        window_counter = 0
        WINDOW_SIZE = 31 # TODO: Put in config file
        window = 31
        if(tot_packets%WINDOW_SIZE==0):
            rang = tot_packets//WINDOW_SIZE
        else:
            rang = tot_packets//WINDOW_SIZE+1

        # Iterate each window
        for window_counter in range(rang):
            print(window)
            if (tot_packets/WINDOW_SIZE-window_counter<1):
                window = (tot_packets-(window_counter)*WINDOW_SIZE)
                print("Window")
                print(window)

            print("-----------------------------------------------------")
            print("Sending window " + str(window_counter))
            
            # rx_acks => remaining packets to send
            rx_acks = 0 
            rx_acks_bools = [0] * window # 0 if the receiver has not received the packet, 1 if the receiver has sent ACK
            timeout = False
            
            # si ha saltado el timeout o el numbero de acks recibidos es menor que la window size tendra que enviar 
            while( (rx_acks < window) or (timeout) ): 
                timeout = False
                for packet_index in range(len(rx_acks_bools)):
                    if(rx_acks_bools[packet_index] == 0):
                        radio_tx.write(packets[window_counter * WINDOW_SIZE + packet_index])
                        print("tx packet " + str(window_counter*WINDOW_SIZE+packet_index))

                # Once it has sent all the packets in the window check ACK and checks the timeout
                started_waiting_at = millis()
                while (not radio_rx.available()) and (not timeout):
                    if (millis() - started_waiting_at) > int(self.timeout_time):
                        timeout = True
                        started_waiting_at = millis()
                        
                if(timeout):
                    print("Ha saltado el timeout")
                else:
                    # Check ACK
                    print("I listen to ACK")
                    ack = radio_rx.read(radio_rx.getDynamicPayloadSize())
                    # Some packets are wrong, they will send the ones that are good
                    print("Received ACK = ")
                    print((ack))
                    for ack_idx in ack[1:window+1]:
                        if(rx_acks_bools[ack_idx] == 0 and ack[0] == window_counter%2):
                            # It was wrong and not is OK
                            print("Packet " + str(ack_idx) + " correct")
                            rx_acks += 1
                            rx_acks_bools[ack_idx] = 1
                    print("ACKS array")
                    print(rx_acks_bools)
                    wrong_packets = window - rx_acks
                    print("Wrong packets " + str(wrong_packets))

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
        WINDOW_SIZE = 31
        data_size = 31
        loop = True
        window_old = -1
        ack_old = False
        last_packet = False
        rx_id_old = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

        while loop:
            if(radio_rx.available()):
                # Set window variables
                rx_id = [0]      # The receiver will check this after receiving a window. Example: [0, 1, 2, 4, 6] --> I have to ask for retx of pkt 3 and 5
                window_bytes = [0] * WINDOW_SIZE * data_size
                end_of_window = False
                last_window = 32
                ack_sent = False

                while(not end_of_window):
                    while(radio_rx.available()):

                        # First check of the payload
                        length = radio_rx.getDynamicPayloadSize()
                        receive_payload = radio_rx.read(length)
                        # now process rx_payload
                        header = receive_payload[0]
                        window = 0x40 & header
                        frame_id = int(0x3f & header)
                        rx_id[0] = window // 64

                        print("Received packet id: " + str(frame_id) + " window: " + str(window) + " window old: " + str(window_old))
                        # print(receive_payload[1:])
                        if(window != window_old):

                            if(header > 127):
                                # This means that eot = 1, the header field will be something like = 1XXX XXXX so it will be > 127
                                last_packet = True
                                last_window = int(frame_id)
                                print("EOT!")
                                if(frame_id not in rx_id[1:]):
                                    rx_id.append(frame_id)
                                    ack_sent = False
                                last_packet_size = len(receive_payload)
                                window_bytes[frame_id * data_size:frame_id * data_size + last_packet_size - 1] = receive_payload[1:]
                            else:
                                if(frame_id not in rx_id[1:]):
                                    rx_id.append(frame_id)
                                    ack_sent = False

                                window_bytes[frame_id * data_size:frame_id * data_size + len(receive_payload) - 1] = receive_payload[1:]
                            if((len(rx_id) == WINDOW_SIZE + 1) or (len(rx_id) == last_window + 2)):
                                end_of_window = True

                                rx_id_old = rx_id

                        else:
                            ack_old = True


                    # send correct ids (rx_id)

                    rx_id_1 = [rx_id[0]]
                    rx_id_2 = rx_id[1:]
                    rx_id_2.sort()
                    rx_id_1.extend(rx_id_2)
                    rx_id = rx_id_1

                    if((len(rx_id) > 1 and rx_id[-1] == (WINDOW_SIZE - 1) and not ack_sent) or (len(rx_id) > 1 and rx_id[-1] == last_window and not ack_sent) and not ack_old):

                        radio_tx.write(bytes(rx_id))
                        print("Sent ACK: " + str(rx_id))
                        ack_sent = True


                    if (ack_old):
                        if(last_packet):
                            rx_id_old = rx_id_old[:last_window + 2]

                        radio_tx.write(bytes(rx_id_old))
                        print("Sent ACK old: " + str(rx_id_old))
                        ack_old = False


                # Once all the window is received correctly, store the packets
                if(len(rx_id) == WINDOW_SIZE + 1):
                    frames.extend(bytes(window_bytes))

                    print("End of window " + str(window) + ", packet saved")
                    window_old = window

                if(len(rx_id) == last_window + 2):
                    frames.extend(bytes(window_bytes[:(last_window) * data_size + last_packet_size - 1]))

                    print("End of window " + str(window) + ", packet saved")
                    window_old = window
                # If it is the last packet save the txt


                if last_packet and len(rx_id) == last_window + 2:
                    # led.green()
                    print('Reception complete.')
                    # If we are here it means we received all the frames so we have to uncompress

                    if self.compression:
                        uncompressed_frames = zlib.decompress(bytes(frames))

                        f = open('file' + str(num_file) + '.txt', 'wb')
                        f.write(bytes(uncompressed_frames))
                        f.close()
                        print('File saved with name: ' + 'file' + str(num_file) + '.txt')
                    else:
                        f = open('file' + str(num_file) + '.txt', 'wb')
                        f.write(bytes(frames))
                        f.close()
                        print('File saved with name: ' + 'file' + str(num_file) + '.txt')
                    frames = []
                    last_packet = False
                    num_packets = 0
                    num_file += 1
                    input('Press Enter to finish')
                    led.off()
                    loop = 0
