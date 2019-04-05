# MTP-software

## Compression class:

```python
create_fragments(string_document_in_bytes, payload_size, number_of_blocks)
```
Number of blocks must be a factor of the payload size, i.e. if we are usign payload_size = 32 bytes number of blocks = [ 2, 4, 8, 16, 32]

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