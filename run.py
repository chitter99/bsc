import argparse
import bsc
import os


parser = argparse.ArgumentParser(description='Compress files with our favorite huffman')
parser.add_argument('file', metavar='file', help='Input file to compress or decompress')
parser.add_argument('--out', '-o', dest='out', metavar='file', help='Output file from compression or decompression')
parser.add_argument('--decompress', '-d', dest='decompress',
                    help='Decompress input file', action='store_true', default=False)
parser.add_argument('--password', '-p', dest='pw', metavar='password',
                    help='Password for encryption / decryption', default=None)

args = parser.parse_args()

if args.decompress:
    output = os.path.splitext(args.file)[0]
    if args.out:
        output = args.out
    bsc.decompress_file(args.file, output, args.pw)
else:
    output = os.path.splitext(args.file)[0] + '.bsc'
    if args.out:
        output = args.out
    bsc.compress_file(args.file, output, args.pw)
