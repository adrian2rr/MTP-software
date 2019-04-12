import Compression
from sys import argv
import time

payload_size = 32

f = open(argv[1], 'rb')
doc = f.read()
f.close()
blocks = int(argv[2])
full_size = len(doc)
C = Compression.Compression()
C.create_fragments(doc, payload_size, blocks)
print("Document size is: " + str(full_size) + " bytes")
print("Padded document size is: " + str(C.new_file_size) + " bytes")
print("Using: " + str(C.blocks) + " blocks, each of size: " + str(C.block_size) + " bytes")

for level in range(0,10):
	tic = time.process_time()
	C.encode(level)
	toc = time.process_time()
	ten = toc-tic
	t_en = '{0:.3e}'.format(ten)

	tic = time.process_time()
	C.decode(C.compressed_list)
	toc = time.process_time()
	tdec = toc - tic
	t_dec = '{0:.3e}'.format(tdec)
	t_tot = '{0:.3e}'.format(ten + tdec)
	i = 0
	count = 0
	for item in C.compressed_list:
		count += len(item)
		i+=1
	enc_size = "{0:.0f}".format(count)
	perc = "%.2f"%(count/full_size*100)
	C.compressed_list = []
	print("Level: " + str(level) + " Time: (enc-dec)  " + t_en + " - "+ t_dec + " s\tTotal size compressed: " + enc_size + " bytes\tCompression ratio: " + perc + " %")
	print("Total time: " + t_tot + " seconds")
