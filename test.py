from bsc import compress_file, decompress_file
from os import remove, path
from filecmp import cmp
from time import sleep


def test(name, file, out, pw=None):
    compress_file(file, "tmp.bsc", pw)
    decompress_file("tmp.bsc", out, pw)

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
    ["Hello World", "test/text/test.txt", "test/text/test_out.txt", None],
    ["Hello World with Password", "test/text/test.txt", "test/text/test_out.txt", "123456"],
    ["Long Text", "test/text/test_lang.txt", "test/text/test_lang_out.txt", None],
    ["Long Text with Password", "test/text/test_lang.txt", "test/text/test_lang_out.txt", "123456"],
    ["Excel File", "test/binary/test.xlsx", "test/binary/test_out.xlsx", None],
    ["Excel with Password", "test/binary/test.xlsx", "test/binary/test_out.xlsx", "123456"],
    ["Image", "test/images/test.jpg", "test/images/test_out.jpg", None],
    ["Image with Password", "test/images/test.jpg", "test/images/test_out.jpg", "123456"]
]

[test(t[0], t[1], t[2], t[3]) for t in tests]
