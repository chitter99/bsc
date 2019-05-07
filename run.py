from colorama import init, Fore, Style
import argparse
import bsc
import os
from threading import Thread
import random


endStr = ["Thanks, come again!", "😊", "© by Michelle Bacher and Aaron Schmid",
          "We <3 Huffman", "provided by Kinderschokolade", "Your advertisement could be here!"]


def compress(file, output, pw):
    """Wrapper for compress function"""
    try:
        bsc.compress_file(file, output, pw)
        print(Fore.GREEN + "Compressed!")
    except bsc.FrequencyOverflowException as err:
        print(err)
    except FileNotFoundError:
        print(Fore.RED + "File not found!")


def decompress(file, output, pw):
    """Wrapper for decompress function"""
    try:
        bsc.decompress_file(file, output, pw)
        print(Fore.GREEN + "Decompressed!")
    except bsc.InvalidPasswordException:
        print(Fore.RED + "Password is invalid!")
    except bsc.InvalidFileFormatException:
        print(Fore.RED + "File not compressed with BSC!")
    except FileNotFoundError:
        print(Fore.RED + "File not found!")


def wheel(text, func, args):
    """Execute func and wait till finished"""
    animation = "|/-\\"
    idx = 0
    thread = Thread(target=func, args=args)
    thread.start()
    while thread.join(0.1) or thread.isAlive():
        print(Fore.WHITE + text + " " + animation[idx % len(animation)], end="\r")
        idx += 1


parser = argparse.ArgumentParser(description='Compress files with our favorite huffman')
parser.add_argument('file', metavar='file', help='Input file to compress or decompress')
parser.add_argument('--out', '-o', dest='out', metavar='file', help='Output file from compression or decompression')
parser.add_argument('--decompress', '-d', dest='decompress',
                    help='Decompress input file', action='store_true', default=False)
parser.add_argument('--password', '-p', dest='pw', metavar='password',
                    help='Password for encryption / decryption', default=None)

args = parser.parse_args()

init()

print(Fore.LIGHTBLACK_EX + Style.DIM + "Welcome to BSC compressor v1.0")

if args.decompress:
    output = os.path.splitext(args.file)[0]
    if args.out:
        output = args.out
    wheel("Decompressing", decompress, (args.file, output, args.pw))
else:
    output = os.path.splitext(args.file)[0] + '.bsc'
    if args.out:
        output = args.out
    wheel("Compressing", compress, (args.file, output, args.pw))

print(Fore.LIGHTBLACK_EX + Style.DIM + random.choice(endStr))