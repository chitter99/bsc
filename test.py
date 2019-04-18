from bsc import compress_file, decompress_file

compress_file("test/text/test.txt", "test/text/test.bsc")
decompress_file("test/text/test.bsc", "test/text/test_out.txt")

compress_file("test/text/test_lang.txt", "test/text/test_lang.bsc")
decompress_file("test/text/test_lang.bsc", "test/text/test_lang_out.txt")

compress_file("test/binary/test.xlsx", "test/binary/test.bsc")
decompress_file("test/binary/test.bsc", "test/binary/test_out.xlsx")

compress_file("test/images/test.jpg", "test/images/test.bsc")
decompress_file("test/images/test.bsc", "test/images/test_out.jpg")

