# BSC
Simple compression algorithm with huffman written in python. Let's be honest, bsc is not really good. Actually it sucks pretty hard compared to zip or other professional standarts. But I don't care because it's my algorithm and I love him like my own child. And who can say he crated it's own compression algorithm (well not really but you get what I mean).

# Usage
Simple compression and decompression.
```commandline
py run.py helloworld.txt
py run.py -d --out helloworld.txt helloworld.bsc
```
Password protected compression and decompression.
```commandline
py run.py -p 123456 nudes.jpg
py run.py -d --out nudes.jpg -p 123456 nudes.bsc
```

# Test
```commandline
py test.py 
```

# API Usage
Simple compression and decompression.
```python
from bsc import compress_file, decompress_file

compress_file("myfile.txt", "myfile.bsc")
decompress_file("myfile.bsc", "myfile_out.txt")
```
Password protected compression and decompression.
```python
from bsc import compress_file, decompress_file

compress_file("myfile.txt", "myfile.bsc", 12345)
decompress_file("myfile.bsc", "myfile_out.txt", 12345)
```

# Todo

- [X] Password encrypt files.
- [ ] Compress multiple files into one archive.
