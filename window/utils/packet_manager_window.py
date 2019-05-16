import zlib


class PacketManager(object):
    def __init__(self, config_file, window):
        super(PacketManager, self).__init__()
        self.config = config_file
        self.document = self.config.document_path
        self.data_size = 31
        self.window_size = window
        self.compression_level = 6

    def create_window(self):
        packets = []
        with open(self.document, 'rb') as doc:
            # data_to_tx are the Bytes to be tx
            data_to_tx = doc.read()

        # COMPRESS
        data_to_tx_compressed = self._compress(data_to_tx)
        # FRAGMENT
        fragments = self._fragment_file(data_to_tx_compressed)

        packet_number = len(fragments)

        for fragment_id, cf in enumerate(fragments):
            packet = self._create_packet_window(cf, fragment_id, packet_number)
            packets.append(packet)

        # There could be cases in which the ratio packet_number/win_size is not an integer
        # padding_in_last_window = packet_number % self.window_size
        # # these packets below will not be decoded by the receiver
        # for i in range(packet_number, padding_in_last_window+packet_number):
        #     pad_packet = [0] * self.payload_size
        #     pad_packet = bytes(pad_packet)
        #     packets.append(pad_packet)
        return packets

    def _compress(self, data_to_compress):
        """
        Params: data_to_compress
                level
        Return: A list with bytes to be tx
        """
        return zlib.compress(data_to_compress, self.compression_level)

    def _fragment_file(self, data_to_tx):
        """
        Conform all the packets in a list. One character is equivalent to one byte in python.
        :return: list of fragments
        """
        fragments = [data_to_tx[i: self.data_size + i] for i in range(0, len(data_to_tx), self.data_size)]
        return fragments

    def _create_packet_window(self, compressed_fragment, fragment_id, packet_number):
        """
        Packet structure for window case:
        *-------------------------------------------------------------*
        | X X X X X X X X |                  DATA                     |
        *-------------------------------------------------------------*
        | EOT (1b) - WN (1b) - WIN_ID(6b) |            DATA                     |
        *-------------------------------------------------------------*
        EOT: End of file
        WN: Window Number (0) or (1)
        WIN_ID: 0..64
        Maximum window size = 64
        """
        id_in_window = fragment_id % self.window_size

        window_number = 0x00
        if fragment_id % (2 * self.window_size) >= self.window_size:
            window_number = 0x40

        eot = 0x00
        if fragment_id == packet_number - 1:
            eot = 0x80
        # We do the OR so the eot is just the first bit instead of the whole byte
        header = eot | window_number
        header = header | id_in_window
        packet = bytes([header])
        packet += compressed_fragment
        return packet
