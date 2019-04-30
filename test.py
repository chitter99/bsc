from bsc import compress_file, decompress_file
from os import remove, path
from filecmp import cmp
from time import sleep


def test(name, file, out):
    compress_file(file, "tmp.bsc")
    decompress_file("tmp.bsc", out)

    bw = "Test " + name + " "
    if cmp(file, out):
        bw += "👍"
    else:
        bw += "👎"

    rate = (path.getsize("tmp.bsc") / path.getsize(file)) * 100 - 100
    bw += " " + str(rate) + " % compression rate "

    if rate < 0:
        bw += "🙂"
    else:
        bw += "😪"

    print(bw)

    remove(out)
    remove("tmp.bsc")

tests = [
    ["Hello World", "test/text/test.txt", "test/text/test_out.txt"],
    ["Long Text", "test/text/test_lang.txt", "test/text/test_lang_out.txt"],
    ["Excel File", "test/binary/test.xlsx", "test/binary/test_out.xlsx"],
    ["Image", "test/images/test.jpg", "test/images/test_out.jpg"],
]

[test(t[0], t[1], t[2]) for t in tests]
