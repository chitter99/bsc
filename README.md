# bsc
Simple compression algorithm with huffman written in python. Let's be honest, bsc is not really good. Actually it sucks pretty hard compared to zip or other professional standarts. But I don't care because it's my algorithm and I love him like my own child. And who can say he crated it's own compression algorithm (well not really but you get what I mean).

# usage

```
# Simple compression
py run.py helloworld.txt
py run.py -d --out helloworld.txt helloworld.bsc
# Password protected compression
py run.py -p 123456 nudes.jpg
py run.py -d --out nudes.jpg -p 123456 nudes.bsc
```

# test
```
py test.py 
```

