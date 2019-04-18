from huffman import encode, apply, reverse
from collections import Counter
from struct import pack, unpack
from bitarray import bitarray
from io import BytesIO


BSC_HEADER_FLAG = b'bsc\0'


class FrequencyOverflowException(Exception):
    pass


class InvalidFileFormatException(Exception):
    pass


def compress_file(file, target):
    with open(file, 'rb') as i:
        text = i.read()
        with open(target, 'wb') as o:
            for s in compress(text):
                o.write(s)
            o.close()
        i.close()


def decompress_file(file, target):
    with open(file, 'rb') as i:
        text = i.read()
        with open(target, 'wb') as o:
            o.write(decompress(text))
            o.close()
        i.close()


def compress(txt):
    feq = Counter(txt)
    out = apply(encode(feq), txt)

    yield BSC_HEADER_FLAG

    for sym in feq:
        fq = feq[sym]
        if fq < 2**8:
            # Use B
            yield pack('B', 1)
            yield pack('B', fq)
        elif fq < 4**8:
            # Use H
            yield pack('B', 2)
            yield pack('H', fq)
        elif fq < 8**8:
            # Use I
            yield pack('B', 3)
            yield pack('I', fq)
        else:
            raise FrequencyOverflowException("Symbol " + sym + " occurred " + fq + " times, we cannot handle that.")
        yield pack('B', sym)

    yield BSC_HEADER_FLAG
    yield bitarray(out).tobytes()


def decompress(txt):
    buff = BytesIO(memoryview(txt))

    if buff.read(len(BSC_HEADER_FLAG)) != BSC_HEADER_FLAG:
        raise InvalidFileFormatException()

    huff = dict()
    blen = 0

    while True:
        chk = buff.read(len(BSC_HEADER_FLAG))
        if chk == BSC_HEADER_FLAG:
            break
        buff.seek(-len(BSC_HEADER_FLAG), 1)

        fqc, fq = unpack('B', buff.read(1))[0], 0
        if fqc is 0x01:
            fq = unpack('B', buff.read(1))[0]
        elif fqc is 0x02:
            fq = unpack('H', buff.read(2))[0]
        elif fqc is 0x03:
            fq = unpack('I', buff.read(4))[0]
        else:
            raise FrequencyOverflowException()

        sym = unpack('B', buff.read(1))[0]
        blen += fq
        huff[sym] = fq

    buff.close()

    out = bitarray()
    out.frombytes(txt[txt.index(BSC_HEADER_FLAG, len(BSC_HEADER_FLAG))+len(BSC_HEADER_FLAG):])
    return reverse(encode(huff), out, blen)

