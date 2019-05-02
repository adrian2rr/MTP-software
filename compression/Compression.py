import zlib


class Compression(object):

	def __init__(self):
		self.compressed_list = []
		self.decompressed_list = []

	def create_fragments(self, document_string, payload_size, blocks):
		self.doc = document_string
		self.payload_size = payload_size
		self.blocks = blocks
		self.total_file_size = len(self.doc)

		# create padding
		self.padding = b'1'
		for i in range(0,blocks-1):
			self.padding = self.padding + b'0'


		self.padded_doc = self.doc + self.padding
		self.padded_doc_size = len(self.padded_doc)
		self.N = int(self.padded_doc_size/self.payload_size)
		# if read file is not a multiple of 32 cut it
		if(self.padded_doc_size%self.N != 0):
		    self.padded_doc = self.padded_doc[:self.N*self.payload_size]
		    self.new_file_size = len(self.padded_doc)
		else:
		    self.new_file_size = self.total_file_size

		self.block_size = int((self.padded_doc_size)/self.blocks)
		self.fragments = [self.padded_doc[i:i+self.block_size] for i in range(0, self.new_file_size, self.block_size)]


	def encode(self, compression_level):
		for string in self.fragments:
			self.compressed_list.append(zlib.compress(string, compression_level))
		return self.compressed_list

	def decode(self,  compressed_list):
		for string in compressed_list:
			self.decompressed_list.append(zlib.decompress(string))
		return self.decompressed_list

	def print_fragments(self):
		i = 0
		for f in self.fragments:
			print(i)
			print(f)
			print("\n")
			i += 1

	def flush():
		self.decompressed_list = []
		self.compressed_list = []