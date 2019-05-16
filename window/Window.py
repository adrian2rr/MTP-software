import RPi.GPIO as GPIO
import threading
import zlib
import time

from .utils.packet_manager_window import PacketManager
from .utils.radio import Transceiver

channel_tx_base = 60
channel_rx_base = 70
irq_rx = 2


class Node:
    def __init__(self, config, led, role):
        self.config = config
        self.window_size = 31
        self.transmitter = Transceiver.transmitter(config)
        self.receiver = Transceiver.receiver(config)
        GPIO.setup(irq_rx, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.packet_manager = PacketManager(config, self.window_size)
        self.file = []
        self.window = []
        self.tx_packets = []
        self.window_index = 0
        self.role = role
        self.led = led
        self.loop = True
        self.timeout_tx = 0.005
        self.timeout_rx_end = 0.01
        self.timeout = None
        self.last_packet = None
        self.fileout = self.config.out_path + str(round(time.time())) + '.txt'

    def start(self):

        if self.role == 'tx':
            self.led.violet()
            self.channel_tx = channel_tx_base
            self.channel_rx = channel_rx_base
            GPIO.add_event_detect(irq_rx, GPIO.FALLING, callback=self.receiver_tx)
            self.file = self.packet_manager.create_window()
            self.window = self.file[0:self.window_size]
            self.tx_packets = self.window
        else:
            self.led.blue()
            self.channel_tx = channel_rx_base
            self.channel_rx = channel_tx_base
            GPIO.add_event_detect(irq_rx, GPIO.FALLING, callback=self.receiver_rx)
            for i in range(0, self.window_size):
                self.window.append(None)

        self.transmitter.setChannel(self.channel_tx)
        self.receiver.setChannel(self.channel_rx)

        self.receiver.maskIRQ(1, 1, 0)

        self.transmitter.printDetails()
        self.receiver.printDetails()

        self.receiver.startListening()

        while self.loop:

            if self.tx_packets:
                packet = self.tx_packets.pop(0)
                self.transmitter.write(packet)
                if self.role == 'tx' and len(self.tx_packets) == 0:
                    self.timeout = threading.Timer(self.timeout_tx, self.repeat_tx)

        GPIO.remove_event_detect(irq_rx)
        self.led.green()
        time.sleep(4)

    def receiver_rx(self, channel):
        length = self.receiver.getDynamicPayloadSize()
        packet = self.receiver.read(length)
        header = packet[0]
        window_e = 0x40 & header
        frame_id = int(0x3f & header)
        eot = 0x80 & header

        error = False

        if self.timeout:
            self.timeout.cancel()

        if self.last_packet and self.last_packet == packet:
            self.tx_packets.append(bytes([header]))

        else:
            self.last_packet = None

            self.window[frame_id] = packet[1:length]

            for i in range(0, frame_id):
                if not self.window[i]:
                    error = True
                    packet = bytes([i])
                    self.tx_packets.append(packet)

            if not error and window_e:
                self.process_final_window(packet, header, eot)

    def process_final_window(self, packet, header, eot):
        self.last_packet = packet
        self.tx_packets.append(bytes([header]))
        for i in range(0, self.window_size):
            if not self.window[i]:
                break
            self.file.append(self.window[i])

        if eot:
            self.timeout = threading.Timer(self.timeout_rx_end, self.receiver_end)

    def receiver_end(self):

        file_aux = []

        for i in range(0, len(self.file)):
            file_aux += self.file[i]

        uncompressed_frames = zlib.decompress(bytes(file_aux))

        f = open(self.fileout, 'wb')
        f.write(bytes(uncompressed_frames))
        f.close()

        self.loop = False

    def receiver_tx(self, channel):
        length = self.receiver.getDynamicPayloadSize()
        packet = self.receiver.read(length)
        header = packet[0]
        window_e = 0x40 & header
        frame_id = int(0x3f & header)
        eot = 0x80 & header

        if not window_e:
            self.tx_packets.insert(0, self.window[frame_id])

        else:
            self.timeout.cancel()
            self.timeout = None

            if not eot:
                self.window_index += 1
                self.window = self.file[self.window_index * self.window_size:(self.window_index + 1) * self.window_size]
                self.tx_packets = self.window

            else:
                self.loop = False

    def repeat_tx(self):
        self.tx_packets.append(self.window[-1])
