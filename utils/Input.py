class Input(object):
    def __init__(self, document):
        super(Input, self).__init__()
        self.document = document

    def create(self):
        packets = []
        file_str = self._read_file()
        fragments = self._fragment_file()
        compressed_fragments= self._compress_fragmnents(fragments)

        for cf in compressed_fragments:
            packet = self._create_packet(cf)
            packets.append(packet)

        return packets

    def _read_file(self):
        with open(self.document, 'r') as doc:
            file_doc = doc.read()

    def _fragment_file(self):
        """

        :return: list of fragments
        """
        fragments = []
        return fragments

    def _compress_fragments(self, fragments):
        """

        :param fragments:
        :return: list of compressed fragments
        """
        compressed_fragments = []
        return compressed_fragments


    def _create_packet(self, compressed_fragment):
        """
        Header: Frame ID, payload_length
        Payload: Data
        CRC:
        :return:packet
        """