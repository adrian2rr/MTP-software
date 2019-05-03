from __future__ import print_function
import time
from RF24 import *

from utils.packet_manager_simple import PacketManager
from utils.radio import configure_radios
from utils.config import get_args, process_config
from utils.ledManager import ledManager

try:
    args = get_args()
    config = process_config(args.config)

except:
    print("missing or invalid arguments")
    exit(0)

millis = lambda: int(round(time.time() * 1000))

print('Quick Mode script! ')

print('TX Role: Ping Out, starting transmission')

# Set led Manager
led = ledManager()
led.red()

# Define comunication parameters
channel_TX = 60
channel_RX = 70
payload_size = config.payload_size

# Start radios
radio_tx, radio_rx = configure_radios(channel_TX, channel_RX,1)
radio_rx.startListening()
radio_tx.stopListening()

# Create packets
packet_manager = PacketManager(config.document_path)
packets = packet_manager.create_window()

#Define loop variables
led.violet()
i=0

# We'll have tot_packets/WINDOW_SIZE windows sent, in each window we'll send WINDOW_SIZE packets
tot_packets = len(packets)
window_counter = 0
WINDOW_SIZE = 32 # TODO: Put in config file

efficient = False
# TODO: to avoid this code mess (below), make classes transmitter and receiver, these ones will have methods like: stop_and_wait(already implemented), sliding_window (this one)
if(not efficient):
    for window_counter in range(tot_packets//WINDOW_SIZE):
        
        # rx_acks => remaining packets to send
        t = time.time()
        rx_acks = 0 # esto de crear la lista asi y aqui no me gusta, habra que cambiarlo, por un contador? --> efficient version
        rx_acks_bools = [0] * WINDOW_SIZE # 0 if the receiver has not received the packet, 1 if the receiver has sent ACK
        elapsed = time.time() - t
        print("Elapsed time = " + str(elapsed))
        timeout = False
        # Start timeout
        
        # si ha saltado el timeout o el numbero de acks recibidos es menor que la window size tendra que enviar 
        while( (rx_acks < WINDOW_SIZE) or (timeout) ): 
            timeout = False
            for packet_index in range(len(rx_acks_bools)):
                if(rx_acks_bools[packet_index] == 0):
                    radio_tx.write(packets[window_counter * WINDOW_SIZE + packet_index])
                    print("tx packet " + str(packet_index))
            # Once it has sent all the packets in the window it checks the ACK and checks the timeout
            started_waiting_at = millis()
            while (not radio_rx.available()) or (not timeout):
                
                if (millis() - started_waiting_at) > int(config.timeout_time):
                    timeout = True
                    started_waiting_at = millis()
                    
            if(timeout):
                print("Ha saltado el timeout")
            else:
                # There is sth in the receiver
                ack = radio_rx.read(radio_rx.getDynamicPayloadSize())
                if(len(ack) == WINDOW_SIZE):
                    # All packets are OK
                    print("ALL PACKETS OK!!!!!!")
                    rx_acks = []
                else:
                    # Some packets are wrong, they will send the ones that are good
                    print("Some packets are wrong")
                    for ack_idx in ack:
                        rx_acks += 1
                        rx_acks_bools[ack_idx] = 1
        window_counter += 1
else: 
    for window_counter in range(tot_packets//WINDOW_SIZE):
        retransmit = False # Se pone a True si hay que retransmitir, ya sea por timeout o por que se lo pide el receptor
        timeout = False # Se pone a True si salta el timeout
        started_waiting_at = millis()

        while(not retransmit):
            for packet_index in range(WINDOW_SIZE):
                radio_tx.write(packets[window_counter * WINDOW_SIZE + packet_index])
            
            
            






led.off()