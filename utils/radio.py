from RF24 import *
import RPi.GPIO as GPIO
import spidev

def configure_radios(channel_TX, channel_RX):
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(24, GPIO.OUT)
    GPIO.output(24, 1)
    GPIO.setup(22, GPIO.OUT)
    GPIO.output(22, 1)

    pipe_Tx = [0xe7, 0xe7, 0xe7, 0xe7, 0xe7]
    pipe_Rx = [0xe7, 0xe7, 0xe7, 0xe7, 0xe7]
    payloadSize = 32

    # Initialize radio transceivers
    # radio_tx = RF24(22, 0);
    radio_tx = RF24(24, 29)
    radio_rx = RF24(26, 31)
    #radio_rx = RF24(GPIO, spidev.SpiDev())

    #radio_tx.begin(0, 22)
    #radio_rx.begin(1, 24)
    radio_tx.begin()
    radio_rx.begin()

    # Set the Payload Size to the limit which is 32 bytes
    radio_tx.setPayloadSize(payloadSize)
    radio_rx.setPayloadSize(payloadSize)

    # Set the Radio Channels
    radio_tx.setChannel(channel_TX)
    radio_rx.setChannel(channel_RX)

    # Set configuration power
    radio_tx.setPALevel(RF24.PA_LOW)
    radio_rx.setPALevel(RF24.PA_LOW)

    # Disable auto ACK
    radio_tx.setAutoAck(False)
    radio_rx.setAutoAck(False)
    #radio_tx.enableDynamicPayloads()
    #radio_rx.enableDynamicPayloads()

    # Open writing and reading pipe
    radio_tx.openWritingPipe(pipe_Tx)
    radio_rx.openReadingPipe(0, pipe_Rx)

    #radio_tx.setRetries(5, 15)

    print("Transmitter configuration")
    radio_tx.printDetails()

    print("Receiver configuration")
    radio_rx.printDetails()

    return radio_tx, radio_rx
