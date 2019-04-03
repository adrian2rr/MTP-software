import time
import zlib
from sys import argv

def test_levels(string, level):
    full_size = len(string)
    tic = time.process_time()
    cs = zlib.compress(string, level)
    toc = time.process_time()
    t_en = '{0:.3e}'.format(toc-tic)
    size = len(cs)
    tic = time.process_time()
    s = zlib.decompress(cs)
    toc = time.process_time()    
    t_dec = '{0:.3e}'.format(toc-tic)
    perc = "%.2f"%(size/full_size*100)
    print("Level: " + str(level) + " Time: (enc-dec)  " + t_en + " - "+ t_dec + " s\tSize compressed: " + str(size) + " bytes\tCompression ratio: " + perc + " %")


def test_levels_blocks(blocks, level):
    full_size = int(0)
    t_en = 0
    enc_size = 0
    t_dec = 0
    n = len(blocks)
   
    for string in blocks:
        full_size += len(string)
        #compress        
        tic = time.process_time()
        cs = zlib.compress(string, level)
        toc = time.process_time()
        t_en += toc-tic

        #decompress
        enc_size = enc_size + len(cs)
        tic = time.process_time()
        s = zlib.decompress(cs)
        toc = time.process_time()    
        t_dec = toc-tic


    perc = "%.2f"%(enc_size/full_size*100)
    enc_size = "{0:.2f}".format(enc_size)
    t_tot = '{0:.3e}'.format(t_en + t_dec)
    #averages
    t_en = '{0:.3e}'.format(t_en/n)
    t_dec = '{0:.3e}'.format(t_dec/n)


    print("Level: " + str(level) + " Time: (enc-dec)  " + t_en + " - "+ t_dec + " s\tTotal size compressed: " + enc_size + " bytes\tCompression ratio: " + perc + " %")
    print("Total time: " + t_tot)


f = open(argv[1], "rb")
doc = f.read()
f.close()

total_file_size = len(doc)
N = int(total_file_size/32)
# if read file is not a multiple of 32 cut it
if(total_file_size%N != 0):
    doc = doc[:N]
    new_file_size = N*32
    print("The last block has been cutted")
else:
    new_file_size = total_file_size

# number of bloc(k)s wanted
# should be a power of 2 until 32: 2,4,8,16,32
k = 4
# reading from argv
if(int(argv[2])%2 == 0 and int(argv[2]) <= 32):
    k = int(argv[2])
else:
    print("Number of blocks should be a power of 2 until 32: 2,4,8,16,32")
    print("Using k = " + str(k))

block_size = int((N*32)/k)

fragments = [doc[i:i+block_size] for i in range(0, new_file_size, block_size)]

print("Blocks size is: " + str(block_size) + " bytes - Number of blocks is: " + str(k))
print("Original file size is: " + str(total_file_size) + " bytes")
print("Cutted file size: " + str(new_file_size) + " bytes")
#print("\nEncoding and decoding whole file")
#for l in range(0,10):
#    test_levels(doc, l)

print("\nEncoding and decoding: " + str(k) + " blocks of " + str(block_size) + " bytes each")
print("------AVERAGES-----")
for l in range(0,10):
    test_levels_blocks(fragments, l)




