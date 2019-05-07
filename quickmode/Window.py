from __future__ import print_function
import time
import zlib

from utils.packet_manager_simple import PacketManager, PacketManagerAck
from utils.radio import configure_radios
# from utils.config import get_args, process_config, payload_size
# import utils.config
from utils.ledManager import ledManager


class Window(object):

    def __init__(self):
        self.PM = PacketManager()
        self.compression = self.PM.use_compression
        self.enable_print = False
        self.millis = lambda: int(round(time.time() * 1000))
        self.led = ledManager()
        # channel1: main channel of communication, from where the payload is sent
        self.channel1 = 60
        # channel2: channel used for the acks sent from the receiving device
        self.channel2 = 70
        self.WINDOW_SIZE = self.PM.window_size
        self.data_size = self.PM.data_size
        self.fileout = "file0.txt"
        # self.config_file = "../configs/config_file.json"
        # self.config = utils.process_config(self.config_file)
        self.payload_size = self.PM.payload_size
        self.timeout_time = self.PM.config.timeout_time

    def rx(self):
        print("Started RX")
        # Initialize radio
        radio_tx, radio_rx = configure_radios(self.channel2, self.channel1, 0)
        radio_rx.startListening()
        radio_tx.stopListening()

        # Create local variables
        frames = []
        last_packet = False
        num_file = 0

        # Create Ack packet
        packet_manager_ack = PacketManagerAck()
        packet_manager_ack.create()

        self.led.blue()

        loop = True
        window_old = -1
        ack_old = False
        last_packet = False
        rx_id_old = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30]

        while loop:
            if(radio_rx.available()):
                # Set window variables
                # The receiver will check this after receiving a window. Example: [0, 1, 2, 4, 6] --> I have to ask for retx of pkt 3 and 5
                rx_id = [0]
                window_bytes = [0] * self.WINDOW_SIZE * self.data_size
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
                        if(self.enable_print):
                            print("Received packet id: " + str(frame_id) + " window: " + str(window) + " window old: " + str(window_old))
                            # print(receive_payload[1:])
                        if(window != window_old):
                            if(header > 127):
                                # This means that eot = 1, the header field will be something like = 1XXX XXXX so it will be > 127
                                last_packet = True
                                last_window = int(frame_id)
                                if(self.enable_print):
                                    print("EOT!")

                                if(frame_id not in rx_id[1:]):
                                    rx_id.append(frame_id)
                                    ack_sent = False
                                last_packet_size = len(receive_payload)
                                window_bytes[frame_id * self.data_size:frame_id * self.data_size + last_packet_size - 1] = receive_payload[1:]
                            else:
                                if(frame_id not in rx_id[1:]):
                                    rx_id.append(frame_id)
                                    ack_sent = False

                                window_bytes[frame_id * self.data_size:frame_id * self.data_size + len(receive_payload) - 1] = receive_payload[1:]
                            if((len(rx_id) == self.WINDOW_SIZE + 1) or (len(rx_id) == last_window + 2)):
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

                    if((len(rx_id) > 1 and rx_id[-1] == (self.WINDOW_SIZE - 1) and not ack_sent) or (len(rx_id) > 1 and rx_id[-1] == last_window and not ack_sent) and not ack_old):
                        radio_tx.write(bytes(rx_id))
                        ack_sent = True
                        if(self.enable_print):
                            print("Sent ACK: " + str(rx_id))

                    if (ack_old):
                        if(last_packet):
                            rx_id_old = rx_id_old[:last_window + 2]
                        radio_tx.write(bytes(rx_id_old))
                        ack_old = False
                        if(self.enable_print):
                            print("Sent ACK old: " + str(rx_id_old))


                # Once all the window is received correctly, store the packets
                if(len(rx_id) == self.WINDOW_SIZE + 1):
                    frames.extend(bytes(window_bytes))
                    window_old = window
                    if(self.enable_print):
                        print("End of window " + str(window) + ", packet saved")

                if(len(rx_id) == last_window + 2):
                    frames.extend(bytes(window_bytes[:(last_window) * self.data_size + last_packet_size - 1]))
                    window_old = window
                    if(self.enable_print):
                        print("End of window " + str(window) + ", packet saved")

                # If it is the last packet save the txt
                if last_packet and len(rx_id) == last_window + 2:
                    self.led.green()
                    print('Reception complete.')
                    # If we are here it means we received all the frames so we have to uncompress

                    if self.compression:
                        uncompressed_frames = zlib.decompress(bytes(frames))

                        f = open(self.fileout, 'wb')
                        f.write(bytes(uncompressed_frames))
                        f.close()
                        print('File saved with name: ' + self.fileout)
                    else:
                        f = open(self.fileout, 'wb')
                        f.write(bytes(frames))
                        f.close()
                        print('File saved with name: ' + self.fileout)
                    frames = []
                    last_packet = False
                    num_file += 1
                    self.led.off()
                    loop = 0

        print("Finished RX")

    def tx(self):
        print("Starting TX")
        # Start radios
        radio_tx, radio_rx = configure_radios(self.channel1, self.channel2, 1)
        radio_rx.startListening()
        radio_tx.stopListening()

        # Create packets
        packets = self.PM.create_window()

        # Define loop variables
        self.led.violet()

        # We'll have tot_packets/WINDOW_SIZE windows sent, in each window we'll send WINDOW_SIZE packets
        tot_packets = len(packets)
        window_counter = 0
        window = 31

        if(tot_packets % self.WINDOW_SIZE == 0):
            rang = tot_packets // self.WINDOW_SIZE
        else:
            rang = tot_packets // self.WINDOW_SIZE + 1

        for window_counter in range(rang):
            print(window)
            if (tot_packets / self.WINDOW_SIZE - window_counter < 1):
                window = (tot_packets - window_counter * self.WINDOW_SIZE)
                if(self.enable_print):
                    print("Window")
                    print(window)
            if(self.enable_print):
                print("-----------------------------------------------------")
                print("Sending window " + str(window_counter))
            # rx_acks => remaining packets to send
            rx_acks = 0
            # 0 if the receiver has not received the packet, 1 if the receiver has sent ACK
            rx_acks_bools = [0] * window
            timeout = False
            # si ha saltado el timeout o el numbero de acks recibidos es menor que la window size tendra que enviar
            while(rx_acks < window or timeout):
                timeout = False
                for packet_index in range(len(rx_acks_bools)):
                    if(rx_acks_bools[packet_index] == 0):
                        radio_tx.write(packets[window_counter * self.WINDOW_SIZE + packet_index])
                        if(self.enable_print):
                            print("tx packet " + str(window_counter * self.WINDOW_SIZE + packet_index))
                # Once it has sent all the packets in the window it checks the ACK and checks the timeout
                started_waiting_at = self.millis()
                while (not radio_rx.available()) and (not timeout):
                    if (self.millis() - started_waiting_at) > int(self.timeout_time):
                        timeout = True
                        started_waiting_at = self.millis()

                if(timeout):
                    if(self.enable_print):
                        print("Ha saltado el timeout")
                else:
                    # There is sth in the receiver
                    if(self.enable_print):
                        print("I listen to ACK")
                    ack = radio_rx.read(radio_rx.getDynamicPayloadSize())
                    # Some packets are wrong, they will send the ones that are good
                    if(self.enable_print):
                        print("Received ACK = ")
                        print((ack))
                    for ack_idx in ack[1:window + 1]:
                        if(rx_acks_bools[ack_idx] == 0 and ack[0] == window_counter % 2):
                            # It was wrong and not is OK
                            if(self.enable_print):
                                print("Packet " + str(ack_idx) + " correct")
                            rx_acks += 1
                            rx_acks_bools[ack_idx] = 1
                    if(self.enable_print):
                        print("ACKS array")
                        print(rx_acks_bools)
                    wrong_packets = window - rx_acks
                    if(self.enable_print):
                        print("Wrong packets " + str(wrong_packets))

        self.led.off()
        print("Finished TX")
