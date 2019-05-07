import zlib
import crc8
import utils.config


class PacketManager(object):
    def __init__(self):
        super(PacketManager, self).__init__()
        self.config_file = "../configs/config_file.json"
        self.config = utils.config.process_config(self.config_file)
        self.document = self.config.document_path
        self.payload_size = self.config.payload_size

        # self.payload_size = 32
        self.data_size = 31
        self.use_compression = True
        self.window_size = 31
        self.compression_level = 6

    def create(self):
        packets = []
        with open(self.document, 'rb') as doc:
            # data_to_tx are the Bytes to be tx
            data_to_tx = doc.read()


        data_to_tx_compressed = self._compress(data_to_tx)
        fragments = self._fragment_file(data_to_tx_compressed)

        packet_number = len(fragments)

        for frame_id, cf in enumerate(fragments):
            packet = self._create_packet(cf, frame_id, packet_number)
            packets.append(packet)

        return packets

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

    def _generate_crc(self, line):

        crc = crc8.crc8()
        crc.update(line)
        # using digest() to return bites in the format b'\xfb'
        # to get only the hexadecimal value 'fb' use hexdigest()
        return crc.digest()

    def _fragment_file(self, data_to_tx):
        """
        Conform all the packets in a list. One character is equivalent to one byte in python.
        :return: list of fragments
        """
        fragments = [data_to_tx[i: self.data_size + i] for i in range(0, len(data_to_tx), self.data_size)]
        return fragments

    def _compress_fragments(self, fragments):
        """
        Compress each fragmented data using zlib library
        :param fragments:
        :return: list of compressed fragments
        """
        compressed_fragments = [zlib.compress(fragment) for fragment in fragments]
        return compressed_fragments

    def _create_packet(self, compressed_fragment, frame_id, packet_number, crc_fragments="", type_of_frame="data"):
        """
        Header (not type of frame for now --> Network mode si)
        *-------------------------------------------------------------*
        | Type_of_frame-0B | Frame_ID-0B | EOT-1B | Payload_length-0B |
        *-------------------------------------------------------------*
        Payload
        *-------------------------------------------------*
        | Data                                            |
        *-------------------------------------------------*
        CRC
        *----------------*
        | CRC-0B         |
        *----------------*

        """
        # TODO: Rules of ifs so that the correct index is assigned to each flag
        # TODO: Last fragment should include padding
        packet = []
        header = []

        # Compute header parameters
        if(frame_id == packet_number - 1):
            eot = 1
        else:
            eot = 0

        identifier = frame_id % 2

        # Create header
        header = bytes([identifier])
        header += bytes([eot])

        # Append header to data
        packet = header
        packet += compressed_fragment

        return packet

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
        packet = []
        id_in_window = fragment_id % self.window_size

        window_number = 0x00
        if((fragment_id % (2 * self.window_size) >= self.window_size)):
            window_number = 0x40

        eot = 0x00
        if(fragment_id == packet_number - 1):
            eot = 0x80
        # We do the OR so the eot is just the first bit instead of the whole byte
        header = eot | window_number
        header = header | id_in_window
        packet = bytes([header])
        packet += compressed_fragment
        print(len(compressed_fragment))
        print(packet)
        return packet


class PacketManagerAck(object):

    def __init__(self):
        pass

    def create(self):
        ack = bytes([0])
        return ack
