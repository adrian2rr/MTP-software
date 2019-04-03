import ctypes

cdef extern from "clib/constants.h":
    ctypedef struct DEVICE_CONFIG:
      char irq_rx
      char irq_tx
      char irq_max
      char crc
      char crc_coding
      char power
      char mode

    ctypedef struct RF_CONFIG:
      char channel
      char con_carrier
      char output_power
      char rate
      char pll

    ctypedef struct STATUS:
      char rx_data
      char tx_data
      char max_retrans

    ctypedef struct FIFO_STATUS:
      char tx_full
      char tx_empty
      char rx_full
      char rx_empty
      char tx_reuse

    ctypedef struct PIPES:
      char pipe0
      char pipe1
      char pipe2
      char pipe3
      char pipe4
      char pipe5

    ctypedef struct AUTO_ACK:
      char pipe0
      char pipe1
      char pipe2
      char pipe3
      char pipe4
      char pipe5

    ctypedef struct FEATURE:
      char dynamic_pay
      char payload_ack
      char no_ack

    ctypedef struct TRANSCIEVER:
      DEVICE_CONFIG device_config
      RF_CONFIG rf_config
      STATUS status
      FIFO_STATUS fifo_status
      PIPES pipes
      AUTO_ACK auto_ack
      FEATURE feature
      char address_width
      char mode

cdef extern from "clib/methods.h":
    TRANSCIEVER system_init(int device, int mode)
    void rx_mode(TRANSCIEVER *transciever)
    void wait_single_message(TRANSCIEVER *transciever, char *rx)
    void print_batch(char *rx, int len)
    void send_single_message(TRANSCIEVER *transciever, char *tx)
    void print_all(TRANSCIEVER *transciever)
    void send_single_message(TRANSCIEVER *transciever, char *tx)
    void rx_mode(TRANSCIEVER *transciever)
    void wait_single_message(TRANSCIEVER *transciever, char *rx)

cdef extern from "clib/spi_connector.h":
    void spi_init()
    void spi_end()

class Device_config:
  def __init__(self, irq_rx = 0x00, irq_tx = 0x00, irq_max = 0x00, crc = 0x01, crc_coding = 0x00, power = 0x00, mode = 0x00):
    self.irq_rx = irq_rx
    self.irq_tx = irq_tx
    self.irq_max = irq_max
    self.crc = crc
    self.crc_coding = crc_coding
    self.power = power
    self.mode = mode

class Rf_config:
  def __init__(self, channel = 0x02, con_carrier = 0x00, output_power = 0x00, rate = 0x00, pll = 0x00):
    self.channel = channel
    self.con_carrier = con_carrier
    self.output_power = output_power
    self.rate = rate
    self.pll = pll

class Status:
  def __init__(self, rx_data = 0x00, tx_data = 0x00, max_retrans = 0x00):
    self.rx_data = rx_data
    self.tx_data = tx_data
    self.max_retrans = max_retrans

class Fifo_status:
  def __init__(self, tx_full = 0x00, tx_empty = 0x00, rx_full = 0x00, rx_empty = 0x00, tx_reuse = 0x00):
    self.tx_full = tx_full
    self.tx_empty = tx_empty
    self.rx_full = rx_full
    self.rx_empty = rx_empty
    self.tx_reuse = tx_reuse

class Pipes:
  def __init__(self, pipe0 = 0x00, pipe1 = 0x00, pipe2 = 0x00, pipe3 = 0x00, pipe4 = 0x00, pipe5 = 0x00):
    self.pipe0 = pipe0
    self.pipe1 = pipe1
    self.pipe2 = pipe2
    self.pipe3 = pipe3
    self.pipe4 = pipe4
    self.pipe5 = pipe5

class Auto_ack:
  def __init__(self, pipe0 = 0x00, pipe1 = 0x00, pipe2 = 0x00, pipe3 = 0x00, pipe4 = 0x00, pipe5 = 0x00):
    self.pipe0 = pipe0
    self.pipe1 = pipe1
    self.pipe2 = pipe2
    self.pipe3 = pipe3
    self.pipe4 = pipe4
    self.pipe5 = pipe5

class Feature:
  def __init__(self, dynamic_pay = 0x00, payload_ack = 0x00, no_ack = 0x00):
    self.dynamic_pay = dynamic_pay
    self.payload_ack = payload_ack
    self.no_ack = no_ack

class Transciever:
  def __init__(self, device, mode):
    self.device_config = Device_config()
    self.rf_config = Rf_config()
    self.status = Status()
    self.fifo_status = Fifo_status()
    self.pipes = Pipes()
    self.auto_ack = Auto_ack()
    self.feature = Feature()
    self.address_width = 0x00
    self.mode = 0x00

    cdef TRANSCIEVER aux

    aux = system_init(device, mode)

    self._get_PYObject(aux)

  def _get_CObject(self):
    cdef TRANSCIEVER aux

    aux.device_config = self.device_config
    aux.rf_config = self.rf_config
    aux.status = self.status
    aux.fifo_status = self.fifo_status
    aux.pipes = self.pipes
    aux.auto_ack = self.auto_ack
    aux.feature = self.feature
    aux.address_width = self.address_width
    aux.mode = self.mode

    return aux

  def _get_PYObject(self, aux : TRANSCIEVER):
    self.device_config = aux.device_config
    self.rf_config = aux.rf_config
    self.status = aux.status
    self.fifo_status = aux.fifo_status
    self.pipes = aux.pipes
    self.auto_ack = aux.auto_ack
    self.feature = aux.feature
    self.address_width = aux.address_width
    self.mode = aux.mode

  def print_info(self):
    cdef TRANSCIEVER aux

    aux = self._get_CObject()

    print_all(&aux)

    self._get_PYObject(aux)

  def py_send_single_message(self, tx : bytes):
    cdef TRANSCIEVER aux

    aux = self._get_CObject()

    send_single_message(&aux, tx)

  def py_rx_mode(self):
    cdef TRANSCIEVER aux

    aux = self._get_CObject()

    rx_mode(&aux)

  def py_wait_single_message(self) -> bytes:
    len = 32

    cdef TRANSCIEVER aux
    cdef char rx[32]

    aux = self._get_CObject()

    wait_single_message(&aux, rx)

    py_bytes = rx[:len]

    return py_bytes


def py_spi_init() -> None:
  spi_init()
  

def py_spi_end() -> None:
  spi_end()
