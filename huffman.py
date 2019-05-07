from heapq import heappush, heappop, heapify


def encode(symb2freq):
    """Huffman encode the given dict mapping symbols to weights"""
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


def apply(huff, txt):
    """Encode txt with huffman codes and return string"""
    out = ""
    for c in txt:
        for p in huff:
            if p[0] == c:
                out += p[1]
    return out


def reverse(huff, txt, leng):
    """Decode huffman encoded txt with huffman codes and return with len defined byte array"""
    out = bytearray()
    curr = ""
    for c in txt:
        curr += "1" if c is True else "0"
        for p in huff:
            if curr == p[1]:
                out.append(p[0])
                curr = ""
                if len(out) is leng:
                    return bytes(out)
    return bytes(out)
