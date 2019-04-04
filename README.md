# MTP-software

## Compression class:

Usage example:

```python

>>> import Compression
>>> f = open('in1.txt', 'rb')
>>> doc = f.read()
>>> f.close()
>>> c = Compression.Compression()
>>> c.create_fragments(doc, 32, 32)
>>> c.total_file_size
1130740
>>> c.new_file_size
1130720
>>> enc = c.encode(6)
>>> dec = c.decode(c.compressed_list)

```