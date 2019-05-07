from huffman import encode, apply, reverse
from collections import Counter
from struct import pack, unpack
from bitarray import bitarray
from io import BytesIO
from simplecrypt import encrypt, decrypt, DecryptionException


BSC_HEADER_FLAG = b'bsc\0'
BSC_HEADER_FLAG_PW = b'pbc\0'


class FrequencyOverflowException(Exception):
    """File has char frequency we cannot handle"""
    pass


class InvalidFileFormatException(Exception):
    """File does not contain BSC Header on first 4 bytes"""
    pass


class InvalidPasswordException(Exception):
    """Password is unable to decrypt file"""
    pass


def compress_file(file, target, password=None):
    """Compress file and save to target location"""
    with open(file, 'rb') as i:
        text = i.read()
        with open(target, 'wb') as o:
            if password is None:
                o.write(compress(text))
            else:
                o.write(compress_password(text, password))
            o.close()
        i.close()


def decompress_file(file, target, password=None):
    """Decompress file and save to target location"""
    with open(file, 'rb') as i:
        text = i.read()
        with open(target, 'wb') as o:
            if password is None:
                o.write(decompress(text))
            else:
                o.write(decompress_password(text, password))
            o.close()
        i.close()


def compress_password(txt, password):
    """Compress text with password"""
    con = bytearray()
    con += BSC_HEADER_FLAG_PW
    con += bytes(encrypt(password, bytes(compress(txt))))
    return con


def decompress_password(txt, password):
    """Decompress text with password"""
    buff = BytesIO(memoryview(txt))

    if buff.read(len(BSC_HEADER_FLAG_PW)) != BSC_HEADER_FLAG_PW:
        raise InvalidFileFormatException()

    try:
        return decompress(decrypt(password, buff.read()))
    except DecryptionException:
        raise InvalidPasswordException()


def compress(txt):
    """Compress text with password"""
    con = bytearray()
    feq = Counter(txt)
    out = apply(encode(feq), txt)

    con += BSC_HEADER_FLAG

    for sym in feq:
        fq = feq[sym]
        if fq < 2**8 - 2:
            # Use next Byte to pack small int, first 0x01 and 0x02 are reserved values.
            con += pack('B', fq + 2)
        elif fq < 4**8:
            # Use H
            con += pack('B', 1)
            con += pack('H', fq)
        elif fq < 8**8:
            # Use I
            con += pack('B', 2)
            con += pack('I', fq)
        else:
            raise FrequencyOverflowException("Symbol " + sym + " occurred " + fq + " times, we cannot handle that!")
        con += pack('B', sym)

    con += BSC_HEADER_FLAG
    con += bitarray(out).tobytes()
    return con


def decompress(txt):
    """Decompress text with password"""
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
            fq = unpack('H', buff.read(2))[0]
        elif fqc is 0x02:
            fq = unpack('I', buff.read(4))[0]
        else:
            # Subtract 2 from fqc because first two values are reserved
            fq = fqc - 2

        sym = unpack('B', buff.read(1))[0]
        blen += fq
        huff[sym] = fq

    buff.close()

    out = bitarray()
    # Cut off unnecessary parts
    out.frombytes(txt[txt.index(BSC_HEADER_FLAG, len(BSC_HEADER_FLAG))+len(BSC_HEADER_FLAG):])
    return reverse(encode(huff), out, blen)

