import zlib
import crc8


class PacketManager(object):
    def __init__(self, document):
        super(PacketManager, self).__init__()
        self.document = document
        self.payload_size = 32
        self.data_size = 30
        self.use_compression = False

    def create(self):
        packets = []
        with open(self.document, 'rb') as doc:
            data_to_tx = doc.read()

        fragments = self._fragment_file(data_to_tx)
        if self.use_compression:
            compressed_fragments = self._compress_fragments(fragments)
        else:
            compressed_fragments = fragments

        for frame_id, cf in enumerate(compressed_fragments):
            packet = self._create_packet(cf, frame_id)
            packets.append(packet)

        return packets

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

    def _create_packet(self, compressed_fragment, frame_id, crc_fragments="", type_of_frame="data"):
        """
        Header (not type of frame for now --> Network mode si)
        *-------------------------------------------------*
        | Type_of_frame | Frame_ID | EOT | Payload_length |
        *-------------------------------------------------*
        Payload
        *-------------------------------------------------*
        | Data                                            |
        *-------------------------------------------------*
        CRC
        *----------------*
        | CRC            |
        *----------------*
        Header: Type_of_frame (ACK, NACK, DATA), Frame_ID, Payload_length, EOT (End of transmission)
        Payload: Data
        CRC:
        :return:packet
        """
        # TODO: Rules of ifs so that the correct index is assigned to each flag
        # TODO: Last fragment should include padding
        packet = []
        header = []
        if type_of_frame == "data":
            tf = 0
        else:
            tf = 1

        header.append(tf)
        header.append(frame_id)
        payload_length = len(compressed_fragment)
        header.append(payload_length)

        packet.extend(header)
        packet.append(compressed_fragment)
        if crc_fragments != "":
            packet.append(crc_fragments)

        return ''.join(packet)