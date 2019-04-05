import chardet

def get_encoding(filename):
    f = open(filename, 'rb')
    doc = f.read()
    f.close()
    return chardet.detect(doc)['encoding']

def convert_encoding(doc_bytes, source_enc, dest_enc):
    return doc_bytes.decode(source_enc).encode(dest_enc)
