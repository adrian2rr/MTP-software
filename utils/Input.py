class Input(object):
    def __init__(self, document):
        super(Input, self).__init__()
        self.document = document
        self.payload_size = 32
        self.data_size = self.payload_size

    def create(self):
        packets = []
        with open(self.document, 'rb') as doc:
            data_to_tx = doc.read()

        fragments = self._fragment_file(data_to_tx)
        compressed_fragments = self._compress_fragments(fragments)

        for cf in compressed_fragments:
            packet = self._create_packet(cf)
            packets.append(packet)

        return packets

    def _fragment_file(self, data_to_tx):
        """
        Conform all the packets in a list. One character is equivalent to one byte in python.
        :return: list of fragments
        """
        fragments = [data_to_tx[i: self.data_size+i] for i in range(0, len(data_to_tx), self.data_size)]
        return fragments

    def _compress_fragments(self, fragments):
        """

        :param fragments:
        :return: list of compressed fragments
        """
        # TODO: Implement compression function
        # now returns fragments without compression
        compressed_fragments = fragments
        return compressed_fragments


    def _create_packet(self, compressed_fragment):
        """
        Header
        *-------------------------------------------------*
        | Type_of_frame | Frame_ID | Payload_length | EOT |
        *-------------------------------------------------*

        Payload
        *-------------------------------------------------*
        | Data                                            |
        *-------------------------------------------------*

        CRC
        *----------------*
        | CRC            |
        *----------------*

        Header: Type_of_frame (ACK, DATA), Frame_ID, Payload_length, EOT (End of transmission)
        Payload: Data
        CRC:
        :return:packet
        """

